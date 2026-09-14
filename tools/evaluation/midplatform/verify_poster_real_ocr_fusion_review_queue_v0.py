#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for Poster Real OCR Fusion Review Queue v0."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, List


FORBIDDEN_ALLOWED = frozenset({"world_model_write", "auto_approve", "scene_delta_write", "navigation_decision"})


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


def main() -> int:
    _find_ws_root()
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke-root", required=True)
    args = ap.parse_args()

    root = _require_abs(args.smoke_root, "--smoke-root")
    blockers: List[str] = []

    paths = {
        "summary": root / "poster_real_ocr_fusion_review_queue_summary.json",
        "candidate": root / "poster_real_ocr_fusion_review_queue_candidate.json",
        "matrix": root / "poster_real_ocr_fusion_review_queue_matrix.json",
        "risk": root / "poster_real_ocr_fusion_review_risk_inheritance_report.json",
        "policy": root / "poster_real_ocr_fusion_review_policy_report.json",
        "decision": root / "poster_real_ocr_fusion_review_decision_placeholder_report.json",
        "chain": root / "poster_real_ocr_fusion_review_source_chain_report.json",
        "metrics": root / "poster_real_ocr_fusion_review_metrics_candidate_report.json",
        "benchmark": root / "poster_real_ocr_fusion_review_benchmark_link_report.json",
        "health": root / "poster_real_ocr_fusion_review_system_health_link_report.json",
        "boundary": root / "poster_real_ocr_fusion_review_no_write_boundary_report.json",
        "sim": root / "poster_real_ocr_fusion_review_simulation_context_report.json",
        "non_claims": root / "poster_real_ocr_fusion_review_non_claims_report.json",
        "followups": root / "poster_real_ocr_fusion_review_open_followups.json",
        "audit": root / "poster_real_ocr_fusion_review_audit_report.json",
    }

    for label, p in paths.items():
        if not p.is_file():
            blockers.append(f"missing:{label}")

    if blockers:
        _write_json(
            root / "poster_real_ocr_fusion_review_verifier_report.json",
            {"verdict": "NO_GO", "blockers": blockers, "checks_passed": 0},
        )
        print(json.dumps({"verdict": "NO_GO", "blockers": blockers}, ensure_ascii=False))
        return 2

    summary = _read_json(paths["summary"])
    candidate = _read_json(paths["candidate"])
    matrix = _read_json(paths["matrix"])
    risk = _read_json(paths["risk"])
    policy = _read_json(paths["policy"])
    decision = _read_json(paths["decision"])
    chain = _read_json(paths["chain"])
    metrics = _read_json(paths["metrics"])
    benchmark = _read_json(paths["benchmark"])
    health = _read_json(paths["health"])
    boundary = _read_json(paths["boundary"])
    sim = _read_json(paths["sim"])
    non_claims = _read_json(paths["non_claims"])
    followups = _read_json(paths["followups"])
    audit = _read_json(paths["audit"])

    if summary.get("queue_scope") != "review_queue_only":
        blockers.append("queue_scope")
    if summary.get("queue_item_count") != 1:
        blockers.append("queue_item_count")
    if summary.get("pending_review_count") != 1:
        blockers.append("pending_review_count")
    if summary.get("approval_granted_count") != 0:
        blockers.append("approval_granted_count")
    if summary.get("auto_approve_invoked") is not False:
        blockers.append("auto_approve_invoked")
    if summary.get("fusion_committed") is not False:
        blockers.append("fusion_committed")
    if summary.get("scene_delta_candidate_generated") is not False:
        blockers.append("scene_delta")

    if candidate.get("review_status") != "pending_review":
        blockers.append("review_status")
    if candidate.get("approval_status") != "not_approved":
        blockers.append("approval_status")
    if candidate.get("auto_approve_allowed") is not False:
        blockers.append("auto_approve_allowed")
    allowed = candidate.get("allowed_next_steps") if isinstance(candidate.get("allowed_next_steps"), list) else []
    for step in allowed:
        if str(step) in FORBIDDEN_ALLOWED or "world_model" in str(step):
            blockers.append(f"forbidden_allowed_step:{step}")

    rows = matrix.get("rows") if isinstance(matrix.get("rows"), list) else []
    if len(rows) != 1:
        blockers.append("matrix_row_count")
    for row in rows:
        if isinstance(row, dict) and row.get("scene_delta_candidate_allowed") is not False:
            blockers.append("scene_delta_allowed")

    if risk.get("commercial_claim_status") != "candidate_only":
        blockers.append("commercial_claim")
    if risk.get("temporal_claim_status") != "candidate_only":
        blockers.append("temporal_claim")
    if risk.get("ttl_required_region_count") != 2:
        blockers.append("ttl_count")
    if risk.get("brand_identity_confirmed") is not False:
        blockers.append("brand")
    if risk.get("qr_decoded") is not False:
        blockers.append("qr_decoded")
    if risk.get("visual_context_consumed_as_text") is not False:
        blockers.append("visual_as_text")

    if policy.get("all_candidates_pending_review") is not True:
        blockers.append("all_pending")
    if policy.get("write_actions_forbidden") is not True:
        blockers.append("write_forbidden")
    if policy.get("scene_delta_candidate_forbidden_in_this_phase") is not True:
        blockers.append("scene_delta_forbidden")

    if decision.get("decision_status") != "not_evaluated":
        blockers.append("decision_status")
    if decision.get("approval_granted") is not False:
        blockers.append("decision_approval")
    if decision.get("decision_committed") is not False:
        blockers.append("decision_committed")

    if not chain.get("fusion_candidate_dryrun_ref") or not chain.get("queue_item_id"):
        blockers.append("source_chain_trace")

    if metrics.get("approval_granted_count") != 0:
        blockers.append("metrics_approval")
    if metrics.get("benchmark_score_generated") is not False:
        blockers.append("benchmark_score")

    if benchmark.get("benchmark_score_generated") is not False:
        blockers.append("benchmark_link_score")
    if benchmark.get("current_phase_updates_benchmark_values") is not False:
        blockers.append("benchmark_update")

    if health.get("provider_health_runtime_checked") is not False:
        blockers.append("health_runtime")

    if boundary.get("boundary_ok") is not True:
        blockers.append("boundary_ok")
    if boundary.get("violations") != []:
        blockers.append("violations")

    if sim.get("simulation_profile_id") != "developer_full":
        blockers.append("sim_profile")

    if non_claims.get("not_approval") is not True:
        blockers.append("non_claims_approval")
    if non_claims.get("not_fusion_fact") is not True:
        blockers.append("non_claims_fusion")
    if non_claims.get("not_benchmark") is not True:
        blockers.append("non_claims_benchmark")

    items = followups.get("items") if isinstance(followups.get("items"), list) else []
    if len(items) < 1:
        blockers.append("followups_empty")

    audit_checks = [
        ("auto_approve_invoked", False),
        ("fusion_committed", False),
        ("scene_delta_candidate_generated", False),
        ("midplatform_fact_written", False),
        ("scene_delta_written", False),
        ("world_model_written", False),
        ("navigation_decision_invoked", False),
        ("approval_granted", False),
        ("runtime_routing_changed", False),
    ]
    for key, expected in audit_checks:
        if audit.get(key) != expected:
            blockers.append(f"audit:{key}")

    if blockers:
        verdict = "NO_GO"
    elif summary.get("phase_verdict_hint") == "CONDITIONAL_GO":
        verdict = "CONDITIONAL_GO"
    else:
        verdict = str(summary.get("phase_verdict_hint") or "GO")

    report = {
        "schema_version": "poster_real_ocr_fusion_review_verifier_report_v0",
        "verdict": verdict,
        "blockers": blockers,
        "checks_passed": 57 - len(blockers),
        "phase_verdict_hint": summary.get("phase_verdict_hint"),
    }
    _write_json(root / "poster_real_ocr_fusion_review_verifier_report.json", report)
    print(json.dumps({"verdict": verdict, "blockers": blockers}, ensure_ascii=False))
    return 0 if verdict in ("GO", "CONDITIONAL_GO") else 2


if __name__ == "__main__":
    raise SystemExit(main())
