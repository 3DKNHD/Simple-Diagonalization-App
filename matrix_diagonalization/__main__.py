"""python -m matrix_diagonalization lanza Streamlit."""

from pathlib import Path
import subprocess
import sys


def main() -> None:
    app = Path(__file__).resolve().parent.parent / "app.py"
    raise SystemExit(
        subprocess.call([sys.executable, "-m", "streamlit", "run", str(app)])
    )


if __name__ == "__main__":
    main()
