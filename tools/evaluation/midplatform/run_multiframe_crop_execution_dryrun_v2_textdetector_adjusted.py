#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase-Multiframe-Crop-Execution-DryRun-v2-TextDetectorAdjusted-001 runner."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

WRITES = [
    ("multiframe_crop_v2_textdetector_adjusted_summary.json", "summary"),
    ("multiframe_crop_v2_adjusted_intake_matrix.json", "intake_matrix"),
    ("multiframe_crop_v2_execution_rule_matrix.json", "rule_matrix"),
    ("multiframe_crop_v2_adjusted_artifact_schema.json", "artifact_schema"),
    ("multiframe_crop_v2_adjusted_artifact_collection.json", "artifact_collection"),
    ("multiframe_crop_v2_adjusted_execution_trace.json", "execution_trace"),
    ("multiframe_crop_v2_geometry_delta_report.json", "geometry_delta"),
    ("multiframe_crop_v2_adjusted_quality_placeholder_report.json", "quality_placeholder"),
    ("multiframe_crop_v2_adjusted_diversity_report.json", "diversity"),
    ("multiframe_crop_v2_ocrrequest_readiness_report.json", "ocr_readiness"),
    ("multiframe_crop_v2_user_guidance_recovery_followup_report.json", "user_guidance"),
    ("multiframe_crop_v2_same_frame_blocker_carryover_report.json", "same_frame_carryover"),
    ("multiframe_crop_v2_future_ocr_ep_sv_plan.json", "future_plan"),
    ("multiframe_crop_v2_source_chain_report.json", "source_chain"),
    ("multiframe_crop_v2_boundary_report.json", "boundary"),
    ("multiframe_crop_v2_metrics_candidate_report.json", "metrics"),
    ("multiframe_crop_v2_benchmark_link_report.json", "benchmark_link"),
    ("multiframe_crop_v2_system_health_link_report.json", "health_link"),
    ("multiframe_crop_v2_no_write_boundary_report.json", "no_write"),
    ("multiframe_crop_v2_simulation_context_report.json", "sim_report"),
    ("multiframe_crop_v2_non_claims_report.json", "non_claims"),
    ("multiframe_crop_v2_open_followups.json", "followups"),
    ("multiframe_crop_v2_audit_report.json", "audit"),
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
    ap.add_argument("--bbox-adjustment-root", required=True)
    ap.add_argument("--text-detector-root", required=True)
    ap.add_argument("--crop-quality-root", required=True)
    ap.add_argument("--evidence-pack-v4-root", required=True)
    ap.add_argument("--multiframe-ocr-root", required=True)
    ap.add_argument("--multiframe-crop-root", required=True)
    ap.add_argument("--text-region-tracklet-root", required=True)
    ap.add_argument("--better-frame-root", required=True)
    ap.add_argument("--multiframe-merge-proposal-root", required=True)
    ap.add_argument("--source-validation-v2-root", required=True)
    ap.add_argument("--semantic-v3-root", required=True)
    ap.add_argument("--evidence-pack-v3-root", required=True)
    ap.add_argument("--linebox-sq-root", required=True)
    ap.add_argument("--mixed-batch-v2-root", required=True)
    ap.add_argument("--benchmark-smoke-root", required=True)
    ap.add_argument("--system-health-root", required=True)
    ap.add_argument("--simulation-root", required=True)
    args = ap.parse_args()

    out = _require_abs(args.output_root, "--output-root")
    out.mkdir(parents=True, exist_ok=True)

    roots = {
        "bbox_adjustment_root": _require_abs(args.bbox_adjustment_root, "ba"),
        "text_detector_root": _require_abs(args.text_detector_root, "td"),
        "crop_quality_root": _require_abs(args.crop_quality_root, "cq"),
        "evidence_pack_v4_root": _require_abs(args.evidence_pack_v4_root, "ep_v4"),
        "multiframe_ocr_root": _require_abs(args.multiframe_ocr_root, "ocr"),
        "multiframe_crop_root": _require_abs(args.multiframe_crop_root, "crop_v1"),
        "text_region_tracklet_root": _require_abs(args.text_region_tracklet_root, "tr"),
        "better_frame_root": _require_abs(args.better_frame_root, "bf"),
        "multiframe_merge_proposal_root": _require_abs(args.multiframe_merge_proposal_root, "mf"),
        "source_validation_v2_root": _require_abs(args.source_validation_v2_root, "sv2"),
        "semantic_v3_root": _require_abs(args.semantic_v3_root, "sem_v3"),
        "evidence_pack_v3_root": _require_abs(args.evidence_pack_v3_root, "ep_v3"),
        "linebox_sq_root": _require_abs(args.linebox_sq_root, "linebox"),
        "mixed_batch_v2_root": _require_abs(args.mixed_batch_v2_root, "mixed"),
        "benchmark_smoke_root": _require_abs(args.benchmark_smoke_root, "bench"),
        "system_health_root": _require_abs(args.system_health_root, "health"),
        "simulation_root": _require_abs(args.simulation_root, "sim"),
    }

    from capabilities.midplatform.multiframe_crop_execution_dryrun_v2_textdetector_adjusted import (
        run_multiframe_crop_execution_dryrun_v2_textdetector_adjusted,
    )

    result = run_multiframe_crop_execution_dryrun_v2_textdetector_adjusted(
        output_root=str(out),
        bbox_adjustment_root=str(roots["bbox_adjustment_root"]),
        text_detector_root=str(roots["text_detector_root"]),
        crop_quality_root=str(roots["crop_quality_root"]),
        evidence_pack_v4_root=str(roots["evidence_pack_v4_root"]),
        multiframe_ocr_root=str(roots["multiframe_ocr_root"]),
        multiframe_crop_root=str(roots["multiframe_crop_root"]),
        text_region_tracklet_root=str(roots["text_region_tracklet_root"]),
        better_frame_root=str(roots["better_frame_root"]),
        multiframe_merge_proposal_root=str(roots["multiframe_merge_proposal_root"]),
        source_validation_v2_root=str(roots["source_validation_v2_root"]),
        semantic_v3_root=str(roots["semantic_v3_root"]),
        evidence_pack_v3_root=str(roots["evidence_pack_v3_root"]),
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

    (out / "multiframe_crop_v2_notes.md").write_text(
        "\n".join(
            [
                "# Multiframe Crop v2 TextDetectorAdjusted",
                "",
                f"- Phase: {summary.get('phase')}",
                f"- proposals: {summary.get('bbox_adjustment_proposal_count_observed')}",
                f"- adjusted crops generated: {summary.get('adjusted_crop_generated_count', summary.get('adjusted_crop_artifact_count'))}",
                f"- same_bbox_risk_count: {summary.get('adjusted_bbox_same_as_original_count')}",
                f"- user_guidance_recovery_needed_later: {summary.get('user_guidance_recovery_needed_later')}",
                "",
                "Re-crop only; no OCR. If v2 re-OCR still empty → User Guidance / STC Sampling.",
                "",
            ]
        ),
        encoding="utf-8",
    )

    gen = result["metrics"].get("adjusted_crop_generated_count", 0)
    print(
        json.dumps(
            {
                "output_root": str(out),
                "phase_verdict_hint": summary.get("phase_verdict_hint"),
                "adjusted_crop_generated_count": gen,
                "same_bbox_risk_count": summary.get("adjusted_bbox_same_as_original_count"),
            },
            ensure_ascii=False,
        )
    )
    return 0 if summary.get("phase_verdict_hint") in ("GO", "CONDITIONAL_GO") else 1


if __name__ == "__main__":
    raise SystemExit(main())
