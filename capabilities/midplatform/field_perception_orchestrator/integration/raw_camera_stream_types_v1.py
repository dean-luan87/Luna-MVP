from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional, Tuple


S2_SCHEMA_VERSION = "a-route-s2-raw-camera-stream-schema-v1"
S2_CONTRACT_VERSION = "a-route-s2-raw-camera-stream-contract-v1"
OWNER = "Field Perception Orchestrator / Raw Camera Stream Adapter"
SOURCE_TYPES = ("IMAGE_FILE", "VIDEO_FILE", "FRAME_REFERENCE", "IMAGE_SEQUENCE")
CONTROL_ACTIONS = ("STOP", "REVOKE")


@dataclass(frozen=True)
class RawFrameRecordV1:
    frame_id: str
    stream_session_id: str
    source_type: str
    source_ref: str
    device_ref: Optional[str]
    frame_index: int
    captured_at: int
    width: int
    height: int
    pixel_format: str
    frame_payload_ref: str
    content_hash: str
    temporal_validity: Dict[str, object]
    sensitivity: str
    trace_ref: str
    provenance_refs: Tuple[str, ...]
    candidate_only: bool = True
    raw_only: bool = True
    do_not_persist: bool = True
    semantic_interpretation: bool = False
    evidence_created: bool = False
    observation_created: bool = False
    schema_version: str = S2_SCHEMA_VERSION
    contract_version: str = S2_CONTRACT_VERSION


@dataclass(frozen=True)
class StreamSessionCandidateV1:
    session_id: str
    source_type: str
    source_ref: str
    started_at: int
    ended_at: Optional[int]
    max_frames: int
    max_duration_ms: int
    observation_demand_ref: str
    capability_requirement_ref: str
    revocation_condition: str
    stop_reason: str
    trace_ref: str
    provenance_refs: Tuple[str, ...]
    bounded: bool = True
    autonomous_continuous_execution: bool = False
    provider_invocation: bool = False
    candidate_only: bool = True
    do_not_persist: bool = True
    schema_version: str = S2_SCHEMA_VERSION
    contract_version: str = S2_CONTRACT_VERSION


@dataclass(frozen=True)
class PerceptionIngressCandidateV1:
    ingress_id: str
    stream_session_ref: str
    frame_refs: Tuple[str, ...]
    source_type: str
    ingress_kind: str
    observation_demand_ref: str
    trace_ref: str
    provenance_refs: Tuple[str, ...]
    candidate_only: bool = True
    raw_only: bool = True
    evidence_created: bool = False
    observation_created: bool = False
    gateway_admission: bool = False
    provider_invocation: bool = False
    natural_language_conclusion_ref: str = ""
    schema_version: str = S2_SCHEMA_VERSION
    contract_version: str = S2_CONTRACT_VERSION


@dataclass(frozen=True)
class StreamControlCandidateV1:
    control_id: str
    session_ref: str
    action: str
    reason: str
    trace_ref: str
    provenance_refs: Tuple[str, ...]
    candidate_only: bool = True
    runtime_execution: bool = False
    provider_invocation: bool = False


@dataclass(frozen=True)
class RawCameraAdapterResultV1:
    accepted: bool
    duplicate: bool
    rejection_code: str
    source_type: str
    session: Optional[StreamSessionCandidateV1]
    frames: Tuple[RawFrameRecordV1, ...]
    ingress: Optional[PerceptionIngressCandidateV1]
    control: Optional[StreamControlCandidateV1]
    component_real: bool
    synthetic_source: bool
    provider_autonomous_continuous_execution: bool = False
    provider_invocation: bool = False
    model_call: bool = False
    semantic_compression: bool = False
    provenance_grants_authority: bool = False
    candidate_only: bool = True


__all__ = [
    "CONTROL_ACTIONS",
    "OWNER",
    "SOURCE_TYPES",
    "RawCameraAdapterResultV1",
    "RawFrameRecordV1",
    "PerceptionIngressCandidateV1",
    "StreamControlCandidateV1",
    "StreamSessionCandidateV1",
]
