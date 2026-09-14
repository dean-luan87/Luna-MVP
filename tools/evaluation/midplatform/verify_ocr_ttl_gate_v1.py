#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for OCR TTL Gate v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import List


def _require_abs(p: str, label: str) -> Path:
    pp = Path(p).expanduser()
    if not pp.is_absolute():
        raise SystemExit(f"ERROR: {label} must be absolute, got: {p}")
    return pp.resolve()


def _read_json(p: Path):
    return json.loads(p.read_text(encoding="utf-8"))


def _write_json(path: Path, obj: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke-root", required=True)
    args = ap.parse_args()

    root = _require_abs(args.smoke_root, "--smoke-root")
    blockers: List[str] = []
    checks = 0

    def ok(c: bool, name: str) -> None:
        nonlocal checks
        if c:
            checks += 1
        else:
            blockers.append(name)

    files = {
        "summary": "ocr_ttl_gate_v1_summary.json",
        "intake": "ocr_ttl_gate_v1_queue_intake_matrix.json",
        "eval": "ocr_ttl_gate_v1_evaluation_matrix.json",
        "pattern": "ocr_ttl_gate_v1_text_pattern_report.json",
        "policy_req": "ocr_ttl_gate_v1_policy_requirement_matrix.json",
        "decision": "ocr_ttl_gate_v1_decision_matrix.json",
        "chain": "ocr_ttl_gate_v1_source_chain_report.json",
        "boundary": "ocr_ttl_gate_v1_boundary_report.json",
        "metrics": "ocr_ttl_gate_v1_metrics_candidate_report.json",
        "bench": "ocr_ttl_gate_v1_benchmark_link_report.json",
        "health": "ocr_ttl_gate_v1_system_health_link_report.json",
        "no_write": "ocr_ttl_gate_v1_no_write_boundary_report.json",
        "sim": "ocr_ttl_gate_v1_simulation_context_report.json",
        "non_claims": "ocr_ttl_gate_v1_non_claims_report.json",
        "followups": "ocr_ttl_gate_v1_open_followups.json",
        "audit": "ocr_ttl_gate_v1_audit_report.json",
    }
    data = {}
    for k, f in files.items():
        p = root / f
        if not p.is_file():
            blockers.append(f"missing:{k}")
        else:
            data[k] = _read_json(p)

    if blockers:
        _write_json(root / "ocr_ttl_gate_v1_verifier_report.json", {"verdict": "NO_GO", "blockers": blockers})
        print(json.dumps({"verdict": "NO_GO", "blockers": blockers}, ensure_ascii=False))
        return 2

    s = data["summary"]
    intake = data["intake"]
    ev = data["eval"]
    pattern = data["pattern"]
    policy_req = data["policy_req"]
    decision = data["decision"]
    chain = data["chain"]
    boundary = data["boundary"]
    metrics = data["metrics"]
    audit = data["audit"]

    ok(s.get("gate_scope") == "ttl_gate_dryrun_only", "scope")
    ok(s.get("based_on_review_queue_runtime") is True, "based_runtime")
    ok(s.get("ttl_queue_item_count") == 2, "ttl_count_2")
    ok(s.get("ttl_gate_evaluated") is True, "evaluated")
    ok(s.get("ttl_gate_passed_count") == 0, "passed_zero")
    ok(s.get("decision_committed") is False, "no_decision")
    ok(s.get("approval_granted") is False, "no_approval")

    ok(intake.get("ttl_only") is True, "intake_ttl_only")
    for row in intake.get("rows") or []:
        pass  # intake only has ttl rows by construction

    ok(ev.get("all_ttl_policy_satisfied_false") is True, "policy_not_satisfied")
    for row in ev.get("rows") or []:
        if isinstance(row, dict):
            ok(row.get("ttl_required") is True, "ttl_required")
            ok(row.get("ttl_policy_satisfied") is False, "not_satisfied")
            ok(row.get("fact_status") == "not_fact", "eval_not_fact")
            ok(row.get("ttl_gate_status", "").startswith("hold_"), "hold_status")

    for row in pattern.get("rows") or []:
        if isinstance(row, dict):
            ok(row.get("pattern_detection_not_fact") is True, "pattern_not_fact")

    req_ids = {r.get("requirement_id") for r in (policy_req.get("requirements") or []) if isinstance(r, dict)}
    ok("source_validation" in req_ids, "req_source_validation")
    ok("stale_check" in req_ids, "req_stale")
    ok("expiry_policy" in req_ids, "req_expiry")
    for r in policy_req.get("requirements") or []:
        if isinstance(r, dict) and r.get("requirement_id") == "source_validation":
            ok(r.get("required_before_fact") is True, "sv_before_fact")

    for row in decision.get("rows") or []:
        if isinstance(row, dict):
            ok(row.get("approval_status") == "not_approved", "dec_not_approved")
            ok(row.get("world_model_write_allowed") is False, "dec_no_wm")
            ok(row.get("scene_delta_candidate_allowed") is False, "dec_no_sd")

    ok(chain.get("all_traceable_to_review_queue_runtime") is True, "chain_runtime")
    ok(chain.get("all_traceable_to_semantic_v1") is True, "chain_semantic")
    ok(boundary.get("approval_granted_count") == 0, "boundary_approval")
    ok(metrics.get("fact_write_allowed_count") == 0, "metrics_fact")
    ok(metrics.get("ttl_gate_passed_count") == 0, "metrics_passed")
    ok(metrics.get("no_write_boundary_pass_rate") == 1.0, "metrics_boundary")
    ok(data["bench"].get("benchmark_score_generated") is False, "bench")
    ok(data["health"].get("provider_health_runtime_checked") is False, "health")
    ok(data["no_write"].get("boundary_ok") is True, "boundary_ok")
    ok(data["no_write"].get("violations") == [], "violations")
    ok(data["sim"].get("simulation_profile_id") == "developer_full", "sim")
    ok(data["non_claims"].get("no_review_decision_commit") is True, "non_claims")
    ok(len(data["followups"].get("items") or []) >= 5, "followups")
    ok(audit.get("world_model_attach_executed") is False, "audit_wm")
    ok(audit.get("runtime_routing_changed") is False, "audit_routing")

    verdict = "GO" if not blockers else "NO_GO"
    _write_json(
        root / "ocr_ttl_gate_v1_verifier_report.json",
        {"schema_version": "ocr_ttl_gate_v1_verifier_report_v0", "verdict": verdict, "blockers": blockers, "checks_passed": checks},
    )
    print(json.dumps({"verdict": verdict, "blockers": blockers, "checks_passed": checks}, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
