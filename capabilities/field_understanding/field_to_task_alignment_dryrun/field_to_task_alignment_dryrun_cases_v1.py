# -*- coding: utf-8 -*-
"""Field to Task Alignment Dry-Run — cases + alignment v1."""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple

from capabilities.field_understanding.field_synthesis_map_place_event_overlay_dryrun.field_synthesis_map_place_event_overlay_dryrun_cases_v1 import (
    build_positive_input_bundles_v1 as build_field_synthesis_input_bundles_v1,
    synthesize_field_decision_v1,
)
from capabilities.field_understanding.field_to_task_alignment_dryrun.field_to_task_alignment_dryrun_types_v1 import (
    FIELD_SYNTHESIS_ENTRYPOINT,
    NEGATIVE_CASE_REFS,
    POSITIVE_CASE_REFS,
    SOURCE_CHAIN,
    TASK_MANAGER_ENTRYPOINT,
)

_CHAIN = (SOURCE_CHAIN, "field_to_task_cases_v1")

_FIELD_SYNTHESIS_CASE_MAP = {
    "mall_find_entrance_task": "mall_stable_map_place_with_slam",
    "subway_station_enter_station_task": "subway_station_indoor_gps_degraded",
    "stadium_concert_ticket_check_task": "stadium_concert_event_overlay",
    "plaza_temporary_market_find_stall_task": "plaza_temporary_market_realtime_overlay",
    "gps_slam_conflict_delay_navigation_task": "gps_slam_map_place_conflict",
}

_USER_TASKS = {
    "mall_find_entrance_task": "找商场入口",
    "subway_station_enter_station_task": "进站",
    "stadium_concert_ticket_check_task": "找检票口",
    "plaza_temporary_market_find_stall_task": "找摊位 / 进入集市",
    "gps_slam_conflict_delay_navigation_task": "去公司",
    "home_return_task_stable_field": "回家",
}

_EVIDENCE_NEEDS = {
    "mall_find_entrance_task": (
        "entrance_sign",
        "doorway",
        "path_accessibility",
    ),
    "subway_station_enter_station_task": (
        "station_entrance",
        "gate",
        "sign",
        "crowd",
    ),
    "stadium_concert_ticket_check_task": (
        "ticket_gate",
        "entrance_zone",
        "crowd_flow",
        "ocr_sign",
    ),
    "plaza_temporary_market_find_stall_task": (
        "stall_sign",
        "pedestrian_flow",
        "walkable_area",
    ),
    "gps_slam_conflict_delay_navigation_task": (
        "conflict_resolution",
        "additional_spatial_evidence",
    ),
    "home_return_task_stable_field": (
        "coarse_map_route",
        "local_spatial_check",
    ),
}


def _bundle_chain(case_ref: str) -> List[str]:
    return list(_CHAIN + (case_ref,))


def _build_home_field_input_bundle() -> Dict[str, Any]:
    from capabilities.field_understanding.field_synthesis_map_place_event_overlay_dryrun.field_synthesis_map_place_event_overlay_dryrun_cases_v1 import (
        _gps_stub,
        _map_place,
        _spatial_binding,
    )

    return {
        "bundle_ref": "bundle_home_return",
        "case_ref": "home_return_task_stable_field",
        "user_goal": "回家",
        "map_place_ref": _map_place(
            "home",
            place_ref="home_map_place_stub",
            poi_name="家",
            category="residential",
        ),
        "gps_gnss_stub": _gps_stub("home", confidence=0.86),
        "spatial_evidence_binding": _spatial_binding(
            "home",
            coordinate_scope="mixed",
            fusion_ref="spatial_odometry_fusion_outdoor_gps_primary_slam_support",
            flags={"pose": True, "motion": True, "anchor": True},
        ),
        "realtime_context_overlay": {},
        "event_overlay": {},
        "evidence_refs": ["map_place_home", "gps_home", "spatial_home"],
        "source_chain": _bundle_chain("home_return_task_stable_field"),
        "field_synthesis_entrypoint": FIELD_SYNTHESIS_ENTRYPOINT,
        "candidate_only": True,
    }


