"""B3 integration-only envelopes; canonical owners remain unchanged."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Optional, Tuple

from capabilities.midplatform.core.decision_governance.decision_io_types_v1 import (
    DecisionGovernanceOutputV1,
)
from capabilities.midplatform.core.intent_governance.intent_io_types_v1 import (
    IntentGovernanceOutputV1,
)
from capabilities.midplatform.core.task_manager_types_v1 import (
    TaskCandidate,
    TaskReadinessCandidate,
)


@dataclass(frozen=True)
class B2CognitiveStateFlowReferenceV1:
    """Validated replay/reference envelope for an already-produced B2 result."""

    case_id: str
    mode: str
    cognitive_state_ref: str
    cognitive_flow_ref: str
    attention_refs: Tuple[str, ...]
    hypothesis_refs: Tuple[str, ...]
    alternative_hypothesis_refs: Tuple[str, ...]
    observation_need_refs: Tuple[str, ...]
    current_world_ref: str
    context_refs: Tuple[str, ...]
    field_refs: Tuple[str, ...]
    pcn_refs: Tuple[str, ...]
    uncertainty_refs: Tuple[str, ...]
    conflict_refs: Tuple[str, ...]
    temporal_refs: Tuple[str, ...]
    trace_ref: str
    provenance_refs: Tuple[str, ...]
    candidate_only: bool = True
    read_only: bool = True
    source_mutation_executed: bool = False
    provider_invocation: bool = False


@dataclass(frozen=True)
class B3TaskBridgeInputV1:
    """Task Manager input adapter payload, not a second Task contract."""

    candidate_id: str
    source_decision_ref: str
    source_health_refs: Tuple[str, ...]
    task_context_refs: Tuple[str, ...]
    required_observation_refs: Tuple[str, ...]
    decision_block_refs: Tuple[str, ...]
    task_summary: str
    trace_ref: str
    governance_ref: Optional[str] = None
    high_risk: bool = False
    health_tag: str = "task_candidate_health"
    fact_status: str = "not_fact"
    candidate_not_fact: bool = True


@dataclass(frozen=True)
class B3ControlledRunResultV1:
    case_id: str
    mode: str
    source: B2CognitiveStateFlowReferenceV1
    intent_output: IntentGovernanceOutputV1
    decision_output: DecisionGovernanceOutputV1
    task_readiness: TaskReadinessCandidate
    task_candidate: Optional[TaskCandidate]
    task_manager_status: str
    task_manager_cancelled: bool
    trace_chain: Tuple[str, ...]
    observation_need_preserved: bool
    safety_guard_preserved: bool
    permission_guard_preserved: bool
    resource_guard_preserved: bool
    uncertainty_refs_preserved: bool
    conflict_refs_preserved: bool
    temporal_refs_preserved: bool
    provenance_complete: bool
    cognitive_input_read_only: bool = True
    intent_mutation: bool = False
    decision_mutation: bool = False
    task_mutation: bool = False
    action_execution: bool = False
    runtime_execution: bool = False
    provider_invocation: bool = False
    semantic_compression: bool = False
    dynamic_cognitive_function_execution: bool = False
    candidate_only: bool = True
    metadata: Dict[str, Any] = field(default_factory=dict)
