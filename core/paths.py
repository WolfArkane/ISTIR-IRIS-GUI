from pathlib import Path

# Nuitla recrée l'arborescence
# Il faut indiquer les chemins

BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"
DATA_DIR = BASE_DIR / "data"
BIN_DIR = BASE_DIR / "bin"