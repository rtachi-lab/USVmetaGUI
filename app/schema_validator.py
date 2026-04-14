from __future__ import annotations

from datetime import date
from functools import lru_cache
from pathlib import Path
from urllib.parse import urlparse

import yaml


class MouseTubeSchemaValidator:
    COMPONENT_MAP = {
        "experiment": "Experiment",
        "protocol": "Protocol",
        "subject": "Subject",
        "user": "User",
        "file": "File",
    }

    NESTED_COMPONENT_MAP = {
        ("subject", "strain"): "Strain",
    }

    IGNORED_REQUIRED_FIELDS = {
        "Experiment": {"id", "protocol"},
        "Protocol": {"id", "user"},
        "Subject": {"id", "strain", "user"},
        "Strain": {"id"},
        "User": {"id"},
        "File": {"id", "experiment", "subject"},
    }

    @classmethod
    def validate_payload(cls, payload: dict, schema_path: Path) -> list[str]:
        components = cls._load_components(schema_path)
        errors: list[str] = []

        for section_name, component_name in cls.COMPONENT_MAP.items():
            section_payload = payload.get(section_name)
            if section_payload is None:
                errors.append(f"{section_name} section is missing")
                continue
            errors.extend(
                cls._validate_object(
                    section_payload,
                    component_name,
                    components,
                    path=section_name,
                )
            )

        for (parent_name, child_name), component_name in cls.NESTED_COMPONENT_MAP.items():
            parent_payload = payload.get(parent_name) or {}
            child_payload = parent_payload.get(child_name)
            if child_payload is None:
                errors.append(f"{parent_name}.{child_name} section is missing")
                continue
            errors.extend(
                cls._validate_object(
                    child_payload,
                    component_name,
                    components,
                    path=f"{parent_name}.{child_name}",
                )
            )

        return errors

    @staticmethod
    @lru_cache(maxsize=4)
    def _load_components(schema_path: Path) -> dict:
        raw = yaml.safe_load(schema_path.read_text(encoding="utf-8"))
        return raw.get("components", {}).get("schemas", {})

    @classmethod
    def _validate_object(cls, obj: dict, component_name: str, components: dict, path: str) -> list[str]:
        schema = components.get(component_name, {})
        properties = schema.get("properties", {})
        required = set(schema.get("required", [])) - cls.IGNORED_REQUIRED_FIELDS.get(component_name, set())

        errors: list[str] = []

        for key in required:
            if key not in obj or obj.get(key) is None or (isinstance(obj.get(key), str) and not obj.get(key).strip()):
                errors.append(f"{path}.{key} is required by schema")

        for key, value in obj.items():
            property_schema = properties.get(key)
            if property_schema is None:
                continue
            errors.extend(cls._validate_value(value, property_schema, components, f"{path}.{key}"))

        return errors

    @classmethod
    def _validate_value(cls, value, schema: dict, components: dict, path: str) -> list[str]:
        if value is None:
            if schema.get("nullable"):
                return []
            return [f"{path} must not be null"]

        if "oneOf" in schema:
            one_of_errors = []
            for option in schema["oneOf"]:
                option_errors = cls._validate_value(value, cls._resolve_schema(option, components), components, path)
                if not option_errors:
                    return []
                one_of_errors.extend(option_errors)
            return [f"{path} is not allowed by schema"]

        resolved_schema = cls._resolve_schema(schema, components)
        schema_type = resolved_schema.get("type")
        errors: list[str] = []

        if "enum" in resolved_schema and value not in resolved_schema["enum"]:
            errors.append(f"{path} must be one of {resolved_schema['enum']}")
            return errors

        if schema_type == "string":
            if not isinstance(value, str):
                return [f"{path} must be a string"]
            max_length = resolved_schema.get("maxLength")
            if max_length is not None and len(value) > max_length:
                errors.append(f"{path} must be at most {max_length} characters")
            value_format = resolved_schema.get("format")
            if value_format == "date" and value:
                try:
                    date.fromisoformat(value)
                except ValueError:
                    errors.append(f"{path} must be an ISO date (YYYY-MM-DD)")
            if value_format == "uri" and value:
                parsed = urlparse(value)
                if not parsed.scheme or not parsed.netloc:
                    errors.append(f"{path} must be a valid URI")
            return errors

        if schema_type == "integer":
            if isinstance(value, bool) or not isinstance(value, int):
                return [f"{path} must be an integer"]
            minimum = resolved_schema.get("minimum")
            maximum = resolved_schema.get("maximum")
            if minimum is not None and value < minimum:
                errors.append(f"{path} must be >= {minimum}")
            if maximum is not None and value > maximum:
                errors.append(f"{path} must be <= {maximum}")
            return errors

        if schema_type == "number":
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                return [f"{path} must be a number"]
            return errors

        if schema_type == "boolean":
            if not isinstance(value, bool):
                return [f"{path} must be a boolean"]
            return errors

        if schema_type == "object" and isinstance(value, dict):
            return []

        return errors

    @staticmethod
    def _resolve_schema(schema: dict, components: dict) -> dict:
        if "$ref" in schema:
            ref_name = schema["$ref"].split("/")[-1]
            return components.get(ref_name, {})
        if "allOf" in schema and schema["allOf"]:
            merged: dict = {}
            for part in schema["allOf"]:
                merged.update(MouseTubeSchemaValidator._resolve_schema(part, components))
            return merged
        return schema
