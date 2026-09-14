"""Synthetic fixtures for Action Governance controlled implementation v1."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Tuple

from capabilities.midplatform.core.action_governance.action_confirmation_types_v1 import (
    ConfirmationStatusV1,
)
from capabilities.midplatform.core.action_governance.action_core_types_v1 import (
    SourceRefV1,
)
from capabilities.midplatform.core.action_governance.action_dependency_types_v1 import (
    ActionDependencyCandidateV1,
)
from capabilities.midplatform.core.action_governance.action_failure_types_v1 import (
    FailureResultReferenceV1,
)
from capabilities.midplatform.core.action_governance.action_io_types_v1 import (
    ActionGovernanceInputV1,
)
from capabilities.midplatform.core.action_governance.action_precondition_types_v1 import (
    ActionPreconditionCandidateV1,
)


@dataclass(frozen=True)
class ActionFixtureCaseV1:
    case_id: str
    description: str
    request: ActionGovernanceInputV1
    expected_state: str
    expected_readiness: str
    expected_runtime_handoff_eligible: bool
    expected_task_handoff_reference_only: bool
    expected_negative_guards: Tuple[str, ...]
    synthetic_only: bool = True


def _ref(owner: str, ref_id: str, ref_type: str = "REFERENCE") -> SourceRefV1:
    return SourceRefV1(owner=owner, ref_id=ref_id, ref_type=ref_type)


def _pre(
    case_id: str, domain: str, status: str, required: bool = True
) -> ActionPreconditionCandidateV1:
    return ActionPreconditionCandidateV1(
        precondition_id=f"precondition:{case_id}:{domain}",
        domain=domain,
        status=status,
        required=required,
        provenance_refs=(f"prov:{case_id}:precondition:{domain}",),
    )


def _dep(
    case_id: str, dep_type: str, status: str, blocking: bool = True
) -> ActionDependencyCandidateV1:
    return ActionDependencyCandidateV1(
        dependency_id=f"dependency:{case_id}:{dep_type}",
        dependency_type=dep_type,
        status=status,
        blocking=blocking,
        provenance_refs=(f"prov:{case_id}:dependency:{dep_type}",),
    )


def _mk(
    case_id: str,
    description: str,
    expected_state: str,
    expected_readiness: str,
    expected_runtime_handoff_eligible: bool,
    expected_task_handoff_reference_only: bool,
    expected_negative_guards: Tuple[str, ...],
    permission_valid: bool = True,
    safety_valid: bool = True,
    confirmation_state: str = "not_required",
    confirmation_stale: bool = False,
    strong_confirmation: bool = False,
    reversibility: str = "reversible",
    resource_state: str = "available",
    target_valid: bool = True,
    cancellation_requested: bool = False,
    rollback_required: bool = False,
    failure_result: Optional[FailureResultReferenceV1] = None,
    revision_requested: bool = False,
    prefer_eligible_state: bool = False,
    preconditions: Tuple[ActionPreconditionCandidateV1, ...] = (),
    dependencies: Tuple[ActionDependencyCandidateV1, ...] = (),
) -> ActionFixtureCaseV1:
    request = ActionGovernanceInputV1(
        scenario_id=case_id,
        selected_decision_refs=(
            _ref("Decision Governance", f"decision:{case_id}", "DECISION_CANDIDATE"),
        ),
        intent_refs=(_ref("Intent Governance", f"intent:{case_id}", "INTENT"),),
        causal_refs=(_ref("Causal Governance", f"causal:{case_id}", "CAUSAL"),),
        target_refs=(_ref("Target Governance", f"target:{case_id}", "TARGET"),),
        context_refs=(_ref("Context Governance", f"context:{case_id}", "CONTEXT"),),
        field_refs=(_ref("Cognitive Field", f"field:{case_id}", "FIELD"),),
        permission_refs=(
            _ref("Permission Governance", f"permission:{case_id}", "PERMISSION"),
        ),
        safety_refs=(_ref("Safety Governance", f"safety:{case_id}", "SAFETY"),),
        confirmation_refs=(
            _ref("Human Oversight", f"confirmation:{case_id}", "CONFIRMATION"),
        ),
        preconditions=preconditions,
        dependencies=dependencies,
        resource_refs=(_ref("Resource Governance", f"resource:{case_id}", "RESOURCE"),),
        resource_state=resource_state,
        permission_valid=permission_valid,
        safety_valid=safety_valid,
        confirmation=ConfirmationStatusV1(
            state=confirmation_state,
            is_stale=confirmation_stale,
            is_fabricated=False,
            strong_confirmation=strong_confirmation,
        ),
        reversibility=reversibility,
        target_valid=target_valid,
        cancellation_requested=cancellation_requested,
        rollback_required=rollback_required,
        failure_result=failure_result,
        revision_requested=revision_requested,
        prefer_eligible_state=prefer_eligible_state,
        task_reference_context_refs=(
            _ref("Task Context", f"task-context:{case_id}", "TASK_CONTEXT"),
        ),
        synthetic_only=True,
        candidate_only=True,
    )
    return ActionFixtureCaseV1(
        case_id=case_id,
        description=description,
        request=request,
        expected_state=expected_state,
        expected_readiness=expected_readiness,
        expected_runtime_handoff_eligible=expected_runtime_handoff_eligible,
        expected_task_handoff_reference_only=expected_task_handoff_reference_only,
        expected_negative_guards=expected_negative_guards,
    )


def get_action_synthetic_fixtures_v1() -> Tuple[ActionFixtureCaseV1, ...]:
    return (
        _mk(
            "A01_SELECTED_DECISION_TO_BASIC_ACTION_CANDIDATE",
            "selected decision refs form a basic action candidate",
            expected_state="READY_CANDIDATE",
            expected_readiness="candidate_ready",
            expected_runtime_handoff_eligible=True,
            expected_task_handoff_reference_only=True,
            expected_negative_guards=("selected_decision_not_action_execution",),
        ),
        _mk(
            "A02_PERMISSION_VALID_TO_ELIGIBLE",
            "permission valid leads to eligible state",
            expected_state="ELIGIBLE",
            expected_readiness="candidate_ready",
            expected_runtime_handoff_eligible=True,
            expected_task_handoff_reference_only=True,
            expected_negative_guards=(
                "permission_context_not_permanent_authorization",
            ),
            prefer_eligible_state=True,
        ),
        _mk(
            "A03_PERMISSION_REVOKED_TO_BLOCKED",
            "permission revoked blocks action candidate",
            expected_state="NEEDS_PERMISSION",
            expected_readiness="blocked",
            expected_runtime_handoff_eligible=False,
            expected_task_handoff_reference_only=True,
            expected_negative_guards=("no_permission_bypass",),
            permission_valid=False,
        ),
        _mk(
            "A04_SAFETY_VETO_TO_BLOCKED",
            "safety veto blocks action candidate",
            expected_state="BLOCKED",
            expected_readiness="blocked",
            expected_runtime_handoff_eligible=False,
            expected_task_handoff_reference_only=True,
            expected_negative_guards=("no_safety_bypass",),
            safety_valid=False,
        ),
        _mk(
            "A05_MISSING_PRECONDITION_TO_PENDING",
            "missing precondition remains pending",
            expected_state="PRECONDITION_PENDING",
            expected_readiness="not_ready",
            expected_runtime_handoff_eligible=False,
            expected_task_handoff_reference_only=True,
            expected_negative_guards=("unknown_precondition_not_satisfied",),
            preconditions=(_pre("A05", "environment", "missing"),),
        ),
        _mk(
            "A06_UNKNOWN_PRECONDITION_NOT_SATISFIED",
            "unknown precondition is not treated as satisfied",
            expected_state="PRECONDITION_PENDING",
            expected_readiness="blocked",
            expected_runtime_handoff_eligible=False,
            expected_task_handoff_reference_only=True,
            expected_negative_guards=("unknown_precondition_not_satisfied",),
            preconditions=(_pre("A06", "target_object", "unknown"),),
        ),
        _mk(
            "A07_HUMAN_CONFIRMATION_REQUIRED",
            "confirmation required keeps candidate not ready",
            expected_state="NEEDS_CONFIRMATION",
            expected_readiness="not_ready",
            expected_runtime_handoff_eligible=False,
            expected_task_handoff_reference_only=True,
            expected_negative_guards=("confirmation_cannot_be_fabricated",),
            confirmation_state="required",
        ),
        _mk(
            "A08_STALE_CONFIRMATION_REJECTED",
            "stale confirmation cannot be reused",
            expected_state="NEEDS_CONFIRMATION",
            expected_readiness="blocked",
            expected_runtime_handoff_eligible=False,
            expected_task_handoff_reference_only=True,
            expected_negative_guards=("stale_confirmation_cannot_be_reused",),
            confirmation_state="confirmed",
            confirmation_stale=True,
        ),
        _mk(
            "A09_REVERSIBLE_ACTION",
            "reversible action can be candidate-ready",
            expected_state="READY_CANDIDATE",
            expected_readiness="candidate_ready",
            expected_runtime_handoff_eligible=True,
            expected_task_handoff_reference_only=True,
            expected_negative_guards=("ready_not_executed",),
            reversibility="reversible",
        ),
        _mk(
            "A10_IRREVERSIBLE_STRONGER_CONFIRMATION_REQUIRED",
            "irreversible action requires stronger confirmation",
            expected_state="NEEDS_CONFIRMATION",
            expected_readiness="not_ready",
            expected_runtime_handoff_eligible=False,
            expected_task_handoff_reference_only=True,
            expected_negative_guards=("confirmation_cannot_be_fabricated",),
            reversibility="irreversible",
            confirmation_state="confirmed",
            strong_confirmation=False,
        ),
        _mk(
            "A11_RESOURCE_UNAVAILABLE_TO_SUSPENDED",
            "resource unavailable leads to suspended",
            expected_state="SUSPENDED",
            expected_readiness="suspended",
            expected_runtime_handoff_eligible=False,
            expected_task_handoff_reference_only=True,
            expected_negative_guards=("no_runtime_side_effect",),
            resource_state="unavailable",
        ),
        _mk(
            "A12_TARGET_INVALIDATED_TO_CANCELLED",
            "target invalidation cancels candidate",
            expected_state="CANCELLED",
            expected_readiness="blocked",
            expected_runtime_handoff_eligible=False,
            expected_task_handoff_reference_only=True,
            expected_negative_guards=("decision_not_action",),
            target_valid=False,
        ),
        _mk(
            "A13_DEPENDENCY_INCOMPLETE_TO_PENDING",
            "dependency incomplete keeps candidate pending",
            expected_state="PRECONDITION_PENDING",
            expected_readiness="not_ready",
            expected_runtime_handoff_eligible=False,
            expected_task_handoff_reference_only=True,
            expected_negative_guards=("action_governance_not_task_manager",),
            dependencies=(_dep("A13", "resource_dependency", "missing"),),
        ),
        _mk(
            "A14_ROLLBACK_REQUIRED_CANDIDATE",
            "rollback required remains candidate-only context",
            expected_state="ROLLBACK_REQUIRED",
            expected_readiness="blocked",
            expected_runtime_handoff_eligible=False,
            expected_task_handoff_reference_only=True,
            expected_negative_guards=("rollback_candidate_not_execution",),
            rollback_required=True,
            failure_result=FailureResultReferenceV1(
                failure_class="partial_execution",
                execution_result_reference="runtime-result:A14",
                failure_trace_reference="failure-trace:A14",
                retry_authority_granted=False,
            ),
        ),
        _mk(
            "A15_ACTION_TO_EXECUTOR_CANDIDATE_ONLY_HANDOFF",
            "runtime executor handoff remains candidate-only",
            expected_state="READY_CANDIDATE",
            expected_readiness="candidate_ready",
            expected_runtime_handoff_eligible=True,
            expected_task_handoff_reference_only=True,
            expected_negative_guards=("action_governance_not_executor",),
        ),
        _mk(
            "A16_ACTION_TO_TASK_MANAGER_REFERENCE_ONLY_HANDOFF",
            "task manager handoff remains reference-only",
            expected_state="READY_CANDIDATE",
            expected_readiness="candidate_ready",
            expected_runtime_handoff_eligible=True,
            expected_task_handoff_reference_only=True,
            expected_negative_guards=("action_governance_not_task_manager",),
        ),
    )
