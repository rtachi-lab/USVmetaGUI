from PySide6.QtCore import Signal
from PySide6.QtWidgets import QHBoxLayout, QListWidget, QListWidgetItem, QPushButton, QVBoxLayout, QWidget

from app.i18n import tr


class TemplateListPage(QWidget):
    back_requested = Signal()
    create_requested = Signal()
    edit_requested = Signal(str)
    duplicate_requested = Signal(str)
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
        self.duplicate_button = QPushButton()
        self.delete_button = QPushButton()

        self.back_button.clicked.connect(self.back_requested.emit)
        self.create_button.clicked.connect(self.create_requested.emit)
        self.edit_button.clicked.connect(self._emit_edit)
        self.duplicate_button.clicked.connect(self._emit_duplicate)
        self.delete_button.clicked.connect(self._emit_delete)

        row.addWidget(self.back_button)
        row.addWidget(self.create_button)
        row.addWidget(self.edit_button)
        row.addWidget(self.duplicate_button)
        row.addWidget(self.delete_button)
        layout.addLayout(row)

        self.apply_language("en")

    def apply_language(self, language: str):
        self.back_button.setText(tr(language, "common.back"))
        self.create_button.setText(tr(language, "template.list.create"))
        self.edit_button.setText(tr(language, "common.edit"))
        self.duplicate_button.setText(tr(language, "common.duplicate"))
        self.delete_button.setText(tr(language, "common.delete"))

    def set_templates(self, templates):
        self.list_widget.clear()
        for template in templates:
            item = QListWidgetItem(template.template_name)
            item.setData(256, template.id)
            self.list_widget.addItem(item)

    def _current_id(self):
        item = self.list_widget.currentItem()
        return item.data(256) if item is not None else None

    def _emit_edit(self):
        current_id = self._current_id()
        if current_id:
            self.edit_requested.emit(current_id)

    def _emit_duplicate(self):
        current_id = self._current_id()
        if current_id:
            self.duplicate_requested.emit(current_id)

    def _emit_delete(self):
        current_id = self._current_id()
        if current_id:
            self.delete_requested.emit(current_id)
