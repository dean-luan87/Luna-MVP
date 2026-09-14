"""Reference-only types for one governed YOLO11n invocation trial."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional, Tuple

from capabilities.midplatform.core.cognitive_state_formation.current_world_types_v1 import (
    CurrentWorldCandidateV1,
)


@dataclass(frozen=True)
class RealCapabilityInvocationTrialV1:
    """The one real provider result plus existing downstream handoffs."""

    trial_id: str
    input_source_ref: str
    requirement_ref: str
    provider_capability_requirement_ref: str
    model_contract_resolution: Any
    model_admission: Any
    observation_control: Any
    frame: Any
    provider_admission: Any
    provider_result: Any
    execution_result: Any
    gateway_admission: Any
    b1_context_result: Any
    current_world: Optional[CurrentWorldCandidateV1]
    real_provider_invocation_count: int
    single_frame: bool
    evidence_refs: Tuple[str, ...]
    trace_refs: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    candidate_only: bool = True
    truth_declared: bool = False
    fact_admitted: bool = False
    world_truth_authority: bool = False
    second_real_invocation_allowed: bool = False
    continuous_camera_allowed: bool = False
    model_download_allowed: bool = False
    action_execution: bool = False
    learning_execution: bool = False
    memory_mutation: bool = False
    logical_resolution_status: str = ""
    runtime_admission_status: str = ""
    executable_capability_created: bool = False
    provider_admission_reached: bool = False
    a_interpretation_reached: bool = False
    second_provider_invocation: bool = False
    terminal_readiness_owner: bool = False
    runtime_admission_bypassed: bool = False
    executable_candidate_bypassed: bool = False
    dynamic_flow_semantic_authority: bool = False


__all__ = ["RealCapabilityInvocationTrialV1"]
