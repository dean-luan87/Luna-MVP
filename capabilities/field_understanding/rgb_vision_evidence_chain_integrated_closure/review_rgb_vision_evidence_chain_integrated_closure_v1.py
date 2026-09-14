# -*- coding: utf-8 -*-
"""RGB Vision Evidence Chain Integrated Closure — review v1."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.field_understanding.rgb_vision_evidence_chain_integrated_closure.rgb_vision_evidence_chain_integrated_closure_registry_v1 import (
    REGISTRY_ID,
    build_rgb_vision_evidence_chain_closure_matrix_v1,
    validate_registry,
)
from capabilities.field_understanding.rgb_vision_evidence_chain_integrated_closure.rgb_vision_evidence_chain_integrated_closure_types_v1 import (
    CANDIDATE_TYPE_COVERED_GO_KEYS,
    CANDIDATE_TYPE_IDS,
    CLOSURE_GOVERNANCE_RULES,
    CLOSURE_PRINCIPLE_ZH,
    CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
    FINAL_DECISION_BLOCKED,
    FINAL_DECISION_GO,
    INTERFACE_ADAPTER_REF,
    NEXT_PHASE_REF,
    NON_EXECUTION_FLAGS,
    PHASE_ID,
    REPLAY_PATH_GO_KEYS,
    RUNTIME_TRIAL_MODE,
    SOURCE_CHAIN,
    SOURCE_COVERAGE_IDS,
    SOURCE_COVERED_GO_KEYS,
    SYMBOL_MEANING_REFS,
    SYSTEM_OBJECTIVE,
    TARGET_ENTRYPOINT,
    TOF_STEREO_DEPTH_ROLE,
    VISION_HARDWARE_BASELINE,
)
from capabilities.midplatform.controlled_trial_governance.controlled_trial_governance_lifecycle_template_v1 import (
    TEMPLATE_ID,
)

DEFAULT_OUTPUT_ROOT = (
    _REPO_ROOT
    / "_tmp_eval_out"
    / "rgb_vision_evidence_chain_integrated_closure_v1_smoke_v0"
)
REVIEW_FILENAME = "rgb_vision_evidence_chain_integrated_closure_review_v1.json"

_PKG = "capabilities/field_understanding/rgb_vision_evidence_chain_integrated_closure"
STEP_FILES = (
    f"{_PKG}/rgb_vision_evidence_chain_integrated_closure_types_v1.py",
    f"{_PKG}/rgb_vision_evidence_chain_integrated_closure_registry_v1.py",
    f"{_PKG}/review_rgb_vision_evidence_chain_integrated_closure_v1.py",
)

_REQUIRED_VERIFY_FLAGS: Tuple[str, ...] = (
    "rgb_vision_integrated_planning_go_verified",
    "rgb_vision_integrated_dryrun_go_verified",
    "roboflow_dataset_integrated_dryrun_go_verified",
    "vision_test_source_backup_pool_go_verified",
    "vision_test_source_integrated_replay_go_verified",
    "rtab_multi_export_spatial_evidence_replay_closure_go_verified",
    "slam_backend_evidence_chain_closure_go_verified",
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


def review_rgb_vision_evidence_chain_integrated_closure_v1(
    *,
    output_root: Optional[str] = None,
    write_file: bool = True,
) -> Dict[str, Any]:
    matrix = build_rgb_vision_evidence_chain_closure_matrix_v1()
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
    sc_closure = matrix.get("source_coverage_closure") or {}
    ct_closure = matrix.get("candidate_type_coverage_closure") or {}
    ds_closure = matrix.get("dataset_test_source_closure") or {}
    replay_closure = matrix.get("replay_path_closure") or {}
    safety_closure = matrix.get("safety_boundary_closure") or {}
    symbol_closure = matrix.get("visual_symbol_evidence_extension_closure") or {}

    template_ok = profile.get("controlled_trial_governance_template_ref") == TEMPLATE_ID

    source_covered = (
        {key: True for key in SOURCE_COVERED_GO_KEYS}
        if sc_closure.get("all_sources_covered")
        else {key: False for key in SOURCE_COVERED_GO_KEYS}
    )
    candidate_type_covered = (
        {key: True for key in CANDIDATE_TYPE_COVERED_GO_KEYS}
        if ct_closure.get("all_candidate_types_covered")
        else {key: False for key in CANDIDATE_TYPE_COVERED_GO_KEYS}
    )
    replay_path = {key: replay_closure.get(key) is True for key in REPLAY_PATH_GO_KEYS}

    go_conditions = {
        "closure_profile_count_eq_1": True,
        "stage_ref_count_eq_5": matrix.get("stage_ref_count") == 5,
        "source_coverage_count_gte_13": sc_closure.get("source_coverage_count", 0) >= 13,
        "candidate_type_coverage_count_gte_11": (
            ct_closure.get("candidate_type_coverage_count", 0) >= 11
        ),
        "rgb_vision_integrated_planning_go_verified": (
            upstream_checks.get("rgb_vision_integrated_planning_go_verified") is True
        ),
        "rgb_vision_integrated_dryrun_go_verified": (
            upstream_checks.get("rgb_vision_integrated_dryrun_go_verified") is True
        ),
        "roboflow_dataset_integrated_dryrun_go_verified": (
            upstream_checks.get("roboflow_dataset_integrated_dryrun_go_verified") is True
        ),
        "vision_test_source_backup_pool_go_verified": (
            upstream_checks.get("vision_test_source_backup_pool_go_verified") is True
        ),
        "vision_test_source_integrated_replay_go_verified": (
            upstream_checks.get("vision_test_source_integrated_replay_go_verified") is True
        ),
        "rtab_multi_export_spatial_evidence_replay_closure_go_verified": (
            upstream_checks.get("rtab_multi_export_spatial_evidence_replay_closure_go_verified")
            is True
        ),
        "slam_backend_evidence_chain_closure_go_verified": (
            upstream_checks.get("slam_backend_evidence_chain_closure_go_verified") is True
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
        "rgb_first_hardware_baseline_preserved": (
            safety_closure.get("rgb_first_hardware_baseline_preserved") is True
        ),
        "tof_stereo_depth_optional_auxiliary_only": (
            safety_closure.get("tof_stereo_depth_optional_auxiliary_only") is True
        ),
        "cognitive_world_reconstruction_objective_preserved": (
            safety_closure.get("cognitive_world_reconstruction_objective_preserved") is True
        ),
        **source_covered,
        **candidate_type_covered,
        **replay_path,
        "backup_pool_not_training_admission": (
            ds_closure.get("backup_pool_not_training_admission") is True
        ),
        "backup_pool_not_runtime_admission": (
            ds_closure.get("backup_pool_not_runtime_admission") is True
        ),
        "dataset_download_allowed_false": ds_closure.get("dataset_download_allowed") is False,
        "training_use_allowed_false": ds_closure.get("training_use_allowed") is False,
        "license_ref_required_for_all": ds_closure.get("license_ref_required_for_all") is True,
        "dataset_ref_required_for_all": ds_closure.get("dataset_ref_required_for_all") is True,
        "annotation_origin_required_for_all": (
            ds_closure.get("annotation_origin_required_for_all") is True
        ),
        "sample_origin_required_for_all": (
            ds_closure.get("sample_origin_required_for_all") is True
        ),
        "roboflow_license_per_dataset_required": (
            ds_closure.get("roboflow_license_per_dataset_required") is True
        ),
        "commercial_use_unknown_until_verified": (
            ds_closure.get("commercial_use_unknown_until_verified") is True
        ),
        "non_commercial_sources_research_test_only": (
            ds_closure.get("non_commercial_sources_research_test_only") is True
        ),
        "dataset_label_not_fact": ds_closure.get("dataset_label_not_fact") is True,
        "annotation_as_evidence_candidate": (
            ds_closure.get("annotation_as_evidence_candidate") is True
        ),
        "ocr_output_not_fact": safety_closure.get("ocr_output_not_fact") is True,
        "segmentation_output_not_route_activation": (
            safety_closure.get("segmentation_output_not_route_activation") is True
        ),
        "tracking_output_not_action_trigger": (
            safety_closure.get("tracking_output_not_action_trigger") is True
        ),
        "monocular_depth_vio_not_field_identity": (
            safety_closure.get("monocular_depth_vio_not_field_identity") is True
        ),
        "scene_relation_not_final_interpretation": (
            safety_closure.get("scene_relation_not_final_interpretation") is True
        ),
        "native_output_direct_to_field_blocked": (
            safety_closure.get("native_output_direct_to_field_blocked") is True
        ),
        "field_task_guidance_candidate_only": (
            replay_closure.get("field_candidate_path_closed") is True
            and replay_closure.get("task_candidate_path_closed") is True
            and replay_closure.get("guidance_candidate_path_closed") is True
        ),
        # Visual Symbol Evidence Extension
        "color_evidence_candidate_covered": (
            symbol_closure.get("color_evidence_candidate_covered") is True
        ),
        "shape_evidence_candidate_covered": (
            symbol_closure.get("shape_evidence_candidate_covered") is True
        ),
        "visual_symbol_candidate_covered": (
            symbol_closure.get("visual_symbol_candidate_covered") is True
        ),
        "symbol_meaning_candidate_candidate_only": (
            symbol_closure.get("symbol_meaning_candidate_candidate_only") is True
        ),
        "color_shape_symbol_not_fact": (
            symbol_closure.get("color_shape_symbol_not_fact") is True
        ),
        "visual_symbol_not_direct_navigation": (
            symbol_closure.get("visual_symbol_not_direct_navigation") is True
        ),
        "visual_symbol_not_direct_speech": (
            symbol_closure.get("visual_symbol_not_direct_speech") is True
        ),
        "visual_symbol_requires_context_validation": (
            symbol_closure.get("visual_symbol_requires_context_validation") is True
        ),
        "symbol_meaning_mapping_count_gte_5": len(SYMBOL_MEANING_REFS) >= 5,
        "integrated_validation_mode_used": (
            NON_EXECUTION_FLAGS["integrated_validation_mode_used"] is True
        ),
        "single_source_validation_not_used": (
            NON_EXECUTION_FLAGS["single_source_validation_not_used"] is True
        ),
        "runtime_activation_allowed_false": (
            NON_EXECUTION_FLAGS["runtime_activation_allowed"] is False
        ),
        "live_camera_connected_false": NON_EXECUTION_FLAGS["live_camera_connected"] is False,
        "live_sensor_connected_false": NON_EXECUTION_FLAGS["live_sensor_connected"] is False,
        "real_navigation_started_false": NON_EXECUTION_FLAGS["real_navigation_started"] is False,
        "real_map_api_connected_false": NON_EXECUTION_FLAGS["real_map_api_connected"] is False,
        "real_gps_connected_false": NON_EXECUTION_FLAGS["real_gps_connected"] is False,
        "ros_connected_false": NON_EXECUTION_FLAGS["ros_connected"] is False,
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
        "source_coverage_count": sc_closure.get("source_coverage_count"),
        "candidate_type_coverage_count": ct_closure.get("candidate_type_coverage_count"),
        "source_coverage_ids": list(SOURCE_COVERAGE_IDS),
        "candidate_type_ids": list(CANDIDATE_TYPE_IDS),
        "runtime_trial_mode": RUNTIME_TRIAL_MODE,
        "vision_hardware_baseline": VISION_HARDWARE_BASELINE,
        "system_objective": SYSTEM_OBJECTIVE,
        "tof_stereo_depth_role": TOF_STEREO_DEPTH_ROLE,
        "target_entrypoint": TARGET_ENTRYPOINT,
        "controlled_trial_governance_template_ref": CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
        **upstream_checks,
        **NON_EXECUTION_FLAGS,
    }

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "step": "RGB Vision Evidence Chain Integrated Closure Review",
        "lifecycle_variant": "rgb_vision_evidence_chain_integrated_closure",
        "closure_principle_zh": CLOSURE_PRINCIPLE_ZH,
        "registry_id": REGISTRY_ID,
        "source_chain": SOURCE_CHAIN,
        "runtime_trial_mode": RUNTIME_TRIAL_MODE,
        "vision_hardware_baseline": VISION_HARDWARE_BASELINE,
        "system_objective": SYSTEM_OBJECTIVE,
        "tof_stereo_depth_role": TOF_STEREO_DEPTH_ROLE,
        "target_entrypoint": TARGET_ENTRYPOINT,
        "interface_adapter_ref": INTERFACE_ADAPTER_REF,
        "controlled_trial_governance_template_ref": CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
        "closure_governance_rules": list(CLOSURE_GOVERNANCE_RULES),
        "non_execution_flags": dict(NON_EXECUTION_FLAGS),
        "registry_validation_ok": registry_ok,
        "upstream_sealed_phase_review": upstream_checks,
        "go_conditions": go_conditions,
        "review_checkpoints": review_checkpoints,
        "rgb_vision_evidence_chain_closure_matrix": matrix,
        "conclusions": {
            "rgb_vision_evidence_chain_status": (
                "rgb_vision_evidence_chain_baseline_sealed" if review_ok else "blocked"
            ),
            "rgb_vision_line_sealed": review_ok,
            "integrated_validation_mode_used": True,
            "rgb_first_hardware_baseline_preserved": True,
            "unified_sources": list(SOURCE_COVERAGE_IDS),
            "unified_candidate_types": list(CANDIDATE_TYPE_IDS),
            "visual_symbol_evidence_extension": {
                "extension_note": (
                    "Color / Shape / Visual Symbol Evidence is part of the RGB Vision Evidence "
                    "Chain. Schema / governance / coverage only in this closure — no model, no "
                    "algorithm, no real image recognition. Color/shape/symbol are not facts; "
                    "symbol meaning must be validated against OCR/object/region/scene context and "
                    "must not directly trigger navigation/action/speech/fact_write."
                ),
                "extension_candidate_types": [
                    "color_evidence_candidate",
                    "shape_evidence_candidate",
                    "visual_symbol_candidate",
                    "symbol_meaning_candidate",
                ],
                "symbol_meaning_refs": list(SYMBOL_MEANING_REFS),
                "future_phase_ref": "Phase-Visual-Symbol-Evidence-DryRun-v1-001",
            },
            "next_phase_ref": NEXT_PHASE_REF,
            "pipeline_summary": {
                "input": "rgb_first_vision_outputs_and_test_sources",
                "stages": list(matrix.get("closure_profile", {}).get("stage_refs") or []),
                "adapter": INTERFACE_ADAPTER_REF,
                "evidence_candidates": list(CANDIDATE_TYPE_IDS),
                "path": "field_task_guidance_candidate_replay_path",
            },
            "transition_note": (
                "RGB vision evidence chain baseline sealed: RGB frame/video, object/segmentation/"
                "tracking/OCR/monocular-depth-VIO/scene-relation, Roboflow, and the multi test-source "
                "backup pool are unified into one RGB-first vision evidence chain. Next: RGB Vision + "
                "SLAM Spatial Evidence Cross-Modal Integrated Closure to merge 'what is seen' with "
                "'where spatial evidence is' into the Luna Phase-One environment cognition mainline."
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
    result = review_rgb_vision_evidence_chain_integrated_closure_v1()
    cp = result["review_checkpoints"]
    print(
        json.dumps(
            {
                "output_review_file": result.get("output_review_file"),
                "stage_ref_count": cp["stage_ref_count"],
                "source_coverage_count": cp["source_coverage_count"],
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
