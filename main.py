"""Punto de entrada: lanza la app Streamlit."""

import subprocess
import sys
from pathlib import Path


def main() -> None:
    app = Path(__file__).resolve().parent / "app.py"
    try:
        import streamlit  # noqa: F401
    except ImportError:
        print("Falta Streamlit. Instálalo con:")
        print("  pip install -r requirements.txt")
        print("Luego:")
        print(f"  streamlit run {app}")
        raise SystemExit(1)
    raise SystemExit(
        subprocess.call([sys.executable, "-m", "streamlit", "run", str(app)])
    )


if __name__ == "__main__":
    main()
