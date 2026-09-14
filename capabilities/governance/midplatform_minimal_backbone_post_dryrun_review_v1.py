# -*- coding: utf-8 -*-
"""Midplatform Minimal Backbone Post-DryRun Review v1 — trust review only (no replan)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.midplatform_minimal_backbone_dryrun_v1 import (
    BLOCK_CHECKS,
    FINAL_DECISION_GO as DRYRUN_FINAL_GO,
    NEXT_PHASE_GO as DRYRUN_NEXT_PHASE,
    PHASE_ID as DRYRUN_PHASE,
    P0_MODULES,
    SCOPE as DRYRUN_SCOPE,
)
from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID

PHASE_ID = "Phase-Midplatform-Minimal-Backbone-Post-DryRun-Review-v1-001"
REVIEW_SCOPE = "midplatform_minimal_backbone_post_dryrun_review_only"
SOURCE_CHAIN = "midplatform_minimal_backbone_post_dryrun_review_v1"

UPSTREAM_PHASE = DRYRUN_PHASE
UPSTREAM_REQUIRED_FINAL = DRYRUN_FINAL_GO
UPSTREAM_NEXT_PHASE = DRYRUN_NEXT_PHASE

FINAL_DECISION_GO = "MIDPLATFORM_MINIMAL_BACKBONE_POST_DRYRUN_REVIEW_CLOSED_READY_FOR_NEXT_ROUTE_DECISION"
FINAL_DECISION_HOLD = "MIDPLATFORM_MINIMAL_BACKBONE_POST_DRYRUN_REVIEW_HOLD_FOR_ISSUE_REVIEW"
NEXT_PHASE_GO = "Phase-Midplatform-Post-Backbone-Roadmap-Decision-v1-001"

ROUTE_OPTION_A = "Phase-Task-Response-Candidate-Single-Chain-Trial-Via-Midplatform-v1-001"
ROUTE_OPTION_B = "Phase-Model-Management-Layer-Recovery-Planning-v1-001"
PREFERRED_ROUTE = "A"

FLOW_IDS: Tuple[str, ...] = (
    "Flow_A_vision_candidate_intake",
    "Flow_B_ocr_mock_candidate_intake",
    "Flow_C_navigation_guidance_candidate_intake",
)

CANDIDATE_TYPES: Tuple[str, ...] = (
    "visual_observation_candidate",
    "ocr_result_candidate",
    "navigation_guidance_candidate",
)

DRYRUN_BOUNDARY_FALSE_FIELDS: Tuple[str, ...] = (
    "runtime_enabled_now",
    "real_runtime_enabled_now",
    "model_runtime_invoked_now",
    "live_camera_enabled_now",
    "ocr_provider_invoked_now",
    "navigation_action_triggered_now",
    "map_write_executed_now",
    "route_commit_executed_now",
    "task_state_committed_now",
    "task_manager_committed_now",
    "active_drive_execution_enabled_now",
    "drive_action_executed_now",
    "tts_invoked_now",
    "llm_invoked_now",
    "user_facing_output_generated_now",
    "world_model_written_now",
    "memory_written_now",
    "library_write_executed_now",
    "hive_sync_executed_now",
    "scene_delta_generated_now",
)

NON_CLAIMS: Tuple[str, ...] = (
    "Post-DryRun Review GO ≠ minimal backbone production runtime",
    "Three flow pass ≠ P0 contracts implemented under capabilities/midplatform/",
    "Ten blocks enforced in dryrun ≠ live provider or navigation action allowed",
    "DryRun closed ≠ Task response single-chain started without Post-Backbone Roadmap Decision",
    "Route readiness ≠ skipping Phase-Midplatform-Post-Backbone-Roadmap-Decision-v1-001",
    "Preferred route A is advisory until roadmap decision phase",
    "task_response_candidate still deferred until roadmap selects A",
    "OCR mock_or_fixture_only in dryrun ≠ real OCR provider",
    "Navigation guidance not_action/not_user_output ≠ navigation runtime",
)

DEFAULT_OUTPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_minimal_backbone_post_dryrun_review"
)


def _not_fact() -> Dict[str, Any]:
    return {
        "candidate_only": True,
        "fact_status": "not_fact",
        "write_allowed": False,
        "runtime_action_allowed": False,
        "user_facing_output_allowed": False,
    }


def _boundary_meta() -> Dict[str, Any]:
    return {
        "midplatform_minimal_backbone_post_dryrun_review_only": True,
        "review_only": True,
        "simulated": True,
        "dryrun_only": True,
        "runtime_enabled_now": False,
        "real_runtime_enabled_now": False,
        "model_runtime_invoked_now": False,
        "live_camera_enabled_now": False,
        "ocr_provider_invoked_now": False,
        "navigation_action_triggered_now": False,
        "map_write_executed_now": False,
        "route_commit_executed_now": False,
        "task_state_committed_now": False,
        "task_manager_committed_now": False,
        "active_drive_execution_enabled_now": False,
        "drive_action_executed_now": False,
        "tts_invoked_now": False,
        "llm_invoked_now": False,
        "user_facing_output_generated_now": False,
        "world_model_written_now": False,
        "memory_written_now": False,
        "library_write_executed_now": False,
        "hive_sync_executed_now": False,
        "scene_delta_generated_now": False,
        "module_implementation_started_now": False,
        "p0_gap_implemented_now": False,
        "task_response_candidate_chain_deferred_now": True,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


def _try_read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def _record_by_type(records: List[Dict[str, Any]], ctype: str) -> Optional[Dict[str, Any]]:
    for rec in records:
        if rec.get("candidate_type") == ctype:
            return rec
    return None


def run_midplatform_minimal_backbone_post_dryrun_review_v1(
    *,
    midplatform_minimal_backbone_dryrun_root: str,
    review_output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []
    dryrun_root = Path(midplatform_minimal_backbone_dryrun_root).expanduser().resolve()
    out_root = (
        Path(review_output_root).expanduser().resolve()
        if review_output_root
        else dryrun_root.parent / "midplatform_minimal_backbone_post_dryrun_review"
    )

    meta = {
        **_boundary_meta(),
        "upstream_dryrun_root": str(dryrun_root),
        "review_output_root": str(out_root),
    }

    dryrun_sm = _try_read_json(dryrun_root / "summary.json") or {}
    dryrun_vr = _try_read_json(dryrun_root / "verifier_report.json") or {}
    trace = _try_read_json(dryrun_root / "minimal_backbone_flow_trace_v1.json") or {}
    gap = _try_read_json(dryrun_root / "minimal_backbone_gap_consumption_result_v1.json") or {}
    readiness = _try_read_json(dryrun_root / "minimal_backbone_dryrun_readiness_decision_v1.json") or {}
    memory = _try_read_json(dryrun_root / "memory_support_access_block_review_v1.json") or {}
    runtime_bundle = _try_read_json(dryrun_root / "runtime_boundary_decision_v1.json") or {}
    intake_bundle = _try_read_json(dryrun_root / "candidate_intake_record_v1.json") or {}
    evidence_bundle = _try_read_json(dryrun_root / "evidence_governance_record_v1.json") or {}
    constitution_bundle = _try_read_json(dryrun_root / "constitution_gate_review_v1.json") or {}
    task_bundle = _try_read_json(dryrun_root / "task_routing_candidate_v1.json") or {}
    guidance_bundle = _try_read_json(dryrun_root / "guidance_candidate_queue_item_v1.json") or {}
    arbitration_bundle = _try_read_json(dryrun_root / "output_arbitration_candidate_v1.json") or {}

    dryrun_verifier_go = dryrun_vr.get("verifier") == "GO" and dryrun_vr.get("passed") is True

    if not dryrun_verifier_go:
        blockers.append("dryrun verifier must be GO")
    if dryrun_sm.get("final_decision") != UPSTREAM_REQUIRED_FINAL:
        blockers.append("dryrun final_decision mismatch")
    if dryrun_sm.get("recommended_next_phase") != UPSTREAM_NEXT_PHASE:
        blockers.append("dryrun recommended_next_phase mismatch")
    if dryrun_sm.get("simulated") is not True:
        blockers.append("dryrun simulated must be true")
    if trace.get("flows_all_pass") is not True:
        blockers.append("flows_all_pass required")
    if readiness.get("block_verification_pass") is not True:
        blockers.append("dryrun block_verification_pass required")
    if gap.get("p0_implemented_count", -1) != 0:
        blockers.append("p0_implemented_count must be 0")
    if task_bundle.get("task_response_candidate_deferred") is not True:
        blockers.append("task_response_candidate must remain deferred in dryrun")

    for field in DRYRUN_BOUNDARY_FALSE_FIELDS:
        if dryrun_sm.get(field) is True:
            blockers.append(f"dryrun {field} must be false")

    input_review = {
        "review_id": "minimal_backbone_dryrun_input_review_v1",
        "upstream_root": str(dryrun_root),
        "upstream_verifier": dryrun_vr.get("verifier"),
        "upstream_verifier_go": dryrun_verifier_go,
        "upstream_phase": dryrun_sm.get("phase"),
        "upstream_scope": dryrun_sm.get("scope"),
        "upstream_final_decision": dryrun_sm.get("final_decision"),
        "upstream_recommended_next_phase": dryrun_sm.get("recommended_next_phase"),
        "upstream_boundary_ok": dryrun_sm.get("boundary_ok"),
        "upstream_simulated": dryrun_sm.get("simulated"),
        "upstream_flows_all_pass": trace.get("flows_all_pass"),
        "task_response_candidate_deferred": task_bundle.get("task_response_candidate_deferred"),
        "p0_contract_level_only": gap.get("p0_implemented_count") == 0,
        "review_pass": len(blockers) == 0,
        "blockers": blockers,
        **meta,
    }

    by_flow = {f.get("flow_id"): f for f in trace.get("flows") or []}
    flow_rows: List[Dict[str, Any]] = []
    flow_issues: List[Dict[str, Any]] = []
    for fid in FLOW_IDS:
        row = by_flow.get(fid)
        passed = row is not None and row.get("flow_pass") is True
        steps_pass = all((s.get("pass") is True) for s in (row or {}).get("steps") or [])
        ok_flow = passed and steps_pass
        flow_rows.append(
            {
                "flow_id": fid,
                "flow_pass": passed,
                "all_steps_pass": steps_pass,
                "trusted": ok_flow,
            }
        )
        if not ok_flow:
            flow_issues.append({"issue_id": fid, "detail": "flow must pass with all steps"})

    flow_abc_review = {
        "review_id": "flow_abc_review_v1",
        "flows": flow_rows,
        "flows_all_pass": all(r["trusted"] for r in flow_rows),
        "three_candidate_flows_trusted": len(flow_issues) == 0,
        "issues": flow_issues,
        "review_pass": len(flow_issues) == 0,
        **meta,
    }

    intake_records = intake_bundle.get("records") or []
    intake_issues: List[Dict[str, Any]] = []
    if len(intake_records) != 3:
        intake_issues.append({"issue_id": "intake_count", "detail": "expected 3 intake records"})
    for ctype in CANDIDATE_TYPES:
        rec = _record_by_type(intake_records, ctype)
        if not rec or rec.get("intake_pass") is not True:
            intake_issues.append({"issue_id": f"intake:{ctype}", "detail": "intake_pass required"})
        elif rec.get("candidate_only") is not True or rec.get("fact_status") != "not_fact":
            intake_issues.append({"issue_id": f"intake_contract:{ctype}", "detail": "candidate_only not_fact"})

    intake_review = {
        "review_id": "candidate_intake_review_v1",
        "bundle_complete": len(intake_records) == 3,
        "records": [
            {
                "candidate_type": r.get("candidate_type"),
                "candidate_id": r.get("candidate_id"),
                "intake_pass": r.get("intake_pass"),
                "candidate_only": r.get("candidate_only"),
                "fact_status": r.get("fact_status"),
            }
            for r in intake_records
        ],
        "issues": intake_issues,
        "review_pass": len(intake_issues) == 0,
        **meta,
    }

    evidence_records = evidence_bundle.get("records") or []
    evidence_issues: List[Dict[str, Any]] = []
    if len(evidence_records) != 3:
        evidence_issues.append({"issue_id": "evidence_count", "detail": "expected 3 evidence records"})
    ocr_ev = _record_by_type(evidence_records, "ocr_result_candidate")
    if not ocr_ev or ocr_ev.get("mock_or_fixture_status") != "mock_or_fixture_only":
        evidence_issues.append({"issue_id": "ocr_mock", "detail": "ocr mock_or_fixture_only required"})
    for rec in evidence_records:
        if rec.get("fact_write_allowed") is True:
            evidence_issues.append(
                {"issue_id": f"fact_write:{rec.get('candidate_type')}", "detail": "fact_write_allowed false"}
            )

    evidence_review = {
        "review_id": "evidence_governance_review_v1",
        "bundle_complete": len(evidence_records) == 3,
        "ocr_mock_or_fixture_only": ocr_ev.get("mock_or_fixture_status") if ocr_ev else None,
        "records": evidence_records,
        "issues": evidence_issues,
        "review_pass": len(evidence_issues) == 0,
        **meta,
    }

    constitution_reviews = constitution_bundle.get("reviews") or []
    constitution_issues: List[Dict[str, Any]] = []
    if len(constitution_reviews) != 3:
        constitution_issues.append({"issue_id": "constitution_count", "detail": "expected 3 reviews"})
    nav_const = _record_by_type(constitution_reviews, "navigation_guidance_candidate")
    for rev in constitution_reviews:
        if rev.get("constitution_pass") is not True:
            constitution_issues.append(
                {"issue_id": f"constitution:{rev.get('candidate_type')}", "detail": "constitution_pass required"}
            )
        if rev.get("fact_upgrade_blocked") is not True:
            constitution_issues.append(
                {"issue_id": f"fact_block:{rev.get('candidate_type')}", "detail": "fact_upgrade_blocked required"}
            )
    if nav_const and nav_const.get("action_boundary_gate") != "pass":
        constitution_issues.append({"issue_id": "nav_action_gate", "detail": "navigation action boundary pass"})
    if nav_const and nav_const.get("output_boundary_gate") != "pass":
        constitution_issues.append({"issue_id": "nav_output_gate", "detail": "navigation output boundary pass"})

    constitution_review = {
        "review_id": "constitution_gate_review_result_v1",
        "bundle_complete": len(constitution_reviews) == 3,
        "all_constitution_pass": all(r.get("constitution_pass") for r in constitution_reviews),
        "navigation_not_action_not_user_output": nav_const is not None
        and nav_const.get("action_boundary_gate") == "pass"
        and nav_const.get("output_boundary_gate") == "pass",
        "reviews": constitution_reviews,
        "issues": constitution_issues,
        "review_pass": len(constitution_issues) == 0,
        **meta,
    }

    task_records = task_bundle.get("records") or []
    guidance_items = guidance_bundle.get("items") or []
    tg_issues: List[Dict[str, Any]] = []
    if task_bundle.get("task_response_candidate_deferred") is not True:
        tg_issues.append({"issue_id": "task_deferred", "detail": "task_response_candidate_deferred"})
    if any(r.get("task_commit_allowed") is True for r in task_records):
        tg_issues.append({"issue_id": "task_commit", "detail": "task_commit_allowed must be false"})
    if len(guidance_items) != 3:
        tg_issues.append({"issue_id": "guidance_count", "detail": "expected 3 guidance items"})
    nav_guid = _record_by_type(guidance_items, "navigation_guidance_candidate")
    for item in guidance_items:
        if item.get("user_facing_output_allowed") is True:
            tg_issues.append(
                {"issue_id": f"guidance_output:{item.get('candidate_type')}", "detail": "no user output"}
            )

    task_guidance_review = {
        "review_id": "task_routing_and_guidance_queue_review_v1",
        "task_routing_records": task_records,
        "task_commit_allowed_any": any(r.get("task_commit_allowed") for r in task_records),
        "task_response_candidate_deferred": task_bundle.get("task_response_candidate_deferred"),
        "guidance_queue_items": guidance_items,
        "guidance_bundle_complete": len(guidance_items) == 3,
        "navigation_user_facing_output_allowed": nav_guid.get("user_facing_output_allowed") if nav_guid else None,
        "issues": tg_issues,
        "review_pass": len(tg_issues) == 0,
        **meta,
    }

    arbitrations = arbitration_bundle.get("candidates") or []
    arb_issues: List[Dict[str, Any]] = []
    if len(arbitrations) != 3:
        arb_issues.append({"issue_id": "arbitration_count", "detail": "expected 3 arbitration candidates"})
    for cand in arbitrations:
        if cand.get("output_allowed") is not False:
            arb_issues.append(
                {"issue_id": f"output_allowed:{cand.get('candidate_type')}", "detail": "output_allowed false"}
            )
        if cand.get("speech_response_candidate_generated_now") is True:
            arb_issues.append({"issue_id": "tts_candidate", "detail": "no speech response"})

    arbitration_review = {
        "review_id": "output_arbitration_review_v1",
        "bundle_complete": len(arbitrations) == 3,
        "all_output_allowed_false": all(c.get("output_allowed") is False for c in arbitrations),
        "candidates": arbitrations,
        "issues": arb_issues,
        "review_pass": len(arb_issues) == 0,
        **meta,
    }

    runtime_issues: List[Dict[str, Any]] = []
    decisions = runtime_bundle.get("decisions") or []
    for dec in decisions:
        if dec.get("real_runtime_allowed") is True:
            runtime_issues.append({"issue_id": "real_runtime", "detail": "real_runtime_allowed false"})
        if dec.get("action_execution_allowed") is True:
            runtime_issues.append({"issue_id": "action_exec", "detail": "action_execution_allowed false"})
        if dec.get("memory_write_allowed") is True or dec.get("world_model_write_allowed") is True:
            runtime_issues.append({"issue_id": "writes", "detail": "writes blocked"})
        if dec.get("model_invocation_allowed") is True or dec.get("provider_invocation_allowed") is True:
            runtime_issues.append({"issue_id": "model_provider", "detail": "invocation blocked"})

    runtime_review = {
        "review_id": "runtime_boundary_review_v1",
        "decisions_reviewed": len(decisions),
        "runtime_boundary_pass": readiness.get("runtime_boundary_pass") is True,
        "blocks_runtime_action_fact_write": len(runtime_issues) == 0,
        "decisions": decisions,
        "issues": runtime_issues,
        "review_pass": len(runtime_issues) == 0 and readiness.get("runtime_boundary_pass") is True,
        **meta,
    }

    block_rows: List[Dict[str, Any]] = []
    block_issues: List[Dict[str, Any]] = []
    for check_id in BLOCK_CHECKS:
        blocked = readiness.get("block_verification_pass") is True
        block_rows.append({"check_id": check_id, "blocked": blocked, "observed_now": False})
        if not blocked:
            block_issues.append({"issue_id": check_id, "detail": "must be blocked"})

    blocked_path_review = {
        "review_id": "blocked_path_review_v1",
        "block_checks": block_rows,
        "block_checks_total": len(BLOCK_CHECKS),
        "all_ten_blocks_blocked": len(block_issues) == 0 and readiness.get("block_verification_pass") is True,
        "memory_writes_blocked": memory.get("all_writes_blocked") is True,
        "support_layer_direct_write_blocked": memory.get("support_layer_direct_write_blocked") is True,
        "issues": block_issues,
        "review_pass": len(block_issues) == 0 and memory.get("all_writes_blocked") is True,
        **meta,
    }

    p0_rows: List[Dict[str, Any]] = []
    p0_issues: List[Dict[str, Any]] = []
    gap_by_mod = {r.get("gap_module"): r for r in gap.get("rows") or []}
    for mod in P0_MODULES:
        row = gap_by_mod.get(mod)
        if mod == "midplatform_minimal_backbone_dryrun_runner_verifier":
            contract_only = row is not None and dryrun_verifier_go
        else:
            contract_only = (
                row is not None
                and row.get("implemented_now") is False
                and row.get("satisfied_for_dryrun") is True
            )
        if not contract_only:
            p0_issues.append({"issue_id": mod, "detail": "contract-level consumption only"})
        p0_rows.append(
            {
                "gap_module": mod,
                "registered": row is not None,
                "implemented_now": (row or {}).get("implemented_now"),
                "contract_level_consumption_only": contract_only,
            }
        )

    p0_review = {
        "review_id": "p0_gap_contract_consumption_review_v1",
        "p0_gaps_total": gap.get("p0_gaps_total"),
        "p0_implemented_count": gap.get("p0_implemented_count"),
        "consumption_pass": gap.get("consumption_pass") is True,
        "rows": p0_rows,
        "issues": p0_issues,
        "review_pass": len(p0_issues) == 0,
        **meta,
    }

    pillar_flows = flow_abc_review.get("review_pass") is True
    pillar_blocks = blocked_path_review.get("review_pass") is True
    pillar_input = input_review.get("review_pass") is True
    layer_reviews_pass = all(
        r.get("review_pass")
        for r in (
            intake_review,
            evidence_review,
            constitution_review,
            task_guidance_review,
            arbitration_review,
            runtime_review,
            p0_review,
        )
    )
    boundary_ok = pillar_input and pillar_flows and pillar_blocks and layer_reviews_pass

    next_route = {
        "decision_id": "next_route_readiness_decision_v1",
        "minimal_backbone_dryrun_closed": boundary_ok,
        "ready_for_next_route_decision": boundary_ok,
        "three_candidate_flows_trusted": pillar_flows,
        "ten_blocks_enforced": pillar_blocks,
        "recommended_next_phase": NEXT_PHASE_GO if boundary_ok else PHASE_ID,
        "route_option_a": ROUTE_OPTION_A,
        "route_option_b": ROUTE_OPTION_B,
        "preferred_route": PREFERRED_ROUTE,
        "preferred_route_label": "Task response candidate into midplatform output layer",
        "alternate_route_label": "Model Management Layer Recovery Planning",
        "do_not_skip_roadmap_decision": True,
        "do_not_open_task_response_directly": True,
        "final_decision": FINAL_DECISION_GO if boundary_ok else FINAL_DECISION_HOLD,
        **meta,
    }

    non_claims = {
        "register_id": "non_claims_register_v1",
        "non_claims": list(NON_CLAIMS),
        **meta,
    }

    summary = {
        "phase": PHASE_ID,
        "review_scope": REVIEW_SCOPE,
        "boundary_ok": boundary_ok,
        "violations": blockers
        + [i["issue_id"] for i in flow_issues + intake_issues + evidence_issues + constitution_issues + tg_issues + arb_issues + runtime_issues + block_issues + p0_issues],
        "final_decision": next_route["final_decision"],
        "recommended_next_phase": next_route["recommended_next_phase"],
        "minimal_backbone_dryrun_closed": boundary_ok,
        "three_candidate_flows_trusted": pillar_flows,
        "ten_blocks_all_blocked": pillar_blocks,
        "ready_for_post_backbone_roadmap_decision": boundary_ok,
        "high_risk_count": 0 if boundary_ok else 1,
        **meta,
    }

    return {
        "minimal_backbone_dryrun_input_review": input_review,
        "flow_abc_review": flow_abc_review,
        "candidate_intake_review": intake_review,
        "evidence_governance_review": evidence_review,
        "constitution_gate_review_result": constitution_review,
        "task_routing_and_guidance_queue_review": task_guidance_review,
        "output_arbitration_review": arbitration_review,
        "runtime_boundary_review": runtime_review,
        "blocked_path_review": blocked_path_review,
        "p0_gap_contract_consumption_review": p0_review,
        "next_route_readiness_decision": next_route,
        "non_claims_register": non_claims,
        "summary": summary,
    }
