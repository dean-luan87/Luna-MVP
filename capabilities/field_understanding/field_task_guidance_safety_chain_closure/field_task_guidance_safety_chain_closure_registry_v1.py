# -*- coding: utf-8 -*-
"""Field Task Guidance Safety Chain Closure — registry v1."""

from __future__ import annotations

from typing import Any, Dict, List, Tuple

from capabilities.field_understanding.field_task_guidance_safety_chain_closure.field_task_guidance_safety_chain_closure_types_v1 import (
    ACTION_SAFETY_ENTRYPOINT,
    CLOSED_CHAIN_STAGE_REFS,
    CLOSURE_GOVERNANCE_RULES,
    FIELD_SYNTHESIS_ENTRYPOINT,
    FINAL_DECISION_CLOSURE_GO,
    GUIDANCE_ENTRYPOINT,
    INTERFACE_LAYER_PROTOCOL_REF,
    MASTER_CHAIN_PIPELINE,
    MODEL_ADMISSION_STANDARD_REF,
    PHASE_ID,
    PLANNING_OBJECT_TYPES,
    SCENARIO_COVERAGE_REFS,
    SEALED_UPSTREAM_PHASE_REFS,
    SOURCE_CHAIN,
    SPEECH_GATE_ENTRYPOINT,
    TASK_MANAGER_ENTRYPOINT,
    ClosedChainCapabilityCoverage,
    ClosedChainGovernanceCoverage,
    ClosedChainScenarioCoverage,
    ClosedChainStageRef,
    FieldTaskGuidanceSafetyChainClosure,
    FieldTaskGuidanceSafetyClosureDecision,
    candidate_to_dict,
)

REGISTRY_ID = "field_task_guidance_safety_chain_closure_registry_v1"
CLOSURE_REF = "field_task_guidance_safety_chain_closure_v1"

REGISTRY: Dict[str, Tuple[str, ...]] = {
    "planning_object_types": PLANNING_OBJECT_TYPES,
    "closed_chain_stage_refs": CLOSED_CHAIN_STAGE_REFS,
    "scenario_coverage_refs": SCENARIO_COVERAGE_REFS,
    "closure_governance_rules": CLOSURE_GOVERNANCE_RULES,
    "master_chain_pipeline": MASTER_CHAIN_PIPELINE,
    "sealed_upstream_phase_refs": SEALED_UPSTREAM_PHASE_REFS,
}