def build_field_trace_for_case(case_ref: str) -> Dict[str, Any]:
    if case_ref == "home_return_task_stable_field":
        bundle = _build_home_field_input_bundle()
    else:
        synthesis_ref = _FIELD_SYNTHESIS_CASE_MAP[case_ref]
        bundle = build_field_synthesis_input_bundles_v1()[synthesis_ref]
    return synthesize_field_decision_v1(bundle)


def build_positive_input_bundles_v1() -> Dict[str, Dict[str, Any]]:
    bundles: Dict[str, Dict[str, Any]] = {}
    for case_ref in POSITIVE_CASE_REFS:
        field_trace = build_field_trace_for_case(case_ref)
        bundles[case_ref] = {
            "bundle_ref": f"bundle_{case_ref}",
            "case_ref": case_ref,
            "user_task": _USER_TASKS[case_ref],
            "field_trace": field_trace,
            "source_chain": _bundle_chain(case_ref),
            "field_synthesis_entrypoint": FIELD_SYNTHESIS_ENTRYPOINT,
            "task_manager_entrypoint": TASK_MANAGER_ENTRYPOINT,
            "candidate_only": True,
        }
    return bundles


def build_negative_input_bundles_v1() -> Dict[str, Dict[str, Any]]:
    base = build_positive_input_bundles_v1()["mall_find_entrance_task"]
    conflict_base = build_positive_input_bundles_v1()["gps_slam_conflict_delay_navigation_task"]
    stadium_base = build_positive_input_bundles_v1()["stadium_concert_ticket_check_task"]

    missing_label = dict(base)
    missing_label_trace = dict(base["field_trace"])
    missing_label_trace["field_interaction_label_candidate"] = {}
    missing_label["field_trace"] = missing_label_trace
    missing_label.update(
        {
            "bundle_ref": "bundle_invalid_missing_label",
            "case_ref": "invalid_missing_field_interaction_label",
        }
    )

    ignore_conflict = dict(conflict_base)
    ignore_conflict_trace = dict(conflict_base["field_trace"])
    ignore_conflict_trace["field_conflict_candidate"] = {}
    ignore_conflict["field_trace"] = ignore_conflict_trace
    ignore_conflict.update(
        {
            "bundle_ref": "bundle_invalid_ignore_conflict",
            "case_ref": "invalid_field_conflict_ignored",
            "ignore_field_conflict": True,
        }
    )

    rewrite_map_place = dict(stadium_base)
    rewrite_trace = dict(stadium_base["field_trace"])
    task_ctx_override = {
        "rewrite_map_place_in_task_context": True,
        "forced_underlying_map_place_ref": "rewritten_stadium_stub",
    }
    rewrite_trace["task_context_override"] = task_ctx_override
    rewrite_map_place["field_trace"] = rewrite_trace
    rewrite_map_place.update(
        {
            "bundle_ref": "bundle_invalid_rewrite_map_place",
            "case_ref": "invalid_event_overlay_rewrites_map_place_in_task",
        }
    )

    direct_action = dict(base)
    direct_action.update(
        {
            "bundle_ref": "bundle_invalid_direct_action",
            "case_ref": "invalid_task_route_hint_direct_action",
            "force_route_hint_direct_action": True,
        }
    )

    return {
        "invalid_missing_field_interaction_label": missing_label,
        "invalid_field_conflict_ignored": ignore_conflict,
        "invalid_event_overlay_rewrites_map_place_in_task": rewrite_map_place,
        "invalid_task_route_hint_direct_action": direct_action,
    }


