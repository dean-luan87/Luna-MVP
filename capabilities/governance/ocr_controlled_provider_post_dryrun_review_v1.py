# -*- coding: utf-8 -*-
"""OCR Controlled Provider Post-DryRun Review v1 — review-only."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.governance.ocr_controlled_provider_dryrun_v1 import (
    BLOCKED_PATHS,
    FINAL_DECISION_GO as DRYRUN_FINAL_GO,
    NEXT_PHASE_GO as DRYRUN_NEXT_PHASE,
    PHASE_ID as DRYRUN_PHASE,
    SCOPE as DRYRUN_SCOPE,
)
from capabilities.governance.ocr_controlled_provider_planning_v1 import (
    CONSTITUTION_BLOCKS,
    HEALTH_BINDINGS,
)

PHASE_ID = "Phase-OCR-Controlled-Provider-Post-DryRun-Review-v1-001"
REVIEW_SCOPE = "ocr_controlled_provider_post_dryrun_review_only"
SOURCE_CHAIN = "ocr_controlled_provider_post_dryrun_review_v1"

UPSTREAM_REQUIRED_FINAL = DRYRUN_FINAL_GO
UPSTREAM_NEXT_PHASE = DRYRUN_NEXT_PHASE

FINAL_DECISION_GO = (
    "OCR_CONTROLLED_PROVIDER_POST_DRYRUN_REVIEW_CLOSED_READY_FOR_AUTHORIZATION_ROADMAP_DECISION"
)
FINAL_DECISION_HOLD = "OCR_CONTROLLED_PROVIDER_POST_DRYRUN_REVIEW_HOLD_FOR_ISSUE_REVIEW"
NEXT_PHASE_GO = "Phase-OCR-Controlled-Provider-Authorization-Roadmap-Decision-v1-001"
NEXT_PHASE_HOLD = "Phase-OCR-Controlled-Provider-Issue-Review-v1-001"

EXPECTED_PROVIDER_FAMILIES: Set[str] = {
    "mock_or_fixture",
    "paddleocr_later",
    "rapidocr_later",
    "external_ocr_later",
}

BRANCH_EXPECTATIONS: Tuple[Dict[str, str], ...] = (
    {"trigger": "provider_timeout", "target": "hold_candidate"},
    {"trigger": "provider_failed", "target": "fallback_candidate"},
    {"trigger": "low_confidence", "target": "reobserve_or_retry_candidate"},
    {"trigger": "empty_result", "target": "retry_or_hold_candidate"},
    {"trigger": "unsupported_region", "target": "fallback_to_visual_candidate"},
    {"trigger": "runtime_boundary_violation", "target": "block_candidate"},
)

BOUNDARY_FALSE_REVIEW: Tuple[str, ...] = (
    "new_provider_readiness_candidate_generated_now",
    "new_ocr_request_candidate_generated_now",
    "new_ocr_roi_candidate_generated_now",
    "new_ocr_result_candidate_generated_now",
    "new_ocr_evidence_pack_candidate_generated_now",
    "ocr_controlled_provider_enabled_now",
    "ocr_controlled_provider_invoked_now",
    "ocr_provider_invoked_now",
    "paddleocr_invoked_now",
    "rapidocr_invoked_now",
    "real_ocr_provider_invoked_now",
    "ocr_model_invoked_now",
    "provider_runtime_invoked_now",
    "ocr_request_submitted_now",
    "image_read_executed_now",
    "crop_executed_now",
    "ocr_fact_generated_now",
    "world_model_written_now",
    "memory_written_now",
    "user_facing_output_generated_now",
    "tts_invoked_now",
    "task_state_committed_now",
)

NON_CLAIMS: Tuple[str, ...] = (
    "Post-DryRun Review GO ≠ OCR provider enabled",
    "Provider readiness ≠ provider invocation",
    "OCRRequest candidate ≠ request submitted",
    "ROI candidate ≠ image read/crop executed",
    "OCR result candidate ≠ OCR fact",
    "Evidence Pack candidate ≠ fact/evidence committed",
    "OCR controlled provider closure ≠ PaddleOCR/RapidOCR allowed",
    "next authorization readiness ≠ trial execution allowed",
)

DEFAULT_OUTPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/ocr_controlled_provider_post_dryrun_review"
)


def _review_meta() -> Dict[str, Any]:
    meta = {
        "ocr_controlled_provider_post_dryrun_review_only": True,
        "review_only": True,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "source_chain": SOURCE_CHAIN,
    }
    for field in BOUNDARY_FALSE_REVIEW:
        meta[field] = False
    meta["new_provider_readiness_candidate_generated_now"] = False
    meta["new_ocr_request_candidate_generated_now"] = False
    meta["new_ocr_roi_candidate_generated_now"] = False
    meta["new_ocr_result_candidate_generated_now"] = False
    meta["new_ocr_evidence_pack_candidate_generated_now"] = False
    return meta


def _try_read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def run_ocr_controlled_provider_post_dryrun_review_v1(
    *,
    ocr_controlled_provider_dryrun_root: str,
    review_output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []
    dryrun_root = Path(ocr_controlled_provider_dryrun_root).expanduser().resolve()
    dryrun_sm = _try_read_json(dryrun_root / "summary.json") or {}
    dryrun_vr = _try_read_json(dryrun_root / "verifier_report.json") or {}

    out_root = (
        Path(review_output_root).expanduser().resolve()
        if review_output_root
        else dryrun_root.parent / "ocr_controlled_provider_post_dryrun_review"
    )
    meta = {**_review_meta(), "upstream_dryrun_root": str(dryrun_root), "review_output_root": str(out_root)}

    readiness = _try_read_json(dryrun_root / "ocr_provider_readiness_candidate_samples_v1.json") or {}
    request = _try_read_json(dryrun_root / "ocr_request_candidate_samples_v1.json") or {}
    roi = _try_read_json(dryrun_root / "ocr_roi_candidate_samples_v1.json") or {}
    result = _try_read_json(dryrun_root / "ocr_result_candidate_samples_v1.json") or {}
    evidence = _try_read_json(dryrun_root / "ocr_evidence_pack_candidate_samples_v1.json") or {}
    trace = _try_read_json(dryrun_root / "ocr_candidate_chain_trace_v1.json") or {}
    health = _try_read_json(dryrun_root / "ocr_health_binding_dryrun_result_v1.json") or {}
    constitution = _try_read_json(dryrun_root / "ocr_constitution_boundary_dryrun_result_v1.json") or {}
    audit = _try_read_json(dryrun_root / "ocr_no_runtime_boundary_audit_v1.json") or {}
    blocked = _try_read_json(dryrun_root / "ocr_blocked_path_result_v1.json") or {}

    dryrun_go = dryrun_vr.get("verifier") == "GO" and dryrun_vr.get("passed") is True
    if not dryrun_go:
        blockers.append("dryrun verifier must be GO")
    if dryrun_sm.get("final_decision") != UPSTREAM_REQUIRED_FINAL:
        blockers.append("dryrun final_decision mismatch")
    if dryrun_sm.get("recommended_next_phase") != UPSTREAM_NEXT_PHASE:
        blockers.append("dryrun recommended_next_phase mismatch")
    if dryrun_sm.get("boundary_ok") is not True:
        blockers.append("dryrun boundary_ok must be true")

    for field in BOUNDARY_FALSE_REVIEW:
        if dryrun_sm.get(field) is True:
            blockers.append(f"dryrun {field} must be false")

    input_review = {
        "review_id": "ocr_controlled_provider_dryrun_input_review_v1",
        "upstream_root": str(dryrun_root),
        "upstream_phase": DRYRUN_PHASE,
        "upstream_scope": DRYRUN_SCOPE,
        "upstream_verifier_go": dryrun_go,
        "upstream_final_decision": dryrun_sm.get("final_decision"),
        "readiness_count": readiness.get("sample_count"),
        "review_pass": len(blockers) == 0,
        "blockers": blockers,
        **meta,
    }

    readiness_issues: List[Dict[str, Any]] = []
    samples = readiness.get("samples") or []
    if readiness.get("sample_count") != 4 or len(samples) != 4:
        readiness_issues.append({"issue_id": "count", "detail": "expected 4 readiness candidates"})
    families = {s.get("provider_family") for s in samples}
    if families != EXPECTED_PROVIDER_FAMILIES:
        readiness_issues.append({"issue_id": "families", "detail": f"expected {EXPECTED_PROVIDER_FAMILIES}"})
    for s in samples:
        for flag in (
            "invocation_allowed",
            "controlled_trial_required",
            "health_binding_required",
            "constitution_gate_required",
            "evidence_pack_required",
        ):
            expected = False if flag == "invocation_allowed" else True
            if s.get(flag) != expected:
                readiness_issues.append({"issue_id": s.get("provider_candidate_id"), "detail": flag})
        if s.get("provider_status") != "planned_candidate":
            readiness_issues.append({"issue_id": s.get("provider_candidate_id"), "detail": "provider_status"})

    readiness_review = {
        "review_id": "ocr_provider_readiness_review_v1",
        "sample_count": len(samples),
        "provider_families": sorted(families),
        "issues": readiness_issues,
        "review_pass": len(readiness_issues) == 0,
        **meta,
    }

    req_issues: List[Dict[str, Any]] = []
    req = (request.get("samples") or [{}])[0]
    if not request.get("samples"):
        req_issues.append({"issue_id": "missing", "detail": "OCRRequest sample required"})
    for key, val in {
        "candidate_only": True,
        "submit_allowed": False,
        "provider_invocation_allowed": False,
    }.items():
        if req.get(key) != val:
            req_issues.append({"issue_id": key, "detail": str(val)})
    for key in ("source_visual_candidate_ref", "source_frame_ref", "roi_ref", "source_chain", "ttl"):
        if not req.get(key):
            req_issues.append({"issue_id": key, "detail": "required"})

    request_review = {
        "review_id": "ocr_request_candidate_review_v1",
        "issues": req_issues,
        "review_pass": len(req_issues) == 0,
        **meta,
    }

    roi_issues: List[Dict[str, Any]] = []
    roi_s = (roi.get("samples") or [{}])[0]
    if not roi.get("samples"):
        roi_issues.append({"issue_id": "missing", "detail": "ROI sample required"})
    else:
        for key, val in {
            "candidate_only": True,
            "image_read_allowed": False,
            "crop_allowed": False,
        }.items():
            if roi_s.get(key) != val:
                roi_issues.append({"issue_id": key, "detail": str(val)})
        for key in ("bbox_or_region_ref", "reason_for_ocr", "source_chain", "ttl"):
            if not roi_s.get(key):
                roi_issues.append({"issue_id": key, "detail": "required"})
        if roi_s.get("confidence_candidate") is None:
            roi_issues.append({"issue_id": "confidence_candidate", "detail": "required"})

    roi_review = {
        "review_id": "ocr_roi_candidate_review_v1",
        "issues": roi_issues,
        "review_pass": len(roi_issues) == 0,
        **meta,
    }

    result_issues: List[Dict[str, Any]] = []
    res = (result.get("samples") or [{}])[0]
    if not result.get("samples"):
        result_issues.append({"issue_id": "missing", "detail": "OCR result sample required"})
    else:
        if res.get("provider_type") not in ("mock_or_fixture", "planned_candidate"):
            result_issues.append({"issue_id": "provider_type", "detail": "mock_or_fixture only"})
        for key, val in {
            "candidate_only": True,
            "fact_status": "not_fact",
            "write_allowed": False,
            "user_facing_output_allowed": False,
        }.items():
            if res.get(key) != val:
                result_issues.append({"issue_id": key, "detail": str(val)})
        for key in ("text_candidate", "source_roi_ref", "source_request_ref", "source_chain", "ttl"):
            if not res.get(key):
                result_issues.append({"issue_id": key, "detail": "required"})
        if res.get("confidence_candidate") is None:
            result_issues.append({"issue_id": "confidence_candidate", "detail": "required"})

    result_review = {
        "review_id": "ocr_result_candidate_review_v1",
        "issues": result_issues,
        "review_pass": len(result_issues) == 0,
        **meta,
    }

    evidence_issues: List[Dict[str, Any]] = []
    ev = (evidence.get("samples") or [{}])[0]
    if not evidence.get("samples"):
        evidence_issues.append({"issue_id": "missing", "detail": "evidence pack sample required"})
    else:
        for key, val in {
            "candidate_only": True,
            "fact_status": "not_fact",
            "validation_required": True,
            "world_model_write_allowed": False,
            "memory_write_allowed": False,
        }.items():
            if ev.get(key) != val:
                evidence_issues.append({"issue_id": key, "detail": str(val)})
        for key in (
            "ocr_request_ref",
            "roi_ref",
            "ocr_result_ref",
            "provider_readiness_ref",
            "source_chain",
            "provenance",
            "ttl",
        ):
            if not ev.get(key):
                evidence_issues.append({"issue_id": key, "detail": "required"})
        if ev.get("confidence_candidate") is None:
            evidence_issues.append({"issue_id": "confidence_candidate", "detail": "required"})

    evidence_review = {
        "review_id": "ocr_evidence_pack_candidate_review_v1",
        "issues": evidence_issues,
        "review_pass": len(evidence_issues) == 0,
        **meta,
    }

    trace_issues: List[Dict[str, Any]] = []
    if trace.get("chain_pass") is not True:
        trace_issues.append({"issue_id": "chain_pass", "detail": "must be true"})

    trace_review = {
        "review_id": "ocr_candidate_chain_trace_review_v1",
        "chain_pass": trace.get("chain_pass"),
        "issues": trace_issues,
        "review_pass": len(trace_issues) == 0,
        **meta,
    }

    branch_issues: List[Dict[str, Any]] = []
    branch_files = {
        "provider_timeout": ("ocr_timeout_fallback_branch_result_v1.json", "hold_candidate"),
        "low_confidence": ("ocr_low_confidence_branch_result_v1.json", "reobserve_or_retry_candidate"),
        "empty_result": ("ocr_empty_result_branch_result_v1.json", "retry_or_hold_candidate"),
        "unsupported_region": ("ocr_unsupported_region_branch_result_v1.json", "fallback_to_visual_candidate"),
        "runtime_boundary_violation": (
            "ocr_runtime_boundary_violation_branch_result_v1.json",
            "block_candidate",
        ),
    }
    for trigger, (fname, target) in branch_files.items():
        data = _try_read_json(dryrun_root / fname) or {}
        if data.get("branch_pass") is not True or data.get("target_candidate") != target:
            branch_issues.append({"issue_id": trigger, "detail": "branch file mismatch"})

    health_routes = {r.get("trigger"): r for r in health.get("routes") or []}
    for exp in BRANCH_EXPECTATIONS:
        row = health_routes.get(exp["trigger"])
        if not row or row.get("target_candidate") != exp["target"] or row.get("executed_now") is True:
            branch_issues.append({"issue_id": exp["trigger"], "detail": "health route mismatch"})

    if health.get("routing_pass") is not True:
        branch_issues.append({"issue_id": "health_routing", "detail": "routing_pass false"})

    branch_review = {
        "review_id": "ocr_branch_review_v1",
        "branches_expected": list(BRANCH_EXPECTATIONS),
        "fallback_executed_now": False,
        "retry_executed_now": False,
        "provider_switch_executed_now": False,
        "issues": branch_issues,
        "review_pass": len(branch_issues) == 0,
        **meta,
    }

    health_issues: List[Dict[str, Any]] = []
    if health.get("routing_pass") is not True or len(health.get("routes") or []) != 6:
        health_issues.append({"issue_id": "routes", "detail": "6 routes required"})
    if health.get("no_automatic_fallback") is not True:
        health_issues.append({"issue_id": "no_fallback", "detail": "must be true"})

    health_review = {
        "review_id": "ocr_health_binding_review_v1",
        "route_count": len(health.get("routes") or []),
        "issues": health_issues,
        "review_pass": len(health_issues) == 0,
        **meta,
    }

    constitution_issues: List[Dict[str, Any]] = []
    block_rows = constitution.get("blocks") or []
    blocks_map = {b.get("block_id"): b for b in block_rows if b.get("block_id")}
    if constitution.get("all_blocked") is not True:
        constitution_issues.append({"issue_id": "all_blocked", "detail": "must be true"})
    for spec in CONSTITUTION_BLOCKS:
        bid = spec["block_id"]
        row = blocks_map.get(bid)
        if not row or row.get("blocked") is not True:
            constitution_issues.append({"issue_id": bid, "detail": "must be blocked"})

    constitution_review = {
        "review_id": "ocr_constitution_boundary_review_v1",
        "issues": constitution_issues,
        "review_pass": len(constitution_issues) == 0,
        **meta,
    }

    runtime_issues: List[Dict[str, Any]] = []
    if audit.get("audit_pass") is not True:
        runtime_issues.append({"issue_id": "audit_pass", "detail": "must pass"})
    for check in audit.get("checks") or []:
        if check.get("passed") is not True:
            runtime_issues.append({"issue_id": check.get("check_id"), "detail": "failed"})

    runtime_review = {
        "review_id": "ocr_no_runtime_boundary_review_v1",
        "issues": runtime_issues,
        "review_pass": len(runtime_issues) == 0,
        **meta,
    }

    blocked_issues: List[Dict[str, Any]] = []
    paths = {p.get("path_id"): p for p in blocked.get("paths") or []}
    if blocked.get("all_blocked") is not True or len(paths) != len(BLOCKED_PATHS):
        blocked_issues.append({"issue_id": "count", "detail": f"expected {len(BLOCKED_PATHS)} paths"})
    for pid in BLOCKED_PATHS:
        row = paths.get(pid)
        if not row or row.get("blocked") is not True:
            blocked_issues.append({"issue_id": pid, "detail": "must be blocked=true"})

    blocked_review = {
        "review_id": "ocr_blocked_path_review_v1",
        "paths_total": len(BLOCKED_PATHS),
        "issues": blocked_issues,
        "review_pass": len(blocked_issues) == 0,
        **meta,
    }

    reviews_pass = (
        len(blockers) == 0
        and input_review.get("review_pass")
        and readiness_review.get("review_pass")
        and request_review.get("review_pass")
        and roi_review.get("review_pass")
        and result_review.get("review_pass")
        and evidence_review.get("review_pass")
        and trace_review.get("review_pass")
        and branch_review.get("review_pass")
        and health_review.get("review_pass")
        and constitution_review.get("review_pass")
        and runtime_review.get("review_pass")
        and blocked_review.get("review_pass")
    )
    boundary_ok = reviews_pass

    closure = {
        "closure_id": "ocr_controlled_provider_closure_decision_v1",
        "ocr_controlled_provider_dryrun_closed": boundary_ok,
        "ocr_candidate_chain_trusted": boundary_ok,
        "final_decision": FINAL_DECISION_GO if boundary_ok else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if boundary_ok else NEXT_PHASE_HOLD,
        **meta,
    }

    next_readiness = {
        "readiness_id": "next_route_readiness_decision_v1",
        "ready_for_authorization_roadmap_decision": boundary_ok,
        "do_not_start_provider_trial_now": True,
        "do_not_invoke_paddleocr_or_rapidocr": True,
        "recommended_next_phase": NEXT_PHASE_GO if boundary_ok else PHASE_ID,
        "final_decision": closure["final_decision"],
        "rationale": (
            "After dryrun closure, decide authorization planning vs provider selection / "
            "local dependency / environment readiness — not trial execution"
        ),
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
        + [i["issue_id"] for i in readiness_issues + req_issues + blocked_issues],
        "final_decision": closure["final_decision"],
        "recommended_next_phase": closure["recommended_next_phase"],
        "high_risk_count": 0 if boundary_ok else 1,
        "ocr_controlled_provider_dryrun_closed": boundary_ok,
        "ocr_candidate_chain_trusted": boundary_ok,
        **meta,
    }

    return {
        "ocr_controlled_provider_dryrun_input_review": input_review,
        "ocr_provider_readiness_review": readiness_review,
        "ocr_request_candidate_review": request_review,
        "ocr_roi_candidate_review": roi_review,
        "ocr_result_candidate_review": result_review,
        "ocr_evidence_pack_candidate_review": evidence_review,
        "ocr_candidate_chain_trace_review": trace_review,
        "ocr_branch_review": branch_review,
        "ocr_health_binding_review": health_review,
        "ocr_constitution_boundary_review": constitution_review,
        "ocr_no_runtime_boundary_review": runtime_review,
        "ocr_blocked_path_review": blocked_review,
        "ocr_controlled_provider_closure_decision": closure,
        "next_route_readiness_decision": next_readiness,
        "non_claims_register": non_claims,
        "summary": summary,
    }
