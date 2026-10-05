import sys, os, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "libs"))

import webview
from api import CombinedAPI

html_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "frontend", "index.html")
data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "data.json")
DEFAULT_DATA = {"name": "ISTIR-IRIS", "version": "dev"}

try:
    with open(data_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if "version" not in data or "name" not in data:
        raise ValueError("Fichier data.json incomplet (clé 'name' ou 'version' manquante)")
    print(data)
except (FileNotFoundError, json.JSONDecodeError, ValueError) as e:
    print(f"WARNING: Impossible de charger {data_path} ({e}), utilisation des valeurs par défaut.", flush=True)

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
    min_size=(650, 350)
    )

api.start_vpn_watcher()
api._window = window

webview.start(debug=True, icon=icon_path)