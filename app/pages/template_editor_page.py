from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QComboBox,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLineEdit,
    QPlainTextEdit,
    QPushButton,
    QScrollArea,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from app.models import ExperimentModel, ProtocolModel, RecordingTemplate, StrainModel, SubjectModel


class TemplateEditorPage(QWidget):
    save_requested = Signal(object)
    cancel_requested = Signal()

    def __init__(self):
        super().__init__()
        self.template_id = None

        root = QVBoxLayout(self)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        content = QWidget()
        self.content_layout = QVBoxLayout(content)

        self._build_meta_section()
        self._build_experiment_section()
        self._build_protocol_section()
        self._build_subject_defaults_section()

        row = QHBoxLayout()
        cancel_button = QPushButton("キャンセル")
        save_button = QPushButton("保存")

        cancel_button.clicked.connect(self.cancel_requested.emit)
        save_button.clicked.connect(self._emit_save)

        row.addWidget(cancel_button)
        row.addWidget(save_button)

        self.content_layout.addLayout(row)
        self.content_layout.addStretch()

        scroll.setWidget(content)
        root.addWidget(scroll)

    def _build_meta_section(self):
        box = QGroupBox("template")
        form = QFormLayout(box)
        self._configure_form_layout(form)

        self.template_name = QLineEdit()
        self.default_user_selector = QComboBox()
        self.default_user_selector.addItem("", None)

        form.addRow("template_name", self.template_name)
        form.addRow("default_user_id", self.default_user_selector)
        self.content_layout.addWidget(box)

    def _build_experiment_section(self):
        box = QGroupBox("experiment")
        form = QFormLayout(box)
        self._configure_form_layout(form)

        self.exp_name = QLineEdit()
        self.exp_group_subject = QLineEdit()
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
        form.addRow("temperature", self.exp_temperature)
        form.addRow("light_cycle", self.exp_light_cycle)
        form.addRow("microphone", self.exp_microphone)
        form.addRow("acquisition_hardware", self.exp_hardware)
        form.addRow("acquisition_software", self.exp_software)
        form.addRow("sampling_rate", self.exp_sampling_rate)
        form.addRow("bit_depth", self.exp_bit_depth)
        form.addRow("laboratory", self.exp_laboratory)

        self.content_layout.addWidget(box)

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

    def _build_subject_defaults_section(self):
        box = QGroupBox("subject_defaults")
        form = QFormLayout(box)
        self._configure_form_layout(form)

        self.subject_origin = QLineEdit()
        self.subject_sex = QComboBox()
        self.subject_sex.addItems(["", "male", "female"])
        self.subject_group = QLineEdit()
        self.subject_genotype = QLineEdit()
        self.subject_treatment = QLineEdit()
        self.strain_name = QLineEdit()
        self.strain_background = QLineEdit()
        self.strain_bibliography = QPlainTextEdit()

        form.addRow("origin", self.subject_origin)
        form.addRow("sex", self.subject_sex)
        form.addRow("group", self.subject_group)
        form.addRow("genotype", self.subject_genotype)
        form.addRow("treatment", self.subject_treatment)
        form.addRow("strain.name", self.strain_name)
        form.addRow("strain.background", self.strain_background)
        form.addRow("strain.bibliography", self.strain_bibliography)

        self.content_layout.addWidget(box)

    def set_users(self, users):
        self.default_user_selector.clear()
        self.default_user_selector.addItem("", None)
        for user in users:
            label = f"{user.name_user or ''} {user.first_name_user or ''} <{user.email_user}>".strip()
            self.default_user_selector.addItem(label, user.id)

    @staticmethod
    def _configure_form_layout(form: QFormLayout):
        form.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.ExpandingFieldsGrow)
        form.setRowWrapPolicy(QFormLayout.RowWrapPolicy.WrapLongRows)

    def load_template(self, template: RecordingTemplate):
        self.template_id = template.id
        self.template_name.setText(template.template_name)

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

        self.default_user_selector.setCurrentIndex(0)
        if template.default_user_id:
            index = self.default_user_selector.findData(template.default_user_id)
            if index >= 0:
                self.default_user_selector.setCurrentIndex(index)

    def clear_form(self):
        self.template_id = None
        self.template_name.clear()
        self.default_user_selector.setCurrentIndex(0)
        self.exp_name.clear()
        self.exp_group_subject.clear()
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
        self.subject_origin.clear()
        self.subject_sex.setCurrentText("")
        self.subject_group.clear()
        self.subject_genotype.clear()
        self.subject_treatment.clear()
        self.strain_name.clear()
        self.strain_background.clear()
        self.strain_bibliography.clear()

    def _emit_save(self):
        template = RecordingTemplate(
            id=self.template_id or "",
            template_name=self.template_name.text().strip(),
            experiment=ExperimentModel(
                name=self.exp_name.text().strip(),
                group_subject=self.exp_group_subject.text().strip() or None,
                temperature=self.exp_temperature.text().strip() or None,
                light_cycle=self.exp_light_cycle.currentText().strip() or None,
                microphone=self.exp_microphone.text().strip() or None,
                acquisition_hardware=self.exp_hardware.text().strip() or None,
                acquisition_software=self.exp_software.text().strip() or None,
                sampling_rate=self.exp_sampling_rate.value() or None,
                bit_depth=self.exp_bit_depth.value() or None,
                laboratory=self.exp_laboratory.toPlainText().strip() or None,
            ),
            protocol=ProtocolModel(
                name=self.protocol_name.text().strip(),
                number_files=self.protocol_number_files.value() or None,
                description=self.protocol_description.toPlainText().strip(),
            ),
            subject_defaults=SubjectModel(
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
            ),
            default_user_id=self.default_user_selector.currentData(),
        )
        self.save_requested.emit(template)