def validate_field_to_task_bundle(bundle: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues: List[str] = []
    field_trace = bundle.get("field_trace") or {}

    if bundle.get("candidate_only") is not True:
        issues.append("bundle_not_candidate_only")
    if not bundle.get("source_chain"):
        issues.append("source_chain_required")

    if not field_trace.get("synthesis_ok"):
        issues.append("field_synthesis_not_ok")

    label = field_trace.get("field_interaction_label_candidate") or {}
    if not label:
        issues.append("field_interaction_label_missing")

    conflict = field_trace.get("field_conflict_candidate") or {}
    if bundle.get("case_ref") == "gps_slam_conflict_delay_navigation_task" and not conflict:
        if not bundle.get("ignore_field_conflict"):
            issues.append("field_conflict_missing_for_conflict_case")

    if bundle.get("ignore_field_conflict") is True and conflict:
        issues.append("field_conflict_must_not_be_ignored")

    override = field_trace.get("task_context_override") or {}
    if override.get("rewrite_map_place_in_task_context") is True:
        fc = field_trace.get("field_candidate") or {}
        expected = fc.get("underlying_map_place_ref")
        forced = override.get("forced_underlying_map_place_ref")
        if forced and forced != expected:
            issues.append("event_overlay_rewrites_map_place_in_task_context")

    if bundle.get("force_route_hint_direct_action") is True:
        issues.append("task_route_hint_direct_action_forbidden")

    return len(issues) == 0, issues


def align_field_to_task_v1(bundle: Dict[str, Any]) -> Dict[str, Any]:
    ok, issues = validate_field_to_task_bundle(bundle)
    case_ref = str(bundle.get("case_ref", "unknown"))
    trace_ref = f"field_to_task_trace_{case_ref}"
    trace_chain = list(bundle.get("source_chain") or []) + [trace_ref]

    field_trace = bundle.get("field_trace") or {}
    if not ok:
        return {
            "trace_ref": trace_ref,
            "case_ref": case_ref,
            "alignment_ok": False,
            "task_context_candidate": {},
            "task_evidence_need_candidate": {},
            "task_route_hint_candidate": {},
            "task_risk_candidate": {},
            "task_manager_decision": {},
            "alignment_issues": issues,
            "source_chain": trace_chain,
            "candidate_only": True,
        }

    fc = field_trace.get("field_candidate") or {}
    fs = field_trace.get("field_state_candidate") or {}
    fl = field_trace.get("field_interaction_label_candidate") or {}
    conflict = field_trace.get("field_conflict_candidate") or {}

    underlying_map_place_ref = fc.get("underlying_map_place_ref") or fl.get("underlying_map_place_ref")
    override = field_trace.get("task_context_override") or {}
    if override.get("rewrite_map_place_in_task_context") is True:
        underlying_map_place_ref = override.get("forced_underlying_map_place_ref", underlying_map_place_ref)

    field_candidate_refs = [
        ref
        for ref in (
            fc.get("candidate_ref"),
            fs.get("candidate_ref"),
            fl.get("candidate_ref"),
            (conflict or {}).get("candidate_ref"),
        )
        if ref
    ]

    has_conflict = bool(conflict)
    gps_weight = fc.get("gps_weight", "none")

    task_context = {
        "candidate_type": "TaskContextCandidate",
        "candidate_ref": f"task_context_{case_ref}",
        "task_context_id": f"task_ctx_{case_ref}",
        "field_label": fl.get("field_label"),
        "underlying_map_place_ref": underlying_map_place_ref,
        "user_task": bundle.get("user_task"),
        "field_state": fs.get("field_state"),
        "internal_field_state_ref": fl.get("internal_field_state_ref"),
        "gps_weight": gps_weight,
        "slam_local_weight": fc.get("slam_local_weight"),
        "field_candidate_refs": field_candidate_refs,
        "source_chain": trace_chain + ["task_context_candidate"],
        "task_manager_entrypoint": TASK_MANAGER_ENTRYPOINT,
        "candidate_only": True,
        "field_label_treated_as_fact": False,
    }

    evidence_kinds = list(_EVIDENCE_NEEDS.get(case_ref, ("spatial_evidence",)))
    task_evidence_need = {
        "candidate_type": "TaskEvidenceNeedCandidate",
        "candidate_ref": f"task_evidence_need_{case_ref}",
        "evidence_need_id": f"evidence_need_{case_ref}",
        "requested_evidence_kinds": evidence_kinds,
        "source_chain": trace_chain + ["task_evidence_need_candidate"],
        "task_manager_entrypoint": TASK_MANAGER_ENTRYPOINT,
        "candidate_only": True,
        "live_sensor_trigger_allowed": False,
    }

    if has_conflict:
        route_status = "blocked_or_needs_more_evidence"
        route_kind = "defer_until_conflict_resolved"
    elif case_ref == "home_return_task_stable_field":
        route_status = "candidate"
        route_kind = "coarse_map_route_plus_local_spatial_check"
    else:
        route_status = "candidate"
        route_kind = "local_spatial_route_hint"

    direct_action = bundle.get("force_route_hint_direct_action") is True
    task_route_hint = {
        "candidate_type": "TaskRouteHintCandidate",
        "candidate_ref": f"task_route_hint_{case_ref}",
        "route_hint_id": f"route_hint_{case_ref}",
        "hint_kind": route_kind,
        "status": route_status,
        "source_chain": trace_chain + ["task_route_hint_candidate"],
        "task_manager_entrypoint": TASK_MANAGER_ENTRYPOINT,
        "candidate_only": True,
        "direct_action_allowed": direct_action,
        "is_action": False,
    }

    risk_kinds: List[str] = []
    if case_ref == "subway_station_enter_station_task":
        risk_kinds.append("indoor_navigation_uncertainty")
    if case_ref == "plaza_temporary_market_find_stall_task":
        risk_kinds.extend(["crowd_density", "queue", "temporary_layout_uncertainty"])
    if has_conflict:
        risk_kinds.append("conflict_requires_resolution")

    task_risk = {
        "candidate_type": "TaskRiskCandidate",
        "candidate_ref": f"task_risk_{case_ref}",
        "risk_id": f"task_risk_{case_ref}",
        "risk_kinds": risk_kinds,
        "source_chain": trace_chain + ["task_risk_candidate"],
        "task_manager_entrypoint": TASK_MANAGER_ENTRYPOINT,
        "candidate_only": True,
        "direct_speech_allowed": False,
        "is_speech": False,
    }

    if bundle.get("ignore_field_conflict") is True:
        task_route_hint["status"] = "candidate"
        task_risk["risk_kinds"] = []

    alignment_ok = not direct_action
    if override.get("rewrite_map_place_in_task_context") and override.get("forced_underlying_map_place_ref") != fc.get(
        "underlying_map_place_ref"
    ):
        alignment_ok = False
        issues = ["event_overlay_rewrites_map_place_in_task_context"]
    else:
        issues = ["task_route_hint_direct_action_forbidden"] if direct_action else []

    task_manager_decision = {
        "decision_ref": f"task_manager_decision_{case_ref}",
        "task_manager_entrypoint": TASK_MANAGER_ENTRYPOINT,
        "admits_task_context": True,
        "admits_task_evidence_need": True,
        "admits_task_route_hint": task_route_hint["status"] != "blocked_or_needs_more_evidence"
        or has_conflict,
        "route_hint_blocked": task_route_hint["status"] == "blocked_or_needs_more_evidence",
        "real_navigation_started": False,
        "direct_action_allowed": False,
        "direct_speech_allowed": False,
        "direct_fact_write_allowed": False,
        "candidate_only": True,
        "source_chain": trace_chain + ["task_manager_decision"],
    }

    if bundle.get("ignore_field_conflict") is True:
        alignment_ok = False
        issues.append("field_conflict_ignored_proceeding_as_safe_forbidden")

    return {
        "trace_ref": trace_ref,
        "case_ref": case_ref,
        "alignment_ok": alignment_ok,
        "task_context_candidate": task_context,
        "task_evidence_need_candidate": task_evidence_need,
        "task_route_hint_candidate": task_route_hint,
        "task_risk_candidate": task_risk,
        "task_manager_decision": task_manager_decision,
        "alignment_issues": issues,
        "source_chain": trace_chain,
        "candidate_only": True,
    }


def evaluate_positive_case(trace: Dict[str, Any], case_ref: str) -> Tuple[bool, List[str]]:
    issues: List[str] = []
    if not trace.get("alignment_ok"):
        issues.append("alignment_failed")
        issues.extend(trace.get("alignment_issues") or [])

    ctx = trace.get("task_context_candidate") or {}
    evidence = trace.get("task_evidence_need_candidate") or {}
    route = trace.get("task_route_hint_candidate") or {}
    risk = trace.get("task_risk_candidate") or {}
    decision = trace.get("task_manager_decision") or {}

    if ctx.get("candidate_only") is not True:
        issues.append("task_context_not_candidate_only")
    if route.get("direct_action_allowed") is True:
        issues.append("route_hint_direct_action")
    if decision.get("real_navigation_started") is True:
        issues.append("real_navigation_started")

    if case_ref == "mall_find_entrance_task":
        if ctx.get("field_label") != "商场":
            issues.append(f"field_label_mismatch:{ctx.get('field_label')!r}")
        for kind in ("entrance_sign", "doorway", "path_accessibility"):
            if kind not in (evidence.get("requested_evidence_kinds") or []):
                issues.append(f"missing_evidence_need:{kind}")

    elif case_ref == "subway_station_enter_station_task":
        if ctx.get("field_label") != "地铁站":
            issues.append(f"field_label_mismatch:{ctx.get('field_label')!r}")
        if ctx.get("gps_weight") != "degraded":
            issues.append("gps_weight_not_degraded")
        if "indoor_navigation_uncertainty" not in (risk.get("risk_kinds") or []):
            issues.append("missing_indoor_navigation_uncertainty_risk")

    elif case_ref == "stadium_concert_ticket_check_task":
        if ctx.get("field_label") != "演唱会现场":
            issues.append(f"field_label_mismatch:{ctx.get('field_label')!r}")
        if ctx.get("underlying_map_place_ref") != "stadium_stub":
            issues.append("underlying_map_place_ref_mismatch")
        for kind in ("ticket_gate", "ocr_sign"):
            if kind not in (evidence.get("requested_evidence_kinds") or []):
                issues.append(f"missing_evidence_need:{kind}")

    elif case_ref == "plaza_temporary_market_find_stall_task":
        if ctx.get("field_label") != "临时集市":
            issues.append(f"field_label_mismatch:{ctx.get('field_label')!r}")
        for kind in ("crowd_density", "queue", "temporary_layout_uncertainty"):
            if kind not in (risk.get("risk_kinds") or []):
                issues.append(f"missing_risk:{kind}")

    elif case_ref == "gps_slam_conflict_delay_navigation_task":
        if route.get("status") != "blocked_or_needs_more_evidence":
            issues.append("route_hint_not_blocked")
        if "conflict_requires_resolution" not in (risk.get("risk_kinds") or []):
            issues.append("missing_conflict_risk")

    elif case_ref == "home_return_task_stable_field":
        if ctx.get("field_label") != "家":
            issues.append(f"field_label_mismatch:{ctx.get('field_label')!r}")
        if route.get("hint_kind") != "coarse_map_route_plus_local_spatial_check":
            issues.append("home_route_hint_kind_mismatch")

    if not ctx.get("internal_field_state_ref"):
        issues.append("field_interaction_label_not_separated")

    return len(issues) == 0, issues


def build_positive_cases_v1() -> Tuple[Dict[str, Any], ...]:
    bundles = build_positive_input_bundles_v1()
    return tuple(
        {
            "case_ref": case_ref,
            "case_kind": "positive",
            "user_task": bundles[case_ref]["user_task"],
            "input_bundle_ref": bundles[case_ref]["bundle_ref"],
            "expected_outcome": {"alignment_ok": True, "candidate_only": True},
            "input_bundle": bundles[case_ref],
        }
        for case_ref in POSITIVE_CASE_REFS
    )


def build_negative_cases_v1() -> Tuple[Dict[str, Any], ...]:
    bundles = build_negative_input_bundles_v1()
    return tuple(
        {
            "case_ref": case_ref,
            "case_kind": "negative",
            "input_bundle_ref": bundles[case_ref]["bundle_ref"],
            "expected_rejected": True,
            "input_bundle": bundles[case_ref],
        }
        for case_ref in NEGATIVE_CASE_REFS
    )
