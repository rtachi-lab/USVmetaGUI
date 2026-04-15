import json

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QHBoxLayout, QLabel, QPlainTextEdit, QPushButton, QVBoxLayout, QWidget

from app.i18n import tr


class JsonPreviewPage(QWidget):
    edit_back_requested = Signal()
    save_requested = Signal()

    def __init__(self):
        super().__init__()
        self.payload = None
        self.current_errors: list[str] = []
        self.language = "en"

        layout = QVBoxLayout(self)
        self.error_label = QLabel()
        self.preview = QPlainTextEdit()
        self.preview.setReadOnly(True)

        row = QHBoxLayout()
        self.back_button = QPushButton()
        self.save_button = QPushButton()

        self.back_button.clicked.connect(self.edit_back_requested.emit)
        self.save_button.clicked.connect(self.save_requested.emit)

        row.addWidget(self.back_button)
        row.addWidget(self.save_button)

        layout.addWidget(self.error_label)
        layout.addWidget(self.preview)
        layout.addLayout(row)

        self.apply_language("en")

    def apply_language(self, language: str):
        self.language = language
        self.back_button.setText(tr(language, "preview.back_to_edit"))
        self.save_button.setText(tr(language, "common.save"))
        self._refresh_error_label()

    def set_payload(self, payload: dict, errors: list[str]):
        self.payload = payload
        self.current_errors = errors
        self.preview.setPlainText(json.dumps(payload, indent=2, ensure_ascii=False))
        self._refresh_error_label()

    def _refresh_error_label(self):
        if self.current_errors:
            self.error_label.setText(tr(self.language, "preview.errors", errors="\n".join(self.current_errors)))
        else:
            self.error_label.setText("")
