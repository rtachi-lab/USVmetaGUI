from PySide6.QtCore import Signal
from PySide6.QtWidgets import QHBoxLayout, QListWidget, QListWidgetItem, QPushButton, QVBoxLayout, QWidget

from app.i18n import tr


class UserListPage(QWidget):
    back_requested = Signal()
    create_requested = Signal()
    edit_requested = Signal(str)
    delete_requested = Signal(str)

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        self.list_widget = QListWidget()
        layout.addWidget(self.list_widget)

        row = QHBoxLayout()
        self.back_button = QPushButton()
        self.create_button = QPushButton()
        self.edit_button = QPushButton()
        self.delete_button = QPushButton()

        self.back_button.clicked.connect(self.back_requested.emit)
        self.create_button.clicked.connect(self.create_requested.emit)
        self.edit_button.clicked.connect(self._emit_edit)
        self.delete_button.clicked.connect(self._emit_delete)

        row.addWidget(self.back_button)
        row.addWidget(self.create_button)
        row.addWidget(self.edit_button)
        row.addWidget(self.delete_button)
        layout.addLayout(row)

        self.apply_language("en")

    def apply_language(self, language: str):
        self.back_button.setText(tr(language, "common.back"))
        self.create_button.setText(tr(language, "user.list.create"))
        self.edit_button.setText(tr(language, "common.edit"))
        self.delete_button.setText(tr(language, "common.delete"))

    def set_users(self, users):
        self.list_widget.clear()
        for user in users:
            label = f"{user.name_user or ''} {user.first_name_user or ''} <{user.email_user}>".strip()
            item = QListWidgetItem(label)
            item.setData(256, user.id)
            self.list_widget.addItem(item)

    def _current_id(self):
        item = self.list_widget.currentItem()
        return item.data(256) if item is not None else None

    def _emit_edit(self):
        current_id = self._current_id()
        if current_id:
            self.edit_requested.emit(current_id)

    def _emit_delete(self):
        current_id = self._current_id()
        if current_id:
            self.delete_requested.emit(current_id)
