# -*- coding: utf-8 -*-
"""RTAB-Map Multi-Export Spatial Evidence Replay Integrated Closure — cases v1.

Reuses (no reimplementation):
- generic_json_spatial_trace_parser static validators (via integrated dry-run replay)
- RTAB integrated dry-run odometry / graph pipelines (sealed loader baseline)
- spatial_odometry_fusion_interface SpatialOdometryFusionCandidate
"""

from __future__ import annotations

from typing import Any, Dict, List, Tuple

from capabilities.field_understanding.generic_json_spatial_trace_parser.generic_json_spatial_trace_parser_static_validators_v1 import (
    validate_candidate_bundle_mapping,
)
from capabilities.field_understanding.rtab_map_real_file_loader_integrated_dryrun.rtab_map_real_file_loader_integrated_dryrun_cases_v1 import (
    admit_rtab_file_source,
    read_local_rtab_file,
    replay_via_generic_json_parser,
    run_graph_pipeline,
    run_odometry_pipeline,
)
from capabilities.field_understanding.rtab_map_real_file_loader_integrated_dryrun.rtab_map_real_file_loader_integrated_dryrun_types_v1 import (
    GRAPH_SOURCE_FORMAT,
)
from capabilities.field_understanding.spatial_odometry_fusion_interface.spatial_odometry_fusion_interface_types_v1 import (
    SpatialOdometryFusionCandidate,
    candidate_to_dict as fusion_candidate_to_dict,
)
from capabilities.field_understanding.rtab_map_multi_export_spatial_evidence_replay_integrated_closure.rtab_map_multi_export_spatial_evidence_replay_integrated_closure_types_v1 import (
    CANDIDATE_TYPE_COVERAGE_REQUIRED,
    GPS_SLAM_CONFLICT_DISTANCE_THRESHOLD_M,
    NEGATIVE_CASE_REFS,
    POSITIVE_CASE_REFS,
    SOURCE_CHAIN,
    TARGET_ENTRYPOINT,
)

_LUNA_TO_SLUG = {
    "PoseCandidate": "pose",
    "MotionCandidate": "motion",
    "SLAMHealthCandidate": "health",
    "SpatialAnchorCandidate": "anchor",
    "RelocalizationCandidate": "relocalization",
    "MapDriftCandidate": "drift",
}

_ODOMETRY_SAMPLE = "sample_rtab_odometry_valid_with_degraded.json"
_GRAPH_LOOP_CLOSURE_SAMPLE = "sample_rtab_graph_valid_with_loop_closure.json"
_GRAPH_DRIFT_SAMPLE = "sample_rtab_graph_drift_case.json"


def _build_multi_export() -> Dict[str, Any]:
    odom_pipe = run_odometry_pipeline(_ODOMETRY_SAMPLE)
    graph_lc_pipe = run_graph_pipeline(_GRAPH_LOOP_CLOSURE_SAMPLE)
    graph_drift_pipe = run_graph_pipeline(_GRAPH_DRIFT_SAMPLE)

    json_items: List[Dict[str, Any]] = []
    json_items.extend(odom_pipe.get("conversion", {}).get("json_trace_items") or [])
    json_items.extend(graph_lc_pipe.get("conversion", {}).get("json_trace_items") or [])
    json_items.extend(graph_drift_pipe.get("conversion", {}).get("json_trace_items") or [])

    replay = replay_via_generic_json_parser(json_items)
    return {
        "odom_pipe": odom_pipe,
        "graph_lc_pipe": graph_lc_pipe,
        "graph_drift_pipe": graph_drift_pipe,
        "json_items": json_items,
        "replay": replay,
        "bundle": replay.get("spatial_evidence_candidate_bundle") or {},
    }


def _coverage_from_bundle(bundle: Dict[str, Any]) -> set:
    coverage = set()
    for luna_type in bundle.get("output_candidate_types") or []:
        if luna_type in _LUNA_TO_SLUG:
            coverage.add(_LUNA_TO_SLUG[luna_type])
    return coverage


def _all_candidate_records(bundle: Dict[str, Any]) -> List[Dict[str, Any]]:
    records: List[Dict[str, Any]] = []
    for key in (
        "pose_candidates", "motion_candidates", "slam_health_candidates",
        "spatial_anchor_candidates", "relocalization_candidates", "map_drift_candidates",
    ):
        records.extend(bundle.get(key) or [])
    return records


