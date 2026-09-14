#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, Mapping


def _find_ws_root() -> Path:
    here = Path(__file__).resolve()
    for parent in here.parents:
        if (parent / "capabilities" / "midplatform").is_dir():
            return parent
    return here.parents[3]


WS_ROOT = _find_ws_root()
if str(WS_ROOT) not in sys.path:
    sys.path.insert(0, str(WS_ROOT))

from capabilities.midplatform.navigation_manager.module.navigation_manager_module_api_v1 import (
    run_navigation_manager_module_v1,
)
from capabilities.midplatform.navigation_manager.module.navigation_manager_module_types_v1 import (
    BOUNDARY_FALSE_FIELDS,
)


def _base_payload(case_id: str) -> Dict[str, Any]:
    return {
        "navigation_request_id": f"nav_req_{case_id}",
        "task_id": f"task_{case_id}",
        "navigation_mode": "route_following",
        "destination_candidate": {
            "destination_ref": f"dst_{case_id}",
            "arrived": False,
        },
        "route_candidate": {
            "route_ref": f"route_{case_id}",
            "route_status": "candidate_ready",
        },
        "route_memory_ref": "",
        "current_position_candidate": {"position_ref": f"pos_{case_id}"},
        "route_progress_candidate": {"progress_ratio": 0.42},
        "observation_candidate": {"observation_ref": f"obs_{case_id}"},
        "vision_evidence_refs": [f"vision_ev_{case_id}"],
        "ocr_evidence_refs": [f"ocr_ev_{case_id}"],
        "map_evidence_candidate": {
            "map_ref": f"map_{case_id}",
            "map_visual_conflict": False,
        },
        "landmark_candidates": ["landmark_storefront"],
        "crossing_candidates": [],
        "traffic_light_candidates": [],
        "obstacle_candidates": [],
        "user_correction_candidate": {"deviation_detected": False},
        "temporal_snapshot": {"temporal_snapshot_ref": f"ts_{case_id}"},
        "permission_context": {"request_rejected": False},
        "version_snapshot": {"navigation_manager": "v1"},
        "trace_context": {"case_id": case_id},
    }


def _boundary_preserved(result: Mapping[str, Any]) -> bool:
    return all(result.get(k) is False for k in BOUNDARY_FALSE_FIELDS)


