#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase-ROI-Crop-Execution-DryRun-v2-BBoxExpansion-001 runner."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

WRITES = [
    ("roi_crop_v2_bbox_expansion_summary.json", "summary"),
    ("roi_crop_v2_expansion_candidate_intake_matrix.json", "intake_matrix"),
    ("roi_crop_v2_bbox_expansion_execution_policy.json", "execution_policy"),
    ("roi_crop_v2_source_frame_resolution_report.json", "source_frame_resolution"),
    ("roi_crop_v2_expanded_bbox_validation_report.json", "bbox_validation"),
    ("roi_crop_v2_expanded_artifact_schema.json", "artifact_schema"),
    ("roi_crop_v2_expanded_artifact_collection.json", "artifact_collection"),
    ("roi_crop_v2_execution_trace.json", "execution_trace"),
    ("roi_crop_v2_size_context_comparison_report.json", "size_comparison"),
    ("roi_crop_v2_expanded_crop_diversity_report.json", "diversity_report"),
    ("roi_crop_v2_deferred_report.json", "deferred_report"),
    ("roi_crop_v2_to_ocrrequest_reference_plan.json", "ocr_ref_plan"),
    ("roi_crop_v2_boundary_report.json", "boundary"),
    ("roi_crop_v2_source_chain_report.json", "source_chain_report"),
    ("roi_crop_v2_metrics_candidate_report.json", "metrics"),
    ("roi_crop_v2_benchmark_link_report.json", "benchmark_link"),
    ("roi_crop_v2_system_health_link_report.json", "health_link"),
    ("roi_crop_v2_no_write_boundary_report.json", "no_write"),
    ("roi_crop_v2_simulation_context_report.json", "sim_report"),
    ("roi_crop_v2_non_claims_report.json", "non_claims"),
    ("roi_crop_v2_open_followups.json", "followups"),
    ("roi_crop_v2_audit_report.json", "audit"),
]


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
    ap.add_argument("--roi-bbox-expansion-root", required=True)
    ap.add_argument("--roi-crop-diversity-root", required=True)
    ap.add_argument("--roi-ocr-quality-diagnosis-root", required=True)
    ap.add_argument("--semantic-v2-root", required=True)
    ap.add_argument("--evidence-pack-v2-root", required=True)
    ap.add_argument("--roi-ocr-gated-submission-root", required=True)
    ap.add_argument("--roi-ocrrequest-reference-root", required=True)
    ap.add_argument("--roi-crop-rerun-root", required=True)
    ap.add_argument("--better-frame-root", required=True)
    ap.add_argument("--roi-retry-root", required=True)
    ap.add_argument("--linebox-sq-root", required=True)
    ap.add_argument("--mixed-batch-v2-root", required=True)
    ap.add_argument("--benchmark-smoke-root", required=True)
    ap.add_argument("--system-health-root", required=True)
    ap.add_argument("--simulation-root", required=True)
    args = ap.parse_args()

    out = _require_abs(args.output_root, "--output-root")
    roots = {
        "roi_bbox_expansion_root": _require_abs(args.roi_bbox_expansion_root, "exp"),
        "roi_crop_diversity_root": _require_abs(args.roi_crop_diversity_root, "motion"),
        "roi_ocr_quality_diagnosis_root": _require_abs(args.roi_ocr_quality_diagnosis_root, "diag"),
        "semantic_v2_root": _require_abs(args.semantic_v2_root, "sem"),
        "evidence_pack_v2_root": _require_abs(args.evidence_pack_v2_root, "ep"),
        "roi_ocr_gated_submission_root": _require_abs(args.roi_ocr_gated_submission_root, "ocr"),
        "roi_ocrrequest_reference_root": _require_abs(args.roi_ocrrequest_reference_root, "ref"),
        "roi_crop_rerun_root": _require_abs(args.roi_crop_rerun_root, "crop"),
        "better_frame_root": _require_abs(args.better_frame_root, "bf"),
        "roi_retry_root": _require_abs(args.roi_retry_root, "retry"),
        "linebox_sq_root": _require_abs(args.linebox_sq_root, "linebox"),
        "mixed_batch_v2_root": _require_abs(args.mixed_batch_v2_root, "v2"),
        "benchmark_smoke_root": _require_abs(args.benchmark_smoke_root, "bench"),
        "system_health_root": _require_abs(args.system_health_root, "health"),
        "simulation_root": _require_abs(args.simulation_root, "sim"),
    }

    from capabilities.midplatform.roi_crop_execution_dryrun_v2_bbox_expansion import (
        run_roi_crop_execution_dryrun_v2_bbox_expansion,
    )

    result = run_roi_crop_execution_dryrun_v2_bbox_expansion(
        output_root=str(out),
        roi_bbox_expansion_root=str(roots["roi_bbox_expansion_root"]),
        roi_crop_diversity_root=str(roots["roi_crop_diversity_root"]),
        roi_ocr_quality_diagnosis_root=str(roots["roi_ocr_quality_diagnosis_root"]),
        semantic_v2_root=str(roots["semantic_v2_root"]),
        evidence_pack_v2_root=str(roots["evidence_pack_v2_root"]),
        roi_ocr_gated_submission_root=str(roots["roi_ocr_gated_submission_root"]),
        roi_ocrrequest_reference_root=str(roots["roi_ocrrequest_reference_root"]),
        roi_crop_rerun_root=str(roots["roi_crop_rerun_root"]),
        better_frame_root=str(roots["better_frame_root"]),
        roi_retry_root=str(roots["roi_retry_root"]),
        linebox_sq_root=str(roots["linebox_sq_root"]),
        mixed_batch_v2_root=str(roots["mixed_batch_v2_root"]),
        benchmark_smoke_root=str(roots["benchmark_smoke_root"]),
        system_health_root=str(roots["system_health_root"]),
        simulation_root=str(roots["simulation_root"]),
    )

    summary = result["summary"]
    summary["output_root"] = str(out)
    summary["input_roots"] = {k: str(v) for k, v in roots.items()}

    for fname, key in WRITES:
        _write_json(out / fname, result[key])

    (out / "roi_crop_v2_notes.md").write_text(
        "\n".join(
            [
                "# ROI Crop v2 BBox Expansion DryRun",
                "",
                f"- Phase: {summary.get('phase')}",
                f"- expanded_crop_generated_count: {summary.get('expanded_crop_generated_count')}",
                f"- phase_verdict_hint: {summary.get('phase_verdict_hint')}",
                "",
                "Expanded crop execution only; no OCR, no OCRRequest, no fact write.",
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
                "expanded_crop_generated_count": summary.get("expanded_crop_generated_count"),
            },
            ensure_ascii=False,
        )
    )
    return 0 if summary.get("phase_verdict_hint") in ("GO", "CONDITIONAL_GO") else 1


if __name__ == "__main__":
    raise SystemExit(main())
