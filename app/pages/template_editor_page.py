from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QComboBox,
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

from app.i18n import tr
from app.models import ExperimentModel, ProtocolModel, RecordingTemplate, StrainModel, SubjectModel


class TemplateEditorPage(QWidget):
    save_requested = Signal(object)
    cancel_requested = Signal()

    def __init__(self):
        super().__init__()
        self.template_id = None
        self.section_boxes = {}
        self.labels = {}

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
        self.cancel_button = QPushButton()
        self.save_button = QPushButton()

        self.cancel_button.clicked.connect(self.cancel_requested.emit)
        self.save_button.clicked.connect(self._emit_save)

        row.addWidget(self.cancel_button)
        row.addWidget(self.save_button)

        self.content_layout.addLayout(row)
        self.content_layout.addStretch()

        scroll.setWidget(content)
        root.addWidget(scroll)

        self.apply_language("en")

    def _build_meta_section(self):
        box = QGroupBox()
        self.section_boxes["group.template"] = box
        form = QFormLayout(box)
        self._configure_form_layout(form)

        self.template_name = QLineEdit()
        self.default_user_selector = QComboBox()
        self.default_user_selector.addItem("", None)

        self._add_form_row(form, "field.template_name", self.template_name)
        self._add_form_row(form, "field.default_user_id", self.default_user_selector)
        self.content_layout.addWidget(box)

    def _build_experiment_section(self):
        box = QGroupBox()
        self.section_boxes["group.experiment"] = box
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

        for key, widget in [
            ("field.name", self.exp_name),
            ("field.group_subject", self.exp_group_subject),
            ("field.temperature", self.exp_temperature),
            ("field.light_cycle", self.exp_light_cycle),
            ("field.microphone", self.exp_microphone),
            ("field.acquisition_hardware", self.exp_hardware),
            ("field.acquisition_software", self.exp_software),
            ("field.sampling_rate", self.exp_sampling_rate),
            ("field.bit_depth", self.exp_bit_depth),
            ("field.laboratory", self.exp_laboratory),
        ]:
            self._add_form_row(form, key, widget)

        self.content_layout.addWidget(box)

    def _build_protocol_section(self):
        box = QGroupBox()
        self.section_boxes["group.protocol"] = box
        form = QFormLayout(box)
        self._configure_form_layout(form)

        self.protocol_name = QLineEdit()
        self.protocol_number_files = QSpinBox()
        self.protocol_number_files.setMaximum(100000)
        self.protocol_description = QPlainTextEdit()

        for key, widget in [
            ("field.name", self.protocol_name),
            ("field.number_files", self.protocol_number_files),
            ("field.description", self.protocol_description),
        ]:
            self._add_form_row(form, key, widget)

        self.content_layout.addWidget(box)

    def _build_subject_defaults_section(self):
        box = QGroupBox()
        self.section_boxes["group.subject_defaults"] = box
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

        for key, widget in [
            ("field.origin", self.subject_origin),
            ("field.sex", self.subject_sex),
            ("field.group", self.subject_group),
            ("field.genotype", self.subject_genotype),
            ("field.treatment", self.subject_treatment),
            ("field.strain.name", self.strain_name),
            ("field.strain.background", self.strain_background),
            ("field.strain.bibliography", self.strain_bibliography),
        ]:
            self._add_form_row(form, key, widget)

        self.content_layout.addWidget(box)

    def _add_form_row(self, form: QFormLayout, label_key: str, widget: QWidget):
        label = QLabel()
        self.labels.setdefault(label_key, []).append(label)
        form.addRow(label, widget)

    @staticmethod
    def _configure_form_layout(form: QFormLayout):
        form.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.ExpandingFieldsGrow)
        form.setRowWrapPolicy(QFormLayout.RowWrapPolicy.WrapLongRows)

    def apply_language(self, language: str):
        for section_key, box in self.section_boxes.items():
            box.setTitle(tr(language, section_key))
        for key, labels in self.labels.items():
            for label in labels:
                label.setText(tr(language, key))
        self.cancel_button.setText(tr(language, "common.cancel"))
        self.save_button.setText(tr(language, "common.save"))

    def set_users(self, users):
        self.default_user_selector.clear()
        self.default_user_selector.addItem("", None)
        for user in users:
            label = f"{user.name_user or ''} {user.first_name_user or ''} <{user.email_user}>".strip()
            self.default_user_selector.addItem(label, user.id)

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