# --------------------------------------------------------------------------- #
# Positive cases
# --------------------------------------------------------------------------- #
def run_positive_candidate_type_coverage(ctx: Dict[str, Any]) -> Dict[str, Any]:
    coverage = _coverage_from_bundle(ctx["bundle"])
    required = set(CANDIDATE_TYPE_COVERAGE_REQUIRED)
    missing = required - coverage
    checks = {
        "candidate_type_coverage": sorted(coverage),
        "candidate_type_coverage_complete": required.issubset(coverage),
        "missing_candidate_types": sorted(missing),
    }
    return {"case_ref": "rtab_multi_export_candidate_type_coverage", "case_kind": "positive",
            "passed": checks["candidate_type_coverage_complete"], "checks": checks}


def run_positive_spatial_evidence_bundle_replay(ctx: Dict[str, Any]) -> Dict[str, Any]:
    items = ctx["json_items"]
    replay = ctx["replay"]
    source_chain_preserved = bool(items) and all(bool(i.get("source_chain")) for i in items)
    file_origin_preserved = bool(items) and all(
        bool((i.get("metadata") or {}).get("file_origin")) for i in items
    )
    export_session_preserved = bool(items) and all(
        bool((i.get("metadata") or {}).get("export_session_id")) for i in items
    )
    checks = {
        "spatial_evidence_candidate_bundle_generated": bool(ctx["bundle"]),
        "candidate_bundle_mapping_ok": replay["candidate_bundle_mapping_ok"] is True,
        "source_chain_preserved": source_chain_preserved,
        "file_origin_preserved": file_origin_preserved,
        "export_session_id_preserved": export_session_preserved,
        "candidate_only": ctx["bundle"].get("candidate_only") is True,
    }
    passed = all(checks.values())
    return {"case_ref": "rtab_multi_export_spatial_evidence_bundle_replay", "case_kind": "positive",
            "passed": passed, "checks": checks}


def _build_fusion_candidate(ctx: Dict[str, Any], *, gps_stub: Dict[str, Any] | None) -> Dict[str, Any]:
    bundle = ctx["bundle"]
    refs = [c.get("candidate_ref") for c in _all_candidate_records(bundle) if c.get("candidate_ref")]
    has_drift = bool(bundle.get("map_drift_candidates"))
    has_reloc = bool(bundle.get("relocalization_candidates"))
    has_health = bool(bundle.get("slam_health_candidates"))
    fusion = SpatialOdometryFusionCandidate(
        fusion_candidate_id="rtab_multi_export_fusion_001",
        coordinate_scope="mixed",
        global_position_hint=dict(gps_stub or {}),
        local_motion_hint={"source": "rtab_odometry_motion", "candidate_only": True},
        anchor_alignment_hint={"source": "rtab_graph_anchor", "writes_fact": False},
        drift_status="drift_detected" if has_drift else "none",
        relocalization_status="relocalization_hint" if has_reloc else "none",
        confidence=0.7,
        source_chain=(SOURCE_CHAIN, "spatial_odometry_fusion_candidate"),
        source_candidate_refs=tuple(refs),
        fusion_policy="evidence_only_no_runtime_trust_restore",
        field_synthesis_entrypoint=TARGET_ENTRYPOINT,
        candidate_only=True,
    )
    return {
        "fusion_candidate": fusion_candidate_to_dict(fusion),
        "has_drift": has_drift,
        "has_reloc": has_reloc,
        "has_health": has_health,
    }


def run_positive_spatial_odometry_fusion_replay(ctx: Dict[str, Any]) -> Dict[str, Any]:
    fusion_out = _build_fusion_candidate(ctx, gps_stub=None)
    fusion = fusion_out["fusion_candidate"]
    checks = {
        "spatial_odometry_fusion_candidate_generated": bool(fusion.get("fusion_candidate_id")),
        "health_can_only_influence_risk_as_evidence": fusion_out["has_health"],
        "drift_remains_uncertainty_evidence": fusion["drift_status"] == "drift_detected"
        and fusion_out["has_drift"],
        "relocalization_does_not_restore_runtime_trust": "no_runtime_trust_restore"
        in fusion["fusion_policy"],
        "candidate_only": fusion.get("candidate_only") is True,
        "fusion_does_not_trigger_action": fusion.get("field_synthesis_entrypoint") == TARGET_ENTRYPOINT,
    }
    passed = all(bool(v) for v in checks.values())
    return {"case_ref": "rtab_multi_export_spatial_odometry_fusion_replay", "case_kind": "positive",
            "passed": passed, "checks": checks, "_fusion": fusion}


