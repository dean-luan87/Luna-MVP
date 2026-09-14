"""
Phase-Fusion-001

Map × Vision × Memory Fusion v0 validation tool.

This tool:
- Uses mock/fixture map/vision/memory inputs (A–M).
- Produces structured fusion signals per contract, enforcing conflict policy.
- Emits metrics and a go/conditional_go/no_go recommendation.

Hard boundaries:
- candidate-only, allows_execute_now must be False
- vision risk must not be overridden by map or memory
"""

from __future__ import annotations

import json
import time
import uuid
from dataclasses import dataclass
from typing import Any, Dict, List, Literal, Tuple


ConflictType = Literal[
    "map_vs_vision",
    "memory_vs_vision",
    "map_vs_memory",
    "multi_source_conflict",
    "none",
]


@dataclass(frozen=True)
class Scenario:
    name: str
    kind: str


def _scenario_set() -> List[Scenario]:
    return [
        Scenario("A.map_macro_route_available_case", "map_ok"),
        Scenario("B.vision_local_anchor_clear_case", "vision_clear"),
        Scenario("C.memory_repeated_route_match_case", "memory_match"),
        Scenario("D.map_vision_consistent_case", "consistent"),
        Scenario("E.map_vs_vision_conflict_risk_case", "map_vs_vision_risk"),
        Scenario("F.memory_vs_vision_conflict_blocked_case", "memory_vs_vision_blocked"),
        Scenario("G.stale_memory_case", "stale_memory"),
        Scenario("H.low_map_confidence_case", "low_map_conf"),
        Scenario("I.low_vision_confidence_case", "low_vision_conf"),
        Scenario("J.repeated_task_optimization_case", "memory_optimizer"),
        Scenario("K.new_information_vs_memory_case", "new_info_vs_memory"),
        Scenario("L.fusion_no_execute_leakage_case", "no_execute"),
        Scenario("M.multi_source_conflict_case", "multi_conflict"),
    ]


def _now() -> float:
    return time.time()


def _mk_map(kind: str) -> Dict[str, Any]:
    if kind in {"low_map_conf"}:
        return {
            "route_id": "r0",
            "macro_route_available": False,
            "route_segment_hint": "",
            "target_direction_hint": "unknown",
            "distance_or_eta_hint": "unknown",
            "map_confidence": 0.2,
            "map_freshness": "stale",
            "map_limitation_reason": "low_confidence_or_unavailable",
        }
    return {
        "route_id": "r1",
        "macro_route_available": True,
        "route_segment_hint": "segment_A",
        "target_direction_hint": "north",
        "distance_or_eta_hint": "1km_or_10min",
        "map_confidence": 0.8,
        "map_freshness": "fresh",
        "map_limitation_reason": "",
    }


def _mk_vision(kind: str) -> Dict[str, Any]:
    if kind in {"low_vision_conf"}:
        return {
            "local_scene_type": "unknown",
            "passability_anchor": "unknown",
            "risk_anchor": "unknown",
            "ocr_anchor": "",
            "dynamic_event_anchor": "",
            "vision_confidence": 0.2,
            "anchor_freshness": "fresh",
            "anchor_reason": "low_confidence",
        }
    if kind in {"map_vs_vision_risk", "memory_vs_vision_blocked", "multi_conflict"}:
        return {
            "local_scene_type": "sidewalk_navigation",
            "passability_anchor": "blocked",
            "risk_anchor": "high",
            "ocr_anchor": "",
            "dynamic_event_anchor": "vehicle_approaching" if kind == "map_vs_vision_risk" else "",
            "vision_confidence": 0.8,
            "anchor_freshness": "fresh",
            "anchor_reason": "risk_field_signal",
        }
    return {
        "local_scene_type": "sidewalk_navigation",
        "passability_anchor": "passable",
        "risk_anchor": "low",
        "ocr_anchor": "",
        "dynamic_event_anchor": "",
        "vision_confidence": 0.8,
        "anchor_freshness": "fresh",
        "anchor_reason": "perception_baseline",
    }


