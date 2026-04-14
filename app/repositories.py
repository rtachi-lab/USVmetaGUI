import json
import uuid
from dataclasses import asdict
from pathlib import Path

from app.models import (
    AppSettings,
    ExperimentModel,
    ProtocolModel,
    RecordingTemplate,
    StrainModel,
    SubjectModel,
    UserModel,
)


class TemplateRepository:
    def __init__(self, path: Path):
        self.path = path

    def list_all(self) -> list[RecordingTemplate]:
        if not self.path.exists():
            return []

        raw = json.loads(self.path.read_text(encoding="utf-8"))
        items = []

        for item in raw:
            subject_defaults_raw = item.get("subject_defaults", {})
            strain_raw = subject_defaults_raw.get("strain", {})

            subject_defaults = SubjectModel(
                name=subject_defaults_raw.get("name", ""),
                origin=subject_defaults_raw.get("origin"),
                sex=subject_defaults_raw.get("sex"),
                group=subject_defaults_raw.get("group"),
                genotype=subject_defaults_raw.get("genotype"),
                treatment=subject_defaults_raw.get("treatment"),
                strain=StrainModel(
                    name=strain_raw.get("name", ""),
                    background=strain_raw.get("background", ""),
                    bibliography=strain_raw.get("bibliography"),
                ),
            )

            items.append(
                RecordingTemplate(
                    id=item["id"],
                    template_name=item["template_name"],
                    experiment=ExperimentModel(**item.get("experiment", {})),
                    protocol=ProtocolModel(**item.get("protocol", {})),
                    subject_defaults=subject_defaults,
                    default_user_id=item.get("default_user_id"),
                )
            )

        return items

    def save_all(self, templates: list[RecordingTemplate]) -> None:
        payload = [asdict(t) for t in templates]
        self.path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")

    def save(self, template: RecordingTemplate) -> None:
        items = self.list_all()
        updated = False
        for i, item in enumerate(items):
            if item.id == template.id:
                items[i] = template
                updated = True
                break
        if not updated:
            items.append(template)
        self.save_all(items)

    def delete(self, template_id: str) -> None:
        items = [item for item in self.list_all() if item.id != template_id]
        self.save_all(items)

    def get(self, template_id: str) -> RecordingTemplate | None:
        for item in self.list_all():
            if item.id == template_id:
                return item
        return None

    @staticmethod
    def new_id() -> str:
        return str(uuid.uuid4())


class UserRepository:
    def __init__(self, path: Path):
        self.path = path

    def list_all(self) -> list[UserModel]:
        if not self.path.exists():
            return []
        raw = json.loads(self.path.read_text(encoding="utf-8"))
        return [UserModel(**item) for item in raw]

    def save_all(self, users: list[UserModel]) -> None:
        payload = [asdict(u) for u in users]
        self.path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")

    def save(self, user: UserModel) -> None:
        users = self.list_all()
        updated = False
        for i, item in enumerate(users):
            if item.id == user.id:
                users[i] = user
                updated = True
                break
        if not updated:
            users.append(user)
        self.save_all(users)

    def get(self, user_id: str) -> UserModel | None:
        for user in self.list_all():
            if user.id == user_id:
                return user
        return None

    def delete(self, user_id: str) -> None:
        users = [user for user in self.list_all() if user.id != user_id]
        self.save_all(users)

    @staticmethod
    def new_id() -> str:
        return str(uuid.uuid4())


class RecordRepository:
    def __init__(self, records_dir: Path):
        self.records_dir = records_dir

    def save(self, payload: dict, filename: str) -> Path:
        path = self.records_dir / filename
        counter = 1
        while path.exists():
            path = self.records_dir / f"{path.stem}_{counter:03d}{path.suffix}"
            counter += 1

        path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
        return path


class SettingsRepository:
    def __init__(self, path: Path):
        self.path = path

    def load(self) -> AppSettings:
        if not self.path.exists():
            return AppSettings()
        raw = json.loads(self.path.read_text(encoding="utf-8"))
        return AppSettings(**raw)

    def save(self, settings: AppSettings) -> None:
        self.path.write_text(
            json.dumps(asdict(settings), indent=2, ensure_ascii=False),
            encoding="utf-8",
        )


def sanitize_filename_part(text: str) -> str:
    return text.replace(" ", "_").replace("/", "-").replace("\\", "-").replace(":", "-")


def make_filename(payload: dict, pattern: str) -> str:
    experiment = payload.get("experiment", {})
    subject = payload.get("subject", {})
    file_data = payload.get("file", {})

    values = {
        "date": sanitize_filename_part(experiment.get("date") or "unknown-date"),
        "subject": sanitize_filename_part(subject.get("name") or "unknown-subject"),
        "number": file_data.get("number") or 1,
    }

    try:
        filename = pattern.format(**values)
    except KeyError:
        filename = "{date}_{subject}.json".format(**values)

    if not filename.endswith(".json"):
        filename += ".json"

    return filename
