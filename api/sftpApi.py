import os, stat, threading
import webview
import paramiko

class SftpApi:

    def connect_sftp(self, password):
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
        local_path_tuple = self._window.create_file_dialog(webview.FileDialog.SAVE, save_filename=filename)
        if not local_path_tuple:
            return {"cancelled": True}
        local_path = local_path_tuple[0]

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