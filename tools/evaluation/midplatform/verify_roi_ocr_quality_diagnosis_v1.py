#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for ROI OCR Quality Diagnosis v1."""

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
        "summary": "roi_ocr_quality_diagnosis_v1_summary.json",
        "intake": "roi_ocr_quality_diagnosis_intake_matrix_v1.json",
        "rules": "roi_ocr_quality_diagnosis_rule_matrix_v1.json",
        "repeated": "roi_ocr_repeated_text_analysis_report_v1.json",
        "diversity": "roi_ocr_crop_diversity_analysis_report_v1.json",
        "geometry": "roi_ocr_crop_geometry_diagnosis_report_v1.json",
        "frame": "roi_ocr_source_frame_reuse_diagnosis_report_v1.json",
        "linebox": "roi_ocr_linebox_source_diagnosis_report_v1.json",
        "provider": "roi_ocr_provider_output_diagnosis_report_v1.json",
        "hypotheses": "roi_ocr_root_cause_hypothesis_matrix_v1.json",
        "decision": "roi_ocr_quality_diagnosis_decision_matrix_v1.json",
        "future": "roi_ocr_quality_future_fix_plan_v1.json",
        "boundary": "roi_ocr_quality_diagnosis_boundary_report_v1.json",
        "chain": "roi_ocr_quality_source_chain_report_v1.json",
        "metrics": "roi_ocr_quality_metrics_candidate_report_v1.json",
        "bench": "roi_ocr_quality_benchmark_link_report_v1.json",
        "health": "roi_ocr_quality_system_health_link_report_v1.json",
        "no_write": "roi_ocr_quality_no_write_boundary_report_v1.json",
        "sim": "roi_ocr_quality_simulation_context_report_v1.json",
        "non_claims": "roi_ocr_quality_non_claims_report_v1.json",
        "followups": "roi_ocr_quality_open_followups_v1.json",
        "audit": "roi_ocr_quality_audit_report_v1.json",
    }
    data = {}
    for k, f in files.items():
        p = root / f
        if not p.is_file():
            blockers.append(f"missing:{k}")
        else:
            data[k] = _read_json(p)

    if blockers:
        _write_json(root / "roi_ocr_quality_verifier_report_v1.json", {"verdict": "NO_GO", "blockers": blockers})
        print(json.dumps({"verdict": "NO_GO", "blockers": blockers}, ensure_ascii=False))
        return 2

    s = data["summary"]
    audit = data["audit"]
    repeated = data["repeated"]
    diversity = data["diversity"]
    frame = data["frame"]
    linebox = data["linebox"]
    provider = data["provider"]
    hypotheses = data["hypotheses"]

    ok(s.get("diagnosis_scope") == "roi_ocr_quality_diagnosis_only", "scope")
    ok(s.get("based_on_semantic_candidate_v2_roiaware") is True, "based_sem")
    ok(s.get("roi_ocr_result_count_observed") == 12, "ocr_12")
    ok(s.get("semantic_diagnostic_candidate_count_observed") == 12, "sem_12")
    ok(s.get("repeated_same_text_detected") is True, "repeated")
    ok(s.get("low_information_text_detected") is True, "low_info")
    ok(s.get("quality_diagnosis_generated") is True, "diag_gen")
    ok(s.get("root_cause_confirmed") is False, "no_confirmed")
    ok(s.get("new_ocr_invoked") is False, "no_ocr")
    ok(s.get("new_crop_generated") is False, "no_crop")

    ok(data["intake"].get("row_count") == 12, "intake_12")
    rule_ids = [r.get("rule_id") for r in (data["rules"].get("rules") or []) if isinstance(r, dict)]
    ok("repeated_same_text_requires_diagnosis" in rule_ids, "rule_repeat")
    ok("low_information_text_requires_diagnosis" in rule_ids, "rule_low")
    ok("no_source_validation_before_quality_diagnosis" in rule_ids, "rule_no_sv")

    ok(repeated.get("repeated_text_ratio") == 1.0, "ratio_1")
    ok(repeated.get("semantic_success_claim_allowed") is False, "no_sem_success")

    ok(diversity.get("crop_diversity_low") is True, "div_low")
    ok(frame.get("source_frame_reuse_risk") is True, "frame_reuse")
    ok(linebox.get("linebox_not_used_as_evidence") is True, "linebox_not_evidence")
    ok(provider.get("provider_failure_claimed") is False, "no_prov_fail")
    ok(provider.get("provider_comparison_claimed") is False, "no_prov_cmp")

    for row in hypotheses.get("rows") or []:
        if isinstance(row, dict):
            ok(row.get("confirmed") is False, "hyp_confirmed")
            break

    ok(data["decision"].get("rows"), "decision_rows")
    for row in data["decision"].get("rows") or []:
        if isinstance(row, dict):
            ok(row.get("fact_write_allowed") is False, "dec_fact")
            ok(row.get("world_model_attach_allowed") is False, "dec_wm")
            break

    phases = [p.get("future_phase") for p in (data["future"].get("phases") or []) if isinstance(p, dict)]
    ok("Crop-Quality-Scoring-v1" in phases, "future_crop")
    ok("ROI-Crop-Diversity-Check-v1" in phases, "future_div")

    ok(data["boundary"].get("source_validation_v2_invoked") is False, "boundary_sv")
    ok(data["chain"].get("all_traceable_to_semantic_v2") is True, "chain_sem")
    ok(data["metrics"].get("confirmed_root_cause_count") == 0, "metrics_confirmed")
    ok(data["bench"].get("benchmark_score_generated") is False, "bench")
    ok(data["no_write"].get("boundary_ok") is True, "boundary_ok")
    ok(data["sim"].get("simulation_profile_id") == "developer_full", "sim")
    ok(audit.get("roi_ocr_quality_diagnosis_v1_executed") is True, "audit")

    verdict = "GO" if not blockers else "NO_GO"
    _write_json(
        root / "roi_ocr_quality_verifier_report_v1.json",
        {
            "schema_version": "roi_ocr_quality_verifier_report_v1",
            "verdict": verdict,
            "blockers": blockers,
            "checks_passed": checks,
        },
    )
    print(json.dumps({"verdict": verdict, "blockers": blockers, "checks_passed": checks}, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