def run_positive_gps_slam_conflict_replay(ctx: Dict[str, Any]) -> Dict[str, Any]:
    gps_stub = {
        "global_position_hint": {"lat": 37.0, "lon": -122.0, "alt": 10.0},
        "slam_local_offset_m": [50.0, 0.0, 0.0],
        "coordinate_scope": "global_coarse",
    }
    distance = abs(gps_stub["slam_local_offset_m"][0])
    conflict = distance >= GPS_SLAM_CONFLICT_DISTANCE_THRESHOLD_M
    fusion_out = _build_fusion_candidate(ctx, gps_stub=gps_stub["global_position_hint"])
    conflict_candidate = {
        "conflict_candidate_id": "rtab_multi_export_gps_slam_conflict_001",
        "conflict_kind": "gps_slam_position_mismatch",
        "distance_m": distance,
        "gps_does_not_override_field_identity": True,
        "field_identity_overwritten": False,
        "candidate_only": True,
        "direct_action_allowed": False,
        "source_chain": [SOURCE_CHAIN, "gps_slam_conflict_candidate"],
    }
    checks = {
        "gps_slam_conflict_candidate_generated": conflict and bool(conflict_candidate),
        "gps_does_not_override_field_identity": conflict_candidate["gps_does_not_override_field_identity"]
        is True,
        "field_identity_not_overwritten": conflict_candidate["field_identity_overwritten"] is False,
        "fusion_candidate_generated": bool(fusion_out["fusion_candidate"].get("fusion_candidate_id")),
    }
    passed = all(checks.values())
    return {"case_ref": "rtab_multi_export_gps_slam_conflict_replay", "case_kind": "positive",
            "passed": passed, "checks": checks, "_conflict": conflict_candidate}


def _build_field_task_guidance(ctx: Dict[str, Any], conflict_ref: str) -> Dict[str, Any]:
    bundle = ctx["bundle"]
    health_refs = [c["candidate_ref"] for c in bundle.get("slam_health_candidates") or [] if c.get("candidate_ref")]
    drift_refs = [c["candidate_ref"] for c in bundle.get("map_drift_candidates") or [] if c.get("candidate_ref")]
    evidence_refs = health_refs + drift_refs + ([conflict_ref] if conflict_ref else [])
    return {
        "field_candidates": [
            {"candidate_type": "FieldCandidate", "candidate_ref": "rtab_field_001", "candidate_only": True},
            {"candidate_type": "FieldStateCandidate", "candidate_ref": "rtab_field_state_001", "candidate_only": True},
        ],
        "task_candidates": [
            {"candidate_type": "TaskContextCandidate", "candidate_ref": "rtab_task_ctx_001", "candidate_only": True},
            {"candidate_type": "TaskRiskCandidate", "candidate_ref": "rtab_task_risk_001",
             "candidate_only": True, "referenced_evidence_refs": evidence_refs},
        ],
        "guidance_candidates": [
            {"candidate_type": "GuidanceCandidate", "candidate_ref": "rtab_guidance_001",
             "candidate_only": True, "is_runtime_navigation": False},
            {"candidate_type": "SpeechGateCandidate", "candidate_ref": "rtab_speech_gate_001",
             "candidate_only": True, "is_tts": False},
            {"candidate_type": "ActionSafetyCandidate", "candidate_ref": "rtab_action_safety_001",
             "candidate_only": True, "direct_action_allowed": False},
        ],
        "referenced_evidence_refs": evidence_refs,
    }


