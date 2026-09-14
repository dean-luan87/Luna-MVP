#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for ROI Retry Proposal Runtime v1."""

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
        "summary": "roi_retry_proposal_runtime_v1_summary.json",
        "intake": "roi_retry_candidate_intake_matrix.json",
        "rules": "roi_retry_rule_matrix_v1.json",
        "schema": "roi_retry_proposal_schema_v1.json",
        "collection": "roi_retry_proposal_collection_v1.json",
        "linebox": "roi_retry_linebox_to_roi_mapping_report.json",
        "mixed": "roi_retry_mixed_region_split_proposal_report.json",
        "priority": "roi_retry_priority_matrix_v1.json",
        "routing": "roi_retry_routing_matrix_v1.json",
        "future": "roi_retry_future_execution_plan_v1.json",
        "boundary": "roi_retry_boundary_report_v1.json",
        "source_chain": "roi_retry_source_chain_report_v1.json",
        "metrics": "roi_retry_metrics_candidate_report_v1.json",
        "bench": "roi_retry_benchmark_link_report_v1.json",
        "health": "roi_retry_system_health_link_report_v1.json",
        "no_write": "roi_retry_no_write_boundary_report_v1.json",
        "sim": "roi_retry_simulation_context_report_v1.json",
        "non_claims": "roi_retry_non_claims_report_v1.json",
        "followups": "roi_retry_open_followups_v1.json",
        "audit": "roi_retry_audit_report_v1.json",
    }
    data = {}
    for k, f in files.items():
        p = root / f
        if not p.is_file():
            blockers.append(f"missing:{k}")
        else:
            data[k] = _read_json(p)

    if blockers:
        _write_json(root / "roi_retry_verifier_report_v1.json", {"verdict": "NO_GO", "blockers": blockers})
        print(json.dumps({"verdict": "NO_GO", "blockers": blockers}, ensure_ascii=False))
        return 2

    s = data["summary"]
    intake = data["intake"]
    rules = data["rules"]
    schema = data["schema"]
    collection = data["collection"]
    linebox = data["linebox"]
    mixed = data["mixed"]
    priority = data["priority"]
    routing = data["routing"]
    future = data["future"]
    boundary = data["boundary"]
    source_chain = data["source_chain"]
    metrics = data["metrics"]
    bench = data["bench"]
    health = data["health"]
    no_write = data["no_write"]
    sim = data["sim"]
    audit = data["audit"]

    ok(s.get("runtime_scope") == "roi_retry_proposal_runtime_only", "scope")
    ok(s.get("based_on_source_validation_v1") is True, "based_sv")
    ok(s.get("roi_retry_proposal_generated") is True, "proposal_generated")
    ok(s.get("roi_crop_executed") is False, "no_crop")
    ok(s.get("ocr_request_generated") is False, "no_ocr_req")
    ok(s.get("ocr_invoked") is False, "no_ocr")
    ok(s.get("provider_invoked") is False, "no_provider")
    ok(s.get("evidence_pack_generated") is False, "no_ep")
    ok(s.get("semantic_candidate_generated") is False, "no_semantic")
    ok(s.get("world_model_attach_executed") is False, "no_wm_attach")
    ok(s.get("scene_delta_candidate_generated") is False, "no_scene_delta")
    ok(s.get("midplatform_fact_written") is False, "no_fact")
    ok(s.get("world_model_written") is False, "no_wm")
    ok(s.get("navigation_decision_invoked") is False, "no_nav")
    ok(s.get("runtime_routing_changed") is False, "no_routing_change")

    ok(intake.get("row_count", 0) >= 1, "intake_exists")
    ok(any(r.get("intake_status") == "accepted" for r in (intake.get("rows") or []) if isinstance(r, dict)), "intake_accepted")

    rule_ids = {r.get("rule_id") for r in (rules.get("rules") or []) if isinstance(r, dict)}
    ok("no_ocr_execution_in_this_phase" in rule_ids, "rule_no_ocr")
    ok("no_evidence_pack_generation_in_this_phase" in rule_ids, "rule_no_ep")

    tmpl = schema.get("template") or schema.get("defaults") or {}
    ok(schema.get("defaults", {}).get("crop_execution_allowed_in_this_phase") is False, "schema_crop_false")
    ok(schema.get("defaults", {}).get("ocr_request_allowed_in_this_phase") is False, "schema_ocr_false")
    ok("proposed_roi_bbox_xyxy" in (schema.get("template") or {}), "schema_bbox_field")

    ok(collection.get("proposal_count", 0) > 0, "proposal_count")
    for prop in collection.get("proposals") or []:
        if isinstance(prop, dict):
            ok("proposed_roi_bbox_xyxy" in prop, "prop_bbox_key")
            ok(prop.get("crop_execution_allowed_in_this_phase") is False, "prop_no_crop")
            ok(prop.get("ocr_request_allowed_in_this_phase") is False, "prop_no_ocr_req")
            break

    ok(linebox.get("row_count", 0) >= 1, "linebox_report")
    for row in linebox.get("rows") or []:
        if isinstance(row, dict):
            ok(row.get("linebox_text_not_evidence") is True, "linebox_not_evidence")
            break

    ok(mixed.get("row_count", 0) >= 1, "mixed_report")
    for row in mixed.get("rows") or []:
        if isinstance(row, dict):
            ok(row.get("semantic_join_allowed") is False, "no_semantic_join")
            ok(row.get("cross_region_text_join_allowed") is False, "no_cross_join")
            break

    ok(priority.get("row_count", 0) >= 1, "priority_exists")
    for row in priority.get("rows") or []:
        if isinstance(row, dict):
            ok(row.get("auto_escalation_committed") is False, "no_auto_escalation")
            break

    ok(routing.get("row_count", 0) >= 1, "routing_exists")
    for row in routing.get("rows") or []:
        if isinstance(row, dict):
            ok(row.get("ocr_request_generated") is False, "route_no_ocr_req")
            ok(row.get("provider_invoked") is False, "route_no_provider")
            break

    phases = [p.get("future_phase") for p in (future.get("phases") or []) if isinstance(p, dict)]
    ok("ROI-Crop-Execution-DryRun-v1" in phases, "future_crop_phase")

    ok(boundary.get("roi_crop_executed") is False, "boundary_no_crop")
    ok(boundary.get("evidence_pack_generated") is False, "boundary_no_ep")

    ok(source_chain.get("row_count", 0) >= 1, "chain_exists")
    ok(source_chain.get("all_traceable_to_source_validation") is True, "trace_sv")
    for row in source_chain.get("rows") or []:
        if isinstance(row, dict):
            ok(row.get("traceable_to_source_validation") is True, "row_trace_sv")
            ok(row.get("source_chain_preserved") is True, "chain_preserved")
            break

    ok(metrics.get("ocr_request_generated_count") == 0, "metrics_ocr_req")
    ok(metrics.get("provider_invoked_count") == 0, "metrics_provider")
    ok(bench.get("benchmark_score_generated") is False, "bench_score")
    ok(health.get("provider_health_runtime_checked") is False, "health_provider")
    ok(no_write.get("boundary_ok") is True, "boundary_ok")
    ok(no_write.get("violations") == [], "no_violations")
    ok(sim.get("simulation_profile_id") == "developer_full", "sim_profile")
    ok(audit.get("roi_retry_proposal_runtime_v1_executed") is True, "audit_executed")
    ok(audit.get("roi_crop_executed") is False, "audit_crop")
    ok(audit.get("world_model_attach_executed") is False, "audit_wm")
    ok(audit.get("scene_delta_candidate_generated") is False, "audit_scene")
    ok(audit.get("midplatform_fact_written") is False, "audit_fact")
    ok(audit.get("world_model_written") is False, "audit_wm_written")
    ok(audit.get("navigation_decision_invoked") is False, "audit_nav")
    ok(audit.get("runtime_routing_changed") is False, "audit_routing")

    verdict = "GO" if not blockers else "NO_GO"
    _write_json(
        root / "roi_retry_verifier_report_v1.json",
        {
            "schema_version": "roi_retry_verifier_report_v1",
            "verdict": verdict,
            "blockers": blockers,
            "checks_passed": checks,
        },
    )
    print(json.dumps({"verdict": verdict, "blockers": blockers, "checks_passed": checks}, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
