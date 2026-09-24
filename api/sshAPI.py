import threading, sys

if sys.platform == "win32":
    from winpty import PtyProcess
else:
    from ptyprocess import PtyProcess

class SshApi:

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

            print('DEBUG: lancement thread SFTP')
            threading.Thread(target=self.connect_sftp, args=(password,), daemon=True).start()

            return {"status": "ok"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def ssh_send_input(self, data):
        if self._proc:
            self._proc.write(data)

    def ssh_resize(self, cols, rows):
        if self._proc:
            self._proc.setwinsize(rows, cols)