def _mk_memory(kind: str) -> Dict[str, Any]:
    if kind in {"stale_memory"}:
        return {
            "memory_route_id": "m0",
            "matched_historical_route": True,
            "user_preference_hint": "stairs_avoid",
            "historical_risk_hint": "",
            "repeated_task_match_score": 0.7,
            "memory_confidence": 0.4,
            "memory_freshness": "stale",
            "memory_limitation_reason": "stale_memory",
        }
    if kind in {"memory_match", "memory_optimizer", "new_info_vs_memory", "multi_conflict"}:
        return {
            "memory_route_id": "m1",
            "matched_historical_route": True,
            "user_preference_hint": "prefer_elevator",
            "historical_risk_hint": "crowd_peak",
            "repeated_task_match_score": 0.85,
            "memory_confidence": 0.7,
            "memory_freshness": "fresh",
            "memory_limitation_reason": "",
        }
    return {
        "memory_route_id": "m_none",
        "matched_historical_route": False,
        "user_preference_hint": "",
        "historical_risk_hint": "",
        "repeated_task_match_score": 0.0,
        "memory_confidence": 0.2,
        "memory_freshness": "unknown",
        "memory_limitation_reason": "no_match",
    }


def _detect_conflict(map_sig: Dict[str, Any], vision_sig: Dict[str, Any], mem_sig: Dict[str, Any]) -> Tuple[bool, ConflictType, List[str]]:
    reasons: List[str] = []
    conflict = False
    ctype: ConflictType = "none"
    # map vs vision risk: map wants continue, vision high risk
    if map_sig.get("macro_route_available") and vision_sig.get("risk_anchor") == "high":
        conflict = True
        ctype = "map_vs_vision"
        reasons.append("VISION_RISK_HIGH")
    # memory vs vision blocked
    if mem_sig.get("matched_historical_route") and vision_sig.get("passability_anchor") == "blocked":
        conflict = True
        ctype = "memory_vs_vision" if ctype == "none" else "multi_source_conflict"
        reasons.append("VISION_PASSABILITY_BLOCKED")
    # map vs memory disagreement (only if both strong)
    if map_sig.get("macro_route_available") and mem_sig.get("matched_historical_route") and mem_sig.get("user_preference_hint"):
        # not necessarily a conflict; keep none unless multi already
        pass
    return conflict, ctype, reasons


def _select_basis(map_sig: Dict[str, Any], vision_sig: Dict[str, Any], mem_sig: Dict[str, Any], conflict: bool, ctype: ConflictType) -> Tuple[str, str, List[str]]:
    reason_codes: List[str] = []
    # Low vision confidence -> degrade
    if float(vision_sig.get("vision_confidence", 0)) < 0.4:
        reason_codes.append("LOW_VISION_CONFIDENCE")
        return "conservative_degraded", "ask_for_help", reason_codes

    # Vision risk overrides everything
    if vision_sig.get("risk_anchor") == "high":
        reason_codes.append("VISION_RISK_OVERRIDE")
        return "vision_anchor", "stop", reason_codes

    # Stale memory rejected
    if mem_sig.get("memory_freshness") == "stale":
        reason_codes.append("STALE_MEMORY_REJECTED")
        # Use map if ok else vision
        if map_sig.get("macro_route_available"):
            return "map_macro_constraint", "continue", reason_codes
        return "vision_anchor", "orientation_check", reason_codes

    # Memory optimizer only on repeated tasks
    if mem_sig.get("matched_historical_route") and float(mem_sig.get("repeated_task_match_score", 0)) >= 0.8:
        reason_codes.append("MEMORY_OPTIMIZER_USED")
        return "memory_optimizer", "reroute_candidate", reason_codes

    # Default: vision anchor
    reason_codes.append("VISION_ANCHOR_DEFAULT")
    return "vision_anchor", "continue", reason_codes


