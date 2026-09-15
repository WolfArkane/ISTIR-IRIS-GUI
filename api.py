import os, json, subprocess, threading, platform, sys, webview, time

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

    def get_salles(self):
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "salles.json")
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)


    def ssh_connect(self, host, username, cols=80, rows=24):
        try:
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

            return {"status": "ok"}
        except Exception as e:
            return {"status": "error", "message": str(e)}


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