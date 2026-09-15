"""Deterministic Action Governance engine for synthetic fixtures."""

from __future__ import annotations

from typing import Tuple

from capabilities.midplatform.core.action_governance.action_core_types_v1 import (
    ActionCandidateV1,
    SourceRefV1,
)
from capabilities.midplatform.core.action_governance.action_dependency_types_v1 import (
    ActionDependencyCandidateV1,
)
from capabilities.midplatform.core.action_governance.action_failure_types_v1 import (
    FailureResultReferenceV1,
)
from capabilities.midplatform.core.action_governance.action_handoff_types_v1 import (
    ActionToRuntimeExecutorHandoffCandidateV1,
    ActionToTaskManagerHandoffCandidateV1,
)
from capabilities.midplatform.core.action_governance.action_io_types_v1 import (
    ActionGovernanceInputV1,
    ActionGovernanceOutputV1,
)
from capabilities.midplatform.core.action_governance.action_lifecycle_types_v1 import (
    CancellationSuspensionStatusV1,
)
from capabilities.midplatform.core.action_governance.action_precondition_types_v1 import (
    ActionPreconditionCandidateV1,
)
from capabilities.midplatform.core.action_governance.action_readiness_types_v1 import (
    ExecutionReadinessCandidateV1,
)
from capabilities.midplatform.core.action_governance.action_registry_v1 import (
    ACTION_OWNER,
    RUNTIME_EXECUTOR_OWNER,
    TASK_MANAGER_OWNER,
)
from capabilities.midplatform.core.action_governance.action_resource_types_v1 import (
    RESOURCE_PENDING_REACTION,
    RESOURCE_UNKNOWN,
    RESOURCE_UNAVAILABLE,
    ResourceConstraintStatusV1,
    normalize_resource_state,
)
from capabilities.midplatform.core.action_governance.action_rollback_types_v1 import (
    RollbackContextCandidateV1,
)
from capabilities.midplatform.core.action_governance.action_state_types_v1 import (
    ActionStateTransitionCandidateV1,
)
from capabilities.midplatform.core.action_governance.action_trace_types_v1 import (
    ActionTraceCandidateV1,
)


