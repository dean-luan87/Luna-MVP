#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase-RealVideo-OCR-Reference-Update-001 runner."""

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
    ap.add_argument("--realvideo-roi-to-ocr-reference-root", required=True)
    ap.add_argument("--realvideo-gated-submission-root", required=True)
    ap.add_argument("--realvideo-readonly-consumer-root", required=True)
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

    from capabilities.midplatform.realvideo_ocr_reference_update_v0 import (
        run_realvideo_ocr_reference_update_v0,
    )

    roi_ref = _require_abs(args.realvideo_roi_to_ocr_reference_root, "roi-to-ocr-reference")
    gated = _require_abs(args.realvideo_gated_submission_root, "gated-submission")
    consumer = _require_abs(args.realvideo_readonly_consumer_root, "readonly-consumer")
    frame = _require_abs(args.realvideo_frame_sample_root, "frame-sample")
    registry = _require_abs(args.realvideo_case_registry_root, "case-registry")
    proposal = _require_abs(args.vision_roi_proposal_root, "vision-roi-proposal")
    bridge = _require_abs(args.vision_roi_to_ocr_bridge_root, "vision-roi-bridge")
    bench = _require_abs(args.benchmark_real_values_smoke_root, "benchmark")
    health = _require_abs(args.system_health_governance_root, "health")
    sim = _require_abs(args.simulation_lab_harness_root, "sim")

    (
        summary,
        candidate,
        alignment,
        rejected_preserve,
        empty_guard,
        case_mapping,
        source_chain,
        metrics,
        benchmark_link,
        health_link,
        boundary,
        sim_report,
        non_claims,
        followups,
        audit,
        errs,
    ) = run_realvideo_ocr_reference_update_v0(
        realvideo_roi_to_ocr_reference_root=str(roi_ref),
        realvideo_gated_submission_root=str(gated),
        realvideo_readonly_consumer_root=str(consumer),
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
        "realvideo_roi_to_ocr_reference_root": str(roi_ref),
        "realvideo_gated_submission_root": str(gated),
        "realvideo_readonly_consumer_root": str(consumer),
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

    _write_json(out / "realvideo_ocr_reference_update_summary.json", summary)
    _write_json(out / "realvideo_ocr_updated_reference_candidate.json", candidate)
    _write_json(out / "realvideo_ocr_reference_update_alignment_matrix.json", alignment)
    _write_json(
        out / "realvideo_ocr_reference_update_rejected_roi_preservation_report.json",
        rejected_preserve,
    )
    _write_json(out / "realvideo_ocr_reference_update_empty_text_guard_report.json", empty_guard)
    _write_json(out / "realvideo_ocr_reference_update_case_mapping_report.json", case_mapping)
    _write_json(out / "realvideo_ocr_reference_update_source_chain_report.json", source_chain)
    _write_json(out / "realvideo_ocr_reference_update_metrics_candidate_report.json", metrics)
    _write_json(out / "realvideo_ocr_reference_update_benchmark_link_report.json", benchmark_link)
    _write_json(out / "realvideo_ocr_reference_update_system_health_link_report.json", health_link)
    _write_json(out / "realvideo_ocr_reference_update_no_write_boundary_report.json", boundary)
    _write_json(out / "realvideo_ocr_reference_update_simulation_context_report.json", sim_report)
    _write_json(out / "realvideo_ocr_reference_update_non_claims_report.json", non_claims)
    _write_json(out / "realvideo_ocr_reference_update_open_followups.json", followups)
    _write_json(out / "realvideo_ocr_reference_update_audit_report.json", audit)

    (out / "realvideo_ocr_reference_update_notes.md").write_text(
        "\n".join(
            [
                "# RealVideo OCR Reference Update",
                "",
                f"- Phase: {summary.get('phase')}",
                f"- reference_scope: {summary.get('reference_scope')}",
                f"- roi_reference_count: {summary.get('roi_reference_count')}",
                f"- ocr_evidence_ref_count: {summary.get('ocr_evidence_ref_count')}",
                f"- empty_text_count: {summary.get('empty_text_count')}",
                f"- phase_verdict_hint: {summary.get('phase_verdict_hint')}",
                "",
                "Parallel reference update only; no OCR re-run, no fusion, no writes.",
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
