from PySide6.QtCore import Signal
from PySide6.QtWidgets import QLabel, QPushButton, QVBoxLayout, QWidget

from app.i18n import tr


class HomePage(QWidget):
    new_record_requested = Signal()
    manage_templates_requested = Signal()
    manage_users_requested = Signal()
    settings_requested = Signal()

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        self.title_label = QLabel("<h1>USV Meta GUI</h1>")
        layout.addWidget(self.title_label)

        self.new_button = QPushButton()
        self.template_button = QPushButton()
        self.user_button = QPushButton()
        self.settings_button = QPushButton()

        self.new_button.clicked.connect(self.new_record_requested.emit)
        self.template_button.clicked.connect(self.manage_templates_requested.emit)
        self.user_button.clicked.connect(self.manage_users_requested.emit)
        self.settings_button.clicked.connect(self.settings_requested.emit)

        layout.addWidget(self.new_button)
        layout.addWidget(self.template_button)
        layout.addWidget(self.user_button)
        layout.addWidget(self.settings_button)
        layout.addStretch()

        self.apply_language("en")

    def apply_language(self, language: str):
        self.new_button.setText(tr(language, "home.new_record"))
        self.template_button.setText(tr(language, "home.manage_templates"))
        self.user_button.setText(tr(language, "home.manage_users"))
        self.settings_button.setText(tr(language, "home.settings"))
