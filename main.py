import sys, os, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "libs"))

import webview
from api import CombinedAPI

html_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "frontend", "index.html")
data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "data.json")
with open(data_path, "r", encoding="utf-8") as f:
    data = json.load(f)
    print(data)


if sys.platform == "win32":
    import ctypes
    try:
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(f"wolfarkane.istir_iris.{data['version']}")
    except Exception:
        pass

icon_path = os.path.join(os.path.dirname(__file__), 'frontend', 'assets', 'favicon.ico')

api = CombinedAPI(None)
window = webview.create_window(
    '{} - {}'.format(data['name'], data['version']),
    html_path,
    js_api=api,
    min_size=(600, 300)
    )

api.start_vpn_watcher()
api._window = window

webview.start(debug=False, icon='./frontend/assets/favicon.ico')