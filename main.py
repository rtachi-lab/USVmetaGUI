import shutil
import sys
from pathlib import Path

from PySide6.QtGui import QFont, QIcon
from PySide6.QtWidgets import QApplication

from app.main_window import MainWindow


def prepare_runtime_files(app_dir: Path, bundle_dir: Path) -> Path:
    data_dir = app_dir / "data"
    bundled_data_dir = bundle_dir / "data"

    if bundled_data_dir.exists() and not data_dir.exists():
        shutil.copytree(bundled_data_dir, data_dir)

    data_dir.mkdir(exist_ok=True)
    (data_dir / "records").mkdir(exist_ok=True)

    schema_path = app_dir / "schema.yaml"
    bundled_schema_path = bundle_dir / "schema.yaml"
    if bundled_schema_path.exists() and not schema_path.exists():
        shutil.copy2(bundled_schema_path, schema_path)

    return data_dir


def main() -> int:
    app = QApplication(sys.argv)
    app.setApplicationName("USV Meta GUI")
    app_font = QFont(app.font())
    app_font.setPointSize(app_font.pointSize() + 2)
    app.setFont(app_font)

    if getattr(sys, "frozen", False):
        app_dir = Path(sys.executable).resolve().parent
        bundle_dir = Path(getattr(sys, "_MEIPASS", app_dir))
    else:
        app_dir = Path(__file__).resolve().parent
        bundle_dir = app_dir

    icon_path = app_dir / "assets" / "app.ico"
    bundled_icon_path = bundle_dir / "assets" / "app.ico"
    if bundled_icon_path.exists() and not icon_path.exists():
        icon_path.parent.mkdir(exist_ok=True)
        shutil.copy2(bundled_icon_path, icon_path)
    if icon_path.exists():
        app.setWindowIcon(QIcon(str(icon_path)))

    data_dir = prepare_runtime_files(app_dir, bundle_dir)

    window = MainWindow(data_dir=data_dir)
    window.resize(672, 656)
    window.setMinimumSize(520, 420)
    if icon_path.exists():
        window.setWindowIcon(QIcon(str(icon_path)))
    window.show()

    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