def run_integration() -> Dict[str, Any]:
    scenarios: Dict[str, Dict[str, Any]] = {}

    c1 = _base_payload("route_following_ready")
    c1["navigation_mode"] = "route_following"
    scenarios["route_following_ready"] = c1

    c2 = _base_payload("route_memory_available")
    c2["navigation_mode"] = "route_memory"
    c2["route_candidate"] = {}
    c2["route_memory_ref"] = "memory_route_alpha"
    scenarios["route_memory_available"] = c2

    c3 = _base_payload("route_unavailable")
    c3["route_candidate"] = {}
    c3["route_memory_ref"] = ""
    scenarios["route_unavailable"] = c3

    c4 = _base_payload("navigation_active")
    c4["route_progress_candidate"] = {"progress_ratio": 0.55}
    scenarios["navigation_active"] = c4

    c5 = _base_payload("navigation_pause")
    c5["navigation_mode"] = "pause_navigation"
    scenarios["navigation_pause"] = c5

    c6 = _base_payload("navigation_resume")
    c6["navigation_mode"] = "resume_navigation"
    scenarios["navigation_resume"] = c6

    c7 = _base_payload("normal_route_progress")
    c7["route_progress_candidate"] = {"progress_ratio": 0.74}
    scenarios["normal_route_progress"] = c7

    c8 = _base_payload("deviation_detected")
    c8["navigation_mode"] = "deviation_check"
    c8["user_correction_candidate"] = {"deviation_detected": True}
    scenarios["deviation_detected"] = c8

    c9 = _base_payload("reroute_candidate")
    c9["navigation_mode"] = "deviation_check"
    c9["user_correction_candidate"] = {"deviation_detected": True}
    scenarios["reroute_candidate"] = c9

    c10 = _base_payload("landmark_detected")
    c10["navigation_mode"] = "find_landmark"
    c10["landmark_candidates"] = ["target_bank", "blue_sign"]
    scenarios["landmark_detected"] = c10

    c11 = _base_payload("crossing_attention")
    c11["navigation_mode"] = "crossing_support"
    c11["crossing_candidates"] = ["zebra_crossing_ahead"]
    scenarios["crossing_attention"] = c11

    c12 = _base_payload("traffic_light_attention")
    c12["navigation_mode"] = "crossing_support"
    c12["traffic_light_candidates"] = ["red_light"]
    scenarios["traffic_light_attention"] = c12

    c13 = _base_payload("obstacle_attention")
    c13["navigation_mode"] = "obstacle_support"
    c13["obstacle_candidates"] = ["temporary_barrier"]
    scenarios["obstacle_attention"] = c13

    c14 = _base_payload("dynamic_collision_risk")
    c14["navigation_mode"] = "obstacle_support"
    c14["obstacle_candidates"] = ["dynamic_collision_risk"]
    scenarios["dynamic_collision_risk"] = c14

    c15 = _base_payload("insufficient_visual_evidence")
    c15["navigation_mode"] = "baseline_safety"
    c15["vision_evidence_refs"] = []
    c15["ocr_evidence_refs"] = []
    scenarios["insufficient_visual_evidence"] = c15

    c16 = _base_payload("conflicting_map_visual_evidence")
    c16["map_evidence_candidate"] = {
        "map_ref": "map_conflict",
        "map_visual_conflict": True,
    }
    scenarios["conflicting_map_visual_evidence"] = c16

    c17 = _base_payload("user_route_correction_candidate")
    c17["user_correction_candidate"] = {
        "deviation_detected": True,
        "correction_hint": "turn_right",
    }
    scenarios["user_route_correction_candidate"] = c17

    c18 = _base_payload("arrival_candidate")
    c18["navigation_mode"] = "arrival_check"
    c18["destination_candidate"] = {"destination_ref": "dst_arrival", "arrived": True}
    c18["route_progress_candidate"] = {"progress_ratio": 1.0}
    scenarios["arrival_candidate"] = c18

    c19 = _base_payload("invalid_request")
    c19["navigation_mode"] = "unknown_mode"
    scenarios["invalid_request"] = c19

    c20 = _base_payload("deterministic_replay")
    scenarios["deterministic_replay"] = c20

    expected_status = {
        "route_following_ready": "navigation_active",
        "route_memory_available": "route_ready",
        "route_unavailable": "route_unavailable",
        "navigation_active": "navigation_active",
        "navigation_pause": "navigation_paused",
        "navigation_resume": "navigation_active",
        "normal_route_progress": "navigation_active",
        "deviation_detected": "reroute_candidate_ready",
        "reroute_candidate": "reroute_candidate_ready",
        "landmark_detected": "navigation_active",
        "crossing_attention": "crossing_attention_required",
        "traffic_light_attention": "crossing_attention_required",
        "obstacle_attention": "obstacle_attention_required",
        "dynamic_collision_risk": "obstacle_attention_required",
        "insufficient_visual_evidence": "insufficient_evidence",
        "conflicting_map_visual_evidence": "conflicted",
        "user_route_correction_candidate": "reroute_candidate_ready",
        "arrival_candidate": "arrival_candidate_ready",
        "invalid_request": "invalid_input",
        "deterministic_replay": "navigation_active",
    }

    guidance_expected = {
        "route_following_ready",
        "navigation_active",
        "navigation_resume",
        "normal_route_progress",
        "deviation_detected",
        "reroute_candidate",
        "landmark_detected",
        "crossing_attention",
        "traffic_light_attention",
        "obstacle_attention",
        "dynamic_collision_risk",
        "user_route_correction_candidate",
        "arrival_candidate",
        "deterministic_replay",
    }

    deviation_expected = {
        "deviation_detected",
        "reroute_candidate",
        "user_route_correction_candidate",
    }
    crossing_expected = {"crossing_attention", "traffic_light_attention"}
    obstacle_expected = {"obstacle_attention", "dynamic_collision_risk"}
    arrival_expected = {"arrival_candidate"}

    rows = []
    failed_cases = []
    route_state_present_when_expected = True
    guidance_candidate_present_when_expected = True
    deviation_candidate_present_when_expected = True
    crossing_assessment_present_when_expected = True
    obstacle_assessment_present_when_expected = True
    arrival_candidate_present_when_expected = True
    task_handoff_present_when_expected = True
    speech_handoff_present_when_expected = True
    diagnostics_present_all = True
    trace_present_all = True
    replay_present_all = True
    deterministic_replay = True
    boundary_preserved = True
    unhandled_exceptions = 0

    for case_id, payload in scenarios.items():
        try:
            result = run_navigation_manager_module_v1(payload)
        except Exception:  # noqa: BLE001
            result = {"module_status": "internal_error"}
            unhandled_exceptions += 1

        status = str(result.get("module_status") or "")
        route_state_present = isinstance(result.get("route_state"), dict) and bool(
            result.get("route_state")
        )
        if case_id != "invalid_request" and not route_state_present:
            route_state_present_when_expected = False

        if case_id in guidance_expected and not isinstance(
            result.get("guidance_candidate"), dict
        ):
            guidance_candidate_present_when_expected = False

        deviation = result.get("deviation_assessment") or {}
        if case_id in deviation_expected and not bool(
            deviation.get("deviation_detected", False)
        ):
            deviation_candidate_present_when_expected = False

        crossing = result.get("crossing_assessment") or {}
        if case_id in crossing_expected and not bool(
            crossing.get("attention_required", False)
        ):
            crossing_assessment_present_when_expected = False

        obstacle = result.get("obstacle_risk_assessment") or {}
        if case_id in obstacle_expected and not bool(
            obstacle.get("attention_required", False)
        ):
            obstacle_assessment_present_when_expected = False

        arrival = result.get("arrival_candidate") or {}
        if case_id in arrival_expected and not bool(arrival.get("arrived", False)):
            arrival_candidate_present_when_expected = False

        if case_id != "invalid_request" and not isinstance(
            result.get("task_handoff_candidate"), dict
        ):
            task_handoff_present_when_expected = False
        if case_id != "invalid_request" and not isinstance(
            result.get("speech_handoff_candidate"), dict
        ):
            speech_handoff_present_when_expected = False

        if not isinstance(result.get("diagnostics"), dict):
            diagnostics_present_all = False
        if not str(result.get("trace_ref") or ""):
            trace_present_all = False
        if not str(result.get("replay_key") or ""):
            replay_present_all = False
        if not _boundary_preserved(result):
            boundary_preserved = False

        case_pass = status == expected_status[case_id]
        case_pass = case_pass and route_state_present
        case_pass = case_pass and isinstance(result.get("diagnostics"), dict)
        case_pass = (
            case_pass
            and bool(result.get("trace_ref"))
            and bool(result.get("replay_key"))
        )
        case_pass = case_pass and _boundary_preserved(result)

        if case_id == "deterministic_replay":
            rerun = run_navigation_manager_module_v1(payload)
            deterministic_replay = deterministic_replay and (
                result.get("module_status") == rerun.get("module_status")
                and result.get("trace_ref") == rerun.get("trace_ref")
                and result.get("replay_key") == rerun.get("replay_key")
            )
            case_pass = case_pass and deterministic_replay

        if not case_pass:
            failed_cases.append(case_id)

        rows.append(
            {
                "case_id": case_id,
                "expected_status": expected_status[case_id],
                "module_status": status,
                "passed": case_pass,
                "trace_ref": result.get("trace_ref"),
                "replay_key": result.get("replay_key"),
            }
        )

    total_cases = len(scenarios)
    passed_cases = total_cases - len(failed_cases)

    return {
        "phase": "Phase-Luna-Navigation-Manager-Functional-Module-Consolidation-And-Integration-v1-001",
        "total_cases": total_cases,
        "passed_cases": passed_cases,
        "failed_cases": failed_cases,
        "route_state_present_when_expected": route_state_present_when_expected,
        "guidance_candidate_present_when_expected": guidance_candidate_present_when_expected,
        "deviation_candidate_present_when_expected": deviation_candidate_present_when_expected,
        "crossing_assessment_present_when_expected": crossing_assessment_present_when_expected,
        "obstacle_assessment_present_when_expected": obstacle_assessment_present_when_expected,
        "arrival_candidate_present_when_expected": arrival_candidate_present_when_expected,
        "task_handoff_present_when_expected": task_handoff_present_when_expected,
        "speech_handoff_present_when_expected": speech_handoff_present_when_expected,
        "diagnostics_present_all": diagnostics_present_all,
        "trace_present_all": trace_present_all,
        "replay_present_all": replay_present_all,
        "deterministic_replay": deterministic_replay,
        "boundary_preserved": boundary_preserved,
        "unhandled_exceptions": unhandled_exceptions,
        "rows": rows,
        "integration_pass": passed_cases == total_cases
        and failed_cases == []
        and route_state_present_when_expected
        and guidance_candidate_present_when_expected
        and deviation_candidate_present_when_expected
        and crossing_assessment_present_when_expected
        and obstacle_assessment_present_when_expected
        and arrival_candidate_present_when_expected
        and task_handoff_present_when_expected
        and speech_handoff_present_when_expected
        and diagnostics_present_all
        and trace_present_all
        and replay_present_all
        and deterministic_replay
        and boundary_preserved
        and unhandled_exceptions == 0,
    }


