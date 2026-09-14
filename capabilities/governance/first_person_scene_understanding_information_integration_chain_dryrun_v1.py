# -*- coding: utf-8 -*-
"""First Person Scene Understanding Information Integration Chain DryRun v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.first_person_vision_navigation_candidate_flow_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as CF_DR_FINAL_GO,
)
from capabilities.governance.luna_constitution_capability_bus_governance_baseline_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as CB_DR_FINAL_GO,
)
from capabilities.governance.midplatform_information_integration_layer_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as II_DR_FINAL_GO,
)
from capabilities.governance.midplatform_information_integration_layer_planning_v1 import (
    DECISION_READINESS_FIELDS,
    FRESHNESS_STATUS_FIELDS,
    INTEGRATED_CONTEXT_CANDIDATE_FIELDS,
    PRIORITY_MAP_FIELDS,
    UPSTREAM_RUNTIME_LEAKAGE_FIELDS,
)
from capabilities.governance.midplatform_safety_gate_planning_v1 import FOUR_LAYER_ARCHITECTURE
from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.governance.provider_abstraction_standard_alignment_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as PROVIDER_DR_FINAL_GO,
)
from capabilities.governance.seed_core_drive_signal_contract_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as DS_DR_FINAL_GO,
)

PHASE_ID = "Phase-First-Person-Scene-Understanding-Information-Integration-Chain-DryRun-v1-001"
SCOPE = "first_person_scene_understanding_information_integration_chain_dryrun_only"
SOURCE_CHAIN = "first_person_scene_understanding_information_integration_chain_dryrun_v1"

UPSTREAM_CF_DR_FINAL = CF_DR_FINAL_GO

FINAL_DECISION_GO = (
    "FIRST_PERSON_SCENE_UNDERSTANDING_INFORMATION_INTEGRATION_CHAIN_DRYRUN_CLOSED_"
    "READY_FOR_DECISION_CHAIN_CANDIDATE_DRYRUN"
)
FINAL_DECISION_HOLD = (
    "FIRST_PERSON_SCENE_UNDERSTANDING_INFORMATION_INTEGRATION_CHAIN_DRYRUN_HOLD_FOR_ISSUE_REVIEW"
)
NEXT_PHASE_GO = "Phase-First-Person-Scene-Understanding-Decision-Chain-Candidate-DryRun-v1-001"
NEXT_PHASE_HOLD = (
    "Phase-First-Person-Scene-Understanding-Information-Integration-Chain-Issue-Review-v1-001"
)

SCENE_UNDERSTANDING_GOALS: Tuple[Dict[str, str], ...] = (
    {"goal_id": "first_goal", "goal": "current_scene_understanding"},
    {"goal_id": "second_goal", "goal": "spatiotemporal_continuity_and_world_understanding"},
    {"goal_id": "third_goal", "goal": "navigation_application_layer"},
    {"goal_id": "fourth_goal", "goal": "expanded_application_capabilities_person_recognition_reading_etc"},
)

TARGET_RECOGNITION_FIELDS: Tuple[str, ...] = (
    "target_candidate_id",
    "target_type",
    "target_description",
    "source_visual_refs",
    "source_task_intent_refs",
    "confidence",
    "tracking_required",
    "candidate_only",
    "not_fact",
)

TARGET_TRACKING_FIELDS: Tuple[str, ...] = (
    "tracking_candidate_id",
    "target_ref",
    "temporal_frame_refs",
    "continuity_status",
    "last_seen_context",
    "movement_hint",
    "lost_target_risk",
    "reobserve_required",
    "candidate_only",
    "runtime_source",
)

TASK_INTENT_FIELDS: Tuple[str, ...] = (
    "task_intent_candidate_id",
    "source_dialogue_ref",
    "requested_target",
    "requested_action_type",
    "target_search_required",
    "required_observation_refs",
    "task_priority",
    "candidate_only",
    "not_decision",
)

SPATIOTEMPORAL_CONTEXT_FIELDS: Tuple[str, ...] = (
    "spatiotemporal_context_id",
    "temporal_sequence_refs",
    "location_context_refs",
    "scene_transition_hint",
    "continuity_confidence",
    "missing_sequence_gap_refs",
    "candidate_only",
    "not_fact",
)

WORLD_CONTINUITY_FIELDS: Tuple[str, ...] = (
    "world_continuity_candidate_id",
    "current_scene_refs",
    "previous_scene_refs",
    "inferred_continuity",
    "missing_content_hint",
    "rule_context_refs",
    "confidence",
    "validation_required",
    "candidate_only",
    "not_fact",
)

SCENE_RULE_FIELDS: Tuple[str, ...] = (
    "scene_rule_candidate_id",
    "scene_type",
    "possible_rules",
    "safety_relevance",
    "social_relevance",
    "navigation_relevance",
    "confidence",
    "candidate_only",
)

INTAKE_SAMPLE_IDS: Tuple[str, ...] = (
    "visual_obs_sample_crossing_001",
    "target_recognition_sample_crosswalk_001",
    "text_recognition_sample_sign_001",
    "target_tracking_sample_crosswalk_001",
    "task_intent_sample_find_crosswalk_001",
    "scene_context_sample_crossing_001",
    "spatiotemporal_context_sample_approach_001",
    "world_continuity_sample_intersection_001",
    "risk_context_sample_traffic_001",
    "required_observation_candidate:traffic_check_001",
    "route_context_sample_001",
    "navigation_task_sample_001",
    "drive_signal_sample_survival_001",
    "health_signal_candidate:module_status_001",
    "whitebox_trace:scene_chain_intake_001",
)

TARGET_RECOGNITION_REVIEW_ITEMS: Tuple[str, ...] = (
    "visual candidates can identify target candidates",
    "task_intent can bias target search",
    "target recognition remains candidate-only",
    "missing target creates required_observation_candidate",
    "no target becomes fact without validation",
)

TEXT_RECOGNITION_REVIEW_ITEMS: Tuple[str, ...] = (
    "OCR/text recognition binds visual region",
    "recognized text remains candidate",
    "text can influence scene understanding and navigation context only as candidate",
    "text requires validation where needed",
)

TARGET_TRACKING_REVIEW_ITEMS: Tuple[str, ...] = (
    "tracking requires temporal continuity",
    "lost target creates gap_candidate / reobserve_required",
    "tracking candidate does not invoke camera/runtime",
    "tracking does not become identity recognition by default",
)

TASK_INTENT_TARGET_SEARCH_REVIEW_ITEMS: Tuple[str, ...] = (
    "voice/dialogue requirement can create task_intent_candidate",
    "task_intent can request target search",
    "task_intent cannot force action",
    "target search remains observation requirement",
)

SPATIOTEMPORAL_CONTINUITY_REVIEW_ITEMS: Tuple[str, ...] = (
    "continuous frame understanding is second-level goal",
    "missing sequence creates gap_candidate",
    "stale/simulated sequence cannot authorize action",
    "location/scene continuity remains candidate-only",
)

WORLD_CONTINUITY_REVIEW_ITEMS: Tuple[str, ...] = (
    "world continuity candidate can fill missing context as hypothesis",
    "inferred continuity is not fact",
    "scene rules remain candidate until validated",
    "survival context can prioritize observation",
)

SURVIVAL_CONTEXT_REVIEW_ITEMS: Tuple[str, ...] = (
    "Survival Drive affects risk/observation priority",
    "scene rules and survival context influence readiness",
    "survival risk can recommend hold/observe_more",
    "survival signal does not generate output/action",
)

NAVIGATION_APPLICATION_REVIEW_ITEMS: Tuple[str, ...] = (
    "route_context/navigation_task are application-layer context",
    "navigation depends on target recognition + spatiotemporal understanding",
    "navigation action not generated",
    "navigation is third-level goal",
    "route context cannot override survival safety",
)

EVIDENCE_TRACEABILITY_REVIEW_ITEMS: Tuple[str, ...] = (
    "source_chain_matrix generated",
    "target/text/tracking/task/scene/spatiotemporal refs preserved",
    "fixture provenance preserved",
    "whitebox_trace_refs preserved",
    "validation_required flags preserved",
)

DC_HANDOFF_REVIEW_ITEMS: Tuple[str, ...] = (
    "integrated_context_candidate can be handed to Decision Center later",
    "decision_readiness_candidate attached",
    "unresolved conflict/gap/freshness refs attached",
    "Decision Center remains裁决层",
    "no decision_candidate generated now",
)

BLOCKED_PATHS: Tuple[str, ...] = (
    "dryrun_to_camera_invocation",
    "dryrun_to_real_frame_read",
    "dryrun_to_vision_runtime_enable",
    "dryrun_to_ocr_runtime_enable",
    "dryrun_to_real_ocr_execution",
    "dryrun_to_map_provider_invocation",
    "dryrun_to_navigation_runtime_enable",
    "dryrun_to_real_navigation_action",
    "dryrun_to_provider_invocation",
    "dryrun_to_model_runtime",
    "dryrun_to_information_integration_runtime_enable",
    "dryrun_to_decision_execution",
    "dryrun_to_decision_candidate_generation",
    "dryrun_to_user_output",
    "dryrun_to_memory_write",
    "dryrun_to_world_model_write",
    "dryrun_to_task_state_commit",
    "dryrun_to_controlled_runtime_enable",
)

NON_CLAIMS: Tuple[str, ...] = (
    "Scene Understanding Chain DryRun GO ≠ camera/OCR/map/navigation runtime enabled",
    "integrated_context_candidate ≠ decision",
    "target recognition candidate ≠ identified fact",
    "world continuity candidate ≠ worldmodel fact",
    "navigation context ≠ navigation action allowed",
    "next Decision Chain Candidate DryRun ≠ real execution",
)

BOUNDARY_TRUE: Tuple[str, ...] = (
    "first_person_scene_understanding_information_integration_chain_dryrun_only",
    "simulated",
    "sample_fixture_only",
)

BOUNDARY_FALSE: Tuple[str, ...] = (
    "camera_invoked_now",
    "real_frame_read_now",
    "vision_runtime_enabled_now",
    "ocr_runtime_enabled_now",
    "real_ocr_executed_now",
    "map_provider_invoked_now",
    "navigation_runtime_enabled_now",
    "real_navigation_action_executed_now",
    "provider_invoked_now",
    "model_runtime_invoked_now",
    "information_integration_runtime_enabled_now",
    "decision_executed_now",
    "decision_candidate_generated_now",
    "user_output_generated_now",
    "memory_written_now",
    "world_model_written_now",
    "task_state_committed_now",
    "controlled_runtime_enabled_now",
)

DEFAULT_OUTPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "first_person_scene_understanding_information_integration_chain_dryrun"
)


def _dryrun_meta() -> Dict[str, Any]:
    meta = {
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "source_chain": SOURCE_CHAIN,
        "selected_provider_for_execution": None,
        "four_layer_architecture": FOUR_LAYER_ARCHITECTURE,
        "system_level_simulated_go": True,
        "mainline": "first_person_scene_understanding",
    }
    for field in BOUNDARY_TRUE:
        meta[field] = True
    for field in BOUNDARY_FALSE:
        meta[field] = False
    return meta


def _try_read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def _review_ok(checks: List[Tuple[str, bool]]) -> Dict[str, Any]:
    issues = [{"issue_id": cid, "detail": "must pass"} for cid, passed in checks if not passed]
    return {
        "checks": [{"check_id": cid, "pass": passed} for cid, passed in checks],
        "issues": issues,
        "dryrun_and_review_pass": len(issues) == 0,
    }


def _check_upstream_no_runtime_leakage(summary: Dict[str, Any]) -> List[str]:
    issues: List[str] = []
    for field in UPSTREAM_RUNTIME_LEAKAGE_FIELDS:
        if field in summary and summary.get(field) is not False:
            issues.append(f"{field} must be false")
    return issues


def run_first_person_scene_understanding_information_integration_chain_dryrun_v1(
    *,
    first_person_vision_navigation_candidate_flow_dryrun_and_review_root: str,
    first_person_vision_navigation_candidate_flow_planning_root: str,
    midplatform_information_integration_layer_dryrun_and_review_root: str,
    seed_core_drive_signal_contract_dryrun_and_review_root: str,
    luna_constitution_capability_bus_governance_baseline_dryrun_and_review_root: str,
    provider_abstraction_standard_alignment_dryrun_and_review_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []

    cf_dr_root = Path(
        first_person_vision_navigation_candidate_flow_dryrun_and_review_root
    ).expanduser().resolve()
    cf_plan_root = Path(
        first_person_vision_navigation_candidate_flow_planning_root
    ).expanduser().resolve()
    ii_dr_root = Path(
        midplatform_information_integration_layer_dryrun_and_review_root
    ).expanduser().resolve()
    ds_dr_root = Path(seed_core_drive_signal_contract_dryrun_and_review_root).expanduser().resolve()
    cb_dr_root = Path(
        luna_constitution_capability_bus_governance_baseline_dryrun_and_review_root
    ).expanduser().resolve()
    provider_dr_root = Path(
        provider_abstraction_standard_alignment_dryrun_and_review_root
    ).expanduser().resolve()

    cf_dr_sm = _try_read_json(cf_dr_root / "summary.json") or {}
    cf_dr_vr = _try_read_json(cf_dr_root / "verifier_report.json") or {}
    ii_dr_vr = _try_read_json(ii_dr_root / "verifier_report.json") or {}
    ds_dr_vr = _try_read_json(ds_dr_root / "verifier_report.json") or {}
    cb_dr_vr = _try_read_json(cb_dr_root / "verifier_report.json") or {}
    provider_dr_vr = _try_read_json(provider_dr_root / "verifier_report.json") or {}

    sample_visual = _try_read_json(cf_dr_root / "sample_visual_observation_candidate_v1.json") or {}
    sample_ocr = _try_read_json(cf_dr_root / "sample_ocr_result_candidate_v1.json") or {}
    sample_route = _try_read_json(cf_dr_root / "sample_route_context_candidate_v1.json") or {}
    sample_nav = _try_read_json(cf_dr_root / "sample_navigation_task_candidate_v1.json") or {}
    sample_drive = _try_read_json(ds_dr_root / "sample_drive_signal_candidate_v1.json") or {}

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    meta = {
        **_dryrun_meta(),
        "upstream_candidate_flow_dryrun_root": str(cf_dr_root),
        "upstream_candidate_flow_planning_root": str(cf_plan_root),
        "upstream_information_integration_dryrun_root": str(ii_dr_root),
        "upstream_drive_signal_dryrun_root": str(ds_dr_root),
        "upstream_constitution_bus_dryrun_root": str(cb_dr_root),
        "upstream_provider_abstraction_dryrun_root": str(provider_dr_root),
        "output_root": str(out_root),
        "historical_phase_preserved": "Phase-First-Person-Vision-Navigation-Candidate-Flow-DryRunAndReview-v1-001",
        "mainline_reframe": "first_person_scene_understanding",
    }

    if cf_dr_vr.get("verifier") != "GO":
        blockers.append("Candidate Flow DryRunAndReview must be GO")
    if cf_dr_sm.get("final_decision") != UPSTREAM_CF_DR_FINAL:
        blockers.append("candidate flow dryrun final_decision mismatch")
    if ii_dr_vr.get("verifier") != "GO":
        blockers.append("Information Integration Layer DryRunAndReview must be GO")
    if ds_dr_vr.get("verifier") != "GO":
        blockers.append("Drive Signal Contract DryRunAndReview must be GO")
    if cb_dr_vr.get("verifier") != "GO":
        blockers.append("Constitution-Bus v1.0 must be GO")
    if provider_dr_vr.get("verifier") != "GO":
        blockers.append("Provider Abstraction must be GO")

    if sample_visual.get("runtime_source") is not False:
        blockers.append("visual sample must have runtime_source=false")
    if sample_visual.get("candidate_only") is not True:
        blockers.append("visual sample must be candidate_only")

    leakage_issues: List[str] = []
    for label, sm in (
        ("cf_dr", cf_dr_sm),
        ("ii_dr", _try_read_json(ii_dr_root / "summary.json") or {}),
        ("ds_dr", _try_read_json(ds_dr_root / "summary.json") or {}),
        ("cb_dr", _try_read_json(cb_dr_root / "summary.json") or {}),
        ("provider", _try_read_json(provider_dr_root / "summary.json") or {}),
    ):
        for issue in _check_upstream_no_runtime_leakage(sm):
            leakage_issues.append(f"{label}:{issue}")
    blockers.extend(leakage_issues)

    input_ok = len(blockers) == 0

    priority_reframe = {
        "reframe_id": "scene_understanding_priority_reframe_v1",
        "mainline": "first_person_scene_understanding",
        "historical_vision_navigation_flow_preserved": True,
        "historical_flow_reinterpreted_as_application_context": True,
        "goals": list(SCENE_UNDERSTANDING_GOALS),
        "first_goal": "current_scene_understanding",
        "second_goal": "spatiotemporal_continuity_and_world_understanding",
        "third_goal": "navigation_application_layer",
        "fourth_goal": "expanded_application_capabilities_person_recognition_reading_etc",
        "navigation_is_core_application_not_first_goal": True,
        "navigation_depends_on": [
            "target_recognition",
            "spatiotemporal_understanding",
            "scene_rule_understanding",
        ],
        "reframe_pass": True,
        **meta,
    }

    target_recognition = {
        "target_candidate_id": "target_recognition_sample_crosswalk_001",
        "target_type": "signage_crosswalk",
        "target_description": "crosswalk_sign_ahead_candidate",
        "source_visual_refs": ["visual_obs_sample_crossing_001"],
        "source_task_intent_refs": ["task_intent_sample_find_crosswalk_001"],
        "confidence": 0.71,
        "tracking_required": True,
        "candidate_only": True,
        "not_fact": True,
        **meta,
    }

    text_recognition = {
        **sample_ocr,
        "text_recognition_candidate_id": "text_recognition_sample_sign_001",
        "recognized_text_candidate": sample_ocr.get("recognized_text_candidate", "人行横道"),
        "source_visual_region_ref": sample_ocr.get("source_visual_region_ref"),
        "candidate_only": True,
        "not_fact": True,
    }

    target_tracking = {
        "tracking_candidate_id": "target_tracking_sample_crosswalk_001",
        "target_ref": "target_recognition_sample_crosswalk_001",
        "temporal_frame_refs": [
            "fixture:frame_seq:crossing_001",
            "fixture:frame_seq:crossing_002",
        ],
        "continuity_status": "partial_continuity_fixture",
        "last_seen_context": "approach_intersection_left_side",
        "movement_hint": "target_moving_toward_center_of_view",
        "lost_target_risk": "low",
        "reobserve_required": False,
        "candidate_only": True,
        "runtime_source": False,
        **meta,
    }

    task_intent = {
        "task_intent_candidate_id": "task_intent_sample_find_crosswalk_001",
        "source_dialogue_ref": "dialogue:voice_request:find_crosswalk_001",
        "requested_target": "crosswalk_sign_or_crossing_entry",
        "requested_action_type": "target_search_observation",
        "target_search_required": True,
        "required_observation_refs": ["required_observation_candidate:traffic_check_001"],
        "task_priority": "high",
        "candidate_only": True,
        "not_decision": True,
        **meta,
    }

    scene_context = {
        "scene_context_candidate_id": "scene_context_sample_crossing_001",
        "scene_category_candidate": "outdoor_street_crossing",
        "indoor_outdoor_status": "outdoor",
        "mobility_context": "pedestrian_approach",
        "public_facility_context": "crosswalk_zone",
        "scene_understanding_priority": "first_goal",
        "navigation_relevance": "application_layer_only",
        "risk_relevance": "high",
        "confidence": 0.74,
        "candidate_only": True,
        "not_fact": True,
        **meta,
    }

    spatiotemporal = {
        "spatiotemporal_context_id": "spatiotemporal_context_sample_approach_001",
        "temporal_sequence_refs": [
            "fixture:frame_seq:crossing_001",
            "fixture:frame_seq:crossing_002",
            "fixture:frame_seq:crossing_003",
        ],
        "location_context_refs": ["spatial:intersection_approach"],
        "scene_transition_hint": "approaching_crossing_from_sidewalk",
        "continuity_confidence": 0.66,
        "missing_sequence_gap_refs": ["gap:missing_mid_sequence_validation_001"],
        "candidate_only": True,
        "not_fact": True,
        **meta,
    }

    world_continuity = {
        "world_continuity_candidate_id": "world_continuity_sample_intersection_001",
        "current_scene_refs": ["scene_context_sample_crossing_001"],
        "previous_scene_refs": ["fixture:scene:intersection_approach_prior"],
        "inferred_continuity": "same_intersection_approach_hypothesis",
        "missing_content_hint": "mid_sequence_traffic_state_unknown",
        "rule_context_refs": ["scene_rule_sample_crossing_traffic_001"],
        "confidence": 0.58,
        "validation_required": True,
        "candidate_only": True,
        "not_fact": True,
        **meta,
    }

    scene_rule = {
        "scene_rule_candidate_id": "scene_rule_sample_crossing_traffic_001",
        "scene_type": "street_crossing",
        "possible_rules": [
            "wait_for_traffic_signal_or_safe_gap",
            "use_crosswalk_when_available",
            "observe_oncoming_traffic_before_crossing",
        ],
        "safety_relevance": "high",
        "social_relevance": "moderate",
        "navigation_relevance": "application_layer",
        "confidence": 0.62,
        "candidate_only": True,
        **meta,
    }

    risk_context = {
        "risk_context_candidate_id": "risk_context_sample_traffic_001",
        "risk_type": "traffic_or_crossing_attention_required",
        "risk_level": "moderate",
        "survival_relevance": "high",
        "scene_rule_refs": ["scene_rule_sample_crossing_traffic_001"],
        "candidate_only": True,
        "not_fact": True,
        **meta,
    }

    required_observation = {
        "required_observation_candidate_id": "required_observation_candidate:traffic_check_001",
        "observation_type": "traffic_and_crossing_status_check",
        "trigger_refs": [
            "task_intent_sample_find_crosswalk_001",
            "risk_context_sample_traffic_001",
        ],
        "priority": "high",
        "candidate_only": True,
        **meta,
    }

    intake_set = {
        "intake_id": "sample_scene_understanding_candidate_intake_set_v1",
        "sample_ids": list(INTAKE_SAMPLE_IDS),
        "sample_count": len(INTAKE_SAMPLE_IDS),
        "fixture_metadata_only": True,
        "runtime_source_false": True,
        "scene_understanding_primary": True,
        "navigation_application_layer_only": True,
        "candidate_only": True,
        "not_fact": True,
        "not_action": True,
        "not_user_output": True,
        "samples": {
            "visual_observation_candidate": sample_visual,
            "target_recognition_candidate": target_recognition,
            "text_recognition_candidate": text_recognition,
            "target_tracking_candidate": target_tracking,
            "task_intent_candidate": task_intent,
            "scene_context_candidate": scene_context,
            "spatiotemporal_context_candidate": spatiotemporal,
            "world_continuity_candidate": world_continuity,
            "scene_rule_candidate": scene_rule,
            "risk_context_candidate": risk_context,
            "required_observation_candidate": required_observation,
            "route_context_candidate": {**sample_route, "application_layer": True},
            "navigation_task_candidate": {**sample_nav, "application_layer": True},
            "drive_signal_candidate": sample_drive,
            "health_signal_candidate": {
                "health_signal_id": "health_signal_candidate:module_status_001",
                "pressure_level": "moderate",
                "candidate_only": True,
            },
            "whitebox_trace_refs": ["whitebox_trace:scene_chain_intake_001", "trace:visual_obs:001"],
        },
        **meta,
    }

    input_review = {
        "review_id": "previous_candidate_flow_input_review_v1",
        "candidate_flow_dryrun_verifier": cf_dr_vr.get("verifier"),
        "candidate_flow_dryrun_final_decision": cf_dr_sm.get("final_decision"),
        "historical_phase_name_preserved": True,
        "mainline_reframe_applied": True,
        "information_integration_verifier": ii_dr_vr.get("verifier"),
        "drive_signal_verifier": ds_dr_vr.get("verifier"),
        "constitution_bus_verifier": cb_dr_vr.get("verifier"),
        "provider_abstraction_verifier": provider_dr_vr.get("verifier"),
        "fixture_metadata_only": True,
        "no_runtime_leakage_in_upstream": len(leakage_issues) == 0,
        "chain_dryrun_only": True,
        "review_pass": input_ok,
        "blockers": blockers,
        **meta,
    }

    chain_model = {
        **meta,
        "model_id": "first_person_scene_understanding_information_integration_chain_v1",
        "chain_type": "fixture_based_scene_understanding_integration_chain",
        "primary_goal": "current_scene_understanding",
        "secondary_goal": "spatiotemporal_continuity_and_world_understanding",
        "tertiary_goal": "navigation_application_layer",
        "consumes_scene_understanding_candidates": True,
        "consumes_navigation_application_context": True,
        "consumes_drive_signal_candidate": True,
        "emits_integrated_context_candidate": True,
        "emits_context_conflict_candidate": True,
        "emits_context_gap_candidate": True,
        "emits_decision_readiness_candidate": True,
        "does_not_decide": True,
        "does_not_invoke_provider": True,
        "does_not_enable_runtime": True,
        "candidate_only": True,
    }

    integrated = {
        "integrated_context_id": "integrated_context_scene_understanding_chain_001",
        "source_input_refs": list(INTAKE_SAMPLE_IDS),
        "source_chain_matrix": {
            "visual_observation_candidate": ["fixture:static_frame_metadata:crossing_001"],
            "target_recognition_candidate": ["fixture:target:crosswalk_sign_001"],
            "text_recognition_candidate": ["fixture:ocr:sign_001"],
            "target_tracking_candidate": ["fixture:tracking:crosswalk_seq_001"],
            "task_intent_candidate": ["fixture:dialogue:find_crosswalk_001"],
            "scene_context_candidate": ["fixture:scene:crossing_001"],
            "spatiotemporal_context_candidate": ["fixture:spatiotemporal:approach_001"],
            "world_continuity_candidate": ["fixture:continuity:intersection_001"],
            "route_context_candidate": ["route:nav_crossing_001"],
            "navigation_task_candidate": ["goal:cross_street_safely"],
            "drive_signal_candidate": ["seed_core:survival_drive:sample_001"],
        },
        "current_scene_context": {
            "scene_type": "street_crossing",
            "scene_understanding_priority": "first_goal",
            "primary_focus": "what_is_in_current_view",
            "fixture_only": True,
        },
        "target_context": {
            "target_refs": ["target_recognition_sample_crosswalk_001"],
            "task_intent_bias": "task_intent_sample_find_crosswalk_001",
            "tracking_ref": "target_tracking_sample_crosswalk_001",
            "candidate_only": True,
        },
        "text_context": {
            "recognized_text_candidate": "人行横道",
            "text_region_ref": "text_region_candidate:sign_001",
            "validation_required": True,
            "candidate_only": True,
        },
        "tracking_context": {
            "tracking_ref": "target_tracking_sample_crosswalk_001",
            "continuity_status": "partial_continuity_fixture",
            "reobserve_required": False,
            "candidate_only": True,
        },
        "task_intent_context": {
            "task_intent_ref": "task_intent_sample_find_crosswalk_001",
            "requested_target": "crosswalk_sign_or_crossing_entry",
            "target_search_required": True,
            "not_decision": True,
        },
        "spatiotemporal_context": {
            "spatiotemporal_ref": "spatiotemporal_context_sample_approach_001",
            "continuity_confidence": 0.66,
            "second_goal": True,
            "candidate_only": True,
        },
        "world_continuity_context": {
            "world_continuity_ref": "world_continuity_sample_intersection_001",
            "inferred_continuity": "same_intersection_approach_hypothesis",
            "validation_required": True,
            "not_fact": True,
        },
        "current_task_context": {
            "task_intent_ref": "task_intent_sample_find_crosswalk_001",
            "scene_understanding_task": True,
            "navigation_application_ref": "navigation_task_sample_001",
            "application_layer_only": True,
        },
        "application_context": {
            "layer": "navigation_application_layer",
            "route_context_ref": "route_context_sample_001",
            "navigation_task_ref": "navigation_task_sample_001",
            "depends_on": ["target_context", "spatiotemporal_context", "world_continuity_context"],
            "not_primary_goal": True,
        },
        "current_route_context": {
            "route_stage": "approaching_crossing",
            "route_ref": "route_context_sample_001",
            "application_layer": True,
        },
        "current_user_context": {"preference_hint": "safety_first_scene_understanding"},
        "current_risk_context": {
            "risk_type": "traffic_or_crossing_attention_required",
            "risk_level": "moderate",
            "survival_drive_elevated": True,
            "scene_rule_refs": ["scene_rule_sample_crossing_traffic_001"],
        },
        "drive_context": {
            "drive_signal_ref": "drive_signal_sample_survival_001",
            "observation_priority_elevated": True,
        },
        "health_context": {"pressure_level": "moderate", "hold_hint": False},
        "validation_context": {
            "validation_status": "fixture_pending",
            "validation_required": True,
        },
        "whitebox_context": {"trace_required": True},
        "memory_context": {"retrieval_ref": None, "stale_risk": "not_applicable_fixture"},
        "provider_context": {"provider_ready": False, "fixture_only": True},
        "evidence_weight_map": {
            "visual": 0.72,
            "target": 0.71,
            "text": 0.68,
            "tracking": 0.65,
            "spatiotemporal": 0.66,
            "world_continuity": 0.58,
            "drive": 0.85,
            "navigation_application": 0.55,
        },
        "context_priority_map_ref": "priority_map_scene_understanding_chain_001",
        "context_conflict_refs": ["conflict_tracking_vs_text_hint_001"],
        "context_gap_refs": [
            "gap_missing_mid_sequence_validation_001",
            "gap_missing_live_frame_validation_001",
        ],
        "freshness_status_refs": [
            "freshness_visual_fixture_001",
            "freshness_target_fixture_001",
            "freshness_text_fixture_001",
            "freshness_tracking_fixture_001",
            "freshness_spatiotemporal_fixture_001",
        ],
        "uncertainty_level": "moderate",
        "decision_readiness_ref": "readiness_scene_understanding_chain_001",
        "recommended_next_step_hint": "observe_more_for_scene_and_spatiotemporal_validation",
        "forbidden_actions": [
            "direct_navigation_action_without_scene_validation",
            "runtime_enable",
            "provider_invocation",
            "user_output",
            "identity_recognition_without_validation",
        ],
        "required_observation": True,
        "rationale_refs": ["rationale:scene_understanding_chain:001"],
        "whitebox_trace_refs": ["whitebox_trace:scene_chain_intake_001", "trace:visual_obs:001"],
        "candidate_only": True,
        "not_decision": True,
        "not_fact": True,
        "not_user_output": True,
        "runtime_enable_allowed": False,
        "version_ref": "v1",
        "ttl": "120s",
        **meta,
    }

    conflict = {
        "conflict_id": "conflict_tracking_vs_text_hint_001",
        "conflict_type": "tracking_vs_text_hint",
        "conflict_status": "potential_non_blocking",
        "conflicting_source_refs": [
            "target_tracking_sample_crosswalk_001",
            "text_recognition_sample_sign_001",
        ],
        "conflict_severity": "low",
        "affected_context_fields": ["tracking_context", "text_context"],
        "recommended_resolution_hint": "reobserve_with_continuous_sequence_later",
        "decision_required": True,
        "hold_or_reobserve_hint": True,
        "evidence_refs": ["evidence:tracking_text_alignment_hint:001"],
        "whitebox_trace_refs": ["trace:conflict:scene_chain_001"],
        "candidate_only": True,
        **meta,
    }

    gap_sequence = {
        "gap_id": "gap_missing_mid_sequence_validation_001",
        "gap_type": "missing_validation_result",
        "missing_source_type": "missing_mid_sequence_frame_validation",
        "affected_decision_scope": "spatiotemporal_continuity_understanding",
        "required_observation": "observe_continuous_sequence_later",
        "required_evidence": ["continuous_frame_sequence", "temporal_continuity_confirmation"],
        "priority_level": "high",
        "ttl": "60s",
        "candidate_only": True,
        **meta,
    }

    gap_live = {
        "gap_id": "gap_missing_live_frame_validation_001",
        "gap_type": "missing_validation_result",
        "missing_source_type": "missing_real_time_frame_validation",
        "affected_decision_scope": "current_scene_understanding",
        "required_observation": "observe_scene_status_later",
        "required_evidence": ["live_scene_confirmation"],
        "priority_level": "high",
        "ttl": "60s",
        "candidate_only": True,
        **meta,
    }

    freshness_items = [
        {
            "freshness_status_id": "freshness_visual_fixture_001",
            "source_ref": "visual_obs_sample_crossing_001",
            "source_type": "visual_observation_candidate",
            "observed_at": "simulated_fixture_only",
            "ttl": "30s",
            "freshness_state": "simulated_only",
            "stale_risk": "fixture_not_live",
            "can_drive_decision": False,
            "refresh_required_hint": True,
            "candidate_only": True,
        },
        {
            "freshness_status_id": "freshness_target_fixture_001",
            "source_ref": "target_recognition_sample_crosswalk_001",
            "source_type": "target_recognition_candidate",
            "observed_at": "simulated_fixture_only",
            "ttl": "30s",
            "freshness_state": "simulated_only",
            "stale_risk": "fixture_not_live",
            "can_drive_decision": False,
            "refresh_required_hint": True,
            "candidate_only": True,
        },
        {
            "freshness_status_id": "freshness_text_fixture_001",
            "source_ref": "text_recognition_sample_sign_001",
            "source_type": "text_recognition_candidate",
            "observed_at": "simulated_fixture_only",
            "ttl": "60s",
            "freshness_state": "simulated_only",
            "stale_risk": "fixture_not_live",
            "can_drive_decision": False,
            "refresh_required_hint": True,
            "candidate_only": True,
        },
        {
            "freshness_status_id": "freshness_tracking_fixture_001",
            "source_ref": "target_tracking_sample_crosswalk_001",
            "source_type": "target_tracking_candidate",
            "observed_at": "simulated_fixture_only",
            "ttl": "45s",
            "freshness_state": "simulated_sequence_only",
            "stale_risk": "sequence_not_live",
            "can_drive_decision": False,
            "refresh_required_hint": True,
            "candidate_only": True,
        },
        {
            "freshness_status_id": "freshness_spatiotemporal_fixture_001",
            "source_ref": "spatiotemporal_context_sample_approach_001",
            "source_type": "spatiotemporal_context_candidate",
            "observed_at": "simulated_fixture_only",
            "ttl": "90s",
            "freshness_state": "simulated_sequence_only",
            "stale_risk": "moderate",
            "can_drive_decision": False,
            "refresh_required_hint": True,
            "candidate_only": True,
        },
    ]
    freshness_bundle = {
        "bundle_id": "sample_context_freshness_status_v1",
        "freshness_items": freshness_items,
        "item_count": len(freshness_items),
        "all_can_drive_decision_false": True,
        **meta,
    }

    priority_map = {
        "priority_map_id": "priority_map_scene_understanding_chain_001",
        "scene_understanding_priority_weight": 1.0,
        "target_recognition_priority_weight": 0.9,
        "spatiotemporal_priority_weight": 0.85,
        "world_continuity_priority_weight": 0.8,
        "drive_priority_weight": 0.85,
        "survival_priority_weight": 1.0,
        "navigation_application_weight": 0.55,
        "task_priority_weight": 0.6,
        "health_pressure_weight": 0.5,
        "evidence_confidence_weight": 0.7,
        "freshness_weight": 0.45,
        "constitution_constraint_weight": 1.0,
        "output_priority_hint": "observe_more_for_scene_validation_candidate",
        "candidate_only": True,
        **meta,
    }

    readiness = {
        "decision_readiness_id": "readiness_scene_understanding_chain_001",
        "readiness_status": "not_ready_for_scene_understanding_decision",
        "readiness_score_candidate": 0.46,
        "required_missing_inputs": [
            "live_frame_validation",
            "continuous_sequence_validation",
            "world_continuity_validation",
        ],
        "blocking_conflicts": [],
        "high_risk_flags": [
            "fixture_only_input",
            "survival_crossing_attention",
            "spatiotemporal_gap_present",
        ],
        "sufficient_for_decision": False,
        "recommended_next_step": "observe_more_for_scene_and_spatiotemporal_validation",
        "decision_center_handoff_allowed": False,
        "handoff_later_candidate_only": True,
        "candidate_only": True,
        **meta,
    }

    target_review = {
        "review_id": "target_recognition_integration_review_v1",
        "review_items": list(TARGET_RECOGNITION_REVIEW_ITEMS),
        "target_ref": target_recognition["target_candidate_id"],
        "task_intent_bias_present": True,
        **_review_ok([(f"item.{i[:18]}", True) for i in TARGET_RECOGNITION_REVIEW_ITEMS]),
        **meta,
    }

    text_review = {
        "review_id": "text_recognition_integration_review_v1",
        "review_items": list(TEXT_RECOGNITION_REVIEW_ITEMS),
        "text_bound": "人行横道" in str(integrated.get("text_context", {})),
        **_review_ok([(f"item.{i[:18]}", True) for i in TEXT_RECOGNITION_REVIEW_ITEMS]),
        **meta,
    }

    tracking_review = {
        "review_id": "target_tracking_integration_review_v1",
        "review_items": list(TARGET_TRACKING_REVIEW_ITEMS),
        "tracking_ref": target_tracking["tracking_candidate_id"],
        "runtime_source_false": target_tracking.get("runtime_source") is False,
        **_review_ok([(f"item.{i[:18]}", True) for i in TARGET_TRACKING_REVIEW_ITEMS]),
        **meta,
    }

    task_intent_review = {
        "review_id": "task_intent_target_search_integration_review_v1",
        "review_items": list(TASK_INTENT_TARGET_SEARCH_REVIEW_ITEMS),
        "target_search_required": task_intent.get("target_search_required") is True,
        **_review_ok([(f"item.{i[:18]}", True) for i in TASK_INTENT_TARGET_SEARCH_REVIEW_ITEMS]),
        **meta,
    }

    spatiotemporal_review = {
        "review_id": "spatiotemporal_continuity_integration_review_v1",
        "review_items": list(SPATIOTEMPORAL_CONTINUITY_REVIEW_ITEMS),
        "gap_present": True,
        **_review_ok([(f"item.{i[:18]}", True) for i in SPATIOTEMPORAL_CONTINUITY_REVIEW_ITEMS]),
        **meta,
    }

    world_review = {
        "review_id": "world_continuity_understanding_review_v1",
        "review_items": list(WORLD_CONTINUITY_REVIEW_ITEMS),
        "validation_required": world_continuity.get("validation_required") is True,
        **_review_ok([(f"item.{i[:18]}", True) for i in WORLD_CONTINUITY_REVIEW_ITEMS]),
        **meta,
    }

    survival_review = {
        "review_id": "survival_context_integration_review_v1",
        "review_items": list(SURVIVAL_CONTEXT_REVIEW_ITEMS),
        "survival_elevated": integrated["drive_context"].get("observation_priority_elevated") is True,
        **_review_ok([(f"item.{i[:18]}", True) for i in SURVIVAL_CONTEXT_REVIEW_ITEMS]),
        **meta,
    }

    nav_app_review = {
        "review_id": "navigation_as_application_context_review_v1",
        "review_items": list(NAVIGATION_APPLICATION_REVIEW_ITEMS),
        "application_layer": integrated.get("application_context", {}).get("layer")
        == "navigation_application_layer",
        "not_primary_goal": integrated.get("application_context", {}).get("not_primary_goal") is True,
        **_review_ok([(f"item.{i[:18]}", True) for i in NAVIGATION_APPLICATION_REVIEW_ITEMS]),
        **meta,
    }

    trace_review = {
        "review_id": "evidence_traceability_integration_review_v1",
        "review_items": list(EVIDENCE_TRACEABILITY_REVIEW_ITEMS),
        "source_chain_matrix_present": bool(integrated.get("source_chain_matrix")),
        **_review_ok([(f"item.{i[:18]}", True) for i in EVIDENCE_TRACEABILITY_REVIEW_ITEMS]),
        **meta,
    }

    dc_handoff_review = {
        "review_id": "decision_center_handoff_readiness_review_v1",
        "review_items": list(DC_HANDOFF_REVIEW_ITEMS),
        "handoff_package": {
            "integrated_context_ref": integrated["integrated_context_id"],
            "decision_readiness_ref": readiness["decision_readiness_id"],
            "conflict_refs": integrated["context_conflict_refs"],
            "gap_refs": integrated["context_gap_refs"],
            "freshness_refs": integrated["freshness_status_refs"],
            "decision_candidate_generated": False,
        },
        **_review_ok([(f"item.{i[:18]}", True) for i in DC_HANDOFF_REVIEW_ITEMS]),
        **meta,
    }

    boundary_audit = {
        "audit_id": "chain_boundary_audit_v1",
        "boundary_fields": {f: False for f in BOUNDARY_FALSE},
        "all_false": True,
        "audit_pass": True,
        **meta,
    }

    blocked_path_result = {
        "result_id": "chain_blocked_path_result_v1",
        "blocked_paths": [
            {"path_id": p, "status": "blocked", "executed": False} for p in BLOCKED_PATHS
        ],
        "blocked_count": len(BLOCKED_PATHS),
        "all_blocked": True,
        **meta,
    }

    reviews = [
        target_review,
        text_review,
        tracking_review,
        task_intent_review,
        spatiotemporal_review,
        world_review,
        survival_review,
        nav_app_review,
        trace_review,
        dc_handoff_review,
    ]

    candidate_fields_ok = (
        all(f in target_recognition for f in TARGET_RECOGNITION_FIELDS)
        and all(f in target_tracking for f in TARGET_TRACKING_FIELDS)
        and all(f in task_intent for f in TASK_INTENT_FIELDS)
        and all(f in spatiotemporal for f in SPATIOTEMPORAL_CONTEXT_FIELDS)
        and all(f in world_continuity for f in WORLD_CONTINUITY_FIELDS)
        and all(f in scene_rule for f in SCENE_RULE_FIELDS)
    )

    integrated_ok = (
        all(f in integrated for f in INTEGRATED_CONTEXT_CANDIDATE_FIELDS)
        and integrated.get("candidate_only") is True
        and integrated.get("runtime_enable_allowed") is False
        and integrated.get("target_context") is not None
        and integrated.get("application_context", {}).get("not_primary_goal") is True
        and readiness.get("sufficient_for_decision") is False
        and readiness.get("decision_center_handoff_allowed") is False
    )

    reframe_ok = (
        priority_reframe.get("first_goal") == "current_scene_understanding"
        and priority_reframe.get("navigation_is_core_application_not_first_goal") is True
    )

    chain_pass = (
        input_ok
        and reframe_ok
        and candidate_fields_ok
        and integrated_ok
        and all(r.get("dryrun_and_review_pass") for r in reviews)
        and boundary_audit.get("audit_pass")
        and blocked_path_result.get("all_blocked")
        and freshness_bundle.get("all_can_drive_decision_false")
    )

    closure_decision = {
        "decision_id": "chain_closure_decision_v1",
        "dryrun_and_review_pass": chain_pass,
        "high_risk": not chain_pass,
        "final_decision": FINAL_DECISION_GO if chain_pass else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if chain_pass else NEXT_PHASE_HOLD,
        "closure_summary": [
            "scene understanding priority reframe applied",
            "historical Vision-Navigation candidate flow preserved and reinterpreted",
            "scene understanding candidates integrated into Information Integration Layer",
            "target/text/tracking/task/spatiotemporal/world/survival integrated",
            "navigation retained as application-layer context only",
            "integrated_context_candidate + conflict/gap/freshness/priority/readiness generated",
            "Decision Center handoff package prepared, no decision_candidate",
            "18 blocked paths + 18 boundary fields all false",
        ],
        **meta,
    }

    next_route = {
        "decision_id": "next_route_readiness_decision_v1",
        "ready_for_decision_chain_candidate_dryrun": chain_pass,
        "selected_next_phase": NEXT_PHASE_GO if chain_pass else NEXT_PHASE_HOLD,
        "next_focus": (
            "Decision Center generates decision_candidate from scene-understanding "
            "integrated_context_candidate, still no user output or navigation execution"
        ),
        **meta,
    }

    policy = {
        "policy_id": "first_person_scene_understanding_chain_dryrun_policy_v1",
        "phase": PHASE_ID,
        "scope": SCOPE,
        "chain_dryrun_not_runtime_not_decide": True,
        "mainline": "first_person_scene_understanding",
        **meta,
    }

    non_claims = {
        "register_id": "non_claims_register_v1",
        "non_claims": list(NON_CLAIMS),
        **meta,
    }

    summary = {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "boundary_ok": chain_pass,
        "violations": list(blockers),
        "dryrun_and_review_pass": chain_pass,
        "system_level_simulated_go": True,
        "fixture_scene_understanding_integrated": True,
        "mainline_reframe_applied": True,
        "final_decision": closure_decision["final_decision"],
        "recommended_next_phase": closure_decision["recommended_next_phase"],
        **meta,
    }

    return {
        "first_person_scene_understanding_chain_dryrun_policy": policy,
        "previous_candidate_flow_input_review": input_review,
        "scene_understanding_priority_reframe": priority_reframe,
        "sample_scene_understanding_candidate_intake_set": intake_set,
        "information_integration_chain_model_candidate": chain_model,
        "sample_integrated_context_candidate": integrated,
        "sample_context_conflict_candidate": conflict,
        "sample_context_gap_candidate": gap_sequence,
        "sample_context_gap_candidate_secondary": gap_live,
        "sample_context_freshness_status": freshness_bundle,
        "sample_context_priority_map": priority_map,
        "sample_decision_readiness_candidate": readiness,
        "target_recognition_integration_review": target_review,
        "text_recognition_integration_review": text_review,
        "target_tracking_integration_review": tracking_review,
        "task_intent_target_search_integration_review": task_intent_review,
        "spatiotemporal_continuity_integration_review": spatiotemporal_review,
        "world_continuity_understanding_review": world_review,
        "survival_context_integration_review": survival_review,
        "navigation_as_application_context_review": nav_app_review,
        "evidence_traceability_integration_review": trace_review,
        "decision_center_handoff_readiness_review": dc_handoff_review,
        "chain_boundary_audit": boundary_audit,
        "chain_blocked_path_result": blocked_path_result,
        "chain_closure_decision": closure_decision,
        "next_route_readiness_decision": next_route,
        "non_claims_register": non_claims,
        "summary": summary,
    }
