# -*- coding: utf-8 -*-
"""Recognition Model Output Adapter Integration Planning — review v1."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.field_understanding.recognition_model_output_adapter_integration_planning.recognition_model_output_adapter_integration_planning_registry_v1 import (
    REGISTRY_ID,
    build_recognition_model_planning_matrix_v1,
    validate_registry,
)
from capabilities.field_understanding.recognition_model_output_adapter_integration_planning.recognition_model_output_adapter_integration_planning_types_v1 import (
    ADAPTER_MAPPING_IDS,
    CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
    FINAL_DECISION_BLOCKED,
    FINAL_DECISION_GO,
    INTERFACE_ADAPTER_REF,
    MODEL_FAMILY_IDS,
    NEXT_PHASE_REF,
    NON_EXECUTION_FLAGS,
    PHASE_ID,
    PLANNING_GOVERNANCE_RULES,
    PLANNING_PRINCIPLE_ZH,
    RUNTIME_TRIAL_MODE,
    SCENARIO_IDS,
    SOURCE_CHAIN,
    TARGET_CHAIN_REF,
    TARGET_ENTRYPOINT,
)
from capabilities.midplatform.controlled_trial_governance.controlled_trial_governance_lifecycle_template_v1 import (
    TEMPLATE_ID,
)

DEFAULT_OUTPUT_ROOT = (
    _REPO_ROOT
    / "_tmp_eval_out"
    / "recognition_model_output_adapter_integration_planning_v1_smoke_v0"
)
REVIEW_FILENAME = "recognition_model_output_adapter_integration_planning_review_v1.json"

_PKG = (
    "capabilities/field_understanding/recognition_model_output_adapter_integration_planning"
)
STEP_FILES = (
    f"{_PKG}/recognition_model_output_adapter_integration_planning_types_v1.py",
    f"{_PKG}/recognition_model_output_adapter_integration_planning_registry_v1.py",
    f"{_PKG}/review_recognition_model_output_adapter_integration_planning_v1.py",
)

_REQUIRED_VERIFY_FLAGS: Tuple[str, ...] = (
    "phase_one_evidence_main_chain_closure_go_verified",
    "rgb_vision_evidence_chain_closure_go_verified",
    "slam_backend_evidence_chain_closure_go_verified",
    "rgb_slam_cross_modal_closure_go_verified",
    "field_task_guidance_safety_chain_closure_go_verified",
    "runtime_governance_closure_go_verified",
    "interface_layer_governance_verified",
    "model_admission_governance_verified",
)


def _load_upstream_artifact(artifact_rel: str) -> Tuple[Optional[Dict[str, Any]], bool]:
    path = _REPO_ROOT / artifact_rel
    if not path.is_file():
        return None, False
    try:
        return json.loads(path.read_text(encoding="utf-8")), True
    except (OSError, json.JSONDecodeError):
        return None, True


def review_sealed_upstream_artifacts(matrix: Dict[str, Any]) -> Tuple[Dict[str, bool], List[str]]:
    issues: List[str] = []
    checks: Dict[str, bool] = {}

    for entry in matrix.get("sealed_upstream_go_artifacts") or []:
        phase_ref = entry["phase_ref"]
        module_path = _REPO_ROOT / entry["module_rel"]
        checks[f"{phase_ref}.module_present"] = module_path.is_file()
        if not module_path.is_file():
            issues.append(f"upstream_module_missing:{phase_ref}")

        artifact, exists = _load_upstream_artifact(entry["artifact_rel"])
        checks[f"{phase_ref}.artifact_present"] = exists
        if not exists:
            issues.append(f"upstream_artifact_missing:{phase_ref}")
            continue

        actual_go = (artifact or {}).get("final_decision")
        go_ok = actual_go == entry["expected_go"]
        checks[f"{phase_ref}.go_sealed"] = go_ok
        if not go_ok:
            issues.append(f"upstream_go_mismatch:{phase_ref}:{actual_go!r}")

        verify_flag = entry.get("verify_flag")
        if verify_flag:
            checks[verify_flag] = go_ok

    checks["controlled_trial_governance_template_ref_ok"] = (
        CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF == TEMPLATE_ID
    )
    for required in _REQUIRED_VERIFY_FLAGS:
        if not checks.get(required, False):
            issues.append(f"{required}_not_verified")

    return checks, issues


def review_recognition_model_output_adapter_integration_planning_v1(
    *,
    output_root: Optional[str] = None,
    write_file: bool = True,
) -> Dict[str, Any]:
    matrix = build_recognition_model_planning_matrix_v1()
    registry_ok, registry_issues = validate_registry()

    failed_checks: List[str] = []
    passed_checks: List[str] = []

    for rel in STEP_FILES:
        if (_REPO_ROOT / rel).is_file():
            passed_checks.append(f"step.file_present={rel.split('/')[-1]}")
        else:
            failed_checks.append(f"step.file_missing={rel}")

    if registry_ok:
        passed_checks.append("registry_validation_ok=true")
    else:
        failed_checks.extend(registry_issues)

    upstream_checks, upstream_issues = review_sealed_upstream_artifacts(matrix)
    failed_checks.extend(upstream_issues)

    families = {m["model_family_id"]: m for m in matrix.get("model_families") or []}
    mappings = {a["adapter_mapping_id"]: a for a in matrix.get("adapter_mappings") or []}
    safety = matrix.get("safety_boundary_policy") or {}
    admission = matrix.get("admission_boundary_policy") or {}
    profile = matrix.get("planning_profile") or {}

    template_ok = profile.get("controlled_trial_governance_template_ref") == TEMPLATE_ID

    family_registered = {
        f"{fid}_registered": families.get(fid, {}).get("registered") is True
        for fid in MODEL_FAMILY_IDS
    }
    # GO key naming uses short forms for some mappings.
    mapping_go_alias = {
        "text_output_to_text_evidence_mapping": "text_output_to_text_evidence_mapping_supported",
        "detection_output_to_object_evidence_mapping": (
            "detection_output_to_object_evidence_mapping_supported"
        ),
        "segmentation_output_to_region_evidence_mapping": (
            "segmentation_output_to_region_evidence_mapping_supported"
        ),
        "tracking_output_to_track_dynamic_risk_mapping": (
            "tracking_output_to_track_dynamic_risk_mapping_supported"
        ),
        "depth_output_to_spatial_hint_mapping": "depth_output_to_spatial_hint_mapping_supported",
        "visual_symbol_output_mapping": "visual_symbol_output_mapping_supported",
        "scene_relation_output_mapping": "scene_relation_output_mapping_supported",
        "uncertainty_conflict_output_mapping": "uncertainty_conflict_output_mapping_supported",
    }
    mapping_supported = {
        mapping_go_alias[mid]: mappings.get(mid, {}).get("supported") is True
        for mid in ADAPTER_MAPPING_IDS
    }

    go_conditions = {
        "planning_profile_count_eq_1": True,
        "model_family_policy_count_gte_7": matrix.get("model_family_policy_count", 0) >= 7,
        "adapter_mapping_policy_count_gte_8": (
            matrix.get("adapter_mapping_policy_count", 0) >= 8
        ),
        "scenario_count_gte_8": matrix.get("scenario_count", 0) >= 8,
        "phase_one_evidence_main_chain_closure_go_verified": (
            upstream_checks.get("phase_one_evidence_main_chain_closure_go_verified") is True
        ),
        "rgb_vision_evidence_chain_closure_go_verified": (
            upstream_checks.get("rgb_vision_evidence_chain_closure_go_verified") is True
        ),
        "slam_backend_evidence_chain_closure_go_verified": (
            upstream_checks.get("slam_backend_evidence_chain_closure_go_verified") is True
        ),
        "rgb_slam_cross_modal_closure_go_verified": (
            upstream_checks.get("rgb_slam_cross_modal_closure_go_verified") is True
        ),
        "field_task_guidance_safety_chain_closure_go_verified": (
            upstream_checks.get("field_task_guidance_safety_chain_closure_go_verified") is True
        ),
        "runtime_governance_closure_go_verified": (
            upstream_checks.get("runtime_governance_closure_go_verified") is True
        ),
        "interface_layer_governance_verified": (
            upstream_checks.get("interface_layer_governance_verified") is True
        ),
        "model_admission_governance_verified": (
            upstream_checks.get("model_admission_governance_verified") is True
        ),
        "controlled_trial_governance_template_ref_ok": template_ok is True,
        **family_registered,
        **mapping_supported,
        "model_output_adapter_required": (
            admission.get("model_output_adapter_required") is True
        ),
        "native_model_output_direct_to_field_blocked": (
            admission.get("native_model_output_direct_to_field_blocked") is True
        ),
        "source_chain_required": admission.get("source_chain_required") is True,
        "license_ref_required": admission.get("license_ref_required") is True,
        "model_origin_required": admission.get("model_origin_required") is True,
        "confidence_required": admission.get("confidence_required") is True,
        "adapter_mapping_ref_required": admission.get("adapter_mapping_ref_required") is True,
        "ocr_output_not_fact": safety.get("ocr_output_not_fact") is True,
        "object_identity_not_fact": safety.get("object_identity_not_fact") is True,
        "segmentation_not_route_activation": (
            safety.get("segmentation_not_route_activation") is True
        ),
        "tracking_not_action_trigger": safety.get("tracking_not_action_trigger") is True,
        "depth_vio_not_field_identity": safety.get("depth_vio_not_field_identity") is True,
        "color_shape_symbol_not_fact": safety.get("color_shape_symbol_not_fact") is True,
        "visual_symbol_requires_context_validation": (
            safety.get("visual_symbol_requires_context_validation") is True
        ),
        "scene_relation_not_final_interpretation": (
            safety.get("scene_relation_not_final_interpretation") is True
        ),
        "field_task_guidance_candidate_only": (
            safety.get("field_task_guidance_candidate_only") is True
        ),
        "guidance_candidate_remains_candidate": (
            safety.get("guidance_candidate_remains_candidate") is True
        ),
        "speech_gate_candidate_not_tts": safety.get("speech_gate_candidate_not_tts") is True,
        "action_safety_candidate_exists": (
            safety.get("action_safety_candidate_exists") is True
        ),
        "model_runtime_execution_allowed_false": (
            NON_EXECUTION_FLAGS["model_runtime_execution_allowed"] is False
        ),
        "model_download_allowed_false": NON_EXECUTION_FLAGS["model_download_allowed"] is False,
        "model_repo_clone_allowed_false": (
            NON_EXECUTION_FLAGS["model_repo_clone_allowed"] is False
        ),
        "model_build_allowed_false": NON_EXECUTION_FLAGS["model_build_allowed"] is False,
        "real_inference_allowed_false": NON_EXECUTION_FLAGS["real_inference_allowed"] is False,
        "dataset_download_allowed_false": NON_EXECUTION_FLAGS["dataset_download_allowed"] is False,
        "training_use_allowed_false": NON_EXECUTION_FLAGS["training_use_allowed"] is False,
        "runtime_activation_allowed_false": (
            NON_EXECUTION_FLAGS["runtime_activation_allowed"] is False
        ),
        "live_camera_connected_false": NON_EXECUTION_FLAGS["live_camera_connected"] is False,
        "live_sensor_connected_false": NON_EXECUTION_FLAGS["live_sensor_connected"] is False,
        "direct_action_allowed_false": NON_EXECUTION_FLAGS["direct_action_allowed"] is False,
        "direct_speech_allowed_false": NON_EXECUTION_FLAGS["direct_speech_allowed"] is False,
        "direct_fact_write_allowed_false": (
            NON_EXECUTION_FLAGS["direct_fact_write_allowed"] is False
        ),
        "commercial_runtime_approved_false": (
            NON_EXECUTION_FLAGS["commercial_runtime_approved"] is False
        ),
    }

    for key, ok in go_conditions.items():
        if ok:
            passed_checks.append(f"go.{key}=true")
        else:
            failed_checks.append(f"go.{key}=false")

    blocker_count = len(failed_checks)
    review_ok = registry_ok and blocker_count == 0

    review_checkpoints: Dict[str, Any] = {
        "planning_profile_count": 1,
        "model_family_policy_count": matrix.get("model_family_policy_count"),
        "adapter_mapping_policy_count": matrix.get("adapter_mapping_policy_count"),
        "scenario_count": matrix.get("scenario_count"),
        "model_family_ids": list(MODEL_FAMILY_IDS),
        "adapter_mapping_ids": list(ADAPTER_MAPPING_IDS),
        "scenario_ids": list(SCENARIO_IDS),
        "runtime_trial_mode": RUNTIME_TRIAL_MODE,
        "target_entrypoint": TARGET_ENTRYPOINT,
        "target_chain_ref": TARGET_CHAIN_REF,
        "interface_adapter_ref": INTERFACE_ADAPTER_REF,
        "controlled_trial_governance_template_ref": CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
        **upstream_checks,
        **NON_EXECUTION_FLAGS,
    }

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "step": "Recognition Model Output Adapter Integration Planning Review",
        "lifecycle_variant": "recognition_model_output_adapter_integration_planning",
        "planning_principle_zh": PLANNING_PRINCIPLE_ZH,
        "registry_id": REGISTRY_ID,
        "source_chain": SOURCE_CHAIN,
        "runtime_trial_mode": RUNTIME_TRIAL_MODE,
        "target_entrypoint": TARGET_ENTRYPOINT,
        "target_chain_ref": TARGET_CHAIN_REF,
        "interface_adapter_ref": INTERFACE_ADAPTER_REF,
        "controlled_trial_governance_template_ref": CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
        "planning_governance_rules": list(PLANNING_GOVERNANCE_RULES),
        "non_execution_flags": dict(NON_EXECUTION_FLAGS),
        "registry_validation_ok": registry_ok,
        "upstream_sealed_phase_review": upstream_checks,
        "go_conditions": go_conditions,
        "review_checkpoints": review_checkpoints,
        "recognition_model_planning_matrix": matrix,
        "conclusions": {
            "recognition_model_output_adapter_integration_planning_status": (
                "recognition_model_output_adapter_integration_planning_ready"
                if review_ok
                else "blocked"
            ),
            "model_families_planned": list(MODEL_FAMILY_IDS),
            "adapter_mappings_planned": list(ADAPTER_MAPPING_IDS),
            "scenarios_planned": list(SCENARIO_IDS),
            "next_phase_ref": NEXT_PHASE_REF,
            "pipeline_summary": {
                "input": "model_native_output",
                "adapter": INTERFACE_ADAPTER_REF,
                "candidate": "luna_evidence_candidate",
                "chain": TARGET_CHAIN_REF,
                "path": "evidence_main_chain -> field_synthesis_v1",
            },
            "transition_note": (
                "Recognition-model integration layer planned: model output -> Interface Adapter -> "
                "Luna evidence candidate -> frozen evidence main chain. No model download / build / "
                "real inference. Next: Phase-Recognition-Model-Output-Adapter-DryRun-v1-001 using "
                "local mock-but-file-based model output samples to validate the adapter before any "
                "real model download or recognition."
            ),
        },
        "blocker_count": blocker_count,
        "failed_checks": failed_checks,
        "passed_checks": passed_checks,
        "final_decision": FINAL_DECISION_GO if review_ok else FINAL_DECISION_BLOCKED,
    }

    if write_file:
        out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
        out_root.mkdir(parents=True, exist_ok=True)
        out_path = out_root / REVIEW_FILENAME
        out_path.write_text(
            json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        result["output_review_file"] = str(out_path)

    return result


def main() -> int:
    result = review_recognition_model_output_adapter_integration_planning_v1()
    cp = result["review_checkpoints"]
    print(
        json.dumps(
            {
                "output_review_file": result.get("output_review_file"),
                "model_family_policy_count": cp["model_family_policy_count"],
                "adapter_mapping_policy_count": cp["adapter_mapping_policy_count"],
                "scenario_count": cp["scenario_count"],
                "blocker_count": result["blocker_count"],
                "final_decision": result["final_decision"],
            },
            ensure_ascii=False,
        )
    )
    return 0 if result["final_decision"] == FINAL_DECISION_GO else 1


if __name__ == "__main__":
    raise SystemExit(main())
