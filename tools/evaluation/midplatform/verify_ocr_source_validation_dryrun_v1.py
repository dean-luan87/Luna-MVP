#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for OCR Source Validation DryRun v1."""

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
        "summary": "ocr_source_validation_v1_summary.json",
        "intake": "ocr_source_validation_v1_candidate_intake_matrix.json",
        "rules": "ocr_source_validation_v1_rule_matrix.json",
        "chain": "ocr_source_validation_v1_evidence_chain_completeness_matrix.json",
        "reliability": "ocr_source_validation_v1_reliability_evaluation_matrix.json",
        "ttl": "ocr_source_validation_v1_ttl_source_validation_matrix.json",
        "scan": "ocr_source_validation_v1_scan_hint_validation_matrix.json",
        "visual": "ocr_source_validation_v1_visual_symbol_validation_matrix.json",
        "sq_e": "ocr_source_validation_v1_sq_e_validation_matrix.json",
        "decision": "ocr_source_validation_v1_decision_matrix.json",
        "routing": "ocr_source_validation_v1_routing_report.json",
        "boundary": "ocr_source_validation_v1_boundary_report.json",
        "source_chain": "ocr_source_validation_v1_source_chain_report.json",
        "metrics": "ocr_source_validation_v1_metrics_candidate_report.json",
        "bench": "ocr_source_validation_v1_benchmark_link_report.json",
        "health": "ocr_source_validation_v1_system_health_link_report.json",
        "no_write": "ocr_source_validation_v1_no_write_boundary_report.json",
        "sim": "ocr_source_validation_v1_simulation_context_report.json",
        "non_claims": "ocr_source_validation_v1_non_claims_report.json",
        "followups": "ocr_source_validation_v1_open_followups.json",
        "audit": "ocr_source_validation_v1_audit_report.json",
    }
    data = {}
    for k, f in files.items():
        p = root / f
        if not p.is_file():
            blockers.append(f"missing:{k}")
        else:
            data[k] = _read_json(p)

    if blockers:
        _write_json(root / "ocr_source_validation_v1_verifier_report.json", {"verdict": "NO_GO", "blockers": blockers})
        print(json.dumps({"verdict": "NO_GO", "blockers": blockers}, ensure_ascii=False))
        return 2

    s = data["summary"]
    intake = data["intake"]
    rules = data["rules"]
    chain = data["chain"]
    reliability = data["reliability"]
    ttl = data["ttl"]
    scan = data["scan"]
    visual = data["visual"]
    sq_e = data["sq_e"]
    decision = data["decision"]
    routing = data["routing"]
    boundary = data["boundary"]
    metrics = data["metrics"]
    audit = data["audit"]

    ok(s.get("validation_scope") == "source_validation_dryrun_only", "scope")
    ok(s.get("source_validation_evaluated") is True, "evaluated")
    ok(s.get("source_validation_passed_count") == 0, "passed_zero")
    ok(s.get("decision_committed") is False, "no_decision")
    ok(s.get("approval_granted") is False, "no_approval")

    ttl_intake = sum(1 for r in (intake.get("rows") or []) if isinstance(r, dict) and r.get("source_origin") == "ttl_gate")
    ok(ttl_intake >= 2, "ttl_intake_2")
    ok(len(scan.get("rows") or []) >= 1, "scan_intake")
    ok(len(visual.get("rows") or []) >= 1, "visual_intake")
    ok(len(sq_e.get("rows") or []) >= 1, "sq_e_intake")

    rule_ids = {r.get("rule_id") for r in (rules.get("rules") or []) if isinstance(r, dict)}
    ok("single_ocr_not_enough_for_fact" in rule_ids, "rule_single_ocr")
    ok("visual_symbol_requires_registry" in rule_ids, "rule_visual")
    ok("sq_e_blocked_cannot_validate" in rule_ids, "rule_sq_e")

    has_gated_complete = False
    has_scan_partial = False
    has_visual_reg = False
    has_sq_e_low = False
    for row in chain.get("rows") or []:
        if isinstance(row, dict):
            st = row.get("chain_completeness_status")
            if st == "complete_for_dryrun":
                has_gated_complete = True
            if st == "partial_scan_only":
                has_scan_partial = True
            if st == "visual_registry_required":
                has_visual_reg = True
            if st == "low_quality_blocked":
                has_sq_e_low = True
    ok(has_gated_complete, "gated_complete")
    ok(has_scan_partial, "scan_partial")
    ok(has_visual_reg, "visual_reg")
    ok(has_sq_e_low, "sq_e_low")

    ok(reliability.get("no_validated_for_fact") is True, "no_validated_for_fact")
    for row in reliability.get("rows") or []:
        if isinstance(row, dict):
            ok(row.get("reliability_status") != "validated_for_fact", "rel_not_validated")

    ok(len(ttl.get("rows") or []) == 2, "ttl_matrix_2")
    for row in ttl.get("rows") or []:
        if isinstance(row, dict):
            ok(row.get("validation_satisfied") is False, "ttl_not_satisfied")

    ok(scan.get("row_count", 0) >= 1, "scan_matrix")
    for row in scan.get("rows") or []:
        if isinstance(row, dict):
            ok(row.get("can_support_fact_validation") is False, "scan_no_fact")

    for row in visual.get("rows") or []:
        if isinstance(row, dict):
            ok(row.get("registry_checked") is False, "registry_not_checked")
            ok(row.get("brand_fact_allowed") is False, "no_brand")

    for row in sq_e.get("rows") or []:
        if isinstance(row, dict):
            ok(row.get("strong_semantic_allowed") is False, "sq_e_no_strong")

    ok(decision.get("all_validation_satisfied_false") is True, "decision_all_false")
    for row in decision.get("rows") or []:
        if isinstance(row, dict):
            ok(row.get("approval_status") == "not_approved", "dec_approval")
            ok(row.get("fact_write_allowed") is False, "dec_fact")
            ok(row.get("world_model_write_allowed") is False, "dec_wm")

    ok(routing.get("source_validation_passed_count") == 0, "routing_passed")
    ok(boundary.get("validation_satisfied_for_fact_count") == 0, "boundary_fact")
    ok(data["source_chain"].get("row_count", 0) >= 1, "chain_exists")
    for row in data["source_chain"].get("rows") or []:
        if isinstance(row, dict):
            ok(row.get("traceable_to_semantic_v1") is True, "trace_semantic")
    ok(metrics.get("fact_write_allowed_count") == 0, "metrics_fact")
    ok(metrics.get("no_write_boundary_pass_rate") == 1.0, "metrics_boundary")
    ok(data["bench"].get("benchmark_score_generated") is False, "bench")
    ok(data["health"].get("provider_health_runtime_checked") is False, "health")
    ok(data["no_write"].get("boundary_ok") is True, "boundary_ok")
    ok(data["sim"].get("simulation_profile_id") == "developer_full", "sim")
    ok(audit.get("world_model_attach_executed") is False, "audit_wm")

    verdict = "GO" if not blockers else "NO_GO"
    _write_json(
        root / "ocr_source_validation_v1_verifier_report.json",
        {"schema_version": "ocr_source_validation_v1_verifier_report_v0", "verdict": verdict, "blockers": blockers, "checks_passed": checks},
    )
    print(json.dumps({"verdict": verdict, "blockers": blockers, "checks_passed": checks}, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
