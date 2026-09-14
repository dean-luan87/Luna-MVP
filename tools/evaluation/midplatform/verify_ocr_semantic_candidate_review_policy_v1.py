#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for OCR Semantic Candidate Review Policy v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import List

TTL_TYPES = {"poster_promo_text", "price_discount_text", "temporal_notice_text"}


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
        "summary": "ocr_semantic_candidate_review_policy_v1_summary.json",
        "intake": "ocr_semantic_review_policy_v1_input_intake_matrix.json",
        "rules": "ocr_semantic_review_policy_v1_rule_matrix.json",
        "queue": "ocr_semantic_review_policy_v1_queue_candidate_matrix.json",
        "ttl": "ocr_semantic_review_policy_v1_ttl_requirement_matrix.json",
        "validation": "ocr_semantic_review_policy_v1_source_validation_matrix.json",
        "visual": "ocr_semantic_review_policy_v1_visual_symbol_registry_routing_matrix.json",
        "scan_roi": "ocr_semantic_review_policy_v1_scan_hint_roi_retry_matrix.json",
        "sq_e": "ocr_semantic_review_policy_v1_sq_e_better_source_matrix.json",
        "decision": "ocr_semantic_review_policy_v1_decision_matrix.json",
        "boundary": "ocr_semantic_review_policy_v1_boundary_report.json",
        "unresolved": "ocr_semantic_review_policy_v1_unresolved_slot_linkage_policy.json",
        "gov": "ocr_semantic_review_policy_v1_governance_routing_report.json",
        "metrics": "ocr_semantic_review_policy_v1_metrics_candidate_report.json",
        "bench": "ocr_semantic_review_policy_v1_benchmark_link_report.json",
        "health": "ocr_semantic_review_policy_v1_system_health_link_report.json",
        "no_write": "ocr_semantic_review_policy_v1_no_write_boundary_report.json",
        "sim": "ocr_semantic_review_policy_v1_simulation_context_report.json",
        "non_claims": "ocr_semantic_review_policy_v1_non_claims_report.json",
        "followups": "ocr_semantic_review_policy_v1_open_followups.json",
        "audit": "ocr_semantic_review_policy_v1_audit_report.json",
    }
    data = {}
    for k, f in files.items():
        p = root / f
        if not p.is_file():
            blockers.append(f"missing:{k}")
        else:
            data[k] = _read_json(p)

    if blockers:
        _write_json(root / "ocr_semantic_review_policy_v1_verifier_report.json", {"verdict": "NO_GO", "blockers": blockers})
        print(json.dumps({"verdict": "NO_GO", "blockers": blockers}, ensure_ascii=False))
        return 2

    s = data["summary"]
    intake = data["intake"]
    rules = data["rules"]
    queue = data["queue"]
    ttl = data["ttl"]
    validation = data["validation"]
    visual = data["visual"]
    scan_roi = data["scan_roi"]
    sq_e = data["sq_e"]
    decision = data["decision"]
    boundary = data["boundary"]
    unresolved = data["unresolved"]
    gov = data["gov"]
    metrics = data["metrics"]
    bench = data["bench"]
    health = data["health"]
    no_write = data["no_write"]
    sim = data["sim"]
    audit = data["audit"]

    ok(s.get("policy_scope") == "review_policy_and_next_action_routing_only", "scope")
    ok(s.get("review_policy_consumes_semantic_v1") is True, "consumes_semantic")
    ok(s.get("tier_aware_review_policy_defined") is True, "tier_aware")
    ok(s.get("ttl_policy_required_for_promo_or_temporal") is True, "ttl_policy")
    ok(s.get("visual_symbol_requires_registry") is True, "visual_registry")
    ok(s.get("scan_hint_not_reviewed_as_fact") is True, "scan_not_fact")
    ok(s.get("world_model_attach_allowed") is False, "wm_attach_false")
    ok(s.get("scene_delta_candidate_allowed") is False, "sd_false")
    ok(s.get("review_decision_committed") is False, "no_decision")

    has_gated = False
    for row in intake.get("rows") or []:
        if not isinstance(row, dict):
            continue
        tier = row.get("evidence_tier")
        route = row.get("review_policy_route")
        if tier == "gated_ocr_primary":
            has_gated = True
            ok(row.get("eligible_for_review_policy") is True, "gated_eligible")
        elif tier == "scan_observation_only":
            ok(route == "roi_or_unresolved_review_later", "scan_route")
        elif tier == "visual_symbol_route":
            ok(route == "visual_symbol_registry_later", "visual_route")
        elif tier == "sq_e_blocked":
            ok(route == "better_source_required", "sq_e_route")
    ok(has_gated, "has_gated_intake")

    rule_ids = {r.get("rule_id") for r in (rules.get("rules") or []) if isinstance(r, dict)}
    ok("no_world_model_attach_in_this_phase" in rule_ids, "rule_no_wm")
    ok("no_scene_delta_candidate_in_this_phase" in rule_ids, "rule_no_sd")

    for q in queue.get("rows") or []:
        if isinstance(q, dict):
            ok(q.get("approval_status") == "not_approved", "queue_not_approved")

    for row in ttl.get("rows") or []:
        if isinstance(row, dict) and row.get("semantic_type_candidate") in TTL_TYPES:
            ok(row.get("ttl_required") is True, "ttl_required_promo")

    ok(validation.get("all_validation_satisfied_false") is True, "validation_false")

    for v in visual.get("rows") or []:
        if isinstance(v, dict):
            ok(v.get("brand_fact_allowed") is False, "visual_no_brand")
            ok(v.get("ordinary_ocr_semantic_allowed") is False, "visual_no_ordinary")

    ok(scan_roi.get("all_fact_review_allowed_false") is True, "scan_no_fact_review")
    ok(sq_e.get("all_strong_semantic_allowed_false") is True, "sq_e_no_strong")

    for d in decision.get("rows") or []:
        if isinstance(d, dict):
            ok(d.get("can_generate_worldmodel_attach") is False, "decision_no_wm")
            ok(d.get("can_generate_scene_delta") is False, "decision_no_sd")

    ok(boundary.get("approval_granted_count") == 0, "boundary_approval")
    ok(unresolved.get("slot_generation_allowed_in_this_phase") is False, "unresolved_no_slot")
    ok(gov.get("world_model_attach_allowed_count") == 0, "gov_wm_count")
    ok(gov.get("scene_delta_candidate_allowed_count") == 0, "gov_sd_count")
    ok(metrics.get("fact_write_allowed_count") == 0, "metrics_fact")
    ok(bench.get("benchmark_score_generated") is False, "bench_no_score")
    ok(health.get("provider_health_runtime_checked") is False, "health_no_runtime")
    ok(no_write.get("boundary_ok") is True, "boundary_ok")
    ok(no_write.get("violations") == [], "boundary_violations")
    ok(sim.get("simulation_profile_id") == "developer_full", "sim_profile")
    ok(data["non_claims"].get("no_review_decision_commit") is True, "non_claims")
    ok(len(data["followups"].get("items") or []) >= 5, "followups")
    ok(audit.get("review_decision_committed") is False, "audit_no_decision")
    ok(audit.get("approval_granted") is False, "audit_approval")
    ok(audit.get("world_model_attach_executed") is False, "audit_wm")
    ok(audit.get("runtime_routing_changed") is False, "audit_routing")

    verdict = "GO" if not blockers else "NO_GO"
    _write_json(
        root / "ocr_semantic_review_policy_v1_verifier_report.json",
        {"schema_version": "ocr_semantic_review_policy_v1_verifier_report_v0", "verdict": verdict, "blockers": blockers, "checks_passed": checks},
    )
    print(json.dumps({"verdict": verdict, "blockers": blockers, "checks_passed": checks}, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