class ActionGovernanceEngineV1:
    def _mk_ref(
        self, owner: str, ref_id: str, ref_type: str = "REFERENCE"
    ) -> SourceRefV1:
        return SourceRefV1(owner=owner, ref_id=ref_id, ref_type=ref_type)

    def _has_precondition_missing(
        self, items: Tuple[ActionPreconditionCandidateV1, ...]
    ) -> bool:
        return any(
            item.required and item.status in {"missing", "violated", "stale"}
            for item in items
        )

    def _has_precondition_unknown(
        self, items: Tuple[ActionPreconditionCandidateV1, ...]
    ) -> bool:
        return any(item.required and item.status == "unknown" for item in items)

    def _has_dependency_incomplete(
        self, items: Tuple[ActionDependencyCandidateV1, ...]
    ) -> bool:
        return any(
            item.blocking and item.status in {"missing", "unknown", "violated", "stale"}
            for item in items
        )

    def _derive_state_and_readiness(
        self, request: ActionGovernanceInputV1, resource_state: str
    ) -> Tuple[str, str, str]:
        if request.cancellation_requested or (not request.target_valid):
            return (
                "CANCELLED",
                "blocked",
                "target_invalidated_or_cancellation_requested",
            )

        if not request.permission_valid:
            return ("NEEDS_PERMISSION", "blocked", "permission_recheck_failed")

        if not request.safety_valid:
            return ("BLOCKED", "blocked", "safety_recheck_failed")

        if request.rollback_required:
            return ("ROLLBACK_REQUIRED", "blocked", "rollback_context_required")

        if resource_state == RESOURCE_UNAVAILABLE:
            return ("SUSPENDED", "suspended", "resource_unavailable")

        if self._has_precondition_missing(request.preconditions):
            return (
                "PRECONDITION_PENDING",
                "not_ready",
                "precondition_missing_or_violated",
            )

        if self._has_precondition_unknown(request.preconditions):
            return (
                "PRECONDITION_PENDING",
                "blocked",
                "precondition_unknown_not_satisfied",
            )

        if self._has_dependency_incomplete(request.dependencies):
            return ("PRECONDITION_PENDING", "not_ready", "dependency_incomplete")

        if request.confirmation.is_fabricated:
            return ("NEEDS_CONFIRMATION", "blocked", "confirmation_fabricated")

        if request.confirmation.is_stale:
            return ("NEEDS_CONFIRMATION", "blocked", "confirmation_stale")

        if (
            request.reversibility == "irreversible"
            and not request.confirmation.strong_confirmation
        ):
            return (
                "NEEDS_CONFIRMATION",
                "not_ready",
                "irreversible_requires_strong_confirmation",
            )

        if request.confirmation.state == "required":
            return ("NEEDS_CONFIRMATION", "not_ready", "human_confirmation_required")

        if request.failure_result and request.failure_result.failure_class:
            return ("FAILED_CANDIDATE", "blocked", "failure_result_reference_intake")

        if request.revision_requested:
            return ("REVISED", "candidate_ready", "revision_requested")

        if request.prefer_eligible_state:
            return ("ELIGIBLE", "candidate_ready", "permission_safety_valid")

        return ("READY_CANDIDATE", "candidate_ready", "all_gates_satisfied")

    def run_case(self, request: ActionGovernanceInputV1) -> ActionGovernanceOutputV1:
        resource_state = normalize_resource_state(request.resource_state)
        state, readiness_state, reason = self._derive_state_and_readiness(
            request, resource_state
        )

        candidate = ActionCandidateV1(
            action_candidate_id=f"action:{request.scenario_id}",
            owner=ACTION_OWNER,
            candidate_kind="ACTION_CANDIDATE",
            source_decision_refs=request.selected_decision_refs,
            intent_refs=request.intent_refs,
            causal_refs=request.causal_refs,
            target_refs=request.target_refs,
            context_refs=request.context_refs,
            field_refs=request.field_refs,
            permission_refs=request.permission_refs,
            safety_refs=request.safety_refs,
            confirmation_refs=request.confirmation_refs,
            precondition_refs=tuple(
                self._mk_ref(ACTION_OWNER, item.precondition_id, "PRECONDITION")
                for item in request.preconditions
            ),
            dependency_refs=tuple(
                self._mk_ref(ACTION_OWNER, item.dependency_id, "DEPENDENCY")
                for item in request.dependencies
            ),
            resource_refs=request.resource_refs,
            reversibility=request.reversibility,
            action_state=state,
            execution_readiness=readiness_state,
            cancellation_policy="candidate_cancel_or_suspend_only",
            rollback_policy="rollback_context_only_no_execution",
            provenance=(
                self._mk_ref(
                    ACTION_OWNER, f"prov:{request.scenario_id}:formation", "PROVENANCE"
                ),
                self._mk_ref(
                    ACTION_OWNER, f"prov:{request.scenario_id}:validation", "PROVENANCE"
                ),
            ),
            revision_lineage=(f"lineage:{request.scenario_id}",),
            action_authority=True,
            runtime_authority=False,
            task_authority=False,
        )

        readiness = ExecutionReadinessCandidateV1(
            state=readiness_state,
            reason=reason,
            candidate_only=True,
            executed=False,
        )

        resource_reaction = "remain_eligible"
        if resource_state == RESOURCE_UNAVAILABLE:
            resource_reaction = "become_suspended"
        elif resource_state == RESOURCE_UNKNOWN:
            resource_reaction = RESOURCE_PENDING_REACTION
        resource_status = ResourceConstraintStatusV1(
            state=resource_state,
            reaction=resource_reaction,
        )

        cancellation_status = CancellationSuspensionStatusV1(
            cancelled=state == "CANCELLED",
            suspended=state == "SUSPENDED",
            reason=reason,
        )

        rollback_context = RollbackContextCandidateV1(
            rollback_required=request.rollback_required,
            rollback_trigger_refs=(f"rollback-trigger:{request.scenario_id}",)
            if request.rollback_required
            else (),
            rollback_executor_responsibility_ref="runtime-executor:rollback-responsibility",
            rollback_result_reference=f"rollback-result:{request.scenario_id}"
            if request.rollback_required
            else "",
            candidate_only=True,
            rollback_executed=False,
        )

        failure_result = request.failure_result or FailureResultReferenceV1(
            failure_class=None,
            execution_result_reference=None,
            failure_trace_reference=None,
            retry_authority_granted=False,
        )

        transitions = (
            ActionStateTransitionCandidateV1(
                action_candidate_id=candidate.action_candidate_id,
                from_state="PROPOSED",
                to_state=state,
                reason_candidate=reason,
                precondition_refs=tuple(
                    item.precondition_id for item in request.preconditions
                ),
                dependency_refs=tuple(
                    item.dependency_id for item in request.dependencies
                ),
                permission_refs=tuple(ref.ref_id for ref in request.permission_refs),
                safety_refs=tuple(ref.ref_id for ref in request.safety_refs),
                provenance_ref=f"prov:{request.scenario_id}:transition",
            ),
        )

        trace = ActionTraceCandidateV1(
            trace_id=f"trace:{request.scenario_id}",
            owner=ACTION_OWNER,
            action_candidate_ref=candidate.action_candidate_id,
            decision_refs=tuple(ref.ref_id for ref in request.selected_decision_refs),
            intent_refs=tuple(ref.ref_id for ref in request.intent_refs),
            causal_refs=tuple(ref.ref_id for ref in request.causal_refs),
            target_refs=tuple(ref.ref_id for ref in request.target_refs),
            context_refs=tuple(ref.ref_id for ref in request.context_refs),
            precondition_refs=tuple(
                item.precondition_id for item in request.preconditions
            ),
            dependency_refs=tuple(item.dependency_id for item in request.dependencies),
            permission_refs=tuple(ref.ref_id for ref in request.permission_refs),
            safety_refs=tuple(ref.ref_id for ref in request.safety_refs),
            confirmation_refs=tuple(ref.ref_id for ref in request.confirmation_refs),
            resource_refs=tuple(ref.ref_id for ref in request.resource_refs),
            rollback_refs=rollback_context.rollback_trigger_refs,
            failure_refs=tuple(
                x
                for x in (
                    failure_result.execution_result_reference,
                    failure_result.failure_trace_reference,
                )
                if x
            ),
            revision_refs=(f"revision:{request.scenario_id}",)
            if request.revision_requested
            else (),
            provenance=(
                f"prov:{request.scenario_id}:admission",
                f"prov:{request.scenario_id}:precondition",
                f"prov:{request.scenario_id}:dependency",
                f"prov:{request.scenario_id}:permission-safety",
                f"prov:{request.scenario_id}:confirmation",
            ),
            candidate_only=True,
        )

        runtime_handoff = ActionToRuntimeExecutorHandoffCandidateV1(
            handoff_id=f"runtime-handoff:{request.scenario_id}",
            producer_owner=ACTION_OWNER,
            consumer_owner=RUNTIME_EXECUTOR_OWNER,
            handoff_kind="ACTION_TO_RUNTIME_EXECUTOR_CANDIDATE_HANDOFF",
            action_candidate_ref=candidate.action_candidate_id,
            target_refs=tuple(ref.ref_id for ref in request.target_refs),
            precondition_refs=tuple(
                item.precondition_id for item in request.preconditions
            ),
            dependency_refs=tuple(item.dependency_id for item in request.dependencies),
            permission_refs=tuple(ref.ref_id for ref in request.permission_refs),
            safety_refs=tuple(ref.ref_id for ref in request.safety_refs),
            confirmation_state=request.confirmation.state,
            resource_refs=tuple(ref.ref_id for ref in request.resource_refs),
            reversibility=request.reversibility,
            rollback_context_ref=rollback_context.rollback_result_reference,
            provenance=(f"prov:{request.scenario_id}:runtime-handoff",),
            execution_readiness=readiness_state,
            candidate_only=True,
            action_executed=False,
            scheduler_executed=False,
            device_control_executed=False,
        )

        task_handoff = ActionToTaskManagerHandoffCandidateV1(
            handoff_id=f"task-handoff:{request.scenario_id}",
            producer_owner=ACTION_OWNER,
            consumer_owner=TASK_MANAGER_OWNER,
            handoff_kind="ACTION_TO_TASK_MANAGER_REFERENCE_HANDOFF",
            action_candidate_ref=candidate.action_candidate_id,
            task_reference_context_refs=tuple(
                ref.ref_id for ref in request.task_reference_context_refs
            ),
            dependency_refs=tuple(item.dependency_id for item in request.dependencies),
            provenance=(f"prov:{request.scenario_id}:task-handoff",),
            reference_only=True,
            task_created=False,
        )

        return ActionGovernanceOutputV1(
            scenario_id=request.scenario_id,
            action_candidate=candidate,
            precondition_results=request.preconditions,
            dependency_results=request.dependencies,
            readiness=readiness,
            resource_status=resource_status,
            cancellation_status=cancellation_status,
            rollback_context=rollback_context,
            failure_result=failure_result,
            transitions=transitions,
            trace_candidate=trace,
            runtime_handoff=runtime_handoff,
            task_handoff=task_handoff,
            candidate_only=True,
            runtime_executed=False,
            action_executed=False,
            task_created=False,
            scheduler_executed=False,
            database_write_executed=False,
            device_control_executed=False,
        )
