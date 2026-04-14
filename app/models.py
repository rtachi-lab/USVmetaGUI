from dataclasses import asdict, dataclass, field
from typing import Optional


@dataclass
class StrainModel:
    name: str = ""
    background: str = ""
    bibliography: Optional[str] = None


@dataclass
class SubjectModel:
    name: str = ""
    origin: Optional[str] = None
    sex: Optional[str] = None
    group: Optional[str] = None
    genotype: Optional[str] = None
    treatment: Optional[str] = None
    strain: StrainModel = field(default_factory=StrainModel)


@dataclass
class UserModel:
    id: Optional[str] = None
    name_user: Optional[str] = None
    first_name_user: Optional[str] = None
    email_user: str = ""
    unit_user: Optional[str] = None
    institution_user: Optional[str] = None
    address_user: Optional[str] = None
    country_user: Optional[str] = None


@dataclass
class ProtocolModel:
    name: str = ""
    number_files: Optional[int] = None
    description: str = ""


@dataclass
class ExperimentModel:
    name: str = ""
    group_subject: Optional[str] = None
    date: Optional[str] = None
    temperature: Optional[str] = None
    light_cycle: Optional[str] = None
    microphone: Optional[str] = None
    acquisition_hardware: Optional[str] = None
    acquisition_software: Optional[str] = None
    sampling_rate: Optional[float] = None
    bit_depth: Optional[float] = None
    laboratory: Optional[str] = None


@dataclass
class FileModel:
    name: Optional[str] = None
    number: Optional[int] = None
    link: Optional[str] = None
    notes: Optional[str] = None
    doi: Optional[str] = None


@dataclass
class InteractionPartnerModel:
    name: Optional[str] = None
    sex: Optional[str] = None
    strain: Optional[str] = None
    genotype: Optional[str] = None
    note: Optional[str] = None


@dataclass
class RecordingRecord:
    experiment: ExperimentModel = field(default_factory=ExperimentModel)
    protocol: ProtocolModel = field(default_factory=ProtocolModel)
    subject: SubjectModel = field(default_factory=SubjectModel)
    user: UserModel = field(default_factory=UserModel)
    file: FileModel = field(default_factory=FileModel)
    interaction_partner: InteractionPartnerModel = field(default_factory=InteractionPartnerModel)
    template_id: Optional[str] = None
    template_name: Optional[str] = None


@dataclass
class RecordingTemplate:
    id: str
    template_name: str
    experiment: ExperimentModel = field(default_factory=ExperimentModel)
    protocol: ProtocolModel = field(default_factory=ProtocolModel)
    subject_defaults: SubjectModel = field(default_factory=SubjectModel)
    default_user_id: Optional[str] = None


@dataclass
class AppSettings:
    records_dir: str = ""
    json_filename_pattern: str = "{date}_{subject}.json"


def dataclass_to_dict(obj):
    return asdict(obj)
