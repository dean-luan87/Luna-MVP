"""Static and behavior validators for Action Governance outputs."""

from __future__ import annotations

from typing import Iterable

from capabilities.midplatform.core.action_governance.action_core_types_v1 import (
    ActionCandidateV1,
    SourceRefV1,
)
from capabilities.midplatform.core.action_governance.action_io_types_v1 import (
    ActionGovernanceOutputV1,
)
from capabilities.midplatform.core.action_governance.action_ownership_guard_v1 import (
    validate_canonical_owner,
    validate_no_parallel_owner_token,
    validate_ref_read_only,
    validate_runtime_handoff_candidate_only,
    validate_task_handoff_reference_only,
)
from capabilities.midplatform.core.action_governance.action_precondition_types_v1 import (
    PRECONDITION_STATUS_SET,
)
from capabilities.midplatform.core.action_governance.action_dependency_types_v1 import (
    DEPENDENCY_STATUS_SET,
)
from capabilities.midplatform.core.action_governance.action_registry_v1 import (
    ACTION_STATE_SET,
    NEGATIVE_GUARD_FLAGS,
)


def validate_input_refs_read_only(all_refs: Iterable[SourceRefV1]) -> bool:
    return validate_ref_read_only(all_refs) and validate_no_parallel_owner_token(
        all_refs
    )


def validate_preconditions(preconditions) -> bool:
    return all(item.status in PRECONDITION_STATUS_SET for item in preconditions)


def validate_dependencies(dependencies) -> bool:
    return all(item.status in DEPENDENCY_STATUS_SET for item in dependencies)


def validate_action_candidate(candidate: ActionCandidateV1) -> bool:
    return (
        validate_canonical_owner(candidate.owner)
        and candidate.candidate_kind == "ACTION_CANDIDATE"
        and candidate.action_state in ACTION_STATE_SET
        and candidate.execution_readiness
        in {"not_ready", "candidate_ready", "blocked", "suspended"}
        and candidate.action_authority is True
        and candidate.runtime_authority is False
        and candidate.task_authority is False
        and bool(candidate.source_decision_refs)
        and bool(candidate.target_refs)
        and bool(candidate.provenance)
    )


def validate_trace_completeness(output: ActionGovernanceOutputV1) -> bool:
    trace = output.trace_candidate
    return (
        bool(trace.decision_refs)
        and bool(trace.target_refs)
        and bool(trace.permission_refs)
        and bool(trace.safety_refs)
        and bool(trace.precondition_refs)
        and bool(trace.dependency_refs)
        and bool(trace.provenance)
    )


def validate_handoffs(output: ActionGovernanceOutputV1) -> bool:
    return validate_runtime_handoff_candidate_only(
        output.runtime_handoff
    ) and validate_task_handoff_reference_only(output.task_handoff)


def validate_no_runtime_side_effects(output: ActionGovernanceOutputV1) -> bool:
    return (
        output.candidate_only is True
        and output.runtime_executed is False
        and output.action_executed is False
        and output.task_created is False
        and output.scheduler_executed is False
        and output.database_write_executed is False
        and output.device_control_executed is False
    )


def validate_negative_guard_flags() -> bool:
    return all(NEGATIVE_GUARD_FLAGS.values())
