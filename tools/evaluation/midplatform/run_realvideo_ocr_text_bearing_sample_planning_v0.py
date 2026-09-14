#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase-RealVideo-OCR-Text-Bearing-Sample-Planning-001 runner."""

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
    ap.add_argument("--realvideo-reference-closure-root", required=True)
    ap.add_argument("--realvideo-reference-update-root", required=True)
    ap.add_argument("--realvideo-readonly-consumer-root", required=True)
    ap.add_argument("--realvideo-gated-submission-root", required=True)
    ap.add_argument("--realvideo-roi-to-ocr-reference-root", required=True)
    ap.add_argument("--realvideo-frame-sample-root", required=True)
    ap.add_argument("--realvideo-case-registry-root", required=True)
    ap.add_argument("--benchmark-real-values-smoke-root", required=True)
    ap.add_argument("--system-health-governance-root", required=True)
    ap.add_argument("--simulation-lab-harness-root", required=True)
    args = ap.parse_args()

    out = _require_abs(args.output_root, "--output-root")
    out.mkdir(parents=True, exist_ok=True)

    from capabilities.midplatform.realvideo_ocr_text_bearing_sample_planning_v0 import (
        run_realvideo_ocr_text_bearing_sample_planning_v0,
    )

    closure = _require_abs(args.realvideo_reference_closure_root, "closure")
    ref_upd = _require_abs(args.realvideo_reference_update_root, "reference-update")
    consumer = _require_abs(args.realvideo_readonly_consumer_root, "consumer")
    gated = _require_abs(args.realvideo_gated_submission_root, "gated")
    roi_ref = _require_abs(args.realvideo_roi_to_ocr_reference_root, "roi-ref")
    frame = _require_abs(args.realvideo_frame_sample_root, "frame")
    registry = _require_abs(args.realvideo_case_registry_root, "registry")
    bench = _require_abs(args.benchmark_real_values_smoke_root, "benchmark")
    health = _require_abs(args.system_health_governance_root, "health")
    sim = _require_abs(args.simulation_lab_harness_root, "sim")

    (
        summary,
        diagnosis,
        sample_definition,
        case_matrix,
        frame_sampling,
        roi_selection,
        gt_plan,
        quality_labels,
        future_chain,
        metrics_binding,
        governance_link,
        acquisition_checklist,
        benchmark_link,
        health_link,
        boundary,
        sim_report,
        non_claims,
        followups,
        audit,
        errs,
    ) = run_realvideo_ocr_text_bearing_sample_planning_v0(
        realvideo_reference_closure_root=str(closure),
        realvideo_reference_update_root=str(ref_upd),
        realvideo_readonly_consumer_root=str(consumer),
        realvideo_gated_submission_root=str(gated),
        realvideo_roi_to_ocr_reference_root=str(roi_ref),
        realvideo_frame_sample_root=str(frame),
        realvideo_case_registry_root=str(registry),
        benchmark_real_values_smoke_root=str(bench),
        system_health_governance_root=str(health),
        simulation_lab_harness_root=str(sim),
        output_root=str(out),
    )

    summary["output_root"] = str(out)
    summary["input_roots"] = {
        "realvideo_reference_closure_root": str(closure),
        "realvideo_reference_update_root": str(ref_upd),
        "realvideo_readonly_consumer_root": str(consumer),
        "realvideo_gated_submission_root": str(gated),
        "realvideo_roi_to_ocr_reference_root": str(roi_ref),
        "realvideo_frame_sample_root": str(frame),
        "realvideo_case_registry_root": str(registry),
        "benchmark_real_values_smoke_root": str(bench),
        "system_health_governance_root": str(health),
        "simulation_lab_harness_root": str(sim),
    }
    if errs:
        summary["errors"] = errs

    _write_json(out / "realvideo_ocr_text_bearing_sample_planning_summary.json", summary)
    _write_json(out / "realvideo_ocr_text_bearing_prior_closure_diagnosis_report.json", diagnosis)
    _write_json(out / "realvideo_ocr_text_bearing_sample_definition.json", sample_definition)
    _write_json(out / "realvideo_ocr_text_bearing_planned_case_matrix.json", case_matrix)
    _write_json(out / "realvideo_ocr_text_bearing_frame_sampling_strategy_plan.json", frame_sampling)
    _write_json(out / "realvideo_ocr_text_bearing_roi_selection_strategy_plan.json", roi_selection)
    _write_json(out / "realvideo_ocr_text_bearing_ground_truth_requirement_plan.json", gt_plan)
    _write_json(out / "realvideo_ocr_text_bearing_quality_risk_label_plan.json", quality_labels)
    _write_json(out / "realvideo_ocr_text_bearing_future_execution_chain_plan.json", future_chain)
    _write_json(out / "realvideo_ocr_text_bearing_metrics_binding_plan.json", metrics_binding)
    _write_json(out / "realvideo_ocr_text_bearing_governance_link_plan.json", governance_link)
    _write_json(out / "realvideo_ocr_text_bearing_sample_acquisition_checklist.json", acquisition_checklist)
    _write_json(out / "realvideo_ocr_text_bearing_benchmark_link_report.json", benchmark_link)
    _write_json(out / "realvideo_ocr_text_bearing_system_health_link_report.json", health_link)
    _write_json(out / "realvideo_ocr_text_bearing_no_write_boundary_report.json", boundary)
    _write_json(out / "realvideo_ocr_text_bearing_simulation_context_report.json", sim_report)
    _write_json(out / "realvideo_ocr_text_bearing_non_claims_report.json", non_claims)
    _write_json(out / "realvideo_ocr_text_bearing_open_followups.json", followups)
    _write_json(out / "realvideo_ocr_text_bearing_audit_report.json", audit)

    (out / "realvideo_ocr_text_bearing_notes.md").write_text(
        "\n".join(
            [
                "# RealVideo OCR Text-Bearing Sample Planning",
                "",
                f"- Phase: {summary.get('phase')}",
                f"- planning_scope: {summary.get('planning_scope')}",
                f"- prior_realvideo_reference_verdict: {summary.get('prior_realvideo_reference_verdict')}",
                f"- planning_case_count: {summary.get('planning_case_count')}",
                f"- phase_verdict_hint: {summary.get('phase_verdict_hint')}",
                "",
                "Planning only; no video load, no frame sampling, no OCR.",
                "",
            ]
        ),
        encoding="utf-8",
    )

    print(
        json.dumps(
            {
                "output_root": str(out),
                "phase_verdict_hint": summary.get("phase_verdict_hint"),
                "errors": errs,
            },
            ensure_ascii=False,
        )
    )
    return 0 if summary.get("phase_verdict_hint") in ("GO", "CONDITIONAL_GO") else 1


if __name__ == "__main__":
    raise SystemExit(main())
