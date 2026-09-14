#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for ROI Crop Diversity Check v1."""

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
        "summary": "roi_crop_diversity_check_v1_summary.json",
        "intake": "roi_crop_diversity_intake_matrix_v1.json",
        "rules": "roi_crop_diversity_rule_matrix_v1.json",
        "bbox": "roi_crop_bbox_diversity_report_v1.json",
        "frame": "roi_crop_frame_diversity_report_v1.json",
        "linebox": "roi_crop_linebox_diversity_report_v1.json",
        "file_dim": "roi_crop_file_dimension_diversity_report_v1.json",
        "proposal": "roi_crop_proposal_mapping_diversity_report_v1.json",
        "score": "roi_crop_diversity_score_report_v1.json",
        "dup": "roi_crop_duplicate_group_report_v1.json",
        "risk": "roi_crop_diversity_risk_decision_matrix_v1.json",
        "future": "roi_crop_diversity_future_fix_plan_v1.json",
        "boundary": "roi_crop_diversity_boundary_report_v1.json",
        "chain": "roi_crop_diversity_source_chain_report_v1.json",
        "metrics": "roi_crop_diversity_metrics_candidate_report_v1.json",
        "bench": "roi_crop_diversity_benchmark_link_report_v1.json",
        "health": "roi_crop_diversity_system_health_link_report_v1.json",
        "no_write": "roi_crop_diversity_no_write_boundary_report_v1.json",
        "sim": "roi_crop_diversity_simulation_context_report_v1.json",
        "non_claims": "roi_crop_diversity_non_claims_report_v1.json",
        "followups": "roi_crop_diversity_open_followups_v1.json",
        "audit": "roi_crop_diversity_audit_report_v1.json",
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
            root / "roi_crop_diversity_verifier_report_v1.json",
            {"verdict": "NO_GO", "blockers": blockers, "checks_passed": 0},
        )
        print(json.dumps({"verdict": "NO_GO", "blockers": blockers}, ensure_ascii=False))
        return 2

    s = data["summary"]
    audit = data["audit"]
    rule_ids = [r.get("rule_id") for r in (data["rules"].get("rules") or []) if isinstance(r, dict)]
    future_phases = [p.get("future_phase") for p in (data["future"].get("phases") or []) if isinstance(p, dict)]
    dup_types = [g.get("group_type") for g in (data["dup"].get("rows") or []) if isinstance(g, dict)]

    ok(s.get("check_scope") == "roi_crop_diversity_check_only", "scope")
    ok(s.get("based_on_roi_ocr_quality_diagnosis") is True, "based_diag")
    ok(s.get("crop_count_observed") == 12, "crop_12")
    ok(s.get("diversity_check_generated") is True, "div_gen")
    ok(s.get("root_cause_confirmed") is False, "no_root")
    ok(s.get("new_crop_generated") is False, "no_crop")
    ok(s.get("new_ocr_invoked") is False, "no_ocr")
    ok(s.get("new_frame_extracted") is False, "no_frame")

    ok(data["intake"].get("row_count") == 12, "intake_12")
    ok("repeated_bbox_requires_diversity_check" in rule_ids, "rule_bbox")
    ok("repeated_frame_requires_diversity_check" in rule_ids, "rule_frame")
    ok("repeated_linebox_requires_diversity_check" in rule_ids, "rule_linebox")

    ok(data["bbox"].get("unique_bbox_count") == 1, "unique_bbox_1")
    ok(data["bbox"].get("bbox_diversity_low") is True, "bbox_low")
    ok(data["frame"].get("unique_frame_count") == 1, "unique_frame_1")
    ok(data["frame"].get("frame_diversity_low") is True, "frame_low")
    ok(data["linebox"].get("linebox_reuse_risk") is True, "lb_reuse")
    ok(data["linebox"].get("linebox_text_used_as_evidence") is False, "lb_no_evidence")

    fd = data["file_dim"]
    ok(fd.get("repeated_dimension_risk") is True or fd.get("crop_dimension_reuse_risk") is True, "dim_risk")

    pr = data["proposal"]
    ok(pr.get("many_proposals_to_one_bbox") is True, "many_bbox")
    ok(pr.get("many_proposals_to_one_frame") is True, "many_frame")

    ok(data["score"].get("quality_claim_allowed") is False, "no_quality_claim")
    ok("combined" in dup_types, "combined_dup")

    for row in data["risk"].get("rows") or []:
        if isinstance(row, dict):
            ok(row.get("blocked_source_validation_v2") is True, "blocked_sv")
            ok(row.get("blocked_world_model_attach") is True, "blocked_wm")
            break

    ok("ROI-BBox-Expansion-Proposal-v1" in future_phases, "future_bbox")
    ok("Multiframe-Merge-Proposal-v1" in future_phases, "future_multi")

    ok(data["boundary"].get("source_validation_v2_invoked") is False, "boundary_sv")
    ok(data["chain"].get("all_traceable_to_quality_diagnosis") is True, "chain_diag")
    ok(data["metrics"].get("crop_diversity_low") is True, "metrics_low")
    ok(data["metrics"].get("source_validation_v2_allowed") is False, "metrics_no_sv")
    ok(data["bench"].get("benchmark_score_generated") is False, "bench_no_score")
    ok(data["health"].get("provider_health_runtime_checked") is False, "health_no_runtime")
    ok(data["no_write"].get("boundary_ok") is True, "boundary_ok")
    ok(data["no_write"].get("violations") == [], "no_violations")
    ok(data["sim"].get("simulation_profile_id") == "developer_full", "sim_profile")
    ok(audit.get("roi_crop_diversity_check_v1_executed") is True, "audit_exec")
    ok(audit.get("world_model_attach_executed") is False, "audit_wm")
    ok(audit.get("midplatform_fact_written") is False, "audit_fact")
    ok(audit.get("runtime_routing_changed") is False, "audit_routing")

    verdict = "GO" if not blockers else "NO_GO"
    _write_json(
        root / "roi_crop_diversity_verifier_report_v1.json",
        {
            "schema_version": "roi_crop_diversity_verifier_report_v1",
            "verdict": verdict,
            "blockers": blockers,
            "checks_passed": checks,
        },
    )
    print(json.dumps({"verdict": verdict, "blockers": blockers, "checks_passed": checks}, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
