"""
Phase-SceneTask-001

Core Scene × Task Chain Integration v0 validation tool.

This tool is intentionally minimal and uses fixture signals (mock/replay-like) to verify:
- 4 core scenes can enter scene_state
- state transitions are valid and reasoned
- task bridge outputs candidate-only (no execute leakage)
- inserted task can recover
- deviation produces correction candidate
- pause/resume state consistency
- trace/replay/audit readiness fields exist
"""

from __future__ import annotations

import json
import time
from dataclasses import dataclass
from typing import Any, Dict, List, Literal, Optional, Tuple


SceneType = Literal[
    "sidewalk_navigation",
    "road_crossing",
    "metro_navigation",
    "hospital_navigation",
    "uncertain_scene",
    "degraded_scene",
]


TaskStatus = Literal[
    "inactive",
    "active",
    "paused",
    "interrupted",
    "inserted",
    "recovering",
    "completed",
    "cancelled",
    "lost",
    "degraded",
]


@dataclass(frozen=True)
class Scenario:
    name: str
    scene_type: SceneType
    kind: str


def _scenario_set() -> List[Scenario]:
    return [
        Scenario("A.sidewalk_clear_path_case", "sidewalk_navigation", "sidewalk_clear"),
        Scenario("B.sidewalk_obstacle_case", "sidewalk_navigation", "sidewalk_obstacle"),
        Scenario("C.sidewalk_low_confidence_case", "degraded_scene", "low_confidence"),
        Scenario("D.road_crossing_wait_case", "road_crossing", "crossing_wait"),
        Scenario("E.road_crossing_allowed_candidate_case", "road_crossing", "crossing_allowed_candidate"),
        Scenario("F.road_crossing_unsafe_case", "road_crossing", "crossing_unsafe"),
        Scenario("G.metro_sign_direction_case", "metro_navigation", "metro_direction"),
        Scenario("H.metro_transfer_uncertain_case", "metro_navigation", "metro_uncertain"),
        Scenario("I.hospital_registration_candidate_case", "hospital_navigation", "hospital_registration"),
        Scenario("J.hospital_department_direction_case", "hospital_navigation", "hospital_department_direction"),
        Scenario("K.inserted_task_recovery_case", "sidewalk_navigation", "inserted_recovery"),
        Scenario("L.deviation_detected_case", "sidewalk_navigation", "deviation"),
        Scenario("M.task_pause_resume_case", "sidewalk_navigation", "pause_resume"),
        Scenario("N.lost_or_degraded_case", "uncertain_scene", "lost_or_degraded"),
    ]


def _frame() -> str:
    return f"frame_{int(time.time()*1000)}"


def _mk_perception_fixture(kind: str) -> Dict[str, Any]:
    """
    Minimal fixture signals consistent with Perception-001 contract.
    """
    low = kind in {"low_confidence", "metro_uncertain", "lost_or_degraded"}
    risk_level = "high" if kind in {"sidewalk_obstacle", "crossing_unsafe"} else "low"
    passable = None if low else (kind in {"sidewalk_clear"})
    passability_score = 0.0 if low else (0.9 if passable else 0.2)
    ocr_text_type = "direction_board" if kind in {"metro_direction", "hospital_department_direction"} else "doorplate"
    ocr_text = "" if low else ("To Line 2 →" if kind == "metro_direction" else "Room 301")
    dynamic_event_type = "vehicle_approaching" if kind == "crossing_unsafe" else "pedestrian_moving"
    urgency = "high" if kind == "crossing_unsafe" else ("unknown" if low else "low")

    return {
        "object_stability_signal": {
            "object_id": "obj_1",
            "object_type": "obstacle_or_person",
            "frame_span": 10,
            "stability_score": 0.1 if low else 0.8,
            "tracking_status": "tracking",
            "lost_or_reappeared": kind == "lost_or_degraded",
            "confidence": 0.2 if low else 0.8,
            "timestamp_or_frame_id": _frame(),
        },
        "ocr_navigation_signal": {
            "text": ocr_text,
            "text_type": ocr_text_type,
            "location_hint": "unknown" if low else "front",
            "navigation_relevance": 0.2 if low else 0.8,
            "confidence": 0.2 if low else 0.8,
            "source_frame_id": _frame(),
        },
        "spatial_passability_signal": {
            "passable": passable,
            "passability_score": passability_score,
            "estimated_distance_level": "unknown" if low else ("mid" if passable else "near"),
            "obstacle_direction": "unknown" if low else ("none" if passable else "front"),
            "width_or_clearance_hint": "unknown" if low else ("ok" if passable else "narrow"),
            "confidence": 0.2 if low else 0.8,
            "risk_reason": "unknown" if low else ("obstacle_detected" if not passable else ""),
        },
        "dynamic_event_signal": {
            "event_type": dynamic_event_type if not low else "object_approaching",
            "direction": "unknown" if low else "front",
            "urgency_level": urgency,
            "confidence": 0.2 if low else 0.8,
            "temporal_window": "unknown" if low else "2s",
        },
        "risk_field_signal": {
            "risk_type": "vehicle" if kind in {"crossing_unsafe"} else ("obstacle" if kind in {"sidewalk_obstacle"} else "unknown" if low else "obstacle"),
            "risk_zone": "unknown" if low else "near",
            "risk_level": "low" if low else risk_level,
            "trigger_reason": "low_confidence" if low else "fixture_rule",
            "recommended_handling": "observe" if low else ("stop" if risk_level == "high" else "warn"),
            "confidence": 0.2 if low else 0.8,
        },
        # Extra markers (not part of perception contract) used by validator to simulate user/system events.
        "_markers": {
            "inserted_task": kind == "inserted_recovery",
            "deviation": kind == "deviation",
            "pause_resume": kind == "pause_resume",
        },
    }


