from PySide6.QtCore import Signal
from PySide6.QtWidgets import QLabel, QPushButton, QVBoxLayout, QWidget


class HomePage(QWidget):
    new_record_requested = Signal()
    manage_templates_requested = Signal()
    manage_users_requested = Signal()
    settings_requested = Signal()

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("<h1>USV Meta GUI</h1>"))

        new_button = QPushButton("新規記録を作成")
        template_button = QPushButton("テンプレート管理")
        user_button = QPushButton("ユーザー管理")
        settings_button = QPushButton("設定")

        new_button.clicked.connect(self.new_record_requested.emit)
        template_button.clicked.connect(self.manage_templates_requested.emit)
        user_button.clicked.connect(self.manage_users_requested.emit)
        settings_button.clicked.connect(self.settings_requested.emit)

        layout.addWidget(new_button)
        layout.addWidget(template_button)
        layout.addWidget(user_button)
        layout.addWidget(settings_button)
        layout.addStretch()
