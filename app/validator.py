from app.models import RecordingRecord


class RecordValidator:
    @staticmethod
    def validate(record: RecordingRecord) -> list[str]:
        errors = []

        if not record.experiment.name.strip():
            errors.append("experiment.name is required")
        if not (record.experiment.date or "").strip():
            errors.append("experiment.date is required")
        if not record.protocol.name.strip():
            errors.append("protocol.name is required")
        if not record.subject.name.strip():
            errors.append("subject.name is required")
        if not record.subject.strain.name.strip():
            errors.append("subject.strain.name is required")
        if not record.user.email_user.strip():
            errors.append("user.email_user is required")
        if not (record.file.name or "").strip():
            errors.append("file.name is required")

        return errors
