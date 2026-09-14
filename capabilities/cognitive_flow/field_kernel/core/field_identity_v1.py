"""Field Identity object for the Current World Representation Core v1.

This object describes Field context. It is not a map boundary, a database
record, or an independently admitted fact.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping


FIELD_KERNEL_SCHEMA_VERSION_V1 = "luna.field_kernel.v1"


@dataclass(frozen=True)
class FieldIdentityV1:
    """A bounded cognitive Field and its declared representation context."""

    field_id: str
    field_type: str
    parent_field_ref: str | None
    physical_context: Mapping[str, Any]
    social_context: Mapping[str, Any]
    task_context: Mapping[str, Any]
    provenance: Mapping[str, Any]
    schema_version: str = FIELD_KERNEL_SCHEMA_VERSION_V1
    candidate_only: bool = True
    world_model: bool = False