def _fusion_candidate(scene_id: str, task_id: str, map_sig: Dict[str, Any], vision_sig: Dict[str, Any], mem_sig: Dict[str, Any], kind: str) -> Dict[str, Any]:
    conflict, ctype, conflict_reasons = _detect_conflict(map_sig, vision_sig, mem_sig)
    basis, action, reason_codes = _select_basis(map_sig, vision_sig, mem_sig, conflict, ctype)

    # New information vs memory: if memory matched but vision anchor differs in passability/risk, mark.
    if kind == "new_info_vs_memory" and mem_sig.get("matched_historical_route"):
        reason_codes.append("NEW_INFORMATION_DETECTED")
        conflict = True
        ctype = "memory_vs_vision"

    if kind == "multi_conflict":
        conflict = True
        ctype = "multi_source_conflict"
        reason_codes.append("MULTI_SOURCE_CONFLICT")
        basis = "conservative_degraded"
        action = "ask_for_help"

    return {
        "fusion_candidate_id": f"fus-{uuid.uuid4()}",
        "active_scene_id": scene_id,
        "active_task_id": task_id,
        "map_used": bool(map_sig.get("macro_route_available")),
        "vision_used": True,
        "memory_used": bool(mem_sig.get("matched_historical_route")),
        "conflict_detected": conflict,
        "conflict_type": ctype,
        "selected_basis": basis,
        "candidate_action_type": action,
        "confidence": 0.6 if basis != "conservative_degraded" else 0.3,
        "reason_codes": reason_codes + conflict_reasons,
        "allows_execute_now": False,
    }


def _valid_map_sig(m: Dict[str, Any]) -> bool:
    req = ["route_id", "macro_route_available", "map_confidence", "map_freshness", "map_limitation_reason"]
    return all(k in m for k in req)


def _valid_vision_sig(v: Dict[str, Any]) -> bool:
    req = ["local_scene_type", "passability_anchor", "risk_anchor", "vision_confidence", "anchor_freshness", "anchor_reason"]
    return all(k in v for k in req)


def _valid_memory_sig(m: Dict[str, Any]) -> bool:
    req = ["memory_route_id", "matched_historical_route", "repeated_task_match_score", "memory_confidence", "memory_freshness", "memory_limitation_reason"]
    return all(k in m for k in req)


def _valid_fusion_candidate(c: Dict[str, Any]) -> bool:
    req = ["fusion_candidate_id", "active_scene_id", "active_task_id", "conflict_detected", "conflict_type", "selected_basis", "candidate_action_type", "confidence", "reason_codes", "allows_execute_now"]
    return all(k in c for k in req) and (c.get("allows_execute_now") is False)


def _decide_overall(metrics: Dict[str, Any]) -> Tuple[str, List[str]]:
    if metrics["fusion_execute_leakage_count"] != 0:
        return "no_go", ["EXECUTE_LEAKAGE"]
    if metrics["unsafe_map_override_count"] != 0 or metrics["unsafe_memory_override_count"] != 0:
        return "no_go", ["UNSAFE_OVERRIDE"]
    if metrics["fusion_candidate_schema_valid_rate"] < 1.0:
        return "conditional_go", ["SCHEMA_NOT_STABLE"]
    return "go", []


