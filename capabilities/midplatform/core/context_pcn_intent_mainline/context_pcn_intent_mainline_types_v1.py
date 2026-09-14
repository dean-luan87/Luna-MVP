from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

from capabilities.midplatform.core.context_pcn_intent_mainline.context_pcn_intent_mainline_error_types_v1 import (
    ContextPcnIntentIntegrationErrorV1,
)
from capabilities.midplatform.core.context_pcn_intent_mainline.context_pcn_intent_mainline_trace_types_v1 import (
    MainlineProvenanceReversePathV1,
    MainlineTraceLinkV1,
)


@dataclass(frozen=True)
class CompatibilityDecisionV1:
    hop_id: str
    compatible: bool
    hard_block: bool
    reason: str
    classification: str


@dataclass(frozen=True)
class ContextToPcnHandoffV1:
    handoff_id: str
    source_owner: str
    target_owner: str
    context_candidate_ref: str
    context_schema_ref: str
    field_context_refs: Tuple[str, ...]
    trace_ref: str
    provenance_ref: str
    version: str
    candidate_only: bool
    source_mutation: bool


@dataclass(frozen=True)
class PcnToIntentHandoffV1:
    handoff_id: str
    source_owner: str
    target_owner: str
    pcn_candidate_ref: str
    identity_self_role_context_refs: Tuple[str, ...]
    trace_ref: str
    provenance_ref: str
    version: str
    candidate_only: bool
    source_mutation: bool


@dataclass(frozen=True)
class IntegrationScenarioDirectiveV1:
    scenario_id: str
    description: str
    force_context_incomplete: bool = False
    remove_context_required_ref: bool = False
    context_to_pcn_version_override: str = ""
    force_pcn_incomplete: bool = False
    remove_pcn_required_ref: bool = False
    pcn_to_intent_version_override: str = ""
    duplicate_context_handoff_probe: bool = False
    duplicate_pcn_handoff_probe: bool = False
    force_missing_trace: bool = False
    force_intent_reject: bool = False


@dataclass(frozen=True)
class NegativeGuardFlagsV1:
    integration_has_no_owner: bool = True
    context_mutation: bool = False
    pcn_mutation: bool = False
    intent_direct_mutation: bool = False
    context_bypass_to_intent: bool = False
    pcn_bypass_intent_governance: bool = False
    database_write: bool = False
    device_control: bool = False
    scheduler_execution: bool = False
    task_mutation: bool = False
    runtime_side_effect: bool = False
    model_call: bool = False


@dataclass
class IntegrationExecutionRecordV1:
    scenario_id: str
    description: str
    stopped_at: str
    success: bool
    context_handoff_id: str
    pcn_handoff_id: str
    context_candidate_ref: str
    pcn_candidate_ref: str
    intent_candidate_ref: str
    compatibility: Tuple[CompatibilityDecisionV1, ...]
    trace: MainlineTraceLinkV1
    provenance: MainlineProvenanceReversePathV1
    guard_flags: NegativeGuardFlagsV1
    errors: Tuple[ContextPcnIntentIntegrationErrorV1, ...]
    diagnostics: Tuple[str, ...] = field(default_factory=tuple)
    metadata: Dict[str, str] = field(default_factory=dict)


@dataclass
class IntegrationRunSummaryV1:
    phase: str
    scenario_count: int
    passed_scenario_count: int
    failed_scenario_count: int
    candidate_only: bool
    synthetic_only: bool
    runtime_executed: bool
    database_write: bool
    device_control: bool
    scheduler_execution: bool
    task_mutation: bool
    source_module_mutation: bool
    model_call: bool
    status: str


@dataclass
class IntegrationRunPayloadV1:
    summary: IntegrationRunSummaryV1
    scenario_results: List[IntegrationExecutionRecordV1]
    artifacts: Dict[str, str]
