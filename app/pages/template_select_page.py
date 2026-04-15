from PySide6.QtCore import Signal
from PySide6.QtWidgets import QHBoxLayout, QListWidget, QListWidgetItem, QPushButton, QVBoxLayout, QWidget

from app.i18n import tr


class TemplateSelectPage(QWidget):
    back_requested = Signal()
    template_selected = Signal(str)
    empty_record_requested = Signal()

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        self.list_widget = QListWidget()

        button_row = QHBoxLayout()
        self.back_button = QPushButton()
        self.empty_button = QPushButton()
        self.open_button = QPushButton()

        self.back_button.clicked.connect(self.back_requested.emit)
        self.empty_button.clicked.connect(self.empty_record_requested.emit)
        self.open_button.clicked.connect(self._emit_selected)

        button_row.addWidget(self.back_button)
        button_row.addWidget(self.empty_button)
        button_row.addWidget(self.open_button)

        layout.addWidget(self.list_widget)
        layout.addLayout(button_row)

        self.apply_language("en")

    def apply_language(self, language: str):
        self.back_button.setText(tr(language, "common.back"))
        self.empty_button.setText(tr(language, "template.select.empty"))
        self.open_button.setText(tr(language, "template.select.open"))

    def set_templates(self, templates):
        self.list_widget.clear()
        for template in templates:
            item = QListWidgetItem(template.template_name)
            item.setData(256, template.id)
            self.list_widget.addItem(item)

    def _emit_selected(self):
        item = self.list_widget.currentItem()
        if item is not None:
            self.template_selected.emit(item.data(256))
