# -*- coding: utf-8 -*-
"""Interface Layer Governance Protocol — types v1."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Dict, Tuple

PHASE_ID = "Phase-Midplatform-Interface-Layer-Governance-Protocol-v1-001"
SCOPE = "interface_layer_governance_protocol_baseline_only"
SOURCE_CHAIN = "interface_layer_governance_v1"

PROTOCOL_ID = "LUNA-PROTO-L1-INTERFACE-LAYER-GOVERNANCE-V1"
PROTOCOL_NAME = "Interface Layer Governance Protocol"
PROTOCOL_LAYER = "L1"
GOVERNANCE_LEVEL = "L1 Midplatform System Protocols"
CLASSIFICATION = "L1 Midplatform System Protocols"

INTERFACE_GOVERNANCE_PRINCIPLE_EN = (
    "Interface Layer Governance Protocol defines how external model/backend outputs "
    "enter Luna. Model Management Protocol governs model identity and lifecycle; "
    "Interface Layer Governance governs ingest shape, adapter obligation, internal "
    "standard format, and main-chain entry constraints."
)
INTERFACE_GOVERNANCE_PRINCIPLE_ZH = (
    "接口层治理协议定义外部模型/后端输出如何进入 Luna。"
    "模型管理协议管模型身份与生命周期；接口层协议管接入形态、adapter 义务、"
    "内部标准格式与主链入口约束。外部模型只提供能力，不得牵引 Luna 主架构。"
)

MODEL_MANAGEMENT_PROTOCOL_REF = "Model Management Protocol"
MODEL_ADMISSION_STANDARD_REF = "Phase-Midplatform-Model-Admission-Governance-Standard-v1-001"
PROVIDER_GOVERNANCE_REF = "provider_runtime_governance_registry_v1"
FIELD_SYNTHESIS_ENTRYPOINT = "field_synthesis_v1"
MIDPLATFORM_SYNTHESIS_ENTRYPOINT = "midplatform_synthesis_v1"

FINAL_DECISION_BASELINE_READY = (
    "INTERFACE_LAYER_GOVERNANCE_PROTOCOL_BASELINE_READY_FOR_ADOPTION"
)
FINAL_DECISION_REVIEW_BLOCKED = "INTERFACE_LAYER_GOVERNANCE_PROTOCOL_BASELINE_REVIEW_BLOCKED"

SHARED_INGEST_CHAIN: Tuple[str, ...] = (
    "External Model / Backend Output",
    "Interface Adapter",
    "Luna Internal Standard Format",
    "Candidate Schema",
    "Domain Profile",
    "Field / Midplatform Synthesis",
)

CORE_INTERFACE_GOVERNANCE_RULES: Tuple[str, ...] = (
    "external_model_must_not_write_luna_main_chain_directly",
    "external_output_must_pass_interface_adapter",
    "interface_adapter_must_emit_luna_internal_standard_format",
    "internal_standard_format_maps_to_candidate_schema",
    "candidate_enters_field_or_midplatform_synthesis_only",
    "no_per_model_private_ingest_entrypoint",
    "interface_layer_bound_by_model_management_and_provider_governance",
    "interface_changes_require_version_lineage_compatibility_policy",
)

INTERFACE_PROFILE_REFS: Tuple[str, ...] = (
    "spatial_evidence_ingest_interface",
    "vision_evidence_ingest_interface",
    "ocr_evidence_ingest_interface",
    "audio_asr_evidence_ingest_interface",
    "scene_graph_world_model_interface",
)

ACTIVE_INTERNAL_STANDARD_REFS: Tuple[str, ...] = ("generic_json_spatial_trace",)
PLANNED_INTERNAL_STANDARD_REFS: Tuple[str, ...] = (
    "generic_vision_detection_segmentation_trace",
    "generic_text_evidence_trace",
    "generic_speech_evidence_trace",
    "generic_field_graph_trace",
)

PLANNING_OBJECT_TYPES: Tuple[str, ...] = (
    "ExternalBackendInterfaceStandard",
    "InterfaceAdapterProfile",
    "InternalStandardFormatRef",
    "CandidateSchemaMappingRef",
    "InterfaceAdmissionPolicy",
    "InterfaceLifecycleDecision",
)

EXTERNAL_BACKEND_INTERFACE_STANDARD_FIELDS: Tuple[str, ...] = (
    "standard_ref",
    "protocol_id",
    "protocol_name",
    "governance_level",
    "model_management_protocol_ref",
    "ingest_chain",
    "core_rules",
    "candidate_only",
)

INTERFACE_ADAPTER_PROFILE_FIELDS: Tuple[str, ...] = (
    "adapter_profile_ref",
    "interface_profile_ref",
    "external_format_refs",
    "internal_standard_format_ref",
    "adapter_role",
    "candidate_only",
)

INTERNAL_STANDARD_FORMAT_REF_FIELDS: Tuple[str, ...] = (
    "format_ref",
    "interface_profile_ref",
    "format_status",
    "parser_ref",
    "field_synthesis_entrypoint",
    "candidate_only",
)

CANDIDATE_SCHEMA_MAPPING_REF_FIELDS: Tuple[str, ...] = (
    "mapping_ref",
    "internal_standard_format_ref",
    "candidate_schema_ref",
    "domain_profile_ref",
    "synthesis_entrypoint",
    "candidate_only",
)

INTERFACE_ADMISSION_POLICY_FIELDS: Tuple[str, ...] = (
    "policy_ref",
    "model_management_protocol_ref",
    "provider_governance_ref",
    "direct_main_chain_write_forbidden",
    "private_ingest_entrypoint_forbidden",
    "runtime_activation_default_false",
    "commercial_runtime_approval_default_false",
    "version_lineage_required",
    "candidate_only",
)

INTERFACE_LIFECYCLE_DECISION_FIELDS: Tuple[str, ...] = (
    "decision_ref",
    "protocol_ref",
    "active_internal_standard_refs",
    "planned_internal_standard_refs",
    "sealed_spatial_evidence_standard",
    "architecture_principle_locked",
    "baseline_planning_only",
    "no_runtime_activation",
    "final_decision",
    "candidate_only",
)

NON_EXECUTION_FLAGS: Dict[str, bool] = {
    "candidate_only": True,
    "protocol_baseline_planning_only": True,
    "no_runtime_activation": True,
    "no_provider_runtime_activation": True,
    "no_commercial_runtime_approval": True,
    "no_direct_main_chain_write": True,
    "no_per_model_private_ingest_entrypoint": True,
}


@dataclass(frozen=True)
class ExternalBackendInterfaceStandard:
    standard_ref: str
    protocol_id: str
    protocol_name: str
    governance_level: str
    model_management_protocol_ref: str
    ingest_chain: Tuple[str, ...]
    core_rules: Tuple[str, ...]
    candidate_only: bool = True


@dataclass(frozen=True)
class InterfaceAdapterProfile:
    adapter_profile_ref: str
    interface_profile_ref: str
    external_format_refs: Tuple[str, ...]
    internal_standard_format_ref: str
    adapter_role: str
    candidate_only: bool = True


@dataclass(frozen=True)
class InternalStandardFormatRef:
    format_ref: str
    interface_profile_ref: str
    format_status: str
    parser_ref: str
    field_synthesis_entrypoint: str
    candidate_only: bool = True


@dataclass(frozen=True)
class CandidateSchemaMappingRef:
    mapping_ref: str
    internal_standard_format_ref: str
    candidate_schema_ref: str
    domain_profile_ref: str
    synthesis_entrypoint: str
    candidate_only: bool = True


@dataclass(frozen=True)
class InterfaceAdmissionPolicy:
    policy_ref: str
    model_management_protocol_ref: str
    provider_governance_ref: str
    direct_main_chain_write_forbidden: bool
    private_ingest_entrypoint_forbidden: bool
    runtime_activation_default_false: bool
    commercial_runtime_approval_default_false: bool
    version_lineage_required: bool
    candidate_only: bool = True


@dataclass(frozen=True)
class InterfaceLifecycleDecision:
    decision_ref: str
    protocol_ref: str
    active_internal_standard_refs: Tuple[str, ...]
    planned_internal_standard_refs: Tuple[str, ...]
    sealed_spatial_evidence_standard: str
    architecture_principle_locked: bool
    baseline_planning_only: bool
    no_runtime_activation: bool
    final_decision: str
    candidate_only: bool = True


def candidate_to_dict(obj: Any) -> Dict[str, Any]:
    return asdict(obj)
