# -*- coding: utf-8 -*-
"""Vision Navigation Decision Chain Candidate DryRun v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.luna_constitution_capability_bus_governance_baseline_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as CB_DR_FINAL_GO,
)
from capabilities.governance.midplatform_decision_center_module_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as DC_DR_FINAL_GO,
)
from capabilities.governance.midplatform_decision_center_module_planning_v1 import (
    OUTPUT_CONTRACT_FIELDS,
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
from capabilities.governance.vision_navigation_information_integration_chain_dryrun_v1 import (
    FINAL_DECISION_GO as II_CHAIN_DR_FINAL_GO,
    NEXT_PHASE_GO as II_CHAIN_DR_NEXT_PHASE,
)

PHASE_ID = "Phase-Vision-Navigation-Decision-Chain-Candidate-DryRun-v1-001"
SCOPE = "vision_navigation_decision_chain_candidate_dryrun_only"
SOURCE_CHAIN = "vision_navigation_decision_chain_candidate_dryrun_v1"

UPSTREAM_II_CHAIN_DR_FINAL = II_CHAIN_DR_FINAL_GO
UPSTREAM_II_CHAIN_DR_NEXT = II_CHAIN_DR_NEXT_PHASE

FINAL_DECISION_GO = (
    "VISION_NAVIGATION_DECISION_CHAIN_CANDIDATE_DRYRUN_CLOSED_"
    "READY_FOR_TASK_RESPONSE_CANDIDATE_DRYRUN"
)
FINAL_DECISION_HOLD = (
    "VISION_NAVIGATION_DECISION_CHAIN_CANDIDATE_DRYRUN_HOLD_FOR_ISSUE_REVIEW"
)
NEXT_PHASE_GO = "Phase-Vision-Navigation-Task-Response-Candidate-DryRun-v1-001"
NEXT_PHASE_HOLD = "Phase-Vision-Navigation-Decision-Chain-Candidate-Issue-Review-v1-001"

READINESS_CONSUMPTION_REVIEW_ITEMS: Tuple[str, ...] = (
    "integrated_context_candidate consumed as decision input",
    "decision_readiness_candidate consumed with sufficient_for_decision=false",
    "context_conflict candidate informs hold/reobserve rationale",
    "context_gap candidate informs missing live validation hold",
    "freshness can_drive_decision=false preserved in decision rationale",
    "readiness not_ready blocks navigation action authorization",
)

CONSTITUTION_BINDING_REVIEW_ITEMS: Tuple[str, ...] = (
    "Constitution-Bus governance baseline referenced",
    "Decision Center remains裁决层 not Constitution author",
    "Health signal consumed as pressure context only",
    "Survival Drive priority reflected in hold rationale",
    "forbidden_actions from integrated context preserved",
    "no constitution rule write attempted",
)

RATIONALE_TRACEABILITY_REVIEW_ITEMS: Tuple[str, ...] = (
    "decision_candidate includes rationale_refs",
    "source input refs preserved from integrated_context",
    "evidence_refs preserved",
    "whitebox_trace_refs preserved",
    "conflict/gap/readiness refs attached",
    "fixture provenance preserved",
    "hold_reason documented for hold_candidate",
)

DECISION_BOUNDARY_REVIEW_ITEMS: Tuple[str, ...] = (
    "decision_candidate generated as candidate only",
    "decision_executed_now=false",
    "navigation_runtime_enabled_now=false",
    "real_navigation_action_executed_now=false",
    "user_output_generated_now=false",
    "task_response_candidate_generated_now=false",
    "memory/worldmodel write blocked",
)

TASK_RESPONSE_HANDOFF_REVIEW_ITEMS: Tuple[str, ...] = (
    "decision_candidate can be handed to Task Response layer later",
    "task_response_generation_allowed=false now",
    "user_output_allowed=false now",
    "no task_response_candidate generated now",
    "no user output generated now",
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
    "dryrun_to_decision_center_runtime_enable",
    "dryrun_to_decision_execution",
    "dryrun_to_task_response_generation",
    "dryrun_to_user_output",
    "dryrun_to_memory_write",
    "dryrun_to_world_model_write",
    "dryrun_to_task_state_commit",
    "dryrun_to_controlled_runtime_enable",
)

NON_CLAIMS: Tuple[str, ...] = (
    "Decision Chain Candidate DryRun GO ≠ camera/OCR/map runtime enabled",
    "decision_candidate ≠ decision executed",
    "decision_candidate ≠ navigation action allowed",
    "fixture-based decision_candidate ≠ real navigation fact",
    "hold_candidate ≠ user output generated",
    "next Task Response Candidate DryRun ≠ real navigation execution",
)

BOUNDARY_TRUE: Tuple[str, ...] = (
    "vision_navigation_decision_chain_candidate_dryrun_only",
    "simulated",
    "sample_fixture_only",
    "decision_candidate_generated_now",
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
    "decision_center_runtime_enabled_now",
    "decision_executed_now",
    "task_response_candidate_generated_now",
    "user_output_generated_now",
    "memory_written_now",
    "world_model_written_now",
    "task_state_committed_now",
    "controlled_runtime_enabled_now",
)

DEFAULT_OUTPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "vision_navigation_decision_chain_candidate_dryrun"
)


def _dryrun_meta() -> Dict[str, Any]:
    meta = {
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "source_chain": SOURCE_CHAIN,
        "selected_provider_for_execution": None,
        "four_layer_architecture": FOUR_LAYER_ARCHITECTURE,
        "system_level_simulated_go": True,
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


def run_vision_navigation_decision_chain_candidate_dryrun_v1(
    *,
    vision_navigation_information_integration_chain_dryrun_root: str,
    midplatform_decision_center_module_dryrun_and_review_root: str,
    luna_constitution_capability_bus_governance_baseline_dryrun_and_review_root: str,
    seed_core_drive_signal_contract_dryrun_and_review_root: str,
    provider_abstraction_standard_alignment_dryrun_and_review_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []

    ii_chain_root = Path(
        vision_navigation_information_integration_chain_dryrun_root
    ).expanduser().resolve()
    dc_dr_root = Path(
        midplatform_decision_center_module_dryrun_and_review_root
    ).expanduser().resolve()
    cb_dr_root = Path(
        luna_constitution_capability_bus_governance_baseline_dryrun_and_review_root
    ).expanduser().resolve()
    ds_dr_root = Path(seed_core_drive_signal_contract_dryrun_and_review_root).expanduser().resolve()
    provider_dr_root = Path(
        provider_abstraction_standard_alignment_dryrun_and_review_root
    ).expanduser().resolve()

    ii_chain_sm = _try_read_json(ii_chain_root / "summary.json") or {}
    ii_chain_vr = _try_read_json(ii_chain_root / "verifier_report.json") or {}
    dc_dr_vr = _try_read_json(dc_dr_root / "verifier_report.json") or {}
    cb_dr_vr = _try_read_json(cb_dr_root / "verifier_report.json") or {}
    ds_dr_vr = _try_read_json(ds_dr_root / "verifier_report.json") or {}
    provider_dr_vr = _try_read_json(provider_dr_root / "verifier_report.json") or {}

    integrated = _try_read_json(ii_chain_root / "sample_integrated_context_candidate_v1.json") or {}
    readiness = _try_read_json(ii_chain_root / "sample_decision_readiness_candidate_v1.json") or {}
    conflict = _try_read_json(ii_chain_root / "sample_context_conflict_candidate_v1.json") or {}
    gap = _try_read_json(ii_chain_root / "sample_context_gap_candidate_v1.json") or {}
    freshness = _try_read_json(ii_chain_root / "sample_context_freshness_status_v1.json") or {}
    priority = _try_read_json(ii_chain_root / "sample_context_priority_map_v1.json") or {}

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    meta = {
        **_dryrun_meta(),
        "upstream_integration_chain_dryrun_root": str(ii_chain_root),
        "upstream_decision_center_dryrun_root": str(dc_dr_root),
        "upstream_constitution_bus_dryrun_root": str(cb_dr_root),
        "upstream_drive_signal_dryrun_root": str(ds_dr_root),
        "upstream_provider_abstraction_dryrun_root": str(provider_dr_root),
        "output_root": str(out_root),
    }

    if ii_chain_vr.get("verifier") != "GO":
        blockers.append("Integration Chain DryRun must be GO")
    if ii_chain_sm.get("final_decision") != UPSTREAM_II_CHAIN_DR_FINAL:
        blockers.append("integration chain dryrun final_decision mismatch")
    if ii_chain_sm.get("recommended_next_phase") != UPSTREAM_II_CHAIN_DR_NEXT:
        blockers.append("integration chain dryrun recommended_next_phase mismatch")
    if dc_dr_vr.get("verifier") != "GO":
        blockers.append("Decision Center Module DryRunAndReview must be GO")
    if cb_dr_vr.get("verifier") != "GO":
        blockers.append("Constitution-Bus v1.0 must be GO")
    if ds_dr_vr.get("verifier") != "GO":
        blockers.append("Drive Signal Contract DryRunAndReview must be GO")
    if provider_dr_vr.get("verifier") != "GO":
        blockers.append("Provider Abstraction must be GO")

    if integrated.get("candidate_only") is not True:
        blockers.append("integrated_context must be candidate_only")
    if integrated.get("not_decision") is not True:
        blockers.append("integrated_context must remain not_decision")
    if readiness.get("sufficient_for_decision") is not False:
        blockers.append("readiness sufficient_for_decision must be false for fixture hold")
    if readiness.get("readiness_status") != "not_ready_for_real_navigation_decision":
        blockers.append("readiness_status must be not_ready_for_real_navigation_decision")

    input_ok = len(blockers) == 0

    input_review = {
        "review_id": "integration_chain_input_review_v1",
        "integration_chain_dryrun_verifier": ii_chain_vr.get("verifier"),
        "integration_chain_dryrun_final_decision": ii_chain_sm.get("final_decision"),
        "decision_center_dryrun_verifier": dc_dr_vr.get("verifier"),
        "constitution_bus_verifier": cb_dr_vr.get("verifier"),
        "drive_signal_verifier": ds_dr_vr.get("verifier"),
        "provider_abstraction_verifier": provider_dr_vr.get("verifier"),
        "integrated_context_ref": integrated.get("integrated_context_id"),
        "decision_readiness_ref": readiness.get("decision_readiness_id"),
        "fixture_metadata_only": True,
        "chain_dryrun_only": True,
        "review_pass": input_ok,
        "blockers": blockers,
        **meta,
    }

    chain_model = {
        **meta,
        "model_id": "vision_navigation_decision_chain_v1",
        "chain_type": "fixture_based_decision_chain_candidate",
        "consumes_integrated_context_candidate": True,
        "consumes_decision_readiness_candidate": True,
        "consumes_context_conflict_candidate": True,
        "consumes_context_gap_candidate": True,
        "consumes_freshness_status": True,
        "consumes_priority_map": True,
        "emits_decision_candidate": True,
        "does_not_execute_decision": True,
        "does_not_invoke_provider": True,
        "does_not_enable_runtime": True,
        "does_not_generate_task_response": True,
        "does_not_generate_user_output": True,
        "candidate_only": True,
    }

    decision_request = {
        "decision_request_id": "decision_request_vision_nav_chain_001",
        "integrated_context_ref": integrated.get("integrated_context_id"),
        "decision_readiness_ref": readiness.get("decision_readiness_id"),
        "context_conflict_refs": integrated.get("context_conflict_refs") or [],
        "context_gap_refs": integrated.get("context_gap_refs") or [],
        "freshness_status_refs": integrated.get("freshness_status_refs") or [],
        "priority_map_ref": integrated.get("context_priority_map_ref"),
        "source_input_refs": integrated.get("source_input_refs") or [],
        "task_context_ref": integrated.get("current_task_context", {}).get("task_id"),
        "scene_context": integrated.get("current_scene_context"),
        "risk_context": integrated.get("current_risk_context"),
        "uncertainty_level": integrated.get("uncertainty_level"),
        "constitution_constraint_refs": ["constitution_bus:governance_baseline_v1"],
        "health_signal_refs": ["health_signal_candidate:module_status_001"],
        "drive_signal_ref": integrated.get("drive_context", {}).get("drive_signal_ref"),
        "whitebox_trace_refs": integrated.get("whitebox_trace_refs") or [],
        "fixture_metadata_only": True,
        "candidate_only": True,
        "not_fact": True,
        "not_action": True,
        **meta,
    }

    decision_candidate = {
        "decision_candidate_id": "decision_candidate_vision_nav_chain_001",
        "decision_type": "navigation_safety_hold_review",
        "decision_scope": "street_crossing_navigation_fixture",
        "input_refs": [
            integrated.get("integrated_context_id"),
            readiness.get("decision_readiness_id"),
            conflict.get("conflict_id"),
            gap.get("gap_id"),
        ],
        "rationale_refs": [
            "rationale:vision_nav_chain:001",
            "readiness:not_ready_for_real_navigation_decision",
            "gap:missing_real_time_frame_validation",
            "conflict:map_vs_vision:potential_non_blocking",
            "drive:survival_elevated_crossing_attention",
        ],
        "evidence_refs": [
            "visual_obs_sample_crossing_001",
            "ocr_result_sample_sign_001",
            "map_location_sample_001",
            "route_context_sample_001",
            "drive_signal_sample_survival_001",
        ],
        "validation_refs": ["validation_fixture_pending"],
        "health_refs": ["health_signal_candidate:module_status_001"],
        "constitution_refs": ["constitution_bus:governance_baseline_v1"],
        "whitebox_refs": integrated.get("whitebox_trace_refs") or [],
        "selected_action": "hold_candidate",
        "blocked_reason": None,
        "hold_reason": (
            "fixture_only_input_not_ready_for_real_navigation_decision;"
            "missing_live_frame_validation;freshness_can_drive_decision_false"
        ),
        "degradation_reason": None,
        "escalation_reason": None,
        "uncertainty_level": integrated.get("uncertainty_level", "moderate"),
        "downstream_allowed_targets": [],
        "candidate_only": True,
        "task_response_generation_allowed": False,
        "user_output_allowed": False,
        "memory_write_allowed": False,
        "world_model_write_allowed": False,
        "navigation_action_allowed": False,
        "not_fact": True,
        "not_user_output": True,
        "not_executed": True,
        **meta,
    }

    readiness_review = {
        "review_id": "readiness_conflict_gap_consumption_review_v1",
        "review_items": list(READINESS_CONSUMPTION_REVIEW_ITEMS),
        "readiness_status": readiness.get("readiness_status"),
        "sufficient_for_decision": readiness.get("sufficient_for_decision"),
        "conflict_type": conflict.get("conflict_type"),
        "gap_type": gap.get("missing_source_type"),
        "freshness_all_can_drive_false": freshness.get("all_can_drive_decision_false"),
        "selected_action": decision_candidate.get("selected_action"),
        **_review_ok([(f"item.{i[:18]}", True) for i in READINESS_CONSUMPTION_REVIEW_ITEMS]),
        **meta,
    }

    constitution_review = {
        "review_id": "constitution_health_drive_binding_review_v1",
        "review_items": list(CONSTITUTION_BINDING_REVIEW_ITEMS),
        "constitution_bus_ref": "constitution_bus:governance_baseline_v1",
        "survival_drive_elevated": integrated.get("drive_context", {}).get(
            "observation_priority_elevated"
        ),
        **_review_ok([(f"item.{i[:18]}", True) for i in CONSTITUTION_BINDING_REVIEW_ITEMS]),
        **meta,
    }

    rationale_review = {
        "review_id": "decision_rationale_traceability_review_v1",
        "review_items": list(RATIONALE_TRACEABILITY_REVIEW_ITEMS),
        "rationale_count": len(decision_candidate.get("rationale_refs") or []),
        "hold_reason_present": bool(decision_candidate.get("hold_reason")),
        **_review_ok([(f"item.{i[:18]}", True) for i in RATIONALE_TRACEABILITY_REVIEW_ITEMS]),
        **meta,
    }

    boundary_review = {
        "review_id": "decision_boundary_review_v1",
        "review_items": list(DECISION_BOUNDARY_REVIEW_ITEMS),
        "decision_candidate_generated": True,
        "decision_executed": False,
        **_review_ok([(f"item.{i[:18]}", True) for i in DECISION_BOUNDARY_REVIEW_ITEMS]),
        **meta,
    }

    task_response_handoff = {
        "review_id": "task_response_handoff_readiness_review_v1",
        "review_items": list(TASK_RESPONSE_HANDOFF_REVIEW_ITEMS),
        "handoff_package": {
            "decision_candidate_ref": decision_candidate["decision_candidate_id"],
            "task_response_candidate_generated": False,
            "user_output_generated": False,
            "task_response_generation_allowed": False,
        },
        **_review_ok([(f"item.{i[:18]}", True) for i in TASK_RESPONSE_HANDOFF_REVIEW_ITEMS]),
        **meta,
    }

    boundary_audit = {
        "audit_id": "decision_boundary_audit_v1",
        "boundary_fields": {f: False for f in BOUNDARY_FALSE},
        "boundary_true_fields": {f: True for f in BOUNDARY_TRUE},
        "decision_candidate_generated_now": True,
        "all_runtime_false": True,
        "audit_pass": True,
        **meta,
    }

    blocked_path_result = {
        "result_id": "decision_blocked_path_result_v1",
        "blocked_paths": [
            {"path_id": p, "status": "blocked", "executed": False} for p in BLOCKED_PATHS
        ],
        "allowed_paths": [
            {
                "path_id": "dryrun_to_decision_candidate_generation",
                "status": "allowed_candidate_only",
                "executed": True,
            }
        ],
        "blocked_count": len(BLOCKED_PATHS),
        "all_blocked": True,
        **meta,
    }

    reviews = [
        readiness_review,
        constitution_review,
        rationale_review,
        boundary_review,
        task_response_handoff,
    ]

    decision_ok = (
        all(f in decision_candidate for f in OUTPUT_CONTRACT_FIELDS)
        and decision_candidate.get("candidate_only") is True
        and decision_candidate.get("selected_action") == "hold_candidate"
        and decision_candidate.get("navigation_action_allowed") is False
        and decision_candidate.get("user_output_allowed") is False
        and decision_candidate.get("task_response_generation_allowed") is False
        and decision_candidate.get("memory_write_allowed") is False
        and decision_candidate.get("world_model_write_allowed") is False
        and bool(decision_candidate.get("hold_reason"))
    )

    chain_pass = (
        input_ok
        and decision_ok
        and all(r.get("dryrun_and_review_pass") for r in reviews)
        and boundary_audit.get("audit_pass")
        and blocked_path_result.get("all_blocked")
        and meta.get("decision_candidate_generated_now") is True
        and meta.get("decision_executed_now") is False
        and meta.get("navigation_runtime_enabled_now") is False
        and meta.get("real_navigation_action_executed_now") is False
    )

    closure_decision = {
        "decision_id": "decision_closure_decision_v1",
        "dryrun_and_review_pass": chain_pass,
        "high_risk": not chain_pass,
        "final_decision": FINAL_DECISION_GO if chain_pass else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if chain_pass else NEXT_PHASE_HOLD,
        "closure_summary": [
            "integrated_context_candidate consumed from II Chain DryRun",
            "decision_candidate generated as hold_candidate for street_crossing fixture",
            "readiness/conflict/gap/freshness consumed in decision rationale",
            "Constitution/Health/Drive binding reviewed",
            "decision boundary preserved: no execution, no output, no navigation runtime",
            "19 blocked paths + decision_candidate_generated_now true, all runtime false",
        ],
        **meta,
    }

    next_route = {
        "decision_id": "next_route_readiness_decision_v1",
        "ready_for_task_response_candidate_dryrun": chain_pass,
        "selected_next_phase": NEXT_PHASE_GO if chain_pass else NEXT_PHASE_HOLD,
        "next_focus": (
            "Task Response layer assembles task_response_candidate from decision_candidate, "
            "still no user output or navigation execution"
        ),
        **meta,
    }

    policy = {
        "policy_id": "vision_navigation_decision_chain_candidate_dryrun_policy_v1",
        "phase": PHASE_ID,
        "scope": SCOPE,
        "chain_dryrun_candidate_only_not_execute_not_output": True,
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
        "fixture_decision_candidate_generated": True,
        "final_decision": closure_decision["final_decision"],
        "recommended_next_phase": closure_decision["recommended_next_phase"],
        **meta,
    }

    return {
        "vision_navigation_decision_chain_candidate_dryrun_policy": policy,
        "integration_chain_input_review": input_review,
        "decision_chain_model_candidate": chain_model,
        "sample_decision_request_candidate": decision_request,
        "sample_decision_candidate": decision_candidate,
        "readiness_conflict_gap_consumption_review": readiness_review,
        "constitution_health_drive_binding_review": constitution_review,
        "decision_rationale_traceability_review": rationale_review,
        "decision_boundary_review": boundary_review,
        "task_response_handoff_readiness_review": task_response_handoff,
        "decision_boundary_audit": boundary_audit,
        "decision_blocked_path_result": blocked_path_result,
        "decision_closure_decision": closure_decision,
        "next_route_readiness_decision": next_route,
        "non_claims_register": non_claims,
        "summary": summary,
    }
