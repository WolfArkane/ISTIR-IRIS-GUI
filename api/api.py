import os, json

class Api:
    def __init__(self, window_ref):
        self._window = window_ref
        self._proc = None
        self._sftp = None
        self._sftp_client = None
        self._ssh_client = None
        self._channel = None
        self._host = None
        self._username = None

    def get_salles(self):
        try:
            path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "salles.json")
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"DEBUG get_salles ERROR: {e}", flush=True)
            return {"salles": [], "error": str(e)}