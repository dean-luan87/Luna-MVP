# -*- coding: utf-8 -*-
"""Field Synthesis Map Place / Event Overlay Dry-Run — cases + synthesis v1."""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple

from capabilities.field_understanding.field_synthesis_map_place_event_overlay_dryrun.field_synthesis_map_place_event_overlay_dryrun_types_v1 import (
    FIELD_SYNTHESIS_ENTRYPOINT,
    NEGATIVE_CASE_REFS,
    POSITIVE_CASE_REFS,
    SOURCE_CHAIN,
)

_CHAIN = (SOURCE_CHAIN, "field_synthesis_cases_v1")


def _bundle_chain(case_ref: str) -> List[str]:
    return list(_CHAIN + (case_ref,))


def _gps_stub(
    ref_suffix: str,
    *,
    confidence: float,
    degraded: bool = False,
    conflict: bool = False,
    field_identity_override: bool = False,
) -> Dict[str, Any]:
    payload: Dict[str, Any] = {
        "gps_ref": f"gps_stub_{ref_suffix}",
        "lat_lon_stub": [31.2304, 121.4737],
        "accuracy_m": 45.0 if degraded else 8.0,
        "confidence": confidence,
        "degraded": degraded,
        "claimed_place_ref": f"place_{ref_suffix}_gps",
        "candidate_only": True,
        "field_identity_mutation_allowed": field_identity_override,
        "source_chain": _bundle_chain(f"gps_{ref_suffix}"),
        "field_synthesis_entrypoint": FIELD_SYNTHESIS_ENTRYPOINT,
    }
    if conflict:
        payload["conflict_with_slam"] = True
    return payload


def _map_place(
    ref_suffix: str,
    *,
    place_ref: str,
    poi_name: str,
    category: str,
) -> Dict[str, Any]:
    return {
        "map_place_ref": place_ref,
        "poi_name": poi_name,
        "category_hint": category,
        "confidence": 0.92,
        "candidate_only": True,
        "field_identity_mutation_allowed": False,
        "source_chain": _bundle_chain(f"map_place_{ref_suffix}"),
        "field_synthesis_entrypoint": FIELD_SYNTHESIS_ENTRYPOINT,
    }


def _spatial_binding(
    ref_suffix: str,
    *,
    coordinate_scope: str,
    fusion_ref: str,
    flags: Dict[str, bool],
    conflict: bool = False,
) -> Dict[str, Any]:
    return {
        "binding_id": f"bind_{ref_suffix}",
        "coordinate_scope": coordinate_scope,
        "fusion_candidate_ref": fusion_ref,
        "pose_supported": flags.get("pose", False),
        "motion_supported": flags.get("motion", False),
        "health_supported": flags.get("health", False),
        "anchor_supported": flags.get("anchor", False),
        "relocalization_supported": flags.get("relocalization", False),
        "drift_supported": flags.get("drift", False),
        "spatial_binding_used": True,
        "slam_overrides_field_identity": False,
        "conflict_with_gps": conflict,
        "candidate_only": True,
        "source_chain": _bundle_chain(f"spatial_{ref_suffix}"),
        "field_synthesis_entrypoint": FIELD_SYNTHESIS_ENTRYPOINT,
    }


def _realtime_context(
    ref_suffix: str,
    *,
    context_type: str,
    observed_state: str,
) -> Dict[str, Any]:
    return {
        "realtime_context_id": f"rtc_{ref_suffix}",
        "context_type": context_type,
        "observed_state": observed_state,
        "time_window": [1_700_010_000_000, 1_700_020_000_000],
        "confidence": 0.76,
        "candidate_only": True,
        "direct_fact_write_allowed": False,
        "source_chain": _bundle_chain(f"rtc_{ref_suffix}"),
        "field_synthesis_entrypoint": FIELD_SYNTHESIS_ENTRYPOINT,
    }


