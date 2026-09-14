# -*- coding: utf-8 -*-
"""RGB Vision / OCR / Segmentation Integrated Evidence Replay Planning — review v1."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.field_understanding.rgb_vision_ocr_segmentation_integrated_evidence_replay_planning.rgb_vision_ocr_segmentation_integrated_evidence_replay_planning_registry_v1 import (
    REGISTRY_ID,
    build_rgb_vision_planning_matrix_v1,
    validate_registry,
)
from capabilities.field_understanding.rgb_vision_ocr_segmentation_integrated_evidence_replay_planning.rgb_vision_ocr_segmentation_integrated_evidence_replay_planning_types_v1 import (
    CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
    DEPTH_HARDWARE_DEFAULT,
    FINAL_DECISION_BLOCKED,
    FINAL_DECISION_GO,
    GENERIC_JSON_PARSER_REF,
    NEXT_PHASE_REF,
    NON_EXECUTION_FLAGS,
    PHASE_ID,
    PLANNING_GOVERNANCE_RULES,
    PLANNING_PRINCIPLE_ZH,
    REPLAY_SCENARIO_GO_KEYS,
    RTAB_MULTI_EXPORT_CLOSURE_REF,
    RUNTIME_TRIAL_MODE,
    SOURCE_CHAIN,
    SYSTEM_OBJECTIVE,
    TARGET_ENTRYPOINT,
    TARGET_INTERNAL_FORMAT,
    TOF_STEREO_DEPTH_ROLE,
    VISION_HARDWARE_BASELINE,
    VISION_SOURCE_GO_KEYS,
)
from capabilities.midplatform.controlled_trial_governance.controlled_trial_governance_lifecycle_template_v1 import (
    TEMPLATE_ID,
)

DEFAULT_OUTPUT_ROOT = (
    _REPO_ROOT
    / "_tmp_eval_out"
    / "rgb_vision_ocr_segmentation_integrated_evidence_replay_planning_v1_smoke_v0"
)
REVIEW_FILENAME = "rgb_vision_ocr_segmentation_integrated_evidence_replay_planning_review_v1.json"

_PKG = "capabilities/field_understanding/rgb_vision_ocr_segmentation_integrated_evidence_replay_planning"
STEP_FILES = (
    f"{_PKG}/rgb_vision_ocr_segmentation_integrated_evidence_replay_planning_types_v1.py",
    f"{_PKG}/rgb_vision_ocr_segmentation_integrated_evidence_replay_planning_registry_v1.py",
    f"{_PKG}/review_rgb_vision_ocr_segmentation_integrated_evidence_replay_planning_v1.py",
)

_REQUIRED_VERIFY_FLAGS: Tuple[str, ...] = (
    "rtab_multi_export_spatial_evidence_replay_closure_go_verified",
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


def _policy_flags(shared: Dict[str, Any], hardware: Dict[str, Any]) -> Dict[str, bool]:
    mapping = shared.get("vision_evidence_candidate_mapping_policy") or {}
    ocr = shared.get("ocr_text_evidence_mapping_policy") or {}
    seg_track = shared.get("segmentation_tracking_evidence_mapping_policy") or {}
    safety = shared.get("safety_boundary_policy") or {}
    return {
        "rgb_first_hardware_baseline_declared": (
            hardware.get("rgb_first_hardware_baseline_declared") is True
        ),
        "tof_stereo_depth_optional_auxiliary_only": (
            hardware.get("tof_stereo_depth_optional_auxiliary_only") is True
        ),
        "cognitive_world_reconstruction_objective_declared": (
            hardware.get("cognitive_world_reconstruction_objective_declared") is True
        ),
        "external_model_output_adapter_required": (
            mapping.get("external_model_output_adapter_required") is True
            and safety.get("external_model_output_adapter_required") is True
        ),
        "native_output_direct_to_field_blocked": (
            mapping.get("native_output_direct_to_field_blocked") is True
            and safety.get("native_output_direct_to_field_blocked") is True
        ),
        "ocr_output_not_fact": ocr.get("ocr_output_not_fact") is True
        and safety.get("ocr_output_not_fact") is True,
        "segmentation_output_not_route_activation": (
            seg_track.get("segmentation_output_not_route_activation") is True
            and safety.get("segmentation_output_not_route_activation") is True
        ),
        "tracking_output_not_action_trigger": (
            seg_track.get("tracking_output_not_action_trigger") is True
            and safety.get("tracking_output_not_action_trigger") is True
        ),
        "monocular_depth_vio_not_field_identity": (
            seg_track.get("monocular_depth_vio_not_field_identity") is True
            and safety.get("monocular_depth_vio_not_field_identity") is True
        ),
        "scene_relation_not_final_interpretation": (
            seg_track.get("scene_relation_not_final_interpretation") is True
            and safety.get("scene_relation_not_final_interpretation") is True
        ),
        "source_chain_required": mapping.get("source_chain_required") is True,
        "confidence_required": mapping.get("confidence_required") is True,
        "origin_metadata_required": mapping.get("origin_metadata_required") is True,
        "guidance_candidate_not_runtime_navigation": (
            safety.get("guidance_candidate_not_runtime_navigation") is True
        ),
        "speech_gate_candidate_not_tts": safety.get("speech_gate_candidate_not_tts") is True,
        "action_safety_candidate_required": (
            safety.get("action_safety_candidate_required") is True
        ),
        "field_task_guidance_replay_path_candidate_only": (
            safety.get("field_task_guidance_replay_candidate_only") is True
        ),
    }


def validate_matrix_v1(matrix: Optional[Dict[str, Any]] = None) -> Tuple[bool, List[str]]:
    matrix = matrix or build_rgb_vision_planning_matrix_v1()
    issues: List[str] = []

    registry_ok, registry_issues = validate_registry()
    issues.extend(registry_issues)

    profile = matrix.get("rgb_vision_planning_profile") or {}
    if profile.get("controlled_trial_governance_template_ref") != CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF:
        issues.append("controlled_trial_governance_template_ref_mismatch")
    if profile.get("generic_json_spatial_trace_parser_ref") != GENERIC_JSON_PARSER_REF:
        issues.append("generic_json_spatial_trace_parser_ref_mismatch")
    if profile.get("rtab_multi_export_closure_ref") != RTAB_MULTI_EXPORT_CLOSURE_REF:
        issues.append("rtab_multi_export_closure_ref_mismatch")
    if profile.get("vision_hardware_baseline") != VISION_HARDWARE_BASELINE:
        issues.append("vision_hardware_baseline_mismatch")
    if profile.get("depth_hardware_default") != DEPTH_HARDWARE_DEFAULT:
        issues.append("depth_hardware_default_mismatch")
    if profile.get("tof_stereo_depth_role") != TOF_STEREO_DEPTH_ROLE:
        issues.append("tof_stereo_depth_role_mismatch")
    if profile.get("system_objective") != SYSTEM_OBJECTIVE:
        issues.append("system_objective_mismatch")
    if profile.get("target_internal_format") != TARGET_INTERNAL_FORMAT:
        issues.append("target_internal_format_mismatch")
    if profile.get("target_entrypoint") != TARGET_ENTRYPOINT:
        issues.append("target_entrypoint_mismatch")
    if profile.get("runtime_trial_mode") != RUNTIME_TRIAL_MODE:
        issues.append("runtime_trial_mode_mismatch")

    if len(matrix.get("vision_output_source_policies") or []) != 7:
        issues.append("vision_output_source_policy_count_not_7")
    if len(matrix.get("replay_scenario_policies") or []) != 7:
        issues.append("replay_scenario_policy_count_not_7")
    if not matrix.get("hardware_baseline_policy"):
        issues.append("hardware_baseline_policy_missing")

    blocked = next(
        (
            s
            for s in matrix.get("replay_scenario_policies") or []
            if s.get("scenario_ref") == "invalid_vision_output_blocked"
        ),
        {},
    )
    if not blocked.get("blocked_scenario"):
        issues.append("invalid_vision_output_must_be_blocked_scenario")

    return len(issues) == 0 and registry_ok, issues


def review_rgb_vision_ocr_segmentation_integrated_evidence_replay_planning_v1(
    *,
    output_root: Optional[str] = None,
    write_file: bool = True,
) -> Dict[str, Any]:
    matrix = build_rgb_vision_planning_matrix_v1()
    matrix_ok, matrix_issues = validate_matrix_v1(matrix)
    registry_ok, registry_issues = validate_registry()

    failed_checks: List[str] = []
    passed_checks: List[str] = []

    for rel in STEP_FILES:
        if (_REPO_ROOT / rel).is_file():
            passed_checks.append(f"step.file_present={rel.split('/')[-1]}")
        else:
            failed_checks.append(f"step.file_missing={rel}")

    if matrix_ok:
        passed_checks.append("matrix_validation_ok=true")
    else:
        failed_checks.extend(matrix_issues)
    if registry_ok:
        passed_checks.append("registry_validation_ok=true")
    else:
        failed_checks.extend(registry_issues)

    upstream_checks, upstream_issues = review_sealed_upstream_artifacts(matrix)
    failed_checks.extend(upstream_issues)

    source_go = matrix.get("vision_source_go_map") or {}
    scenario_go = matrix.get("replay_scenario_go_map") or {}
    shared = matrix.get("shared_mapping_policies") or {}
    hardware = matrix.get("hardware_baseline_policy") or {}
    policy_flags = _policy_flags(shared, hardware)

    template_ok = (
        matrix.get("rgb_vision_planning_profile", {}).get(
            "controlled_trial_governance_template_ref"
        )
        == TEMPLATE_ID
    )

    review_checkpoints: Dict[str, Any] = {
        "planning_profile_count": 1,
        "vision_output_source_policy_count": len(
            matrix.get("vision_output_source_policies") or []
        ),
        "integrated_replay_scenario_count": len(matrix.get("replay_scenario_policies") or []),
        "rtab_multi_export_spatial_evidence_replay_closure_go_verified": upstream_checks.get(
            "rtab_multi_export_spatial_evidence_replay_closure_go_verified", False
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
        **source_go,
        **scenario_go,
        **policy_flags,
        "runtime_trial_mode_locked": RUNTIME_TRIAL_MODE,
        "vision_hardware_baseline_locked": VISION_HARDWARE_BASELINE,
        "target_internal_format_locked": TARGET_INTERNAL_FORMAT,
        "target_entrypoint_locked": TARGET_ENTRYPOINT,
        **NON_EXECUTION_FLAGS,
    }

    go_conditions = {
        "planning_profile_count_eq_1": review_checkpoints["planning_profile_count"] == 1,
        "vision_output_source_policy_count_eq_7": (
            review_checkpoints["vision_output_source_policy_count"] == 7
        ),
        "integrated_replay_scenario_count_eq_7": (
            review_checkpoints["integrated_replay_scenario_count"] == 7
        ),
        "rtab_multi_export_spatial_evidence_replay_closure_go_verified": (
            review_checkpoints["rtab_multi_export_spatial_evidence_replay_closure_go_verified"]
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
        "rgb_first_hardware_baseline_declared": (
            policy_flags["rgb_first_hardware_baseline_declared"] is True
        ),
        "tof_stereo_depth_optional_auxiliary_only": (
            policy_flags["tof_stereo_depth_optional_auxiliary_only"] is True
        ),
        "cognitive_world_reconstruction_objective_declared": (
            policy_flags["cognitive_world_reconstruction_objective_declared"] is True
        ),
        **{key: source_go.get(key) is True for key in VISION_SOURCE_GO_KEYS},
        **{key: scenario_go.get(key) is True for key in REPLAY_SCENARIO_GO_KEYS},
        "external_model_output_adapter_required": (
            policy_flags["external_model_output_adapter_required"] is True
        ),
        "native_output_direct_to_field_blocked": (
            policy_flags["native_output_direct_to_field_blocked"] is True
        ),
        "ocr_output_not_fact": policy_flags["ocr_output_not_fact"] is True,
        "segmentation_output_not_route_activation": (
            policy_flags["segmentation_output_not_route_activation"] is True
        ),
        "tracking_output_not_action_trigger": (
            policy_flags["tracking_output_not_action_trigger"] is True
        ),
        "monocular_depth_vio_not_field_identity": (
            policy_flags["monocular_depth_vio_not_field_identity"] is True
        ),
        "scene_relation_not_final_interpretation": (
            policy_flags["scene_relation_not_final_interpretation"] is True
        ),
        "source_chain_required": policy_flags["source_chain_required"] is True,
        "confidence_required": policy_flags["confidence_required"] is True,
        "origin_metadata_required": policy_flags["origin_metadata_required"] is True,
        "integrated_validation_mode_used": (
            review_checkpoints["integrated_validation_mode_used"] is True
        ),
        "single_loader_validation_not_used": (
            review_checkpoints["single_loader_validation_not_used"] is True
        ),
        "candidate_only_enforced": review_checkpoints["candidate_only_enforced"] is True,
        "real_file_replay_execution_allowed_false": (
            review_checkpoints["real_file_replay_execution_allowed"] is False
        ),
        "runtime_activation_allowed_false": (
            review_checkpoints["runtime_activation_allowed"] is False
        ),
        "live_camera_connected_false": review_checkpoints["live_camera_connected"] is False,
        "live_sensor_connected_false": review_checkpoints["live_sensor_connected"] is False,
        "real_navigation_started_false": review_checkpoints["real_navigation_started"] is False,
        "real_map_api_connected_false": review_checkpoints["real_map_api_connected"] is False,
        "real_gps_connected_false": review_checkpoints["real_gps_connected"] is False,
        "ros_connected_false": review_checkpoints["ros_connected"] is False,
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
    review_ok = matrix_ok and registry_ok and blocker_count == 0

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "step": "RGB Vision / OCR / Segmentation Integrated Evidence Replay Planning Review",
        "lifecycle_variant": "rgb_first_integrated_evidence_replay_planning_review",
        "planning_principle_zh": PLANNING_PRINCIPLE_ZH,
        "registry_id": REGISTRY_ID,
        "runtime_trial_mode": RUNTIME_TRIAL_MODE,
        "vision_hardware_baseline": VISION_HARDWARE_BASELINE,
        "depth_hardware_default": DEPTH_HARDWARE_DEFAULT,
        "tof_stereo_depth_role": TOF_STEREO_DEPTH_ROLE,
        "system_objective": SYSTEM_OBJECTIVE,
        "target_internal_format": TARGET_INTERNAL_FORMAT,
        "target_entrypoint": TARGET_ENTRYPOINT,
        "controlled_trial_governance_template_ref": CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
        "rtab_multi_export_closure_ref": RTAB_MULTI_EXPORT_CLOSURE_REF,
        "generic_json_spatial_trace_parser_ref": GENERIC_JSON_PARSER_REF,
        "planning_governance_rules": list(PLANNING_GOVERNANCE_RULES),
        "non_execution_flags": dict(NON_EXECUTION_FLAGS),
        "matrix_review_ok": matrix_ok,
        "upstream_sealed_phase_review": upstream_checks,
        "go_conditions": go_conditions,
        "review_checkpoints": review_checkpoints,
        "rgb_vision_planning_matrix": matrix,
        "conclusions": {
            "rgb_vision_planning_status": (
                "ready_for_rgb_vision_integrated_evidence_replay_dryrun"
                if review_ok
                else "blocked"
            ),
            "rgb_first_baseline": True,
            "tof_stereo_depth_optional_auxiliary_only": True,
            "vision_planning_not_live_runtime": True,
            "generic_json_parser_reused": True,
            "integrated_validation_mode_used": True,
            "next_phase_ref": NEXT_PHASE_REF,
            "pipeline_summary": {
                "input": "external_rgb_vision_ocr_segmentation_tracking_model_output",
                "adapter": "external_vision_interface_adapter",
                "internal_format": TARGET_INTERNAL_FORMAT,
                "parser": GENERIC_JSON_PARSER_REF,
                "bundle": "spatial_evidence_candidate_bundle",
                "path": "field_task_guidance_candidate_replay_path",
            },
            "transition_note": (
                "RGB-first integrated evidence replay planning baseline locked. Next: integrated "
                "dry-run with local RGB image/video samples + mock-but-file-based model outputs "
                "to validate vision / OCR / segmentation / tracking into Luna evidence replay."
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
    result = review_rgb_vision_ocr_segmentation_integrated_evidence_replay_planning_v1()
    cp = result["review_checkpoints"]
    print(
        json.dumps(
            {
                "output_review_file": result.get("output_review_file"),
                "planning_profile_count": cp["planning_profile_count"],
                "vision_output_source_policy_count": cp["vision_output_source_policy_count"],
                "integrated_replay_scenario_count": cp["integrated_replay_scenario_count"],
                "rgb_first_hardware_baseline_declared": cp["rgb_first_hardware_baseline_declared"],
                "invalid_vision_output_blocked": cp.get("invalid_vision_output_blocked"),
                "blocker_count": result["blocker_count"],
                "final_decision": result["final_decision"],
            },
            ensure_ascii=False,
        )
    )
    return 0 if result["final_decision"] == FINAL_DECISION_GO else 1


if __name__ == "__main__":
    raise SystemExit(main())
