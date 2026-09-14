"""Pure lifecycle validation for Current Cognitive Context v1."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Mapping

from .context_types_v1 import (
    CURRENT_COGNITIVE_CONTEXT_SCHEMA_VERSION_V1,
    ContextLifecycleStatusV1,
)


class ContextLifecycleReasonCodeV1(str, Enum):
    TRANSITION_ALLOWED = "context_lifecycle_transition_allowed"
    SOURCE_STATUS_UNSUPPORTED = "context_lifecycle_source_status_unsupported"
    TARGET_STATUS_UNSUPPORTED = "context_lifecycle_target_status_unsupported"
    ARCHIVED_TERMINAL = "context_lifecycle_archived_terminal"
    SUPERSEDED_REACTIVATION_FORBIDDEN = "context_lifecycle_superseded_reactivation_forbidden"
    REQUESTED_ACTIVATION_FORBIDDEN = "context_lifecycle_requested_activation_forbidden"
    BUILT_ARCHIVAL_FORBIDDEN = "context_lifecycle_built_archival_forbidden"
    TRANSITION_FORBIDDEN = "context_lifecycle_transition_forbidden"


@dataclass(frozen=True)
class ContextLifecycleValidationResultV1:
    validation_result: bool
    reason_code: str
    source_status: str
    target_status: str
    provenance: Mapping[str, Any]
    trace: str
    schema_version: str = CURRENT_COGNITIVE_CONTEXT_SCHEMA_VERSION_V1


_ALLOWED_TRANSITIONS_V1 = {
    (ContextLifecycleStatusV1.REQUESTED.value, ContextLifecycleStatusV1.BUILT.value),
    (ContextLifecycleStatusV1.BUILT.value, ContextLifecycleStatusV1.VALIDATED.value),
    (ContextLifecycleStatusV1.VALIDATED.value, ContextLifecycleStatusV1.ACTIVE.value),
    (ContextLifecycleStatusV1.ACTIVE.value, ContextLifecycleStatusV1.REFRESHED.value),
    (ContextLifecycleStatusV1.ACTIVE.value, ContextLifecycleStatusV1.SUPERSEDED.value),
    (ContextLifecycleStatusV1.REFRESHED.value, ContextLifecycleStatusV1.ACTIVE.value),
    (ContextLifecycleStatusV1.REFRESHED.value, ContextLifecycleStatusV1.SUPERSEDED.value),
    (ContextLifecycleStatusV1.SUPERSEDED.value, ContextLifecycleStatusV1.ARCHIVED.value),
}


def validate_context_lifecycle_transition_v1(
    source_status: str,
    target_status: str,
    provenance: Mapping[str, Any],
    trace: str,
) -> ContextLifecycleValidationResultV1:
    """Validate lifecycle progression without reading or modifying Context."""

    statuses = {status.value for status in ContextLifecycleStatusV1}
    result_provenance = dict(provenance)
    if source_status not in statuses:
        return ContextLifecycleValidationResultV1(False, ContextLifecycleReasonCodeV1.SOURCE_STATUS_UNSUPPORTED.value, source_status, target_status, result_provenance, trace)
    if target_status not in statuses:
        return ContextLifecycleValidationResultV1(False, ContextLifecycleReasonCodeV1.TARGET_STATUS_UNSUPPORTED.value, source_status, target_status, result_provenance, trace)
    if source_status == ContextLifecycleStatusV1.ARCHIVED.value:
        return ContextLifecycleValidationResultV1(False, ContextLifecycleReasonCodeV1.ARCHIVED_TERMINAL.value, source_status, target_status, result_provenance, trace)
    if source_status == ContextLifecycleStatusV1.SUPERSEDED.value and target_status == ContextLifecycleStatusV1.ACTIVE.value:
        return ContextLifecycleValidationResultV1(False, ContextLifecycleReasonCodeV1.SUPERSEDED_REACTIVATION_FORBIDDEN.value, source_status, target_status, result_provenance, trace)
    if source_status == ContextLifecycleStatusV1.REQUESTED.value and target_status == ContextLifecycleStatusV1.ACTIVE.value:
        return ContextLifecycleValidationResultV1(False, ContextLifecycleReasonCodeV1.REQUESTED_ACTIVATION_FORBIDDEN.value, source_status, target_status, result_provenance, trace)
    if source_status == ContextLifecycleStatusV1.BUILT.value and target_status == ContextLifecycleStatusV1.ARCHIVED.value:
        return ContextLifecycleValidationResultV1(False, ContextLifecycleReasonCodeV1.BUILT_ARCHIVAL_FORBIDDEN.value, source_status, target_status, result_provenance, trace)
    if (source_status, target_status) not in _ALLOWED_TRANSITIONS_V1:
        return ContextLifecycleValidationResultV1(False, ContextLifecycleReasonCodeV1.TRANSITION_FORBIDDEN.value, source_status, target_status, result_provenance, trace)
    return ContextLifecycleValidationResultV1(True, ContextLifecycleReasonCodeV1.TRANSITION_ALLOWED.value, source_status, target_status, result_provenance, trace)