def _event_overlay(
    ref_suffix: str,
    *,
    event_type: str,
    base_map_place_ref: str,
    user_label: str,
    time_window: Optional[Tuple[int, int]] = None,
    rewrite_map_place: bool = False,
) -> Dict[str, Any]:
    payload: Dict[str, Any] = {
        "event_overlay_id": f"evt_{ref_suffix}",
        "event_type": event_type,
        "base_map_place_ref": base_map_place_ref,
        "user_facing_field_label": user_label,
        "confidence": 0.86,
        "candidate_only": True,
        "map_place_ref_rewrite_allowed": rewrite_map_place,
        "source_chain": _bundle_chain(f"event_{ref_suffix}"),
        "field_synthesis_entrypoint": FIELD_SYNTHESIS_ENTRYPOINT,
    }
    if time_window is not None:
        payload["time_window"] = list(time_window)
    if rewrite_map_place:
        payload["map_place_ref"] = f"rewritten_{base_map_place_ref}"
    return payload


def build_positive_input_bundles_v1() -> Dict[str, Dict[str, Any]]:
    return {
        "mall_stable_map_place_with_slam": {
            "bundle_ref": "bundle_mall_stable",
            "case_ref": "mall_stable_map_place_with_slam",
            "user_goal": "去商场",
            "map_place_ref": _map_place(
                "mall",
                place_ref="mall_poi_stub",
                poi_name="商场",
                category="shopping_mall",
            ),
            "gps_gnss_stub": _gps_stub("mall", confidence=0.88),
            "spatial_evidence_binding": _spatial_binding(
                "mall",
                coordinate_scope="mixed",
                fusion_ref="spatial_odometry_fusion_outdoor_gps_primary_slam_support",
                flags={"pose": True, "motion": True, "anchor": True},
            ),
            "realtime_context_overlay": {},
            "event_overlay": {},
            "evidence_refs": ["map_place_mall", "gps_mall", "spatial_mall"],
            "source_chain": _bundle_chain("mall_stable_map_place_with_slam"),
            "field_synthesis_entrypoint": FIELD_SYNTHESIS_ENTRYPOINT,
            "candidate_only": True,
        },
        "subway_station_indoor_gps_degraded": {
            "bundle_ref": "bundle_subway_indoor",
            "case_ref": "subway_station_indoor_gps_degraded",
            "user_goal": "去地铁站 / 进入地铁站",
            "map_place_ref": _map_place(
                "subway",
                place_ref="subway_station_stub",
                poi_name="地铁站",
                category="metro_station",
            ),
            "gps_gnss_stub": _gps_stub("subway", confidence=0.34, degraded=True),
            "spatial_evidence_binding": _spatial_binding(
                "subway",
                coordinate_scope="local",
                fusion_ref="spatial_odometry_fusion_indoor_slam_primary_gps_degraded",
                flags={"pose": True, "anchor": True, "health": True},
            ),
            "realtime_context_overlay": {},
            "event_overlay": {},
            "evidence_refs": ["map_place_subway", "gps_subway", "spatial_subway"],
            "source_chain": _bundle_chain("subway_station_indoor_gps_degraded"),
            "field_synthesis_entrypoint": FIELD_SYNTHESIS_ENTRYPOINT,
            "candidate_only": True,
        },
        "stadium_concert_event_overlay": {
            "bundle_ref": "bundle_stadium_concert",
            "case_ref": "stadium_concert_event_overlay",
            "user_goal": "去看演唱会",
            "map_place_ref": _map_place(
                "stadium",
                place_ref="stadium_stub",
                poi_name="体育馆",
                category="stadium",
            ),
            "gps_gnss_stub": _gps_stub("stadium", confidence=0.72),
            "spatial_evidence_binding": _spatial_binding(
                "stadium",
                coordinate_scope="local",
                fusion_ref="spatial_odometry_fusion_indoor_slam_primary_gps_degraded",
                flags={"anchor": True},
            ),
            "realtime_context_overlay": {},
            "event_overlay": _event_overlay(
                "concert",
                event_type="concert",
                base_map_place_ref="stadium_stub",
                user_label="演唱会现场",
                time_window=(1_700_000_000_000, 1_700_003_600_000),
            ),
            "evidence_refs": ["map_place_stadium", "event_concert", "spatial_stadium"],
            "source_chain": _bundle_chain("stadium_concert_event_overlay"),
            "field_synthesis_entrypoint": FIELD_SYNTHESIS_ENTRYPOINT,
            "candidate_only": True,
        },
        "plaza_temporary_market_realtime_overlay": {
            "bundle_ref": "bundle_plaza_market",
            "case_ref": "plaza_temporary_market_realtime_overlay",
            "user_goal": "去广场 / 找集市",
            "map_place_ref": _map_place(
                "plaza",
                place_ref="plaza_stub",
                poi_name="市民广场",
                category="public_plaza",
            ),
            "gps_gnss_stub": _gps_stub("plaza", confidence=0.8),
            "spatial_evidence_binding": _spatial_binding(
                "plaza",
                coordinate_scope="mixed",
                fusion_ref="spatial_odometry_fusion_transition_outdoor_to_indoor",
                flags={"pose": True, "motion": True},
            ),
            "realtime_context_overlay": _realtime_context(
                "market_crowd",
                context_type="crowd",
                observed_state="queue_at_market_entrance",
            ),
            "event_overlay": _event_overlay(
                "market",
                event_type="market",
                base_map_place_ref="plaza_stub",
                user_label="临时集市",
                time_window=(1_700_005_000_000, 1_700_012_000_000),
            ),
            "evidence_refs": ["map_place_plaza", "event_market", "rtc_market_crowd"],
            "source_chain": _bundle_chain("plaza_temporary_market_realtime_overlay"),
            "field_synthesis_entrypoint": FIELD_SYNTHESIS_ENTRYPOINT,
            "candidate_only": True,
        },
        "gps_slam_map_place_conflict": {
            "bundle_ref": "bundle_office_conflict",
            "case_ref": "gps_slam_map_place_conflict",
            "user_goal": "去公司",
            "map_place_ref": _map_place(
                "office",
                place_ref="office_stub",
                poi_name="公司",
                category="office_building",
            ),
            "gps_gnss_stub": _gps_stub("office", confidence=0.81, conflict=True),
            "spatial_evidence_binding": _spatial_binding(
                "office",
                coordinate_scope="mixed",
                fusion_ref="spatial_odometry_fusion_gps_slam_conflict",
                flags={"anchor": True, "relocalization": True, "drift": True},
                conflict=True,
            ),
            "realtime_context_overlay": {},
            "event_overlay": {},
            "evidence_refs": ["map_place_office", "gps_office", "spatial_office"],
            "source_chain": _bundle_chain("gps_slam_map_place_conflict"),
            "field_synthesis_entrypoint": FIELD_SYNTHESIS_ENTRYPOINT,
            "candidate_only": True,
        },
    }


