from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QFormLayout,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from app.models import UserModel


class UserEditorPage(QWidget):
    save_requested = Signal(object)
    cancel_requested = Signal()

    def __init__(self):
        super().__init__()
        self.user_id = None

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

        form.addRow("name_user", self.name_user)
        form.addRow("first_name_user", self.first_name_user)
        form.addRow("email_user", self.email_user)
        form.addRow("unit_user", self.unit_user)
        form.addRow("institution_user", self.institution_user)
        form.addRow("address_user", self.address_user)
        form.addRow("country_user", self.country_user)

        row = QHBoxLayout()
        cancel_button = QPushButton("キャンセル")
        save_button = QPushButton("保存")

        cancel_button.clicked.connect(self.cancel_requested.emit)
        save_button.clicked.connect(self._emit_save)

        row.addWidget(cancel_button)
        row.addWidget(save_button)

        layout.addLayout(form)
        layout.addLayout(row)
        layout.addStretch()

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
