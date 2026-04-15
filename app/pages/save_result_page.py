from PySide6.QtCore import Signal
from PySide6.QtWidgets import QLabel, QPushButton, QVBoxLayout, QWidget

from app.i18n import tr


class SaveResultPage(QWidget):
    create_next_same_context_requested = Signal()
    create_next_same_subject_requested = Signal()
    go_home_requested = Signal()

    def __init__(self):
        super().__init__()
        self.saved_path = ""
        self.language = "en"

        layout = QVBoxLayout(self)
        self.label = QLabel()
        self.same_context_button = QPushButton()
        self.same_subject_button = QPushButton()
        self.home_button = QPushButton()

        self.same_context_button.clicked.connect(self.create_next_same_context_requested.emit)
        self.same_subject_button.clicked.connect(self.create_next_same_subject_requested.emit)
        self.home_button.clicked.connect(self.go_home_requested.emit)

        layout.addWidget(self.label)
        layout.addWidget(self.same_context_button)
        layout.addWidget(self.same_subject_button)
        layout.addWidget(self.home_button)
        layout.addStretch()

        self.apply_language("en")

    def apply_language(self, language: str):
        self.language = language
        self.same_context_button.setText(tr(language, "record.next_same_context"))
        self.same_subject_button.setText(tr(language, "record.next_same_subject"))
        self.home_button.setText(tr(language, "record.home"))
        self._refresh_label(language)

    def set_saved_path(self, path: str):
        self.saved_path = path
        self._refresh_label(self.language)

    def _refresh_label(self, language: str):
        if self.saved_path:
            self.label.setText(f"{tr(language, 'common.saved')}\n{self.saved_path}")
        else:
            self.label.setText(tr(language, "common.saved"))