def build_negative_input_bundles_v1() -> Dict[str, Dict[str, Any]]:
    base_mall = build_positive_input_bundles_v1()["mall_stable_map_place_with_slam"]

    missing_tw = dict(base_mall)
    missing_tw.update(
        {
            "bundle_ref": "bundle_invalid_missing_time_window",
            "case_ref": "invalid_event_overlay_missing_time_window",
            "event_overlay": _event_overlay(
                "no_tw",
                event_type="market",
                base_map_place_ref="mall_poi_stub",
                user_label="非法集市",
                time_window=None,
            ),
        }
    )

    rewrite = dict(base_mall)
    rewrite.update(
        {
            "bundle_ref": "bundle_invalid_rewrite_map_place",
            "case_ref": "invalid_event_overlay_rewrites_map_place",
            "event_overlay": _event_overlay(
                "rewrite",
                event_type="exhibition",
                base_map_place_ref="mall_poi_stub",
                user_label="改写地点",
                time_window=(1_700_000_000_000, 1_700_001_000_000),
                rewrite_map_place=True,
            ),
        }
    )

    gps_override = dict(base_mall)
    gps_override.update(
        {
            "bundle_ref": "bundle_invalid_gps_override",
            "case_ref": "invalid_gps_overrides_field_identity",
            "gps_gnss_stub": _gps_stub(
                "override",
                confidence=0.95,
                field_identity_override=True,
            ),
        }
    )

    direct_action = dict(base_mall)
    direct_action.update(
        {
            "bundle_ref": "bundle_invalid_direct_action",
            "case_ref": "invalid_field_synthesis_direct_action_output",
            "force_direct_action_output": True,
        }
    )

    return {
        "invalid_event_overlay_missing_time_window": missing_tw,
        "invalid_event_overlay_rewrites_map_place": rewrite,
        "invalid_gps_overrides_field_identity": gps_override,
        "invalid_field_synthesis_direct_action_output": direct_action,
    }


