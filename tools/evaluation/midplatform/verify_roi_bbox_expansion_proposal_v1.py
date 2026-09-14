#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for ROI BBox Expansion Proposal v1."""

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
        "summary": "roi_bbox_expansion_proposal_v1_summary.json",
        "intake": "roi_bbox_expansion_intake_matrix_v1.json",
        "rules": "roi_bbox_expansion_rule_matrix_v1.json",
        "schema": "roi_bbox_expansion_candidate_schema_v1.json",
        "strategies": "roi_bbox_expansion_strategy_matrix_v1.json",
        "candidates": "roi_bbox_expansion_candidate_collection_v1.json",
        "grouping": "roi_bbox_expansion_source_bbox_grouping_report_v1.json",
        "bounds": "roi_bbox_expansion_bounds_check_report_v1.json",
        "impact": "roi_bbox_expansion_impact_estimate_report_v1.json",
        "risk": "roi_bbox_expansion_risk_report_v1.json",
        "future": "roi_bbox_expansion_future_crop_rerun_plan_v1.json",
        "decision": "roi_bbox_expansion_decision_matrix_v1.json",
        "boundary": "roi_bbox_expansion_boundary_report_v1.json",
        "chain": "roi_bbox_expansion_source_chain_report_v1.json",
        "metrics": "roi_bbox_expansion_metrics_candidate_report_v1.json",
        "bench": "roi_bbox_expansion_benchmark_link_report_v1.json",
        "health": "roi_bbox_expansion_system_health_link_report_v1.json",
        "no_write": "roi_bbox_expansion_no_write_boundary_report_v1.json",
        "sim": "roi_bbox_expansion_simulation_context_report_v1.json",
        "non_claims": "roi_bbox_expansion_non_claims_report_v1.json",
        "followups": "roi_bbox_expansion_open_followups_v1.json",
        "audit": "roi_bbox_expansion_audit_report_v1.json",
    }
    data = {}
    for k, f in files.items():
        p = root / f
        if not p.is_file():
            blockers.append(f"missing:{k}")
        else:
            data[k] = _read_json(p)

    if blockers:
        _write_json(
            root / "roi_bbox_expansion_verifier_report_v1.json",
            {"verdict": "NO_GO", "blockers": blockers, "checks_passed": 0},
        )
        print(json.dumps({"verdict": "NO_GO", "blockers": blockers}, ensure_ascii=False))
        return 2

    s = data["summary"]
    audit = data["audit"]
    rule_ids = [r.get("rule_id") for r in (data["rules"].get("rules") or []) if isinstance(r, dict)]
    strat_ids = [x.get("strategy_id") for x in (data["strategies"].get("strategies") or []) if isinstance(x, dict)]

    ok(s.get("proposal_scope") == "bbox_expansion_proposal_only", "scope")
    ok(s.get("based_on_roi_crop_diversity_check") is True, "based_div")
    ok(s.get("based_on_roi_ocr_quality_diagnosis") is True, "based_diag")
    ok(s.get("bbox_expansion_proposal_generated") is True, "prop_gen")
    ok(s.get("new_crop_generated") is False, "no_crop")
    ok(s.get("new_ocr_invoked") is False, "no_ocr")
    ok(s.get("new_frame_extracted") is False, "no_frame")

    ok(data["intake"].get("row_count") == 12, "intake_12")
    ok("original_bbox_must_be_preserved" in rule_ids, "rule_preserve")
    ok("no_crop_generation_in_this_phase" in rule_ids, "rule_no_crop")
    ok("no_ocr_execution_in_this_phase" in rule_ids, "rule_no_ocr")

    ok(data["schema"].get("template"), "schema_tpl")
    ok("padding_small" in strat_ids, "strat_small")
    ok("padding_medium" in strat_ids, "strat_medium")
    ok("line_region_expand" in strat_ids, "strat_line")
    ok("contextual_expand" in strat_ids, "strat_ctx")

    ok(data["candidates"].get("candidate_count", 0) >= 4, "cand_4")
    groups = data["grouping"].get("groups") or []
    ok(data["grouping"].get("source_bbox_group_count") == 1, "group_1")
    if groups and isinstance(groups[0], dict):
        ok(groups[0].get("member_count") == 12, "member_12")

    bounds_ok = True
    for row in data["bounds"].get("rows") or []:
        if not isinstance(row, dict):
            continue
        st = row.get("bounds_status")
        if st == "invalid":
            bounds_ok = False
            break
        if st not in ("within_bounds", "clipped", "unknown_frame_bounds"):
            bounds_ok = False
            break
        if st == "within_bounds" and row.get("within_bounds") is not True:
            bounds_ok = False
            break
    ok(bounds_ok, "bounds_ok")

    ok(data["impact"].get("estimate_is_diagnostic_only") is True, "impact_diag")
    for row in data["risk"].get("rows") or []:
        if isinstance(row, dict):
            ok(row.get("requires_future_crop_quality_scoring") is True, "risk_scoring")
            break

    ok(data["future"].get("future_phase") == "ROI-Crop-Execution-DryRun-v2-BBoxExpansion", "future_phase")
    for row in data["decision"].get("rows") or []:
        if isinstance(row, dict):
            ok(row.get("fact_write_allowed") is False, "dec_fact")
            break

    ok(data["boundary"].get("source_validation_v2_invoked") is False, "boundary_sv")
    ok(data["chain"].get("all_traceable_to_diversity_check") is True, "chain_div")
    for row in data["chain"].get("rows") or []:
        if isinstance(row, dict):
            ok(row.get("traceable_to_crop_artifact") is True, "chain_crop")
            break

    ok(data["metrics"].get("new_crop_generated_count") == 0, "metrics_no_crop")
    ok(data["metrics"].get("new_ocr_invoked_count") == 0, "metrics_no_ocr")
    ok(data["bench"].get("benchmark_score_generated") is False, "bench")
    ok(data["health"].get("provider_health_runtime_checked") is False, "health")
    ok(data["no_write"].get("boundary_ok") is True, "boundary_ok")
    ok(data["no_write"].get("violations") == [], "no_violations")
    ok(data["sim"].get("simulation_profile_id") == "developer_full", "sim")
    ok(audit.get("roi_bbox_expansion_proposal_v1_executed") is True, "audit")
    ok(audit.get("world_model_attach_executed") is False, "audit_wm")
    ok(audit.get("midplatform_fact_written") is False, "audit_fact")

    verdict = "GO" if not blockers else "NO_GO"
    _write_json(
        root / "roi_bbox_expansion_verifier_report_v1.json",
        {
            "schema_version": "roi_bbox_expansion_verifier_report_v1",
            "verdict": verdict,
            "blockers": blockers,
            "checks_passed": checks,
        },
    )
    print(json.dumps({"verdict": verdict, "blockers": blockers, "checks_passed": checks}, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