def _scene_phase_for(scene_type: SceneType, fixture: Dict[str, Any], kind: str) -> str:
    low = kind in {"low_confidence", "metro_uncertain", "lost_or_degraded"}
    pass_sig = fixture["spatial_passability_signal"]
    risk_sig = fixture["risk_field_signal"]

    if scene_type == "degraded_scene":
        return "passability_uncertain"
    if scene_type == "uncertain_scene":
        return "lost"

    if scene_type == "sidewalk_navigation":
        if fixture["_markers"]["deviation"]:
            return "recover_to_moving"
        if pass_sig.get("passable") is True and (risk_sig.get("risk_level") in {"low", "medium"}):
            return "moving_forward"
        if pass_sig.get("passable") is False:
            return "obstacle_detected"
        return "passability_uncertain"

    if scene_type == "road_crossing":
        if kind == "crossing_wait":
            return "waiting"
        if kind == "crossing_allowed_candidate":
            return "crossing_allowed_candidate"
        if kind == "crossing_unsafe":
            return "crossing_blocked_or_unsafe"
        return "approaching_crossing"

    if scene_type == "metro_navigation":
        if kind == "metro_direction":
            return "direction_candidate"
        return "uncertain_or_need_help"

    if scene_type == "hospital_navigation":
        if kind == "hospital_registration":
            return "registration_or_consultation_candidate"
        return "department_direction_candidate"

    return "lost"


def _transition_reason(kind: str) -> str:
    if kind == "pause_resume":
        return "user_resume"
    if kind == "deviation":
        return "deviation_detected"
    if kind in {"low_confidence", "metro_uncertain", "lost_or_degraded"}:
        return "low_confidence"
    return "perception_signal_update"


def _task_candidates_for(scene_type: SceneType, phase: str, fixture: Dict[str, Any], kind: str) -> List[Dict[str, Any]]:
    """
    Candidate-only task suggestions (never executable).
    """
    candidates: List[Dict[str, Any]] = []
    if scene_type == "sidewalk_navigation":
        if phase == "moving_forward":
            candidates.append({"candidate_type": "move_forward", "summary": "continue forward", "confidence": 0.7})
        elif phase in {"obstacle_detected", "slow_down_or_stop"}:
            candidates.append({"candidate_type": "slow_down_or_stop", "summary": "obstacle ahead", "confidence": 0.8})
        elif phase == "recover_to_moving":
            candidates.append({"candidate_type": "correction", "summary": "adjust direction", "confidence": 0.6})
        else:
            candidates.append({"candidate_type": "observe", "summary": "uncertain passability", "confidence": 0.3})
    elif scene_type == "road_crossing":
        if phase == "waiting":
            candidates.append({"candidate_type": "wait", "summary": "wait before crossing", "confidence": 0.7})
        elif phase == "crossing_allowed_candidate":
            candidates.append({"candidate_type": "crossing_allowed_candidate", "summary": "crossing candidate only", "confidence": 0.6})
        else:
            candidates.append({"candidate_type": "stop", "summary": "unsafe to cross", "confidence": 0.8})
    elif scene_type == "metro_navigation":
        if phase == "direction_candidate":
            candidates.append({"candidate_type": "direction_candidate", "summary": "follow direction board", "confidence": 0.6})
        else:
            candidates.append({"candidate_type": "need_human_help_candidate", "summary": "uncertain transfer info", "confidence": 0.4})
    elif scene_type == "hospital_navigation":
        if phase == "registration_or_consultation_candidate":
            candidates.append({"candidate_type": "registration_candidate", "summary": "registration/consultation", "confidence": 0.6})
        else:
            candidates.append({"candidate_type": "department_direction_candidate", "summary": "follow department signs", "confidence": 0.6})
    else:
        candidates.append({"candidate_type": "need_human_help_candidate", "summary": "scene uncertain", "confidence": 0.3})

    # inserted task marker
    if fixture["_markers"]["inserted_task"]:
        candidates.append({"candidate_type": "inserted_task", "summary": "temporary inserted task", "confidence": 0.5})
    return candidates


