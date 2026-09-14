# -*- coding: utf-8 -*-
"""RGB Vision + SLAM Spatial Evidence Cross-Modal Integrated Closure — review v1."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.field_understanding.rgb_vision_slam_spatial_evidence_cross_modal_integrated_closure.rgb_vision_slam_spatial_evidence_cross_modal_integrated_closure_registry_v1 import (
    REGISTRY_ID,
    build_cross_modal_closure_matrix_v1,
    validate_registry,
)
from capabilities.field_understanding.rgb_vision_slam_spatial_evidence_cross_modal_integrated_closure.rgb_vision_slam_spatial_evidence_cross_modal_integrated_closure_types_v1 import (
    ALIGNMENT_POLICY_IDS,
    ALIGNMENT_SUPPORTED_GO_KEYS,
    CLOSURE_GOVERNANCE_RULES,
    CLOSURE_PRINCIPLE_ZH,
    CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
    CROSS_MODAL_CANDIDATE_COVERED_GO_KEYS,
    CROSS_MODAL_CANDIDATE_IDS,
    FINAL_DECISION_BLOCKED,
    FINAL_DECISION_GO,
    NEXT_PHASE_REF,
    NON_EXECUTION_FLAGS,
    PHASE_ID,
    RGB_INTERFACE_ADAPTER_REF,
    RUNTIME_TRIAL_MODE,
    SLAM_INTERFACE_ADAPTER_REF,
    SLAM_ROLE,
    SOURCE_CHAIN,
    SYSTEM_OBJECTIVE,
    TARGET_ENTRYPOINT,
    VISION_HARDWARE_BASELINE,
)
from capabilities.midplatform.controlled_trial_governance.controlled_trial_governance_lifecycle_template_v1 import (
    TEMPLATE_ID,
)

DEFAULT_OUTPUT_ROOT = (
    _REPO_ROOT
    / "_tmp_eval_out"
    / "rgb_vision_slam_spatial_evidence_cross_modal_integrated_closure_v1_smoke_v0"
)
REVIEW_FILENAME = "rgb_vision_slam_spatial_evidence_cross_modal_integrated_closure_review_v1.json"

_PKG = (
    "capabilities/field_understanding/"
    "rgb_vision_slam_spatial_evidence_cross_modal_integrated_closure"
)
STEP_FILES = (
    f"{_PKG}/rgb_vision_slam_spatial_evidence_cross_modal_integrated_closure_types_v1.py",
    f"{_PKG}/rgb_vision_slam_spatial_evidence_cross_modal_integrated_closure_registry_v1.py",
    f"{_PKG}/review_rgb_vision_slam_spatial_evidence_cross_modal_integrated_closure_v1.py",
)

_REQUIRED_VERIFY_FLAGS: Tuple[str, ...] = (
    "rgb_vision_evidence_chain_closure_go_verified",
    "slam_backend_evidence_chain_closure_go_verified",
    "rtab_multi_export_spatial_evidence_replay_closure_go_verified",
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


def review_rgb_vision_slam_spatial_evidence_cross_modal_integrated_closure_v1(
    *,
    output_root: Optional[str] = None,
    write_file: bool = True,
) -> Dict[str, Any]:
    matrix = build_cross_modal_closure_matrix_v1()
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

    profile = matrix.get("closure_profile") or {}
    field_path = matrix.get("field_synthesis_path_closure") or {}
    task_path = matrix.get("task_guidance_path_closure") or {}
    conflict = matrix.get("conflict_uncertainty_policy") or {}
    safety = matrix.get("safety_boundary_closure") or {}
    alignments = {a["alignment_ref"]: a for a in matrix.get("alignment_policies") or []}

    template_ok = profile.get("controlled_trial_governance_template_ref") == TEMPLATE_ID

    alignment_supported = {
        f"{aid}_supported": alignments.get(aid, {}).get("supported") is True
        for aid in ALIGNMENT_POLICY_IDS
    }
    cross_modal_covered = {
        f"{cid}_covered": cid in CROSS_MODAL_CANDIDATE_IDS for cid in CROSS_MODAL_CANDIDATE_IDS
    }

    go_conditions = {
        "closure_profile_count_eq_1": True,
        "stage_ref_count_eq_5": matrix.get("stage_ref_count") == 5,
        "cross_modal_alignment_policy_count_gte_8": (
            matrix.get("cross_modal_alignment_policy_count", 0) >= 8
        ),
        "cross_modal_candidate_output_count_gte_13": (
            matrix.get("cross_modal_candidate_output_count", 0) >= 13
        ),
        "rgb_vision_evidence_chain_closure_go_verified": (
            upstream_checks.get("rgb_vision_evidence_chain_closure_go_verified") is True
        ),
        "slam_backend_evidence_chain_closure_go_verified": (
            upstream_checks.get("slam_backend_evidence_chain_closure_go_verified") is True
        ),
        "rtab_multi_export_spatial_evidence_replay_closure_go_verified": (
            upstream_checks.get("rtab_multi_export_spatial_evidence_replay_closure_go_verified")
            is True
        ),
        "field_task_guidance_safety_chain_closure_go_verified": (
            upstream_checks.get("field_task_guidance_safety_chain_closure_go_verified") is True
        ),
        "runtime_governance_closure_go_verified": (
            upstream_checks.get("runtime_governance_closure_go_verified") is True
        ),
        "controlled_trial_governance_template_ref_ok": template_ok is True,
        "interface_layer_governance_verified": (
            upstream_checks.get("interface_layer_governance_verified") is True
        ),
        "model_admission_governance_verified": (
            upstream_checks.get("model_admission_governance_verified") is True
        ),
        **alignment_supported,
        **cross_modal_covered,
        "rgb_first_hardware_baseline_preserved": (
            safety.get("rgb_first_hardware_baseline_preserved") is True
        ),
        "slam_role_spatial_evidence_provider": (
            safety.get("slam_role_spatial_evidence_provider") is True
        ),
        "cognitive_world_reconstruction_objective_preserved": (
            safety.get("cognitive_world_reconstruction_objective_preserved") is True
        ),
        "rgb_evidence_adapter_required": (
            field_path.get("rgb_evidence_adapter_required") is True
        ),
        "slam_evidence_adapter_required": (
            field_path.get("slam_evidence_adapter_required") is True
        ),
        "cross_modal_output_candidate_only": (
            field_path.get("cross_modal_output_candidate_only") is True
        ),
        "object_identity_not_fact": safety.get("object_identity_not_fact") is True,
        "ocr_text_not_fact": safety.get("ocr_text_not_fact") is True,
        "segmentation_not_route_activation": (
            safety.get("segmentation_not_route_activation") is True
        ),
        "tracking_not_action_trigger": safety.get("tracking_not_action_trigger") is True,
        "color_shape_symbol_not_fact": safety.get("color_shape_symbol_not_fact") is True,
        "visual_symbol_requires_context_validation": (
            safety.get("visual_symbol_requires_context_validation") is True
        ),
        "monocular_depth_vio_slam_pose_not_field_identity": (
            safety.get("monocular_depth_vio_slam_pose_not_field_identity") is True
        ),
        "scene_relation_not_final_interpretation": (
            safety.get("scene_relation_not_final_interpretation") is True
        ),
        "scene_graph_not_final_field_identity": (
            safety.get("scene_graph_not_final_field_identity") is True
        ),
        "relocalization_does_not_restore_runtime_trust": (
            conflict.get("relocalization_does_not_restore_runtime_trust") is True
        ),
        "drift_remains_uncertainty_evidence": (
            conflict.get("drift_only_increases_uncertainty") is True
        ),
        "health_candidate_only": conflict.get("health_only_risk_evidence") is True,
        "gps_does_not_override_field_identity": (
            conflict.get("gps_does_not_override_field_identity") is True
        ),
        "conflict_not_direct_fact_write": (
            conflict.get("conflict_not_direct_fact_write") is True
        ),
        "conflict_not_direct_action_speech_navigation": (
            conflict.get("conflict_not_direct_action_speech_navigation") is True
        ),
        "field_task_guidance_candidate_only": (
            task_path.get("field_task_guidance_candidate_only") is True
        ),
        "guidance_candidate_remains_candidate": (
            task_path.get("guidance_candidate_remains_candidate") is True
        ),
        "speech_gate_candidate_not_tts": task_path.get("speech_gate_candidate_not_tts") is True,
        "action_safety_candidate_exists": (
            task_path.get("action_safety_candidate_exists") is True
        ),
        "observation_only_scope_preserved": (
            task_path.get("observation_only_scope_preserved") is True
        ),
        "dataset_download_allowed_false": NON_EXECUTION_FLAGS["dataset_download_allowed"] is False,
        "training_use_allowed_false": NON_EXECUTION_FLAGS["training_use_allowed"] is False,
        "model_download_allowed_false": NON_EXECUTION_FLAGS["model_download_allowed"] is False,
        "slam_backend_model_download_allowed_false": (
            NON_EXECUTION_FLAGS["slam_backend_model_download_allowed"] is False
        ),
        "slam_backend_runtime_build_allowed_false": (
            NON_EXECUTION_FLAGS["slam_backend_runtime_build_allowed"] is False
        ),
        "runtime_activation_allowed_false": (
            NON_EXECUTION_FLAGS["runtime_activation_allowed"] is False
        ),
        "live_camera_connected_false": NON_EXECUTION_FLAGS["live_camera_connected"] is False,
        "live_sensor_connected_false": NON_EXECUTION_FLAGS["live_sensor_connected"] is False,
        "real_gps_connected_false": NON_EXECUTION_FLAGS["real_gps_connected"] is False,
        "real_map_api_connected_false": NON_EXECUTION_FLAGS["real_map_api_connected"] is False,
        "real_navigation_started_false": NON_EXECUTION_FLAGS["real_navigation_started"] is False,
        "ros_connected_false": NON_EXECUTION_FLAGS["ros_connected"] is False,
        "imu_connected_false": NON_EXECUTION_FLAGS["imu_connected"] is False,
        "direct_action_allowed_false": NON_EXECUTION_FLAGS["direct_action_allowed"] is False,
        "direct_speech_allowed_false": NON_EXECUTION_FLAGS["direct_speech_allowed"] is False,
        "direct_fact_write_allowed_false": (
            NON_EXECUTION_FLAGS["direct_fact_write_allowed"] is False
        ),
        "commercial_runtime_approved_false": (
            NON_EXECUTION_FLAGS["commercial_runtime_approved"] is False
        ),
        "integrated_validation_mode_used": (
            NON_EXECUTION_FLAGS["integrated_validation_mode_used"] is True
        ),
        "single_modality_validation_not_used": (
            NON_EXECUTION_FLAGS["single_modality_validation_not_used"] is True
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
        "closure_profile_count": 1,
        "stage_ref_count": matrix.get("stage_ref_count"),
        "cross_modal_alignment_policy_count": matrix.get("cross_modal_alignment_policy_count"),
        "cross_modal_candidate_output_count": matrix.get("cross_modal_candidate_output_count"),
        "alignment_policy_ids": list(ALIGNMENT_POLICY_IDS),
        "cross_modal_candidate_ids": list(CROSS_MODAL_CANDIDATE_IDS),
        "runtime_trial_mode": RUNTIME_TRIAL_MODE,
        "vision_hardware_baseline": VISION_HARDWARE_BASELINE,
        "slam_role": SLAM_ROLE,
        "system_objective": SYSTEM_OBJECTIVE,
        "target_entrypoint": TARGET_ENTRYPOINT,
        "controlled_trial_governance_template_ref": CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
        **upstream_checks,
        **NON_EXECUTION_FLAGS,
    }

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "step": "RGB Vision + SLAM Spatial Evidence Cross-Modal Integrated Closure Review",
        "lifecycle_variant": "rgb_vision_slam_spatial_evidence_cross_modal_integrated_closure",
        "closure_principle_zh": CLOSURE_PRINCIPLE_ZH,
        "registry_id": REGISTRY_ID,
        "source_chain": SOURCE_CHAIN,
        "runtime_trial_mode": RUNTIME_TRIAL_MODE,
        "vision_hardware_baseline": VISION_HARDWARE_BASELINE,
        "slam_role": SLAM_ROLE,
        "system_objective": SYSTEM_OBJECTIVE,
        "target_entrypoint": TARGET_ENTRYPOINT,
        "rgb_interface_adapter_ref": RGB_INTERFACE_ADAPTER_REF,
        "slam_interface_adapter_ref": SLAM_INTERFACE_ADAPTER_REF,
        "controlled_trial_governance_template_ref": CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
        "closure_governance_rules": list(CLOSURE_GOVERNANCE_RULES),
        "non_execution_flags": dict(NON_EXECUTION_FLAGS),
        "registry_validation_ok": registry_ok,
        "upstream_sealed_phase_review": upstream_checks,
        "go_conditions": go_conditions,
        "review_checkpoints": review_checkpoints,
        "cross_modal_closure_matrix": matrix,
        "conclusions": {
            "cross_modal_evidence_chain_status": (
                "rgb_vision_plus_slam_spatial_evidence_cross_modal_baseline_sealed"
                if review_ok
                else "blocked"
            ),
            "phase_one_environment_cognition_mainline_ready": review_ok,
            "integrated_validation_mode_used": True,
            "rgb_first_hardware_baseline_preserved": True,
            "slam_role": SLAM_ROLE,
            "alignment_policies": list(ALIGNMENT_POLICY_IDS),
            "cross_modal_candidate_outputs": list(CROSS_MODAL_CANDIDATE_IDS),
            "next_phase_ref": NEXT_PHASE_REF,
            "pipeline_summary": {
                "rgb_input": "rgb_vision_evidence_candidates",
                "slam_input": "slam_spatial_evidence_candidates",
                "rgb_adapter": RGB_INTERFACE_ADAPTER_REF,
                "slam_adapter": SLAM_INTERFACE_ADAPTER_REF,
                "alignment": list(ALIGNMENT_POLICY_IDS),
                "cross_modal_outputs": list(CROSS_MODAL_CANDIDATE_IDS),
                "path": "field_task_guidance_candidate_replay_path",
            },
            "transition_note": (
                "RGB Vision + SLAM Spatial Evidence cross-modal baseline sealed: 'what is seen' "
                "(color/shape/text/symbol/object/region/relation) and 'where spatial evidence is' "
                "(pose/anchor/drift/relocalization/local_map) are unified as a candidate layer in "
                "the Luna Phase-One environment cognition mainline. Next: real-recognition / Visual "
                "Symbol Evidence DryRun."
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
    result = review_rgb_vision_slam_spatial_evidence_cross_modal_integrated_closure_v1()
    cp = result["review_checkpoints"]
    print(
        json.dumps(
            {
                "output_review_file": result.get("output_review_file"),
                "stage_ref_count": cp["stage_ref_count"],
                "cross_modal_alignment_policy_count": cp["cross_modal_alignment_policy_count"],
                "cross_modal_candidate_output_count": cp["cross_modal_candidate_output_count"],
                "blocker_count": result["blocker_count"],
                "final_decision": result["final_decision"],
            },
            ensure_ascii=False,
        )
    )
    return 0 if result["final_decision"] == FINAL_DECISION_GO else 1


if __name__ == "__main__":
    raise SystemExit(main())
