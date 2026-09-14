#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase-Multiframe-Crop-Execution-DryRun-v1-001 runner."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

WRITES = [
    ("multiframe_crop_execution_dryrun_v1_summary.json", "summary"),
    ("multiframe_crop_tracklet_intake_matrix_v1.json", "intake_matrix"),
    ("multiframe_crop_execution_rule_matrix_v1.json", "rule_matrix"),
    ("multiframe_crop_artifact_schema_v1.json", "crop_schema"),
    ("multiframe_crop_artifact_collection_v1.json", "crop_collection"),
    ("multiframe_crop_execution_trace_v1.json", "execution_trace"),
    ("multiframe_crop_bbox_validation_report_v1.json", "bbox_validation"),
    ("multiframe_crop_quality_placeholder_report_v1.json", "quality_placeholder"),
    ("multiframe_crop_diversity_report_v1.json", "diversity"),
    ("multiframe_projection_risk_carryover_report_v1.json", "projection_risk"),
    ("multiframe_ocrrequest_readiness_report_v1.json", "ocr_readiness"),
    ("multiframe_crop_same_frame_blocker_carryover_report_v1.json", "same_frame_carryover"),
    ("multiframe_future_ocr_ep_sv_plan_v1.json", "future_plan"),
    ("multiframe_crop_source_chain_report_v1.json", "source_chain_report"),
    ("multiframe_crop_boundary_report_v1.json", "boundary"),
    ("multiframe_crop_metrics_candidate_report_v1.json", "metrics"),
    ("multiframe_crop_benchmark_link_report_v1.json", "benchmark_link"),
    ("multiframe_crop_system_health_link_report_v1.json", "health_link"),
    ("multiframe_crop_no_write_boundary_report_v1.json", "no_write"),
    ("multiframe_crop_simulation_context_report_v1.json", "sim_report"),
    ("multiframe_crop_non_claims_report_v1.json", "non_claims"),
    ("multiframe_crop_open_followups_v1.json", "followups"),
    ("multiframe_crop_audit_report_v1.json", "audit"),
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
    ap.add_argument("--text-region-tracklet-root", required=True)
    ap.add_argument("--better-frame-root", required=True)
    ap.add_argument("--multiframe-merge-proposal-root", required=True)
    ap.add_argument("--source-validation-v2-root", required=True)
    ap.add_argument("--semantic-v3-root", required=True)
    ap.add_argument("--evidence-pack-v3-root", required=True)
    ap.add_argument("--ocrrequest-gated-submission-v2-root", required=True)
    ap.add_argument("--roi-ocrrequest-reference-v2-root", required=True)
    ap.add_argument("--roi-crop-v2-root", required=True)
    ap.add_argument("--linebox-sq-root", required=True)
    ap.add_argument("--mixed-batch-v2-root", required=True)
    ap.add_argument("--benchmark-smoke-root", required=True)
    ap.add_argument("--system-health-root", required=True)
    ap.add_argument("--simulation-root", required=True)
    args = ap.parse_args()

    out = _require_abs(args.output_root, "--output-root")
    out.mkdir(parents=True, exist_ok=True)

    roots = {
        "text_region_tracklet_root": _require_abs(args.text_region_tracklet_root, "tr"),
        "better_frame_root": _require_abs(args.better_frame_root, "bf"),
        "multiframe_merge_proposal_root": _require_abs(args.multiframe_merge_proposal_root, "mf"),
        "source_validation_v2_root": _require_abs(args.source_validation_v2_root, "sv2"),
        "semantic_v3_root": _require_abs(args.semantic_v3_root, "sem_v3"),
        "evidence_pack_v3_root": _require_abs(args.evidence_pack_v3_root, "ep_v3"),
        "ocrrequest_gated_submission_v2_root": _require_abs(
            args.ocrrequest_gated_submission_v2_root, "ocr_v2"
        ),
        "roi_ocrrequest_reference_v2_root": _require_abs(
            args.roi_ocrrequest_reference_v2_root, "ref_v2"
        ),
        "roi_crop_v2_root": _require_abs(args.roi_crop_v2_root, "crop_v2"),
        "linebox_sq_root": _require_abs(args.linebox_sq_root, "linebox"),
        "mixed_batch_v2_root": _require_abs(args.mixed_batch_v2_root, "mixed"),
        "benchmark_smoke_root": _require_abs(args.benchmark_smoke_root, "bench"),
        "system_health_root": _require_abs(args.system_health_root, "health"),
        "simulation_root": _require_abs(args.simulation_root, "sim"),
    }

    from capabilities.midplatform.multiframe_crop_execution_dryrun_v1 import (
        run_multiframe_crop_execution_dryrun_v1,
    )

    result = run_multiframe_crop_execution_dryrun_v1(
        output_root=str(out),
        text_region_tracklet_root=str(roots["text_region_tracklet_root"]),
        better_frame_root=str(roots["better_frame_root"]),
        multiframe_merge_proposal_root=str(roots["multiframe_merge_proposal_root"]),
        source_validation_v2_root=str(roots["source_validation_v2_root"]),
        semantic_v3_root=str(roots["semantic_v3_root"]),
        evidence_pack_v3_root=str(roots["evidence_pack_v3_root"]),
        ocrrequest_gated_submission_v2_root=str(roots["ocrrequest_gated_submission_v2_root"]),
        roi_ocrrequest_reference_v2_root=str(roots["roi_ocrrequest_reference_v2_root"]),
        roi_crop_v2_root=str(roots["roi_crop_v2_root"]),
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

    coll = result["crop_collection"]
    gen = summary.get("multiframe_crop_generated_count") or summary.get("multiframe_crop_artifact_count")
    (out / "multiframe_crop_notes.md").write_text(
        "\n".join(
            [
                "# Multiframe Crop Execution DryRun v1",
                "",
                f"- Phase: {summary.get('phase')}",
                f"- projected regions: {summary.get('projected_region_count_observed')}",
                f"- crops generated: {result['metrics'].get('crop_generated_count')}",
                f"- same-frame blocker still active",
                "",
                "Projection crops only; no OCR / OCRRequest / EP / Semantic.",
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
                "multiframe_crop_artifact_count": summary.get("multiframe_crop_artifact_count"),
                "crop_generated_count": result["metrics"].get("crop_generated_count"),
            },
            ensure_ascii=False,
        )
    )
    return 0 if summary.get("phase_verdict_hint") in ("GO", "CONDITIONAL_GO") else 1


if __name__ == "__main__":
    raise SystemExit(main())
