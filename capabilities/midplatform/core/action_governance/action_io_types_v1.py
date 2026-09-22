"""I/O contract types for Action Governance controlled implementation v1."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Tuple

from capabilities.midplatform.core.action_governance.action_confirmation_types_v1 import (
    ConfirmationStatusV1,
)
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
from capabilities.midplatform.core.action_governance.action_lifecycle_types_v1 import (
    CancellationSuspensionStatusV1,
)
from capabilities.midplatform.core.action_governance.action_precondition_types_v1 import (
    ActionPreconditionCandidateV1,
)
from capabilities.midplatform.core.action_governance.action_readiness_types_v1 import (
    ExecutionReadinessCandidateV1,
)
from capabilities.midplatform.core.action_governance.action_resource_types_v1 import (
    ResourceConstraintStatusV1,
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


@dataclass(frozen=True)
class ActionGovernanceInputV1:
    scenario_id: str
    selected_decision_refs: Tuple[SourceRefV1, ...]
    intent_refs: Tuple[SourceRefV1, ...]
    causal_refs: Tuple[SourceRefV1, ...]
    target_refs: Tuple[SourceRefV1, ...]
    context_refs: Tuple[SourceRefV1, ...]
    field_refs: Tuple[SourceRefV1, ...]
    permission_refs: Tuple[SourceRefV1, ...]
    safety_refs: Tuple[SourceRefV1, ...]
    confirmation_refs: Tuple[SourceRefV1, ...]
    preconditions: Tuple[ActionPreconditionCandidateV1, ...]
    dependencies: Tuple[ActionDependencyCandidateV1, ...]
    resource_refs: Tuple[SourceRefV1, ...]
    resource_state: str
    permission_valid: bool
    safety_valid: bool
    confirmation: ConfirmationStatusV1
    reversibility: str
    target_valid: bool
    cancellation_requested: bool
    rollback_required: bool
    failure_result: Optional[FailureResultReferenceV1]
    revision_requested: bool
    prefer_eligible_state: bool = False
    task_reference_context_refs: Tuple[SourceRefV1, ...] = ()
    synthetic_only: bool = True
    candidate_only: bool = True
    working_envelope_ref: Optional[str] = None
    working_envelope_version_ref: Optional[str] = None


@dataclass(frozen=True)
class ActionGovernanceOutputV1:
    scenario_id: str
    action_candidate: ActionCandidateV1
    precondition_results: Tuple[ActionPreconditionCandidateV1, ...]
    dependency_results: Tuple[ActionDependencyCandidateV1, ...]
    readiness: ExecutionReadinessCandidateV1
    resource_status: ResourceConstraintStatusV1
    cancellation_status: CancellationSuspensionStatusV1
    rollback_context: RollbackContextCandidateV1
    failure_result: FailureResultReferenceV1
    transitions: Tuple[ActionStateTransitionCandidateV1, ...]
    trace_candidate: ActionTraceCandidateV1
    runtime_handoff: ActionToRuntimeExecutorHandoffCandidateV1
    task_handoff: ActionToTaskManagerHandoffCandidateV1
    candidate_only: bool
    runtime_executed: bool
    action_executed: bool
    task_created: bool
    scheduler_executed: bool
    database_write_executed: bool
    device_control_executed: bool
    working_envelope_ref: Optional[str] = None
    working_envelope_version_ref: Optional[str] = None
