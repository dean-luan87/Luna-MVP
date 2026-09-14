from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Tuple

from capabilities.midplatform.core.cognitive_execution_chain.cognitive_execution_chain_error_types_v1 import (
    CognitiveExecutionChainErrorV1,
)
from capabilities.midplatform.core.cognitive_execution_chain.cognitive_execution_chain_trace_types_v1 import (
    EndToEndTraceV1,
    ProvenanceReversePathV1,
)


@dataclass(frozen=True)
class CompatibilityDecisionV1:
    hop_id: str
    compatibility_status: str
    allow_handoff: bool
    hard_block: bool
    reason: str


@dataclass(frozen=True)
class HandoffEnvelopeV1:
    handoff_id: str
    source_owner: str
    target_owner: str
    source_candidate_ref: str
    required_refs: Tuple[str, ...]
    trace_ref: str
    provenance_ref: str
    schema_version: str
    contract_version: str


@dataclass(frozen=True)
class ReconsiderationCandidateV1:
    route_id: str
    source_owner: str
    target_owner: str
    reason: str
    related_refs: Tuple[str, ...]
    candidate_only: bool = True


@dataclass(frozen=True)
class DiagnosticsCandidateV1:
    origin_layer: str
    error_namespace: str
    trace_refs: Tuple[str, ...]
    failure_category: str
    remediation_candidate_refs: Tuple[str, ...]
    candidate_only: bool = True


@dataclass(frozen=True)
class IntegrationScenarioDirectiveV1:
    scenario_id: str
    category: str
    description: str
    force_causal_uncertainty_high: bool = False
    force_decision_abstain: bool = False
    force_decision_permission_veto: bool = False
    force_action_permission_revoked: bool = False
    force_action_stale_confirmation: bool = False
    force_action_cancelled: bool = False
    force_runtime_admission_reject: bool = False
    force_runtime_failure: bool = False
    force_runtime_timeout: bool = False
    force_runtime_partial: bool = False
    force_runtime_rollback: bool = False
    force_version_incompatible_hop: str = ""
    force_version_migration_required_hop: str = ""
    force_missing_trace_hop: str = ""
    duplicate_handoff_probe: bool = False
    duplicate_action_handoff_probe: bool = False
    duplicate_feedback_probe: bool = False
    repeat_same_failure_probe: bool = False
    no_new_evidence_probe: bool = False
    permission_hard_block_probe: bool = False
    retry_authority_exhausted_probe: bool = False


@dataclass
class IntegrationExecutionRecordV1:
    scenario_id: str
    stopped_at: str
    runtime_attempted: bool
    runtime_side_effect: bool
    owner_bypass: bool
    runtime_bypass: bool
    handoff_path: Tuple[str, ...]
    compatibility: Tuple[CompatibilityDecisionV1, ...]
    end_to_end_trace: EndToEndTraceV1
    provenance: ProvenanceReversePathV1
    reconsideration_candidates: Tuple[ReconsiderationCandidateV1, ...]
    diagnostics_candidates: Tuple[DiagnosticsCandidateV1, ...]
    errors: Tuple[CognitiveExecutionChainErrorV1, ...]
    metadata: Dict[str, str] = field(default_factory=dict)


@dataclass
class IntegrationRunSummaryV1:
    phase: str
    scenario_count: int
    passed_scenario_count: int
    failed_scenario_count: int
    candidate_only: bool
    runtime_executed: bool
    database_write: bool
    device_control: bool
    scheduler_execution: bool
    task_mutation: bool
    field_mutation: bool
    memory_mutation: bool
    status: str


@dataclass
class IntegrationRunPayloadV1:
    summary: IntegrationRunSummaryV1
    scenario_results: List[IntegrationExecutionRecordV1]
    artifacts: Dict[str, str]
