# -*- coding: utf-8 -*-
"""Task to Guidance Safety Gate Dry-Run — run + review v1."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.midplatform.core.dryrun_lifecycle_template_v1 import write_json_file
from capabilities.field_understanding.task_to_guidance_safety_gate_dryrun.task_to_guidance_safety_gate_dryrun_cases_v1 import (
    align_task_to_guidance_safety_v1,
    build_negative_cases_v1,
    build_positive_cases_v1,
    evaluate_positive_case,
    validate_task_to_guidance_bundle,
)
from capabilities.field_understanding.task_to_guidance_safety_gate_dryrun.task_to_guidance_safety_gate_dryrun_types_v1 import (
    ACTION_SAFETY_ENTRYPOINT,
    BASIC_NAVIGATION_GUIDANCE_LOOP_REF,
    DRYRUN_PRINCIPLE_ZH,
    FIELD_SYNTHESIS_DRYRUN_REF,
    FIELD_TO_TASK_DRYRUN_REF,
    FINAL_DECISION_DRYRUN_BLOCKED,
    FINAL_DECISION_DRYRUN_GO,
    GUIDANCE_ENTRYPOINT,
    INTERFACE_LAYER_PROTOCOL_REF,
    NEGATIVE_CASE_REFS,
    NON_EXECUTION_FLAGS,
    PHASE_ID,
    POSITIVE_CASE_REFS,
    SPEECH_GATE_ENTRYPOINT,
    TASK_MANAGER_ENTRYPOINT,
    TASK_MANAGER_REF,
)

DEFAULT_OUTPUT_ROOT = (
    _REPO_ROOT / "_tmp_eval_out" / "task_to_guidance_safety_gate_dryrun_v1_smoke_v0"
)
OUTPUT_FILENAME = "task_to_guidance_safety_gate_dryrun_run_and_review_v1.json"

_UPSTREAM_ARTIFACTS: Tuple[Dict[str, Any], ...] = (
    {
        "phase_ref": FIELD_TO_TASK_DRYRUN_REF,
        "artifact_rel": (
            "_tmp_eval_out/field_to_task_alignment_dryrun_v1_smoke_v0/"
            "field_to_task_alignment_dryrun_run_and_review_v1.json"
        ),
        "expected_go": "FIELD_TO_TASK_ALIGNMENT_DRYRUN_GO",
        "module_rel": (
            "capabilities/field_understanding/field_to_task_alignment_dryrun/"
            "field_to_task_alignment_dryrun_types_v1.py"
        ),
        "require_go": True,
    },
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
        "phase_ref": BASIC_NAVIGATION_GUIDANCE_LOOP_REF,
        "artifact_rel": None,
        "expected_go": None,
        "module_rel": "capabilities/midplatform/basic_navigation_guidance_loop_dryrun_v1.py",
        "require_go": False,
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
            checks[f"{phase_ref}.skeleton_present"] = (_REPO_ROOT / skeleton_rel).is_file()

        artifact_rel = entry.get("artifact_rel")
        if not artifact_rel:
            checks[f"{phase_ref}.binding_ok"] = module_ok
            continue

        artifact_path = _REPO_ROOT / artifact_rel
        if not artifact_path.is_file():
            checks[f"{phase_ref}.artifact_present"] = False
            if entry.get("require_go", True):
                issues.append(f"upstream_artifact_missing:{phase_ref}")
            continue

        checks[f"{phase_ref}.artifact_present"] = True
        if not entry.get("require_go", True):
            continue

        try:
            data = json.loads(artifact_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            issues.append(f"upstream_artifact_unreadable:{phase_ref}")
            continue

        expected_go = entry["expected_go"]
        go_ok = data.get("final_decision") == expected_go
        checks[f"{phase_ref}.go_sealed"] = go_ok
        if not go_ok:
            issues.append(f"upstream_go_mismatch:{phase_ref}:{data.get('final_decision')!r}")

    return len(issues) == 0, issues, checks


def run_and_review_task_to_guidance_safety_gate_dryrun_v1(
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
        trace = align_task_to_guidance_safety_v1(bundle)
        ok, eval_issues = evaluate_positive_case(trace, case["case_ref"])
        positive_traces.append(trace)
        positive_results.append(
            {
                "case_ref": case["case_ref"],
                "guidance_ok": trace.get("guidance_ok"),
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
        valid, validation_issues = validate_task_to_guidance_bundle(bundle)
        trace = align_task_to_guidance_safety_v1(bundle)
        rejected = (not valid) or (not trace.get("guidance_ok"))
        negative_results.append(
            {
                "case_ref": case["case_ref"],
                "validation_ok": valid,
                "validation_issues": validation_issues,
                "guidance_ok": trace.get("guidance_ok"),
                "rejected_as_expected": rejected,
            }
        )
        if rejected:
            invalid_expected_reject_count += 1

    upstream_ok, upstream_issues, upstream_checks = _verify_upstream()
    by_case = {t["case_ref"]: t for t in positive_traces}

    def _g(ref: str) -> Dict[str, Any]:
        return (by_case.get(ref) or {}).get("guidance_candidate") or {}

    def _s(ref: str) -> Dict[str, Any]:
        return (by_case.get(ref) or {}).get("speech_gate_candidate") or {}

    def _a(ref: str) -> Dict[str, Any]:
        return (by_case.get(ref) or {}).get("action_safety_candidate") or {}

    review_checkpoints: Dict[str, Any] = {
        "positive_case_count": len(positive_cases),
        "negative_case_count": len(negative_cases),
        "positive_pass_count": positive_pass_count,
        "invalid_expected_reject_count": invalid_expected_reject_count,
        "mall_find_entrance_guidance_candidate_ok": (
            _g("mall_find_entrance_guidance_candidate").get("guidance_type") == "find_entrance_hint"
            and by_case.get("mall_find_entrance_guidance_candidate", {}).get("guidance_ok") is True
        ),
        "subway_enter_station_cautious_guidance_ok": (
            _g("subway_enter_station_guidance_candidate").get("guidance_type")
            == "cautious_indoor_guidance_candidate"
        ),
        "stadium_concert_ticket_gate_guidance_ok": (
            _g("stadium_concert_ticket_gate_guidance_candidate").get("field_label") == "演唱会现场"
            and _g("stadium_concert_ticket_gate_guidance_candidate").get("underlying_map_place_ref")
            == "stadium_stub"
        ),
        "plaza_market_crowd_safety_downgrade_ok": (
            _g("plaza_market_crowd_safety_guidance_candidate").get("guidance_action_strength")
            == "observe_wait_request_evidence"
        ),
        "gps_slam_conflict_guidance_blocked": (
            _g("gps_slam_conflict_guidance_blocked").get("guidance_status")
            == "blocked_or_needs_more_evidence"
            and _a("gps_slam_conflict_guidance_blocked").get("safety_status") == "blocked"
        ),
        "home_return_stable_guidance_candidate_ok": (
            _g("home_return_stable_guidance_candidate").get("guidance_type")
            == "coarse_route_with_local_check"
            and _a("home_return_stable_guidance_candidate").get("safety_status") == "pending"
        ),
        "task_route_hint_not_action": all(
            (by_case.get(ref) or {}).get("guidance_candidate", {}).get("is_navigation_runtime") is not True
            for ref in POSITIVE_CASE_REFS
        ),
        "guidance_candidate_not_runtime_navigation": all(
            (by_case.get(ref) or {}).get("guidance_candidate", {}).get("is_navigation_runtime") is not True
            for ref in POSITIVE_CASE_REFS
        ),
        "speech_gate_candidate_not_tts": all(
            (by_case.get(ref) or {}).get("speech_gate_candidate", {}).get("trigger_tts") is not True
            for ref in POSITIVE_CASE_REFS
        ),
        "action_safety_candidate_required": all(
            bool((by_case.get(ref) or {}).get("action_safety_candidate")) for ref in POSITIVE_CASE_REFS
        ),
        "candidate_only_enforced": all(
            (by_case.get(ref) or {}).get("guidance_candidate", {}).get("candidate_only") is True
            for ref in POSITIVE_CASE_REFS
        ),
        "direct_action_allowed": False,
        "direct_speech_allowed": False,
        "direct_fact_write_allowed": False,
        "real_navigation_started": False,
        "live_sensor_connected": False,
        "task_manager_entrypoint_locked": TASK_MANAGER_ENTRYPOINT,
        "guidance_entrypoint_locked": GUIDANCE_ENTRYPOINT,
        "speech_gate_entrypoint_locked": SPEECH_GATE_ENTRYPOINT,
        "action_safety_entrypoint_locked": ACTION_SAFETY_ENTRYPOINT,
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
        "mall_find_entrance_guidance_candidate_ok": review_checkpoints[
            "mall_find_entrance_guidance_candidate_ok"
        ],
        "subway_enter_station_cautious_guidance_ok": review_checkpoints[
            "subway_enter_station_cautious_guidance_ok"
        ],
        "stadium_concert_ticket_gate_guidance_ok": review_checkpoints[
            "stadium_concert_ticket_gate_guidance_ok"
        ],
        "plaza_market_crowd_safety_downgrade_ok": review_checkpoints[
            "plaza_market_crowd_safety_downgrade_ok"
        ],
        "gps_slam_conflict_guidance_blocked": review_checkpoints["gps_slam_conflict_guidance_blocked"],
        "home_return_stable_guidance_candidate_ok": review_checkpoints[
            "home_return_stable_guidance_candidate_ok"
        ],
        "task_route_hint_not_action": review_checkpoints["task_route_hint_not_action"],
        "guidance_candidate_not_runtime_navigation": review_checkpoints[
            "guidance_candidate_not_runtime_navigation"
        ],
        "speech_gate_candidate_not_tts": review_checkpoints["speech_gate_candidate_not_tts"],
        "action_safety_candidate_required": review_checkpoints["action_safety_candidate_required"],
        "candidate_only_enforced": review_checkpoints["candidate_only_enforced"],
        "direct_action_allowed_false": review_checkpoints["direct_action_allowed"] is False,
        "direct_speech_allowed_false": review_checkpoints["direct_speech_allowed"] is False,
        "direct_fact_write_allowed_false": review_checkpoints["direct_fact_write_allowed"] is False,
        "real_navigation_started_false": review_checkpoints["real_navigation_started"] is False,
        "live_sensor_connected_false": review_checkpoints["live_sensor_connected"] is False,
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
        "step": "Task to Guidance Safety Gate Dry-Run Run + Review",
        "lifecycle_variant": "compressed_task_to_guidance_safety_gate_dryrun",
        "dryrun_principle_zh": DRYRUN_PRINCIPLE_ZH,
        "model_binding": {
            "task_manager_entrypoint": TASK_MANAGER_ENTRYPOINT,
            "guidance_entrypoint": GUIDANCE_ENTRYPOINT,
            "speech_gate_entrypoint": SPEECH_GATE_ENTRYPOINT,
            "action_safety_entrypoint": ACTION_SAFETY_ENTRYPOINT,
            "field_to_task_dryrun_ref": FIELD_TO_TASK_DRYRUN_REF,
            "field_synthesis_dryrun_ref": FIELD_SYNTHESIS_DRYRUN_REF,
            "task_manager_ref": TASK_MANAGER_REF,
            "basic_navigation_guidance_loop_ref": BASIC_NAVIGATION_GUIDANCE_LOOP_REF,
            "interface_layer_protocol_ref": INTERFACE_LAYER_PROTOCOL_REF,
            "candidate_only": True,
        },
        "pipeline": [
            "TaskContextCandidate / TaskEvidenceNeedCandidate / TaskRouteHintCandidate / TaskRiskCandidate",
            "GuidanceEvidenceRequestCandidate",
            "GuidanceCandidate",
            "SpeechGateCandidate",
            "ActionSafetyCandidate",
            "GuidanceSafetyDryRunDecision",
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
            "task_to_guidance_safety_gate_status": "go" if review_ok else "blocked",
            "recommended_next_step": (
                "Total closure: Field build → Task candidate → Guidance/Safety candidate chain"
            ),
        },
        "output_root": str(out_root),
        "output_file": str(out_path),
        "blocker_count": blocker_count,
        "failed_checks": failed_checks,
        "final_decision": FINAL_DECISION_DRYRUN_GO if review_ok else FINAL_DECISION_DRYRUN_BLOCKED,
    }

    if write_file:
        write_json_file(out_path, result)

    return result


def main() -> int:
    result = run_and_review_task_to_guidance_safety_gate_dryrun_v1()
    checkpoints = result["review_checkpoints"]
    print(
        json.dumps(
            {
                "output_file": result.get("output_file"),
                "positive_pass_count": checkpoints["positive_pass_count"],
                "invalid_expected_reject_count": checkpoints["invalid_expected_reject_count"],
                "gps_slam_conflict_guidance_blocked": checkpoints["gps_slam_conflict_guidance_blocked"],
                "action_safety_candidate_required": checkpoints["action_safety_candidate_required"],
                "blocker_count": result["blocker_count"],
                "final_decision": result["final_decision"],
            },
            ensure_ascii=False,
        )
    )
    return 0 if result["final_decision"] == FINAL_DECISION_DRYRUN_GO else 1


if __name__ == "__main__":
    raise SystemExit(main())