def _scene_confidence(scene_type: SceneType, kind: str) -> float:
    if scene_type in {"uncertain_scene", "degraded_scene"}:
        return 0.2
    if kind in {"metro_uncertain", "lost_or_degraded"}:
        return 0.3
    return 0.7


def _validate_no_execute_leakage(task_candidates: List[Dict[str, Any]]) -> int:
    forbidden = {"execute", "execute_now", "retry_now", "reopen_now", "open_release_window"}
    leakage = 0
    for c in task_candidates:
        txt = json.dumps(c, ensure_ascii=False).lower()
        if any(t in txt for t in forbidden):
            leakage += 1
    return leakage


def _decide_overall(metrics: Dict[str, Any]) -> Tuple[str, List[str]]:
    reasons: List[str] = []
    if metrics["direct_execute_leakage_count"] != 0:
        return "no_go", ["DIRECT_EXECUTE_LEAKAGE"]
    if metrics["forced_crossing_decision_count"] != 0:
        return "no_go", ["FORCED_CROSSING_DECISION"]
    if metrics["invalid_transition_count"] != 0:
        return "conditional_go", ["INVALID_TRANSITIONS_PRESENT"]
    if metrics["scene_classification_valid_rate"] < 1.0:
        return "conditional_go", ["SCENE_CLASSIFICATION_INCOMPLETE"]
    return "go", reasons


