# -*- coding: utf-8 -*-
"""First Person Vision Navigation Candidate Flow Planning v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.luna_constitution_capability_bus_governance_baseline_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as CB_DR_FINAL_GO,
)
from capabilities.governance.midplatform_controlled_runtime_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as CR_DR_FINAL_GO,
)
from capabilities.governance.midplatform_information_integration_layer_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as II_DR_FINAL_GO,
)
from capabilities.governance.midplatform_safety_gate_planning_v1 import FOUR_LAYER_ARCHITECTURE
from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.governance.provider_abstraction_standard_alignment_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as PROVIDER_DR_FINAL_GO,
)
from capabilities.governance.seed_core_drive_signal_contract_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as DS_DR_FINAL_GO,
)
from capabilities.governance.seed_core_pluggable_layer_architecture_planning_v1 import (
    UPSTREAM_RUNTIME_LEAKAGE_FIELDS,
)
from capabilities.governance.vision_ocr_navigation_task_mainline_resume_v1 import (
    FINAL_DECISION_GO as MAINLINE_RESUME_FINAL_GO,
    NEXT_PHASE_GO as MAINLINE_RESUME_NEXT_PHASE,
)

PHASE_ID = "Phase-First-Person-Vision-Navigation-Candidate-Flow-Planning-v1-001"
SCOPE = "first_person_vision_navigation_candidate_flow_planning_only"
SOURCE_CHAIN = "first_person_vision_navigation_candidate_flow_planning_v1"

UPSTREAM_MAINLINE_FINAL = MAINLINE_RESUME_FINAL_GO
UPSTREAM_MAINLINE_NEXT = MAINLINE_RESUME_NEXT_PHASE

FINAL_DECISION_GO = (
    "FIRST_PERSON_VISION_NAVIGATION_CANDIDATE_FLOW_PLANNING_READY_FOR_DRYRUN_AND_REVIEW"
)
FINAL_DECISION_HOLD = "FIRST_PERSON_VISION_NAVIGATION_CANDIDATE_FLOW_PLANNING_HOLD_FOR_ISSUE_REVIEW"
NEXT_PHASE_GO = "Phase-First-Person-Vision-Navigation-Candidate-Flow-DryRunAndReview-v1-001"
NEXT_PHASE_HOLD = "Phase-First-Person-Vision-Navigation-Candidate-Flow-Issue-Review-v1-001"

PERCEPTION_ZONE_CONFIRMATIONS: Tuple[str, ...] = (
    "Perception Zone outputs candidate/evidence/context",
    "does not output fact",
    "does not write Memory / WorldModel",
    "does not generate user output",
    "does not execute navigation action",
    "does not invoke provider/runtime",
    "all outputs must carry source_chain / confidence / ttl / evidence_refs / whitebox_trace_refs",
)

VISUAL_OBSERVATION_FIELDS: Tuple[str, ...] = (
    "visual_observation_candidate_id",
    "source_frame_ref",
    "observation_mode",
    "scene_type_candidate",
    "detected_object_refs",
    "obstacle_refs",
    "risk_refs",
    "spatial_context_refs",
    "confidence",
    "ttl",
    "source_chain",
    "evidence_refs",
    "whitebox_trace_refs",
    "candidate_only",
    "not_fact",
    "runtime_source",
)

VISUAL_EVIDENCE_FIELDS: Tuple[str, ...] = (
    "visual_evidence_candidate_id",
    "source_observation_ref",
    "evidence_type",
    "evidence_payload_ref",
    "confidence",
    "ttl",
    "validation_required",
    "source_chain",
    "whitebox_trace_refs",
    "candidate_only",
)

SCENE_CONTEXT_FIELDS: Tuple[str, ...] = (
    "scene_context_candidate_id",
    "scene_category_candidate",
    "indoor_outdoor_status",
    "mobility_context",
    "public_facility_context",
    "navigation_relevance",
    "risk_relevance",
    "confidence",
    "ttl",
    "candidate_only",
    "not_fact",
)

OBSTACLE_FIELDS: Tuple[str, ...] = (
    "obstacle_candidate_id",
    "obstacle_type_candidate",
    "relative_position",
    "approximate_distance_band",
    "movement_status_candidate",
    "collision_risk_level",
    "confidence",
    "ttl",
    "required_reobserve",
    "candidate_only",
)

RISK_CONTEXT_FIELDS: Tuple[str, ...] = (
    "risk_context_candidate_id",
    "risk_type",
    "risk_level",
    "risk_source_refs",
    "survival_drive_priority_hint",
    "recommended_hold_or_observe_more",
    "forbidden_actions",
    "required_observation",
    "confidence",
    "ttl",
    "candidate_only",
)

OCR_RESULT_FIELDS: Tuple[str, ...] = (
    "ocr_result_candidate_id",
    "source_visual_region_ref",
    "recognized_text_candidate",
    "text_confidence",
    "language_hint",
    "text_region_refs",
    "signage_context_refs",
    "validation_required",
    "ttl",
    "source_chain",
    "evidence_refs",
    "candidate_only",
    "not_fact",
)

TEXT_REGION_FIELDS: Tuple[str, ...] = (
    "text_region_candidate_id",
    "region_ref",
    "region_type_candidate",
    "approximate_position",
    "readability_status",
    "ocr_required",
    "confidence",
    "ttl",
    "candidate_only",
)

SIGNAGE_CONTEXT_FIELDS: Tuple[str, ...] = (
    "signage_context_candidate_id",
    "signage_type_candidate",
    "possible_meaning",
    "navigation_relevance",
    "safety_relevance",
    "confidence",
    "ttl",
    "validation_required",
    "candidate_only",
)

MAP_LOCATION_FIELDS: Tuple[str, ...] = (
    "map_location_context_candidate_id",
    "location_source_type",
    "approximate_location_ref",
    "location_confidence",
    "map_context_refs",
    "route_relevance",
    "stale_risk",
    "ttl",
    "source_chain",
    "candidate_only",
    "not_fact",
)

ROUTE_CONTEXT_FIELDS: Tuple[str, ...] = (
    "route_context_candidate_id",
    "active_route_ref",
    "route_stage_candidate",
    "next_waypoint_candidate",
    "expected_direction_candidate",
    "deviation_risk",
    "route_confidence",
    "ttl",
    "candidate_only",
)

NAVIGATION_TASK_FIELDS: Tuple[str, ...] = (
    "navigation_task_candidate_id",
    "task_goal_ref",
    "task_stage",
    "task_priority",
    "task_progress_candidate",
    "route_context_ref",
    "location_context_ref",
    "required_observation_refs",
    "safety_hold_refs",
    "candidate_only",
    "task_state_commit_allowed",
)

TASK_ROUTE_PROGRESS_FIELDS: Tuple[str, ...] = (
    "progress_candidate_id",
    "navigation_task_ref",
    "route_context_ref",
    "progress_status_candidate",
    "deviation_candidate",
    "next_decision_need",
    "confidence",
    "ttl",
    "candidate_only",
)

REQUIRED_OBSERVATION_FIELDS: Tuple[str, ...] = (
    "required_observation_id",
    "observation_reason",
    "target_zone",
    "required_source_type",
    "priority_level",
    "survival_drive_ref",
    "task_drive_ref",
    "expected_candidate_type",
    "ttl",
    "candidate_only",
)

VISUAL_OCR_MAP_BINDING_CONFIRMATIONS: Tuple[str, ...] = (
    "visual observation can produce OCR region need",
    "OCR result must bind visual region",
    "map location can contextualize visual/route candidates",
    "visual vs map conflict creates context_conflict_candidate later",
    "OCR signage can influence route_context_candidate only as candidate",
    "no binding creates fact by itself",
)

DRIVE_OBSERVATION_PRIORITY_CONFIRMATIONS: Tuple[str, ...] = (
    "Survival Drive risk signal can raise observation priority",
    "Task Drive can raise route/task observation relevance",
    "Resource Governance can reduce observation frequency or detail",
    "Health Management can recommend hold/degrade",
    "Autonomous World Observation can create required_observation_candidate",
    "drive signal cannot invoke camera/provider/runtime",
)

II_HANDOFF_CONFIRMATIONS: Tuple[str, ...] = (
    "all candidates flow to Information Integration Layer",
    "integrated_context_candidate generated later",
    "conflict/gap/freshness handled by Information Integration",
    "Decision Center remains later裁决层",
    "no decision_candidate generated now",
)

TRACEABILITY_FIELDS: Tuple[str, ...] = (
    "source_chain",
    "source_candidate_refs",
    "evidence_refs",
    "validation_required",
    "confidence",
    "ttl",
    "whitebox_trace_refs",
    "provider_candidate_refs",
    "capability_bus_contract_refs",
)

NON_CLAIMS: Tuple[str, ...] = (
    "Candidate Flow Planning GO ≠ camera enabled",
    "visual_observation_candidate planned ≠ real frame read",
    "ocr_result_candidate planned ≠ OCR executed",
    "map_location_context_candidate planned ≠ map provider invoked",
    "navigation_task_candidate planned ≠ navigation task committed",
    "next DryRunAndReview ≠ runtime execution",
)

BOUNDARY_TRUE: Tuple[str, ...] = ("first_person_vision_navigation_candidate_flow_planning_only",)

BOUNDARY_FALSE: Tuple[str, ...] = (
    "camera_invoked_now",
    "real_frame_read_now",
    "vision_runtime_enabled_now",
    "ocr_runtime_enabled_now",
    "map_provider_invoked_now",
    "navigation_runtime_enabled_now",
    "provider_invoked_now",
    "model_runtime_invoked_now",
    "real_ocr_executed_now",
    "real_navigation_action_executed_now",
    "user_output_generated_now",
    "memory_written_now",
    "world_model_written_now",
    "task_state_committed_now",
    "controlled_runtime_enabled_now",
)

DEFAULT_OUTPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "first_person_vision_navigation_candidate_flow_planning"
)


def _planning_meta() -> Dict[str, Any]:
    meta = {
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "source_chain": SOURCE_CHAIN,
        "selected_provider_for_execution": None,
        "four_layer_architecture": FOUR_LAYER_ARCHITECTURE,
        "vision_ocr_map_navigation_runtime_deferred": True,
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


def _contract_doc(
    contract_id: str,
    fields: Tuple[str, ...],
    meta: Dict[str, Any],
    **defaults: Any,
) -> Dict[str, Any]:
    doc = {
        "contract_id": contract_id,
        "required_fields": list(fields),
        "field_count": len(fields),
        "candidate_only": True,
        **meta,
    }
    if defaults:
        doc["defaults"] = defaults
    return doc


def _policy_doc(policy_id: str, confirmations: Tuple[str, ...], meta: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "policy_id": policy_id,
        "confirmations": list(confirmations),
        "confirmation_count": len(confirmations),
        **meta,
    }


def _check_upstream_no_runtime_leakage(summary: Dict[str, Any]) -> List[str]:
    issues: List[str] = []
    for field in UPSTREAM_RUNTIME_LEAKAGE_FIELDS:
        if field in summary and summary.get(field) is not False:
            issues.append(f"{field} must be false")
    return issues


def run_first_person_vision_navigation_candidate_flow_planning_v1(
    *,
    vision_ocr_navigation_task_mainline_resume_root: str,
    luna_constitution_capability_bus_governance_baseline_dryrun_and_review_root: str,
    midplatform_information_integration_layer_dryrun_and_review_root: str,
    seed_core_drive_signal_contract_dryrun_and_review_root: str,
    provider_abstraction_standard_alignment_dryrun_and_review_root: str,
    midplatform_controlled_runtime_dryrun_and_review_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []

    mainline_root = Path(vision_ocr_navigation_task_mainline_resume_root).expanduser().resolve()
    cb_dr_root = Path(
        luna_constitution_capability_bus_governance_baseline_dryrun_and_review_root
    ).expanduser().resolve()
    ii_dr_root = Path(
        midplatform_information_integration_layer_dryrun_and_review_root
    ).expanduser().resolve()
    ds_dr_root = Path(seed_core_drive_signal_contract_dryrun_and_review_root).expanduser().resolve()
    provider_dr_root = Path(
        provider_abstraction_standard_alignment_dryrun_and_review_root
    ).expanduser().resolve()
    cr_dr_root = Path(midplatform_controlled_runtime_dryrun_and_review_root).expanduser().resolve()

    mainline_sm = _try_read_json(mainline_root / "summary.json") or {}
    mainline_vr = _try_read_json(mainline_root / "verifier_report.json") or {}
    cb_dr_vr = _try_read_json(cb_dr_root / "verifier_report.json") or {}
    ii_dr_vr = _try_read_json(ii_dr_root / "verifier_report.json") or {}
    ds_dr_vr = _try_read_json(ds_dr_root / "verifier_report.json") or {}
    provider_dr_vr = _try_read_json(provider_dr_root / "verifier_report.json") or {}
    cr_dr_vr = _try_read_json(cr_dr_root / "verifier_report.json") or {}

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    meta = {
        **_planning_meta(),
        "upstream_mainline_resume_root": str(mainline_root),
        "upstream_constitution_bus_dryrun_root": str(cb_dr_root),
        "upstream_information_integration_dryrun_root": str(ii_dr_root),
        "upstream_drive_signal_dryrun_root": str(ds_dr_root),
        "upstream_provider_abstraction_dryrun_root": str(provider_dr_root),
        "upstream_controlled_runtime_dryrun_root": str(cr_dr_root),
        "output_root": str(out_root),
    }

    if mainline_vr.get("verifier") != "GO":
        blockers.append("Mainline Resume verifier must be GO")
    if mainline_sm.get("final_decision") != UPSTREAM_MAINLINE_FINAL:
        blockers.append("mainline resume final_decision mismatch")
    if mainline_sm.get("recommended_next_phase") != UPSTREAM_MAINLINE_NEXT:
        blockers.append("mainline resume recommended_next_phase mismatch")
    if cb_dr_vr.get("verifier") != "GO":
        blockers.append("Constitution-Bus v1.0 DryRunAndReview must be GO")
    if ii_dr_vr.get("verifier") != "GO":
        blockers.append("Information Integration Layer DryRunAndReview must be GO")
    if ds_dr_vr.get("verifier") != "GO":
        blockers.append("Drive Signal Contract DryRunAndReview must be GO")
    if provider_dr_vr.get("verifier") != "GO":
        blockers.append("Provider Abstraction DryRunAndReview must be GO")
    if cr_dr_vr.get("verifier") != "GO":
        blockers.append("Controlled Runtime DryRunAndReview must be GO")

    leakage_issues: List[str] = []
    for label, sm in (
        ("mainline", mainline_sm),
        ("cb_dr", _try_read_json(cb_dr_root / "summary.json") or {}),
        ("ii_dr", _try_read_json(ii_dr_root / "summary.json") or {}),
        ("ds_dr", _try_read_json(ds_dr_root / "summary.json") or {}),
        ("provider", _try_read_json(provider_dr_root / "summary.json") or {}),
        ("cr_dr", _try_read_json(cr_dr_root / "summary.json") or {}),
    ):
        for issue in _check_upstream_no_runtime_leakage(sm):
            leakage_issues.append(f"{label}:{issue}")
    blockers.extend(leakage_issues)

    input_ok = len(blockers) == 0

    input_review = {
        "review_id": "mainline_resume_input_review_v1",
        "mainline_resume_verifier": mainline_vr.get("verifier"),
        "mainline_resume_final_decision": mainline_sm.get("final_decision"),
        "constitution_bus_verifier": cb_dr_vr.get("verifier"),
        "information_integration_verifier": ii_dr_vr.get("verifier"),
        "drive_signal_verifier": ds_dr_vr.get("verifier"),
        "provider_abstraction_verifier": provider_dr_vr.get("verifier"),
        "controlled_runtime_verifier": cr_dr_vr.get("verifier"),
        "vision_ocr_map_navigation_runtime_deferred": True,
        "no_runtime_leakage_in_upstream": len(leakage_issues) == 0,
        "planning_only": True,
        "review_pass": input_ok,
        "blockers": blockers,
        **meta,
    }

    perception_flow = {
        "definition_id": "perception_zone_candidate_flow_definition_v1",
        "zone": "Perception Zone",
        "output_types": [
            "visual_observation_candidate",
            "visual_evidence_candidate",
            "scene_context_candidate",
            "obstacle_candidate",
            "risk_context_candidate",
            "ocr_result_candidate",
            "text_region_candidate",
            "signage_context_candidate",
            "map_location_context_candidate",
            "route_context_candidate",
            "navigation_task_candidate",
            "task_route_progress_candidate",
            "required_observation_candidate",
        ],
        "output_type_count": 13,
        "confirmations": list(PERCEPTION_ZONE_CONFIRMATIONS),
        "confirmation_count": len(PERCEPTION_ZONE_CONFIRMATIONS),
        **meta,
    }

    visual_observation = _contract_doc(
        "visual_observation_candidate_contract_v1",
        VISUAL_OBSERVATION_FIELDS,
        meta,
        candidate_only=True,
        not_fact=True,
        runtime_source=False,
    )
    visual_evidence = _contract_doc(
        "visual_evidence_candidate_contract_v1",
        VISUAL_EVIDENCE_FIELDS,
        meta,
        validation_required=True,
        candidate_only=True,
    )
    scene_context = _contract_doc(
        "scene_context_candidate_contract_v1",
        SCENE_CONTEXT_FIELDS,
        meta,
        candidate_only=True,
        not_fact=True,
    )
    obstacle = _contract_doc(
        "obstacle_candidate_contract_v1",
        OBSTACLE_FIELDS,
        meta,
        candidate_only=True,
    )
    risk_context = _contract_doc(
        "risk_context_candidate_contract_v1",
        RISK_CONTEXT_FIELDS,
        meta,
        candidate_only=True,
    )
    ocr_result = _contract_doc(
        "ocr_result_candidate_contract_v1",
        OCR_RESULT_FIELDS,
        meta,
        validation_required=True,
        candidate_only=True,
        not_fact=True,
    )
    text_region = _contract_doc("text_region_candidate_contract_v1", TEXT_REGION_FIELDS, meta)
    signage = _contract_doc(
        "signage_context_candidate_contract_v1",
        SIGNAGE_CONTEXT_FIELDS,
        meta,
        validation_required=True,
        candidate_only=True,
    )
    map_location = _contract_doc(
        "map_location_context_candidate_contract_v1",
        MAP_LOCATION_FIELDS,
        meta,
        candidate_only=True,
        not_fact=True,
    )
    route_context = _contract_doc("route_context_candidate_contract_v1", ROUTE_CONTEXT_FIELDS, meta)
    navigation_task = _contract_doc(
        "navigation_task_candidate_contract_v1",
        NAVIGATION_TASK_FIELDS,
        meta,
        candidate_only=True,
        task_state_commit_allowed=False,
    )
    task_progress = _contract_doc(
        "task_route_progress_candidate_contract_v1",
        TASK_ROUTE_PROGRESS_FIELDS,
        meta,
    )
    required_observation = _contract_doc(
        "required_observation_candidate_contract_v1",
        REQUIRED_OBSERVATION_FIELDS,
        meta,
    )

    binding_policy = _policy_doc(
        "visual_ocr_map_candidate_binding_policy_v1",
        VISUAL_OCR_MAP_BINDING_CONFIRMATIONS,
        meta,
    )
    drive_priority = _policy_doc(
        "drive_signal_to_observation_priority_policy_v1",
        DRIVE_OBSERVATION_PRIORITY_CONFIRMATIONS,
        meta,
    )
    handoff_plan = _policy_doc(
        "candidate_to_information_integration_handoff_plan_v1",
        II_HANDOFF_CONFIRMATIONS,
        meta,
    )
    traceability = {
        "policy_id": "candidate_evidence_traceability_policy_v1",
        "required_fields": list(TRACEABILITY_FIELDS),
        "field_count": len(TRACEABILITY_FIELDS),
        "all_candidates_must_preserve": True,
        **meta,
    }

    boundary_matrix = {
        "matrix_id": "candidate_flow_boundary_matrix_v1",
        "boundary_fields": {f: False for f in BOUNDARY_FALSE},
        "all_false": True,
        "boundary_pass": True,
        **meta,
    }

    dryrun_plan = {
        "plan_id": "candidate_flow_dryrun_plan_v1",
        "next_phase": NEXT_PHASE_GO,
        "dryrun_objectives": [
            "generate sample visual_observation_candidate / ocr_result_candidate / map_location_context_candidate / route_context_candidate / navigation_task_candidate",
            "verify candidate flow completeness",
            "verify candidates do not become fact / action / output",
            "verify drive_signal affects observation priority only",
            "verify Information Integration handoff",
            "no real camera/OCR/map/navigation runtime",
        ],
        **meta,
    }

    contracts_ok = (
        len(VISUAL_OBSERVATION_FIELDS) >= 16
        and len(OCR_RESULT_FIELDS) >= 13
        and len(NAVIGATION_TASK_FIELDS) >= 11
        and len(PERCEPTION_ZONE_CONFIRMATIONS) == 7
    )
    planning_pass = input_ok and contracts_ok

    planning_decision = {
        "decision_id": "first_person_vision_navigation_candidate_flow_planning_decision_v1",
        "planning_pass": planning_pass,
        "high_risk": not planning_pass,
        "final_decision": FINAL_DECISION_GO if planning_pass else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if planning_pass else NEXT_PHASE_HOLD,
        "architecture_summary": [
            "Perception Zone candidate flow defined for first-person vision/OCR/map/navigation",
            "13 candidate contracts for visual/OCR/map/route/task/observation chain",
            "candidates flow to Information Integration Layer as evidence/context only",
            "drive signal affects observation priority, not camera/provider/runtime",
            "no camera/OCR/map/navigation runtime in this planning phase",
        ],
        **meta,
    }

    policy = {
        "policy_id": "first_person_vision_navigation_candidate_flow_policy_v1",
        "phase": PHASE_ID,
        "scope": SCOPE,
        "zone": "Perception Zone",
        "candidate_contract_count": 13,
        "planning_not_runtime_not_execute": True,
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
        "boundary_ok": planning_pass,
        "violations": list(blockers),
        "planning_pass": planning_pass,
        "final_decision": planning_decision["final_decision"],
        "recommended_next_phase": planning_decision["recommended_next_phase"],
        **meta,
    }

    return {
        "first_person_vision_navigation_candidate_flow_policy": policy,
        "mainline_resume_input_review": input_review,
        "perception_zone_candidate_flow_definition": perception_flow,
        "visual_observation_candidate_contract": visual_observation,
        "visual_evidence_candidate_contract": visual_evidence,
        "scene_context_candidate_contract": scene_context,
        "obstacle_candidate_contract": obstacle,
        "risk_context_candidate_contract": risk_context,
        "ocr_result_candidate_contract": ocr_result,
        "text_region_candidate_contract": text_region,
        "signage_context_candidate_contract": signage,
        "map_location_context_candidate_contract": map_location,
        "route_context_candidate_contract": route_context,
        "navigation_task_candidate_contract": navigation_task,
        "task_route_progress_candidate_contract": task_progress,
        "required_observation_candidate_contract": required_observation,
        "visual_ocr_map_candidate_binding_policy": binding_policy,
        "drive_signal_to_observation_priority_policy": drive_priority,
        "candidate_to_information_integration_handoff_plan": handoff_plan,
        "candidate_evidence_traceability_policy": traceability,
        "candidate_flow_boundary_matrix": boundary_matrix,
        "candidate_flow_dryrun_plan": dryrun_plan,
        "non_claims_register": non_claims,
        "first_person_vision_navigation_candidate_flow_planning_decision": planning_decision,
        "summary": summary,
    }
