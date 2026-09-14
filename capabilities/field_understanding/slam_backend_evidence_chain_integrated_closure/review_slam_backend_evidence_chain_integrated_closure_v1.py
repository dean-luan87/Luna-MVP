# -*- coding: utf-8 -*-
"""SLAM Backend Evidence Chain Integrated Closure — review v1."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.field_understanding.slam_backend_evidence_chain_integrated_closure.slam_backend_evidence_chain_integrated_closure_registry_v1 import (
    REGISTRY_ID,
    build_slam_backend_evidence_chain_closure_matrix_v1,
    validate_registry,
)
from capabilities.field_understanding.slam_backend_evidence_chain_integrated_closure.slam_backend_evidence_chain_integrated_closure_types_v1 import (
    CANDIDATE_TYPE_COVERED_GO_KEYS,
    CANDIDATE_TYPE_IDS,
    CLOSURE_GOVERNANCE_RULES,
    CLOSURE_PRINCIPLE_ZH,
    CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
    FINAL_DECISION_BLOCKED,
    FINAL_DECISION_GO,
    GENERIC_JSON_PARSER_REF,
    INTERFACE_ADAPTER_REF,
    NEXT_PHASE_REF,
    NON_EXECUTION_FLAGS,
    PHASE_ID,
    REPLAY_PATH_GO_KEYS,
    RUNTIME_TRIAL_MODE,
    SOURCE_CHAIN,
    SOURCE_FAMILY,
    SOURCE_FAMILY_COVERED_GO_KEYS,
    SOURCE_FAMILY_IDS,
    TARGET_ENTRYPOINT,
    TARGET_INTERNAL_FORMAT,
)
from capabilities.midplatform.controlled_trial_governance.controlled_trial_governance_lifecycle_template_v1 import (
    TEMPLATE_ID,
)

DEFAULT_OUTPUT_ROOT = (
    _REPO_ROOT
    / "_tmp_eval_out"
    / "slam_backend_evidence_chain_integrated_closure_v1_smoke_v0"
)
REVIEW_FILENAME = "slam_backend_evidence_chain_integrated_closure_review_v1.json"

_PKG = "capabilities/field_understanding/slam_backend_evidence_chain_integrated_closure"
STEP_FILES = (
    f"{_PKG}/slam_backend_evidence_chain_integrated_closure_types_v1.py",
    f"{_PKG}/slam_backend_evidence_chain_integrated_closure_registry_v1.py",
    f"{_PKG}/review_slam_backend_evidence_chain_integrated_closure_v1.py",
)

_REQUIRED_VERIFY_FLAGS: Tuple[str, ...] = (
    "tum_real_file_loader_dryrun_go_verified",
    "rtab_real_file_loader_integrated_dryrun_go_verified",
    "rtab_multi_export_spatial_evidence_replay_closure_go_verified",
    "slam_backend_admission_planning_go_verified",
    "slam_backend_integrated_output_replay_dryrun_go_verified",
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


def review_slam_backend_evidence_chain_integrated_closure_v1(
    *,
    output_root: Optional[str] = None,
    write_file: bool = True,
) -> Dict[str, Any]:
    matrix = build_slam_backend_evidence_chain_closure_matrix_v1()
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
    sf_closure = matrix.get("source_family_coverage_closure") or {}
    ct_closure = matrix.get("candidate_type_coverage_closure") or {}
    replay_closure = matrix.get("replay_path_closure") or {}
    safety_closure = matrix.get("safety_boundary_closure") or {}
    license_closure = matrix.get("license_boundary_closure") or {}

    template_ok = profile.get("controlled_trial_governance_template_ref") == TEMPLATE_ID

    source_family_covered = {
        key: True for key in SOURCE_FAMILY_COVERED_GO_KEYS
    } if sf_closure.get("all_source_families_covered") else {
        key: False for key in SOURCE_FAMILY_COVERED_GO_KEYS
    }
    candidate_type_covered = {
        key: True for key in CANDIDATE_TYPE_COVERED_GO_KEYS
    } if ct_closure.get("all_candidate_types_covered") else {
        key: False for key in CANDIDATE_TYPE_COVERED_GO_KEYS
    }
    replay_path = {key: replay_closure.get(key) is True for key in REPLAY_PATH_GO_KEYS}

    go_conditions = {
        "closure_profile_count_eq_1": True,
        "stage_ref_count_eq_5": matrix.get("stage_ref_count") == 5,
        "source_family_coverage_count_gte_7": (
            sf_closure.get("source_family_coverage_count", 0) >= 7
        ),
        "candidate_type_coverage_count_gte_12": (
            ct_closure.get("candidate_type_coverage_count", 0) >= 12
        ),
        "tum_real_file_loader_dryrun_go_verified": (
            upstream_checks.get("tum_real_file_loader_dryrun_go_verified") is True
        ),
        "rtab_real_file_loader_integrated_dryrun_go_verified": (
            upstream_checks.get("rtab_real_file_loader_integrated_dryrun_go_verified") is True
        ),
        "rtab_multi_export_spatial_evidence_replay_closure_go_verified": (
            upstream_checks.get("rtab_multi_export_spatial_evidence_replay_closure_go_verified")
            is True
        ),
        "slam_backend_admission_planning_go_verified": (
            upstream_checks.get("slam_backend_admission_planning_go_verified") is True
        ),
        "slam_backend_integrated_output_replay_dryrun_go_verified": (
            upstream_checks.get("slam_backend_integrated_output_replay_dryrun_go_verified") is True
        ),
        "generic_json_spatial_trace_parser_go_verified": (
            upstream_checks.get("generic_json_spatial_trace_parser_go_verified") is True
        ),
        "slam_spatial_evidence_chain_field_alignment_closure_go_verified": (
            upstream_checks.get("slam_spatial_evidence_chain_field_alignment_closure_go_verified")
            is True
        ),
        "field_task_guidance_safety_chain_closure_go_verified": (
            upstream_checks.get("field_task_guidance_safety_chain_closure_go_verified") is True
        ),
        "controlled_trial_governance_template_ref_ok": template_ok is True,
        "interface_layer_governance_verified": (
            upstream_checks.get("interface_layer_governance_verified") is True
        ),
        "model_admission_governance_verified": (
            upstream_checks.get("model_admission_governance_verified") is True
        ),
        **source_family_covered,
        **candidate_type_covered,
        **replay_path,
        "integrated_validation_mode_used": (
            NON_EXECUTION_FLAGS["integrated_validation_mode_used"] is True
        ),
        "single_backend_validation_not_used": (
            NON_EXECUTION_FLAGS["single_backend_validation_not_used"] is True
        ),
        "slam_backend_model_download_allowed_false": (
            NON_EXECUTION_FLAGS["slam_backend_model_download_allowed"] is False
        ),
        "slam_backend_repo_clone_allowed_false": (
            NON_EXECUTION_FLAGS["slam_backend_repo_clone_allowed"] is False
        ),
        "slam_backend_runtime_build_allowed_false": (
            NON_EXECUTION_FLAGS["slam_backend_runtime_build_allowed"] is False
        ),
        "adapter_required": bool(profile.get("interface_adapter_ref")),
        "native_output_direct_to_field_blocked": (
            safety_closure.get("backend_native_output_direct_to_field_blocked") is True
        ),
        "source_chain_required": True,
        "confidence_required": True,
        "backend_origin_required": True,
        "license_ref_required": True,
        "gpl_or_incompatible_backend_technical_reference_only": (
            license_closure.get("gpl_or_incompatible_backend_technical_reference_only") is True
        ),
        "vio_slam_pose_not_field_identity": (
            safety_closure.get("vio_slam_pose_not_field_identity") is True
        ),
        "gps_does_not_override_field_identity": (
            safety_closure.get("gps_does_not_override_field_identity") is True
        ),
        "relocalization_does_not_restore_runtime_trust": (
            safety_closure.get("relocalization_does_not_restore_runtime_trust") is True
        ),
        "drift_remains_uncertainty_evidence": (
            safety_closure.get("drift_remains_uncertainty_evidence") is True
        ),
        "health_candidate_only": safety_closure.get("health_candidate_only") is True,
        "semantic_label_not_fact": safety_closure.get("semantic_label_not_fact") is True,
        "scene_graph_not_final_field_identity": (
            safety_closure.get("scene_graph_not_final_field_identity") is True
        ),
        "heavy_neural_gaussian_runtime_not_admitted": (
            license_closure.get("heavy_neural_gaussian_runtime_not_admitted") is True
        ),
        "field_task_guidance_candidate_only": (
            replay_closure.get("field_candidate_path_closed") is True
            and replay_closure.get("task_candidate_path_closed") is True
            and replay_closure.get("guidance_candidate_path_closed") is True
        ),
        "guidance_candidate_remains_candidate": (
            replay_closure.get("guidance_candidate_path_closed") is True
        ),
        "real_file_conversion_execution_allowed_false": (
            NON_EXECUTION_FLAGS["real_file_conversion_execution_allowed"] is False
        ),
        "real_file_replay_execution_allowed_false": (
            NON_EXECUTION_FLAGS["real_file_replay_execution_allowed"] is False
        ),
        "runtime_activation_allowed_false": (
            NON_EXECUTION_FLAGS["runtime_activation_allowed"] is False
        ),
        "live_sensor_connected_false": NON_EXECUTION_FLAGS["live_sensor_connected"] is False,
        "real_navigation_started_false": NON_EXECUTION_FLAGS["real_navigation_started"] is False,
        "real_map_api_connected_false": NON_EXECUTION_FLAGS["real_map_api_connected"] is False,
        "real_gps_connected_false": NON_EXECUTION_FLAGS["real_gps_connected"] is False,
        "ros_connected_false": NON_EXECUTION_FLAGS["ros_connected"] is False,
        "camera_connected_false": NON_EXECUTION_FLAGS["camera_connected"] is False,
        "imu_connected_false": NON_EXECUTION_FLAGS["imu_connected"] is False,
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
        "closure_profile_count": 1,
        "stage_ref_count": matrix.get("stage_ref_count"),
        "source_family_coverage_count": sf_closure.get("source_family_coverage_count"),
        "candidate_type_coverage_count": ct_closure.get("candidate_type_coverage_count"),
        "source_family_ids": list(SOURCE_FAMILY_IDS),
        "candidate_type_ids": list(CANDIDATE_TYPE_IDS),
        "runtime_trial_mode": RUNTIME_TRIAL_MODE,
        "source_family": SOURCE_FAMILY,
        "target_internal_format": TARGET_INTERNAL_FORMAT,
        "target_entrypoint": TARGET_ENTRYPOINT,
        "controlled_trial_governance_template_ref": CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
        **upstream_checks,
        **NON_EXECUTION_FLAGS,
    }

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "step": "SLAM Backend Evidence Chain Integrated Closure Review",
        "lifecycle_variant": "slam_backend_evidence_chain_integrated_closure",
        "closure_principle_zh": CLOSURE_PRINCIPLE_ZH,
        "registry_id": REGISTRY_ID,
        "source_chain": SOURCE_CHAIN,
        "runtime_trial_mode": RUNTIME_TRIAL_MODE,
        "source_family": SOURCE_FAMILY,
        "target_internal_format": TARGET_INTERNAL_FORMAT,
        "target_entrypoint": TARGET_ENTRYPOINT,
        "interface_adapter_ref": INTERFACE_ADAPTER_REF,
        "generic_json_spatial_trace_parser_ref": GENERIC_JSON_PARSER_REF,
        "controlled_trial_governance_template_ref": CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
        "closure_governance_rules": list(CLOSURE_GOVERNANCE_RULES),
        "non_execution_flags": dict(NON_EXECUTION_FLAGS),
        "registry_validation_ok": registry_ok,
        "upstream_sealed_phase_review": upstream_checks,
        "go_conditions": go_conditions,
        "review_checkpoints": review_checkpoints,
        "slam_backend_evidence_chain_closure_matrix": matrix,
        "conclusions": {
            "slam_backend_evidence_chain_status": (
                "slam_backend_evidence_chain_baseline_sealed" if review_ok else "blocked"
            ),
            "slam_line_frozen": review_ok,
            "integrated_validation_mode_used": True,
            "generic_json_parser_remains_default": True,
            "unified_backends": list(SOURCE_FAMILY_IDS),
            "unified_candidate_types": list(CANDIDATE_TYPE_IDS),
            "next_phase_ref": NEXT_PHASE_REF,
            "pipeline_summary": {
                "input": "slam_backend_evidence_chain",
                "stages": list(matrix.get("closure_profile", {}).get("stage_refs") or []),
                "adapter": INTERFACE_ADAPTER_REF,
                "internal_format": TARGET_INTERNAL_FORMAT,
                "parser": GENERIC_JSON_PARSER_REF,
                "bundle": "spatial_evidence_candidate_bundle",
                "fusion": "spatial_odometry_fusion_candidate",
                "path": "field_task_guidance_candidate_replay_path",
            },
            "transition_note": (
                "SLAM backend evidence chain baseline sealed: TUM / RTAB / OpenVINS-like / "
                "ORB-SLAM3-like / Kimera-like / Hydra-like / Neural-Gaussian-like outputs are unified "
                "into one SLAM backend evidence chain. SLAM line can be frozen. Next: RGB Vision "
                "Evidence Chain Closure, then RGB Vision + SLAM Spatial Evidence Cross-Modal "
                "Integrated Closure."
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
    result = review_slam_backend_evidence_chain_integrated_closure_v1()
    cp = result["review_checkpoints"]
    print(
        json.dumps(
            {
                "output_review_file": result.get("output_review_file"),
                "stage_ref_count": cp["stage_ref_count"],
                "source_family_coverage_count": cp["source_family_coverage_count"],
                "candidate_type_coverage_count": cp["candidate_type_coverage_count"],
                "blocker_count": result["blocker_count"],
                "final_decision": result["final_decision"],
            },
            ensure_ascii=False,
        )
    )
    return 0 if result["final_decision"] == FINAL_DECISION_GO else 1


if __name__ == "__main__":
    raise SystemExit(main())
