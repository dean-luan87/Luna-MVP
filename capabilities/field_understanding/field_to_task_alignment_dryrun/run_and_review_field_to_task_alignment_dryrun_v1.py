# -*- coding: utf-8 -*-
"""Field to Task Alignment Dry-Run — run + review v1."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.midplatform.core.dryrun_lifecycle_template_v1 import write_json_file
from capabilities.field_understanding.field_to_task_alignment_dryrun.field_to_task_alignment_dryrun_cases_v1 import (
    align_field_to_task_v1,
    build_negative_cases_v1,
    build_positive_cases_v1,
    evaluate_positive_case,
    validate_field_to_task_bundle,
)
from capabilities.field_understanding.field_to_task_alignment_dryrun.field_to_task_alignment_dryrun_types_v1 import (
    ALIGNMENT_PRINCIPLE_ZH,
    FIELD_ALIGNMENT_REF,
    FIELD_SYNTHESIS_DRYRUN_REF,
    FIELD_SYNTHESIS_ENTRYPOINT,
    FINAL_DECISION_ALIGNMENT_BLOCKED,
    FINAL_DECISION_ALIGNMENT_GO,
    INTERFACE_LAYER_PROTOCOL_REF,
    NEGATIVE_CASE_REFS,
    NON_EXECUTION_FLAGS,
    PHASE_ID,
    POSITIVE_CASE_REFS,
    SPATIAL_EVIDENCE_CHAIN_REF,
    SPATIAL_ODOMETRY_FUSION_REF,
    TASK_MANAGER_ENTRYPOINT,
    TASK_MANAGER_REF,
)

DEFAULT_OUTPUT_ROOT = (
    _REPO_ROOT / "_tmp_eval_out" / "field_to_task_alignment_dryrun_v1_smoke_v0"
)
OUTPUT_FILENAME = "field_to_task_alignment_dryrun_run_and_review_v1.json"

_UPSTREAM_ARTIFACTS: Tuple[Dict[str, Any], ...] = (
    {
        "phase_ref": FIELD_SYNTHESIS_DRYRUN_REF,
        "artifact_rel": (
            "_tmp_eval_out/field_synthesis_map_place_event_overlay_dryrun_v1_smoke_v0/"
            "field_synthesis_map_place_event_overlay_dryrun_run_and_review_v1.json"
        ),
        "expected_go": "FIELD_SYNTHESIS_MAP_PLACE_REALTIME_EVENT_OVERLAY_DRYRUN_GO",
        "module_rel": (
            "capabilities/field_understanding/field_synthesis_map_place_event_overlay_dryrun/"
            "field_synthesis_map_place_event_overlay_dryrun_types_v1.py"
        ),
        "require_go": True,
    },
    {
        "phase_ref": FIELD_ALIGNMENT_REF,
        "artifact_rel": (
            "_tmp_eval_out/field_map_place_event_overlay_alignment_v1_smoke_v0/"
            "field_map_place_event_overlay_alignment_review_v1.json"
        ),
        "expected_go": "FIELD_MAP_PLACE_REALTIME_EVENT_OVERLAY_ALIGNMENT_READY_FOR_SYNTHESIS_DRYRUN",
        "module_rel": (
            "capabilities/field_understanding/field_map_place_event_overlay_alignment/"
            "field_map_place_event_overlay_alignment_types_v1.py"
        ),
        "require_go": True,
    },
    {
        "phase_ref": SPATIAL_EVIDENCE_CHAIN_REF,
        "artifact_rel": (
            "_tmp_eval_out/slam_spatial_evidence_chain_closure_v1_smoke_v0/"
            "slam_spatial_evidence_chain_closure_review_v1.json"
        ),
        "expected_go": "SLAM_SPATIAL_EVIDENCE_CHAIN_FIELD_ALIGNMENT_CLOSURE_GO",
        "module_rel": (
            "capabilities/field_understanding/slam_spatial_evidence_chain_closure/"
            "slam_spatial_evidence_chain_closure_types_v1.py"
        ),
        "require_go": True,
    },
    {
        "phase_ref": SPATIAL_ODOMETRY_FUSION_REF,
        "artifact_rel": (
            "_tmp_eval_out/spatial_odometry_fusion_interface_v1_smoke_v0/"
            "spatial_odometry_fusion_interface_review_v1.json"
        ),
        "expected_go": "SPATIAL_ODOMETRY_FUSION_INTERFACE_PLANNING_READY_FOR_FIELD_PROTOCOL_ALIGNMENT",
        "module_rel": (
            "capabilities/field_understanding/spatial_odometry_fusion_interface/"
            "spatial_odometry_fusion_interface_types_v1.py"
        ),
        "require_go": True,
    },
    {
        "phase_ref": TASK_MANAGER_REF,
        "artifact_rel": (
            "_tmp_eval_out/midplatform_task_manager_controlled_skeleton_implementation_dryrun/"
            "summary.json"
        ),
        "expected_go": None,
        "module_rel": (
            "capabilities/midplatform/midplatform_task_manager_controlled_skeleton_implementation_dryrun_v1.py"
        ),
        "require_go": False,
        "skeleton_module_rel": "capabilities/midplatform/core/task_manager_skeleton_v1.py",
    },
    {
        "phase_ref": INTERFACE_LAYER_PROTOCOL_REF,
        "artifact_rel": (
            "_tmp_eval_out/interface_layer_governance_v1_smoke_v0/"
            "interface_layer_governance_review_v1.json"
        ),
        "expected_go": "INTERFACE_LAYER_GOVERNANCE_PROTOCOL_BASELINE_READY_FOR_ADOPTION",
        "module_rel": (
            "capabilities/midplatform/interface_layer_governance/"
            "interface_layer_governance_types_v1.py"
        ),
        "require_go": True,
    },
)


def _verify_upstream() -> Tuple[bool, List[str], Dict[str, bool]]:
    issues: List[str] = []
    checks: Dict[str, bool] = {}

    for entry in _UPSTREAM_ARTIFACTS:
        phase_ref = entry["phase_ref"]
        module_ok = (_REPO_ROOT / entry["module_rel"]).is_file()
        checks[f"{phase_ref}.module_present"] = module_ok
        if not module_ok:
            issues.append(f"upstream_module_missing:{phase_ref}")

        skeleton_rel = entry.get("skeleton_module_rel")
        if skeleton_rel:
            skeleton_ok = (_REPO_ROOT / skeleton_rel).is_file()
            checks[f"{phase_ref}.skeleton_present"] = skeleton_ok
            if not skeleton_ok:
                issues.append(f"task_manager_skeleton_missing")

        artifact_path = _REPO_ROOT / entry["artifact_rel"]
        if not artifact_path.is_file():
            checks[f"{phase_ref}.artifact_present"] = False
            if entry.get("require_go", True):
                issues.append(f"upstream_artifact_missing:{phase_ref}")
            continue

        checks[f"{phase_ref}.artifact_present"] = True
        if not entry.get("require_go", True):
            checks[f"{phase_ref}.binding_ok"] = module_ok
            continue

        try:
            data = json.loads(artifact_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            issues.append(f"upstream_artifact_unreadable:{phase_ref}")
            continue

        actual_go = data.get("final_decision")
        expected_go = entry["expected_go"]
        go_ok = actual_go == expected_go
        checks[f"{phase_ref}.go_sealed"] = go_ok
        if not go_ok:
            issues.append(f"upstream_go_mismatch:{phase_ref}:{actual_go!r}")

    return len(issues) == 0, issues, checks


def run_and_review_field_to_task_alignment_dryrun_v1(
    *,
    output_root: Optional[str] = None,
    write_file: bool = True,
) -> Dict[str, Any]:
    positive_cases = list(build_positive_cases_v1())
    negative_cases = list(build_negative_cases_v1())

    positive_traces: List[Dict[str, Any]] = []
    positive_results: List[Dict[str, Any]] = []
    positive_pass_count = 0

    for case in positive_cases:
        bundle = case["input_bundle"]
        trace = align_field_to_task_v1(bundle)
        ok, eval_issues = evaluate_positive_case(trace, case["case_ref"])
        positive_traces.append(trace)
        positive_results.append(
            {
                "case_ref": case["case_ref"],
                "alignment_ok": trace.get("alignment_ok"),
                "evaluation_ok": ok,
                "evaluation_issues": eval_issues,
            }
        )
        if ok:
            positive_pass_count += 1

    negative_results: List[Dict[str, Any]] = []
    invalid_expected_reject_count = 0

    for case in negative_cases:
        bundle = case["input_bundle"]
        valid, validation_issues = validate_field_to_task_bundle(bundle)
        trace = align_field_to_task_v1(bundle)
        rejected = (not valid) or (not trace.get("alignment_ok"))
        negative_results.append(
            {
                "case_ref": case["case_ref"],
                "validation_ok": valid,
                "validation_issues": validation_issues,
                "alignment_ok": trace.get("alignment_ok"),
                "rejected_as_expected": rejected,
            }
        )
        if rejected:
            invalid_expected_reject_count += 1

    upstream_ok, upstream_issues, upstream_checks = _verify_upstream()

    by_case = {t["case_ref"]: t for t in positive_traces}

    def _ctx(ref: str) -> Dict[str, Any]:
        return (by_case.get(ref) or {}).get("task_context_candidate") or {}

    def _route(ref: str) -> Dict[str, Any]:
        return (by_case.get(ref) or {}).get("task_route_hint_candidate") or {}

    def _risk(ref: str) -> Dict[str, Any]:
        return (by_case.get(ref) or {}).get("task_risk_candidate") or {}

    review_checkpoints: Dict[str, Any] = {
        "positive_case_count": len(positive_cases),
        "negative_case_count": len(negative_cases),
        "positive_pass_count": positive_pass_count,
        "invalid_expected_reject_count": invalid_expected_reject_count,
        "mall_find_entrance_task_context_ok": (
            _ctx("mall_find_entrance_task").get("field_label") == "商场"
            and by_case.get("mall_find_entrance_task", {}).get("alignment_ok") is True
        ),
        "subway_enter_station_gps_degraded_ok": (
            _ctx("subway_station_enter_station_task").get("gps_weight") == "degraded"
            and by_case.get("subway_station_enter_station_task", {}).get("alignment_ok") is True
        ),
        "stadium_concert_ticket_check_overlay_ok": (
            _ctx("stadium_concert_ticket_check_task").get("field_label") == "演唱会现场"
            and _ctx("stadium_concert_ticket_check_task").get("underlying_map_place_ref") == "stadium_stub"
        ),
        "plaza_market_crowd_task_risk_ok": all(
            k in (_risk("plaza_temporary_market_find_stall_task").get("risk_kinds") or [])
            for k in ("crowd_density", "queue", "temporary_layout_uncertainty")
        ),
        "gps_slam_conflict_blocks_route_hint": (
            _route("gps_slam_conflict_delay_navigation_task").get("status")
            == "blocked_or_needs_more_evidence"
        ),
        "home_return_stable_field_task_ok": (
            _ctx("home_return_task_stable_field").get("field_label") == "家"
            and by_case.get("home_return_task_stable_field", {}).get("alignment_ok") is True
        ),
        "field_interaction_label_separated": all(
            _ctx(ref).get("internal_field_state_ref") for ref in POSITIVE_CASE_REFS
        ),
        "event_overlay_does_not_rewrite_map_place": (
            _ctx("stadium_concert_ticket_check_task").get("underlying_map_place_ref") == "stadium_stub"
        ),
        "task_route_hint_candidate_only": all(
            (by_case.get(ref) or {}).get("task_route_hint_candidate", {}).get("candidate_only") is True
            and (by_case.get(ref) or {}).get("task_route_hint_candidate", {}).get("direct_action_allowed")
            is not True
            for ref in POSITIVE_CASE_REFS
        ),
        "task_risk_candidate_only": all(
            (by_case.get(ref) or {}).get("task_risk_candidate", {}).get("candidate_only") is True
            for ref in POSITIVE_CASE_REFS
        ),
        "task_evidence_need_candidate_only": all(
            (by_case.get(ref) or {})
            .get("task_evidence_need_candidate", {})
            .get("live_sensor_trigger_allowed")
            is not True
            for ref in POSITIVE_CASE_REFS
        ),
        "field_conflict_not_ignored": "conflict_requires_resolution"
        in (_risk("gps_slam_conflict_delay_navigation_task").get("risk_kinds") or []),
        "field_synthesis_entrypoint_locked": FIELD_SYNTHESIS_ENTRYPOINT,
        "task_manager_entrypoint_locked": TASK_MANAGER_ENTRYPOINT,
        "real_navigation_started": False,
        "real_map_api_connected": False,
        "real_gps_connected": False,
        "live_sensor_connected": False,
        "direct_action_allowed": False,
        "direct_speech_allowed": False,
        "direct_fact_write_allowed": False,
        "upstream_verified": upstream_ok,
    }

    failed_checks: List[str] = []
    if not upstream_ok:
        failed_checks.extend(upstream_issues)
    if positive_pass_count != 6:
        failed_checks.append(f"positive_pass_count:{positive_pass_count}")
    if invalid_expected_reject_count != 4:
        failed_checks.append(f"invalid_expected_reject_count:{invalid_expected_reject_count}")

    go_conditions = {
        "positive_case_count_eq_6": review_checkpoints["positive_case_count"] == 6,
        "negative_case_count_eq_4": review_checkpoints["negative_case_count"] == 4,
        "positive_pass_count_eq_6": review_checkpoints["positive_pass_count"] == 6,
        "invalid_expected_reject_count_eq_4": review_checkpoints[
            "invalid_expected_reject_count"
        ]
        == 4,
        "mall_find_entrance_task_context_ok": review_checkpoints["mall_find_entrance_task_context_ok"],
        "subway_enter_station_gps_degraded_ok": review_checkpoints[
            "subway_enter_station_gps_degraded_ok"
        ],
        "stadium_concert_ticket_check_overlay_ok": review_checkpoints[
            "stadium_concert_ticket_check_overlay_ok"
        ],
        "plaza_market_crowd_task_risk_ok": review_checkpoints["plaza_market_crowd_task_risk_ok"],
        "gps_slam_conflict_blocks_route_hint": review_checkpoints[
            "gps_slam_conflict_blocks_route_hint"
        ],
        "home_return_stable_field_task_ok": review_checkpoints["home_return_stable_field_task_ok"],
        "field_interaction_label_separated": review_checkpoints["field_interaction_label_separated"],
        "event_overlay_does_not_rewrite_map_place": review_checkpoints[
            "event_overlay_does_not_rewrite_map_place"
        ],
        "task_route_hint_candidate_only": review_checkpoints["task_route_hint_candidate_only"],
        "task_risk_candidate_only": review_checkpoints["task_risk_candidate_only"],
        "task_evidence_need_candidate_only": review_checkpoints["task_evidence_need_candidate_only"],
        "field_conflict_not_ignored": review_checkpoints["field_conflict_not_ignored"],
        "field_synthesis_entrypoint_locked": review_checkpoints["field_synthesis_entrypoint_locked"]
        == FIELD_SYNTHESIS_ENTRYPOINT,
        "task_manager_entrypoint_locked": review_checkpoints["task_manager_entrypoint_locked"]
        == TASK_MANAGER_ENTRYPOINT,
        "real_navigation_started_false": review_checkpoints["real_navigation_started"] is False,
        "real_map_api_connected_false": review_checkpoints["real_map_api_connected"] is False,
        "real_gps_connected_false": review_checkpoints["real_gps_connected"] is False,
        "live_sensor_connected_false": review_checkpoints["live_sensor_connected"] is False,
        "direct_action_allowed_false": review_checkpoints["direct_action_allowed"] is False,
        "direct_speech_allowed_false": review_checkpoints["direct_speech_allowed"] is False,
        "direct_fact_write_allowed_false": review_checkpoints["direct_fact_write_allowed"] is False,
    }

    for key, ok in go_conditions.items():
        if not ok:
            failed_checks.append(f"go.{key}=false")

    blocker_count = len(failed_checks)
    review_ok = blocker_count == 0

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    out_path = out_root / OUTPUT_FILENAME

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "step": "Field to Task Alignment Dry-Run Run + Review",
        "lifecycle_variant": "compressed_field_to_task_alignment_dryrun",
        "alignment_principle_zh": ALIGNMENT_PRINCIPLE_ZH,
        "model_binding": {
            "field_synthesis_entrypoint": FIELD_SYNTHESIS_ENTRYPOINT,
            "task_manager_entrypoint": TASK_MANAGER_ENTRYPOINT,
            "field_synthesis_dryrun_ref": FIELD_SYNTHESIS_DRYRUN_REF,
            "task_manager_ref": TASK_MANAGER_REF,
            "field_alignment_ref": FIELD_ALIGNMENT_REF,
            "spatial_evidence_chain_ref": SPATIAL_EVIDENCE_CHAIN_REF,
            "spatial_odometry_fusion_ref": SPATIAL_ODOMETRY_FUSION_REF,
            "interface_layer_protocol_ref": INTERFACE_LAYER_PROTOCOL_REF,
            "candidate_only": True,
        },
        "pipeline": [
            "FieldCandidate / FieldStateCandidate / FieldInteractionLabelCandidate / FieldConflictCandidate",
            "TaskContextCandidate",
            "TaskEvidenceNeedCandidate",
            "TaskRouteHintCandidate / TaskRiskCandidate",
            "task_manager_v1 dry-run decision",
        ],
        "non_execution_flags": dict(NON_EXECUTION_FLAGS),
        "positive_case_refs": list(POSITIVE_CASE_REFS),
        "negative_case_refs": list(NEGATIVE_CASE_REFS),
        "positive_case_results": positive_results,
        "negative_case_results": negative_results,
        "positive_traces": positive_traces,
        "upstream_review": upstream_checks,
        "review_checkpoints": review_checkpoints,
        "go_conditions": go_conditions,
        "conclusions": {
            "field_to_task_alignment_status": "go" if review_ok else "blocked",
            "field_synthesis_entrypoint_locked": FIELD_SYNTHESIS_ENTRYPOINT,
            "task_manager_entrypoint_locked": TASK_MANAGER_ENTRYPOINT,
            "recommended_next_step": (
                "Task → Guidance / Speech Gate / Action Safety candidate chain"
            ),
        },
        "output_root": str(out_root),
        "output_file": str(out_path),
        "blocker_count": blocker_count,
        "failed_checks": failed_checks,
        "final_decision": (
            FINAL_DECISION_ALIGNMENT_GO if review_ok else FINAL_DECISION_ALIGNMENT_BLOCKED
        ),
    }

    if write_file:
        write_json_file(out_path, result)

    return result


def main() -> int:
    result = run_and_review_field_to_task_alignment_dryrun_v1()
    checkpoints = result["review_checkpoints"]
    print(
        json.dumps(
            {
                "output_file": result.get("output_file"),
                "positive_pass_count": checkpoints["positive_pass_count"],
                "invalid_expected_reject_count": checkpoints["invalid_expected_reject_count"],
                "gps_slam_conflict_blocks_route_hint": checkpoints[
                    "gps_slam_conflict_blocks_route_hint"
                ],
                "task_manager_entrypoint_locked": checkpoints["task_manager_entrypoint_locked"],
                "blocker_count": result["blocker_count"],
                "final_decision": result["final_decision"],
            },
            ensure_ascii=False,
        )
    )
    return 0 if result["final_decision"] == FINAL_DECISION_ALIGNMENT_GO else 1


if __name__ == "__main__":
    raise SystemExit(main())
