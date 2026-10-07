import sys, shutils
from pathlib import Path
from .paths import BIN_DIR

def platform_dir() -> str:
    return {"win32" : "windows", "darwin": "macos"}.get(sys.platform, "linux")