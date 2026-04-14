import json

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QLabel, QPushButton, QHBoxLayout, QPlainTextEdit, QVBoxLayout, QWidget


class JsonPreviewPage(QWidget):
    edit_back_requested = Signal()
    save_requested = Signal()

    def __init__(self):
        super().__init__()
        self.payload = None

        layout = QVBoxLayout(self)
        self.error_label = QLabel()
        self.preview = QPlainTextEdit()
        self.preview.setReadOnly(True)

        row = QHBoxLayout()
        back_button = QPushButton("戻って修正")
        save_button = QPushButton("保存")

        back_button.clicked.connect(self.edit_back_requested.emit)
        save_button.clicked.connect(self.save_requested.emit)

        row.addWidget(back_button)
        row.addWidget(save_button)

        layout.addWidget(self.error_label)
        layout.addWidget(self.preview)
        layout.addLayout(row)

    def set_payload(self, payload: dict, errors: list[str]):
        self.payload = payload
        self.preview.setPlainText(json.dumps(payload, indent=2, ensure_ascii=False))
        if errors:
            self.error_label.setText("Errors:\n" + "\n".join(errors))
        else:
            self.error_label.setText("")
