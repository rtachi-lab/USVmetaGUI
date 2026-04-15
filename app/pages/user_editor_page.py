from PySide6.QtCore import Signal
from PySide6.QtWidgets import QFormLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget

from app.i18n import tr
from app.models import UserModel


class UserEditorPage(QWidget):
    save_requested = Signal(object)
    cancel_requested = Signal()

    FIELD_KEYS = [
        ("name_user", "field.name_user"),
        ("first_name_user", "field.first_name_user"),
        ("email_user", "field.email_user"),
        ("unit_user", "field.unit_user"),
        ("institution_user", "field.institution_user"),
        ("address_user", "field.address_user"),
        ("country_user", "field.country_user"),
    ]

    def __init__(self):
        super().__init__()
        self.user_id = None
        self.labels = {}

        layout = QVBoxLayout(self)
        form = QFormLayout()
        form.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.ExpandingFieldsGrow)
        form.setRowWrapPolicy(QFormLayout.RowWrapPolicy.WrapLongRows)

        self.name_user = QLineEdit()
        self.first_name_user = QLineEdit()
        self.email_user = QLineEdit()
        self.unit_user = QLineEdit()
        self.institution_user = QLineEdit()
        self.address_user = QLineEdit()
        self.country_user = QLineEdit()

        for attr_name, key in self.FIELD_KEYS:
            label = QLabel()
            self.labels[key] = label
            form.addRow(label, getattr(self, attr_name))

        row = QHBoxLayout()
        self.cancel_button = QPushButton()
        self.save_button = QPushButton()

        self.cancel_button.clicked.connect(self.cancel_requested.emit)
        self.save_button.clicked.connect(self._emit_save)

        row.addWidget(self.cancel_button)
        row.addWidget(self.save_button)

        layout.addLayout(form)
        layout.addLayout(row)
        layout.addStretch()

        self.apply_language("en")

    def apply_language(self, language: str):
        for key, label in self.labels.items():
            label.setText(tr(language, key))
        self.cancel_button.setText(tr(language, "common.cancel"))
        self.save_button.setText(tr(language, "common.save"))

    def clear_form(self):
        self.user_id = None
        self.name_user.clear()
        self.first_name_user.clear()
        self.email_user.clear()
        self.unit_user.clear()
        self.institution_user.clear()
        self.address_user.clear()
        self.country_user.clear()

    def load_user(self, user: UserModel):
        self.user_id = user.id
        self.name_user.setText(user.name_user or "")
        self.first_name_user.setText(user.first_name_user or "")
        self.email_user.setText(user.email_user or "")
        self.unit_user.setText(user.unit_user or "")
        self.institution_user.setText(user.institution_user or "")
        self.address_user.setText(user.address_user or "")
        self.country_user.setText(user.country_user or "")

    def _emit_save(self):
        user = UserModel(
            id=self.user_id,
            name_user=self.name_user.text().strip() or None,
            first_name_user=self.first_name_user.text().strip() or None,
            email_user=self.email_user.text().strip(),
            unit_user=self.unit_user.text().strip() or None,
            institution_user=self.institution_user.text().strip() or None,
            address_user=self.address_user.text().strip() or None,
            country_user=self.country_user.text().strip() or None,
        )
        self.save_requested.emit(user)
