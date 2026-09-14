"""Types for the non-writing A3 Runtime Capability registration candidate v1."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Tuple


RUNTIME_CAPABILITY_REGISTRATION_SCHEMA_VERSION_V1 = (
    "luna.cognitive_analysis.runtime_capability_registration_candidate.v1"
)


@dataclass(frozen=True)
class CognitiveAnalysisRuntimeRegistrationCandidateV1:
    """A candidate only; it is never a Registry record or activation request."""

    capability_id: str
    capability_label: str
    capability_type: str
    capability_owner: str
    lifecycle_state: str
    required_contracts: Tuple[str, ...]
    protocol_dependencies: Tuple[str, ...]
    diagnostics_binding: Tuple[str, ...]
    registry_ref: str
    registry_entry_mapping: Mapping[str, object]
    manifest_schema_status: str
    registry_write_applied: bool
    capability_activation_applied: bool
    permission_grant_applied: bool
    runtime_authorized: bool
    schema_version: str = RUNTIME_CAPABILITY_REGISTRATION_SCHEMA_VERSION_V1
