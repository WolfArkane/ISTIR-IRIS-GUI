import sys


def platform_dir() -> str:
    return {"win32" : "windows", "darwin": "macos"}.get(sys.platform, "linux")