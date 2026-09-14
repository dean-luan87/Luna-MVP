# -*- coding: utf-8 -*-
"""P1 Real Install / Local Availability DryRun — types v1.

Based on the GO P1 Download/License Planning, P1 Execution DryRun Foundation, P1
Execution Trace Streaming DryRun and its Post-Review, this phase runs a P1 model
asset *real local availability* dry-run. It only does local-environment probing,
import-spec checks (importlib.util.find_spec ONLY), dependency-gap checks, local
weight-path visibility, license / runtime-eligibility alignment and
fallback / blocked / deferred determination.

It does NOT download models, NOT install dependencies, NOT run real inference,
NOT connect live camera/sensor, NOT enter runtime, NOT trigger
action/speech/fact_write/navigation, and NOT enter the semantic layer.

Key boundaries:
1. Probe only via importlib.util.find_spec; never execute import side effects.
2. Package visibility is NOT runtime approval.
3. Weight visibility is NOT inference approval.
4. Install readiness is NOT runtime readiness; runtime trial eligibility stays false.
5. AGPL / unknown / research-only licenses must not become commercial runtime.
6. Reserved-only / deferred VLM families are not executed.
7. All test processes/conclusions go to the protected, non-deletable test board.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Dict, Tuple

from capabilities.midplatform.controlled_trial_governance.controlled_trial_governance_lifecycle_template_v1 import (
    TEMPLATE_ID,
)
from capabilities.test_board.test_board_protocol_v1 import (
    REQUIRED_TEST_BOARD_FIELDS,
    TEST_BOARD_GOVERNANCE_RULES,
)

PHASE_ID = "Phase-P1-Real-Install-Local-Availability-DryRun-v1-001"
SCOPE = "p1_real_install_local_availability_dryrun"
SOURCE_CHAIN = "p1_real_install_local_availability_dryrun_v1"

PLANNING_PRINCIPLE_ZH = (
    "基于已 GO 的 P1 Download/License Planning、P1 Execution DryRun Foundation、P1 Execution Trace "
    "Streaming DryRun 及其 Post-Review，执行 P1 模型资产真实本地安装与可见性 dry-run。只做本地环境探针、"
    "import spec 检查（仅 importlib.util.find_spec）、dependency gap 检查、local weight path 可见性检查、"
    "license / runtime eligibility 对齐检查、fallback / blocked / deferred 判定。不下载模型、不安装依赖、"
    "不执行真实 inference、不接 live camera/sensor、不进入 runtime、不触发 action/speech/fact_write/navigation、"
    "不进入语义层。package 可见不等于 runtime 批准；weight 可见不等于 inference 批准；install readiness 不等于 "
    "runtime readiness；runtime trial eligibility 全部保持 false。所有测试过程与结论必须写入 protected / "
    "non-deletable 测试板块。"
)

LUNA_CORE_PRINCIPLE = (
    "luna_remains_emotion_multimodal_brain_and_world_understanding_first_"
    "p1_real_install_local_availability_dryrun_is_local_probe_only_find_spec_only_no_install_no_download_no_inference_no_runtime"
)

# --------------------------------------------------------------------------- #
# Bindings
# --------------------------------------------------------------------------- #
DRYRUN_MODE = "p1_real_install_local_availability_dryrun_only"
LOCAL_AVAILABILITY_PROBE_ONLY = True
EXISTING_GOVERNANCE_REUSE_REQUIRED = True
NEW_ADMISSION_CONTRACT_CREATED = False
NEW_RUNTIME_GOVERNANCE_CREATED = False
CONTROLLED_TRIAL_TEMPLATE_REUSED = True

STREAMING_POST_REVIEW_REF = "Phase-P1-Execution-Trace-Streaming-DryRun-Post-Review-v1-001"
P1_DOWNLOAD_LICENSE_PLANNING_REF = "Phase-Recognition-Model-P1-Download-License-Planning-v1-001"
MODEL_GOVERNANCE_INTEGRATED_CLOSURE_REF = (
    "Phase-Recognition-Midplatform-Model-Governance-Integrated-Closure-v1-001"
)
TARGET_CHAIN_REF = "Phase-PhaseOne-Environment-Cognition-Evidence-Main-Chain-Closure-v1-001"
CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF = TEMPLATE_ID

NEXT_STEP_OPTIONS_REF = "p1_real_install_plan_or_controlled_install_dryrun"

STREAMING_POST_REVIEW_EXPECTED_GO = "P1_EXECUTION_TRACE_STREAMING_DRYRUN_POST_REVIEW_GO"
TEST_BOARD_PROTOCOL_EXPECTED_GO = "TEST_BOARD_PROTECTED_ARTIFACT_RULE_GO"

# Test board binding
TEST_BOARD_MODULE = "recognition_models"
TEST_BOARD_TEST_MODE = "dry_run"

# --------------------------------------------------------------------------- #
# Install readiness states
# --------------------------------------------------------------------------- #
LOCAL_READY = "LOCAL_READY"
PARTIAL_READY = "PARTIAL_READY"
INSTALL_REQUIRED = "INSTALL_REQUIRED"
BLOCKED_BY_LICENSE = "BLOCKED_BY_LICENSE"
DEFERRED_RESOURCE_HEAVY = "DEFERRED_RESOURCE_HEAVY"
RESERVED_ONLY = "RESERVED_ONLY"

INSTALL_READINESS_STATES: Tuple[str, ...] = (
    LOCAL_READY,
    PARTIAL_READY,
    INSTALL_REQUIRED,
    BLOCKED_BY_LICENSE,
    DEFERRED_RESOURCE_HEAVY,
    RESERVED_ONLY,
)

# --------------------------------------------------------------------------- #
# P1/P2 asset table (17). Probe metadata is static; package/weight visibility is
# resolved live via importlib.util.find_spec in the review (no import executed).
#   license_class: apache_or_mit | agpl | unknown
#   classification policy keys: reserved_only, deferred_resource_heavy,
#   license_blocked (hard runtime block but local probe allowed).
# --------------------------------------------------------------------------- #
LOCAL_ASSETS: Tuple[Dict[str, Any], ...] = (
    # ---- P1-A Segmentation ---- #
    {
        "asset_id": "mobile_sam", "family": "segmentation", "tier": "P1-A",
        "package_name": "mobile_sam", "import_name": "mobile_sam",
        "weight_required": True,
        "expected_weight_paths": ("models/mobile_sam/mobile_sam.pt", "weights/mobile_sam.pt"),
        "required_dependencies": ("torch", "torchvision"), "optional_dependencies": ("timm",),
        "license_type": "apache_like", "license_class": "apache_or_mit",
        "runtime_eligibility_level": 2,
        "reserved_only": False, "deferred_resource_heavy": False, "license_blocked": False,
    },
    {
        "asset_id": "fast_sam", "family": "segmentation", "tier": "P1-A",
        "package_name": "ultralytics", "import_name": "ultralytics",
        "weight_required": True,
        "expected_weight_paths": ("models/fastsam/FastSAM.pt", "weights/FastSAM-x.pt"),
        "required_dependencies": ("torch", "ultralytics"), "optional_dependencies": ("clip",),
        "license_type": "agpl_3_0", "license_class": "agpl",
        "runtime_eligibility_level": 2,
        "reserved_only": False, "deferred_resource_heavy": False, "license_blocked": True,
    },
    {
        "asset_id": "sam2", "family": "segmentation", "tier": "P1-A",
        "package_name": "sam2", "import_name": "sam2",
        "weight_required": True,
        "expected_weight_paths": ("models/sam2/sam2_hiera.pt",),
        "required_dependencies": ("torch", "torchvision"), "optional_dependencies": (),
        "license_type": "unknown", "license_class": "unknown",
        "runtime_eligibility_level": 1,
        "reserved_only": False, "deferred_resource_heavy": True, "license_blocked": False,
    },
    # ---- P1-B Tracking ---- #
    {
        "asset_id": "byte_track", "family": "tracking", "tier": "P1-B",
        "package_name": "yolox", "import_name": "yolox",
        "weight_required": False,
        "expected_weight_paths": (),
        "required_dependencies": ("numpy", "scipy"), "optional_dependencies": ("lap", "cython_bbox"),
        "license_type": "mit", "license_class": "apache_or_mit",
        "runtime_eligibility_level": 2,
        "reserved_only": False, "deferred_resource_heavy": False, "license_blocked": False,
    },
    {
        "asset_id": "deep_sort", "family": "tracking", "tier": "P1-B",
        "package_name": "deep_sort_realtime", "import_name": "deep_sort_realtime",
        "weight_required": True,
        "expected_weight_paths": ("models/deep_sort/ckpt.t7",),
        "required_dependencies": ("numpy", "scipy"), "optional_dependencies": ("torch",),
        "license_type": "mit", "license_class": "apache_or_mit",
        "runtime_eligibility_level": 2,
        "reserved_only": False, "deferred_resource_heavy": False, "license_blocked": False,
    },
    {
        "asset_id": "supervision", "family": "tracking", "tier": "P1-B",
        "package_name": "supervision", "import_name": "supervision",
        "weight_required": False,
        "expected_weight_paths": (),
        "required_dependencies": ("numpy", "opencv-python"), "optional_dependencies": (),
        "license_type": "mit", "license_class": "apache_or_mit",
        "runtime_eligibility_level": 1,
        "reserved_only": False, "deferred_resource_heavy": False, "license_blocked": False,
    },
    # ---- P1-C Depth / Spatial Hint ---- #
    {
        "asset_id": "midas", "family": "depth_spatial_hint", "tier": "P1-C",
        "package_name": "timm", "import_name": "timm",
        "weight_required": True,
        "expected_weight_paths": ("models/midas/dpt_swin2_tiny.pt", "weights/midas_v21_small.pt"),
        "required_dependencies": ("torch", "timm"), "optional_dependencies": ("opencv-python",),
        "license_type": "mit", "license_class": "apache_or_mit",
        "runtime_eligibility_level": 2,
        "reserved_only": False, "deferred_resource_heavy": False, "license_blocked": False,
    },
    {
        "asset_id": "depth_anything", "family": "depth_spatial_hint", "tier": "P1-C",
        "package_name": "depth_anything", "import_name": "depth_anything",
        "weight_required": True,
        "expected_weight_paths": ("models/depth_anything/depth_anything_vits14.pth",),
        "required_dependencies": ("torch", "torchvision"), "optional_dependencies": ("xformers",),
        "license_type": "apache_2_0", "license_class": "apache_or_mit",
        "runtime_eligibility_level": 1,
        "reserved_only": False, "deferred_resource_heavy": True, "license_blocked": False,
    },
    {
        "asset_id": "zoe_depth", "family": "depth_spatial_hint", "tier": "P1-C",
        "package_name": "zoedepth", "import_name": "zoedepth",
        "weight_required": True,
        "expected_weight_paths": ("models/zoedepth/ZoeD_M12_N.pt",),
        "required_dependencies": ("torch", "timm"), "optional_dependencies": (),
        "license_type": "mit", "license_class": "apache_or_mit",
        "runtime_eligibility_level": 1,
        "reserved_only": False, "deferred_resource_heavy": True, "license_blocked": False,
    },
    # ---- P1-D Object Detection Completion ---- #
    {
        "asset_id": "yolov8n", "family": "object_detection_completion", "tier": "P1-D",
        "package_name": "ultralytics", "import_name": "ultralytics",
        "weight_required": True,
        "expected_weight_paths": ("models/yolov8/yolov8n.pt", "weights/yolov8n.pt"),
        "required_dependencies": ("torch", "ultralytics"), "optional_dependencies": (),
        "license_type": "agpl_3_0", "license_class": "agpl",
        "runtime_eligibility_level": 2,
        "reserved_only": False, "deferred_resource_heavy": False, "license_blocked": True,
    },
    {
        "asset_id": "rt_detr", "family": "object_detection_completion", "tier": "P1-D",
        "package_name": "ultralytics", "import_name": "ultralytics",
        "weight_required": True,
        "expected_weight_paths": ("models/rtdetr/rtdetr-l.pt",),
        "required_dependencies": ("torch", "ultralytics"), "optional_dependencies": (),
        "license_type": "apache_2_0", "license_class": "apache_or_mit",
        "runtime_eligibility_level": 1,
        "reserved_only": False, "deferred_resource_heavy": False, "license_blocked": False,
    },
    {
        "asset_id": "grounding_dino", "family": "object_detection_completion", "tier": "P1-D",
        "package_name": "groundingdino", "import_name": "groundingdino",
        "weight_required": True,
        "expected_weight_paths": ("models/groundingdino/groundingdino_swint_ogc.pth",),
        "required_dependencies": ("torch", "torchvision", "transformers"), "optional_dependencies": (),
        "license_type": "apache_2_0", "license_class": "apache_or_mit",
        "runtime_eligibility_level": 1,
        "reserved_only": False, "deferred_resource_heavy": True, "license_blocked": False,
    },
    # ---- P2 Scene Relation / VLM (reserved/deferred) ---- #
    {
        "asset_id": "scene_relation_vlm", "family": "scene_relation_vlm", "tier": "P2",
        "package_name": "transformers", "import_name": "transformers",
        "weight_required": False,
        "expected_weight_paths": (),
        "required_dependencies": ("torch", "transformers"), "optional_dependencies": (),
        "license_type": "unknown", "license_class": "unknown",
        "runtime_eligibility_level": 0,
        "reserved_only": True, "deferred_resource_heavy": True, "license_blocked": False,
    },
    {
        "asset_id": "open_vocab_vlm", "family": "scene_relation_vlm", "tier": "P2",
        "package_name": "open_clip", "import_name": "open_clip",
        "weight_required": False,
        "expected_weight_paths": (),
        "required_dependencies": ("torch", "open_clip_torch"), "optional_dependencies": (),
        "license_type": "unknown", "license_class": "unknown",
        "runtime_eligibility_level": 0,
        "reserved_only": True, "deferred_resource_heavy": True, "license_blocked": False,
    },
    # ---- P2 Audio / Speech ---- #
    {
        "asset_id": "sense_voice", "family": "audio_speech", "tier": "P2",
        "package_name": "funasr", "import_name": "funasr",
        "weight_required": True,
        "expected_weight_paths": ("models/sensevoice/model.pt",),
        "required_dependencies": ("torch", "funasr"), "optional_dependencies": (),
        "license_type": "apache_2_0", "license_class": "apache_or_mit",
        "runtime_eligibility_level": 1,
        "reserved_only": True, "deferred_resource_heavy": False, "license_blocked": False,
    },
    {
        "asset_id": "pyannote", "family": "audio_speech", "tier": "P2",
        "package_name": "pyannote.audio", "import_name": "pyannote.audio",
        "weight_required": True,
        "expected_weight_paths": ("models/pyannote/segmentation.bin",),
        "required_dependencies": ("torch", "pyannote.audio"), "optional_dependencies": (),
        "license_type": "unknown", "license_class": "unknown",
        "runtime_eligibility_level": 0,
        "reserved_only": True, "deferred_resource_heavy": False, "license_blocked": True,
    },
    # ---- P2 Emotion Bridge (reserved-only) ---- #
    {
        "asset_id": "emotion_multimodal_bridge", "family": "emotion_multimodal_bridge", "tier": "P2",
        "package_name": "luna_emotion_bridge", "import_name": "luna_emotion_bridge",
        "weight_required": False,
        "expected_weight_paths": (),
        "required_dependencies": (), "optional_dependencies": (),
        "license_type": "unknown", "license_class": "unknown",
        "runtime_eligibility_level": 0,
        "reserved_only": True, "deferred_resource_heavy": True, "license_blocked": False,
    },
)

# --------------------------------------------------------------------------- #
# Fallback readiness chains (8)
# --------------------------------------------------------------------------- #
FALLBACK_READINESS_CHAINS: Tuple[Dict[str, str], ...] = (
    {"trigger": "fastsam_unavailable_or_blocked", "fallback_route": "mobile_sam_preferred_path"},
    {"trigger": "mobile_sam_unavailable", "fallback_route": "segmentation_disabled_with_availability_context"},
    {"trigger": "rt_detr_unavailable", "fallback_route": "yolov8n_test_only_local_path_if_available"},
    {"trigger": "yolo_unavailable", "fallback_route": "opencv_visual_symbol_object_placeholder_fallback"},
    {"trigger": "depth_anything_unavailable", "fallback_route": "midas_light_path_if_available"},
    {"trigger": "midas_unavailable", "fallback_route": "spatial_hint_disabled_with_uncertainty_context"},
    {"trigger": "vlm_deferred", "fallback_route": "scene_relation_disabled_path"},
    {"trigger": "audio_emotion_reserved", "fallback_route": "reserved_only_no_execution_path"},
)

# --------------------------------------------------------------------------- #
# Negative guards (15: A..O)
# --------------------------------------------------------------------------- #
NEGATIVE_GUARDS: Tuple[Dict[str, str], ...] = (
    {"guard_id": "invalid_a_real_dependency_install", "go_key": "no_dependency_install", "depends_on": "dependency_install_not_performed"},
    {"guard_id": "invalid_b_model_weight_download", "go_key": "no_model_weight_download", "depends_on": "download_not_performed"},
    {"guard_id": "invalid_c_real_inference", "go_key": "no_real_inference", "depends_on": "real_inference_not_performed"},
    {"guard_id": "invalid_d_import_probe_uses_real_import", "go_key": "find_spec_probe_only", "depends_on": "find_spec_probe_only_true"},
    {"guard_id": "invalid_e_package_visible_as_runtime_approval", "go_key": "package_visibility_not_runtime_approval", "depends_on": "package_visibility_not_runtime_approval"},
    {"guard_id": "invalid_f_weight_visible_as_inference_approval", "go_key": "weight_visibility_not_inference_approval", "depends_on": "weight_visibility_not_inference_approval"},
    {"guard_id": "invalid_g_agpl_unknown_as_commercial_runtime", "go_key": "license_not_commercial_runtime", "depends_on": "commercial_runtime_not_approved"},
    {"guard_id": "invalid_h_reserved_deferred_vlm_runtime_eligible", "go_key": "reserved_deferred_not_runtime_eligible", "depends_on": "reserved_deferred_not_executed"},
    {"guard_id": "invalid_i_can_enter_runtime_trial_true", "go_key": "runtime_trial_eligibility_all_false", "depends_on": "runtime_trial_eligibility_all_false"},
    {"guard_id": "invalid_j_semantic_promotion_allowed", "go_key": "semantic_promotion_blocked", "depends_on": "semantic_promotion_not_allowed"},
    {"guard_id": "invalid_k_action_speech_factwrite_navigation_allowed", "go_key": "action_speech_factwrite_navigation_blocked", "depends_on": "action_speech_factwrite_navigation_not_allowed"},
    {"guard_id": "invalid_l_vla_action_chain_allowed", "go_key": "vla_action_chain_blocked", "depends_on": "vla_action_chain_not_allowed"},
    {"guard_id": "invalid_m_test_record_not_written_to_board", "go_key": "test_board_record_required_enforced", "depends_on": "test_board_record_required_true"},
    {"guard_id": "invalid_n_test_artifact_not_protected", "go_key": "test_board_protected_marking_enforced", "depends_on": "test_board_protected_non_deletable_true"},
    {"guard_id": "invalid_o_cleanup_allows_test_board_deletion", "go_key": "cleanup_must_not_delete_test_board", "depends_on": "cleanup_does_not_delete_test_board"},
)

# --------------------------------------------------------------------------- #
# Governance rules (phase 30 + test board 6)
# --------------------------------------------------------------------------- #
LOCAL_AVAILABILITY_PHASE_GOVERNANCE_RULES: Tuple[str, ...] = (
    "this_phase_is_local_availability_dry_run_only",
    "no_real_dependency_install_is_allowed",
    "no_pip_install_is_allowed",
    "no_model_download_is_allowed",
    "no_weight_download_is_allowed",
    "no_dataset_download_is_allowed",
    "no_real_inference_is_allowed",
    "only_importlib_util_find_spec_probes_are_allowed",
    "package_visibility_is_not_runtime_approval",
    "weight_visibility_is_not_inference_approval",
    "install_readiness_is_not_runtime_readiness",
    "runtime_trial_eligibility_remains_false",
    "commercial_runtime_is_not_approved",
    "agpl_unknown_research_only_licenses_must_not_become_commercial_runtime",
    "reserved_only_families_are_not_executed",
    "deferred_vlm_nodes_are_not_executed",
    "candidate_only_boundary_must_be_preserved",
    "semantic_promotion_is_not_allowed",
    "guidance_support_is_not_navigation_runtime",
    "speech_gate_does_not_trigger_tts",
    "action_safety_does_not_trigger_action",
    "vla_action_chain_is_excluded",
    "test_board_record_is_required",
    "test_process_record_is_required",
    "test_conclusion_record_is_required",
    "test_artifacts_are_protected",
    "test_records_are_non_deletable",
    "cleanup_must_not_delete_test_board_artifacts",
    "local_availability_success_is_not_real_output_adapter_approval",
    "local_availability_success_is_not_runtime_approval",
)

ALL_GOVERNANCE_RULES: Tuple[str, ...] = (
    LOCAL_AVAILABILITY_PHASE_GOVERNANCE_RULES + TEST_BOARD_GOVERNANCE_RULES
)

REQUIRED_TEST_BOARD_FIELDS_LOCAL: Dict[str, bool] = dict(REQUIRED_TEST_BOARD_FIELDS)

DRYRUN_OBJECT_TYPES: Tuple[str, ...] = (
    "P1RealInstallLocalAvailabilityProfile",
    "LocalPackageProbe",
    "ImportSpecProbe",
    "LocalWeightPathProbe",
    "DependencyGapRecord",
    "LicenseRuntimeAlignmentCheck",
    "InstallReadinessRecord",
    "LocalAvailabilityState",
    "ModelAssetAvailabilityMatrix",
    "FallbackReadinessRecord",
    "BlockedDeferredReason",
    "P1LocalAvailabilityAuditRecord",
    "NegativeLocalAvailabilityGuard",
    "P1RealInstallLocalAvailabilityDryRunDecision",
)

HANDOFF_READINESS_TARGETS: Tuple[Dict[str, str], ...] = (
    {
        "target_ref": "Phase-P1-Real-Install-Plan-Controlled-Install-DryRun-v1-001",
        "go_key": "p1_real_install_plan_controlled_install_dryrun_readiness_recorded",
    },
)

FINAL_DECISION_GO = "P1_REAL_INSTALL_LOCAL_AVAILABILITY_DRYRUN_GO"
FINAL_DECISION_BLOCKED = "P1_REAL_INSTALL_LOCAL_AVAILABILITY_DRYRUN_BLOCKED"

REUSE_FLAGS: Dict[str, bool] = {
    "existing_governance_reuse_required": True,
    "controlled_trial_template_reused": True,
    "test_board_protocol_reused": True,
}

NEGATED_CREATION_FLAGS: Dict[str, bool] = {
    "new_admission_contract_created": False,
    "new_runtime_governance_created": False,
}

DRYRUN_TRUE_INVARIANTS: Dict[str, bool] = {
    "find_spec_probe_only": True,
    "no_real_import_executed": True,
    "package_visibility_not_runtime_approval": True,
    "weight_visibility_not_inference_approval": True,
    "install_readiness_not_runtime_readiness": True,
    "runtime_trial_eligibility_all_false": True,
    "reserved_only_not_executed": True,
    "deferred_vlm_not_executed": True,
    "candidate_only_boundary_preserved": True,
    "local_availability_success_not_real_output_adapter_approval": True,
    "local_availability_success_not_runtime_approval": True,
    "luna_emotion_multimodal_brain_first_preserved": True,
}

NON_EXECUTION_FLAGS: Dict[str, bool] = {
    "real_install_performed": False,
    "dependency_install_performed": False,
    "model_download_performed": False,
    "weight_download_performed": False,
    "dataset_download_performed": False,
    "real_inference_performed": False,
    "runtime_execution_allowed": False,
    "runtime_activation_allowed": False,
    "live_camera_connected": False,
    "live_sensor_connected": False,
    "continuous_runtime_allowed": False,
    "navigation_runtime_allowed": False,
    "action_runtime_allowed": False,
    "speech_runtime_allowed": False,
    "fact_write_runtime_allowed": False,
    "semantic_promotion_allowed": False,
    "vla_action_chain_allowed": False,
    "commercial_runtime_approved": False,
}


def classify_install_readiness(
    *,
    reserved_only: bool,
    license_blocked: bool,
    license_class: str,
    deferred_resource_heavy: bool,
    package_visible: bool,
    weight_required: bool,
    local_weight_visible: bool,
    missing_required_count: int,
) -> str:
    """Local install-readiness classification (probe-only, never runtime).

    Precedence: reserved_only -> license hard block (unknown/agpl) ->
    deferred resource heavy -> visibility/weight/dep based readiness.
    """
    if reserved_only:
        return RESERVED_ONLY
    if license_blocked or license_class in ("unknown",):
        return BLOCKED_BY_LICENSE
    if deferred_resource_heavy:
        return DEFERRED_RESOURCE_HEAVY
    if not package_visible:
        return INSTALL_REQUIRED
    # package visible from here.
    weight_ok = (not weight_required) or local_weight_visible
    if missing_required_count == 0 and weight_ok:
        return LOCAL_READY
    return PARTIAL_READY


@dataclass(frozen=True)
class P1RealInstallLocalAvailabilityProfile:
    profile_ref: str
    phase_id: str
    dryrun_mode: str
    local_availability_probe_only: bool
    existing_governance_reuse_required: bool
    new_admission_contract_created: bool
    new_runtime_governance_created: bool
    controlled_trial_template_reused: bool
    streaming_post_review_ref: str
    p1_download_license_planning_ref: str
    model_governance_integrated_closure_ref: str
    target_chain_ref: str
    controlled_trial_governance_template_ref: str
    luna_core_principle: str
    install_readiness_states: Tuple[str, ...]
    required_test_board_fields: Dict[str, bool]
    governance_rules: Tuple[str, ...]


@dataclass(frozen=True)
class LocalPackageProbe:
    asset_id: str
    model_family: str
    package_name: str
    import_probe_allowed: bool
    importlib_find_spec_used: bool
    package_visible: bool
    probe_error: str
    no_install_performed: bool


@dataclass(frozen=True)
class ImportSpecProbe:
    asset_id: str
    import_name: str
    spec_found: bool
    module_origin_available: bool
    import_executed: bool
    no_model_loaded: bool
    no_inference: bool


@dataclass(frozen=True)
class LocalWeightPathProbe:
    asset_id: str
    expected_weight_paths: Tuple[str, ...]
    local_weight_visible: bool
    weight_path_count: int
    no_weight_download: bool
    weight_required_for_real_inference: bool
    local_weight_missing_is_not_blocker_for_dryrun: bool


@dataclass(frozen=True)
class DependencyGapRecord:
    asset_id: str
    required_dependency_names: Tuple[str, ...]
    visible_dependency_names: Tuple[str, ...]
    missing_dependency_names: Tuple[str, ...]
    optional_dependency_names: Tuple[str, ...]
    dependency_install_performed: bool
    install_gap_severity: str


@dataclass(frozen=True)
class LicenseRuntimeAlignmentCheck:
    asset_id: str
    license_type: str
    commercial_runtime_approved: bool
    test_only: bool
    runtime_eligible_level: int
    license_blocks_runtime: bool
    license_allows_local_probe: bool


@dataclass(frozen=True)
class InstallReadinessRecord:
    asset_id: str
    install_readiness_state: str
    next_action: str
    install_dryrun_passed: bool
    real_install_required_before_inference: bool
    blocked_reason_refs: Tuple[str, ...]


@dataclass(frozen=True)
class LocalAvailabilityState:
    asset_id: str
    state: str
    runtime_eligible: bool


@dataclass(frozen=True)
class ModelAssetAvailabilityMatrix:
    asset_id: str
    family: str
    tier: str
    package_visible: bool
    local_weight_visible: bool
    dependency_gap_severity: str
    license_status: str
    runtime_eligibility_level: int
    install_readiness_state: str
    fallback_available: bool
    deferred_or_reserved: bool
    can_enter_next_install_dryrun: bool
    can_enter_real_output_adapter_dryrun: bool
    can_enter_runtime_trial: bool
    blocker_reason: str


@dataclass(frozen=True)
class FallbackReadinessRecord:
    trigger: str
    fallback_route: str
    candidate_only: bool
    triggers_install_or_inference: bool


@dataclass(frozen=True)
class BlockedDeferredReason:
    asset_id: str
    reason_code: str
    detail: str


@dataclass(frozen=True)
class P1LocalAvailabilityAuditRecord:
    audit_ref: str
    asset_count: int
    candidate_only: bool
    written_to_test_board: bool
    protected: bool
    non_deletable: bool


@dataclass
class NegativeLocalAvailabilityGuard:
    guard_id: str
    go_key: str
    depends_on: str
    passed: bool
    notes: Tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class P1RealInstallLocalAvailabilityHandoffReadiness:
    target_ref: str
    readiness_recorded: bool
    entered_this_phase: bool


@dataclass(frozen=True)
class P1RealInstallLocalAvailabilityDryRunDecision:
    decision_ref: str
    local_availability_profile_count: int
    model_asset_count: int
    local_package_probe_count: int
    import_spec_probe_count: int
    local_weight_path_probe_count: int
    dependency_gap_record_count: int
    license_runtime_alignment_check_count: int
    install_readiness_record_count: int
    model_asset_availability_matrix_count: int
    fallback_readiness_record_count: int
    blocked_deferred_reason_count: int
    negative_guard_count: int
    negative_guard_passed: int
    test_board_record_count: int
    blocker_count: int
    final_decision: str


def candidate_to_dict(obj: Any) -> Dict[str, Any]:
    return asdict(obj)
