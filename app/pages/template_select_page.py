from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QHBoxLayout,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class TemplateSelectPage(QWidget):
    back_requested = Signal()
    template_selected = Signal(str)
    empty_record_requested = Signal()

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        self.list_widget = QListWidget()

        button_row = QHBoxLayout()
        back_button = QPushButton("戻る")
        empty_button = QPushButton("空で開始")
        open_button = QPushButton("選択して開始")

        back_button.clicked.connect(self.back_requested.emit)
        empty_button.clicked.connect(self.empty_record_requested.emit)
        open_button.clicked.connect(self._emit_selected)

        button_row.addWidget(back_button)
        button_row.addWidget(empty_button)
        button_row.addWidget(open_button)

        layout.addWidget(self.list_widget)
        layout.addLayout(button_row)

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
