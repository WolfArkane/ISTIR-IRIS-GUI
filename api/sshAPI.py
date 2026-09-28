import threading
import paramiko
from .jsutil import js_string

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
                        self._window.evaluate_js(f"writeToTerminal({js_string(text)})")
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
            self._window.evaluate_js(f"onSftpReady(false, {js_string(e)})")
            return {"status": "error", "message": str(e)}

    def ssh_send_input(self, data):
        if not self._channel:
            return
        try:
            self._channel.send(data)
        except Exception as e:
            print(f"DEBUG ssh_send_input error: {e}", flush=True)

    def ssh_resize(self, cols, rows):
        if not self._channel:
            return
        try:
            self._channel.resize_pty(width=cols, height=rows)
        except Exception as e:
            print(f"DEBUG ssh_resize error: {e}", flush=True)

    def ssh_disconnect(self):
        try:
            if self._channel:
                self._channel.close()
        except Exception as e:
            print(f"DEBUG ssh_disconnect channel error: {e}", flush=True)
        try:
            if self._ssh_client:
                self._ssh_client.close()
        except Exception as e:
            print(f"DEBUG ssh_disconnect client error: {e}", flush=True)