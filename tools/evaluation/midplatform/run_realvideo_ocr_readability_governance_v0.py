#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase-RealVideo-OCR-Readability-Governance-001 runner."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def _find_ws_root() -> Path:
    here = Path(__file__).resolve()
    for parent in here.parents:
        if (parent / "capabilities" / "midplatform").is_dir():
            if (parent / "_eval_out").is_dir():
                return parent
            sibling = parent.parent / "Luna-Workspace-Min"
            if (sibling / "_eval_out").is_dir():
                return sibling
            return parent
    return here.parents[3]


WS_ROOT = _find_ws_root()
if str(WS_ROOT) not in sys.path:
    sys.path.insert(0, str(WS_ROOT))


def _require_abs(p: str, label: str) -> Path:
    pp = Path(p).expanduser()
    if not pp.is_absolute():
        raise SystemExit(f"ERROR: {label} must be absolute, got: {p}")
    return pp.resolve()


def _write_json(path: Path, obj: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output-root", required=True)
    ap.add_argument("--text-bearing-sample-planning-root", required=True)
    ap.add_argument("--realvideo-reference-closure-root", required=True)
    ap.add_argument("--realvideo-reference-update-root", required=True)
    ap.add_argument("--realvideo-readonly-consumer-root", required=True)
    ap.add_argument("--existing-video-candidate-scan-root", required=True)
    ap.add_argument("--poster-fusion-gate-chain-closure-root", required=True)
    ap.add_argument("--public-facility-governance-root", required=True)
    ap.add_argument("--benchmark-real-values-smoke-root", required=True)
    ap.add_argument("--system-health-governance-root", required=True)
    ap.add_argument("--simulation-lab-harness-root", required=True)
    args = ap.parse_args()

    out = _require_abs(args.output_root, "--output-root")

    from capabilities.midplatform.realvideo_ocr_readability_governance_v0 import (
        run_realvideo_ocr_readability_governance_v0,
    )

    roots = {
        "planning": _require_abs(args.text_bearing_sample_planning_root, "planning"),
        "closure": _require_abs(args.realvideo_reference_closure_root, "closure"),
        "ref_upd": _require_abs(args.realvideo_reference_update_root, "ref-upd"),
        "consumer": _require_abs(args.realvideo_readonly_consumer_root, "consumer"),
        "scan": _require_abs(args.existing_video_candidate_scan_root, "scan"),
        "poster": _require_abs(args.poster_fusion_gate_chain_closure_root, "poster"),
        "facility": _require_abs(args.public_facility_governance_root, "facility"),
        "bench": _require_abs(args.benchmark_real_values_smoke_root, "bench"),
        "health": _require_abs(args.system_health_governance_root, "health"),
        "sim": _require_abs(args.simulation_lab_harness_root, "sim"),
    }

    (
        summary,
        factor_matrix,
        eligibility_policy,
        partial_policy,
        enhancement_boundary,
        visual_fallback,
        facility_policy,
        multiframe_policy,
        risk_examples,
        submission_plan,
        metrics_binding,
        governance_link,
        benchmark_link,
        health_link,
        boundary,
        sim_report,
        non_claims,
        followups,
        audit,
        errs,
    ) = run_realvideo_ocr_readability_governance_v0(
        text_bearing_sample_planning_root=str(roots["planning"]),
        realvideo_reference_closure_root=str(roots["closure"]),
        realvideo_reference_update_root=str(roots["ref_upd"]),
        realvideo_readonly_consumer_root=str(roots["consumer"]),
        existing_video_candidate_scan_root=str(roots["scan"]),
        poster_fusion_gate_chain_closure_root=str(roots["poster"]),
        public_facility_governance_root=str(roots["facility"]),
        benchmark_real_values_smoke_root=str(roots["bench"]),
        system_health_governance_root=str(roots["health"]),
        simulation_lab_harness_root=str(roots["sim"]),
        output_root=str(out),
    )

    summary["output_root"] = str(out.resolve())
    summary["input_roots"] = {k: str(v) for k, v in roots.items()}
    if errs:
        summary["errors"] = errs

    _write_json(out / "realvideo_ocr_readability_governance_summary.json", summary)
    _write_json(out / "realvideo_ocr_readability_factor_matrix.json", factor_matrix)
    _write_json(out / "realvideo_ocr_eligibility_grade_policy.json", eligibility_policy)
    _write_json(out / "realvideo_ocr_partial_evidence_policy.json", partial_policy)
    _write_json(out / "realvideo_ocr_enhancement_boundary_policy.json", enhancement_boundary)
    _write_json(out / "realvideo_ocr_visual_symbol_fallback_policy.json", visual_fallback)
    _write_json(out / "realvideo_ocr_public_facility_semantic_first_policy.json", facility_policy)
    _write_json(out / "realvideo_ocr_multiframe_recovery_policy.json", multiframe_policy)
    _write_json(out / "realvideo_ocr_readability_risk_examples_report.json", risk_examples)
    _write_json(out / "realvideo_ocr_readability_submission_strategy_update_plan.json", submission_plan)
    _write_json(out / "realvideo_ocr_readability_metrics_binding_plan.json", metrics_binding)
    _write_json(out / "realvideo_ocr_readability_governance_link_report.json", governance_link)
    _write_json(out / "realvideo_ocr_readability_benchmark_link_report.json", benchmark_link)
    _write_json(out / "realvideo_ocr_readability_system_health_link_report.json", health_link)
    _write_json(out / "realvideo_ocr_readability_no_write_boundary_report.json", boundary)
    _write_json(out / "realvideo_ocr_readability_simulation_context_report.json", sim_report)
    _write_json(out / "realvideo_ocr_readability_non_claims_report.json", non_claims)
    _write_json(out / "realvideo_ocr_readability_open_followups.json", followups)
    _write_json(out / "realvideo_ocr_readability_audit_report.json", audit)

    (out / "realvideo_ocr_readability_notes.md").write_text(
        "\n".join(
            [
                "# RealVideo OCR Readability Governance",
                "",
                f"- Phase: {summary.get('phase')}",
                f"- governance_scope: {summary.get('governance_scope')}",
                f"- phase_verdict_hint: {summary.get('phase_verdict_hint')}",
                "",
                "Governance only; no video/OCR/evidence/fact writes.",
                "",
            ]
        ),
        encoding="utf-8",
    )

    print(
        json.dumps(
            {"output_root": str(out), "phase_verdict_hint": summary.get("phase_verdict_hint"), "errors": errs},
            ensure_ascii=False,
        )
    )
    return 0 if summary.get("phase_verdict_hint") in ("GO", "CONDITIONAL_GO") else 1


if __name__ == "__main__":
    raise SystemExit(main())
