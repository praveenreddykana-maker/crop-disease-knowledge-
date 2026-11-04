import sys
import os
import importlib.util
from pathlib import Path

backend_dir = Path(__file__).resolve().parent / "backend"
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

# Load backend/main.py specifically
backend_main_path = backend_dir / "main.py"
spec = importlib.util.spec_from_file_location("backend_main", str(backend_main_path))
backend_main = importlib.util.module_from_spec(spec)
sys.modules["backend_main"] = backend_main
spec.loader.exec_module(backend_main)

app = backend_main.app
