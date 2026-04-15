from PySide6.QtCore import Signal
from PySide6.QtWidgets import QComboBox, QFormLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget

from app.i18n import tr
from app.models import AppSettings


class SettingsPage(QWidget):
    save_requested = Signal(object)
    back_requested = Signal()

    def __init__(self):
        super().__init__()
        self.labels = {}

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
        self.language_selector = QComboBox()
        self.language_selector.addItem("English", "en")
        self.language_selector.addItem("Japanese", "ja")

        for key, widget in [
            ("settings.language", self.language_selector),
            ("settings.records_dir", self.records_dir),
            ("settings.filename_pattern", self.json_filename_pattern),
        ]:
            label = QLabel()
            self.labels[key] = label
            form.addRow(label, widget)

        row = QHBoxLayout()
        self.back_button = QPushButton()
        self.save_button = QPushButton()

        self.back_button.clicked.connect(self.back_requested.emit)
        self.save_button.clicked.connect(self._emit_save)

        row.addWidget(self.back_button)
        row.addWidget(self.save_button)

        layout.addLayout(form)
        layout.addLayout(row)
        layout.addStretch()

        self.apply_language("en")

    def apply_language(self, language: str):
        self.labels["settings.language"].setText(tr(language, "settings.language"))
        self.labels["settings.records_dir"].setText(tr(language, "settings.records_dir"))
        self.labels["settings.filename_pattern"].setText(tr(language, "settings.filename_pattern"))
        self.language_selector.setItemText(0, tr(language, "language.en"))
        self.language_selector.setItemText(1, tr(language, "language.ja"))
        self.back_button.setText(tr(language, "common.back"))
        self.save_button.setText(tr(language, "common.save"))

    def load_settings(self, settings: AppSettings):
        self.records_dir.setText(settings.records_dir or "")
        self.json_filename_pattern.setCurrentText(settings.json_filename_pattern or "{date}_{subject}.json")
        index = self.language_selector.findData(settings.language or "en")
        self.language_selector.setCurrentIndex(index if index >= 0 else 0)

    def _emit_save(self):
        settings = AppSettings(
            records_dir=self.records_dir.text().strip(),
            json_filename_pattern=self.json_filename_pattern.currentText().strip() or "{date}_{subject}.json",
            language=self.language_selector.currentData() or "en",
        )
        self.save_requested.emit(settings)