def main() -> int:
    report = run_integration()
    output_root = Path(
        "_tmp_eval_out/navigation_manager_module_integration_v1_smoke_v0"
    ).resolve()
    output_root.mkdir(parents=True, exist_ok=True)
    output_path = output_root / "navigation_manager_module_integration_v1.json"
    output_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "integration_pass": report["integration_pass"],
                "total_cases": report["total_cases"],
                "passed_cases": report["passed_cases"],
                "failed_cases": report["failed_cases"],
                "route_state_present_when_expected": report[
                    "route_state_present_when_expected"
                ],
                "guidance_candidate_present_when_expected": report[
                    "guidance_candidate_present_when_expected"
                ],
                "deviation_candidate_present_when_expected": report[
                    "deviation_candidate_present_when_expected"
                ],
                "crossing_assessment_present_when_expected": report[
                    "crossing_assessment_present_when_expected"
                ],
                "obstacle_assessment_present_when_expected": report[
                    "obstacle_assessment_present_when_expected"
                ],
                "arrival_candidate_present_when_expected": report[
                    "arrival_candidate_present_when_expected"
                ],
                "task_handoff_present_when_expected": report[
                    "task_handoff_present_when_expected"
                ],
                "speech_handoff_present_when_expected": report[
                    "speech_handoff_present_when_expected"
                ],
                "diagnostics_present_all": report["diagnostics_present_all"],
                "trace_present_all": report["trace_present_all"],
                "replay_present_all": report["replay_present_all"],
                "deterministic_replay": report["deterministic_replay"],
                "boundary_preserved": report["boundary_preserved"],
                "unhandled_exceptions": report["unhandled_exceptions"],
                "output": str(output_path),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0 if report["integration_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
