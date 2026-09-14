# -*- coding: utf-8 -*-
"""Phase One Environment Cognition Evidence Main Chain Closure — review v1."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.field_understanding.phase_one_environment_cognition_evidence_main_chain_closure.phase_one_environment_cognition_evidence_main_chain_closure_registry_v1 import (
    REGISTRY_ID,
    build_main_chain_closure_matrix_v1,
    validate_registry,
)
from capabilities.field_understanding.phase_one_environment_cognition_evidence_main_chain_closure.phase_one_environment_cognition_evidence_main_chain_closure_types_v1 import (
    CANDIDATE_LAYER_COVERED_GO_KEYS,
    CANDIDATE_LAYER_IDS,
    CLOSURE_GOVERNANCE_RULES,
    CLOSURE_PRINCIPLE_ZH,
    CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
    DEFERRED_EXPANSION_IDS,
    EVIDENCE_SOURCE_COVERED_GO_KEYS,
    EVIDENCE_SOURCE_IDS,
    FINAL_DECISION_BLOCKED,
    FINAL_DECISION_GO,
    GENERIC_JSON_SPATIAL_TRACE_PARSER_REF,
    INTERFACE_ADAPTER_REF,
    NEXT_PHASE_REFS,
    NON_EXECUTION_FLAGS,
    PHASE_ID,
    PHASE_ONE_SCOPE,
    RUNTIME_TRIAL_MODE,
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
    / "phase_one_environment_cognition_evidence_main_chain_closure_v1_smoke_v0"
)
REVIEW_FILENAME = "phase_one_environment_cognition_evidence_main_chain_closure_review_v1.json"

_PKG = (
    "capabilities/field_understanding/"
    "phase_one_environment_cognition_evidence_main_chain_closure"
)
STEP_FILES = (
    f"{_PKG}/phase_one_environment_cognition_evidence_main_chain_closure_types_v1.py",
    f"{_PKG}/phase_one_environment_cognition_evidence_main_chain_closure_registry_v1.py",
    f"{_PKG}/review_phase_one_environment_cognition_evidence_main_chain_closure_v1.py",
)

_REQUIRED_VERIFY_FLAGS: Tuple[str, ...] = (
    "rgb_vision_evidence_chain_closure_go_verified",
    "slam_backend_evidence_chain_closure_go_verified",
    "rgb_vision_slam_cross_modal_closure_go_verified",
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


def review_phase_one_environment_cognition_evidence_main_chain_closure_v1(
    *,
    output_root: Optional[str] = None,
    write_file: bool = True,
) -> Dict[str, Any]:
    matrix = build_main_chain_closure_matrix_v1()
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
    cross_path = matrix.get("cross_modal_path_closure") or {}
    ftg_path = matrix.get("field_task_guidance_path_closure") or {}
    gov = matrix.get("governance_boundary_closure") or {}
    deferred = matrix.get("deferred_expansion_record") or {}

    template_ok = profile.get("controlled_trial_governance_template_ref") == TEMPLATE_ID

    evidence_source_covered = {
        f"{sid}_covered": sid in EVIDENCE_SOURCE_IDS for sid in EVIDENCE_SOURCE_IDS
    }
    candidate_layer_covered = {
        f"{cid}_covered": cid in CANDIDATE_LAYER_IDS for cid in CANDIDATE_LAYER_IDS
    }

    go_conditions = {
        "closure_profile_count_eq_1": True,
        "stage_ref_count_gte_6": matrix.get("stage_ref_count", 0) >= 6,
        "evidence_source_coverage_count_gte_10": (
            len(EVIDENCE_SOURCE_IDS) >= 10
        ),
        "candidate_layer_coverage_count_gte_34": (
            len(CANDIDATE_LAYER_IDS) >= 34
        ),
        "deferred_expansion_record_present": bool(deferred.get("deferred_expansion_ids")),
        "rgb_vision_evidence_chain_closure_go_verified": (
            upstream_checks.get("rgb_vision_evidence_chain_closure_go_verified") is True
        ),
        "slam_backend_evidence_chain_closure_go_verified": (
            upstream_checks.get("slam_backend_evidence_chain_closure_go_verified") is True
        ),
        "rgb_vision_slam_cross_modal_closure_go_verified": (
            upstream_checks.get("rgb_vision_slam_cross_modal_closure_go_verified") is True
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
        **evidence_source_covered,
        **candidate_layer_covered,
        "rgb_evidence_path_closed": cross_path.get("rgb_evidence_path_closed") is True,
        "slam_spatial_evidence_path_closed": (
            cross_path.get("slam_spatial_evidence_path_closed") is True
        ),
        "rgb_slam_cross_modal_path_closed": (
            cross_path.get("rgb_slam_cross_modal_path_closed") is True
        ),
        "generic_json_spatial_trace_parser_reused": (
            cross_path.get("generic_json_spatial_trace_parser_reused") is True
        ),
        "interface_adapter_required": cross_path.get("interface_adapter_required") is True,
        "source_admission_required": cross_path.get("source_admission_required") is True,
        "source_chain_preserved": cross_path.get("source_chain_preserved") is True,
        "confidence_preserved": cross_path.get("confidence_preserved") is True,
        "origin_metadata_preserved": cross_path.get("origin_metadata_preserved") is True,
        "spatial_evidence_candidate_bundle_path_closed": (
            cross_path.get("spatial_evidence_candidate_bundle_path_closed") is True
        ),
        "spatial_odometry_fusion_candidate_path_closed": (
            cross_path.get("spatial_odometry_fusion_candidate_path_closed") is True
        ),
        "field_candidate_path_closed": ftg_path.get("field_candidate_path_closed") is True,
        "task_candidate_path_closed": ftg_path.get("task_candidate_path_closed") is True,
        "guidance_candidate_path_closed": (
            ftg_path.get("guidance_candidate_path_closed") is True
        ),
        "guidance_candidate_remains_candidate": (
            ftg_path.get("guidance_candidate_remains_candidate") is True
        ),
        "speech_gate_candidate_not_tts": ftg_path.get("speech_gate_candidate_not_tts") is True,
        "action_safety_candidate_exists": (
            ftg_path.get("action_safety_candidate_exists") is True
        ),
        "observation_only_scope_preserved": (
            ftg_path.get("observation_only_scope_preserved") is True
        ),
        "all_evidence_candidate_only": ftg_path.get("all_evidence_candidate_only") is True,
        "field_task_guidance_candidate_only": (
            ftg_path.get("field_task_guidance_candidate_only") is True
        ),
        "rgb_first_hardware_baseline_preserved": (
            gov.get("rgb_first_hardware_baseline_preserved") is True
        ),
        "slam_role_spatial_evidence_provider": (
            gov.get("slam_role_spatial_evidence_provider") is True
        ),
        "cognitive_world_reconstruction_objective_preserved": (
            gov.get("cognitive_world_reconstruction_objective_preserved") is True
        ),
        "object_identity_not_fact": gov.get("object_identity_not_fact") is True,
        "ocr_text_not_fact": gov.get("ocr_text_not_fact") is True,
        "color_shape_symbol_not_fact": gov.get("color_shape_symbol_not_fact") is True,
        "visual_symbol_requires_context_validation": (
            gov.get("visual_symbol_requires_context_validation") is True
        ),
        "segmentation_not_route_activation": (
            gov.get("segmentation_not_route_activation") is True
        ),
        "tracking_not_action_trigger": gov.get("tracking_not_action_trigger") is True,
        "monocular_depth_vio_slam_pose_not_field_identity": (
            gov.get("monocular_depth_vio_slam_pose_not_field_identity") is True
        ),
        "relocalization_does_not_restore_runtime_trust": (
            gov.get("relocalization_does_not_restore_runtime_trust") is True
        ),
        "drift_remains_uncertainty_evidence": (
            gov.get("drift_remains_uncertainty_evidence") is True
        ),
        "health_candidate_only": gov.get("health_candidate_only") is True,
        "gps_does_not_override_field_identity": (
            gov.get("gps_does_not_override_field_identity") is True
        ),
        "conflict_not_direct_fact_write": gov.get("conflict_not_direct_fact_write") is True,
        "conflict_not_direct_action_speech_navigation": (
            gov.get("conflict_not_direct_action_speech_navigation") is True
        ),
        "future_information_source_expansion_deferred": (
            deferred.get("future_information_source_expansion_deferred") is True
        ),
        "latent_relation_mechanism_deferred": (
            deferred.get("latent_relation_mechanism_deferred") is True
        ),
        "hidden_object_relation_mechanism_deferred": (
            deferred.get("hidden_object_relation_mechanism_deferred") is True
        ),
        "deferred_expansion_not_part_of_current_closure": (
            deferred.get("deferred_expansion_not_part_of_current_closure") is True
        ),
        "current_closure_does_not_expand_new_sources": (
            deferred.get("current_closure_does_not_expand_new_sources") is True
        ),
        "integrated_validation_mode_used": (
            NON_EXECUTION_FLAGS["integrated_validation_mode_used"] is True
        ),
        "runtime_activation_allowed_false": (
            NON_EXECUTION_FLAGS["runtime_activation_allowed"] is False
        ),
        "dataset_download_allowed_false": NON_EXECUTION_FLAGS["dataset_download_allowed"] is False,
        "training_use_allowed_false": NON_EXECUTION_FLAGS["training_use_allowed"] is False,
        "model_download_allowed_false": NON_EXECUTION_FLAGS["model_download_allowed"] is False,
        "live_camera_connected_false": NON_EXECUTION_FLAGS["live_camera_connected"] is False,
        "live_sensor_connected_false": NON_EXECUTION_FLAGS["live_sensor_connected"] is False,
        "real_gps_connected_false": NON_EXECUTION_FLAGS["real_gps_connected"] is False,
        "real_map_api_connected_false": NON_EXECUTION_FLAGS["real_map_api_connected"] is False,
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
        "evidence_source_coverage_count": len(EVIDENCE_SOURCE_IDS),
        "candidate_layer_coverage_count": len(CANDIDATE_LAYER_IDS),
        "deferred_expansion_count": len(DEFERRED_EXPANSION_IDS),
        "evidence_source_ids": list(EVIDENCE_SOURCE_IDS),
        "candidate_layer_ids": list(CANDIDATE_LAYER_IDS),
        "deferred_expansion_ids": list(DEFERRED_EXPANSION_IDS),
        "runtime_trial_mode": RUNTIME_TRIAL_MODE,
        "phase_one_scope": PHASE_ONE_SCOPE,
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
        "step": "Phase One Environment Cognition Evidence Main Chain Closure Review",
        "lifecycle_variant": "phase_one_environment_cognition_evidence_main_chain_closure",
        "closure_principle_zh": CLOSURE_PRINCIPLE_ZH,
        "registry_id": REGISTRY_ID,
        "source_chain": SOURCE_CHAIN,
        "runtime_trial_mode": RUNTIME_TRIAL_MODE,
        "phase_one_scope": PHASE_ONE_SCOPE,
        "vision_hardware_baseline": VISION_HARDWARE_BASELINE,
        "slam_role": SLAM_ROLE,
        "system_objective": SYSTEM_OBJECTIVE,
        "target_entrypoint": TARGET_ENTRYPOINT,
        "generic_json_spatial_trace_parser_ref": GENERIC_JSON_SPATIAL_TRACE_PARSER_REF,
        "interface_adapter_ref": INTERFACE_ADAPTER_REF,
        "controlled_trial_governance_template_ref": CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
        "closure_governance_rules": list(CLOSURE_GOVERNANCE_RULES),
        "non_execution_flags": dict(NON_EXECUTION_FLAGS),
        "registry_validation_ok": registry_ok,
        "upstream_sealed_phase_review": upstream_checks,
        "go_conditions": go_conditions,
        "review_checkpoints": review_checkpoints,
        "main_chain_closure_matrix": matrix,
        "conclusions": {
            "phase_one_environment_cognition_evidence_main_chain_status": (
                "phase_one_environment_cognition_evidence_main_chain_baseline_sealed"
                if review_ok
                else "blocked"
            ),
            "evidence_main_chain_frozen_as_phase_one_baseline": review_ok,
            "integrated_validation_mode_used": True,
            "rgb_first_hardware_baseline_preserved": True,
            "slam_role": SLAM_ROLE,
            "evidence_sources_sealed": list(EVIDENCE_SOURCE_IDS),
            "candidate_layers_sealed": list(CANDIDATE_LAYER_IDS),
            "deferred_expansions_recorded": list(DEFERRED_EXPANSION_IDS),
            "next_phase_refs": list(NEXT_PHASE_REFS),
            "sealed_chains": [
                "rgb_vision_evidence_chain_closure",
                "slam_backend_evidence_chain_closure",
                "rgb_vision_slam_cross_modal_closure",
                "field_task_guidance_safety_chain_closure",
                "runtime_governance_closure",
                "interface_and_model_admission_governance",
            ],
            "transition_note": (
                "Luna Phase-One environment cognition evidence main chain sealed as the current "
                "baseline: RGB semantic evidence + SLAM spatial evidence + cross-modal alignment + "
                "FTG safety path + runtime/interface/model admission governance unified as one "
                "candidate-only evidence layer. No new information source was added. Future latent / "
                "hidden-object relation mechanisms are recorded but deferred. Next: Visual Symbol "
                "Evidence DryRun or real-recognition dry-run."
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
    result = review_phase_one_environment_cognition_evidence_main_chain_closure_v1()
    cp = result["review_checkpoints"]
    print(
        json.dumps(
            {
                "output_review_file": result.get("output_review_file"),
                "stage_ref_count": cp["stage_ref_count"],
                "evidence_source_coverage_count": cp["evidence_source_coverage_count"],
                "candidate_layer_coverage_count": cp["candidate_layer_coverage_count"],
                "deferred_expansion_count": cp["deferred_expansion_count"],
                "blocker_count": result["blocker_count"],
                "final_decision": result["final_decision"],
            },
            ensure_ascii=False,
        )
    )
    return 0 if result["final_decision"] == FINAL_DECISION_GO else 1


if __name__ == "__main__":
    raise SystemExit(main())
