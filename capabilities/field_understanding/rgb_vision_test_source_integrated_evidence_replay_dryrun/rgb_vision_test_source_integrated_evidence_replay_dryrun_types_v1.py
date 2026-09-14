# -*- coding: utf-8 -*-
"""RGB Vision Test Source Integrated Evidence Replay DryRun — types v1.

Multi test-source integrated evidence replay. Selects 3-5 representative test
sources from the sealed Luna Vision Test Source Backup Pool (Roboflow / COCO /
ADE20K / TextOCR / Visual Genome) and validates that heterogeneous annotation /
sample metadata can be unified — via license/source admission + interface adapter
— into Luna RGB-first evidence candidates, then replayed through a Field / Task /
Guidance candidate path. Candidate-only; local controlled samples only.

  multi test-source samples
  -> unified license/source admission
  -> external vision interface adapter
  -> unified Luna evidence candidates
  -> Field / Task / Guidance candidate replay
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Dict, Tuple

from capabilities.midplatform.controlled_trial_governance.controlled_trial_governance_lifecycle_template_v1 import (
    TEMPLATE_ID,
)
from capabilities.field_understanding.rgb_vision_ocr_segmentation_integrated_evidence_replay_dryrun.rgb_vision_ocr_segmentation_integrated_evidence_replay_dryrun_types_v1 import (
    INTERFACE_ADAPTER_REF,
    TARGET_ENTRYPOINT,
    TARGET_INTERNAL_FORMAT,
    VISION_HARDWARE_BASELINE,
    SYSTEM_OBJECTIVE,
    GENERIC_JSON_PARSER_REF,
)

PHASE_ID = "Phase-RGB-Vision-Test-Source-Integrated-Evidence-Replay-DryRun-v1-001"
SCOPE = "rgb_vision_test_source_integrated_evidence_replay_dryrun"
SOURCE_CHAIN = "rgb_vision_test_source_integrated_evidence_replay_dryrun_v1"

DRYRUN_PRINCIPLE_ZH = (
    "基于已封口的 Luna Vision Test Source Backup Pool 与 RGB Vision / Roboflow integrated dry-run，"
    "执行多测试源 integrated evidence replay dry-run。从备用池中选 3-5 个轻量代表性测试源"
    "（Roboflow / COCO / ADE20K / TextOCR / Visual Genome），验证不同数据源的 annotation / sample "
    "metadata 能否统一进入 Luna RGB-first evidence candidate replay。只用本地受控样例或小样本 "
    "mock-but-file-based annotation；不下载大规模数据集，不训练模型，不接 live camera，不启动 "
    "runtime，不触发 navigation / action / speech / fact_write。集中验证，不拆单一来源。"
)

RUNTIME_TRIAL_MODE = "vision_test_source_integrated_replay_dryrun_only"
CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF = TEMPLATE_ID

# --------------------------------------------------------------------------- #
# Bindings
# --------------------------------------------------------------------------- #
_VISION_HARDWARE_BASELINE = VISION_HARDWARE_BASELINE
_SYSTEM_OBJECTIVE = SYSTEM_OBJECTIVE
_TARGET_ENTRYPOINT = TARGET_ENTRYPOINT
_INTERFACE_ADAPTER_REF = INTERFACE_ADAPTER_REF

# --------------------------------------------------------------------------- #
# Upstream references
# --------------------------------------------------------------------------- #
TEST_SOURCE_POOL_REF = "Phase-Luna-Vision-Test-Source-Backup-Pool-v1-001"
RGB_VISION_INTEGRATED_DRYRUN_REF = (
    "Phase-RGB-Vision-OCR-Segmentation-Integrated-Evidence-Replay-DryRun-v1-001"
)
ROBOFLOW_INTEGRATED_DRYRUN_REF = (
    "Phase-RGB-Vision-Roboflow-Dataset-Integrated-Evidence-Replay-DryRun-v1-001"
)
RGB_VISION_PLANNING_REF = (
    "Phase-RGB-Vision-OCR-Segmentation-Integrated-Evidence-Replay-Planning-v1-001"
)
RTAB_MULTI_EXPORT_CLOSURE_REF = (
    "Phase-RTAB-Map-Multi-Export-Spatial-Evidence-Replay-Integrated-Closure-v1-001"
)
FIELD_TASK_GUIDANCE_SAFETY_CHAIN_CLOSURE_REF = (
    "Phase-Field-Task-Guidance-Safety-Chain-Closure-v1-001"
)
GOVERNANCE_CLOSURE_REF = (
    "Phase-PhaseOne-Environment-Cognition-Controlled-Runtime-Trial-Governance-Closure-v1-001"
)
INTERFACE_LAYER_GOVERNANCE_REF = "Phase-Midplatform-Interface-Layer-Governance-Protocol-v1-001"
MODEL_ADMISSION_GOVERNANCE_REF = "Phase-Midplatform-Model-Admission-Governance-Standard-v1-001"

# --------------------------------------------------------------------------- #
# Test source samples
# --------------------------------------------------------------------------- #
FORMAT_REF = "vision_test_source_sample"

# source_id -> sample file
SAMPLE_SOURCES: Dict[str, str] = {
    "roboflow_universe": "roboflow_universe_sample.json",
    "coco": "coco_sample.json",
    "ade20k": "ade20k_sample.json",
    "textocr": "textocr_sample.json",
    "visual_genome": "visual_genome_sample.json",
}

RECOGNIZED_ANNOTATION_FORMATS: Tuple[str, ...] = (
    "yolo",
    "coco",
    "voc",
    "json",
    "semantic_segmentation",
    "text_polygon",
    "scene_graph",
)

# Unified admission fields each sample must carry.
ADMISSION_REQUIRED_FIELDS: Tuple[str, ...] = (
    "dataset_ref",
    "license_ref",
    "source_chain",
    "annotation_origin",
    "sample_origin",
    "annotation_format",
    "confidence",
    "allowed_use",
    "commercial_use_status",
    "candidate_mapping",
)

# Annotation type -> evidence candidate
ANNOTATION_TYPE_TO_CANDIDATE: Dict[str, Tuple[str, ...]] = {
    "bbox": ("object_evidence_candidate",),
    "object": ("object_evidence_candidate",),
    "segmentation": ("region_evidence_candidate",),
    "polygon": ("region_evidence_candidate",),
    "region": ("region_evidence_candidate",),
    "text": ("text_evidence_candidate",),
    "attribute": ("attribute_candidate",),
    "relationship": ("scene_relation_candidate",),
    "relation": ("scene_relation_candidate",),
}

ALL_EVIDENCE_CANDIDATE_TYPES: Tuple[str, ...] = (
    "scene_observation_candidate",
    "object_evidence_candidate",
    "region_evidence_candidate",
    "text_evidence_candidate",
    "attribute_candidate",
    "scene_relation_candidate",
    "task_context_candidate",
    "task_risk_candidate",
)

# Allowed-use / commercial vocab (kept consistent with the backup pool).
ALLOWED_USE_RESEARCH_TEST_ONLY = "research_test_only"
COMMERCIAL_NON_COMMERCIAL = "non_commercial"
COMMERCIAL_UNKNOWN = "unknown_until_license_verified"
COMMERCIAL_PER_DATASET = "per_dataset_license_required"

# Flags that must never be present on an admitted test-source sample.
PROHIBITED_OUTPUT_FLAGS: Tuple[str, ...] = (
    "direct_fact_write",
    "fact_write",
    "rewrite_field_fact",
    "route_activation",
    "direct_action",
    "direct_speech",
    "bypass_adapter",
    "native_direct_to_field",
    "direct_to_field_task_guidance",
)

# Flags that assert a dataset label as Luna truth.
AUTO_TRUST_FLAGS: Tuple[str, ...] = (
    "annotation_auto_trusted",
    "dataset_label_as_fact",
    "label_is_truth",
)

# Flags asserting commercial readiness without verified license.
COMMERCIAL_READY_FLAGS: Tuple[str, ...] = (
    "commercial_ready",
    "commercial_use_approved",
)

SAMPLES_REL_DIR = (
    "capabilities/field_understanding/"
    "rgb_vision_test_source_integrated_evidence_replay_dryrun/samples"
)

SAMPLE_FILES: Tuple[str, ...] = (
    "roboflow_universe_sample.json",
    "coco_sample.json",
    "ade20k_sample.json",
    "textocr_sample.json",
    "visual_genome_sample.json",
    "invalid_missing_license_ref.json",
    "invalid_missing_dataset_or_sample_origin.json",
    "invalid_annotation_auto_trusted.json",
    "invalid_non_commercial_marked_commercial_ready.json",
    "invalid_fact_write_route_activation_direct_action.json",
    "invalid_native_annotation_bypass_adapter.json",
)

POSITIVE_CASE_REFS: Tuple[str, ...] = (
    "roboflow_sample_to_luna_evidence_replay",
    "coco_sample_to_object_region_replay",
    "ade20k_sample_to_scene_region_replay",
    "textocr_sample_to_text_evidence_replay",
    "visual_genome_sample_to_scene_relation_replay",
    "multi_source_field_task_guidance_replay_path",
    "multi_source_observation_only_scope_replay",
)

NEGATIVE_CASE_REFS: Tuple[str, ...] = (
    "invalid_missing_license_ref_rejected",
    "invalid_missing_dataset_or_sample_origin_rejected",
    "invalid_annotation_auto_trusted_rejected",
    "invalid_non_commercial_marked_commercial_ready_rejected",
    "invalid_fact_write_route_activation_direct_action_rejected",
    "invalid_native_annotation_bypass_adapter_rejected",
)

FIELD_TASK_GUIDANCE_CANDIDATE_TYPES: Tuple[str, ...] = (
    "FieldCandidate",
    "FieldStateCandidate",
    "TaskContextCandidate",
    "TaskEvidenceNeedCandidate",
    "TaskRiskCandidate",
    "GuidanceCandidate",
    "SpeechGateCandidate",
    "ActionSafetyCandidate",
)

DRYRUN_OBJECT_TYPES: Tuple[str, ...] = (
    "RGBVisionTestSourceIntegratedReplayDryRunProfile",
    "VisionTestSourceSampleBundle",
    "VisionTestSourceAdmissionResult",
    "VisionAnnotationAdapterMappingResult",
    "VisionDatasetEvidenceCandidateResult",
    "VisionTestSourceFieldTaskGuidanceReplayResult",
    "VisionTestSourceRiskBoundaryResult",
    "RGBVisionTestSourceIntegratedReplayDryRunDecision",
)

DRYRUN_GOVERNANCE_RULES: Tuple[str, ...] = (
    "test_source_integrated_replay_is_not_training_admission",
    "test_source_integrated_replay_is_not_runtime_admission",
    "dataset_download_is_not_allowed_in_this_phase",
    "only_local_controlled_samples_may_be_read",
    "license_ref_dataset_ref_source_chain_annotation_origin_sample_origin_required",
    "commercial_use_remains_unknown_until_license_verified",
    "non_commercial_sources_must_remain_research_test_only",
    "dataset_labels_are_not_luna_truth",
    "annotation_is_evidence_candidate_not_fact",
    "interface_adapter_mapping_is_required",
    "native_annotation_output_must_not_enter_field_task_guidance_directly",
    "segmentation_region_annotation_is_not_route_activation",
    "ocr_text_annotation_is_not_fact",
    "scene_relation_annotation_is_not_final_interpretation",
    "field_task_guidance_replay_remains_candidate_only",
    "guidance_candidate_must_not_become_runtime_navigation",
    "speech_gate_candidate_must_not_become_tts",
    "action_safety_candidate_must_exist",
    "rgb_first_hardware_baseline_must_be_preserved",
    "integrated_validation_mode_must_be_used_no_single_source_split",
    "no_live_camera_no_live_sensor_no_real_gps_no_map_api_no_ros",
    "no_navigation_no_action_no_speech_no_fact_write",
    "controlled_trial_governance_lifecycle_template_must_be_referenced",
)

FINAL_DECISION_GO = "RGB_VISION_TEST_SOURCE_INTEGRATED_EVIDENCE_REPLAY_DRYRUN_GO"
FINAL_DECISION_BLOCKED = "RGB_VISION_TEST_SOURCE_INTEGRATED_EVIDENCE_REPLAY_DRYRUN_BLOCKED"

NEXT_PHASE_REF = "Phase-RGB-Vision-Evidence-Chain-Integrated-Closure-v1-001"

NON_EXECUTION_FLAGS: Dict[str, bool] = {
    "candidate_only_enforced": True,
    "integrated_validation_mode_used": True,
    "single_source_validation_not_used": True,
    "real_file_replay_execution_allowed": True,
    "dataset_download_allowed": False,
    "training_use_allowed": False,
    "runtime_activation_allowed": False,
    "live_camera_connected": False,
    "live_sensor_connected": False,
    "real_navigation_started": False,
    "real_map_api_connected": False,
    "real_gps_connected": False,
    "ros_connected": False,
    "camera_connected": False,
    "imu_connected": False,
    "direct_action_allowed": False,
    "direct_speech_allowed": False,
    "direct_fact_write_allowed": False,
    "commercial_runtime_approved": False,
}


@dataclass(frozen=True)
class RGBVisionTestSourceIntegratedReplayDryRunProfile:
    profile_ref: str
    phase_id: str
    controlled_trial_governance_template_ref: str
    test_source_pool_ref: str
    rgb_vision_integrated_dryrun_ref: str
    roboflow_integrated_dryrun_ref: str
    field_task_guidance_safety_chain_closure_ref: str
    interface_adapter_ref: str
    generic_json_spatial_trace_parser_ref: str
    vision_hardware_baseline: str
    system_objective: str
    target_internal_format: str
    target_entrypoint: str
    runtime_trial_mode: str
    sample_sources: Dict[str, str]
    recognized_annotation_formats: Tuple[str, ...]
    admission_required_fields: Tuple[str, ...]
    annotation_type_to_candidate: Dict[str, Tuple[str, ...]]
    field_task_guidance_candidate_types: Tuple[str, ...]
    governance_rules: Tuple[str, ...]


@dataclass(frozen=True)
class VisionTestSourceSampleBundle:
    bundle_ref: str
    source_id: str
    sample_file: str
    annotation_format: str
    image_count: int
    annotation_count: int
    source_chain: str


@dataclass(frozen=True)
class VisionTestSourceAdmissionResult:
    result_ref: str
    source_id: str
    sample_file: str
    file_source_admitted: bool
    controlled_samples_path_ok: bool
    format_ref_ok: bool
    required_fields_present: bool
    annotation_format_recognized: bool
    license_present: bool
    dataset_ref_present: bool
    sample_origin_present: bool
    confidence_present: bool
    annotation_not_auto_trusted: bool
    commercial_integrity_ok: bool
    prohibited_flags_absent: bool
    rejection_reasons: Tuple[str, ...]
    source_chain: str


@dataclass(frozen=True)
class VisionAnnotationAdapterMappingResult:
    result_ref: str
    source_id: str
    output_candidate_types: Tuple[str, ...]
    candidate_count: int
    adapter_mapping_used: bool
    source_chain_preserved: bool
    confidence_preserved: bool
    license_ref_preserved: bool
    dataset_ref_preserved: bool
    annotation_origin_preserved: bool
    sample_origin_preserved: bool
    candidate_only: bool
    source_chain: str


@dataclass(frozen=True)
class VisionDatasetEvidenceCandidateResult:
    result_ref: str
    source_id: str
    scene_observation_candidate_generated: bool
    object_evidence_candidate_generated: bool
    region_evidence_candidate_generated: bool
    text_evidence_candidate_generated: bool
    attribute_candidate_generated: bool
    scene_relation_candidate_generated: bool
    dataset_label_not_fact: bool
    candidate_only: bool
    source_chain: str


@dataclass(frozen=True)
class VisionTestSourceFieldTaskGuidanceReplayResult:
    result_ref: str
    field_task_guidance_replay_path_ok: bool
    task_context_references_evidence_candidates: bool
    task_risk_references_uncertainty_evidence: bool
    guidance_candidate_remains_candidate: bool
    speech_gate_candidate_not_tts: bool
    action_safety_candidate_exists: bool
    observation_only_scope_preserved: bool
    candidate_only: bool
    source_chain: str


@dataclass(frozen=True)
class VisionTestSourceRiskBoundaryResult:
    result_ref: str
    missing_license_ref_rejected: bool
    missing_dataset_or_sample_origin_rejected: bool
    annotation_auto_trusted_rejected: bool
    non_commercial_marked_commercial_ready_rejected: bool
    fact_write_route_activation_direct_action_rejected: bool
    native_annotation_bypass_adapter_rejected: bool
    source_chain: str


@dataclass(frozen=True)
class RGBVisionTestSourceIntegratedReplayDryRunDecision:
    decision_ref: str
    dryrun_profile_count: int
    sample_source_count: int
    sample_file_count: int
    positive_case_count: int
    negative_case_count: int
    positive_pass_count: int
    invalid_expected_reject_count: int
    test_source_backup_pool_go_verified: bool
    rgb_vision_integrated_dryrun_go_verified: bool
    roboflow_integrated_dryrun_go_verified: bool
    field_task_guidance_safety_chain_closure_go_verified: bool
    interface_layer_governance_verified: bool
    model_admission_governance_verified: bool
    controlled_trial_governance_template_ref_ok: bool
    final_decision: str
    real_file_replay_execution_allowed: bool = True
    runtime_activation_allowed: bool = False


def candidate_to_dict(obj: Any) -> Dict[str, Any]:
    return asdict(obj)
