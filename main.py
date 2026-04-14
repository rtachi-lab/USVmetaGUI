import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication

from app.main_window import MainWindow


def main() -> int:
    app = QApplication(sys.argv)
    app.setApplicationName("USV Meta GUI")

    base_dir = Path(__file__).resolve().parent
    data_dir = base_dir / "data"
    data_dir.mkdir(exist_ok=True)
    (data_dir / "records").mkdir(exist_ok=True)

    window = MainWindow(data_dir=data_dir)
    window.resize(1100, 800)
    window.show()

    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
