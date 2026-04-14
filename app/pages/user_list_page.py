from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QHBoxLayout,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


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
        back_button = QPushButton("戻る")
        create_button = QPushButton("新規作成")
        edit_button = QPushButton("編集")
        delete_button = QPushButton("削除")

        back_button.clicked.connect(self.back_requested.emit)
        create_button.clicked.connect(self.create_requested.emit)
        edit_button.clicked.connect(self._emit_edit)
        delete_button.clicked.connect(self._emit_delete)

        row.addWidget(back_button)
        row.addWidget(create_button)
        row.addWidget(edit_button)
        row.addWidget(delete_button)
        layout.addLayout(row)

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