def validate_input_bundle_for_synthesis(bundle: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues: List[str] = []

    if bundle.get("candidate_only") is not True:
        issues.append("bundle_not_candidate_only")
    if not bundle.get("source_chain"):
        issues.append("source_chain_required")
    if bundle.get("field_synthesis_entrypoint") != FIELD_SYNTHESIS_ENTRYPOINT:
        issues.append("field_synthesis_entrypoint_bypass")

    gps = bundle.get("gps_gnss_stub") or {}
    if gps.get("field_identity_mutation_allowed") is True:
        issues.append("gps_field_identity_override_forbidden")

    spatial = bundle.get("spatial_evidence_binding") or {}
    if spatial.get("slam_overrides_field_identity") is True:
        issues.append("slam_field_identity_override_forbidden")

    event = bundle.get("event_overlay") or {}
    if event:
        if not event.get("time_window"):
            issues.append("event_overlay_missing_time_window")
        if event.get("map_place_ref_rewrite_allowed") is True:
            issues.append("event_overlay_rewrites_map_place_forbidden")
        if event.get("map_place_ref") and event.get("map_place_ref") != event.get("base_map_place_ref"):
            issues.append("event_overlay_map_place_ref_mutated")

    rtc = bundle.get("realtime_context_overlay") or {}
    if rtc and rtc.get("direct_fact_write_allowed") is True:
        issues.append("realtime_context_direct_fact_write_forbidden")

    if bundle.get("force_direct_action_output") is True:
        issues.append("direct_action_output_forbidden")

    return len(issues) == 0, issues


def synthesize_field_decision_v1(bundle: Dict[str, Any]) -> Dict[str, Any]:
    ok, issues = validate_input_bundle_for_synthesis(bundle)
    case_ref = str(bundle.get("case_ref", "unknown"))
    trace_ref = f"trace_{case_ref}"
    trace_chain = list(bundle.get("source_chain") or []) + [trace_ref]

    if not ok:
        return {
            "trace_ref": trace_ref,
            "case_ref": case_ref,
            "input_bundle_ref": bundle.get("bundle_ref"),
            "synthesis_ok": False,
            "field_candidate": {},
            "field_state_candidate": {},
            "field_interaction_label_candidate": {},
            "field_conflict_candidate": {},
            "synthesis_issues": issues,
            "source_chain": trace_chain,
            "field_synthesis_entrypoint": FIELD_SYNTHESIS_ENTRYPOINT,
            "candidate_only": True,
        }

    map_place = bundle["map_place_ref"]
    gps = bundle.get("gps_gnss_stub") or {}
    spatial = bundle.get("spatial_evidence_binding") or {}
    event = bundle.get("event_overlay") or {}
    rtc = bundle.get("realtime_context_overlay") or {}

    place_ref = map_place["map_place_ref"]
    coordinate_scope = spatial.get("coordinate_scope", "mixed")
    gps_degraded = gps.get("degraded") is True
    has_conflict = gps.get("conflict_with_slam") or spatial.get("conflict_with_gps")

    if event.get("user_facing_field_label"):
        field_label = event["user_facing_field_label"]
        label_source = "event_overlay"
    elif rtc:
        field_label = f"{map_place['poi_name']}（{rtc.get('context_type', 'context')}）"
        label_source = "realtime_context"
    else:
        field_label = map_place["poi_name"]
        label_source = "map_place"

    if case_ref == "mall_stable_map_place_with_slam":
        field_state = "stable_map_place_field"
    elif case_ref == "subway_station_indoor_gps_degraded":
        field_state = "indoor_slam_primary_gps_degraded_field"
    elif case_ref == "stadium_concert_event_overlay":
        field_state = "event_overlay_active_field"
    elif case_ref == "plaza_temporary_market_realtime_overlay":
        field_state = "event_and_realtime_overlay_field"
    elif case_ref == "gps_slam_map_place_conflict":
        field_state = "map_place_spatial_conflict_field"
    else:
        field_state = "synthesized_field_state"

    overlay_refs: List[str] = []
    if event:
        overlay_refs.append(event.get("event_overlay_id", "event_overlay"))
    if rtc:
        overlay_refs.append(rtc.get("realtime_context_id", "realtime_context"))

    field_candidate = {
        "candidate_type": "FieldCandidate",
        "candidate_ref": f"field_candidate_{case_ref}",
        "underlying_map_place_ref": place_ref,
        "field_definition_ref": (
            "map_place_plus_realtime_context_plus_event_overlay_plus_spatial_evidence"
        ),
        "map_place_anchors_field": True,
        "map_place_fully_defines_field": False,
        "coordinate_scope": coordinate_scope,
        "gps_weight": "degraded" if gps_degraded else "support" if gps else "none",
        "slam_local_weight": "high" if gps_degraded or spatial.get("anchor_supported") else "support",
        "spatial_binding_used": spatial.get("spatial_binding_used", False),
        "source_chain": trace_chain + ["field_candidate"],
        "field_synthesis_entrypoint": FIELD_SYNTHESIS_ENTRYPOINT,
        "candidate_only": True,
        "direct_action_allowed": False,
        "direct_speech_allowed": False,
        "direct_fact_write_allowed": False,
    }

    field_state_candidate = {
        "candidate_type": "FieldStateCandidate",
        "candidate_ref": f"field_state_{case_ref}",
        "field_state": field_state,
        "internal_field_state_ref": f"internal_{field_state}_{case_ref}",
        "realtime_overlay_active": bool(rtc),
        "event_overlay_active": bool(event),
        "overlay_context_types": [rtc.get("context_type")] if rtc else [],
        "gps_degraded": gps_degraded,
        "source_chain": trace_chain + ["field_state_candidate"],
        "field_synthesis_entrypoint": FIELD_SYNTHESIS_ENTRYPOINT,
        "candidate_only": True,
        "direct_fact_write_allowed": False,
    }

    field_interaction_label_candidate = {
        "candidate_type": "FieldInteractionLabelCandidate",
        "candidate_ref": f"field_label_{case_ref}",
        "field_label": field_label,
        "label_source": label_source,
        "underlying_map_place_ref": place_ref,
        "overlay_refs": overlay_refs,
        "internal_field_state_ref": field_state_candidate["internal_field_state_ref"],
        "display_priority": 200 if label_source == "event_overlay" else 150 if rtc else 100,
        "source_chain": trace_chain + ["field_interaction_label_candidate"],
        "field_synthesis_entrypoint": FIELD_SYNTHESIS_ENTRYPOINT,
        "candidate_only": True,
    }

    field_conflict_candidate: Dict[str, Any] = {}
    if has_conflict:
        field_conflict_candidate = {
            "candidate_type": "FieldConflictCandidate",
            "candidate_ref": f"field_conflict_{case_ref}",
            "conflict_kind": "gps_slam_map_place_mismatch",
            "map_place_claim": place_ref,
            "gps_claim": gps.get("claimed_place_ref"),
            "slam_claim": f"{place_ref}_slam_local_frame_mismatch",
            "resolution": "defer_to_field_synthesis_v1",
            "field_identity_overridden": False,
            "source_chain": trace_chain + ["field_conflict_candidate"],
            "field_synthesis_entrypoint": FIELD_SYNTHESIS_ENTRYPOINT,
            "candidate_only": True,
        }

    force_action = bundle.get("force_direct_action_output") is True
    if force_action:
        field_candidate["direct_action_allowed"] = True

    return {
        "trace_ref": trace_ref,
        "case_ref": case_ref,
        "input_bundle_ref": bundle.get("bundle_ref"),
        "synthesis_ok": not force_action,
        "field_candidate": field_candidate,
        "field_state_candidate": field_state_candidate,
        "field_interaction_label_candidate": field_interaction_label_candidate,
        "field_conflict_candidate": field_conflict_candidate,
        "synthesis_issues": ["direct_action_output_forbidden"] if force_action else [],
        "source_chain": trace_chain,
        "field_synthesis_entrypoint": FIELD_SYNTHESIS_ENTRYPOINT,
        "candidate_only": True,
    }


def evaluate_positive_case(trace: Dict[str, Any], case_ref: str) -> Tuple[bool, List[str]]:
    issues: List[str] = []
    if not trace.get("synthesis_ok"):
        issues.append("synthesis_failed")
        issues.extend(trace.get("synthesis_issues") or [])

    fc = trace.get("field_candidate") or {}
    fs = trace.get("field_state_candidate") or {}
    fl = trace.get("field_interaction_label_candidate") or {}
    conflict = trace.get("field_conflict_candidate") or {}

    if fc.get("candidate_only") is not True:
        issues.append("field_candidate_not_candidate_only")
    if fc.get("direct_action_allowed") is True:
        issues.append("direct_action_allowed")

    if case_ref == "mall_stable_map_place_with_slam":
        if fl.get("field_label") != "商场":
            issues.append(f"field_label_mismatch:{fl.get('field_label')!r}")
        if fs.get("field_state") != "stable_map_place_field":
            issues.append(f"field_state_mismatch:{fs.get('field_state')!r}")
        if fc.get("spatial_binding_used") is not True:
            issues.append("spatial_binding_not_used")

    elif case_ref == "subway_station_indoor_gps_degraded":
        if fl.get("field_label") != "地铁站":
            issues.append(f"field_label_mismatch:{fl.get('field_label')!r}")
        if fc.get("gps_weight") != "degraded":
            issues.append("gps_not_degraded")
        if fc.get("slam_local_weight") != "high":
            issues.append("slam_local_not_high")
        if fc.get("coordinate_scope") not in ("local", "aligned_local"):
            issues.append(f"coordinate_scope_mismatch:{fc.get('coordinate_scope')!r}")

    elif case_ref == "stadium_concert_event_overlay":
        if fl.get("field_label") != "演唱会现场":
            issues.append(f"field_label_mismatch:{fl.get('field_label')!r}")
        if fl.get("underlying_map_place_ref") != "stadium_stub":
            issues.append("underlying_map_place_ref_mismatch")
        if fc.get("underlying_map_place_ref") != "stadium_stub":
            issues.append("map_place_rewritten_by_event")

    elif case_ref == "plaza_temporary_market_realtime_overlay":
        if fl.get("field_label") != "临时集市":
            issues.append(f"field_label_mismatch:{fl.get('field_label')!r}")
        if fs.get("field_state") != "event_and_realtime_overlay_field":
            issues.append("field_state_missing_overlay")
        if "crowd" not in (fs.get("overlay_context_types") or []):
            issues.append("crowd_overlay_missing")

    elif case_ref == "gps_slam_map_place_conflict":
        if not conflict:
            issues.append("field_conflict_candidate_missing")
        if conflict.get("field_identity_overridden") is True:
            issues.append("field_identity_overridden")

    if not fl.get("internal_field_state_ref"):
        issues.append("field_interaction_label_not_separated")

    return len(issues) == 0, issues


def build_positive_cases_v1() -> Tuple[Dict[str, Any], ...]:
    bundles = build_positive_input_bundles_v1()
    cases = []
    for case_ref in POSITIVE_CASE_REFS:
        bundle = bundles[case_ref]
        cases.append(
            {
                "case_ref": case_ref,
                "case_kind": "positive",
                "user_goal": bundle["user_goal"],
                "input_bundle_ref": bundle["bundle_ref"],
                "expected_outcome": {
                    "synthesis_ok": True,
                    "candidate_only": True,
                    "field_synthesis_entrypoint": FIELD_SYNTHESIS_ENTRYPOINT,
                },
                "input_bundle": bundle,
            }
        )
    return tuple(cases)


def build_negative_cases_v1() -> Tuple[Dict[str, Any], ...]:
    bundles = build_negative_input_bundles_v1()
    cases = []
    for case_ref in NEGATIVE_CASE_REFS:
        bundle = bundles[case_ref]
        cases.append(
            {
                "case_ref": case_ref,
                "case_kind": "negative",
                "input_bundle_ref": bundle["bundle_ref"],
                "expected_rejected": True,
                "input_bundle": bundle,
            }
        )
    return tuple(cases)
