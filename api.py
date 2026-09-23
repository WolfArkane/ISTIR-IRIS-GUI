import os, json, subprocess, threading, platform, sys, webview, time, stat
import paramiko

if sys.platform == "win32":
    from winpty import PtyProcess
else:
    from ptyprocess import PtyProcess

import psutil, ipaddress
ISTIC_SUBNET = ipaddress.ip_network("148.60.9.0/24")

def is_vpn_connected():
    for iface, addrs in psutil.net_if_addrs().items():
        for addr in addrs:
            if addr.family.name == "AF_INET":
                print(f"DEBUG: interface={iface}, ip={addr.address}")
                try:
                    ip = ipaddress.ip_address(addr.address)
                    if ip in ISTIC_SUBNET:
                        return True
                except ValueError:
                    continue
    return False


class Api:
    def __init__(self, window_ref):
        self._window = window_ref
        self._proc = None
        self._sftp = None
        self._sftp_client = None
        self._host = None
        self._username = None

    def get_salles(self):
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "salles.json")
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)


    def ssh_connect(self, host, username, password, cols=80, rows=24):
        try:
            self._host = host
            self._username = username

            print(f"DEBUG: connexion à {username}@{host} ({cols}x{rows})")
            self._proc = PtyProcess.spawn(["ssh", f"{username}@{host}"], dimensions=(rows, cols))

            def read_loop():
                while True:
                    try:
                        data = self._proc.read(1024)
                    except EOFError:
                        break
                    if not data:
                        break
                    text = data.decode(errors="ignore") if isinstance(data, bytes) else data
                    safe_text = text.replace("\\", "\\\\").replace("`", "\\`")
                    self._window.evaluate_js(f"writeToTerminal(`{safe_text}`)")

            threading.Thread(target=read_loop, daemon=True).start()

            # Connexion SFTP paramiko en parallèle
            print('DEBUG: lancement thread SFTP')
            threading.Thread(target=self._connect_sftp, args=(password,), daemon=True).start()
            
            return {"status": "ok"}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    

    def _connect_sftp(self, password):
        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(self._host, username=self._username, password=password, timeout=10)
            self._sftp_client = client
            self._sftp = client.open_sftp()
            print("DEBUG: SFTP connecté avec succès")
            self._window.evaluate_js("onSftpReady(true)")
        except Exception as e:
            print(f"DEBUG SFTP ERROR : {type(e).__name__}: {e}")
            self._window.evaluate_js(f"onSftpReady(false, `{str(e)}`)")


    def sftp_list_dir(self, path="."):
        if not self._sftp:
            return {"error": "SFTP non connecté"}
        try:
            if path == ".":
                path = self._sftp.normalize(".")
            entries = self._sftp.listdir_attr(path)
            result = sorted([
                {"name": e.filename, "size": e.st_size, "is_dir": stat.S_ISDIR(e.st_mode)}
                for e in entries
            ], key=lambda x: (not x["is_dir"], x["name"].lower()))
            return {"path": path, "entries": result}
        except Exception as e:
            return {"error": str(e)}


    def sftp_download(self, remote_path, filename):
        # On ajoute [0] à la fin pour récupérer la chaîne de caractères dans le tuple
        local_path_tuple = self._window.create_file_dialog(webview.FileDialog.SAVE, save_filename=filename)
        if not local_path_tuple:
            return {"cancelled": True}
    
        local_path = local_path_tuple[0] # Extrait le chemin (str) du tuple

        def run():
            try:
                self._sftp.get(remote_path, local_path, callback=lambda s, t: self._window.evaluate_js(f"onSftpProgress({s},{t})"))
                self._window.evaluate_js("onSftpDone(true)")
            except Exception as e:
                self._window.evaluate_js(f"onSftpDone(false, `{str(e)}`)")

        threading.Thread(target=run, daemon=True).start()
        return {"started": True}



    def sftp_upload(self, remote_dir):
        files = self._window.create_file_dialog(webview.FileDialog.OPEN)
        if not files:
            return {"cancelled": True}
        local_path = files[0]
        remote_path = f"{remote_dir.rstrip('/')}/{os.path.basename(local_path)}"

        def run():
            try:
                self._sftp.put(local_path, remote_path,
                    callback=lambda s, t: self._window.evaluate_js(f"onSftpProgress({s},{t})"))
                self._window.evaluate_js("onSftpDone(true)")
            except Exception as e:
                self._window.evaluate_js(f"onSftpDone(false, `{str(e)}`)")

        threading.Thread(target=run, daemon=True).start()
        return {"started": True}


    def ssh_send_input(self, data):
        if self._proc:
            self._proc.write(data)

    def ssh_resize(self, cols, rows):
        if self._proc:
            self._proc.setwinsize(rows, cols)
    
    def start_vpn_watcher(self):
        def watch():
            last_state = None
            while True:
                connected = is_vpn_connected()
                if connected != last_state:
                    self._window.evaluate_js(f"updateVpnStatus({str(connected).lower()})")
                    last_state = connected
                time.sleep(5)
        threading.Thread(target=watch, daemon=True).start()