# -*- coding: utf-8 -*-
"""SLAM Backend Real File Output Integrated Admission Planning — review v1."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.field_understanding.slam_backend_real_file_output_integrated_admission_planning.slam_backend_real_file_output_integrated_admission_planning_registry_v1 import (
    REGISTRY_ID,
    build_slam_backend_planning_matrix_v1,
    validate_registry,
)
from capabilities.field_understanding.slam_backend_real_file_output_integrated_admission_planning.slam_backend_real_file_output_integrated_admission_planning_types_v1 import (
    BACKEND_REGISTERED_GO_KEYS,
    CANDIDATE_MAPPING_GO_KEYS,
    CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
    FINAL_DECISION_BLOCKED,
    FINAL_DECISION_GO,
    GENERIC_JSON_PARSER_REF,
    INTEGRATED_SCENARIO_GO_KEYS,
    INTERFACE_ADAPTER_REF,
    NEXT_PHASE_REF,
    NON_EXECUTION_FLAGS,
    PHASE_ID,
    PLANNING_GOVERNANCE_RULES,
    PLANNING_PRINCIPLE_ZH,
    RUNTIME_TRIAL_MODE,
    SOURCE_CHAIN,
    SOURCE_FAMILY,
    TARGET_ENTRYPOINT,
    TARGET_INTERNAL_FORMAT,
)
from capabilities.midplatform.controlled_trial_governance.controlled_trial_governance_lifecycle_template_v1 import (
    TEMPLATE_ID,
)

DEFAULT_OUTPUT_ROOT = (
    _REPO_ROOT
    / "_tmp_eval_out"
    / "slam_backend_real_file_output_integrated_admission_planning_v1_smoke_v0"
)
REVIEW_FILENAME = "slam_backend_real_file_output_integrated_admission_planning_review_v1.json"

_PKG = "capabilities/field_understanding/slam_backend_real_file_output_integrated_admission_planning"
STEP_FILES = (
    f"{_PKG}/slam_backend_real_file_output_integrated_admission_planning_types_v1.py",
    f"{_PKG}/slam_backend_real_file_output_integrated_admission_planning_registry_v1.py",
    f"{_PKG}/review_slam_backend_real_file_output_integrated_admission_planning_v1.py",
)

_REQUIRED_VERIFY_FLAGS: Tuple[str, ...] = (
    "tum_real_file_loader_dryrun_go_verified",
    "rtab_multi_export_spatial_evidence_replay_closure_go_verified",
    "generic_json_spatial_trace_parser_go_verified",
    "slam_spatial_evidence_chain_field_alignment_closure_go_verified",
    "field_task_guidance_safety_chain_closure_go_verified",
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
            if entry.get("require_go", True):
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


def review_slam_backend_real_file_output_integrated_admission_planning_v1(
    *,
    output_root: Optional[str] = None,
    write_file: bool = True,
) -> Dict[str, Any]:
    matrix = build_slam_backend_planning_matrix_v1()
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

    profile = matrix.get("slam_backend_planning_profile") or {}
    license_policy = matrix.get("license_boundary_policy") or {}
    format_policy = matrix.get("format_admission_policy") or {}
    mapping_policy = matrix.get("mapping_policy") or {}
    replay_policy = matrix.get("replay_boundary_policy") or {}
    backend_registered = matrix.get("backend_registered_map") or {}
    scenario_support = matrix.get("scenario_support_map") or {}
    candidate_support = matrix.get("candidate_mapping_support_map") or {}

    template_ok = profile.get("controlled_trial_governance_template_ref") == TEMPLATE_ID

    review_checkpoints: Dict[str, Any] = {
        "planning_profile_count": 1,
        "slam_backend_source_policy_count": matrix.get("slam_backend_source_policy_count", 0),
        "integrated_scenario_count": matrix.get("integrated_scenario_count", 0),
        "tum_real_file_loader_dryrun_go_verified": upstream_checks.get(
            "tum_real_file_loader_dryrun_go_verified", False
        ),
        "rtab_multi_export_spatial_evidence_replay_closure_go_verified": upstream_checks.get(
            "rtab_multi_export_spatial_evidence_replay_closure_go_verified", False
        ),
        "generic_json_spatial_trace_parser_go_verified": upstream_checks.get(
            "generic_json_spatial_trace_parser_go_verified", False
        ),
        "slam_spatial_evidence_chain_field_alignment_closure_go_verified": upstream_checks.get(
            "slam_spatial_evidence_chain_field_alignment_closure_go_verified", False
        ),
        "field_task_guidance_safety_chain_closure_go_verified": upstream_checks.get(
            "field_task_guidance_safety_chain_closure_go_verified", False
        ),
        "interface_layer_governance_verified": upstream_checks.get(
            "interface_layer_governance_verified", False
        ),
        "model_admission_governance_verified": upstream_checks.get(
            "model_admission_governance_verified", False
        ),
        "controlled_trial_governance_template_ref_ok": template_ok,
        "adapter_required": format_policy.get("adapter_required") is True,
        "native_output_direct_to_field_blocked": (
            replay_policy.get("backend_native_output_direct_to_field_blocked") is True
        ),
        "source_chain_required": format_policy.get("source_chain_required") is True,
        "confidence_required": format_policy.get("confidence_required") is True,
        "license_ref_required": format_policy.get("license_ref_required") is True,
        "gpl_or_incompatible_backend_technical_reference_only": (
            license_policy.get("gpl_or_incompatible_backend_technical_reference_only") is True
        ),
        "vio_slam_pose_not_field_identity": (
            replay_policy.get("vio_slam_pose_not_field_identity") is True
        ),
        "gps_does_not_override_field_identity": (
            replay_policy.get("gps_does_not_override_field_identity") is True
        ),
        "relocalization_does_not_restore_runtime_trust": (
            replay_policy.get("relocalization_does_not_restore_runtime_trust") is True
        ),
        "drift_remains_uncertainty_evidence": (
            replay_policy.get("drift_remains_uncertainty_evidence") is True
        ),
        "health_candidate_only": replay_policy.get("health_candidate_only") is True,
        "semantic_label_not_fact": mapping_policy.get("semantic_label_not_fact") is True,
        "scene_graph_not_final_field_identity": (
            mapping_policy.get("scene_graph_not_final_field_identity") is True
        ),
        "heavy_neural_gaussian_runtime_not_admitted": (
            replay_policy.get("heavy_neural_gaussian_runtime_not_admitted") is True
        ),
        "field_task_guidance_candidate_only": (
            replay_policy.get("field_task_guidance_candidate_only") is True
        ),
        **backend_registered,
        **scenario_support,
        **candidate_support,
        "runtime_trial_mode_locked": RUNTIME_TRIAL_MODE,
        "source_family_locked": SOURCE_FAMILY,
        "target_internal_format_locked": TARGET_INTERNAL_FORMAT,
        "target_entrypoint_locked": TARGET_ENTRYPOINT,
        **NON_EXECUTION_FLAGS,
    }

    go_conditions = {
        "planning_profile_count_eq_1": review_checkpoints["planning_profile_count"] == 1,
        "slam_backend_source_policy_count_gte_7": (
            review_checkpoints["slam_backend_source_policy_count"] >= 7
        ),
        "integrated_scenario_count_eq_8": (
            review_checkpoints["integrated_scenario_count"] == 8
        ),
        "tum_real_file_loader_dryrun_go_verified": (
            review_checkpoints["tum_real_file_loader_dryrun_go_verified"] is True
        ),
        "rtab_multi_export_spatial_evidence_replay_closure_go_verified": (
            review_checkpoints["rtab_multi_export_spatial_evidence_replay_closure_go_verified"]
            is True
        ),
        "generic_json_spatial_trace_parser_go_verified": (
            review_checkpoints["generic_json_spatial_trace_parser_go_verified"] is True
        ),
        "slam_spatial_evidence_chain_field_alignment_closure_go_verified": (
            review_checkpoints["slam_spatial_evidence_chain_field_alignment_closure_go_verified"]
            is True
        ),
        "field_task_guidance_safety_chain_closure_go_verified": (
            review_checkpoints["field_task_guidance_safety_chain_closure_go_verified"] is True
        ),
        "controlled_trial_governance_template_ref_ok": template_ok is True,
        "interface_layer_governance_verified": (
            review_checkpoints["interface_layer_governance_verified"] is True
        ),
        "model_admission_governance_verified": (
            review_checkpoints["model_admission_governance_verified"] is True
        ),
        **{key: backend_registered.get(key) is True for key in BACKEND_REGISTERED_GO_KEYS},
        **{key: candidate_support.get(key) is True for key in CANDIDATE_MAPPING_GO_KEYS},
        **{key: scenario_support.get(key) is True for key in INTEGRATED_SCENARIO_GO_KEYS},
        "integrated_validation_mode_used": (
            review_checkpoints["integrated_validation_mode_used"] is True
        ),
        "single_backend_validation_not_used": (
            review_checkpoints["single_backend_validation_not_used"] is True
        ),
        "adapter_required": review_checkpoints["adapter_required"] is True,
        "native_output_direct_to_field_blocked": (
            review_checkpoints["native_output_direct_to_field_blocked"] is True
        ),
        "source_chain_required": review_checkpoints["source_chain_required"] is True,
        "confidence_required": review_checkpoints["confidence_required"] is True,
        "license_ref_required": review_checkpoints["license_ref_required"] is True,
        "gpl_or_incompatible_backend_technical_reference_only": (
            review_checkpoints["gpl_or_incompatible_backend_technical_reference_only"] is True
        ),
        "vio_slam_pose_not_field_identity": (
            review_checkpoints["vio_slam_pose_not_field_identity"] is True
        ),
        "gps_does_not_override_field_identity": (
            review_checkpoints["gps_does_not_override_field_identity"] is True
        ),
        "relocalization_does_not_restore_runtime_trust": (
            review_checkpoints["relocalization_does_not_restore_runtime_trust"] is True
        ),
        "drift_remains_uncertainty_evidence": (
            review_checkpoints["drift_remains_uncertainty_evidence"] is True
        ),
        "health_candidate_only": review_checkpoints["health_candidate_only"] is True,
        "semantic_label_not_fact": review_checkpoints["semantic_label_not_fact"] is True,
        "scene_graph_not_final_field_identity": (
            review_checkpoints["scene_graph_not_final_field_identity"] is True
        ),
        "heavy_neural_gaussian_runtime_not_admitted": (
            review_checkpoints["heavy_neural_gaussian_runtime_not_admitted"] is True
        ),
        "field_task_guidance_candidate_only": (
            review_checkpoints["field_task_guidance_candidate_only"] is True
        ),
        "real_file_conversion_execution_allowed_false": (
            review_checkpoints["real_file_conversion_execution_allowed"] is False
        ),
        "real_file_replay_execution_allowed_false": (
            review_checkpoints["real_file_replay_execution_allowed"] is False
        ),
        "runtime_activation_allowed_false": (
            review_checkpoints["runtime_activation_allowed"] is False
        ),
        "live_sensor_connected_false": review_checkpoints["live_sensor_connected"] is False,
        "real_navigation_started_false": review_checkpoints["real_navigation_started"] is False,
        "real_map_api_connected_false": review_checkpoints["real_map_api_connected"] is False,
        "real_gps_connected_false": review_checkpoints["real_gps_connected"] is False,
        "ros_connected_false": review_checkpoints["ros_connected"] is False,
        "camera_connected_false": review_checkpoints["camera_connected"] is False,
        "imu_connected_false": review_checkpoints["imu_connected"] is False,
        "direct_action_allowed_false": review_checkpoints["direct_action_allowed"] is False,
        "direct_speech_allowed_false": review_checkpoints["direct_speech_allowed"] is False,
        "direct_fact_write_allowed_false": (
            review_checkpoints["direct_fact_write_allowed"] is False
        ),
        "commercial_runtime_approved_false": (
            review_checkpoints["commercial_runtime_approved"] is False
        ),
    }

    for key, ok in go_conditions.items():
        if ok:
            passed_checks.append(f"go.{key}=true")
        else:
            failed_checks.append(f"go.{key}=false")

    blocker_count = len(failed_checks)
    review_ok = registry_ok and blocker_count == 0

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "step": "SLAM Backend Real File Output Integrated Admission Planning Review",
        "lifecycle_variant": "slam_backend_real_file_output_integrated_admission_planning_review",
        "planning_principle_zh": PLANNING_PRINCIPLE_ZH,
        "registry_id": REGISTRY_ID,
        "runtime_trial_mode": RUNTIME_TRIAL_MODE,
        "source_family": SOURCE_FAMILY,
        "target_internal_format": TARGET_INTERNAL_FORMAT,
        "target_entrypoint": TARGET_ENTRYPOINT,
        "interface_adapter_ref": INTERFACE_ADAPTER_REF,
        "generic_json_spatial_trace_parser_ref": GENERIC_JSON_PARSER_REF,
        "controlled_trial_governance_template_ref": CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
        "planning_governance_rules": list(PLANNING_GOVERNANCE_RULES),
        "non_execution_flags": dict(NON_EXECUTION_FLAGS),
        "registry_validation_ok": registry_ok,
        "upstream_sealed_phase_review": upstream_checks,
        "go_conditions": go_conditions,
        "review_checkpoints": review_checkpoints,
        "slam_backend_planning_matrix": matrix,
        "conclusions": {
            "slam_backend_admission_planning_status": (
                "ready_for_slam_backend_integrated_output_replay_dryrun"
                if review_ok
                else "blocked"
            ),
            "integrated_validation_mode_used": True,
            "single_backend_validation_not_used": True,
            "generic_json_parser_remains_default": True,
            "multi_backend_admission_baseline_locked": review_ok,
            "next_phase_ref": NEXT_PHASE_REF,
            "pipeline_summary": {
                "input": "slam_backend_real_file_outputs",
                "adapter": INTERFACE_ADAPTER_REF,
                "internal_format": TARGET_INTERNAL_FORMAT,
                "parser": GENERIC_JSON_PARSER_REF,
                "bundle": "spatial_evidence_candidate_bundle",
                "fusion": "spatial_odometry_fusion_candidate",
                "path": "field_task_guidance_candidate_replay_path",
            },
            "transition_note": (
                "Multi-backend SLAM/VIO/scene-graph real-file-output admission baseline locked "
                "(generic trajectory / RTAB / OpenVINS / ORB-SLAM3 / Kimera / Hydra / Neural-Gaussian). "
                "Next: SLAM Backend Integrated Output Replay DryRun with mock-but-file-based samples."
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
    result = review_slam_backend_real_file_output_integrated_admission_planning_v1()
    cp = result["review_checkpoints"]
    print(
        json.dumps(
            {
                "output_review_file": result.get("output_review_file"),
                "slam_backend_source_policy_count": cp["slam_backend_source_policy_count"],
                "integrated_scenario_count": cp["integrated_scenario_count"],
                "blocker_count": result["blocker_count"],
                "final_decision": result["final_decision"],
            },
            ensure_ascii=False,
        )
    )
    return 0 if result["final_decision"] == FINAL_DECISION_GO else 1


if __name__ == "__main__":
    raise SystemExit(main())