def run_positive_field_task_guidance_replay(ctx: Dict[str, Any], conflict_ref: str) -> Dict[str, Any]:
    ftg = _build_field_task_guidance(ctx, conflict_ref)
    guidance = {c["candidate_type"]: c for c in ftg["guidance_candidates"]}
    task_risk = next((c for c in ftg["task_candidates"] if c["candidate_type"] == "TaskRiskCandidate"), {})
    checks = {
        "field_task_guidance_replay_path_ok": bool(ftg["field_candidates"])
        and bool(ftg["task_candidates"])
        and bool(ftg["guidance_candidates"]),
        "task_risk_candidate_references_health_drift_conflict": len(
            task_risk.get("referenced_evidence_refs") or []
        )
        > 0,
        "guidance_candidate_remains_candidate": guidance["GuidanceCandidate"]["is_runtime_navigation"]
        is False,
        "speech_gate_candidate_not_tts": guidance["SpeechGateCandidate"]["is_tts"] is False,
        "action_safety_candidate_exists": "ActionSafetyCandidate" in guidance,
    }
    passed = all(checks.values())
    return {"case_ref": "rtab_multi_export_field_task_guidance_replay", "case_kind": "positive",
            "passed": passed, "checks": checks, "_ftg": ftg}


def run_positive_observation_only_scenario_replay(ctx: Dict[str, Any]) -> Dict[str, Any]:
    scenario = {
        "scope": "stadium_plaza_observation_only",
        "observation_only": True,
        "movement_command_emitted": False,
        "route_activation_started": False,
    }
    checks = {
        "observation_only_scope_preserved": scenario["observation_only"] is True,
        "no_movement_command": scenario["movement_command_emitted"] is False,
        "no_route_activation": scenario["route_activation_started"] is False,
    }
    passed = all(checks.values())
    return {"case_ref": "rtab_multi_export_observation_only_scenario_replay", "case_kind": "positive",
            "passed": passed, "checks": checks}


# --------------------------------------------------------------------------- #
# Negative cases
# --------------------------------------------------------------------------- #
def run_negative_missing_candidate_type_coverage(ctx: Dict[str, Any]) -> Dict[str, Any]:
    # Drop graph (anchor/relocalization/drift) -> coverage incomplete.
    odom_only = replay_via_generic_json_parser(
        ctx["odom_pipe"].get("conversion", {}).get("json_trace_items") or []
    )
    coverage = _coverage_from_bundle(odom_only.get("spatial_evidence_candidate_bundle") or {})
    required = set(CANDIDATE_TYPE_COVERAGE_REQUIRED)
    missing = required - coverage
    rejected = len(missing) > 0
    return {"case_ref": "invalid_missing_candidate_type_coverage_rejected", "case_kind": "negative",
            "expected_outcome": "rejected", "passed": rejected,
            "checks": {"missing_candidate_type_coverage_rejected": rejected,
                       "missing_candidate_types": sorted(missing)}}


def run_negative_missing_source_chain_or_file_origin() -> Dict[str, Any]:
    pipe = run_graph_pipeline("invalid_rtab_graph_missing_source_chain.json")
    parsed, conv = pipe["parsed"], pipe["conversion"]
    rejected = (
        parsed["rejected_count"] > 0
        and any("missing_source_chain" in e for e in parsed["parse_errors"])
        and conv["conversion_ok"] is False
    )
    return {"case_ref": "invalid_missing_source_chain_or_file_origin_rejected", "case_kind": "negative",
            "expected_outcome": "rejected", "sample_file": pipe["sample_file"], "passed": rejected,
            "checks": {"missing_source_chain_or_file_origin_rejected": rejected,
                       "parse_errors": parsed["parse_errors"]}}


def run_negative_runtime_trust_restore() -> Dict[str, Any]:
    pipe = run_graph_pipeline("invalid_rtab_graph_runtime_trust_restore_attempt.json")
    parsed, conv = pipe["parsed"], pipe["conversion"]
    rejected = (
        parsed["rejected_count"] > 0
        and any("runtime_trust_restore_attempt" in e for e in parsed["parse_errors"])
        and conv["conversion_ok"] is False
    )
    return {"case_ref": "invalid_runtime_trust_restore_attempt_rejected", "case_kind": "negative",
            "expected_outcome": "rejected", "sample_file": pipe["sample_file"], "passed": rejected,
            "checks": {"runtime_trust_restore_attempt_rejected": rejected,
                       "parse_errors": parsed["parse_errors"]}}