_UPSTREAM_GO_ARTIFACTS: Tuple[Dict[str, Any], ...] = (
    {
        "phase_ref": "Phase-SLAM-Spatial-Evidence-Chain-Field-Alignment-Closure-v1-001",
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
        "phase_ref": "Phase-Field-Map-Place-Realtime-Event-Overlay-Alignment-v1-001",
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
        "phase_ref": "Phase-Field-Synthesis-Map-Place-Realtime-Event-Overlay-DryRun-v1-001",
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
        "phase_ref": "Phase-Field-To-Task-Alignment-DryRun-v1-001",
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
        "phase_ref": "Phase-Task-To-Guidance-Safety-Gate-DryRun-v1-001",
        "artifact_rel": (
            "_tmp_eval_out/task_to_guidance_safety_gate_dryrun_v1_smoke_v0/"
            "task_to_guidance_safety_gate_dryrun_run_and_review_v1.json"
        ),
        "expected_go": "TASK_TO_GUIDANCE_SAFETY_GATE_DRYRUN_GO",
        "module_rel": (
            "capabilities/field_understanding/task_to_guidance_safety_gate_dryrun/"
            "task_to_guidance_safety_gate_dryrun_types_v1.py"
        ),
        "require_go": True,
    },
    {
        "phase_ref": "Phase-Spatial-Odometry-Fusion-Interface-GPS-SLAM-Planning-v1-001",
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
        "phase_ref": "Phase-Midplatform-Task-Manager-Controlled-Skeleton-Implementation-DryRun-v1-001",
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
        "phase_ref": "Phase-Midplatform-Interface-Layer-Governance-Protocol-v1-001",
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
    {
        "phase_ref": MODEL_ADMISSION_STANDARD_REF,
        "artifact_rel": (
            "_tmp_eval_out/model_admission_governance_v1_smoke_v0/"
            "model_admission_governance_run_and_review_v1.json"
        ),
        "expected_go": "MODEL_ADMISSION_GOVERNANCE_STANDARD_REVIEW_GO",
        "module_rel": (
            "capabilities/midplatform/model_admission_governance/"
            "model_admission_governance_types_v1.py"
        ),
        "require_go": True,
    },
)

_SCENARIO_MAP: Tuple[Dict[str, str], ...] = (
    {
        "scenario_ref": "mall_find_entrance_chain_closed",
        "field_synthesis_case_ref": "mall_stable_map_place_with_slam",
        "field_to_task_case_ref": "mall_find_entrance_task",
        "task_to_guidance_case_ref": "mall_find_entrance_guidance_candidate",
    },
    {
        "scenario_ref": "subway_enter_station_chain_closed",
        "field_synthesis_case_ref": "subway_station_indoor_gps_degraded",
        "field_to_task_case_ref": "subway_station_enter_station_task",
        "task_to_guidance_case_ref": "subway_enter_station_guidance_candidate",
    },
    {
        "scenario_ref": "stadium_concert_ticket_gate_chain_closed",
        "field_synthesis_case_ref": "stadium_concert_event_overlay",
        "field_to_task_case_ref": "stadium_concert_ticket_check_task",
        "task_to_guidance_case_ref": "stadium_concert_ticket_gate_guidance_candidate",
    },
    {
        "scenario_ref": "plaza_market_crowd_chain_closed",
        "field_synthesis_case_ref": "plaza_temporary_market_realtime_overlay",
        "field_to_task_case_ref": "plaza_temporary_market_find_stall_task",
        "task_to_guidance_case_ref": "plaza_market_crowd_safety_guidance_candidate",
    },
    {
        "scenario_ref": "gps_slam_conflict_chain_closed",
        "field_synthesis_case_ref": "gps_slam_map_place_conflict",
        "field_to_task_case_ref": "gps_slam_conflict_delay_navigation_task",
        "task_to_guidance_case_ref": "gps_slam_conflict_guidance_blocked",
    },
    {
        "scenario_ref": "home_return_chain_closed",
        "field_synthesis_case_ref": "home_return_embedded_in_field_to_task",
        "field_to_task_case_ref": "home_return_task_stable_field",
        "task_to_guidance_case_ref": "home_return_stable_guidance_candidate",
    },
)


def is_registered(domain: str, value: str) -> bool:
    return value in REGISTRY.get(domain, ())


def validate_registry() -> Tuple[bool, List[str]]:
    issues: List[str] = []
    if len(PLANNING_OBJECT_TYPES) != 6:
        issues.append("planning_object_types_count_not_6")
    if len(CLOSED_CHAIN_STAGE_REFS) != 6:
        issues.append("closed_chain_stage_refs_count_not_6")
    if len(SCENARIO_COVERAGE_REFS) != 6:
        issues.append("scenario_coverage_refs_count_not_6")
    if len(SEALED_UPSTREAM_PHASE_REFS) != 9:
        issues.append("sealed_upstream_phase_refs_count_not_9")
    if len(CLOSURE_GOVERNANCE_RULES) != 14:
        issues.append("closure_governance_rules_count_not_14")
    return len(issues) == 0, issues


def build_closed_chain_stages_v1() -> Tuple[ClosedChainStageRef, ...]:
    return (
        ClosedChainStageRef(
            stage_ref="spatial_evidence_ingest_chain",
            stage_zh="SLAM 空间证据 ingest → generic_json_spatial_trace → fusion",
            coverage_items=(
                "generic_json_spatial_trace",
                "pose",
                "motion",
                "health",
                "anchor",
                "relocalization",
                "drift",
                "gps_gnss_stub",
                "spatial_odometry_fusion_candidate",
            ),
            upstream_phase_refs=(
                "Phase-SLAM-Spatial-Evidence-Chain-Field-Alignment-Closure-v1-001",
                "Phase-Spatial-Odometry-Fusion-Interface-GPS-SLAM-Planning-v1-001",
            ),
            chain_closed=True,
        ),
        ClosedChainStageRef(
            stage_ref="field_alignment_chain",
            stage_zh="Field 协议对齐：map_place + context + event + spatial binding",
            coverage_items=(
                "map_place_ref",
                "realtime_context_overlay",
                "event_overlay",
                "spatial_evidence_binding",
                "field_interaction_label",
                "field_conflict_candidate",
            ),
            upstream_phase_refs=(
                "Phase-Field-Map-Place-Realtime-Event-Overlay-Alignment-v1-001",
            ),
            chain_closed=True,
        ),
        ClosedChainStageRef(
            stage_ref="field_synthesis_chain",
            stage_zh="Field Synthesis dry-run：6 典型场合成",
            coverage_items=(
                "stable_map_place_field",
                "indoor_gps_degraded_field",
                "event_overlay_field",
                "realtime_context_field",
                "gps_slam_conflict_field",
                "home_return_stable_field",
            ),
            upstream_phase_refs=(
                "Phase-Field-Synthesis-Map-Place-Realtime-Event-Overlay-DryRun-v1-001",
            ),
            chain_closed=True,
        ),
        ClosedChainStageRef(
            stage_ref="field_to_task_chain",
            stage_zh="Field → Task 对齐 dry-run",
            coverage_items=(
                "TaskContextCandidate",
                "TaskEvidenceNeedCandidate",
                "TaskRouteHintCandidate",
                "TaskRiskCandidate",
                "conflict_blocks_route_hint",
            ),
            upstream_phase_refs=("Phase-Field-To-Task-Alignment-DryRun-v1-001",),
            chain_closed=True,
        ),
        ClosedChainStageRef(
            stage_ref="task_to_guidance_chain",
            stage_zh="Task → Guidance / Speech Gate / Action Safety",
            coverage_items=(
                "GuidanceEvidenceRequestCandidate",
                "GuidanceCandidate",
                "SpeechGateCandidate",
                "ActionSafetyCandidate",
                "high_risk_guidance_downgrade",
                "gps_slam_conflict_guidance_blocked",
            ),
            upstream_phase_refs=("Phase-Task-To-Guidance-Safety-Gate-DryRun-v1-001",),
            chain_closed=True,
        ),
        ClosedChainStageRef(
            stage_ref="governance_and_safety_chain",
            stage_zh="治理与安全边界：candidate-only + 无 runtime",
            coverage_items=(
                "candidate_only_enforced",
                "no_direct_action",
                "no_direct_speech_tts",
                "no_direct_fact_write",
                "no_real_navigation_runtime",
                "no_live_sensor_connection",
                "source_chain_preserved",
                "action_safety_candidate_required",
            ),
            upstream_phase_refs=(
                "Phase-Midplatform-Interface-Layer-Governance-Protocol-v1-001",
                MODEL_ADMISSION_STANDARD_REF,
                "Phase-Midplatform-Task-Manager-Controlled-Skeleton-Implementation-DryRun-v1-001",
            ),
            chain_closed=True,
        ),
    )


def build_capability_coverage_v1() -> ClosedChainCapabilityCoverage:
    return ClosedChainCapabilityCoverage(
        coverage_ref="closed_chain_capability_coverage_v1",
        pose_supported=True,
        motion_supported=True,
        health_supported=True,
        anchor_supported=True,
        relocalization_supported=True,
        drift_supported=True,
        spatial_odometry_fusion_supported=True,
        field_conflict_candidate_supported=True,
        field_candidate_supported=True,
        task_context_candidate_supported=True,
        task_evidence_need_candidate_supported=True,
        task_route_hint_candidate_supported=True,
        task_risk_candidate_supported=True,
        guidance_candidate_supported=True,
        speech_gate_candidate_supported=True,
        action_safety_candidate_supported=True,
    )


def build_governance_coverage_v1() -> ClosedChainGovernanceCoverage:
    return ClosedChainGovernanceCoverage(
        coverage_ref="closed_chain_governance_coverage_v1",
        candidate_only_enforced=True,
        source_chain_preserved=True,
        gps_does_not_override_field_identity=True,
        slam_does_not_override_field_identity=True,
        event_overlay_does_not_rewrite_map_place=True,
        field_interaction_label_separated=True,
        task_route_hint_not_action=True,
        guidance_candidate_not_runtime_navigation=True,
        speech_gate_candidate_not_tts=True,
        action_safety_candidate_required=True,
        gps_slam_conflict_blocks_action_like_guidance=True,
    )


def build_scenario_coverage_v1() -> Tuple[ClosedChainScenarioCoverage, ...]:
    return tuple(
        ClosedChainScenarioCoverage(
            scenario_ref=entry["scenario_ref"],
            field_synthesis_case_ref=entry["field_synthesis_case_ref"],
            field_to_task_case_ref=entry["field_to_task_case_ref"],
            task_to_guidance_case_ref=entry["task_to_guidance_case_ref"],
            chain_closed=True,
        )
        for entry in _SCENARIO_MAP
    )


def build_field_task_guidance_safety_chain_closure_matrix_v1() -> Dict[str, Any]:
    stages = build_closed_chain_stages_v1()
    capability = build_capability_coverage_v1()
    governance = build_governance_coverage_v1()
    scenarios = build_scenario_coverage_v1()

    closure = FieldTaskGuidanceSafetyChainClosure(
        closure_ref=CLOSURE_REF,
        phase_id=PHASE_ID,
        master_chain_pipeline=MASTER_CHAIN_PIPELINE,
        closed_chain_stage_refs=CLOSED_CHAIN_STAGE_REFS,
        sealed_upstream_phase_refs=SEALED_UPSTREAM_PHASE_REFS,
        field_synthesis_entrypoint=FIELD_SYNTHESIS_ENTRYPOINT,
        task_manager_entrypoint=TASK_MANAGER_ENTRYPOINT,
        guidance_entrypoint=GUIDANCE_ENTRYPOINT,
        speech_gate_entrypoint=SPEECH_GATE_ENTRYPOINT,
        action_safety_entrypoint=ACTION_SAFETY_ENTRYPOINT,
        interface_layer_protocol_ref=INTERFACE_LAYER_PROTOCOL_REF,
        governance_rules=CLOSURE_GOVERNANCE_RULES,
    )

    decision = FieldTaskGuidanceSafetyClosureDecision(
        decision_ref="field_task_guidance_safety_closure_decision_v1",
        closure_ref=CLOSURE_REF,
        closed_stage_count=len(stages),
        sealed_upstream_phases_verified=True,
        scenario_coverage_count=len(scenarios),
        final_decision=FINAL_DECISION_CLOSURE_GO,
    )

    return {
        "registry_id": REGISTRY_ID,
        "source_chain": SOURCE_CHAIN,
        "field_task_guidance_safety_chain_closure": candidate_to_dict(closure),
        "closed_chain_stages": [candidate_to_dict(s) for s in stages],
        "capability_coverage": candidate_to_dict(capability),
        "governance_coverage": candidate_to_dict(governance),
        "scenario_coverage": [candidate_to_dict(s) for s in scenarios],
        "closure_governance_rules": list(CLOSURE_GOVERNANCE_RULES),
        "master_chain_pipeline": list(MASTER_CHAIN_PIPELINE),
        "sealed_upstream_go_artifacts": list(_UPSTREAM_GO_ARTIFACTS),
        "scenario_case_map": list(_SCENARIO_MAP),
        "closure_decision": candidate_to_dict(decision),
    }
