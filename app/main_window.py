import copy
from pathlib import Path

from PySide6.QtWidgets import QMainWindow, QMessageBox, QStackedWidget

from app.models import AppSettings
from app.pages.home_page import HomePage
from app.pages.json_preview_page import JsonPreviewPage
from app.pages.record_editor_page import RecordEditorPage
from app.pages.save_result_page import SaveResultPage
from app.pages.settings_page import SettingsPage
from app.pages.template_editor_page import TemplateEditorPage
from app.pages.template_list_page import TemplateListPage
from app.pages.template_select_page import TemplateSelectPage
from app.pages.user_editor_page import UserEditorPage
from app.pages.user_list_page import UserListPage
from app.repositories import (
    RecordRepository,
    SettingsRepository,
    TemplateRepository,
    UserRepository,
    make_filename,
)
from app.schema_validator import MouseTubeSchemaValidator
from app.serializer import MouseTubeSerializer
from app.validator import RecordValidator


class MainWindow(QMainWindow):
    def __init__(self, data_dir: Path):
        super().__init__()
        self.setWindowTitle("USV Meta GUI")

        self.data_dir = data_dir
        self.schema_path = data_dir.parent / "schema.yaml"
        self.template_repo = TemplateRepository(data_dir / "templates.json")
        self.user_repo = UserRepository(data_dir / "users.json")
        self.settings_repo = SettingsRepository(data_dir / "settings.json")
        self.settings = self.settings_repo.load()

        if not self.settings.records_dir:
            self.settings.records_dir = str(data_dir / "records")
            self.settings_repo.save(self.settings)

        records_dir = Path(self.settings.records_dir)
        records_dir.mkdir(parents=True, exist_ok=True)
        self.record_repo = RecordRepository(records_dir)

        self.current_record = None
        self.current_payload = None

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.home_page = HomePage()
        self.template_select_page = TemplateSelectPage()
        self.record_editor_page = RecordEditorPage()
        self.preview_page = JsonPreviewPage()
        self.save_result_page = SaveResultPage()
        self.template_list_page = TemplateListPage()
        self.template_editor_page = TemplateEditorPage()
        self.user_list_page = UserListPage()
        self.user_editor_page = UserEditorPage()
        self.settings_page = SettingsPage()

        for page in [
            self.home_page,
            self.template_select_page,
            self.record_editor_page,
            self.preview_page,
            self.save_result_page,
            self.template_list_page,
            self.template_editor_page,
            self.user_list_page,
            self.user_editor_page,
            self.settings_page,
        ]:
            self.stack.addWidget(page)

        self._connect_signals()
        self.show_home()

    def _connect_signals(self):
        self.home_page.new_record_requested.connect(self.show_template_select)
        self.home_page.manage_templates_requested.connect(self.show_template_list)
        self.home_page.manage_users_requested.connect(self.show_user_list)
        self.home_page.settings_requested.connect(self.show_settings)

        self.template_select_page.back_requested.connect(self.show_home)
        self.template_select_page.empty_record_requested.connect(self.start_empty_record)
        self.template_select_page.template_selected.connect(self.start_record_from_template)

        self.record_editor_page.cancel_requested.connect(self.show_home)
        self.record_editor_page.preview_requested.connect(self.show_preview)

        self.preview_page.edit_back_requested.connect(self.back_to_editor)
        self.preview_page.save_requested.connect(self.save_record)

        self.save_result_page.create_next_same_context_requested.connect(self.create_next_same_context)
        self.save_result_page.create_next_same_subject_requested.connect(self.create_next_same_subject)
        self.save_result_page.go_home_requested.connect(self.show_home)

        self.template_list_page.back_requested.connect(self.show_home)
        self.template_list_page.create_requested.connect(self.create_template)
        self.template_list_page.edit_requested.connect(self.edit_template)
        self.template_list_page.duplicate_requested.connect(self.duplicate_template)
        self.template_list_page.delete_requested.connect(self.delete_template)

        self.template_editor_page.cancel_requested.connect(self.show_template_list)
        self.template_editor_page.save_requested.connect(self.save_template)

        self.user_list_page.back_requested.connect(self.show_home)
        self.user_list_page.create_requested.connect(self.create_user)
        self.user_list_page.edit_requested.connect(self.edit_user)
        self.user_list_page.delete_requested.connect(self.delete_user)

        self.user_editor_page.cancel_requested.connect(self.show_user_list)
        self.user_editor_page.save_requested.connect(self.save_user)

        self.settings_page.back_requested.connect(self.show_home)
        self.settings_page.save_requested.connect(self.save_settings)

    def show_home(self):
        self.record_editor_page.clear_validation_errors()
        self.stack.setCurrentWidget(self.home_page)

    def show_template_select(self):
        self.template_select_page.set_templates(self.template_repo.list_all())
        self.stack.setCurrentWidget(self.template_select_page)

    def start_empty_record(self):
        self.record_editor_page.set_users(self.user_repo.list_all())
        self.record_editor_page.clear_form()
        self.stack.setCurrentWidget(self.record_editor_page)

    def start_record_from_template(self, template_id: str):
        template = self.template_repo.get(template_id)
        self.record_editor_page.set_users(self.user_repo.list_all())
        self.record_editor_page.clear_form()
        if template is not None:
            self.record_editor_page.load_template(template)
        self.stack.setCurrentWidget(self.record_editor_page)

    def show_preview(self, record):
        self.current_record = record
        payload = MouseTubeSerializer.serialize(record)
        errors = self._validate_record_and_payload(record, payload)
        self.record_editor_page.show_validation_errors(errors)
        self.current_payload = payload
        self.preview_page.set_payload(payload, errors)
        self.stack.setCurrentWidget(self.preview_page)

    def back_to_editor(self):
        self.stack.setCurrentWidget(self.record_editor_page)

    def save_record(self):
        if self.current_record is None or self.current_payload is None:
            return

        errors = self._validate_record_and_payload(self.current_record, self.current_payload)
        if errors:
            self.record_editor_page.show_validation_errors(errors)
            self.stack.setCurrentWidget(self.record_editor_page)
            QMessageBox.warning(self, "Validation Error", "\n".join(errors))
            return

        filename = make_filename(self.current_payload, self.settings.json_filename_pattern)
        saved_path = self.record_repo.save(self.current_payload, filename)
        self.record_editor_page.clear_validation_errors()
        self.save_result_page.set_saved_path(str(saved_path))
        self.stack.setCurrentWidget(self.save_result_page)

    def create_next_same_context(self):
        if self.current_record is None:
            self.show_template_select()
            return

        next_record = copy.deepcopy(self.current_record)
        next_record.subject.name = ""
        next_record.file.name = None
        next_record.file.number = 1
        next_record.file.link = None
        next_record.file.notes = None
        next_record.file.doi = None
        next_record.interaction_partner.name = None
        next_record.interaction_partner.sex = None
        next_record.interaction_partner.strain = None
        next_record.interaction_partner.genotype = None
        next_record.interaction_partner.note = None

        self.record_editor_page.set_users(self.user_repo.list_all())
        self.record_editor_page.clear_form()
        self.record_editor_page.set_record(next_record)
        self.stack.setCurrentWidget(self.record_editor_page)

    def create_next_same_subject(self):
        if self.current_record is None:
            self.show_template_select()
            return

        next_record = copy.deepcopy(self.current_record)
        current_number = next_record.file.number or 0
        next_record.file.name = None
        next_record.file.number = current_number + 1 if current_number > 0 else 1
        next_record.file.link = None
        next_record.file.notes = None
        next_record.file.doi = None
        next_record.interaction_partner.name = None
        next_record.interaction_partner.sex = None
        next_record.interaction_partner.strain = None
        next_record.interaction_partner.genotype = None
        next_record.interaction_partner.note = None

        self.record_editor_page.set_users(self.user_repo.list_all())
        self.record_editor_page.clear_form()
        self.record_editor_page.set_record(next_record)
        self.stack.setCurrentWidget(self.record_editor_page)

    def show_template_list(self):
        self.template_list_page.set_templates(self.template_repo.list_all())
        self.stack.setCurrentWidget(self.template_list_page)

    def create_template(self):
        self.template_editor_page.clear_form()
        self.template_editor_page.set_users(self.user_repo.list_all())
        self.stack.setCurrentWidget(self.template_editor_page)

    def edit_template(self, template_id: str):
        template = self.template_repo.get(template_id)
        if template is None:
            QMessageBox.warning(self, "Template Error", "Template not found.")
            return
        self.template_editor_page.clear_form()
        self.template_editor_page.set_users(self.user_repo.list_all())
        self.template_editor_page.load_template(template)
        self.stack.setCurrentWidget(self.template_editor_page)

    def save_template(self, template):
        if not template.template_name:
            QMessageBox.warning(self, "Validation Error", "template_name is required")
            return
        if not template.id:
            template.id = self.template_repo.new_id()
        self.template_repo.save(template)
        self.show_template_list()

    def duplicate_template(self, template_id: str):
        template = self.template_repo.get(template_id)
        if template is None:
            QMessageBox.warning(self, "Template Error", "Template not found.")
            return

        duplicated = copy.deepcopy(template)
        duplicated.id = self.template_repo.new_id()
        duplicated.template_name = f"{template.template_name} (copy)"

        self.template_repo.save(duplicated)
        self.show_template_list()

    def delete_template(self, template_id: str):
        template = self.template_repo.get(template_id)
        if template is None:
            QMessageBox.warning(self, "Template Error", "Template not found.")
            return

        reply = QMessageBox.question(self, "Delete Template", f"Delete template '{template.template_name}'?")
        if reply == QMessageBox.StandardButton.Yes:
            self.template_repo.delete(template_id)
            self.show_template_list()

    def show_user_list(self):
        self.user_list_page.set_users(self.user_repo.list_all())
        self.stack.setCurrentWidget(self.user_list_page)

    def create_user(self):
        self.user_editor_page.clear_form()
        self.stack.setCurrentWidget(self.user_editor_page)

    def edit_user(self, user_id: str):
        user = self.user_repo.get(user_id)
        if user is None:
            QMessageBox.warning(self, "User Error", "User not found.")
            return
        self.user_editor_page.clear_form()
        self.user_editor_page.load_user(user)
        self.stack.setCurrentWidget(self.user_editor_page)

    def save_user(self, user):
        if not user.email_user:
            QMessageBox.warning(self, "Validation Error", "email_user is required")
            return
        if not user.id:
            user.id = self.user_repo.new_id()
        self.user_repo.save(user)
        self.show_user_list()

    def delete_user(self, user_id: str):
        user = self.user_repo.get(user_id)
        if user is None:
            QMessageBox.warning(self, "User Error", "User not found.")
            return

        label = f"{user.name_user or ''} {user.first_name_user or ''} <{user.email_user}>".strip()
        reply = QMessageBox.question(self, "Delete User", f"Delete user '{label}'?")
        if reply == QMessageBox.StandardButton.Yes:
            self.user_repo.delete(user_id)
            self.show_user_list()

    def show_settings(self):
        self.settings_page.load_settings(self.settings)
        self.stack.setCurrentWidget(self.settings_page)

    def save_settings(self, settings: AppSettings):
        self.settings = settings
        self.settings_repo.save(settings)

        records_dir = Path(settings.records_dir)
        records_dir.mkdir(parents=True, exist_ok=True)
        self.record_repo = RecordRepository(records_dir)

        self.show_home()

    def _validate_record_and_payload(self, record, payload: dict) -> list[str]:
        errors = RecordValidator.validate(record)
        if self.schema_path.exists():
            errors.extend(MouseTubeSchemaValidator.validate_payload(payload, self.schema_path))
        return errors
