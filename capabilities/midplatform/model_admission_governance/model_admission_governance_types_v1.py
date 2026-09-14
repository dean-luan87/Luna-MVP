# -*- coding: utf-8 -*-
"""Model Admission Governance Standard — types v1."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Dict, Tuple

PHASE_ID = "Phase-Midplatform-Model-Admission-Governance-Standard-v1-001"
SCOPE = "model_admission_governance_standard_planning_only"
SOURCE_CHAIN = "model_admission_governance_v1"

ADMISSION_GOVERNANCE_PRINCIPLE_EN = (
    "Model admission governance defines one shared lifecycle for adding, updating, "
    "disabling, replacing, or removing models. Domain-specific models may define "
    "profiles and adapters, but must not define separate governance lifecycles."
)
ADMISSION_GOVERNANCE_PRINCIPLE_ZH = (
    "模型准入治理为所有模型的新增、更新、禁用、替换、删除定义唯一共享生命周期。"
    "领域模型可以定义 profile 和 adapter，但不能重新定义一套治理流程。"
)

INHERITED_TRANSLATION_PRINCIPLE_ZH = "能翻译，不等于能启用。"
INHERITED_ADMISSION_PRINCIPLE_ZH = "能准入规划，不等于 runtime enable。"
INHERITED_CANDIDATE_PRINCIPLE_ZH = (
    "能生成 output candidate，不等于能 action / speech / fact_write。"
)

DRYRUN_LIFECYCLE_TEMPLATE_REF = "Phase-Midplatform-DryRun-Lifecycle-Template-v1-001"
SHARED_RUNTIME_GOVERNANCE_REF = "provider_runtime_governance_registry_v1"
SHARED_ADAPTER_CONTRACT_REF = "generic_slam_adapter_contract_v1"
DEFAULT_LIFECYCLE_VARIANT = "compressed"

FINAL_DECISION_READY_FOR_DRYRUN_CASES = (
    "MODEL_ADMISSION_GOVERNANCE_STANDARD_READY_FOR_DRYRUN_CASES"
)
FINAL_DECISION_CASES_READY_FOR_RUNNER = (
    "MODEL_ADMISSION_GOVERNANCE_CASES_READY_FOR_RUNNER"
)
FINAL_DECISION_STANDARD_REVIEW_GO = (
    "MODEL_ADMISSION_GOVERNANCE_STANDARD_REVIEW_GO"
)
FINAL_DECISION_STANDARD_REVIEW_BLOCKED = (
    "MODEL_ADMISSION_GOVERNANCE_STANDARD_REVIEW_BLOCKED"
)

SHARED_ADMISSION_LIFECYCLE_CHAIN: Tuple[str, ...] = (
    "Model Registry",
    "Model Capability Profile",
    "License / Source Gate",
    "Adapter Contract",
    "Provider Admission",
    "Runtime Governance",
    "Output Candidate Contract",
    "Domain Profile",
    "Dry-run Lifecycle",
    "Handoff / Runtime Trial",
)

MODEL_OPERATIONS: Tuple[str, ...] = (
    "add_model",
    "update_model",
    "disable_model",
    "replace_model",
    "remove_model",
    "deprecate_model",
    "rollback_model",
)

MODEL_TYPES: Tuple[str, ...] = (
    "vision",
    "ocr",
    "slam",
    "vio",
    "scene_graph",
    "segmentation",
    "tracking",
    "asr",
    "tts",
    "speaker_diarization",
    "face_expression",
    "world_model",
    "search",
    "planning",
    "unknown",
)

DOMAIN_PROFILE_ALLOWED_FIELDS: Tuple[str, ...] = (
    "domain_profile_ref",
    "adapter_profile_ref",
    "candidate_schema_mapping_ref",
    "input_output_mapping_ref",
    "model_capability_profile_ref",
)

FORBIDDEN_DOMAIN_OVERRIDES: Tuple[str, ...] = (
    "domain_specific_lifecycle",
    "bypass_model_registry",
    "bypass_license_gate",
    "bypass_adapter_contract",
    "bypass_provider_admission",
    "bypass_runtime_governance",
    "direct_action_output",
    "direct_speech_output",
    "direct_fact_write_output",
    "hard_delete_without_deprecate",
)

NON_EXECUTION_FLAGS: Dict[str, bool] = {
    "candidate_only_default": True,
    "runtime_enabled_default": False,
    "commercial_runtime_approved_default": False,
    "shared_lifecycle_required": True,
    "domain_profile_allowed": True,
    "domain_specific_lifecycle_forbidden": True,
    "lineage_required_for_update_replace_remove": True,
    "dryrun_lifecycle_template_required": True,
}

MODEL_ADMISSION_STANDARD_FIELDS: Tuple[str, ...] = (
    "standard_ref",
    "standard_version",
    "lifecycle_chain",
    "supported_operations",
    "lifecycle_variant_default",
    "dryrun_lifecycle_template_ref",
    "shared_runtime_governance_ref",
    "domain_profile_allowed_fields",
    "domain_specific_lifecycle_forbidden",
    "candidate_only_default",
    "runtime_enabled_default",
    "commercial_runtime_approved_default",
    "lineage_required_for_update_replace_remove",
)

MODEL_REGISTRY_ENTRY_FIELDS: Tuple[str, ...] = (
    "model_id",
    "model_family",
    "model_role",
    "domain_id",
    "model_type",
    "capability_profile_ref",
    "adapter_contract_ref",
    "provider_admission_ref",
    "runtime_governance_ref",
    "license_gate_ref",
    "source_chain",
    "input_contract_ref",
    "output_candidate_contract_ref",
    "domain_profile_ref",
    "lifecycle_variant",
    "candidate_only_default",
    "runtime_enabled_default",
    "commercial_runtime_approved",
    "registry_status",
    "lineage_ref",
)

MODEL_CAPABILITY_PROFILE_FIELDS: Tuple[str, ...] = (
    "profile_ref",
    "model_id",
    "model_type",
    "capability_tags",
    "input_modalities",
    "output_candidate_types",
    "latency_class",
    "compute_class",
    "offline_capable",
    "wearable_fit",
    "candidate_only_default",
)

MODEL_SOURCE_LICENSE_GATE_FIELDS: Tuple[str, ...] = (
    "license_gate_ref",
    "model_id",
    "license_type",
    "license_risk",
    "source_provenance_ref",
    "commercial_runtime_approved",
    "technical_reference_allowed",
    "license_gate_required",
    "candidate_only_default",
)

MODEL_ADAPTER_CONTRACT_REF_FIELDS: Tuple[str, ...] = (
    "adapter_contract_ref",
    "model_id",
    "adapter_profile_ref",
    "contract_status",
    "adapter_contract_required",
    "bypass_forbidden",
    "candidate_only_default",
)

MODEL_PROVIDER_ADMISSION_REF_FIELDS: Tuple[str, ...] = (
    "provider_admission_ref",
    "model_id",
    "provider_ref",
    "admission_stage",
    "provider_admission_required",
    "bypass_forbidden",
    "runtime_enabled_default",
    "candidate_only_default",
)

MODEL_RUNTIME_GOVERNANCE_REF_FIELDS: Tuple[str, ...] = (
    "runtime_governance_ref",
    "model_id",
    "shared_runtime_governance_ref",
    "runtime_governance_required",
    "bypass_forbidden",
    "runtime_enabled_default",
    "candidate_only_default",
)

MODEL_ADMISSION_PLANNING_DECISION_FIELDS: Tuple[str, ...] = (
    "decision_ref",
    "standard_ref",
    "registered_model_ids",
    "shared_lifecycle_required",
    "domain_profile_allowed",
    "domain_specific_lifecycle_forbidden",
    "candidate_only_default",
    "runtime_enabled_default",
    "commercial_runtime_approved_default",
    "lineage_required_for_update_replace_remove",
    "dryrun_lifecycle_template_required",
    "dryrun_lifecycle_template_ref",
    "final_decision",
    "candidate_only",
)


@dataclass(frozen=True)
class ModelAdmissionStandard:
    standard_ref: str
    standard_version: str
    lifecycle_chain: Tuple[str, ...]
    supported_operations: Tuple[str, ...]
    lifecycle_variant_default: str
    dryrun_lifecycle_template_ref: str
    shared_runtime_governance_ref: str
    domain_profile_allowed_fields: Tuple[str, ...]
    domain_specific_lifecycle_forbidden: bool
    candidate_only_default: bool
    runtime_enabled_default: bool
    commercial_runtime_approved_default: bool
    lineage_required_for_update_replace_remove: bool


@dataclass(frozen=True)
class ModelRegistryEntry:
    model_id: str
    model_family: str
    model_role: str
    domain_id: str
    model_type: str
    capability_profile_ref: str
    adapter_contract_ref: str
    provider_admission_ref: str
    runtime_governance_ref: str
    license_gate_ref: str
    source_chain: Tuple[str, ...]
    input_contract_ref: str
    output_candidate_contract_ref: str
    domain_profile_ref: str
    lifecycle_variant: str
    candidate_only_default: bool
    runtime_enabled_default: bool
    commercial_runtime_approved: bool
    registry_status: str
    lineage_ref: str


@dataclass(frozen=True)
class ModelCapabilityProfile:
    profile_ref: str
    model_id: str
    model_type: str
    capability_tags: Tuple[str, ...]
    input_modalities: Tuple[str, ...]
    output_candidate_types: Tuple[str, ...]
    latency_class: str
    compute_class: str
    offline_capable: bool
    wearable_fit: str
    candidate_only_default: bool = True


@dataclass(frozen=True)
class ModelSourceLicenseGate:
    license_gate_ref: str
    model_id: str
    license_type: str
    license_risk: str
    source_provenance_ref: str
    commercial_runtime_approved: bool
    technical_reference_allowed: bool
    license_gate_required: bool
    candidate_only_default: bool = True


@dataclass(frozen=True)
class ModelAdapterContractRef:
    adapter_contract_ref: str
    model_id: str
    adapter_profile_ref: str
    contract_status: str
    adapter_contract_required: bool
    bypass_forbidden: bool
    candidate_only_default: bool = True


@dataclass(frozen=True)
class ModelProviderAdmissionRef:
    provider_admission_ref: str
    model_id: str
    provider_ref: str
    admission_stage: str
    provider_admission_required: bool
    bypass_forbidden: bool
    runtime_enabled_default: bool
    candidate_only_default: bool = True


@dataclass(frozen=True)
class ModelRuntimeGovernanceRef:
    runtime_governance_ref: str
    model_id: str
    shared_runtime_governance_ref: str
    runtime_governance_required: bool
    bypass_forbidden: bool
    runtime_enabled_default: bool
    candidate_only_default: bool = True


@dataclass(frozen=True)
class ModelAdmissionPlanningDecision:
    decision_ref: str
    standard_ref: str
    registered_model_ids: Tuple[str, ...]
    shared_lifecycle_required: bool
    domain_profile_allowed: bool
    domain_specific_lifecycle_forbidden: bool
    candidate_only_default: bool
    runtime_enabled_default: bool
    commercial_runtime_approved_default: bool
    lineage_required_for_update_replace_remove: bool
    dryrun_lifecycle_template_required: bool
    dryrun_lifecycle_template_ref: str
    final_decision: str
    candidate_only: bool = True


def candidate_to_dict(obj: Any) -> Dict[str, Any]:
    return asdict(obj)
