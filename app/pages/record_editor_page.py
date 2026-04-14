from PySide6.QtCore import QDate, Qt, Signal
from PySide6.QtWidgets import (
    QComboBox,
    QDateEdit,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPlainTextEdit,
    QPushButton,
    QScrollArea,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from app.models import (
    ExperimentModel,
    FileModel,
    InteractionPartnerModel,
    ProtocolModel,
    RecordingRecord,
    StrainModel,
    SubjectModel,
    UserModel,
)


class RecordEditorPage(QWidget):
    preview_requested = Signal(object)
    cancel_requested = Signal()

    def __init__(self):
        super().__init__()
        self._users_by_id = {}
        self._validation_widgets = {}

        root = QVBoxLayout(self)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        content = QWidget()
        self.content_layout = QVBoxLayout(content)

        self._build_experiment_section()
        self._build_protocol_section()
        self._build_subject_section()
        self._build_user_section()
        self._build_file_section()
        self._build_interaction_section()
        self._build_validation_summary()

        button_row = QHBoxLayout()
        cancel_button = QPushButton("キャンセル")
        preview_button = QPushButton("JSONプレビュー")
        cancel_button.clicked.connect(self.cancel_requested.emit)
        preview_button.clicked.connect(self._emit_preview)

        button_row.addWidget(cancel_button)
        button_row.addWidget(preview_button)

        self.content_layout.addLayout(button_row)
        self.content_layout.addStretch()

        scroll.setWidget(content)
        root.addWidget(scroll)

        self.clear_form()

    def _build_validation_summary(self):
        self.validation_label = QLabel()
        self.validation_label.setWordWrap(True)
        self.validation_label.hide()
        self.content_layout.addWidget(self.validation_label)

    def _build_experiment_section(self):
        box = QGroupBox("experiment")
        form = QFormLayout(box)
        self._configure_form_layout(form)
        self.exp_name = QLineEdit()
        self.exp_group_subject = QLineEdit()
        self.exp_date = QDateEdit()
        self.exp_date.setCalendarPopup(True)
        self.exp_date.setDisplayFormat("yyyy-MM-dd")
        self.exp_temperature = QLineEdit()
        self.exp_light_cycle = QComboBox()
        self.exp_light_cycle.addItems(["", "day", "night"])
        self.exp_microphone = QLineEdit()
        self.exp_hardware = QLineEdit()
        self.exp_software = QLineEdit()
        self.exp_sampling_rate = QSpinBox()
        self.exp_sampling_rate.setMaximum(1_000_000)
        self.exp_sampling_rate.setSpecialValueText("")
        self.exp_sampling_rate.setSuffix(" Hz")
        self.exp_bit_depth = QSpinBox()
        self.exp_bit_depth.setMaximum(1024)
        self.exp_bit_depth.setSpecialValueText("")
        self.exp_laboratory = QPlainTextEdit()

        form.addRow("name", self.exp_name)
        form.addRow("group_subject", self.exp_group_subject)
        form.addRow("date", self.exp_date)
        form.addRow("temperature", self.exp_temperature)
        form.addRow("light_cycle", self.exp_light_cycle)
        form.addRow("microphone", self.exp_microphone)
        form.addRow("acquisition_hardware", self.exp_hardware)
        form.addRow("acquisition_software", self.exp_software)
        form.addRow("sampling_rate", self.exp_sampling_rate)
        form.addRow("bit_depth", self.exp_bit_depth)
        form.addRow("laboratory", self.exp_laboratory)
        self.content_layout.addWidget(box)
        self._register_validation_widget("experiment.name", self.exp_name)
        self._register_validation_widget("experiment.date", self.exp_date)

    def _build_protocol_section(self):
        box = QGroupBox("protocol")
        form = QFormLayout(box)
        self._configure_form_layout(form)
        self.protocol_name = QLineEdit()
        self.protocol_number_files = QSpinBox()
        self.protocol_number_files.setMaximum(100000)
        self.protocol_description = QPlainTextEdit()
        form.addRow("name", self.protocol_name)
        form.addRow("number_files", self.protocol_number_files)
        form.addRow("description", self.protocol_description)
        self.content_layout.addWidget(box)
        self._register_validation_widget("protocol.name", self.protocol_name)

    def _build_subject_section(self):
        box = QGroupBox("subject")
        form = QFormLayout(box)
        self._configure_form_layout(form)
        self.subject_name = QLineEdit()
        self.subject_origin = QLineEdit()
        self.subject_sex = QComboBox()
        self.subject_sex.addItems(["", "male", "female"])
        self.subject_group = QLineEdit()
        self.subject_genotype = QLineEdit()
        self.subject_treatment = QLineEdit()
        self.strain_name = QLineEdit()
        self.strain_background = QLineEdit()
        self.strain_bibliography = QPlainTextEdit()
        form.addRow("name", self.subject_name)
        form.addRow("origin", self.subject_origin)
        form.addRow("sex", self.subject_sex)
        form.addRow("group", self.subject_group)
        form.addRow("genotype", self.subject_genotype)
        form.addRow("treatment", self.subject_treatment)
        form.addRow("strain.name", self.strain_name)
        form.addRow("strain.background", self.strain_background)
        form.addRow("strain.bibliography", self.strain_bibliography)
        self.content_layout.addWidget(box)
        self._register_validation_widget("subject.name", self.subject_name)
        self._register_validation_widget("subject.strain.name", self.strain_name)

    def _build_user_section(self):
        box = QGroupBox("user")
        form = QFormLayout(box)
        self._configure_form_layout(form)
        self.user_selector = QComboBox()
        self.user_selector.currentIndexChanged.connect(self._apply_selected_user)
        self.user_name = QLineEdit()
        self.user_first_name = QLineEdit()
        self.user_email = QLineEdit()
        self.user_unit = QLineEdit()
        self.user_institution = QLineEdit()
        self.user_address = QLineEdit()
        self.user_country = QLineEdit()
        form.addRow("preset", self.user_selector)
        form.addRow("name_user", self.user_name)
        form.addRow("first_name_user", self.user_first_name)
        form.addRow("email_user", self.user_email)
        form.addRow("unit_user", self.user_unit)
        form.addRow("institution_user", self.user_institution)
        form.addRow("address_user", self.user_address)
        form.addRow("country_user", self.user_country)
        self.content_layout.addWidget(box)
        self._register_validation_widget("user.email_user", self.user_email)

    def _build_file_section(self):
        box = QGroupBox("file")
        form = QFormLayout(box)
        self._configure_form_layout(form)
        file_name_row = QHBoxLayout()
        self.file_name = QLineEdit()
        suggest_button = QPushButton("候補を提案")
        suggest_button.clicked.connect(self._suggest_file_name)
        file_name_row.addWidget(self.file_name)
        file_name_row.addWidget(suggest_button)
        file_name_widget = QWidget()
        file_name_widget.setLayout(file_name_row)
        self.file_number = QSpinBox()
        self.file_number.setMaximum(100000)
        self.file_link = QLineEdit()
        self.file_notes = QPlainTextEdit()
        self.file_doi = QLineEdit()
        form.addRow("name", file_name_widget)
        form.addRow("number", self.file_number)
        form.addRow("link", self.file_link)
        form.addRow("notes", self.file_notes)
        form.addRow("doi", self.file_doi)
        self.content_layout.addWidget(box)
        self._register_validation_widget("file.name", self.file_name)

    def _build_interaction_section(self):
        box = QGroupBox("interaction helper")
        form = QFormLayout(box)
        self._configure_form_layout(form)
        self.partner_name = QLineEdit()
        self.partner_sex = QComboBox()
        self.partner_sex.addItems(["", "male", "female"])
        self.partner_strain = QLineEdit()
        self.partner_genotype = QLineEdit()
        self.partner_note = QLineEdit()
        form.addRow("partner name", self.partner_name)
        form.addRow("partner sex", self.partner_sex)
        form.addRow("partner strain", self.partner_strain)
        form.addRow("partner genotype", self.partner_genotype)
        form.addRow("partner note", self.partner_note)
        self.content_layout.addWidget(box)

    def set_users(self, users):
        self._users_by_id = {user.id: user for user in users if user.id}
        self.user_selector.blockSignals(True)
        self.user_selector.clear()
        self.user_selector.addItem("", None)
        for user in users:
            label = f"{user.name_user or ''} {user.first_name_user or ''} <{user.email_user}>".strip()
            self.user_selector.addItem(label, user.id)
        self.user_selector.blockSignals(False)

    def _apply_selected_user(self):
        user_id = self.user_selector.currentData()
        if not user_id:
            return
        user = self._users_by_id.get(user_id)
        if not user:
            return
        self.user_name.setText(user.name_user or "")
        self.user_first_name.setText(user.first_name_user or "")
        self.user_email.setText(user.email_user or "")
        self.user_unit.setText(user.unit_user or "")
        self.user_institution.setText(user.institution_user or "")
        self.user_address.setText(user.address_user or "")
        self.user_country.setText(user.country_user or "")

    def apply_user_by_id(self, user_id: str | None):
        if not user_id:
            return
        index = self.user_selector.findData(user_id)
        if index >= 0:
            self.user_selector.setCurrentIndex(index)
            self._apply_selected_user()

    def clear_form(self):
        self.clear_validation_errors()
        self.exp_name.clear()
        self.exp_group_subject.clear()
        self.exp_date.setDate(QDate.currentDate())
        self.exp_temperature.clear()
        self.exp_light_cycle.setCurrentText("")
        self.exp_microphone.clear()
        self.exp_hardware.clear()
        self.exp_software.clear()
        self.exp_sampling_rate.setValue(0)
        self.exp_bit_depth.setValue(0)
        self.exp_laboratory.clear()
        self.protocol_name.clear()
        self.protocol_number_files.setValue(0)
        self.protocol_description.clear()
        self.subject_name.clear()
        self.subject_origin.clear()
        self.subject_sex.setCurrentText("")
        self.subject_group.clear()
        self.subject_genotype.clear()
        self.subject_treatment.clear()
        self.strain_name.clear()
        self.strain_background.clear()
        self.strain_bibliography.clear()
        self.user_selector.setCurrentIndex(0)
        self.user_name.clear()
        self.user_first_name.clear()
        self.user_email.clear()
        self.user_unit.clear()
        self.user_institution.clear()
        self.user_address.clear()
        self.user_country.clear()
        self.file_name.clear()
        self.file_number.setValue(0)
        self.file_link.clear()
        self.file_notes.clear()
        self.file_doi.clear()
        self.partner_name.clear()
        self.partner_sex.setCurrentText("")
        self.partner_strain.clear()
        self.partner_genotype.clear()
        self.partner_note.clear()

    def load_template(self, template):
        self.clear_validation_errors()
        self.exp_name.setText(template.experiment.name or "")
        self.exp_group_subject.setText(template.experiment.group_subject or "")
        self.exp_temperature.setText(template.experiment.temperature or "")
        self.exp_light_cycle.setCurrentText(template.experiment.light_cycle or "")
        self.exp_microphone.setText(template.experiment.microphone or "")
        self.exp_hardware.setText(template.experiment.acquisition_hardware or "")
        self.exp_software.setText(template.experiment.acquisition_software or "")
        self.exp_sampling_rate.setValue(template.experiment.sampling_rate or 0)
        self.exp_bit_depth.setValue(template.experiment.bit_depth or 0)
        self.exp_laboratory.setPlainText(template.experiment.laboratory or "")
        self.protocol_name.setText(template.protocol.name or "")
        self.protocol_number_files.setValue(template.protocol.number_files or 0)
        self.protocol_description.setPlainText(template.protocol.description or "")
        self.subject_origin.setText(template.subject_defaults.origin or "")
        self.subject_sex.setCurrentText(template.subject_defaults.sex or "")
        self.subject_group.setText(template.subject_defaults.group or "")
        self.subject_genotype.setText(template.subject_defaults.genotype or "")
        self.subject_treatment.setText(template.subject_defaults.treatment or "")
        self.strain_name.setText(template.subject_defaults.strain.name or "")
        self.strain_background.setText(template.subject_defaults.strain.background or "")
        self.strain_bibliography.setPlainText(template.subject_defaults.strain.bibliography or "")
        self.apply_user_by_id(template.default_user_id)

    def set_record(self, record: RecordingRecord):
        self.clear_validation_errors()
        self.exp_name.setText(record.experiment.name or "")
        self.exp_group_subject.setText(record.experiment.group_subject or "")
        if record.experiment.date:
            date = QDate.fromString(record.experiment.date, "yyyy-MM-dd")
            if date.isValid():
                self.exp_date.setDate(date)
        self.exp_temperature.setText(record.experiment.temperature or "")
        self.exp_light_cycle.setCurrentText(record.experiment.light_cycle or "")
        self.exp_microphone.setText(record.experiment.microphone or "")
        self.exp_hardware.setText(record.experiment.acquisition_hardware or "")
        self.exp_software.setText(record.experiment.acquisition_software or "")
        self.exp_sampling_rate.setValue(record.experiment.sampling_rate or 0)
        self.exp_bit_depth.setValue(record.experiment.bit_depth or 0)
        self.exp_laboratory.setPlainText(record.experiment.laboratory or "")
        self.protocol_name.setText(record.protocol.name or "")
        self.protocol_number_files.setValue(record.protocol.number_files or 0)
        self.protocol_description.setPlainText(record.protocol.description or "")
        self.subject_name.setText(record.subject.name or "")
        self.subject_origin.setText(record.subject.origin or "")
        self.subject_sex.setCurrentText(record.subject.sex or "")
        self.subject_group.setText(record.subject.group or "")
        self.subject_genotype.setText(record.subject.genotype or "")
        self.subject_treatment.setText(record.subject.treatment or "")
        self.strain_name.setText(record.subject.strain.name or "")
        self.strain_background.setText(record.subject.strain.background or "")
        self.strain_bibliography.setPlainText(record.subject.strain.bibliography or "")
        self.user_name.setText(record.user.name_user or "")
        self.user_first_name.setText(record.user.first_name_user or "")
        self.user_email.setText(record.user.email_user or "")
        self.user_unit.setText(record.user.unit_user or "")
        self.user_institution.setText(record.user.institution_user or "")
        self.user_address.setText(record.user.address_user or "")
        self.user_country.setText(record.user.country_user or "")
        self.file_name.setText(record.file.name or "")
        self.file_number.setValue(record.file.number or 0)
        self.file_link.setText(record.file.link or "")
        self.file_notes.setPlainText(record.file.notes or "")
        self.file_doi.setText(record.file.doi or "")
        self.partner_name.setText(record.interaction_partner.name or "")
        self.partner_sex.setCurrentText(record.interaction_partner.sex or "")
        self.partner_strain.setText(record.interaction_partner.strain or "")
        self.partner_genotype.setText(record.interaction_partner.genotype or "")
        self.partner_note.setText(record.interaction_partner.note or "")

    def collect_record(self) -> RecordingRecord:
        experiment = ExperimentModel(
            name=self.exp_name.text().strip(),
            group_subject=self.exp_group_subject.text().strip() or None,
            date=self.exp_date.date().toString("yyyy-MM-dd"),
            temperature=self.exp_temperature.text().strip() or None,
            light_cycle=self.exp_light_cycle.currentText().strip() or None,
            microphone=self.exp_microphone.text().strip() or None,
            acquisition_hardware=self.exp_hardware.text().strip() or None,
            acquisition_software=self.exp_software.text().strip() or None,
            sampling_rate=self.exp_sampling_rate.value() or None,
            bit_depth=self.exp_bit_depth.value() or None,
            laboratory=self.exp_laboratory.toPlainText().strip() or None,
        )
        protocol = ProtocolModel(
            name=self.protocol_name.text().strip(),
            number_files=self.protocol_number_files.value() or None,
            description=self.protocol_description.toPlainText().strip(),
        )
        subject = SubjectModel(
            name=self.subject_name.text().strip(),
            origin=self.subject_origin.text().strip() or None,
            sex=self.subject_sex.currentText().strip() or None,
            group=self.subject_group.text().strip() or None,
            genotype=self.subject_genotype.text().strip() or None,
            treatment=self.subject_treatment.text().strip() or None,
            strain=StrainModel(
                name=self.strain_name.text().strip(),
                background=self.strain_background.text().strip(),
                bibliography=self.strain_bibliography.toPlainText().strip() or None,
            ),
        )
        user = UserModel(
            name_user=self.user_name.text().strip() or None,
            first_name_user=self.user_first_name.text().strip() or None,
            email_user=self.user_email.text().strip(),
            unit_user=self.user_unit.text().strip() or None,
            institution_user=self.user_institution.text().strip() or None,
            address_user=self.user_address.text().strip() or None,
            country_user=self.user_country.text().strip() or None,
        )
        file_model = FileModel(
            name=self.file_name.text().strip() or self._build_suggested_file_name(),
            number=self.file_number.value() or None,
            link=self.file_link.text().strip() or None,
            notes=self.file_notes.toPlainText().strip() or None,
            doi=self.file_doi.text().strip() or None,
        )
        partner = InteractionPartnerModel(
            name=self.partner_name.text().strip() or None,
            sex=self.partner_sex.currentText().strip() or None,
            strain=self.partner_strain.text().strip() or None,
            genotype=self.partner_genotype.text().strip() or None,
            note=self.partner_note.text().strip() or None,
        )
        return RecordingRecord(
            experiment=experiment,
            protocol=protocol,
            subject=subject,
            user=user,
            file=file_model,
            interaction_partner=partner,
        )

    def _emit_preview(self):
        self.preview_requested.emit(self.collect_record())

    def _register_validation_widget(self, field_name: str, widget: QWidget):
        self._validation_widgets[field_name] = widget

    @staticmethod
    def _configure_form_layout(form: QFormLayout):
        form.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.ExpandingFieldsGrow)
        form.setRowWrapPolicy(QFormLayout.RowWrapPolicy.WrapLongRows)

    def clear_validation_errors(self):
        self.validation_label.clear()
        self.validation_label.hide()
        for widget in self._validation_widgets.values():
            widget.setStyleSheet("")
            widget.setToolTip("")

    def show_validation_errors(self, errors: list[str]):
        self.clear_validation_errors()
        if not errors:
            return

        self.validation_label.setText("\n".join(errors))
        self.validation_label.setStyleSheet("color: #b00020; font-weight: 600;")
        self.validation_label.show()

        highlighted_widget = None
        for error in errors:
            field_name = error.split(" is required", 1)[0]
            widget = self._validation_widgets.get(field_name)
            if widget is None:
                continue
            widget.setStyleSheet("border: 2px solid #b00020;")
            widget.setToolTip(error)
            if highlighted_widget is None:
                highlighted_widget = widget

        if highlighted_widget is not None:
            highlighted_widget.setFocus()

    def _build_suggested_file_name(self) -> str:
        date_text = self.exp_date.date().toString("yyyy-MM-dd")
        subject_text = self.subject_name.text().strip() or "unknown-subject"
        number = self.file_number.value()
        safe_subject = subject_text.replace(" ", "_").replace("/", "-").replace("\\", "-")
        if number > 0:
            return f"{date_text}_{safe_subject}_{number:03d}.wav"
        return f"{date_text}_{safe_subject}.wav"

    def _suggest_file_name(self):
        self.file_name.setText(self._build_suggested_file_name())
