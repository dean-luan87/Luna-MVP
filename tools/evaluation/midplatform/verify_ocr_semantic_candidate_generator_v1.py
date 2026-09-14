#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for OCR Semantic Candidate Generator v1."""

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
        "summary": "ocr_semantic_candidate_v1_summary.json",
        "matrix": "ocr_semantic_candidate_v1_evidence_tier_input_matrix.json",
        "gated": "ocr_semantic_candidate_v1_gated_ocr_collection.json",
        "scan": "ocr_semantic_candidate_v1_scan_observation_hint_report.json",
        "visual": "ocr_semantic_candidate_v1_visual_symbol_route_report.json",
        "blocked": "ocr_semantic_candidate_v1_sq_e_blocked_report.json",
        "routing": "ocr_semantic_candidate_v1_routing_decision_matrix.json",
        "types": "ocr_semantic_candidate_v1_type_classification_report.json",
        "raw": "ocr_semantic_candidate_v1_raw_text_preservation_report.json",
        "basis": "ocr_semantic_candidate_v1_interpretation_basis_report.json",
        "gov": "ocr_semantic_candidate_v1_governance_routing_report.json",
        "unresolved": "ocr_semantic_candidate_v1_unresolved_slot_linkage_plan.json",
        "risk": "ocr_semantic_candidate_v1_quality_risk_report.json",
        "chain": "ocr_semantic_candidate_v1_source_chain_report.json",
        "metrics": "ocr_semantic_candidate_v1_metrics_candidate_report.json",
        "bench": "ocr_semantic_candidate_v1_benchmark_link_report.json",
        "health": "ocr_semantic_candidate_v1_system_health_link_report.json",
        "boundary": "ocr_semantic_candidate_v1_no_write_boundary_report.json",
        "sim": "ocr_semantic_candidate_v1_simulation_context_report.json",
        "non_claims": "ocr_semantic_candidate_v1_non_claims_report.json",
        "followups": "ocr_semantic_candidate_v1_open_followups.json",
        "audit": "ocr_semantic_candidate_v1_audit_report.json",
    }
    data = {}
    for k, f in files.items():
        p = root / f
        if not p.is_file():
            blockers.append(f"missing:{k}")
        else:
            data[k] = _read_json(p)

    if blockers:
        _write_json(root / "ocr_semantic_candidate_v1_verifier_report.json", {"verdict": "NO_GO", "blockers": blockers})
        print(json.dumps({"verdict": "NO_GO", "blockers": blockers}, ensure_ascii=False))
        return 2

    s = data["summary"]
    matrix = data["matrix"]
    gated = data["gated"]
    scan = data["scan"]
    visual = data["visual"]
    blocked = data["blocked"]
    routing = data["routing"]
    types = data["types"]
    raw = data["raw"]
    basis = data["basis"]
    gov = data["gov"]
    unresolved = data["unresolved"]
    risk = data["risk"]
    chain = data["chain"]
    metrics = data["metrics"]
    bench = data["bench"]
    health = data["health"]
    boundary = data["boundary"]
    sim = data["sim"]
    audit = data["audit"]

    ok(s.get("generator_scope") == "semantic_candidate_v1_tier_aware_dryrun", "scope")
    ok(s.get("based_on_evidence_pack_adapter_v1") is True, "based_adapter")
    ok(s.get("semantic_candidate_consumes_evidence_tier") is True, "consumes_tier")
    ok(s.get("scan_observation_not_promoted_to_ocr_semantic") is True, "scan_not_promoted")
    ok(s.get("visual_symbol_route_not_interpreted_as_plain_text") is True, "visual_not_plain")
    ok(s.get("sq_e_blocked_no_strong_semantic") is True, "sq_e_no_strong")
    ok(s.get("semantic_model_invoked") is False, "no_semantic_model")
    ok(s.get("raw_text_overwritten") is False, "no_overwrite")

    for row in matrix.get("rows") or []:
        if not isinstance(row, dict):
            continue
        tier = row.get("evidence_tier")
        elig = row.get("eligible_for_semantic_candidate_v1")
        if tier == "gated_ocr_primary":
            ok(elig is True, "matrix_gated_eligible")
        elif tier == "scan_observation_only":
            ok(elig is False and row.get("semantic_route") == "scan_observation_hint", "matrix_scan")
        elif tier == "visual_symbol_route":
            ok(elig is False and row.get("semantic_route") == "visual_symbol_candidate", "matrix_visual")
        elif tier == "sq_e_blocked":
            ok(elig is False and row.get("semantic_route") == "blocked_low_quality", "matrix_blocked")

    candidates = gated.get("candidates") or []
    ok(gated.get("candidate_count") == len(candidates), "gated_count")
    for c in candidates:
        if not isinstance(c, dict):
            continue
        ok(c.get("evidence_tier") == "gated_ocr_primary", "cand_tier")
        ok((c.get("source_ocr_request_ref") or {}).get("request_id"), "cand_ocr_ref")
        ok(c.get("source_quality_grade"), "cand_sq")
        ok(c.get("semantic_model_invoked") is False, "cand_no_model")
        ok(c.get("raw_text_overwritten") is False, "cand_no_overwrite")

    for h in scan.get("hints") or []:
        if isinstance(h, dict):
            fu = h.get("forbidden_usage") or []
            ok("world_model_attach" in fu, "scan_forbid_wm")
            ok("navigation_decision" in fu, "scan_forbid_nav")

    for v in visual.get("routes") or []:
        if isinstance(v, dict):
            ok(v.get("ordinary_ocr_semantic_allowed") is False, "visual_no_ordinary")
            ok(v.get("no_brand_fact_without_registry_or_review") is True, "visual_no_brand_fact")

    ok(blocked.get("strong_semantic_generated") is False, "blocked_no_strong")
    for item in blocked.get("items") or []:
        if isinstance(item, dict):
            ok(item.get("strong_semantic_generated") is False, "blocked_item")

    for row in routing.get("rows") or []:
        if isinstance(row, dict):
            ok(row.get("world_model_attach_allowed") is False, "route_wm")
            ok(row.get("scene_delta_candidate_allowed") is False, "route_sd")

    ok(types.get("scan_not_in_gated_distribution") is True, "types_scan_sep")
    ok(raw.get("raw_text_preservation_rate") == 1.0, "raw_rate")
    ok(basis.get("main_candidates_require_ocr_request_ref") is True, "basis_ocr_ref")
    ok(gov.get("world_model_attach_allowed") is False, "gov_wm")
    ok(unresolved.get("slot_generation_allowed_in_this_phase") is False, "unresolved_no_slot")
    ok(risk is not None, "risk_exists")
    ok(chain.get("main_semantic_traceable_to_ocr_request") is True, "chain_ocr")
    ok(chain.get("scan_hint_traceable_to_scan_observation") is True, "chain_scan")
    ok(metrics.get("semantic_candidate_consumes_evidence_tier") is True, "metrics_tier")
    ok(bench.get("benchmark_score_generated") is False, "bench_no_score")
    ok(health.get("provider_health_runtime_checked") is False, "health_no_runtime")
    ok(boundary.get("boundary_ok") is True, "boundary_ok")
    ok(boundary.get("violations") == [], "boundary_violations")
    ok(sim.get("simulation_profile_id") == "developer_full", "sim_profile")
    ok(data["non_claims"].get("no_ocr_execution") is True, "non_claims")
    ok(len(data["followups"].get("items") or []) >= 5, "followups")
    ok(audit.get("semantic_model_invoked") is False, "audit_model")
    ok(audit.get("scan_observation_promoted_to_fact") is False, "audit_scan")
    ok(audit.get("visual_symbol_committed_as_brand_fact") is False, "audit_visual")
    ok(audit.get("sq_e_strong_semantic_generated") is False, "audit_sq_e")
    ok(audit.get("world_model_attach_executed") is False, "audit_wm")
    ok(audit.get("runtime_routing_changed") is False, "audit_routing")

    verdict = "GO" if not blockers else "NO_GO"
    _write_json(
        root / "ocr_semantic_candidate_v1_verifier_report.json",
        {"schema_version": "ocr_semantic_candidate_v1_verifier_report_v0", "verdict": verdict, "blockers": blockers, "checks_passed": checks},
    )
    print(json.dumps({"verdict": verdict, "blockers": blockers, "checks_passed": checks}, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
