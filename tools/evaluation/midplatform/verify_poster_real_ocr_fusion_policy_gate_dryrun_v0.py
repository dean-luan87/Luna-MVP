#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for Poster Real OCR Fusion Policy Gate DryRun v0."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, List


FORBIDDEN_ALLOWED = frozenset({"world_model_write", "auto_approve", "scene_delta_write", "navigation_decision"})
BLOCKING_REQ_IDS = frozenset(
    {
        "review_decision_required",
        "ttl_policy_required",
        "source_validation_required",
        "user_visible_uncertainty_required",
    }
)


def _find_ws_root() -> Path:
    here = Path(__file__).resolve()
    for parent in here.parents:
        if (parent / "capabilities" / "midplatform").is_dir():
            if str(parent) not in sys.path:
                sys.path.insert(0, str(parent))
            return parent
    return here.parents[3]


def _require_abs(p: str, label: str) -> Path:
    pp = Path(p).expanduser()
    if not pp.is_absolute():
        raise SystemExit(f"ERROR: {label} must be absolute, got: {p}")
    return pp.resolve()


def _read_json(p: Path) -> Any:
    return json.loads(p.read_text(encoding="utf-8"))


def _write_json(path: Path, obj: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _req_by_id(matrix: dict, req_id: str) -> dict:
    for row in matrix.get("rows") or []:
        if isinstance(row, dict) and row.get("requirement_id") == req_id:
            return row
    return {}


def main() -> int:
    _find_ws_root()
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke-root", required=True)
    args = ap.parse_args()

    root = _require_abs(args.smoke_root, "--smoke-root")
    blockers: List[str] = []

    paths = {
        "summary": root / "poster_real_ocr_fusion_policy_gate_dryrun_summary.json",
        "candidate": root / "poster_real_ocr_fusion_policy_gate_candidate.json",
        "req_matrix": root / "poster_real_ocr_fusion_policy_requirement_matrix.json",
        "decision": root / "poster_real_ocr_fusion_policy_gate_decision_matrix.json",
        "ttl_carryover": root / "poster_real_ocr_fusion_policy_ttl_carryover_report.json",
        "review_carryover": root / "poster_real_ocr_fusion_policy_review_queue_carryover_report.json",
        "commercial": root / "poster_real_ocr_fusion_policy_commercial_temporal_report.json",
        "visual": root / "poster_real_ocr_fusion_policy_visual_symbol_report.json",
        "scene_delta": root / "poster_real_ocr_fusion_policy_scene_delta_eligibility_report.json",
        "chain": root / "poster_real_ocr_fusion_policy_source_chain_report.json",
        "metrics": root / "poster_real_ocr_fusion_policy_metrics_candidate_report.json",
        "benchmark": root / "poster_real_ocr_fusion_policy_benchmark_link_report.json",
        "health": root / "poster_real_ocr_fusion_policy_system_health_link_report.json",
        "boundary": root / "poster_real_ocr_fusion_policy_no_write_boundary_report.json",
        "sim": root / "poster_real_ocr_fusion_policy_simulation_context_report.json",
        "non_claims": root / "poster_real_ocr_fusion_policy_non_claims_report.json",
        "followups": root / "poster_real_ocr_fusion_policy_open_followups.json",
        "audit": root / "poster_real_ocr_fusion_policy_audit_report.json",
    }

    for label, p in paths.items():
        if not p.is_file():
            blockers.append(f"missing:{label}")

    if blockers:
        _write_json(
            root / "poster_real_ocr_fusion_policy_verifier_report.json",
            {"verdict": "NO_GO", "blockers": blockers, "checks_passed": 0},
        )
        print(json.dumps({"verdict": "NO_GO", "blockers": blockers}, ensure_ascii=False))
        return 2

    summary = _read_json(paths["summary"])
    candidate = _read_json(paths["candidate"])
    req_matrix = _read_json(paths["req_matrix"])
    decision = _read_json(paths["decision"])
    ttl_carryover = _read_json(paths["ttl_carryover"])
    review_carryover = _read_json(paths["review_carryover"])
    commercial = _read_json(paths["commercial"])
    visual = _read_json(paths["visual"])
    scene_delta = _read_json(paths["scene_delta"])
    chain = _read_json(paths["chain"])
    metrics = _read_json(paths["metrics"])
    benchmark = _read_json(paths["benchmark"])
    health = _read_json(paths["health"])
    boundary = _read_json(paths["boundary"])
    sim = _read_json(paths["sim"])
    non_claims = _read_json(paths["non_claims"])
    followups = _read_json(paths["followups"])
    audit = _read_json(paths["audit"])

    if summary.get("gate_scope") != "policy_gate_dryrun_only":
        blockers.append("gate_scope")
    if summary.get("policy_gate_evaluated") is not True:
        blockers.append("policy_gate_evaluated")
    if summary.get("policy_candidate_count") != 1:
        blockers.append("policy_candidate_count")
    if summary.get("policy_gate_passed_count") != 0:
        blockers.append("policy_gate_passed_count")
    if summary.get("policy_gate_hold_count") != 1:
        blockers.append("policy_gate_hold_count")
    if summary.get("approval_granted_count") != 0:
        blockers.append("approval_granted_count")
    if summary.get("auto_approve_invoked") is not False:
        blockers.append("auto_approve_invoked")
    if summary.get("fusion_committed") is not False:
        blockers.append("fusion_committed")
    if summary.get("scene_delta_candidate_generated") is not False:
        blockers.append("scene_delta")

    if candidate.get("policy_gate_status") != "evaluated_dryrun":
        blockers.append("policy_gate_status")
    if candidate.get("policy_gate_decision") != "hold_for_review":
        blockers.append("policy_gate_decision")
    if candidate.get("policy_gate_passed") is not False:
        blockers.append("policy_gate_passed")
    if candidate.get("scene_delta_candidate_allowed") is not False:
        blockers.append("scene_delta_candidate_allowed")
    if candidate.get("approval_status") != "not_approved":
        blockers.append("approval_status")
    if candidate.get("write_allowed") is not False:
        blockers.append("write_allowed")
    allowed = candidate.get("allowed_next_steps") if isinstance(candidate.get("allowed_next_steps"), list) else []
    for step in allowed:
        if str(step) in FORBIDDEN_ALLOWED or "world_model" in str(step):
            blockers.append(f"forbidden_allowed_step:{step}")

    for req_id in BLOCKING_REQ_IDS:
        row = _req_by_id(req_matrix, req_id)
        if not row:
            blockers.append(f"missing_req:{req_id}")
        elif row.get("blocking") is not True:
            blockers.append(f"blocking_false:{req_id}")
        elif row.get("required_before_fact_write") is not True:
            blockers.append(f"required_before_fact_write:{req_id}")

    for req_id in ("review_decision_required", "ttl_policy_required", "source_validation_required",
                   "user_visible_uncertainty_required", "conflict_detection_required", "stale_detection_required"):
        row = _req_by_id(req_matrix, req_id)
        if row and row.get("satisfied_in_this_phase") is not False:
            blockers.append(f"satisfied_should_be_false:{req_id}")

    drows = decision.get("rows") if isinstance(decision.get("rows"), list) else []
    for row in drows:
        if isinstance(row, dict):
            if row.get("world_model_write_allowed") is not False:
                blockers.append("world_model_write_allowed")
            if row.get("scene_delta_candidate_allowed") is not False:
                blockers.append("decision_scene_delta_allowed")

    if ttl_carryover.get("ttl_gate_decision") != "hold_for_review":
        blockers.append("ttl_gate_decision")
    if ttl_carryover.get("ttl_gate_passed") is not False:
        blockers.append("ttl_gate_passed")

    if review_carryover.get("approval_status_unchanged") is not True:
        blockers.append("approval_status_unchanged")
    if review_carryover.get("review_status_unchanged") is not True:
        blockers.append("review_status_unchanged")

    if commercial.get("commercial_claim_status") != "candidate_only":
        blockers.append("commercial_claim_status")
    if commercial.get("temporal_claim_status") != "candidate_only":
        blockers.append("temporal_claim_status")

    if visual.get("visual_context_consumed_as_text") is not False:
        blockers.append("visual_context_consumed_as_text")
    if visual.get("brand_identity_confirmed") is not False:
        blockers.append("brand_identity_confirmed")
    if visual.get("qr_decoded") is not False:
        blockers.append("qr_decoded")

    if scene_delta.get("scene_delta_candidate_allowed") is not False:
        blockers.append("eligibility_scene_delta_allowed")
    if scene_delta.get("scene_delta_candidate_generated") is not False:
        blockers.append("eligibility_scene_delta_generated")

    trace = chain.get("policy_candidate_ttl_region_trace") if isinstance(
        chain.get("policy_candidate_ttl_region_trace"), list
    ) else []
    if len(trace) < 2:
        blockers.append("policy_candidate_ttl_region_trace")
    for t in trace:
        if isinstance(t, dict) and not t.get("real_ocr_evidence_ref"):
            blockers.append(f"missing_ocr_evidence:{t.get('source_region_id')}")

    if metrics.get("scene_delta_candidate_allowed_count") != 0:
        blockers.append("scene_delta_candidate_allowed_count")
    if benchmark.get("benchmark_score_generated") is not False:
        blockers.append("benchmark_score_generated")
    if health.get("provider_health_runtime_checked") is not False:
        blockers.append("provider_health_runtime_checked")

    if boundary.get("boundary_ok") is not True:
        blockers.append("boundary_ok")
    violations = boundary.get("violations") if isinstance(boundary.get("violations"), list) else None
    if violations != []:
        blockers.append("violations")

    if sim.get("simulation_profile_id") != "developer_full":
        blockers.append("simulation_profile_id")

    if non_claims.get("not_policy_approval") is not True:
        blockers.append("not_policy_approval")
    if non_claims.get("not_scene_delta_candidate_ready") is not True:
        blockers.append("not_scene_delta_ready")

    items = followups.get("items") if isinstance(followups.get("items"), list) else []
    if len(items) < 8:
        blockers.append("followups_count")

    if audit.get("auto_approve_invoked") is not False:
        blockers.append("audit_auto_approve")
    if audit.get("fusion_committed") is not False:
        blockers.append("audit_fusion_committed")
    if audit.get("scene_delta_candidate_generated") is not False:
        blockers.append("audit_scene_delta")
    if audit.get("midplatform_fact_written") is not False:
        blockers.append("audit_midplatform")
    if audit.get("scene_delta_written") is not False:
        blockers.append("audit_scene_delta_written")
    if audit.get("world_model_written") is not False:
        blockers.append("audit_world_model")
    if audit.get("navigation_decision_invoked") is not False:
        blockers.append("audit_navigation")
    if audit.get("runtime_routing_changed") is not False:
        blockers.append("audit_routing")

    verdict = "GO" if not blockers else "NO_GO"
    report = {
        "schema_version": "poster_real_ocr_fusion_policy_verifier_report_v0",
        "verdict": verdict,
        "blockers": blockers,
        "checks_passed": 68 - len(blockers) if verdict == "GO" else max(0, 68 - len(blockers)),
        "smoke_root": str(root),
    }
    _write_json(root / "poster_real_ocr_fusion_policy_verifier_report.json", report)
    print(json.dumps({"verdict": verdict, "blockers": blockers}, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