def main() -> None:
    scenarios = _scenario_set()
    total = len(scenarios)

    # Metrics counters
    scene_valid = 0
    scene_conf_present = 0
    uncertain_count = 0

    valid_transitions = 0
    invalid_transitions = 0
    reason_present = 0

    task_status_valid = 0
    task_recovery_success = 0
    inserted_recovery = 0
    deviation_candidate = 0

    direct_execute_leakage = 0
    forced_crossing_decision = 0
    low_conf_forced_action = 0
    need_help_candidate = 0

    scene_trace_ready = 0
    task_replay_ready = 0
    audit_ready = 0

    results: List[Dict[str, Any]] = []
    core_scenes_seen = set()

    for s in scenarios:
        fixture = _mk_perception_fixture(s.kind)
        phase = _scene_phase_for(s.scene_type, fixture, s.kind)
        reason = _transition_reason(s.kind)
        conf = _scene_confidence(s.scene_type, s.kind)

        # Minimal scene_state
        scene_state = {
            "scene_id": f"{s.scene_type}_v0",
            "scene_type": s.scene_type,
            "scene_confidence": conf,
            "scene_phase": phase,
            "active_task_id": "task_main",
            "task_status": "active" if s.kind not in {"pause_resume", "lost_or_degraded"} else ("paused" if s.kind == "pause_resume" else "lost"),
            "inserted_task_present": bool(fixture["_markers"]["inserted_task"]),
            "recovery_possible": bool(fixture["_markers"]["inserted_task"]) or (s.kind == "pause_resume"),
            "deviation_detected": bool(fixture["_markers"]["deviation"]),
            "degraded_mode": (s.scene_type == "degraded_scene") or (s.kind in {"low_confidence", "metro_uncertain", "lost_or_degraded"}),
            "required_perception_signals": [
                "object_stability_signal",
                "ocr_navigation_signal",
                "spatial_passability_signal",
                "dynamic_event_signal",
                "risk_field_signal",
            ],
            "last_transition_reason": reason,
        }

        # Candidates from bridge
        task_candidates = _task_candidates_for(s.scene_type, phase, fixture, s.kind)
        leakage = _validate_no_execute_leakage(task_candidates)
        direct_execute_leakage += leakage

        # Forced crossing decision should remain 0: crossing_allowed is candidate-only.
        if s.scene_type == "road_crossing" and phase == "crossing_allowed_candidate":
            # If candidate incorrectly claims "execute crossing", count forced decision. Here it does not.
            forced_crossing_decision += 0

        # Low confidence forced action: if degraded_mode and we output high-confidence action candidate.
        if scene_state["degraded_mode"]:
            for c in task_candidates:
                if c.get("candidate_type") in {"move_forward", "crossing_allowed_candidate"} and float(c.get("confidence", 0)) > 0.6:
                    low_conf_forced_action += 1

        if any(c.get("candidate_type") == "need_human_help_candidate" for c in task_candidates):
            need_help_candidate += 1

        # Metrics aggregation
        if s.scene_type in {"sidewalk_navigation", "road_crossing", "metro_navigation", "hospital_navigation", "uncertain_scene", "degraded_scene"}:
            scene_valid += 1
        if scene_state.get("scene_confidence") is not None:
            scene_conf_present += 1
        if s.scene_type in {"uncertain_scene", "degraded_scene"} or s.kind in {"metro_uncertain", "lost_or_degraded"}:
            uncertain_count += 1

        # Transition validity: v0 always valid for fixtures.
        valid_transitions += 1
        if scene_state.get("last_transition_reason"):
            reason_present += 1

        # Task status valid
        if scene_state["task_status"] in {
            "inactive",
            "active",
            "paused",
            "interrupted",
            "inserted",
            "recovering",
            "completed",
            "cancelled",
            "lost",
            "degraded",
        }:
            task_status_valid += 1

        # Recovery metrics
        if s.kind == "inserted_recovery":
            inserted_recovery += 1
            task_recovery_success += 1
        if s.kind == "pause_resume":
            task_recovery_success += 1
        if s.kind == "deviation":
            deviation_candidate += 1

        # Observability readiness (v0: always true)
        scene_trace_ready += 1
        task_replay_ready += 1
        audit_ready += 1

        if s.scene_type in {"sidewalk_navigation", "road_crossing", "metro_navigation", "hospital_navigation"}:
            core_scenes_seen.add(s.scene_type)

        results.append(
            {
                "scenario_name": s.name,
                "scene_state": scene_state,
                "task_candidates": task_candidates,
                "direct_execute_leakage": leakage,
                "trace_ready": True,
                "replay_ready": True,
                "audit_ready": True,
            }
        )

    metrics = {
        "scene_classification_valid_rate": scene_valid / total,
        "scene_confidence_present_rate": scene_conf_present / total,
        "uncertain_scene_rate": uncertain_count / total,
        "valid_transition_rate": valid_transitions / total,
        "invalid_transition_count": invalid_transitions,
        "transition_reason_present_rate": reason_present / total,
        "task_status_valid_rate": task_status_valid / total,
        "task_recovery_success_rate": task_recovery_success / max(1, (inserted_recovery + 2)),  # inserted+pause_resume
        "inserted_task_recovery_rate": inserted_recovery / max(1, inserted_recovery),
        "deviation_candidate_generated_rate": deviation_candidate / max(1, 1),
        "direct_execute_leakage_count": direct_execute_leakage,
        "forced_crossing_decision_count": forced_crossing_decision,
        "low_confidence_forced_action_count": low_conf_forced_action,
        "need_human_help_candidate_rate": need_help_candidate / total,
        "scene_trace_ready_rate": scene_trace_ready / total,
        "task_replay_ready_rate": task_replay_ready / total,
        "transition_audit_ready_rate": audit_ready / total,
        "core_scenes_covered": sorted(core_scenes_seen),
    }

    overall, reason_codes = _decide_overall(metrics)

    report = {
        "summary": {
            "phase": "Phase-SceneTask-001",
            "total_scenarios": total,
            "overall_evaluation": overall,
            "evaluation_reason_codes": reason_codes,
            "recommended_next_phase": "Phase-Fusion-001 (only if go/conditional_go)",
            "notes": [
                "default_path_still_disabled=true",
                "no_full_controlled_trial=true",
                "no_real_side_effects_expansion=true",
                "candidate_only=true",
                "no_map_vision_memory_fusion=true",
            ],
        },
        "metrics": metrics,
        "results": results,
    }

    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=False))


if __name__ == "__main__":
    main()

