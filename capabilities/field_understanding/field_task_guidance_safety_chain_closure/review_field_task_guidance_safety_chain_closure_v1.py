# -*- coding: utf-8 -*-
"""Field Task Guidance Safety Chain Closure — review v1."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.field_understanding.field_task_guidance_safety_chain_closure.field_task_guidance_safety_chain_closure_registry_v1 import (
    REGISTRY_ID,
    _SCENARIO_MAP,
    build_field_task_guidance_safety_chain_closure_matrix_v1,
    validate_registry,
)
from capabilities.field_understanding.field_task_guidance_safety_chain_closure.field_task_guidance_safety_chain_closure_types_v1 import (
    ACTION_SAFETY_ENTRYPOINT,
    CLOSED_CHAIN_STAGE_REFS,
    CLOSURE_GOVERNANCE_RULES,
    CLOSURE_PRINCIPLE_ZH,
    FIELD_SYNTHESIS_ENTRYPOINT,
    FINAL_DECISION_CLOSURE_BLOCKED,
    FINAL_DECISION_CLOSURE_GO,
    GUIDANCE_ENTRYPOINT,
    INTERFACE_LAYER_PROTOCOL_REF,
    NON_EXECUTION_FLAGS,
    PHASE_ID,
    PLANNING_OBJECT_TYPES,
    SCENARIO_COVERAGE_REFS,
    SEALED_UPSTREAM_PHASE_REFS,
    SPEECH_GATE_ENTRYPOINT,
    TASK_MANAGER_ENTRYPOINT,
)

DEFAULT_OUTPUT_ROOT = (
    _REPO_ROOT / "_tmp_eval_out" / "field_task_guidance_safety_chain_closure_v1_smoke_v0"
)
REVIEW_FILENAME = "field_task_guidance_safety_chain_closure_review_v1.json"

STEP_FILES = (
    "capabilities/field_understanding/field_task_guidance_safety_chain_closure/"
    "field_task_guidance_safety_chain_closure_types_v1.py",
    "capabilities/field_understanding/field_task_guidance_safety_chain_closure/"
    "field_task_guidance_safety_chain_closure_registry_v1.py",
    "capabilities/field_understanding/field_task_guidance_safety_chain_closure/"
    "review_field_task_guidance_safety_chain_closure_v1.py",
)

_DRYRUN_ARTIFACTS = {
    "field_synthesis": (
        "_tmp_eval_out/field_synthesis_map_place_event_overlay_dryrun_v1_smoke_v0/"
        "field_synthesis_map_place_event_overlay_dryrun_run_and_review_v1.json"
    ),
    "field_to_task": (
        "_tmp_eval_out/field_to_task_alignment_dryrun_v1_smoke_v0/"
        "field_to_task_alignment_dryrun_run_and_review_v1.json"
    ),
    "task_to_guidance": (
        "_tmp_eval_out/task_to_guidance_safety_gate_dryrun_v1_smoke_v0/"
        "task_to_guidance_safety_gate_dryrun_run_and_review_v1.json"
    ),
}


def _load_json(rel: str) -> Optional[Dict[str, Any]]:
    path = _REPO_ROOT / rel
    if not path.is_file():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def _case_passed(artifact: Optional[Dict[str, Any]], case_ref: str, *, ok_key: str) -> bool:
    if not artifact:
        return False
    for result in artifact.get("positive_case_results") or []:
        if result.get("case_ref") == case_ref:
            return result.get(ok_key) is True
    return False


def _verify_scenario_chains() -> Tuple[Dict[str, bool], List[str]]:
    issues: List[str] = []
    fs = _load_json(_DRYRUN_ARTIFACTS["field_synthesis"])
    ft = _load_json(_DRYRUN_ARTIFACTS["field_to_task"])
    tg = _load_json(_DRYRUN_ARTIFACTS["task_to_guidance"])

    checks: Dict[str, bool] = {}
    for entry in _SCENARIO_MAP:
        scenario_ref = entry["scenario_ref"]
        fs_ref = entry["field_synthesis_case_ref"]
        if fs_ref == "home_return_embedded_in_field_to_task":
            fs_ok = _case_passed(ft, entry["field_to_task_case_ref"], ok_key="evaluation_ok")
        else:
            fs_ok = _case_passed(fs, fs_ref, ok_key="evaluation_ok")
        ft_ok = _case_passed(ft, entry["field_to_task_case_ref"], ok_key="evaluation_ok")
        tg_ok = _case_passed(tg, entry["task_to_guidance_case_ref"], ok_key="evaluation_ok")
        closed = fs_ok and ft_ok and tg_ok
        checks[scenario_ref] = closed
        if not closed:
            issues.append(
                f"{scenario_ref}:fs={fs_ok}:ft={ft_ok}:tg={tg_ok}"
            )

    return checks, issues


def _load_upstream_artifact(artifact_rel: str) -> Tuple[Optional[Dict[str, Any]], bool]:
    path = _REPO_ROOT / artifact_rel
    if not path.is_file():
        return None, False
    try:
        return json.loads(path.read_text(encoding="utf-8")), True
    except (OSError, json.JSONDecodeError):
        return None, True


def review_sealed_upstream_artifacts(
    matrix: Dict[str, Any],
) -> Tuple[Dict[str, bool], List[str]]:
    issues: List[str] = []
    checks: Dict[str, bool] = {}

    for entry in matrix.get("sealed_upstream_go_artifacts") or []:
        phase_ref = entry["phase_ref"]
        module_path = _REPO_ROOT / entry["module_rel"]
        checks[f"{phase_ref}.module_present"] = module_path.is_file()
        if not module_path.is_file():
            issues.append(f"upstream_module_missing:{phase_ref}")

        skeleton_rel = entry.get("skeleton_module_rel")
        if skeleton_rel:
            checks[f"{phase_ref}.skeleton_present"] = (_REPO_ROOT / skeleton_rel).is_file()

        artifact_rel = entry.get("artifact_rel")
        if not artifact_rel:
            continue

        artifact, exists = _load_upstream_artifact(artifact_rel)
        checks[f"{phase_ref}.artifact_present"] = exists
        if not exists:
            if entry.get("require_go", True):
                issues.append(f"upstream_artifact_missing:{phase_ref}")
            continue

        if not entry.get("require_go", True):
            checks[f"{phase_ref}.binding_ok"] = checks[f"{phase_ref}.module_present"]
            continue

        actual_go = (artifact or {}).get("final_decision")
        expected_go = entry["expected_go"]
        go_ok = actual_go == expected_go
        checks[f"{phase_ref}.go_sealed"] = go_ok
        if not go_ok:
            issues.append(f"upstream_go_mismatch:{phase_ref}:{actual_go!r}")

    required_go_phases = [
        p for p in SEALED_UPSTREAM_PHASE_REFS
        if p != "Phase-Midplatform-Task-Manager-Controlled-Skeleton-Implementation-DryRun-v1-001"
    ]
    checks["sealed_upstream_phases_verified"] = all(
        checks.get(f"{phase}.go_sealed", False) for phase in required_go_phases
    ) and all(
        checks.get(f"{phase}.module_present", False) for phase in SEALED_UPSTREAM_PHASE_REFS
    )
    if not checks["sealed_upstream_phases_verified"]:
        issues.append("sealed_upstream_phases_not_fully_verified")

    return checks, issues


def validate_closure_matrix_v1(
    matrix: Optional[Dict[str, Any]] = None,
) -> Tuple[bool, List[str]]:
    matrix = matrix or build_field_task_guidance_safety_chain_closure_matrix_v1()
    issues: List[str] = []

    registry_ok, registry_issues = validate_registry()
    issues.extend(registry_issues)

    closure = matrix.get("field_task_guidance_safety_chain_closure") or {}
    if closure.get("field_synthesis_entrypoint") != FIELD_SYNTHESIS_ENTRYPOINT:
        issues.append("field_synthesis_entrypoint_mismatch")
    if closure.get("task_manager_entrypoint") != TASK_MANAGER_ENTRYPOINT:
        issues.append("task_manager_entrypoint_mismatch")
    if closure.get("guidance_entrypoint") != GUIDANCE_ENTRYPOINT:
        issues.append("guidance_entrypoint_mismatch")
    if closure.get("speech_gate_entrypoint") != SPEECH_GATE_ENTRYPOINT:
        issues.append("speech_gate_entrypoint_mismatch")
    if closure.get("action_safety_entrypoint") != ACTION_SAFETY_ENTRYPOINT:
        issues.append("action_safety_entrypoint_mismatch")
    if closure.get("interface_layer_protocol_ref") != INTERFACE_LAYER_PROTOCOL_REF:
        issues.append("interface_layer_protocol_ref_mismatch")
    if tuple(closure.get("governance_rules") or ()) != CLOSURE_GOVERNANCE_RULES:
        issues.append("closure_governance_rules_mismatch")

    stages = matrix.get("closed_chain_stages") or []
    if len(stages) != 6:
        issues.append(f"closed_stage_count:{len(stages)}")

    stage_refs = {s.get("stage_ref") for s in stages}
    if stage_refs != set(CLOSED_CHAIN_STAGE_REFS):
        issues.append(f"closed_chain_stage_refs_mismatch:{sorted(stage_refs)!r}")

    for stage in stages:
        if stage.get("chain_closed") is not True:
            issues.append(f"{stage.get('stage_ref')}.chain_not_closed")

    capability = matrix.get("capability_coverage") or {}
    for flag in (
        "pose_supported",
        "motion_supported",
        "health_supported",
        "anchor_supported",
        "relocalization_supported",
        "drift_supported",
        "spatial_odometry_fusion_supported",
        "field_conflict_candidate_supported",
        "field_candidate_supported",
        "task_context_candidate_supported",
        "task_evidence_need_candidate_supported",
        "task_route_hint_candidate_supported",
        "task_risk_candidate_supported",
        "guidance_candidate_supported",
        "speech_gate_candidate_supported",
        "action_safety_candidate_supported",
    ):
        if capability.get(flag) is not True:
            issues.append(f"capability_coverage.{flag}=false")

    governance = matrix.get("governance_coverage") or {}
    for flag in (
        "candidate_only_enforced",
        "source_chain_preserved",
        "gps_does_not_override_field_identity",
        "slam_does_not_override_field_identity",
        "event_overlay_does_not_rewrite_map_place",
        "field_interaction_label_separated",
        "task_route_hint_not_action",
        "guidance_candidate_not_runtime_navigation",
        "speech_gate_candidate_not_tts",
        "action_safety_candidate_required",
        "gps_slam_conflict_blocks_action_like_guidance",
    ):
        if governance.get(flag) is not True:
            issues.append(f"governance_coverage.{flag}=false")

    scenarios = matrix.get("scenario_coverage") or []
    if len(scenarios) != 6:
        issues.append(f"scenario_coverage_count:{len(scenarios)}")

    return len(issues) == 0 and registry_ok, issues


def review_field_task_guidance_safety_chain_closure_v1(
    *,
    output_root: Optional[str] = None,
    write_file: bool = True,
) -> Dict[str, Any]:
    matrix = build_field_task_guidance_safety_chain_closure_matrix_v1()
    matrix_ok, matrix_issues = validate_closure_matrix_v1(matrix)
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

    scenario_checks, scenario_issues = _verify_scenario_chains()
    failed_checks.extend(scenario_issues)

    capability = matrix.get("capability_coverage") or {}
    governance = matrix.get("governance_coverage") or {}
    stages = matrix.get("closed_chain_stages") or []

    stage_closed = {s["stage_ref"]: s.get("chain_closed") is True for s in stages}

    review_checkpoints: Dict[str, Any] = {
        "closed_stage_count": len(stages),
        "sealed_upstream_phases_verified": upstream_checks.get("sealed_upstream_phases_verified", False),
        **scenario_checks,
        **stage_closed,
        "spatial_evidence_ingest_chain_closed": stage_closed.get("spatial_evidence_ingest_chain"),
        "field_alignment_chain_closed": stage_closed.get("field_alignment_chain"),
        "field_synthesis_chain_closed": stage_closed.get("field_synthesis_chain"),
        "field_to_task_chain_closed": stage_closed.get("field_to_task_chain"),
        "task_to_guidance_chain_closed": stage_closed.get("task_to_guidance_chain"),
        "governance_and_safety_chain_closed": stage_closed.get("governance_and_safety_chain"),
        **{k: capability.get(k) for k in capability if k.endswith("_supported")},
        "candidate_only_enforced": governance.get("candidate_only_enforced"),
        "source_chain_preserved": governance.get("source_chain_preserved"),
        "gps_does_not_override_field_identity": governance.get("gps_does_not_override_field_identity"),
        "slam_does_not_override_field_identity": governance.get("slam_does_not_override_field_identity"),
        "event_overlay_does_not_rewrite_map_place": governance.get("event_overlay_does_not_rewrite_map_place"),
        "field_interaction_label_separated": governance.get("field_interaction_label_separated"),
        "task_route_hint_not_action": governance.get("task_route_hint_not_action"),
        "guidance_candidate_not_runtime_navigation": governance.get("guidance_candidate_not_runtime_navigation"),
        "speech_gate_candidate_not_tts": governance.get("speech_gate_candidate_not_tts"),
        "action_safety_candidate_required": governance.get("action_safety_candidate_required"),
        "gps_slam_conflict_blocks_action_like_guidance": governance.get(
            "gps_slam_conflict_blocks_action_like_guidance"
        ),
        "field_synthesis_entrypoint_locked": FIELD_SYNTHESIS_ENTRYPOINT,
        "task_manager_entrypoint_locked": TASK_MANAGER_ENTRYPOINT,
        "guidance_entrypoint_locked": GUIDANCE_ENTRYPOINT,
        "speech_gate_entrypoint_locked": SPEECH_GATE_ENTRYPOINT,
        "action_safety_entrypoint_locked": ACTION_SAFETY_ENTRYPOINT,
        "real_navigation_started": False,
        "real_map_api_connected": False,
        "real_gps_connected": False,
        "live_sensor_connected": False,
        "runtime_activation_allowed": False,
        "direct_action_allowed": False,
        "direct_speech_allowed": False,
        "direct_fact_write_allowed": False,
    }

    go_conditions = {
        "closed_stage_count_eq_6": review_checkpoints["closed_stage_count"] == 6,
        "sealed_upstream_phases_verified": review_checkpoints["sealed_upstream_phases_verified"] is True,
        "spatial_evidence_ingest_chain_closed": review_checkpoints["spatial_evidence_ingest_chain_closed"] is True,
        "field_alignment_chain_closed": review_checkpoints["field_alignment_chain_closed"] is True,
        "field_synthesis_chain_closed": review_checkpoints["field_synthesis_chain_closed"] is True,
        "field_to_task_chain_closed": review_checkpoints["field_to_task_chain_closed"] is True,
        "task_to_guidance_chain_closed": review_checkpoints["task_to_guidance_chain_closed"] is True,
        "governance_and_safety_chain_closed": review_checkpoints["governance_and_safety_chain_closed"] is True,
        **{ref: review_checkpoints.get(ref) is True for ref in SCENARIO_COVERAGE_REFS},
        "pose_supported": capability.get("pose_supported") is True,
        "motion_supported": capability.get("motion_supported") is True,
        "health_supported": capability.get("health_supported") is True,
        "anchor_supported": capability.get("anchor_supported") is True,
        "relocalization_supported": capability.get("relocalization_supported") is True,
        "drift_supported": capability.get("drift_supported") is True,
        "spatial_odometry_fusion_supported": capability.get("spatial_odometry_fusion_supported") is True,
        "field_conflict_candidate_supported": capability.get("field_conflict_candidate_supported") is True,
        "field_candidate_supported": capability.get("field_candidate_supported") is True,
        "task_context_candidate_supported": capability.get("task_context_candidate_supported") is True,
        "task_evidence_need_candidate_supported": capability.get("task_evidence_need_candidate_supported") is True,
        "task_route_hint_candidate_supported": capability.get("task_route_hint_candidate_supported") is True,
        "task_risk_candidate_supported": capability.get("task_risk_candidate_supported") is True,
        "guidance_candidate_supported": capability.get("guidance_candidate_supported") is True,
        "speech_gate_candidate_supported": capability.get("speech_gate_candidate_supported") is True,
        "action_safety_candidate_supported": capability.get("action_safety_candidate_supported") is True,
        "candidate_only_enforced": governance.get("candidate_only_enforced") is True,
        "source_chain_preserved": governance.get("source_chain_preserved") is True,
        "gps_does_not_override_field_identity": governance.get("gps_does_not_override_field_identity") is True,
        "slam_does_not_override_field_identity": governance.get("slam_does_not_override_field_identity") is True,
        "event_overlay_does_not_rewrite_map_place": governance.get("event_overlay_does_not_rewrite_map_place") is True,
        "field_interaction_label_separated": governance.get("field_interaction_label_separated") is True,
        "task_route_hint_not_action": governance.get("task_route_hint_not_action") is True,
        "guidance_candidate_not_runtime_navigation": governance.get("guidance_candidate_not_runtime_navigation") is True,
        "speech_gate_candidate_not_tts": governance.get("speech_gate_candidate_not_tts") is True,
        "action_safety_candidate_required": governance.get("action_safety_candidate_required") is True,
        "gps_slam_conflict_blocks_action_like_guidance": governance.get(
            "gps_slam_conflict_blocks_action_like_guidance"
        )
        is True,
        "real_navigation_started_false": review_checkpoints["real_navigation_started"] is False,
        "real_map_api_connected_false": review_checkpoints["real_map_api_connected"] is False,
        "real_gps_connected_false": review_checkpoints["real_gps_connected"] is False,
        "live_sensor_connected_false": review_checkpoints["live_sensor_connected"] is False,
        "runtime_activation_allowed_false": review_checkpoints["runtime_activation_allowed"] is False,
        "direct_action_allowed_false": review_checkpoints["direct_action_allowed"] is False,
        "direct_speech_allowed_false": review_checkpoints["direct_speech_allowed"] is False,
        "direct_fact_write_allowed_false": review_checkpoints["direct_fact_write_allowed"] is False,
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
        "step": "Field Task Guidance Safety Chain Closure Matrix + Review",
        "lifecycle_variant": "compressed_master_chain_closure_review",
        "closure_principle_zh": CLOSURE_PRINCIPLE_ZH,
        "registry_id": REGISTRY_ID,
        "planning_object_types": list(PLANNING_OBJECT_TYPES),
        "master_chain_pipeline": list(matrix.get("master_chain_pipeline") or []),
        "closure_governance_rules": list(CLOSURE_GOVERNANCE_RULES),
        "non_execution_flags": dict(NON_EXECUTION_FLAGS),
        "matrix_review_ok": matrix_ok,
        "upstream_sealed_phase_review": upstream_checks,
        "scenario_chain_verification": scenario_checks,
        "go_conditions": go_conditions,
        "review_checkpoints": review_checkpoints,
        "closure_matrix": matrix,
        "conclusions": {
            "phase_one_environment_cognition_chain_status": "sealed" if review_ok else "blocked",
            "master_chain_sealed": review_ok,
            "field_synthesis_entrypoint_locked": FIELD_SYNTHESIS_ENTRYPOINT,
            "task_manager_entrypoint_locked": TASK_MANAGER_ENTRYPOINT,
            "guidance_safety_entrypoints_locked": {
                "guidance": GUIDANCE_ENTRYPOINT,
                "speech_gate": SPEECH_GATE_ENTRYPOINT,
                "action_safety": ACTION_SAFETY_ENTRYPOINT,
            },
            "deferred_expansion_lines": [
                "Vision evidence: OCR / object detection / tracking / segmentation (observation pool)",
                "Spatial semantics: Kimera / Hydra / scene graph",
                "Runtime admission: candidate-only to controlled runtime trial",
            ],
        },
        "blocker_count": blocker_count,
        "failed_checks": failed_checks,
        "passed_checks": passed_checks,
        "final_decision": FINAL_DECISION_CLOSURE_GO if review_ok else FINAL_DECISION_CLOSURE_BLOCKED,
    }

    if write_file:
        out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
        out_root.mkdir(parents=True, exist_ok=True)
        out_path = out_root / REVIEW_FILENAME
        out_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        result["output_review_file"] = str(out_path)

    return result


def main() -> int:
    result = review_field_task_guidance_safety_chain_closure_v1()
    checkpoints = result["review_checkpoints"]
    print(
        json.dumps(
            {
                "output_review_file": result.get("output_review_file"),
                "closed_stage_count": checkpoints["closed_stage_count"],
                "sealed_upstream_phases_verified": checkpoints["sealed_upstream_phases_verified"],
                "mall_find_entrance_chain_closed": checkpoints.get("mall_find_entrance_chain_closed"),
                "gps_slam_conflict_chain_closed": checkpoints.get("gps_slam_conflict_chain_closed"),
                "action_safety_candidate_supported": checkpoints.get("action_safety_candidate_supported"),
                "blocker_count": result["blocker_count"],
                "final_decision": result["final_decision"],
            },
            ensure_ascii=False,
        )
    )
    return 0 if result["final_decision"] == FINAL_DECISION_CLOSURE_GO else 1


if __name__ == "__main__":
    raise SystemExit(main())
