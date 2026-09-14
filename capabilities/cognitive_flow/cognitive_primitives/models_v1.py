"""Pure normalization and validation helpers for Cognitive Primitive Layer v1."""

from __future__ import annotations

from typing import Any, Mapping, Tuple

from .types_v1 import COGNITIVE_PRIMITIVE_SCHEMA_VERSION_V1, EvidenceSourceTypeV1


def require_nonempty_text(value: Any, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string")
    return value.strip()


def require_mapping(value: Any, field_name: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise ValueError(f"{field_name} must be a mapping")
    return dict(value)


def normalize_refs(value: Any, field_name: str) -> Tuple[str, ...]:
    if value is None:
        return ()
    if not isinstance(value, (tuple, list)):
        raise ValueError(f"{field_name} must be a sequence of non-empty strings")
    refs = tuple(require_nonempty_text(item, field_name) for item in value)
    return refs


def normalize_schema_version(value: Any) -> str:
    if value is None:
        return COGNITIVE_PRIMITIVE_SCHEMA_VERSION_V1
    version = require_nonempty_text(value, "schema_version")
    if version != COGNITIVE_PRIMITIVE_SCHEMA_VERSION_V1:
        raise ValueError("unsupported cognitive primitive schema_version")
    return version


def normalize_confidence(value: Any) -> float:
    if not isinstance(value, (float, int)) or isinstance(value, bool):
        raise ValueError("confidence must be a number between 0.0 and 1.0")
    confidence = float(value)
    if not 0.0 <= confidence <= 1.0:
        raise ValueError("confidence must be a number between 0.0 and 1.0")
    return confidence


def normalize_evidence_source_type(value: Any) -> str:
    source_type = require_nonempty_text(value, "source_type")
    allowed = {item.value for item in EvidenceSourceTypeV1}
    if source_type not in allowed:
        raise ValueError("source_type is not supported by Evidence Reference v1")
    return source_type

