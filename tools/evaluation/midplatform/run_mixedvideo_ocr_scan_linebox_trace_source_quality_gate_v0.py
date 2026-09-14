#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase-MixedVideo-OCR-Scan-LineBox-Trace-SourceQualityGate-001 runner."""

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
    ap.add_argument("--mixed-batch-root", required=True)
    ap.add_argument("--readability-governance-root", required=True)
    ap.add_argument("--evidence-pack-contract-root", required=True)
    ap.add_argument("--benchmark-smoke-root", required=True)
    ap.add_argument("--system-health-root", required=True)
    ap.add_argument("--simulation-root", required=True)
    ap.add_argument("--p0-video-path", required=True)
    ap.add_argument("--no-rescan", action="store_true", help="Skip P0 RapidOCR rescan")
    args = ap.parse_args()

    out = _require_abs(args.output_root, "--output-root")
    roots = {
        "mixed_batch_root": _require_abs(args.mixed_batch_root, "mixed-batch"),
        "readability_governance_root": _require_abs(args.readability_governance_root, "readability"),
        "evidence_pack_contract_root": _require_abs(args.evidence_pack_contract_root, "contract"),
        "benchmark_smoke_root": _require_abs(args.benchmark_smoke_root, "benchmark"),
        "system_health_root": _require_abs(args.system_health_root, "health"),
        "simulation_root": _require_abs(args.simulation_root, "sim"),
        "p0_video_path": _require_abs(args.p0_video_path, "p0-video"),
    }

    from capabilities.midplatform.mixedvideo_ocr_scan_linebox_trace_source_quality_gate_v0 import (
        run_mixedvideo_ocr_scan_linebox_trace_source_quality_gate_v0,
    )

    (
        summary,
        linebox_trace_report,
        plan_update_doc,
        gate_policy,
        eval_matrix,
        consistency_report,
        full_frame_risk,
        roi_plan,
        scan_obs_policy,
        ep_update,
        sem_guard,
        metrics,
        benchmark_link,
        health_link,
        boundary,
        sim_report,
        non_claims,
        followups,
        audit,
        errs,
    ) = run_mixedvideo_ocr_scan_linebox_trace_source_quality_gate_v0(
        output_root=str(out),
        mixed_batch_root=str(roots["mixed_batch_root"]),
        readability_governance_root=str(roots["readability_governance_root"]),
        evidence_pack_contract_root=str(roots["evidence_pack_contract_root"]),
        benchmark_smoke_root=str(roots["benchmark_smoke_root"]),
        system_health_root=str(roots["system_health_root"]),
        simulation_root=str(roots["simulation_root"]),
        p0_video_path=str(roots["p0_video_path"]),
        rescan_p0=not args.no_rescan,
    )

    summary["output_root"] = str(out)
    summary["input_roots"] = {k: str(v) for k, v in roots.items()}

    writes = [
        ("mixedvideo_ocr_scan_linebox_trace_quality_gate_summary.json", summary),
        ("mixedvideo_ocr_scan_linebox_trace_report.json", linebox_trace_report),
        ("mixedvideo_selected_frame_linebox_plan_update.json", plan_update_doc),
        ("mixedvideo_ocr_source_quality_gate_policy.json", gate_policy),
        ("mixedvideo_ocr_source_quality_evaluation_matrix.json", eval_matrix),
        ("mixedvideo_scan_vs_pack_consistency_report.json", consistency_report),
        ("mixedvideo_full_frame_ocr_risk_report.json", full_frame_risk),
        ("mixedvideo_ocr_roi_crop_requirement_plan.json", roi_plan),
        ("mixedvideo_scan_observation_vs_evidence_policy.json", scan_obs_policy),
        ("mixedvideo_ocr_evidence_pack_update_recommendation.json", ep_update),
        ("mixedvideo_semantic_candidate_guard_update_plan.json", sem_guard),
        ("mixedvideo_ocr_scan_linebox_quality_metrics_candidate_report.json", metrics),
        ("mixedvideo_ocr_scan_linebox_quality_benchmark_link_report.json", benchmark_link),
        ("mixedvideo_ocr_scan_linebox_quality_system_health_link_report.json", health_link),
        ("mixedvideo_ocr_scan_linebox_quality_no_write_boundary_report.json", boundary),
        ("mixedvideo_ocr_scan_linebox_quality_simulation_context_report.json", sim_report),
        ("mixedvideo_ocr_scan_linebox_quality_non_claims_report.json", non_claims),
        ("mixedvideo_ocr_scan_linebox_quality_open_followups.json", followups),
        ("mixedvideo_ocr_scan_linebox_quality_audit_report.json", audit),
    ]
    for fname, obj in writes:
        _write_json(out / fname, obj)

    notes = [
        "# MixedVideo OCR Scan LineBox Trace + Source Quality Gate",
        "",
        f"- phase_verdict_hint: {summary.get('phase_verdict_hint')}",
        f"- ocr_scan_invoked: {summary.get('ocr_scan_invoked')}",
        f"- linebox_available_count: {summary.get('linebox_available_count')}",
        "",
        "## Architecture principle",
        "",
        "OCR failure may stem from input source quality, not only provider.",
        "Govern input before changing OCR model. Low-quality inputs must not",
        "enter evidence with the same weight as high-quality inputs.",
        "",
    ]
    if not summary.get("ocr_scan_invoked"):
        notes.append("P0 rescan was skipped or failed; linebox may be incomplete.\n")
    (out / "mixedvideo_ocr_scan_linebox_quality_notes.md").write_text("\n".join(notes), encoding="utf-8")

    print(
        json.dumps(
            {"output_root": str(out), "phase_verdict_hint": summary.get("phase_verdict_hint"), "errors": errs},
            ensure_ascii=False,
        )
    )
    return 0 if summary.get("phase_verdict_hint") in ("GO", "CONDITIONAL_GO") else 1


if __name__ == "__main__":
    raise SystemExit(main())
