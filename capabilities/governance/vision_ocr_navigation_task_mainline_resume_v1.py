# -*- coding: utf-8 -*-
"""Vision OCR Navigation Task Mainline Resume Planning v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.luna_constitution_capability_bus_governance_baseline_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as CB_DR_FINAL_GO,
    NEXT_PHASE_GO as CB_DR_NEXT_PHASE,
)
from capabilities.governance.luna_constitution_capability_bus_governance_baseline_planning_v1 import (
    HEALTH_OVERSIGHT_PRINCIPLE,
    UPSTREAM_RUNTIME_LEAKAGE_FIELDS,
)
from capabilities.governance.midplatform_cognitive_zoning_architecture_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as CZ_DR_FINAL_GO,
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
from capabilities.governance.seed_core_pluggable_layer_architecture_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as SC_DR_FINAL_GO,
)

PHASE_ID = "Phase-Vision-OCR-Navigation-Task-Mainline-Resume-v1-001"
SCOPE = "vision_ocr_navigation_task_mainline_resume_planning_only"
SOURCE_CHAIN = "vision_ocr_navigation_task_mainline_resume_v1"

UPSTREAM_CB_DR_FINAL = CB_DR_FINAL_GO
UPSTREAM_CB_DR_NEXT = CB_DR_NEXT_PHASE

FINAL_DECISION_GO = (
    "VISION_OCR_NAVIGATION_TASK_MAINLINE_RESUME_READY_FOR_FIRST_PERSON_VISION_NAVIGATION_CANDIDATE_FLOW_PLANNING"
)
FINAL_DECISION_HOLD = "VISION_OCR_NAVIGATION_TASK_MAINLINE_RESUME_HOLD_FOR_ISSUE_REVIEW"
NEXT_PHASE_GO = "Phase-First-Person-Vision-Navigation-Candidate-Flow-Planning-v1-001"
NEXT_PHASE_HOLD = "Phase-Vision-OCR-Navigation-Task-Mainline-Issue-Review-v1-001"

MAINLINE_RESUME_CONFIRMATIONS: Tuple[str, ...] = (
    "本阶段恢复主线，不执行 runtime",
    "第一视角视觉 / OCR / 导航 / 任务链重新接入 Luna 2.0 架构",
    "视觉/OCR/地图/导航均作为 Pluggable Capability Modules",
    "所有模块必须通过 Constitution-Bus Governance v1.0 传递合同与治理约束",
    "感知输出为 candidate/evidence，不是 fact",
    "导航输出为 task/navigation candidate，不是实际行动",
    "用户输出仍需 Output / Safety / Speech / Display Gate later",
    "runtime 仍受 Controlled Runtime 约束",
)

FIRST_PERSON_VISION_ITEMS: Tuple[str, ...] = (
    "visual_observation_candidate",
    "visual_evidence_candidate",
    "scene_context_candidate",
    "obstacle_candidate",
    "risk_context_candidate",
    "observation_priority from Seed Core / Survival Drive",
    "provider abstraction required if vision provider-backed",
    "no camera/runtime invocation now",
)

OCR_CHAIN_ITEMS: Tuple[str, ...] = (
    "ocr_result_candidate",
    "text_region_candidate",
    "signage_context_candidate",
    "readable_region_candidate",
    "ocr_evidence_candidate",
    "provider readiness later required",
    "no OCR execution now",
    "OCR output not fact by default",
)

NAVIGATION_TASK_ITEMS: Tuple[str, ...] = (
    "navigation_task_candidate",
    "route_context_candidate",
    "location_context_candidate",
    "deviation_candidate",
    "next_action_candidate",
    "safety_hold_candidate",
    "task_progress_candidate",
    "no real navigation action now",
)

CAPABILITY_BUS_BINDING_CONFIRMATIONS: Tuple[str, ...] = (
    "Vision / OCR / Map / Navigation modules must register later through Capability Bus",
    "each module declares module_id / capability_domain / input_contract / output_contract",
    "provider-backed modules bind Provider Abstraction",
    "runtime-capable modules bind Controlled Runtime",
    "health_status_ref transported by Bus only",
    "Bus does not judge health",
    "Health Management remains external oversight",
)

DRIVE_SIGNAL_BINDING_CONFIRMATIONS: Tuple[str, ...] = (
    "Survival Drive can elevate environmental risk",
    "Task Drive can elevate navigation task relevance",
    "Resource Governance can recommend degraded observation / low-power mode",
    "Health Management can recommend hold/degrade through health signal",
    "Autonomous World Observation can request observation_intent_candidate",
    "Emotion Engine and Evolutionary Recursion remain candidate-only and non-runtime",
    "drive signals cannot directly execute navigation",
)

II_BINDING_CONFIRMATIONS: Tuple[str, ...] = (
    "Information Integration consumes visual/OCR/map/task/drive/health/whitebox/provider candidates",
    "emits integrated_context_candidate",
    "flags conflicts/gaps/freshness/priority",
    "does not make final decision",
    "does not invoke provider",
    "does not write Memory/WorldModel",
)

DECISION_CENTER_BINDING_CONFIRMATIONS: Tuple[str, ...] = (
    "Decision Center consumes integrated_context_candidate later",
    "decides hold / observe_more / ask_user / allow_task_response_candidate / block",
    "Decision Center does not invoke provider directly",
    "Decision Center does not bypass gates",
    "navigation action requires Controlled Runtime later",
)

RUNTIME_DEFERMENT_ITEMS: Tuple[str, ...] = (
    "Vision runtime deferred",
    "OCR runtime deferred",
    "Map provider runtime deferred",
    "Navigation action runtime deferred",
    "real frame read deferred",
    "real OCR execution deferred",
    "real navigation output deferred",
    "all future runtime requires admission / authorization / execution window / evidence / rollback / post-review",
)

CANDIDATE_FLOW_STEPS: Tuple[str, ...] = (
    "Perception Zone",
    "visual_observation_candidate / ocr_result_candidate / map_location_context_candidate",
    "Information Integration",
    "integrated_context_candidate",
    "Decision Center",
    "task_response_candidate later",
    "Output/Gate chain later",
)

EVIDENCE_FLOW_ITEMS: Tuple[str, ...] = (
    "visual_evidence_candidate",
    "ocr_evidence_candidate",
    "map_evidence_candidate",
    "task_evidence_candidate",
    "validation_result_candidate",
    "whitebox_trace_refs",
    "evidence does not become fact by default",
)

TASK_ROUTE_FLOW_ITEMS: Tuple[str, ...] = (
    "user_task_context",
    "active_route_context",
    "route_progress_candidate",
    "deviation_candidate",
    "location_confidence",
    "route_risk_candidate",
    "required_observation",
    "next_decision_need",
)

SAFETY_PRIORITY_CONFIRMATIONS: Tuple[str, ...] = (
    "Survival safety priority > task progress",
    "traffic / obstacle / fall / collision / lost-context risk can trigger hold/observe_more",
    "task preference cannot override safety",
    "user preference cannot override safety",
    "emergency risk can elevate observation priority",
    "no direct user output without gates",
)

NON_CLAIMS: Tuple[str, ...] = (
    "Mainline Resume GO ≠ Vision/OCR/Map runtime enabled",
    "candidate flow planned ≠ real camera/OCR/navigation execution",
    "Capability Bus binding planned ≠ modules registered",
    "Decision binding planned ≠ navigation decision executed",
    "next Candidate Flow Planning ≠ runtime execution",
)

BOUNDARY_TRUE: Tuple[str, ...] = ("vision_ocr_navigation_task_mainline_resume_planning_only",)

BOUNDARY_FALSE: Tuple[str, ...] = (
    "vision_runtime_enabled_now",
    "ocr_runtime_enabled_now",
    "map_provider_invoked_now",
    "navigation_runtime_enabled_now",
    "provider_invoked_now",
    "model_runtime_invoked_now",
    "camera_invoked_now",
    "real_frame_read_now",
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
    "vision_ocr_navigation_task_mainline_resume"
)


def _planning_meta() -> Dict[str, Any]:
    meta = {
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "source_chain": SOURCE_CHAIN,
        "selected_provider_for_execution": None,
        "four_layer_architecture": FOUR_LAYER_ARCHITECTURE,
        "luna_2_0_governance_baseline_closed": True,
        "constitution_bus_v1_0_validated": True,
        "health_oversight_external_to_bus": True,
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


def _policy_doc(
    policy_id: str,
    confirmations: Tuple[str, ...],
    meta: Dict[str, Any],
    **extra: Any,
) -> Dict[str, Any]:
    doc = {
        "policy_id": policy_id,
        "confirmations": list(confirmations),
        "confirmation_count": len(confirmations),
        **meta,
    }
    doc.update(extra)
    return doc


def _check_upstream_no_runtime_leakage(summary: Dict[str, Any]) -> List[str]:
    issues: List[str] = []
    for field in UPSTREAM_RUNTIME_LEAKAGE_FIELDS:
        if field in summary and summary.get(field) is not False:
            issues.append(f"{field} must be false")
    return issues


def run_vision_ocr_navigation_task_mainline_resume_v1(
    *,
    luna_constitution_capability_bus_governance_baseline_dryrun_and_review_root: str,
    midplatform_information_integration_layer_dryrun_and_review_root: str,
    seed_core_drive_signal_contract_dryrun_and_review_root: str,
    seed_core_pluggable_layer_architecture_dryrun_and_review_root: str,
    midplatform_cognitive_zoning_architecture_dryrun_and_review_root: str,
    provider_abstraction_standard_alignment_dryrun_and_review_root: str,
    midplatform_controlled_runtime_dryrun_and_review_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []

    cb_dr_root = Path(
        luna_constitution_capability_bus_governance_baseline_dryrun_and_review_root
    ).expanduser().resolve()
    ii_dr_root = Path(
        midplatform_information_integration_layer_dryrun_and_review_root
    ).expanduser().resolve()
    ds_dr_root = Path(seed_core_drive_signal_contract_dryrun_and_review_root).expanduser().resolve()
    sc_dr_root = Path(seed_core_pluggable_layer_architecture_dryrun_and_review_root).expanduser().resolve()
    cz_dr_root = Path(midplatform_cognitive_zoning_architecture_dryrun_and_review_root).expanduser().resolve()
    provider_dr_root = Path(
        provider_abstraction_standard_alignment_dryrun_and_review_root
    ).expanduser().resolve()
    cr_dr_root = Path(midplatform_controlled_runtime_dryrun_and_review_root).expanduser().resolve()

    cb_dr_sm = _try_read_json(cb_dr_root / "summary.json") or {}
    cb_dr_vr = _try_read_json(cb_dr_root / "verifier_report.json") or {}
    ii_dr_vr = _try_read_json(ii_dr_root / "verifier_report.json") or {}
    ds_dr_vr = _try_read_json(ds_dr_root / "verifier_report.json") or {}
    sc_dr_vr = _try_read_json(sc_dr_root / "verifier_report.json") or {}
    cz_dr_vr = _try_read_json(cz_dr_root / "verifier_report.json") or {}
    provider_dr_vr = _try_read_json(provider_dr_root / "verifier_report.json") or {}
    cr_dr_vr = _try_read_json(cr_dr_root / "verifier_report.json") or {}

    plan_root = cb_dr_root.parent / "luna_constitution_capability_bus_governance_baseline_planning"
    health_policy = _try_read_json(plan_root / "constitution_bus_external_health_oversight_policy_v1.json") or {}

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    meta = {
        **_planning_meta(),
        "upstream_constitution_bus_dryrun_root": str(cb_dr_root),
        "upstream_information_integration_dryrun_root": str(ii_dr_root),
        "upstream_drive_signal_dryrun_root": str(ds_dr_root),
        "upstream_seed_core_pluggable_dryrun_root": str(sc_dr_root),
        "upstream_cognitive_zoning_dryrun_root": str(cz_dr_root),
        "upstream_provider_abstraction_dryrun_root": str(provider_dr_root),
        "upstream_controlled_runtime_dryrun_root": str(cr_dr_root),
        "output_root": str(out_root),
    }

    if cb_dr_vr.get("verifier") != "GO":
        blockers.append("Constitution-Bus Governance Baseline DryRunAndReview must be GO")
    if cb_dr_sm.get("final_decision") != UPSTREAM_CB_DR_FINAL:
        blockers.append("constitution bus dryrun final_decision mismatch")
    if cb_dr_sm.get("recommended_next_phase") != UPSTREAM_CB_DR_NEXT:
        blockers.append("constitution bus dryrun recommended_next_phase mismatch")
    if ii_dr_vr.get("verifier") != "GO":
        blockers.append("Information Integration Layer DryRunAndReview must be GO")
    if ds_dr_vr.get("verifier") != "GO":
        blockers.append("Drive Signal Contract DryRunAndReview must be GO")
    if sc_dr_vr.get("verifier") != "GO":
        blockers.append("Seed Core / Pluggable DryRunAndReview must be GO")
    if cz_dr_vr.get("verifier") != "GO":
        blockers.append("Cognitive Zoning DryRunAndReview must be GO")
    if provider_dr_vr.get("verifier") != "GO":
        blockers.append("Provider Abstraction DryRunAndReview must be GO")
    if cr_dr_vr.get("verifier") != "GO":
        blockers.append("Controlled Runtime DryRunAndReview must be GO")
    if health_policy.get("principle") != HEALTH_OVERSIGHT_PRINCIPLE:
        blockers.append("Health Oversight Is External to Constitution-Bus must be written")

    leakage_issues: List[str] = []
    for label, sm in (
        ("cb_dr", cb_dr_sm),
        ("ii_dr", _try_read_json(ii_dr_root / "summary.json") or {}),
        ("ds_dr", _try_read_json(ds_dr_root / "summary.json") or {}),
        ("sc_dr", _try_read_json(sc_dr_root / "summary.json") or {}),
        ("cz_dr", _try_read_json(cz_dr_root / "summary.json") or {}),
        ("provider", _try_read_json(provider_dr_root / "summary.json") or {}),
        ("cr_dr", _try_read_json(cr_dr_root / "summary.json") or {}),
    ):
        for issue in _check_upstream_no_runtime_leakage(sm):
            leakage_issues.append(f"{label}:{issue}")
    blockers.extend(leakage_issues)

    input_ok = len(blockers) == 0

    input_review = {
        "review_id": "constitution_bus_governance_input_review_v1",
        "constitution_bus_dryrun_verifier": cb_dr_vr.get("verifier"),
        "constitution_bus_dryrun_final_decision": cb_dr_sm.get("final_decision"),
        "information_integration_dryrun_verifier": ii_dr_vr.get("verifier"),
        "drive_signal_dryrun_verifier": ds_dr_vr.get("verifier"),
        "seed_core_pluggable_dryrun_verifier": sc_dr_vr.get("verifier"),
        "cognitive_zoning_dryrun_verifier": cz_dr_vr.get("verifier"),
        "provider_abstraction_verifier": provider_dr_vr.get("verifier"),
        "controlled_runtime_verifier": cr_dr_vr.get("verifier"),
        "health_oversight_external_principle": health_policy.get("principle"),
        "health_oversight_written": health_policy.get("principle") == HEALTH_OVERSIGHT_PRINCIPLE,
        "luna_2_0_governance_baseline_closed": True,
        "no_runtime_leakage_in_upstream": len(leakage_issues) == 0,
        "planning_only": True,
        "review_pass": input_ok,
        "blockers": blockers,
        **meta,
    }

    scope_definition = {
        "definition_id": "mainline_resume_scope_definition_v1",
        "confirmations": list(MAINLINE_RESUME_CONFIRMATIONS),
        "confirmation_count": len(MAINLINE_RESUME_CONFIRMATIONS),
        "architecture_reentry": "first_person_vision_ocr_navigation_task → Luna 2.0 modular governance chain",
        **meta,
    }

    vision_plan = {
        "plan_id": "first_person_vision_chain_reentry_plan_v1",
        "chain_items": list(FIRST_PERSON_VISION_ITEMS),
        "item_count": len(FIRST_PERSON_VISION_ITEMS),
        "zone": "Perception Zone",
        "candidate_only": True,
        **meta,
    }

    ocr_plan = {
        "plan_id": "ocr_context_chain_reentry_plan_v1",
        "chain_items": list(OCR_CHAIN_ITEMS),
        "item_count": len(OCR_CHAIN_ITEMS),
        "candidate_only": True,
        **meta,
    }

    navigation_plan = {
        "plan_id": "navigation_task_chain_reentry_plan_v1",
        "chain_items": list(NAVIGATION_TASK_ITEMS),
        "item_count": len(NAVIGATION_TASK_ITEMS),
        "candidate_only": True,
        **meta,
    }

    bus_binding = _policy_doc(
        "capability_bus_binding_for_vision_ocr_navigation_v1",
        CAPABILITY_BUS_BINDING_CONFIRMATIONS,
        meta,
        constitution_bus_version="1.0.0",
        health_oversight_principle=HEALTH_OVERSIGHT_PRINCIPLE,
    )

    drive_binding = _policy_doc(
        "seed_core_drive_signal_binding_for_navigation_v1",
        DRIVE_SIGNAL_BINDING_CONFIRMATIONS,
        meta,
    )

    ii_binding = _policy_doc(
        "information_integration_binding_for_navigation_v1",
        II_BINDING_CONFIRMATIONS,
        meta,
    )

    decision_binding = _policy_doc(
        "decision_center_binding_for_navigation_v1",
        DECISION_CENTER_BINDING_CONFIRMATIONS,
        meta,
    )

    runtime_deferment = {
        "register_id": "controlled_runtime_deferment_for_vision_ocr_navigation_v1",
        "deferred_items": list(RUNTIME_DEFERMENT_ITEMS),
        "item_count": len(RUNTIME_DEFERMENT_ITEMS),
        "controlled_runtime_still_deferred": True,
        **meta,
    }

    candidate_flow = {
        "flow_id": "vision_ocr_navigation_candidate_flow_v1",
        "flow_steps": list(CANDIDATE_FLOW_STEPS),
        "step_count": len(CANDIDATE_FLOW_STEPS),
        "candidate_only": True,
        "no_runtime_now": True,
        **meta,
    }

    evidence_flow = {
        "flow_id": "vision_ocr_navigation_evidence_flow_v1",
        "evidence_items": list(EVIDENCE_FLOW_ITEMS),
        "item_count": len(EVIDENCE_FLOW_ITEMS),
        "not_fact_by_default": True,
        **meta,
    }

    task_route_flow = {
        "flow_id": "task_route_context_flow_v1",
        "flow_items": list(TASK_ROUTE_FLOW_ITEMS),
        "item_count": len(TASK_ROUTE_FLOW_ITEMS),
        **meta,
    }

    safety_policy = _policy_doc(
        "safety_survival_navigation_priority_policy_v1",
        SAFETY_PRIORITY_CONFIRMATIONS,
        meta,
    )

    boundary_matrix = {
        "matrix_id": "mainline_resume_boundary_matrix_v1",
        "boundary_fields": {f: False for f in BOUNDARY_FALSE},
        "all_false": True,
        "boundary_pass": True,
        **meta,
    }

    next_phase_plan = {
        "plan_id": "mainline_resume_next_phase_plan_v1",
        "next_phase": NEXT_PHASE_GO,
        "next_objective": (
            "plan first-person vision / OCR / map / navigation candidate flow "
            "into Information Integration Layer without real runtime"
        ),
        "controlled_first": "candidate flow before runtime",
        **meta,
    }

    contracts_ok = (
        len(MAINLINE_RESUME_CONFIRMATIONS) == 8
        and len(CANDIDATE_FLOW_STEPS) == 7
        and len(RUNTIME_DEFERMENT_ITEMS) == 8
    )
    planning_pass = input_ok and contracts_ok

    resume_decision = {
        "decision_id": "vision_ocr_navigation_task_mainline_resume_decision_v1",
        "planning_pass": planning_pass,
        "high_risk": not planning_pass,
        "final_decision": FINAL_DECISION_GO if planning_pass else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if planning_pass else NEXT_PHASE_HOLD,
        "architecture_summary": [
            "Luna 2.0 governance baseline reconnected to first-person vision/OCR/navigation/task mainline",
            "Perception → Information Integration → Decision → Output/Gate candidate chain defined",
            "Constitution-Bus v1.0 + external health oversight binding for vision/OCR/navigation modules",
            "Controlled Runtime deferred; candidate flow first, no real camera/OCR/navigation runtime",
        ],
        **meta,
    }

    policy = {
        "policy_id": "vision_ocr_navigation_task_mainline_resume_policy_v1",
        "phase": PHASE_ID,
        "scope": SCOPE,
        "mainline": "first_person_vision_ocr_navigation_task",
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
        "final_decision": resume_decision["final_decision"],
        "recommended_next_phase": resume_decision["recommended_next_phase"],
        **meta,
    }

    return {
        "vision_ocr_navigation_task_mainline_resume_policy": policy,
        "constitution_bus_governance_input_review": input_review,
        "mainline_resume_scope_definition": scope_definition,
        "first_person_vision_chain_reentry_plan": vision_plan,
        "ocr_context_chain_reentry_plan": ocr_plan,
        "navigation_task_chain_reentry_plan": navigation_plan,
        "capability_bus_binding_for_vision_ocr_navigation": bus_binding,
        "seed_core_drive_signal_binding_for_navigation": drive_binding,
        "information_integration_binding_for_navigation": ii_binding,
        "decision_center_binding_for_navigation": decision_binding,
        "controlled_runtime_deferment_for_vision_ocr_navigation": runtime_deferment,
        "vision_ocr_navigation_candidate_flow": candidate_flow,
        "vision_ocr_navigation_evidence_flow": evidence_flow,
        "task_route_context_flow": task_route_flow,
        "safety_survival_navigation_priority_policy": safety_policy,
        "mainline_resume_boundary_matrix": boundary_matrix,
        "mainline_resume_next_phase_plan": next_phase_plan,
        "non_claims_register": non_claims,
        "vision_ocr_navigation_task_mainline_resume_decision": resume_decision,
        "summary": summary,
    }
