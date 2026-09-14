#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for RealVideo OCR Readability Governance v0."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, List


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


def _op_allowed(ops: List[Any], name: str) -> bool:
    for o in ops:
        if isinstance(o, dict) and o.get("operation") == name:
            return o.get("allowed") is True
    return False


def main() -> int:
    _find_ws_root()
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke-root", required=True)
    args = ap.parse_args()

    root = _require_abs(args.smoke_root, "--smoke-root")
    blockers: List[str] = []

    paths = {
        "summary": root / "realvideo_ocr_readability_governance_summary.json",
        "factors": root / "realvideo_ocr_readability_factor_matrix.json",
        "grades": root / "realvideo_ocr_eligibility_grade_policy.json",
        "partial": root / "realvideo_ocr_partial_evidence_policy.json",
        "enhancement": root / "realvideo_ocr_enhancement_boundary_policy.json",
        "visual": root / "realvideo_ocr_visual_symbol_fallback_policy.json",
        "facility": root / "realvideo_ocr_public_facility_semantic_first_policy.json",
        "multiframe": root / "realvideo_ocr_multiframe_recovery_policy.json",
        "examples": root / "realvideo_ocr_readability_risk_examples_report.json",
        "submission": root / "realvideo_ocr_readability_submission_strategy_update_plan.json",
        "metrics": root / "realvideo_ocr_readability_metrics_binding_plan.json",
        "gov_link": root / "realvideo_ocr_readability_governance_link_report.json",
        "benchmark": root / "realvideo_ocr_readability_benchmark_link_report.json",
        "health": root / "realvideo_ocr_readability_system_health_link_report.json",
        "boundary": root / "realvideo_ocr_readability_no_write_boundary_report.json",
        "sim": root / "realvideo_ocr_readability_simulation_context_report.json",
        "non_claims": root / "realvideo_ocr_readability_non_claims_report.json",
        "followups": root / "realvideo_ocr_readability_open_followups.json",
        "audit": root / "realvideo_ocr_readability_audit_report.json",
    }

    for label, p in paths.items():
        if not p.is_file():
            blockers.append(f"missing:{label}")

    if blockers:
        _write_json(
            root / "realvideo_ocr_readability_verifier_report.json",
            {"verdict": "NO_GO", "blockers": blockers, "checks_passed": 0},
        )
        print(json.dumps({"verdict": "NO_GO", "blockers": blockers}, ensure_ascii=False))
        return 2

    summary = _read_json(paths["summary"])
    factors = _read_json(paths["factors"])
    grades = _read_json(paths["grades"])
    partial = _read_json(paths["partial"])
    enhancement = _read_json(paths["enhancement"])
    visual = _read_json(paths["visual"])
    facility = _read_json(paths["facility"])
    multiframe = _read_json(paths["multiframe"])
    examples = _read_json(paths["examples"])
    submission = _read_json(paths["submission"])
    metrics = _read_json(paths["metrics"])
    gov_link = _read_json(paths["gov_link"])
    benchmark = _read_json(paths["benchmark"])
    health = _read_json(paths["health"])
    boundary = _read_json(paths["boundary"])
    sim = _read_json(paths["sim"])
    non_claims = _read_json(paths["non_claims"])
    followups = _read_json(paths["followups"])
    audit = _read_json(paths["audit"])

    if summary.get("governance_scope") != "readability_governance_only":
        blockers.append("governance_scope")
    if summary.get("ocr_readability_governance_defined") is not True:
        blockers.append("governance_defined")
    if summary.get("ocr_enhancement_boundary_defined") is not True:
        blockers.append("enhancement_boundary_defined")
    if summary.get("runtime_execution") is not False:
        blockers.append("runtime_execution")
    if summary.get("video_loaded") is not False:
        blockers.append("video_loaded")
    if summary.get("frame_sampled") is not False:
        blockers.append("frame_sampled")
    if summary.get("ocr_invoked") is not False:
        blockers.append("ocr_invoked")

    factor_rows = factors.get("factors") or []
    factor_ids = {f.get("factor_id") for f in factor_rows if isinstance(f, dict)}
    if len(factor_rows) < 13:
        blockers.append("factor_count")
    if "occlusion_level" not in factor_ids:
        blockers.append("occlusion_level")
    if "logo_or_visual_symbol_likelihood" not in factor_ids:
        blockers.append("logo_factor")

    grade_rows = {g.get("grade"): g for g in (grades.get("grades") or []) if isinstance(g, dict)}
    for g in ("A", "B", "C", "D", "E"):
        if g not in grade_rows:
            blockers.append(f"grade_{g}")
    if grade_rows.get("D", {}).get("route_to_visual_symbol_evidence") is not True:
        blockers.append("grade_D_visual")
    if grade_rows.get("E", {}).get("ocr_submission_allowed") is not False:
        blockers.append("grade_E_submit")

    if partial.get("raw_ocr_text_must_be_preserved") is not True:
        blockers.append("raw_preserved")
    if partial.get("completion_committed") is not False:
        blockers.append("completion_committed")

    ops = enhancement.get("operations") or []
    if _op_allowed(ops, "overwrite_raw_ocr_text"):
        blockers.append("overwrite_allowed")
    if _op_allowed(ops, "write_enhanced_text_as_fact"):
        blockers.append("write_fact_allowed")

    if visual.get("no_brand_fact_without_registry_or_review") is not True:
        blockers.append("no_brand_fact")

    if facility.get("semantic_first_required") is not True:
        blockers.append("semantic_first")

    if multiframe.get("output_status") != "candidate_only":
        blockers.append("multiframe_output_status")

    ex_ids = {e.get("example_id") for e in (examples.get("examples") or []) if isinstance(e, dict)}
    for eid in ("construction_bank_occluded", "gap_logo_sign", "american_style_glasses_sign"):
        if eid not in ex_ids:
            blockers.append(f"example:{eid}")

    if submission.get("readability_grade_required_before_submission") is not True:
        blockers.append("grade_required")
    if submission.get("grade_D_route_to_visual_symbol") is not True:
        blockers.append("grade_D_route")

    if metrics.get("current_phase_collects_metrics") is not False:
        blockers.append("collects_metrics")

    if gov_link.get("public_facility_governance_linked") is not True:
        blockers.append("facility_linked")

    if benchmark.get("current_phase_updates_benchmark_values") is not False:
        blockers.append("benchmark_update")

    if health.get("provider_health_runtime_checked") is not False:
        blockers.append("health_runtime")

    if boundary.get("boundary_ok") is not True:
        blockers.append("boundary_ok")
    if boundary.get("violations") != []:
        blockers.append("violations")
    if boundary.get("governance_only") is not True:
        blockers.append("governance_only")

    if sim.get("simulation_profile_id") != "developer_full":
        blockers.append("sim_profile")

    if non_claims.get("no_ocr_output_modification") is not True:
        blockers.append("non_claims_modify")
    if non_claims.get("not_benchmark") is not True:
        blockers.append("non_claims_benchmark")

    if not (followups.get("items") or []):
        blockers.append("followups")

    audit_checks = [
        ("video_loaded", False),
        ("frame_sampled", False),
        ("ocr_invoked", False),
        ("rapidocr_invoked", False),
        ("fusion_invoked", False),
        ("scene_delta_candidate_generated", False),
        ("midplatform_fact_written", False),
        ("world_model_written", False),
        ("navigation_decision_invoked", False),
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
        "schema_version": "realvideo_ocr_readability_verifier_report_v0",
        "verdict": verdict,
        "blockers": blockers,
        "checks_passed": 63 - len(blockers),
        "smoke_root": str(root),
    }
    _write_json(root / "realvideo_ocr_readability_verifier_report.json", report)
    print(json.dumps({"verdict": verdict, "blockers": blockers}, ensure_ascii=False))
    return 0 if verdict in ("GO", "CONDITIONAL_GO") else 2


if __name__ == "__main__":
    raise SystemExit(main())
