# -*- coding: utf-8 -*-
"""Midplatform Information Integration Layer Planning v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.midplatform_candidate_evidence_flow_integration_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as CEF_DR_FINAL_GO,
)
from capabilities.governance.midplatform_cognitive_zoning_architecture_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as CZ_DR_FINAL_GO,
    NO_UNIVERSAL_BRAIN_REVIEW_RULES,
)
from capabilities.governance.midplatform_decision_center_module_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as DC_DR_FINAL_GO,
)
from capabilities.governance.midplatform_end_to_end_output_chain_simulation_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as E2E_DR_FINAL_GO,
)
from capabilities.governance.midplatform_frontend_model_influence_simulation_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as FMIS_DR_FINAL_GO,
)
from capabilities.governance.midplatform_safety_gate_planning_v1 import FOUR_LAYER_ARCHITECTURE
from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.governance.provider_abstraction_standard_alignment_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as PROVIDER_ABS_DR_FINAL_GO,
)
from capabilities.governance.seed_core_drive_signal_contract_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as DS_DR_FINAL_GO,
    NEXT_PHASE_GO as DS_DR_NEXT_PHASE,
)
from capabilities.governance.seed_core_drive_signal_contract_planning_v1 import (
    CONFLICT_TYPES as DRIVE_CONFLICT_TYPES,
    INTEGRATION_PLAN_CONFIRMATIONS,
)
from capabilities.governance.seed_core_pluggable_layer_architecture_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as SC_DR_FINAL_GO,
)
from capabilities.governance.seed_core_pluggable_layer_architecture_planning_v1 import (
    UPSTREAM_RUNTIME_LEAKAGE_FIELDS,
)

PHASE_ID = "Phase-Midplatform-Information-Integration-Layer-Planning-v1-001"
SCOPE = "information_integration_layer_planning_only"
SOURCE_CHAIN = "midplatform_information_integration_layer_planning_v1"

UPSTREAM_DS_DR_FINAL = DS_DR_FINAL_GO
UPSTREAM_DS_DR_NEXT = DS_DR_NEXT_PHASE

FINAL_DECISION_GO = "MIDPLATFORM_INFORMATION_INTEGRATION_LAYER_PLANNING_READY_FOR_DRYRUN_AND_REVIEW"
FINAL_DECISION_HOLD = "MIDPLATFORM_INFORMATION_INTEGRATION_LAYER_PLANNING_HOLD_FOR_ISSUE_REVIEW"
NEXT_PHASE_GO = "Phase-Midplatform-Information-Integration-Layer-DryRunAndReview-v1-001"
NEXT_PHASE_HOLD = "Phase-Midplatform-Information-Integration-Layer-Issue-Review-v1-001"

INTEGRATION_INPUT_SOURCES: Tuple[str, ...] = (
    "visual_observation_candidate",
    "ocr_result_candidate",
    "asr_transcript_candidate",
    "map_location_context_candidate",
    "route_context_candidate",
    "task_context_candidate",
    "memory_retrieval_candidate",
    "worldmodel_context_candidate",
    "validation_result_candidate",
    "health_signal_candidate",
    "whitebox_trace_candidate",
    "provider_status_candidate",
    "drive_signal_candidate",
    "seed_core_signal_candidate",
    "seed_core_hint_candidate",
    "user_preference_candidate",
    "personal_continuity_context_candidate",
    "resource_budget_hint_candidate",
)

INTEGRATION_INPUT_CONFIRMATIONS: Tuple[str, ...] = (
    "all inputs are candidate/evidence/signal/context",
    "no input is treated as fact by default",
    "source_chain required",
    "ttl/freshness required where applicable",
    "confidence/status required where applicable",
)

INTEGRATED_CONTEXT_CANDIDATE_FIELDS: Tuple[str, ...] = (
    "integrated_context_id",
    "source_input_refs",
    "source_chain_matrix",
    "current_task_context",
    "current_scene_context",
    "current_route_context",
    "current_user_context",
    "current_risk_context",
    "drive_context",
    "health_context",
    "validation_context",
    "whitebox_context",
    "memory_context",
    "provider_context",
    "evidence_weight_map",
    "context_priority_map_ref",
    "context_conflict_refs",
    "context_gap_refs",
    "freshness_status_refs",
    "uncertainty_level",
    "decision_readiness_ref",
    "recommended_next_step_hint",
    "forbidden_actions",
    "required_observation",
    "rationale_refs",
    "whitebox_trace_refs",
    "candidate_only",
    "not_decision",
    "not_fact",
    "not_user_output",
    "runtime_enable_allowed",
)

CONTEXT_CONFLICT_FIELDS: Tuple[str, ...] = (
    "conflict_id",
    "conflict_type",
    "conflicting_source_refs",
    "conflict_severity",
    "affected_context_fields",
    "recommended_resolution_hint",
    "decision_required",
    "hold_or_reobserve_hint",
    "evidence_refs",
    "whitebox_trace_refs",
    "candidate_only",
)

CONTEXT_CONFLICT_TYPES: Tuple[str, ...] = (
    "visual_vs_ocr",
    "map_vs_vision",
    "task_vs_survival",
    "memory_vs_current_observation",
    "provider_status_vs_runtime_request",
    "health_vs_task",
    "resource_vs_task",
    "emotion_vs_safety",
    "evolution_vs_governance",
    "stale_vs_current",
)

CONTEXT_GAP_FIELDS: Tuple[str, ...] = (
    "gap_id",
    "gap_type",
    "missing_source_type",
    "affected_decision_scope",
    "required_observation",
    "required_evidence",
    "priority_level",
    "ttl",
    "candidate_only",
)

CONTEXT_GAP_TYPES: Tuple[str, ...] = (
    "missing_visual_context",
    "missing_ocr_context",
    "missing_location_context",
    "missing_task_context",
    "missing_validation_result",
    "missing_health_signal",
    "missing_drive_signal",
    "missing_provider_status",
    "missing_memory_context",
    "missing_user_confirmation",
)

FRESHNESS_STATUS_FIELDS: Tuple[str, ...] = (
    "freshness_status_id",
    "source_ref",
    "source_type",
    "observed_at",
    "ttl",
    "freshness_state",
    "stale_risk",
    "can_drive_decision",
    "refresh_required_hint",
    "candidate_only",
)

PRIORITY_MAP_FIELDS: Tuple[str, ...] = (
    "priority_map_id",
    "drive_priority_weight",
    "survival_priority_weight",
    "task_priority_weight",
    "health_pressure_weight",
    "resource_pressure_weight",
    "evidence_confidence_weight",
    "freshness_weight",
    "user_preference_weight",
    "constitution_constraint_weight",
    "urgency_weight",
    "output_priority_hint",
    "candidate_only",
)

DECISION_READINESS_FIELDS: Tuple[str, ...] = (
    "decision_readiness_id",
    "readiness_status",
    "readiness_score_candidate",
    "required_missing_inputs",
    "blocking_conflicts",
    "high_risk_flags",
    "sufficient_for_decision",
    "recommended_next_step",
    "decision_center_handoff_allowed",
    "candidate_only",
)

DRIVE_SIGNAL_INTEGRATION_CONFIRMATIONS: Tuple[str, ...] = (
    "drive_signal_candidate is consumed as priority/attention/readiness input",
    "Survival Drive can elevate risk priority",
    "Task Drive can elevate task relevance",
    "Resource Governance can recommend hold/degrade/fallback",
    "Health Management can influence readiness",
    "Emotion Engine can influence tone/social context only after constraints",
    "Evolutionary Recursion can only create proposal/ref refs, not direct change",
    "drive signal cannot make decision",
    "drive signal cannot enable runtime",
)

PERCEPTION_INTEGRATION_CONFIRMATIONS: Tuple[str, ...] = (
    "visual / OCR / ASR / map inputs remain candidate/evidence",
    "conflicting perception inputs produce conflict_candidate",
    "missing perception input produces gap_candidate",
    "low-confidence perception increases uncertainty",
    "perception result does not become fact without validation/admission",
)

MEMORY_WM_INTEGRATION_CONFIRMATIONS: Tuple[str, ...] = (
    "memory retrieval is context candidate, not fact",
    "worldmodel context may be historical/stale",
    "current observation can override memory only after validation/decision later",
    "Memory/WorldModel write not allowed",
    "Personal Continuity context requires identity/permission refs later",
)

TASK_ROUTE_MAP_CONFIRMATIONS: Tuple[str, ...] = (
    "task context affects relevance",
    "route context affects urgency",
    "map context affects spatial reasoning",
    "route/task cannot override Survival Drive under risk",
    "missing route/location context can trigger required_observation",
    "navigation action not generated here",
)

HEALTH_VALIDATION_WHITEBOX_CONFIRMATIONS: Tuple[str, ...] = (
    "validation fail can block readiness",
    "health pressure can reduce readiness",
    "whitebox trace required for transformation",
    "missing trace creates issue/gap candidate",
    "integration does not mutate validation result",
    "integration does not mutate health signal",
)

PROVIDER_STATUS_CONFIRMATIONS: Tuple[str, ...] = (
    "provider readiness status enters provider_context",
    "provider not ready blocks runtime readiness",
    "provider failure creates issue/fallback candidate",
    "provider status does not select provider",
    "provider status does not invoke provider",
    "provider auto-switch forbidden",
)

SCORING_POLICY_ITEMS: Tuple[str, ...] = (
    "conflict severity levels",
    "gap priority levels",
    "freshness states",
    "stale data handling",
    "confidence weighting",
    "evidence weighting",
    "drive priority weighting",
    "readiness score candidate semantics",
)

SCORING_CONFIRMATIONS: Tuple[str, ...] = (
    "scores are candidate-only",
    "scores do not decide",
    "scores do not authorize runtime",
    "high-risk score forces handoff to Decision Center / Governance later",
)

HANDOFF_PLAN_ITEMS: Tuple[str, ...] = (
    "integrated_context_candidate → decision_request_candidate enrichment later",
    "decision_readiness_candidate must be attached",
    "unresolved conflict must be attached",
    "context_gap_candidate must be attached",
    "all source_chain refs preserved",
    "Decision Center remains final decision module",
)

NO_UNIVERSAL_BRAIN_BOUNDARIES: Tuple[str, ...] = (
    "Information Integration Layer does not replace Perception Zone",
    "does not replace Memory / WorldModel Zone",
    "does not replace Drive Zone",
    "does not replace Decision Center",
    "does not replace Governance Zone",
    "does not replace Execution Zone",
    "does not invoke providers",
    "does not execute actions",
    "information integration cannot become universal brain",
)

LAYER_NOT_RESPONSIBILITIES: Tuple[str, ...] = (
    "不做最终裁决",
    "不生成 decision_candidate",
    "不调用 provider/model",
    "不写 Memory / WorldModel",
    "不提交 task_state",
    "不生成 user output",
    "不启 runtime",
)

LAYER_CORE_RESPONSIBILITIES: Tuple[str, ...] = (
    "consume multi-source candidate/evidence/signal/context",
    "assemble integrated_context_candidate",
    "detect conflict / gap / stale / priority",
    "preserve source_chain / evidence / traceability",
    "prepare decision_readiness_candidate",
    "handoff to Decision Center later",
)

TRACEABILITY_FIELDS: Tuple[str, ...] = (
    "source_input_refs",
    "source_chain_matrix",
    "evidence_refs",
    "validation_refs",
    "health_refs",
    "drive_signal_refs",
    "seed_core_signal_refs",
    "memory_refs",
    "map_refs",
    "provider_refs",
    "whitebox_trace_refs",
    "version_ref",
    "ttl",
)

NON_CLAIMS: Tuple[str, ...] = (
    "Information Integration Planning GO ≠ integration runtime enabled",
    "integrated_context_candidate planned ≠ decision made",
    "context priority planned ≠ action authorized",
    "drive signal consumed ≠ drive can execute",
    "next DryRunAndReview ≠ model/provider invocation",
)

BOUNDARY_TRUE: Tuple[str, ...] = ("information_integration_layer_planning_only",)

BOUNDARY_FALSE: Tuple[str, ...] = (
    "information_integration_runtime_enabled_now",
    "information_integration_executed_now",
    "model_runtime_invoked_now",
    "provider_invoked_now",
    "llm_invoked_now",
    "vision_runtime_invoked_now",
    "ocr_runtime_invoked_now",
    "map_provider_invoked_now",
    "memory_retrieval_invoked_now",
    "memory_written_now",
    "world_model_written_now",
    "decision_executed_now",
    "decision_candidate_generated_now",
    "task_state_committed_now",
    "user_output_generated_now",
    "controlled_runtime_enabled_now",
)

DEFAULT_OUTPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_information_integration_layer_planning"
)


def _planning_meta() -> Dict[str, Any]:
    meta = {
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "source_chain": SOURCE_CHAIN,
        "selected_provider_for_execution": None,
        "four_layer_architecture": FOUR_LAYER_ARCHITECTURE,
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


def _contract_doc(contract_id: str, fields: Tuple[str, ...], meta: Dict[str, Any], **extra: Any) -> Dict[str, Any]:
    doc = {
        "contract_id": contract_id,
        "required_fields": list(fields),
        "field_count": len(fields),
        "candidate_only": True,
        **meta,
    }
    doc.update(extra)
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


def run_midplatform_information_integration_layer_planning_v1(
    *,
    seed_core_drive_signal_contract_dryrun_and_review_root: str,
    seed_core_pluggable_layer_architecture_dryrun_and_review_root: str,
    midplatform_cognitive_zoning_architecture_dryrun_and_review_root: str,
    provider_abstraction_standard_alignment_dryrun_and_review_root: str,
    midplatform_frontend_model_influence_simulation_dryrun_and_review_root: str,
    midplatform_end_to_end_output_chain_simulation_dryrun_and_review_root: str,
    midplatform_candidate_evidence_flow_integration_dryrun_and_review_root: str,
    midplatform_decision_center_module_dryrun_and_review_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []

    ds_dr_root = Path(seed_core_drive_signal_contract_dryrun_and_review_root).expanduser().resolve()
    sc_dr_root = Path(seed_core_pluggable_layer_architecture_dryrun_and_review_root).expanduser().resolve()
    cz_dr_root = Path(midplatform_cognitive_zoning_architecture_dryrun_and_review_root).expanduser().resolve()
    provider_dr_root = Path(
        provider_abstraction_standard_alignment_dryrun_and_review_root
    ).expanduser().resolve()
    fmis_dr_root = Path(
        midplatform_frontend_model_influence_simulation_dryrun_and_review_root
    ).expanduser().resolve()
    e2e_dr_root = Path(
        midplatform_end_to_end_output_chain_simulation_dryrun_and_review_root
    ).expanduser().resolve()
    cef_dr_root = Path(
        midplatform_candidate_evidence_flow_integration_dryrun_and_review_root
    ).expanduser().resolve()
    dc_dr_root = Path(midplatform_decision_center_module_dryrun_and_review_root).expanduser().resolve()

    ds_dr_sm = _try_read_json(ds_dr_root / "summary.json") or {}
    ds_dr_vr = _try_read_json(ds_dr_root / "verifier_report.json") or {}
    sc_dr_vr = _try_read_json(sc_dr_root / "verifier_report.json") or {}
    cz_dr_sm = _try_read_json(cz_dr_root / "summary.json") or {}
    cz_dr_vr = _try_read_json(cz_dr_root / "verifier_report.json") or {}
    provider_dr_vr = _try_read_json(provider_dr_root / "verifier_report.json") or {}
    provider_dr_sm = _try_read_json(provider_dr_root / "summary.json") or {}
    fmis_dr_vr = _try_read_json(fmis_dr_root / "verifier_report.json") or {}
    fmis_dr_sm = _try_read_json(fmis_dr_root / "summary.json") or {}
    e2e_dr_vr = _try_read_json(e2e_dr_root / "verifier_report.json") or {}
    e2e_dr_sm = _try_read_json(e2e_dr_root / "summary.json") or {}
    cef_dr_vr = _try_read_json(cef_dr_root / "verifier_report.json") or {}
    dc_dr_vr = _try_read_json(dc_dr_root / "verifier_report.json") or {}

    brain_review = _try_read_json(cz_dr_root / "no_universal_brain_policy_review_v1.json") or {}
    integration_zone_review = _try_read_json(
        cz_dr_root / "zone_responsibility_matrix_review_v1.json"
    ) or {}
    ii_zone = next(
        (
            z
            for z in (integration_zone_review.get("zone_reviews") or [])
            if z.get("zone_id") == "information_integration_zone"
        ),
        {},
    )

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    meta = {
        **_planning_meta(),
        "upstream_drive_signal_dryrun_root": str(ds_dr_root),
        "upstream_seed_core_pluggable_dryrun_root": str(sc_dr_root),
        "upstream_cognitive_zoning_dryrun_root": str(cz_dr_root),
        "upstream_provider_abstraction_dryrun_root": str(provider_dr_root),
        "upstream_fmis_dryrun_root": str(fmis_dr_root),
        "upstream_e2e_simulation_dryrun_root": str(e2e_dr_root),
        "upstream_candidate_evidence_flow_dryrun_root": str(cef_dr_root),
        "upstream_decision_center_dryrun_root": str(dc_dr_root),
        "output_root": str(out_root),
    }

    if ds_dr_vr.get("verifier") != "GO":
        blockers.append("Drive Signal Contract DryRunAndReview must be GO")
    if ds_dr_sm.get("final_decision") != UPSTREAM_DS_DR_FINAL:
        blockers.append("drive signal dryrun final_decision mismatch")
    if ds_dr_sm.get("recommended_next_phase") != UPSTREAM_DS_DR_NEXT:
        blockers.append("drive signal dryrun recommended_next_phase mismatch")
    if sc_dr_vr.get("verifier") != "GO":
        blockers.append("Seed Core / Pluggable DryRunAndReview must be GO")
    if cz_dr_vr.get("verifier") != "GO":
        blockers.append("Cognitive Zoning DryRunAndReview must be GO")
    if not brain_review.get("dryrun_and_review_pass"):
        blockers.append("No Universal Brain policy must pass")
    if not ii_zone.get("dryrun_and_review_pass"):
        blockers.append("Information Integration Zone must be validated")
    if provider_dr_vr.get("verifier") != "GO":
        blockers.append("Provider Abstraction DryRunAndReview must be GO")
    if provider_dr_sm.get("final_decision") != PROVIDER_ABS_DR_FINAL_GO:
        blockers.append("provider abstraction dryrun final_decision mismatch")
    if fmis_dr_vr.get("verifier") != "GO":
        blockers.append("FMIS DryRunAndReview must be GO")
    if fmis_dr_sm.get("final_decision") != FMIS_DR_FINAL_GO:
        blockers.append("FMIS dryrun final_decision mismatch")
    if e2e_dr_vr.get("verifier") != "GO":
        blockers.append("E2E Simulation DryRunAndReview must be GO")
    if e2e_dr_sm.get("final_decision") != E2E_DR_FINAL_GO:
        blockers.append("E2E simulation dryrun final_decision mismatch")
    if cef_dr_vr.get("verifier") != "GO":
        blockers.append("Candidate Evidence Flow DryRunAndReview must be GO")
    if dc_dr_vr.get("verifier") != "GO":
        blockers.append("Decision Center Module DryRunAndReview must be GO")

    leakage_issues: List[str] = []
    for label, sm in (
        ("drive_signal_dr", ds_dr_sm),
        ("sc_pluggable_dr", _try_read_json(sc_dr_root / "summary.json") or {}),
        ("cognitive_zoning_dr", cz_dr_sm),
        ("provider", provider_dr_sm),
        ("fmis", fmis_dr_sm),
        ("e2e", e2e_dr_sm),
        ("cef", _try_read_json(cef_dr_root / "summary.json") or {}),
        ("decision_center", _try_read_json(dc_dr_root / "summary.json") or {}),
    ):
        for issue in _check_upstream_no_runtime_leakage(sm):
            leakage_issues.append(f"{label}:{issue}")
    blockers.extend(leakage_issues)

    input_ok = len(blockers) == 0

    input_review = {
        "review_id": "upstream_drive_signal_input_review_v1",
        "drive_signal_dryrun_verifier": ds_dr_vr.get("verifier"),
        "drive_signal_dryrun_final_decision": ds_dr_sm.get("final_decision"),
        "drive_signal_contracts_validated": True,
        "cognitive_zoning_dryrun_verifier": cz_dr_vr.get("verifier"),
        "information_integration_zone_validated": ii_zone.get("dryrun_and_review_pass"),
        "no_universal_brain_pass": brain_review.get("dryrun_and_review_pass"),
        "provider_abstraction_go": provider_dr_vr.get("verifier") == "GO",
        "fmis_go": fmis_dr_vr.get("verifier") == "GO",
        "e2e_go": e2e_dr_vr.get("verifier") == "GO",
        "candidate_evidence_flow_go": cef_dr_vr.get("verifier") == "GO",
        "decision_center_go": dc_dr_vr.get("verifier") == "GO",
        "no_runtime_leakage_in_upstream": len(leakage_issues) == 0,
        "planning_only": True,
        "review_pass": input_ok,
        "blockers": blockers,
        **meta,
    }

    layer_definition = {
        "definition_id": "information_integration_layer_definition_v1",
        "module_id": "midplatform_information_integration_layer_v1",
        "zone": "Information Integration Zone",
        "role": "multi_source_context_assembly_and_decision_readiness_preparation",
        "architectural_layer": "InformationIntegration",
        "runtime_enabled_now": False,
        "not_universal_brain": True,
        "not_decision_center": True,
        "not_memory_writer": True,
        "not_worldmodel_writer": True,
        "not_runtime_executor": True,
        "core_responsibilities": list(LAYER_CORE_RESPONSIBILITIES),
        "not_responsibilities": list(LAYER_NOT_RESPONSIBILITIES),
        **meta,
    }

    input_taxonomy = {
        "taxonomy_id": "integration_input_source_taxonomy_v1",
        "input_sources": list(INTEGRATION_INPUT_SOURCES),
        "source_count": len(INTEGRATION_INPUT_SOURCES),
        "confirmations": list(INTEGRATION_INPUT_CONFIRMATIONS),
        **meta,
    }

    integrated_context_contract = _contract_doc(
        "integrated_context_candidate_contract_v1",
        INTEGRATED_CONTEXT_CANDIDATE_FIELDS,
        meta,
        defaults={
            "candidate_only": True,
            "not_decision": True,
            "not_fact": True,
            "not_user_output": True,
            "runtime_enable_allowed": False,
        },
    )

    conflict_contract = _contract_doc(
        "context_conflict_candidate_contract_v1",
        CONTEXT_CONFLICT_FIELDS,
        meta,
        conflict_types=list(CONTEXT_CONFLICT_TYPES),
        conflict_type_count=len(CONTEXT_CONFLICT_TYPES),
        defaults={"decision_required": True, "candidate_only": True},
    )

    gap_contract = _contract_doc(
        "context_gap_candidate_contract_v1",
        CONTEXT_GAP_FIELDS,
        meta,
        gap_types=list(CONTEXT_GAP_TYPES),
        gap_type_count=len(CONTEXT_GAP_TYPES),
    )

    freshness_contract = _contract_doc(
        "context_freshness_status_contract_v1",
        FRESHNESS_STATUS_FIELDS,
        meta,
        defaults={"can_drive_decision": False, "candidate_only": True},
    )

    priority_contract = _contract_doc(
        "context_priority_map_contract_v1",
        PRIORITY_MAP_FIELDS,
        meta,
    )

    readiness_contract = _contract_doc(
        "decision_readiness_candidate_contract_v1",
        DECISION_READINESS_FIELDS,
        meta,
        defaults={
            "sufficient_for_decision": False,
            "decision_center_handoff_allowed": False,
            "candidate_only": True,
        },
    )

    drive_policy = _policy_doc("drive_signal_integration_policy_v1", DRIVE_SIGNAL_INTEGRATION_CONFIRMATIONS, meta)
    perception_policy = _policy_doc(
        "perception_context_integration_policy_v1", PERCEPTION_INTEGRATION_CONFIRMATIONS, meta
    )
    memory_policy = _policy_doc(
        "memory_worldmodel_context_integration_policy_v1", MEMORY_WM_INTEGRATION_CONFIRMATIONS, meta
    )
    task_policy = _policy_doc(
        "task_route_map_context_integration_policy_v1", TASK_ROUTE_MAP_CONFIRMATIONS, meta
    )
    health_policy = _policy_doc(
        "health_validation_whitebox_integration_policy_v1",
        HEALTH_VALIDATION_WHITEBOX_CONFIRMATIONS,
        meta,
    )
    provider_policy = _policy_doc("provider_status_integration_policy_v1", PROVIDER_STATUS_CONFIRMATIONS, meta)

    scoring_policy = {
        "policy_id": "conflict_gap_freshness_scoring_policy_v1",
        "scoring_items": list(SCORING_POLICY_ITEMS),
        "item_count": len(SCORING_POLICY_ITEMS),
        "confirmations": list(SCORING_CONFIRMATIONS),
        "drive_conflict_types_aligned": [c["conflict_id"] for c in DRIVE_CONFLICT_TYPES],
        **meta,
    }

    handoff_plan = {
        "plan_id": "information_integration_to_decision_center_handoff_plan_v1",
        "handoff_items": list(HANDOFF_PLAN_ITEMS),
        "item_count": len(HANDOFF_PLAN_ITEMS),
        "decision_center_final": True,
        **meta,
    }

    no_brain_boundary = {
        "policy_id": "information_integration_no_universal_brain_boundary_v1",
        "boundaries": list(NO_UNIVERSAL_BRAIN_BOUNDARIES),
        "boundary_count": len(NO_UNIVERSAL_BRAIN_BOUNDARIES),
        "no_universal_brain_rules": list(NO_UNIVERSAL_BRAIN_REVIEW_RULES),
        **meta,
    }

    traceability = {
        "policy_id": "information_integration_traceability_policy_v1",
        "required_fields": list(TRACEABILITY_FIELDS),
        "field_count": len(TRACEABILITY_FIELDS),
        "all_transformations_must_preserve": True,
        **meta,
    }

    boundary_matrix = {
        "matrix_id": "information_integration_boundary_matrix_v1",
        "boundary_fields": {f: False for f in BOUNDARY_FALSE},
        "all_false": True,
        "boundary_pass": True,
        **meta,
    }

    dryrun_plan = {
        "plan_id": "information_integration_dryrun_plan_v1",
        "next_phase": NEXT_PHASE_GO,
        "dryrun_objectives": [
            "generate information_integration_model_candidate",
            "generate sample integrated_context_candidate",
            "generate conflict/gap/freshness/priority/readiness samples",
            "verify drive_signal / perception / memory / task / map / health / validation / whitebox / provider status integration",
            "verify no decision / no model/provider / no Memory/WorldModel write",
            "verify Decision Center handoff",
        ],
        **meta,
    }

    contracts_ok = (
        len(INTEGRATION_INPUT_SOURCES) == 18
        and len(INTEGRATED_CONTEXT_CANDIDATE_FIELDS) >= 28
        and len(CONTEXT_CONFLICT_TYPES) == 10
        and len(CONTEXT_GAP_TYPES) == 10
    )
    planning_pass = input_ok and contracts_ok

    planning_decision = {
        "decision_id": "information_integration_layer_planning_decision_v1",
        "planning_pass": planning_pass,
        "high_risk": not planning_pass,
        "final_decision": FINAL_DECISION_GO if planning_pass else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if planning_pass else NEXT_PHASE_HOLD,
        "architecture_summary": [
            "Information Integration Layer = multi-source context assembly + decision readiness preparation",
            "consumes 18 input source types including drive_signal_candidate",
            "produces integrated_context_candidate + conflict/gap/freshness/priority/readiness candidates",
            "does not decide, does not invoke provider/model, does not write Memory/WorldModel",
            "handoff to Decision Center later with full traceability",
        ],
        **meta,
    }

    policy = {
        "policy_id": "information_integration_layer_planning_policy_v1",
        "phase": PHASE_ID,
        "scope": SCOPE,
        "module_id": "midplatform_information_integration_layer_v1",
        "input_source_count": len(INTEGRATION_INPUT_SOURCES),
        "planning_not_runtime_not_decide": True,
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
        "information_integration_layer_planning_policy": policy,
        "upstream_drive_signal_input_review": input_review,
        "information_integration_layer_definition": layer_definition,
        "integration_input_source_taxonomy": input_taxonomy,
        "integrated_context_candidate_contract": integrated_context_contract,
        "context_conflict_candidate_contract": conflict_contract,
        "context_gap_candidate_contract": gap_contract,
        "context_freshness_status_contract": freshness_contract,
        "context_priority_map_contract": priority_contract,
        "decision_readiness_candidate_contract": readiness_contract,
        "drive_signal_integration_policy": drive_policy,
        "perception_context_integration_policy": perception_policy,
        "memory_worldmodel_context_integration_policy": memory_policy,
        "task_route_map_context_integration_policy": task_policy,
        "health_validation_whitebox_integration_policy": health_policy,
        "provider_status_integration_policy": provider_policy,
        "conflict_gap_freshness_scoring_policy": scoring_policy,
        "information_integration_to_decision_center_handoff_plan": handoff_plan,
        "information_integration_no_universal_brain_boundary": no_brain_boundary,
        "information_integration_traceability_policy": traceability,
        "information_integration_boundary_matrix": boundary_matrix,
        "information_integration_dryrun_plan": dryrun_plan,
        "non_claims_register": non_claims,
        "information_integration_layer_planning_decision": planning_decision,
        "summary": summary,
    }
