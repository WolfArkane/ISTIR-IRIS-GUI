import threading
import paramiko

class SshApi:

    def ssh_connect(self, host, username, password, cols=80, rows=24, port=22):
        try:
            self._host = host
            self._username = username

            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(host, port=port, username=username, password=password, timeout=10)
            self._ssh_client = client

            self._channel = client.invoke_shell(term="xterm", width=cols, height=rows)

            def read_loop():
                while True:
                    try:
                        data = self._channel.recv(1024)
                        if not data:
                            break
                        text = data.decode(errors="ignore")
                        safe_text = text.replace("\\", "\\\\").replace("`", "\\`")
                        self._window.evaluate_js(f"writeToTerminal(`{safe_text}`)")
                    except Exception as e:
                        print(f"DEBUG ssh read error: {e}")
                        break
                self._window.evaluate_js("onSshClosed()")

            threading.Thread(target=read_loop, daemon=True).start()

            # SFTP sur le même client, pas de reconnexion nécessaire
            self._sftp_client = client
            self._sftp = client.open_sftp()
            self._window.evaluate_js("onSftpReady(true)")

            return {"status": "ok"}
        except Exception as e:
            self._window.evaluate_js(f"onSftpReady(false, `{str(e)}`)")
            return {"status": "error", "message": str(e)}

    def ssh_send_input(self, data):
        if self._channel:
            self._channel.send(data)

    def ssh_resize(self, cols, rows):
        if self._channel:
            self._channel.resize_pty(width=cols, height=rows)

    def ssh_disconnect(self):
        if self._channel:
            self._channel.close()
        if self._ssh_client:
            self._ssh_client.close()