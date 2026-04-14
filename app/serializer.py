from app.models import RecordingRecord


class MouseTubeSerializer:
    @staticmethod
    def _clean(value):
        if value == "":
            return None
        return value

    @classmethod
    def build_notes(cls, original_notes, partner):
        parts = []
        if original_notes and original_notes.strip():
            parts.append(original_notes.strip())

        partner_values = [partner.name, partner.sex, partner.strain, partner.genotype, partner.note]
        if any(v for v in partner_values):
            text = (
                f"Interaction partner: {partner.name or ''}; "
                f"sex={partner.sex or ''}; "
                f"strain={partner.strain or ''}; "
                f"genotype={partner.genotype or ''}; "
                f"note={partner.note or ''}"
            ).strip()
            parts.append(text)

        merged = "\n".join(parts).strip()
        return merged or None

    @classmethod
    def serialize(cls, record: RecordingRecord) -> dict:
        return {
            "experiment": {
                "name": record.experiment.name,
                "group_subject": cls._clean(record.experiment.group_subject),
                "date": cls._clean(record.experiment.date),
                "temperature": cls._clean(record.experiment.temperature),
                "light_cycle": cls._clean(record.experiment.light_cycle),
                "microphone": cls._clean(record.experiment.microphone),
                "acquisition_hardware": cls._clean(record.experiment.acquisition_hardware),
                "acquisition_software": cls._clean(record.experiment.acquisition_software),
                "sampling_rate": record.experiment.sampling_rate,
                "bit_depth": record.experiment.bit_depth,
                "laboratory": cls._clean(record.experiment.laboratory),
            },
            "protocol": {
                "name": record.protocol.name,
                "number_files": record.protocol.number_files,
                "description": cls._clean(record.protocol.description),
            },
            "subject": {
                "name": record.subject.name,
                "origin": cls._clean(record.subject.origin),
                "sex": cls._clean(record.subject.sex),
                "group": cls._clean(record.subject.group),
                "genotype": cls._clean(record.subject.genotype),
                "treatment": cls._clean(record.subject.treatment),
                "strain": {
                    "name": record.subject.strain.name,
                    "background": cls._clean(record.subject.strain.background),
                    "bibliography": cls._clean(record.subject.strain.bibliography),
                },
            },
            "user": {
                "name_user": cls._clean(record.user.name_user),
                "first_name_user": cls._clean(record.user.first_name_user),
                "email_user": record.user.email_user,
                "unit_user": cls._clean(record.user.unit_user),
                "institution_user": cls._clean(record.user.institution_user),
                "address_user": cls._clean(record.user.address_user),
                "country_user": cls._clean(record.user.country_user),
            },
            "file": {
                "name": cls._clean(record.file.name),
                "number": record.file.number,
                "link": cls._clean(record.file.link),
                "notes": cls.build_notes(record.file.notes, record.interaction_partner),
                "doi": cls._clean(record.file.doi),
            },
        }
