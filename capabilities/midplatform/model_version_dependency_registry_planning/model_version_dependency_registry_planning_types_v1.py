# -*- coding: utf-8 -*-
"""Midplatform Model Version / Dependency Registry Planning — types v1.

A lightweight midplatform-layer model version & environment dependency manager.
Inserted BEFORE the P1 Real Install / Local Availability DryRun, it standardizes,
per model asset: model version, package version, import name, weight version,
runtime backend, environment constraints, license binding, dependency group,
hardware requirements, fallback compatibility and probe policy.

This phase is registry / planning / governance ONLY. It does NOT download models,
NOT install dependencies, NOT run inference, NOT enter runtime, NOT connect live
camera/sensor, NOT trigger navigation/action/speech/fact_write, and NOT enter the
semantic layer. It becomes the upstream governance asset for all later model
install / local availability / real output dry-runs.
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

PHASE_ID = "Phase-Midplatform-Model-Version-Dependency-Registry-Planning-v1-001"
SCOPE = "model_version_dependency_registry_planning"
SOURCE_CHAIN = "model_version_dependency_registry_planning_v1"

PLANNING_PRINCIPLE_ZH = (
    "在进入 P1 Real Install / Local Availability DryRun 之前，新增一个中台层的轻量模型版本与环境依赖管理器。"
    "该阶段用于规范管理模型资产的 model version、package version、import name、weight version、runtime backend、"
    "environment constraints、license binding、dependency group、hardware requirements、fallback compatibility、"
    "probe policy。只做 registry / planning / governance，不下载模型、不安装依赖、不执行 inference、不进入 runtime、"
    "不接 live camera/sensor、不触发 navigation/action/speech/fact_write、不进入语义层。它成为后续所有模型 "
    "install / local availability / real output dry-run 的上游治理资产：后续本地可见性探针不再散跑，必须依据本 "
    "registry 执行。"
)

LUNA_CORE_PRINCIPLE = (
    "luna_remains_emotion_multimodal_brain_and_world_understanding_first_"
    "midplatform_owns_model_version_and_dependency_registry_planning_only_no_install_no_download_no_inference_no_runtime"
)

# --------------------------------------------------------------------------- #
# Bindings
# --------------------------------------------------------------------------- #
PLANNING_ONLY = True
REGISTRY_PLANNING_ONLY = True
MIDPLATFORM_REGISTRY_LAYER = True
MODEL_VERSION_DEPENDENCY_MANAGER_CREATED = True
EXISTING_GOVERNANCE_REUSE_REQUIRED = True
NEW_RUNTIME_GOVERNANCE_CREATED = False
CONTROLLED_TRIAL_TEMPLATE_REUSED = True

P1_DOWNLOAD_LICENSE_PLANNING_REF = "Phase-Recognition-Model-P1-Download-License-Planning-v1-001"
MODEL_GOVERNANCE_INTEGRATED_CLOSURE_REF = (
    "Phase-Recognition-Midplatform-Model-Governance-Integrated-Closure-v1-001"
)
MODEL_ADMISSION_GOVERNANCE_REF = "Phase-Midplatform-Model-Admission-Governance-Standard-v1-001"
INTERFACE_LAYER_GOVERNANCE_REF = "Phase-Midplatform-Interface-Layer-Governance-Protocol-v1-001"
TARGET_CHAIN_REF = "Phase-PhaseOne-Environment-Cognition-Evidence-Main-Chain-Closure-v1-001"
CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF = TEMPLATE_ID

DOWNSTREAM_CONSUMER_REF = "Phase-P1-Real-Install-Local-Availability-DryRun-v1-001"

TEST_BOARD_PROTOCOL_EXPECTED_GO = "TEST_BOARD_PROTECTED_ARTIFACT_RULE_GO"

# Test board binding
TEST_BOARD_MODULE = "midplatform"
TEST_BOARD_TEST_MODE = "virtual_test"  # closest allowed mode to "planning"; see note below.
# NOTE: the test board protocol enumerates the allowed test_modes; "planning" is
# not one of them. The phase records test_mode="planning" as an explicit field in
# the review payload while the protocol record uses the allowed mode. We surface
# the requested label via PLANNING_TEST_MODE_LABEL for traceability.
PLANNING_TEST_MODE_LABEL = "planning"

# --------------------------------------------------------------------------- #
# Version lock policies (>= 5)
# --------------------------------------------------------------------------- #
EXACT_PIN = "exact_pin"
MINOR_RANGE = "minor_range"
FLOATING_PLANNING_ONLY = "floating_planning_only"
UNKNOWN_PLANNING_ONLY = "unknown_planning_only"
BLOCKED_UNTIL_VERSION_KNOWN = "blocked_until_version_known"

VERSION_LOCK_POLICIES: Tuple[Dict[str, str], ...] = (
    {"policy": EXACT_PIN, "allowed_stage": "real_inference_runtime_trial_commercial", "note": "pinned exact version"},
    {"policy": MINOR_RANGE, "allowed_stage": "install_dryrun_or_later_with_review", "note": "minor range, change requires review"},
    {"policy": FLOATING_PLANNING_ONLY, "allowed_stage": "planning_only", "note": "floating allowed for planning only"},
    {"policy": UNKNOWN_PLANNING_ONLY, "allowed_stage": "planning_only", "note": "unknown allowed for planning, blocks runtime/inference"},
    {"policy": BLOCKED_UNTIL_VERSION_KNOWN, "allowed_stage": "blocked", "note": "blocked until a version is visible/known"},
)

VERSION_LOCK_STAGE_RULES: Dict[str, str] = {
    "planning": "floating_or_unknown_allowed",
    "install_dryrun": "visible_version_or_missing_version_record_required",
    "real_inference": "pinned_or_approved_version_required",
    "runtime_trial": "pinned_plus_reviewed_version_required",
    "commercial_runtime": "pinned_plus_license_approved_plus_owner_approval_required",
}

# --------------------------------------------------------------------------- #
# Dependency groups (>= 8 -> 10)
# --------------------------------------------------------------------------- #
DEPENDENCY_GROUPS: Tuple[Dict[str, Any], ...] = (
    {"group_id": "cv_core", "packages": ("opencv-python", "numpy", "pillow")},
    {"group_id": "torch_core", "packages": ("torch", "torchvision")},
    {"group_id": "onnx_core", "packages": ("onnxruntime",)},
    {"group_id": "sam_family", "packages": ("segment-anything", "mobile-sam", "fastsam", "sam2")},
    {"group_id": "tracking_family", "packages": ("supervision", "bytetrack", "deep-sort-realtime")},
    {"group_id": "depth_family", "packages": ("midas", "depth-anything", "transformers", "timm")},
    {"group_id": "detection_family", "packages": ("ultralytics", "rtdetr", "groundingdino")},
    {"group_id": "audio_family", "packages": ("sensevoice", "pyannote.audio")},
    {"group_id": "vlm_family", "packages": ("transformers", "accelerate", "safetensors")},
    {"group_id": "governance_core", "packages": ("pydantic", "jsonschema")},
)

# --------------------------------------------------------------------------- #
# Dependency risk levels
# --------------------------------------------------------------------------- #
RISK_LOW = "LOW"
RISK_MEDIUM = "MEDIUM"
RISK_HIGH = "HIGH"
RISK_BLOCKED = "BLOCKED"

# --------------------------------------------------------------------------- #
# Model registry asset table (17). Static planning metadata; no probing here —
# the later P1 local availability dry-run backfills visible/missing versions.
# --------------------------------------------------------------------------- #
REGISTRY_ASSETS: Tuple[Dict[str, Any], ...] = (
    # ---- P1-A Segmentation ---- #
    {
        "asset_id": "mobile_sam", "canonical_name": "MobileSAM", "model_family": "segmentation", "tier": "P1-A",
        "source_category": "open_source", "open_form": "open_weights",
        "primary_package_name": "mobile_sam", "import_name": "mobile_sam",
        "optional_package_names": ("timm",), "required_dependency_names": ("torch", "torchvision"),
        "dependency_group": "sam_family",
        "weight_required": True, "expected_weight_names": ("mobile_sam.pt",),
        "expected_weight_paths": ("models/mobile_sam/mobile_sam.pt", "weights/mobile_sam.pt"),
        "backend_allowed_values": ("torch_cpu", "torch_gpu"), "gpu_required": False,
        "cpu_allowed": True, "onnx_allowed": False, "opencv_allowed": False,
        "license_type": "apache_like", "license_class": "apache_or_mit",
        "runtime_eligibility_level": 2, "reserved_only": False, "deferred_resource_heavy": False,
        "risk": RISK_MEDIUM,
    },
    {
        "asset_id": "fast_sam", "canonical_name": "FastSAM", "model_family": "segmentation", "tier": "P1-A",
        "source_category": "open_source", "open_form": "open_weights",
        "primary_package_name": "ultralytics", "import_name": "ultralytics",
        "optional_package_names": ("clip",), "required_dependency_names": ("torch", "ultralytics"),
        "dependency_group": "sam_family",
        "weight_required": True, "expected_weight_names": ("FastSAM-x.pt",),
        "expected_weight_paths": ("models/fastsam/FastSAM.pt", "weights/FastSAM-x.pt"),
        "backend_allowed_values": ("torch_cpu", "torch_gpu"), "gpu_required": False,
        "cpu_allowed": True, "onnx_allowed": False, "opencv_allowed": False,
        "license_type": "agpl_3_0", "license_class": "agpl",
        "runtime_eligibility_level": 2, "reserved_only": False, "deferred_resource_heavy": False,
        "risk": RISK_HIGH,
    },
    {
        "asset_id": "sam2_observation_node", "canonical_name": "SAM2", "model_family": "segmentation", "tier": "P1-A",
        "source_category": "open_source", "open_form": "open_weights",
        "primary_package_name": "sam2", "import_name": "sam2",
        "optional_package_names": (), "required_dependency_names": ("torch", "torchvision"),
        "dependency_group": "sam_family",
        "weight_required": True, "expected_weight_names": ("sam2_hiera.pt",),
        "expected_weight_paths": ("models/sam2/sam2_hiera.pt",),
        "backend_allowed_values": ("torch_gpu", "deferred"), "gpu_required": True,
        "cpu_allowed": False, "onnx_allowed": False, "opencv_allowed": False,
        "license_type": "unknown", "license_class": "unknown",
        "runtime_eligibility_level": 1, "reserved_only": False, "deferred_resource_heavy": True,
        "risk": RISK_HIGH,
    },
    # ---- P1-B Tracking ---- #
    {
        "asset_id": "byte_track", "canonical_name": "ByteTrack", "model_family": "tracking", "tier": "P1-B",
        "source_category": "open_source", "open_form": "open_code",
        "primary_package_name": "bytetrack", "import_name": "yolox",
        "optional_package_names": ("lap", "cython_bbox"), "required_dependency_names": ("numpy", "scipy"),
        "dependency_group": "tracking_family",
        "weight_required": False, "expected_weight_names": (), "expected_weight_paths": (),
        "backend_allowed_values": ("cpu", "torch_cpu"), "gpu_required": False,
        "cpu_allowed": True, "onnx_allowed": False, "opencv_allowed": False,
        "license_type": "mit", "license_class": "apache_or_mit",
        "runtime_eligibility_level": 2, "reserved_only": False, "deferred_resource_heavy": False,
        "risk": RISK_MEDIUM,
    },
    {
        "asset_id": "deep_sort", "canonical_name": "DeepSORT", "model_family": "tracking", "tier": "P1-B",
        "source_category": "open_source", "open_form": "open_weights",
        "primary_package_name": "deep_sort_realtime", "import_name": "deep_sort_realtime",
        "optional_package_names": ("torch",), "required_dependency_names": ("numpy", "scipy"),
        "dependency_group": "tracking_family",
        "weight_required": True, "expected_weight_names": ("ckpt.t7",),
        "expected_weight_paths": ("models/deep_sort/ckpt.t7",),
        "backend_allowed_values": ("cpu", "torch_cpu"), "gpu_required": False,
        "cpu_allowed": True, "onnx_allowed": False, "opencv_allowed": False,
        "license_type": "mit", "license_class": "apache_or_mit",
        "runtime_eligibility_level": 2, "reserved_only": False, "deferred_resource_heavy": False,
        "risk": RISK_MEDIUM,
    },
    {
        "asset_id": "supervision", "canonical_name": "supervision", "model_family": "tracking", "tier": "P1-B",
        "source_category": "open_source", "open_form": "open_code",
        "primary_package_name": "supervision", "import_name": "supervision",
        "optional_package_names": (), "required_dependency_names": ("numpy", "opencv-python"),
        "dependency_group": "tracking_family",
        "weight_required": False, "expected_weight_names": (), "expected_weight_paths": (),
        "backend_allowed_values": ("cpu", "opencv_rule"), "gpu_required": False,
        "cpu_allowed": True, "onnx_allowed": False, "opencv_allowed": True,
        "license_type": "mit", "license_class": "apache_or_mit",
        "runtime_eligibility_level": 1, "reserved_only": False, "deferred_resource_heavy": False,
        "risk": RISK_LOW,
    },
    # ---- P1-C Depth / Spatial Hint ---- #
    {
        "asset_id": "midas", "canonical_name": "MiDaS", "model_family": "depth_spatial_hint", "tier": "P1-C",
        "source_category": "open_source", "open_form": "open_weights",
        "primary_package_name": "timm", "import_name": "timm",
        "optional_package_names": ("opencv-python",), "required_dependency_names": ("torch", "timm"),
        "dependency_group": "depth_family",
        "weight_required": True, "expected_weight_names": ("midas_v21_small.pt",),
        "expected_weight_paths": ("models/midas/dpt_swin2_tiny.pt", "weights/midas_v21_small.pt"),
        "backend_allowed_values": ("torch_cpu", "torch_gpu"), "gpu_required": False,
        "cpu_allowed": True, "onnx_allowed": False, "opencv_allowed": False,
        "license_type": "mit", "license_class": "apache_or_mit",
        "runtime_eligibility_level": 2, "reserved_only": False, "deferred_resource_heavy": False,
        "risk": RISK_MEDIUM,
    },
    {
        "asset_id": "depth_anything", "canonical_name": "DepthAnything", "model_family": "depth_spatial_hint", "tier": "P1-C",
        "source_category": "open_source", "open_form": "open_weights",
        "primary_package_name": "depth_anything", "import_name": "depth_anything",
        "optional_package_names": ("xformers",), "required_dependency_names": ("torch", "torchvision"),
        "dependency_group": "depth_family",
        "weight_required": True, "expected_weight_names": ("depth_anything_vits14.pth",),
        "expected_weight_paths": ("models/depth_anything/depth_anything_vits14.pth",),
        "backend_allowed_values": ("torch_gpu", "torch_cpu", "deferred"), "gpu_required": False,
        "cpu_allowed": True, "onnx_allowed": False, "opencv_allowed": False,
        "license_type": "apache_2_0", "license_class": "apache_or_mit",
        "runtime_eligibility_level": 1, "reserved_only": False, "deferred_resource_heavy": True,
        "risk": RISK_MEDIUM,
    },
    {
        "asset_id": "zoe_depth", "canonical_name": "ZoeDepth", "model_family": "depth_spatial_hint", "tier": "P1-C",
        "source_category": "open_source", "open_form": "open_weights",
        "primary_package_name": "zoedepth", "import_name": "zoedepth",
        "optional_package_names": (), "required_dependency_names": ("torch", "timm"),
        "dependency_group": "depth_family",
        "weight_required": True, "expected_weight_names": ("ZoeD_M12_N.pt",),
        "expected_weight_paths": ("models/zoedepth/ZoeD_M12_N.pt",),
        "backend_allowed_values": ("torch_gpu", "deferred"), "gpu_required": True,
        "cpu_allowed": False, "onnx_allowed": False, "opencv_allowed": False,
        "license_type": "mit", "license_class": "apache_or_mit",
        "runtime_eligibility_level": 1, "reserved_only": False, "deferred_resource_heavy": True,
        "risk": RISK_HIGH,
    },
    # ---- P1-D Object Detection Completion ---- #
    {
        "asset_id": "yolov8n", "canonical_name": "YOLOv8n", "model_family": "object_detection_completion", "tier": "P1-D",
        "source_category": "open_source", "open_form": "open_weights",
        "primary_package_name": "ultralytics", "import_name": "ultralytics",
        "optional_package_names": (), "required_dependency_names": ("torch", "ultralytics"),
        "dependency_group": "detection_family",
        "weight_required": True, "expected_weight_names": ("yolov8n.pt",),
        "expected_weight_paths": ("models/yolov8/yolov8n.pt", "weights/yolov8n.pt"),
        "backend_allowed_values": ("torch_cpu", "torch_gpu"), "gpu_required": False,
        "cpu_allowed": True, "onnx_allowed": True, "opencv_allowed": False,
        "license_type": "agpl_3_0", "license_class": "agpl",
        "runtime_eligibility_level": 2, "reserved_only": False, "deferred_resource_heavy": False,
        "risk": RISK_HIGH,
    },
    {
        "asset_id": "rt_detr", "canonical_name": "RT-DETR", "model_family": "object_detection_completion", "tier": "P1-D",
        "source_category": "open_source", "open_form": "open_weights",
        "primary_package_name": "ultralytics", "import_name": "ultralytics",
        "optional_package_names": (), "required_dependency_names": ("torch", "ultralytics"),
        "dependency_group": "detection_family",
        "weight_required": True, "expected_weight_names": ("rtdetr-l.pt",),
        "expected_weight_paths": ("models/rtdetr/rtdetr-l.pt",),
        "backend_allowed_values": ("torch_cpu", "torch_gpu"), "gpu_required": False,
        "cpu_allowed": True, "onnx_allowed": True, "opencv_allowed": False,
        "license_type": "apache_2_0", "license_class": "apache_or_mit",
        "runtime_eligibility_level": 1, "reserved_only": False, "deferred_resource_heavy": False,
        "risk": RISK_MEDIUM,
    },
    {
        "asset_id": "grounding_dino", "canonical_name": "GroundingDINO", "model_family": "object_detection_completion", "tier": "P1-D",
        "source_category": "open_source", "open_form": "open_weights",
        "primary_package_name": "groundingdino", "import_name": "groundingdino",
        "optional_package_names": (), "required_dependency_names": ("torch", "torchvision", "transformers"),
        "dependency_group": "detection_family",
        "weight_required": True, "expected_weight_names": ("groundingdino_swint_ogc.pth",),
        "expected_weight_paths": ("models/groundingdino/groundingdino_swint_ogc.pth",),
        "backend_allowed_values": ("torch_gpu", "deferred"), "gpu_required": True,
        "cpu_allowed": False, "onnx_allowed": False, "opencv_allowed": False,
        "license_type": "apache_2_0", "license_class": "apache_or_mit",
        "runtime_eligibility_level": 1, "reserved_only": False, "deferred_resource_heavy": True,
        "risk": RISK_HIGH,
    },
    # ---- P2 Scene Relation / VLM ---- #
    {
        "asset_id": "scene_relation_vlm", "canonical_name": "scene_relation_vlm", "model_family": "scene_relation_vlm", "tier": "P2",
        "source_category": "open_source", "open_form": "open_weights",
        "primary_package_name": "transformers", "import_name": "transformers",
        "optional_package_names": ("accelerate", "safetensors"), "required_dependency_names": ("torch", "transformers"),
        "dependency_group": "vlm_family",
        "weight_required": False, "expected_weight_names": (), "expected_weight_paths": (),
        "backend_allowed_values": ("deferred",), "gpu_required": True,
        "cpu_allowed": False, "onnx_allowed": False, "opencv_allowed": False,
        "license_type": "unknown", "license_class": "unknown",
        "runtime_eligibility_level": 0, "reserved_only": True, "deferred_resource_heavy": True,
        "risk": RISK_BLOCKED,
    },
    {
        "asset_id": "open_vocab_vlm", "canonical_name": "open_vocab_vlm", "model_family": "scene_relation_vlm", "tier": "P2",
        "source_category": "open_source", "open_form": "open_weights",
        "primary_package_name": "open_clip", "import_name": "open_clip",
        "optional_package_names": ("accelerate", "safetensors"), "required_dependency_names": ("torch", "open_clip_torch"),
        "dependency_group": "vlm_family",
        "weight_required": False, "expected_weight_names": (), "expected_weight_paths": (),
        "backend_allowed_values": ("deferred",), "gpu_required": True,
        "cpu_allowed": False, "onnx_allowed": False, "opencv_allowed": False,
        "license_type": "unknown", "license_class": "unknown",
        "runtime_eligibility_level": 0, "reserved_only": True, "deferred_resource_heavy": True,
        "risk": RISK_BLOCKED,
    },
    # ---- P2 Audio / Speech ---- #
    {
        "asset_id": "sense_voice", "canonical_name": "SenseVoice", "model_family": "audio_speech", "tier": "P2",
        "source_category": "open_source", "open_form": "open_weights",
        "primary_package_name": "funasr", "import_name": "funasr",
        "optional_package_names": (), "required_dependency_names": ("torch", "funasr"),
        "dependency_group": "audio_family",
        "weight_required": True, "expected_weight_names": ("model.pt",),
        "expected_weight_paths": ("models/sensevoice/model.pt",),
        "backend_allowed_values": ("reserved_only",), "gpu_required": False,
        "cpu_allowed": True, "onnx_allowed": False, "opencv_allowed": False,
        "license_type": "apache_2_0", "license_class": "apache_or_mit",
        "runtime_eligibility_level": 1, "reserved_only": True, "deferred_resource_heavy": False,
        "risk": RISK_BLOCKED,
    },
    {
        "asset_id": "pyannote", "canonical_name": "pyannote", "model_family": "audio_speech", "tier": "P2",
        "source_category": "open_source", "open_form": "gated_weights",
        "primary_package_name": "pyannote.audio", "import_name": "pyannote.audio",
        "optional_package_names": (), "required_dependency_names": ("torch", "pyannote.audio"),
        "dependency_group": "audio_family",
        "weight_required": True, "expected_weight_names": ("segmentation.bin",),
        "expected_weight_paths": ("models/pyannote/segmentation.bin",),
        "backend_allowed_values": ("reserved_only",), "gpu_required": False,
        "cpu_allowed": True, "onnx_allowed": False, "opencv_allowed": False,
        "license_type": "unknown", "license_class": "unknown",
        "runtime_eligibility_level": 0, "reserved_only": True, "deferred_resource_heavy": False,
        "risk": RISK_BLOCKED,
    },
    # ---- P2 Emotion Bridge ---- #
    {
        "asset_id": "emotion_multimodal_bridge", "canonical_name": "emotion_multimodal_bridge", "model_family": "emotion_multimodal_bridge", "tier": "P2",
        "source_category": "internal_reserved", "open_form": "reserved",
        "primary_package_name": "luna_emotion_bridge", "import_name": "luna_emotion_bridge",
        "optional_package_names": (), "required_dependency_names": (),
        "dependency_group": "governance_core",
        "weight_required": False, "expected_weight_names": (), "expected_weight_paths": (),
        "backend_allowed_values": ("reserved_only",), "gpu_required": False,
        "cpu_allowed": True, "onnx_allowed": False, "opencv_allowed": False,
        "license_type": "unknown", "license_class": "unknown",
        "runtime_eligibility_level": 0, "reserved_only": True, "deferred_resource_heavy": True,
        "risk": RISK_BLOCKED,
    },
)

REGISTERED_MODEL_FAMILIES: Tuple[str, ...] = (
    "segmentation",
    "tracking",
    "depth_spatial_hint",
    "object_detection_completion",
    "scene_relation_vlm",
    "audio_speech",
    "emotion_multimodal_bridge",
)

# --------------------------------------------------------------------------- #
# Fallback compatibility chains (>= 8 -> 9)
# --------------------------------------------------------------------------- #
FALLBACK_COMPATIBILITY_CHAINS: Tuple[Dict[str, str], ...] = (
    {"primary_asset_id": "fast_sam", "fallback_asset_id": "mobile_sam", "fallback_condition": "fast_sam_unavailable_or_blocked"},
    {"primary_asset_id": "mobile_sam", "fallback_asset_id": "segmentation_disabled", "fallback_condition": "mobile_sam_unavailable"},
    {"primary_asset_id": "rt_detr", "fallback_asset_id": "yolov8n_test_only", "fallback_condition": "rt_detr_unavailable"},
    {"primary_asset_id": "yolov8n", "fallback_asset_id": "opencv_symbol_or_placeholder", "fallback_condition": "yolov8n_unavailable"},
    {"primary_asset_id": "depth_anything", "fallback_asset_id": "midas", "fallback_condition": "depth_anything_unavailable"},
    {"primary_asset_id": "midas", "fallback_asset_id": "spatial_hint_disabled", "fallback_condition": "midas_unavailable"},
    {"primary_asset_id": "scene_relation_vlm", "fallback_asset_id": "scene_relation_disabled", "fallback_condition": "vlm_deferred"},
    {"primary_asset_id": "pyannote", "fallback_asset_id": "audio_reserved_no_execution", "fallback_condition": "pyannote_sensevoice_reserved"},
    {"primary_asset_id": "emotion_multimodal_bridge", "fallback_asset_id": "emotion_reserved_no_execution", "fallback_condition": "emotion_bridge_reserved"},
)

# --------------------------------------------------------------------------- #
# Negative guards (18: A..R)
# --------------------------------------------------------------------------- #
NEGATIVE_GUARDS: Tuple[Dict[str, str], ...] = (
    {"guard_id": "invalid_a_unknown_version_enters_runtime", "go_key": "unknown_model_version_blocks_runtime", "depends_on": "unknown_version_blocks_runtime"},
    {"guard_id": "invalid_b_unknown_version_enters_real_inference", "go_key": "unknown_model_version_blocks_real_inference", "depends_on": "unknown_version_blocks_inference"},
    {"guard_id": "invalid_c_package_visible_as_runtime_approval", "go_key": "package_visibility_not_runtime_approval", "depends_on": "package_visibility_not_runtime_approval"},
    {"guard_id": "invalid_d_weight_visible_as_inference_approval", "go_key": "weight_visibility_not_inference_approval", "depends_on": "weight_visibility_not_inference_approval"},
    {"guard_id": "invalid_e_agpl_unknown_research_as_commercial_runtime", "go_key": "agpl_unknown_research_license_blocks_commercial_runtime", "depends_on": "license_blocks_commercial_runtime"},
    {"guard_id": "invalid_f_real_install_executed", "go_key": "no_real_install", "depends_on": "no_install_performed"},
    {"guard_id": "invalid_g_download_executed", "go_key": "no_download", "depends_on": "no_download_performed"},
    {"guard_id": "invalid_h_real_import_instead_of_find_spec", "go_key": "find_spec_probe_only_for_later", "depends_on": "find_spec_probe_only_for_later"},
    {"guard_id": "invalid_i_reserved_deferred_runtime_eligible", "go_key": "reserved_deferred_not_runtime_eligible", "depends_on": "reserved_deferred_not_runtime_eligible"},
    {"guard_id": "invalid_j_runtime_backend_unknown_runtime", "go_key": "runtime_backend_unknown_blocks_runtime", "depends_on": "runtime_backend_unknown_blocks_runtime"},
    {"guard_id": "invalid_k_dependency_drift_no_review", "go_key": "dependency_version_drift_requires_review", "depends_on": "dependency_version_drift_requires_review"},
    {"guard_id": "invalid_l_schema_drift_no_review", "go_key": "schema_drift_requires_review", "depends_on": "schema_drift_requires_review"},
    {"guard_id": "invalid_m_semantic_promotion_allowed", "go_key": "semantic_promotion_blocked", "depends_on": "semantic_promotion_not_allowed"},
    {"guard_id": "invalid_n_action_speech_factwrite_navigation_allowed", "go_key": "action_speech_factwrite_navigation_blocked", "depends_on": "action_speech_factwrite_navigation_not_allowed"},
    {"guard_id": "invalid_o_vla_action_chain_allowed", "go_key": "vla_action_chain_blocked", "depends_on": "vla_action_chain_not_allowed"},
    {"guard_id": "invalid_p_test_record_not_written_to_board", "go_key": "test_board_record_required_enforced", "depends_on": "test_board_record_required_true"},
    {"guard_id": "invalid_q_test_artifact_not_protected", "go_key": "test_board_protected_marking_enforced", "depends_on": "test_board_protected_non_deletable_true"},
    {"guard_id": "invalid_r_cleanup_allows_test_board_deletion", "go_key": "cleanup_must_not_delete_test_board", "depends_on": "cleanup_does_not_delete_test_board"},
)

# --------------------------------------------------------------------------- #
# Governance rules (39 phase + 6 test board = 45)
# --------------------------------------------------------------------------- #
REGISTRY_PHASE_GOVERNANCE_RULES: Tuple[str, ...] = (
    "this_phase_is_model_version_dependency_registry_planning_only",
    "midplatform_owns_model_version_and_dependency_registry",
    "model_version_records_are_required",
    "package_dependency_records_are_required",
    "import_name_binding_records_are_required",
    "weight_version_records_are_required_for_weight_based_models",
    "runtime_backend_records_are_required",
    "environment_constraint_records_are_required",
    "license_dependency_binding_records_are_required",
    "compatibility_constraints_are_required",
    "fallback_compatibility_records_are_required",
    "version_lock_policy_is_required",
    "dependency_risk_records_are_required",
    "unknown_model_version_is_allowed_only_for_planning",
    "unknown_model_version_blocks_runtime",
    "unknown_model_version_blocks_real_inference",
    "package_visibility_is_not_runtime_approval",
    "weight_visibility_is_not_inference_approval",
    "agpl_unknown_research_only_license_blocks_commercial_runtime",
    "runtime_backend_unknown_blocks_runtime",
    "dependency_version_drift_requires_review",
    "schema_drift_requires_review",
    "no_real_install_is_allowed",
    "no_pip_install_is_allowed",
    "no_dependency_install_is_allowed",
    "no_model_download_is_allowed",
    "no_weight_download_is_allowed",
    "no_dataset_download_is_allowed",
    "no_real_inference_is_allowed",
    "only_importlib_util_find_spec_probes_are_allowed_for_later_local_availability_dry_run",
    "reserved_only_families_are_not_runtime_eligible",
    "deferred_families_are_not_runtime_eligible",
    "commercial_runtime_is_not_approved",
    "candidate_only_boundary_is_preserved",
    "semantic_promotion_is_not_allowed",
    "guidance_support_is_not_navigation_runtime",
    "speech_gate_does_not_trigger_tts",
    "action_safety_does_not_trigger_action",
    "vla_action_chain_is_excluded",
)

ALL_GOVERNANCE_RULES: Tuple[str, ...] = (
    REGISTRY_PHASE_GOVERNANCE_RULES + TEST_BOARD_GOVERNANCE_RULES
)

REQUIRED_TEST_BOARD_FIELDS_LOCAL: Dict[str, bool] = dict(REQUIRED_TEST_BOARD_FIELDS)

DRYRUN_OBJECT_TYPES: Tuple[str, ...] = (
    "ModelVersionDependencyRegistryProfile",
    "ModelIdentityRecord",
    "ModelVersionRecord",
    "PackageDependencyRecord",
    "ImportNameBindingRecord",
    "WeightVersionRecord",
    "RuntimeBackendRecord",
    "EnvironmentConstraintRecord",
    "HardwareRequirementRecord",
    "LicenseDependencyBindingRecord",
    "OptionalDependencyGroupRecord",
    "ProbePolicyRecord",
    "CompatibilityConstraintRecord",
    "FallbackCompatibilityRecord",
    "VersionLockPolicy",
    "DependencyRiskRecord",
    "ModelVersionDependencyRegistryDecision",
)

HANDOFF_READINESS_TARGETS: Tuple[Dict[str, str], ...] = (
    {
        "target_ref": DOWNSTREAM_CONSUMER_REF,
        "go_key": "p1_real_install_local_availability_dryrun_must_consume_this_registry",
    },
)

FINAL_DECISION_GO = "MIDPLATFORM_MODEL_VERSION_DEPENDENCY_REGISTRY_PLANNING_GO"
FINAL_DECISION_BLOCKED = "MIDPLATFORM_MODEL_VERSION_DEPENDENCY_REGISTRY_PLANNING_BLOCKED"

REUSE_FLAGS: Dict[str, bool] = {
    "existing_governance_reuse_required": True,
    "controlled_trial_template_reused": True,
    "test_board_protocol_reused": True,
}

CREATION_FLAGS: Dict[str, bool] = {
    "model_version_dependency_manager_created": True,
    "midplatform_registry_layer": True,
    "registry_planning_only": True,
    "new_runtime_governance_created": False,
}

REQUIRED_RECORD_KIND_FLAGS: Dict[str, bool] = {
    "model_version_records_required": True,
    "package_dependency_records_required": True,
    "import_name_binding_records_required": True,
    "weight_version_records_required": True,
    "runtime_backend_records_required": True,
    "environment_constraint_records_required": True,
    "license_dependency_binding_records_required": True,
    "compatibility_constraints_required": True,
    "fallback_compatibility_required": True,
    "version_lock_policy_required": True,
    "dependency_risk_records_required": True,
}

PLANNING_TRUE_INVARIANTS: Dict[str, bool] = {
    "unknown_model_version_blocks_runtime": True,
    "unknown_model_version_blocks_real_inference": True,
    "package_visibility_not_runtime_approval": True,
    "weight_visibility_not_inference_approval": True,
    "agpl_unknown_research_license_blocks_commercial_runtime": True,
    "runtime_backend_unknown_blocks_runtime": True,
    "dependency_version_drift_requires_review": True,
    "schema_drift_requires_review": True,
    "reserved_only_not_runtime_eligible": True,
    "deferred_family_not_runtime_eligible": True,
    "candidate_only_boundary_preserved": True,
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


@dataclass(frozen=True)
class ModelVersionDependencyRegistryProfile:
    profile_ref: str
    phase_id: str
    planning_only: bool
    registry_planning_only: bool
    midplatform_registry_layer: bool
    model_version_dependency_manager_created: bool
    existing_governance_reuse_required: bool
    new_runtime_governance_created: bool
    controlled_trial_template_reused: bool
    p1_download_license_planning_ref: str
    model_governance_integrated_closure_ref: str
    model_admission_governance_ref: str
    interface_layer_governance_ref: str
    downstream_consumer_ref: str
    target_chain_ref: str
    controlled_trial_governance_template_ref: str
    luna_core_principle: str
    registered_model_families: Tuple[str, ...]
    required_test_board_fields: Dict[str, bool]
    governance_rules: Tuple[str, ...]


@dataclass(frozen=True)
class ModelIdentityRecord:
    asset_id: str
    canonical_name: str
    model_family: str
    tier: str
    source_category: str
    open_form: str
    registry_status: str
    owner_layer: str
    admission_ref: str
    license_ref: str
    output_adapter_ref: str
    fallback_ref: str


@dataclass(frozen=True)
class ModelVersionRecord:
    asset_id: str
    model_version_policy: str
    pinned_model_version: str
    allowed_version_range: str
    version_source: str
    version_unknown_allowed_for_planning: bool
    version_unknown_blocks_runtime: bool
    version_unknown_blocks_inference: bool
    version_change_requires_review: bool
    version_drift_detection_required: bool


@dataclass(frozen=True)
class PackageDependencyRecord:
    asset_id: str
    primary_package_name: str
    import_probe_name: str
    optional_package_names: Tuple[str, ...]
    required_dependency_names: Tuple[str, ...]
    dependency_group: str
    version_pin_policy: str
    visible_version_required_for_install_dryrun: bool
    dependency_conflict_risk: str
    no_install_in_this_phase: bool


@dataclass(frozen=True)
class ImportNameBindingRecord:
    asset_id: str
    package_name: str
    import_name: str
    importlib_find_spec_allowed: bool
    real_import_allowed: bool
    import_side_effect_risk: str
    probe_policy_ref: str
    no_model_load_on_probe: bool


@dataclass(frozen=True)
class WeightVersionRecord:
    asset_id: str
    weight_required: bool
    expected_weight_names: Tuple[str, ...]
    expected_weight_paths: Tuple[str, ...]
    weight_version_policy: str
    weight_hash_required_for_future_runtime: bool
    weight_source_allowed: str
    auto_weight_download_allowed: bool
    local_weight_visible_unknown_allowed_for_planning: bool
    weight_visible_not_inference_approval: bool


@dataclass(frozen=True)
class RuntimeBackendRecord:
    asset_id: str
    backend_type: str
    backend_allowed_values: Tuple[str, ...]
    gpu_required: bool
    cpu_allowed: bool
    onnx_allowed: bool
    opencv_allowed: bool
    backend_unknown_blocks_runtime: bool
    backend_change_requires_review: bool


@dataclass(frozen=True)
class EnvironmentConstraintRecord:
    asset_id: str
    python_version_policy: str
    os_policy: str
    macos_arm64_compatibility: str
    cuda_required: bool
    mps_possible: bool
    cpu_only_possible: bool
    memory_requirement_tier: str
    disk_requirement_tier: str
    offline_allowed: bool
    internet_required_for_install: bool
    internet_required_for_runtime: bool
    environment_unknown_blocks_runtime: bool


@dataclass(frozen=True)
class HardwareRequirementRecord:
    asset_id: str
    gpu_required: bool
    min_memory_tier: str
    min_disk_tier: str
    accelerator_preference: str
    cpu_fallback_possible: bool


@dataclass(frozen=True)
class LicenseDependencyBindingRecord:
    asset_id: str
    license_type: str
    license_source: str
    commercial_runtime_approved: bool
    test_only: bool
    license_unknown_blocks_runtime: bool
    agpl_blocks_commercial_runtime: bool
    research_only_blocks_runtime: bool
    license_change_requires_review: bool
    dependency_license_risk: str


@dataclass(frozen=True)
class OptionalDependencyGroupRecord:
    group_id: str
    packages: Tuple[str, ...]
    install_in_this_phase: bool
    visible_version_required_for_install_dryrun: bool


@dataclass(frozen=True)
class ProbePolicyRecord:
    asset_id: str
    probe_method: str
    importlib_find_spec_only: bool
    real_import_allowed: bool
    no_model_load_on_probe: bool
    package_visible_not_runtime_approval: bool


@dataclass(frozen=True)
class CompatibilityConstraintRecord:
    asset_id: str
    compatible_with_adapter: bool
    compatible_with_output_schema: bool
    compatible_with_midplatform_data_handling: bool
    compatible_with_midplatform_model_control: bool
    incompatible_reason: str
    schema_drift_requires_review: bool


@dataclass(frozen=True)
class FallbackCompatibilityRecord:
    primary_asset_id: str
    fallback_asset_id: str
    fallback_condition: str
    fallback_output_schema_compatible: bool
    fallback_license_compatible: bool
    fallback_runtime_boundary_preserved: bool


@dataclass(frozen=True)
class VersionLockPolicy:
    policy: str
    allowed_stage: str
    note: str


@dataclass(frozen=True)
class DependencyRiskRecord:
    asset_id: str
    risk_level: str
    risk_factors: Tuple[str, ...]
    runtime_eligible: bool


@dataclass
class NegativeRegistryGuard:
    guard_id: str
    go_key: str
    depends_on: str
    passed: bool
    notes: Tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class RegistryHandoffReadiness:
    target_ref: str
    readiness_recorded: bool
    entered_this_phase: bool


@dataclass(frozen=True)
class ModelVersionDependencyRegistryDecision:
    decision_ref: str
    registry_profile_count: int
    model_identity_record_count: int
    model_version_record_count: int
    package_dependency_record_count: int
    import_name_binding_record_count: int
    weight_version_record_count: int
    runtime_backend_record_count: int
    environment_constraint_record_count: int
    hardware_requirement_record_count: int
    license_dependency_binding_record_count: int
    optional_dependency_group_record_count: int
    probe_policy_record_count: int
    compatibility_constraint_record_count: int
    fallback_compatibility_record_count: int
    version_lock_policy_count: int
    dependency_risk_record_count: int
    negative_guard_count: int
    negative_guard_passed: int
    test_board_record_count: int
    blocker_count: int
    final_decision: str


def candidate_to_dict(obj: Any) -> Dict[str, Any]:
    return asdict(obj)