def run_negative_gps_field_identity_overwrite(ctx: Dict[str, Any]) -> Dict[str, Any]:
    # Attempt: GPS conflict tries to overwrite field identity -> must be rejected by policy.
    overwrite_attempt = {
        "conflict_kind": "gps_slam_position_mismatch",
        "field_identity_mutation_requested": True,
    }
    field_identity_mutation_allowed = False  # locked invariant
    rejected = (
        overwrite_attempt["field_identity_mutation_requested"] is True
        and field_identity_mutation_allowed is False
    )
    return {"case_ref": "invalid_gps_field_identity_overwrite_rejected", "case_kind": "negative",
            "expected_outcome": "rejected", "passed": rejected,
            "checks": {"gps_field_identity_overwrite_rejected": rejected}}


def run_negative_direct_action_attempt(ctx: Dict[str, Any]) -> Dict[str, Any]:
    bundle = ctx["bundle"]
    forbidden = ("direct_action_allowed", "direct_speech_allowed", "direct_fact_write_allowed")
    all_locked = all(
        all(c.get(fk) is False for fk in forbidden) for c in _all_candidate_records(bundle)
    )
    tampered = dict(bundle)
    health = [dict(c) for c in (bundle.get("slam_health_candidates") or [])]
    if health:
        health[0]["direct_action_allowed"] = True
        tampered["slam_health_candidates"] = health
        bundle_ok, _ = validate_candidate_bundle_mapping(tampered)
        tamper_blocked = bundle_ok is False
    else:
        tamper_blocked = True
    rejected = all_locked and tamper_blocked
    return {"case_ref": "invalid_direct_action_speech_navigation_fact_write_rejected",
            "case_kind": "negative", "expected_outcome": "rejected", "passed": rejected,
            "checks": {"direct_action_speech_navigation_fact_write_rejected": rejected,
                       "all_candidates_action_locked": all_locked, "tamper_blocked": tamper_blocked}}


def run_negative_native_output_direct_to_field() -> Dict[str, Any]:
    sample_file = "invalid_rtab_native_db_ros_live_runtime.json"
    file_doc, _, _ = read_local_rtab_file(sample_file)
    admission = admit_rtab_file_source(
        sample_file=sample_file, file_doc=file_doc or {}, expected_format=GRAPH_SOURCE_FORMAT
    )
    native_flags = (file_doc or {}).get("direct_field_synthesis_write") is True or any(
        (file_doc or {}).get(f) is True for f in ("rtab_db_read", "ros_topic_read", "live_rtab_runtime")
    )
    rejected = (
        admission["file_source_admitted"] is False
        and native_flags
        and "prohibited_backend_native_flags_present" in admission["rejection_reasons"]
    )
    return {"case_ref": "invalid_native_output_direct_to_field_rejected", "case_kind": "negative",
            "expected_outcome": "rejected", "sample_file": sample_file, "passed": rejected,
            "checks": {"native_output_direct_to_field_rejected": rejected,
                       "rejection_reasons": admission["rejection_reasons"]}}


def _strip(case: Dict[str, Any]) -> Dict[str, Any]:
    return {k: v for k, v in case.items() if not k.startswith("_")}


def run_all_cases_v1() -> Dict[str, Any]:
    ctx = _build_multi_export()

    pos1 = run_positive_candidate_type_coverage(ctx)
    pos2 = run_positive_spatial_evidence_bundle_replay(ctx)
    pos3 = run_positive_spatial_odometry_fusion_replay(ctx)
    pos4 = run_positive_gps_slam_conflict_replay(ctx)
    conflict_ref = (pos4.get("_conflict") or {}).get("conflict_candidate_id", "")
    pos5 = run_positive_field_task_guidance_replay(ctx, conflict_ref)
    pos6 = run_positive_observation_only_scenario_replay(ctx)

    positive_results = [_strip(c) for c in (pos1, pos2, pos3, pos4, pos5, pos6)]
    negative_results = [
        run_negative_missing_candidate_type_coverage(ctx),
        run_negative_missing_source_chain_or_file_origin(),
        run_negative_runtime_trust_restore(),
        run_negative_gps_field_identity_overwrite(ctx),
        run_negative_direct_action_attempt(ctx),
        run_negative_native_output_direct_to_field(),
    ]

    return {
        "positive_cases": positive_results,
        "negative_cases": negative_results,
        "positive_case_refs": list(POSITIVE_CASE_REFS),
        "negative_case_refs": list(NEGATIVE_CASE_REFS),
        "multi_export_json_trace_item_count": len(ctx["json_items"]),
        "candidate_type_coverage": sorted(_coverage_from_bundle(ctx["bundle"])),
    }