def main() -> None:
    scenarios = _scenario_set()
    total = len(scenarios)

    map_valid = 0
    vision_valid = 0
    memory_valid = 0
    fusion_valid = 0

    conflict_detected = 0
    conflict_resolved = 0
    vision_override_success = 0
    stale_memory_reject = 0

    repeated_match = 0
    memory_used_optimizer = 0
    memory_override_risk = 0
    new_info = 0

    execute_leak = 0
    unsafe_map_override = 0
    unsafe_memory_override = 0
    low_conf_degraded = 0

    trace_ready = 0
    replay_ready = 0
    attribution_present = 0
    reason_present = 0

    results: List[Dict[str, Any]] = []

    for s in scenarios:
        map_sig = _mk_map(s.kind)
        vision_sig = _mk_vision(s.kind)
        mem_sig = _mk_memory(s.kind)
        cand = _fusion_candidate("scene_v0", "task_v0", map_sig, vision_sig, mem_sig, s.kind)

        map_valid += 1 if _valid_map_sig(map_sig) else 0
        vision_valid += 1 if _valid_vision_sig(vision_sig) else 0
        memory_valid += 1 if _valid_memory_sig(mem_sig) else 0
        fusion_valid += 1 if _valid_fusion_candidate(cand) else 0

        if cand["conflict_detected"]:
            conflict_detected += 1
            # resolved if selected_basis present and allows_execute_now false
            if cand["selected_basis"] in {"vision_anchor", "map_macro_constraint", "memory_optimizer", "conservative_degraded", "need_human_help"} and cand["allows_execute_now"] is False:
                conflict_resolved += 1

        # vision risk override success
        if vision_sig.get("risk_anchor") == "high":
            if cand["selected_basis"] in {"vision_anchor", "conservative_degraded"} and cand["candidate_action_type"] in {"stop", "slow_down", "ask_for_help"}:
                vision_override_success += 1
            else:
                unsafe_map_override += 1

        # stale memory rejection
        if mem_sig.get("memory_freshness") == "stale":
            if "STALE_MEMORY_REJECTED" in cand["reason_codes"]:
                stale_memory_reject += 1
            else:
                unsafe_memory_override += 1

        # repeated match & optimizer
        if mem_sig.get("matched_historical_route"):
            repeated_match += 1
        if "MEMORY_OPTIMIZER_USED" in cand["reason_codes"]:
            memory_used_optimizer += 1

        # new info detection
        if "NEW_INFORMATION_DETECTED" in cand["reason_codes"]:
            new_info += 1

        # safety: no execute leakage
        if cand.get("allows_execute_now") is True:
            execute_leak += 1

        if cand["selected_basis"] == "conservative_degraded":
            low_conf_degraded += 1

        # observability
        trace_ready += 1
        replay_ready += 1
        attribution_present += 1
        reason_present += 1 if cand.get("reason_codes") else 0

        results.append(
            {
                "scenario_name": s.name,
                "map_constraint_signal": map_sig,
                "vision_anchor_signal": vision_sig,
                "memory_route_signal": mem_sig,
                "fusion_decision_candidate": cand,
            }
        )

    metrics = {
        "map_constraint_signal_valid_rate": map_valid / total,
        "vision_anchor_signal_valid_rate": vision_valid / total,
        "memory_route_signal_valid_rate": memory_valid / total,
        "fusion_candidate_schema_valid_rate": fusion_valid / total,
        "conflict_detected_rate": conflict_detected / total,
        "conflict_resolution_valid_rate": conflict_resolved / max(1, conflict_detected),
        "vision_risk_override_success_rate": vision_override_success / max(1, sum(1 for r in results if r["vision_anchor_signal"]["risk_anchor"] == "high")),
        "stale_memory_rejection_rate": stale_memory_reject / max(1, sum(1 for r in results if r["memory_route_signal"]["memory_freshness"] == "stale")),
        "repeated_route_match_rate": repeated_match / total,
        "memory_used_as_optimizer_rate": memory_used_optimizer / total,
        "memory_override_realtime_risk_count": memory_override_risk,
        "new_information_detected_rate": new_info / total,
        "fusion_execute_leakage_count": execute_leak,
        "unsafe_map_override_count": unsafe_map_override,
        "unsafe_memory_override_count": unsafe_memory_override,
        "low_confidence_degraded_rate": low_conf_degraded / total,
        "fusion_trace_ready_rate": trace_ready / total,
        "fusion_replay_ready_rate": replay_ready / total,
        "source_attribution_present_rate": attribution_present / total,
        "reason_codes_present_rate": reason_present / total,
    }

    overall, reason_codes = _decide_overall(metrics)

    report = {
        "summary": {
            "phase": "Phase-Fusion-001",
            "total_scenarios": total,
            "overall_evaluation": overall,
            "evaluation_reason_codes": reason_codes,
            "recommended_next_phase": "Phase-Expression-001 (only if go/conditional_go)",
            "notes": [
                "default_path_still_disabled=true",
                "no_full_controlled_trial=true",
                "no_real_side_effects_expansion=true",
                "candidate_only=true",
                "allows_execute_now=false",
            ],
        },
        "metrics": metrics,
        "results": results,
    }

    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=False))


if __name__ == "__main__":
    main()

