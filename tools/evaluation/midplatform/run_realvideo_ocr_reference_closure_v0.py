#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase-RealVideo-OCR-Reference-Closure-001 runner."""

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
    ap.add_argument("--realvideo-reference-update-root", required=True)
    ap.add_argument("--realvideo-readonly-consumer-root", required=True)
    ap.add_argument("--realvideo-gated-submission-root", required=True)
    ap.add_argument("--realvideo-roi-to-ocr-reference-root", required=True)
    ap.add_argument("--realvideo-frame-sample-root", required=True)
    ap.add_argument("--realvideo-case-registry-root", required=True)
    ap.add_argument("--vision-roi-proposal-root", required=True)
    ap.add_argument("--vision-roi-to-ocr-bridge-root", required=True)
    ap.add_argument("--benchmark-real-values-smoke-root", required=True)
    ap.add_argument("--system-health-governance-root", required=True)
    ap.add_argument("--simulation-lab-harness-root", required=True)
    args = ap.parse_args()

    out = _require_abs(args.output_root, "--output-root")
    out.mkdir(parents=True, exist_ok=True)

    from capabilities.midplatform.realvideo_ocr_reference_closure_v0 import (
        run_realvideo_ocr_reference_closure_v0,
    )

    ref_upd = _require_abs(args.realvideo_reference_update_root, "reference-update")
    consumer = _require_abs(args.realvideo_readonly_consumer_root, "readonly-consumer")
    gated = _require_abs(args.realvideo_gated_submission_root, "gated-submission")
    roi_ref = _require_abs(args.realvideo_roi_to_ocr_reference_root, "roi-reference")
    frame = _require_abs(args.realvideo_frame_sample_root, "frame-sample")
    registry = _require_abs(args.realvideo_case_registry_root, "case-registry")
    proposal = _require_abs(args.vision_roi_proposal_root, "vision-proposal")
    bridge = _require_abs(args.vision_roi_to_ocr_bridge_root, "vision-bridge")
    bench = _require_abs(args.benchmark_real_values_smoke_root, "benchmark")
    health = _require_abs(args.system_health_governance_root, "health")
    sim = _require_abs(args.simulation_lab_harness_root, "sim")

    (
        summary,
        phase_matrix,
        lineage,
        alignment_closure,
        rejected_closure,
        empty_closure,
        case_mapping_closure,
        provider_closure,
        metrics,
        benchmark_link,
        health_link,
        boundary,
        sim_report,
        non_claims,
        followups,
        audit,
        errs,
    ) = run_realvideo_ocr_reference_closure_v0(
        realvideo_reference_update_root=str(ref_upd),
        realvideo_readonly_consumer_root=str(consumer),
        realvideo_gated_submission_root=str(gated),
        realvideo_roi_to_ocr_reference_root=str(roi_ref),
        realvideo_frame_sample_root=str(frame),
        realvideo_case_registry_root=str(registry),
        vision_roi_proposal_root=str(proposal),
        vision_roi_to_ocr_bridge_root=str(bridge),
        benchmark_real_values_smoke_root=str(bench),
        system_health_governance_root=str(health),
        simulation_lab_harness_root=str(sim),
        output_root=str(out),
    )

    summary["output_root"] = str(out)
    summary["input_roots"] = {
        "realvideo_reference_update_root": str(ref_upd),
        "realvideo_readonly_consumer_root": str(consumer),
        "realvideo_gated_submission_root": str(gated),
        "realvideo_roi_to_ocr_reference_root": str(roi_ref),
        "realvideo_frame_sample_root": str(frame),
        "realvideo_case_registry_root": str(registry),
        "vision_roi_proposal_root": str(proposal),
        "vision_roi_to_ocr_bridge_root": str(bridge),
        "benchmark_real_values_smoke_root": str(bench),
        "system_health_governance_root": str(health),
        "simulation_lab_harness_root": str(sim),
    }
    if errs:
        summary["errors"] = errs

    _write_json(out / "realvideo_ocr_reference_closure_summary.json", summary)
    _write_json(out / "realvideo_ocr_reference_closure_phase_matrix.json", phase_matrix)
    _write_json(out / "realvideo_ocr_reference_lineage_closure_report.json", lineage)
    _write_json(out / "realvideo_ocr_reference_alignment_closure_report.json", alignment_closure)
    _write_json(out / "realvideo_ocr_reference_rejected_roi_closure_report.json", rejected_closure)
    _write_json(out / "realvideo_ocr_reference_empty_text_closure_report.json", empty_closure)
    _write_json(out / "realvideo_ocr_reference_case_mapping_closure_report.json", case_mapping_closure)
    _write_json(out / "realvideo_ocr_reference_provider_closure_report.json", provider_closure)
    _write_json(out / "realvideo_ocr_reference_metrics_closure_candidate_report.json", metrics)
    _write_json(out / "realvideo_ocr_reference_closure_benchmark_link_report.json", benchmark_link)
    _write_json(out / "realvideo_ocr_reference_closure_system_health_link_report.json", health_link)
    _write_json(out / "realvideo_ocr_reference_closure_no_write_boundary_report.json", boundary)
    _write_json(out / "realvideo_ocr_reference_closure_simulation_context_report.json", sim_report)
    _write_json(out / "realvideo_ocr_reference_closure_non_claims_report.json", non_claims)
    _write_json(out / "realvideo_ocr_reference_closure_open_followups.json", followups)
    _write_json(out / "realvideo_ocr_reference_closure_audit_report.json", audit)

    (out / "realvideo_ocr_reference_closure_notes.md").write_text(
        "\n".join(
            [
                "# RealVideo OCR Reference Closure",
                "",
                f"- Phase: {summary.get('phase')}",
                f"- closure_scope: {summary.get('closure_scope')}",
                f"- realvideo_ocr_reference_status: {summary.get('realvideo_ocr_reference_status')}",
                f"- aligned_ocr_evidence_count: {summary.get('aligned_ocr_evidence_count')}",
                f"- empty_text_count: {summary.get('empty_text_count')}",
                f"- phase_verdict_hint: {summary.get('phase_verdict_hint')}",
                "",
                "Reference chain closure only; no OCR re-run, no fusion, no writes.",
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
