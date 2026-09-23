import sys, os, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "libs"))

import webview
from api import Api

html_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "frontend", "index.html")

data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "data.json")
with open(data_path, "r", encoding="utf-8") as f:
    data = json.load(f)
    print(data)

api = Api(None)
window = webview.create_window(
    '{} - {}'.format(data['name'], data['version']),
    html_path,
    js_api=api,
    min_size=(600, 300)
    )

api.start_vpn_watcher()
api._window = window

webview.start(debug=True)