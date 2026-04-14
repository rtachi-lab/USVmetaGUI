from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QComboBox,
    QFormLayout,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from app.models import AppSettings


class SettingsPage(QWidget):
    save_requested = Signal(object)
    back_requested = Signal()

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        form = QFormLayout()
        form.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.ExpandingFieldsGrow)
        form.setRowWrapPolicy(QFormLayout.RowWrapPolicy.WrapLongRows)

        self.records_dir = QLineEdit()
        self.json_filename_pattern = QComboBox()
        self.json_filename_pattern.setEditable(True)
        self.json_filename_pattern.addItems(
            [
                "{date}_{subject}.json",
                "{date}_{subject}_{number}.json",
            ]
        )

        form.addRow("records_dir", self.records_dir)
        form.addRow("json_filename_pattern", self.json_filename_pattern)

        row = QHBoxLayout()
        back_button = QPushButton("戻る")
        save_button = QPushButton("保存")

        back_button.clicked.connect(self.back_requested.emit)
        save_button.clicked.connect(self._emit_save)

        row.addWidget(back_button)
        row.addWidget(save_button)

        layout.addLayout(form)
        layout.addLayout(row)
        layout.addStretch()

    def load_settings(self, settings: AppSettings):
        self.records_dir.setText(settings.records_dir or "")
        self.json_filename_pattern.setCurrentText(settings.json_filename_pattern or "{date}_{subject}.json")

    def _emit_save(self):
        settings = AppSettings(
            records_dir=self.records_dir.text().strip(),
            json_filename_pattern=self.json_filename_pattern.currentText().strip() or "{date}_{subject}.json",
        )
        self.save_requested.emit(settings)
