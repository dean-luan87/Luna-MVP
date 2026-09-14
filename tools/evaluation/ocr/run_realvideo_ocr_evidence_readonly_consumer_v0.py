#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase-RealVideo-OCR-Evidence-ReadOnly-Consumer-001 runner."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def _find_ws_root() -> Path:
    here = Path(__file__).resolve()
    for parent in here.parents:
        if (parent / "capabilities" / "ocr_runtime").is_dir():
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

    from capabilities.ocr_runtime.realvideo_ocr_evidence_readonly_consumer_v0 import (
        run_realvideo_ocr_evidence_readonly_consumer_v0,
    )

    roots = {
        "gated_submission": _require_abs(args.realvideo_gated_submission_root, "gated-submission"),
        "roi_ref": _require_abs(args.realvideo_roi_to_ocr_reference_root, "roi-ref"),
        "frame_sample": _require_abs(args.realvideo_frame_sample_root, "frame-sample"),
        "case_registry": _require_abs(args.realvideo_case_registry_root, "case-registry"),
        "vision_proposal": _require_abs(args.vision_roi_proposal_root, "vision-proposal"),
        "vision_bridge": _require_abs(args.vision_roi_to_ocr_bridge_root, "vision-bridge"),
        "bench": _require_abs(args.benchmark_real_values_smoke_root, "bench"),
        "health": _require_abs(args.system_health_governance_root, "health"),
        "sim": _require_abs(args.simulation_lab_harness_root, "sim"),
    }

    (
        summary,
        by_candidate,
        by_frame,
        by_roi,
        by_case,
        empty_guard,
        rejected_carryover,
        provider_summary,
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
    ) = run_realvideo_ocr_evidence_readonly_consumer_v0(
        realvideo_gated_submission_root=str(roots["gated_submission"]),
        realvideo_roi_to_ocr_reference_root=str(roots["roi_ref"]),
        realvideo_frame_sample_root=str(roots["frame_sample"]),
        realvideo_case_registry_root=str(roots["case_registry"]),
        vision_roi_proposal_root=str(roots["vision_proposal"]),
        vision_roi_to_ocr_bridge_root=str(roots["vision_bridge"]),
        benchmark_real_values_smoke_root=str(roots["bench"]),
        system_health_governance_root=str(roots["health"]),
        simulation_lab_harness_root=str(roots["sim"]),
        output_root=str(out),
    )

    summary["input_roots"] = {k: str(v) for k, v in roots.items()}
    if errs:
        summary["errors"] = errs

    _write_json(out / "realvideo_ocr_evidence_readonly_consumer_summary.json", summary)
    _write_json(out / "realvideo_ocr_evidence_by_candidate_index.json", by_candidate)
    _write_json(out / "realvideo_ocr_evidence_by_frame_index.json", by_frame)
    _write_json(out / "realvideo_ocr_evidence_by_roi_index.json", by_roi)
    _write_json(out / "realvideo_ocr_evidence_by_case_index.json", by_case)
    _write_json(out / "realvideo_ocr_empty_text_interpretation_guard_report.json", empty_guard)
    _write_json(out / "realvideo_ocr_readonly_rejected_roi_carryover_report.json", rejected_carryover)
    _write_json(out / "realvideo_ocr_readonly_provider_summary_report.json", provider_summary)
    _write_json(out / "realvideo_ocr_readonly_source_chain_report.json", source_chain)
    _write_json(out / "realvideo_ocr_readonly_metrics_candidate_report.json", metrics)
    _write_json(out / "realvideo_ocr_readonly_benchmark_link_report.json", benchmark_link)
    _write_json(out / "realvideo_ocr_readonly_system_health_link_report.json", health_link)
    _write_json(out / "realvideo_ocr_readonly_no_write_boundary_report.json", boundary)
    _write_json(out / "realvideo_ocr_readonly_simulation_context_report.json", sim_report)
    _write_json(out / "realvideo_ocr_readonly_non_claims_report.json", non_claims)
    _write_json(out / "realvideo_ocr_readonly_open_followups.json", followups)
    _write_json(out / "realvideo_ocr_readonly_audit_report.json", audit)

    (out / "realvideo_ocr_readonly_notes.md").write_text(
        "\n".join(
            [
                "# RealVideo OCR Evidence ReadOnly Consumer",
                "",
                f"- Phase: {summary.get('phase')}",
                f"- consumer_scope: {summary.get('consumer_scope')}",
                f"- evidence_count_observed: {summary.get('evidence_count_observed')}",
                f"- empty_text_count: {summary.get('empty_text_count')}",
                f"- phase_verdict_hint: {summary.get('phase_verdict_hint')}",
                "",
                "Read-only index only; no OCR re-run, no fusion, no writes.",
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
