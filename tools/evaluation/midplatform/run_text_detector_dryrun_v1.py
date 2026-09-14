#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase-Text-Detector-DryRun-v1-001 runner."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

WRITES = [
    ("text_detector_dryrun_v1_summary.json", "summary"),
    ("text_detector_input_intake_matrix_v1.json", "intake_matrix"),
    ("text_detector_rule_matrix_v1.json", "rule_matrix"),
    ("text_detector_supervision_tooling_report_v1.json", "supervision_report"),
    ("text_region_candidate_schema_v1.json", "candidate_schema"),
    ("text_region_candidate_collection_v1.json", "candidate_collection"),
    ("text_detector_slicing_tiling_plan_report_v1.json", "slicing_plan"),
    ("text_detector_result_matrix_v1.json", "result_matrix"),
    ("text_detector_projection_overlap_drift_report_v1.json", "overlap_drift"),
    ("text_detector_bbox_adjustment_candidate_report_v1.json", "bbox_adjustment"),
    ("text_detector_quality_confidence_report_v1.json", "quality_confidence"),
    ("text_detector_empty_ocr_explanation_report_v1.json", "empty_ocr_explanation"),
    ("text_detector_future_bbox_adjustment_reocr_plan_v1.json", "future_plan"),
    ("text_detector_source_chain_report_v1.json", "source_chain"),
    ("text_detector_semantic_sv_blocker_carryover_report_v1.json", "semantic_sv_blocker"),
    ("text_detector_boundary_report_v1.json", "boundary"),
    ("text_detector_metrics_candidate_report_v1.json", "metrics"),
    ("text_detector_benchmark_link_report_v1.json", "benchmark_link"),
    ("text_detector_system_health_link_report_v1.json", "health_link"),
    ("text_detector_no_write_boundary_report_v1.json", "no_write"),
    ("text_detector_simulation_context_report_v1.json", "sim_report"),
    ("text_detector_non_claims_report_v1.json", "non_claims"),
    ("text_detector_open_followups_v1.json", "followups"),
    ("text_detector_audit_report_v1.json", "audit"),
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
        "crop_quality_root": _require_abs(args.crop_quality_root, "cq"),
        "evidence_pack_v4_root": _require_abs(args.evidence_pack_v4_root, "ep_v4"),
        "multiframe_ocr_root": _require_abs(args.multiframe_ocr_root, "ocr"),
        "multiframe_crop_root": _require_abs(args.multiframe_crop_root, "crop"),
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

    from capabilities.midplatform.text_detector_dryrun_v1 import run_text_detector_dryrun_v1

    result = run_text_detector_dryrun_v1(
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

    (out / "text_detector_notes.md").write_text(
        "\n".join(
            [
                "# Text Detector DryRun v1",
                "",
                f"- Phase: {summary.get('phase')}",
                f"- crop intake: {result['intake_matrix'].get('crop_count')}",
                f"- frame intake: {result['intake_matrix'].get('frame_count')}",
                f"- text_region_candidates: {summary.get('text_region_candidate_count')}",
                f"- bbox_adjustment_candidates: {summary.get('bbox_adjustment_candidate_count')}",
                f"- supervision_used: {summary.get('supervision_used')}",
                "",
                "Text-like bbox candidates only; no OCR, no facts.",
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
                "text_region_candidate_count": summary.get("text_like_region_candidate_count"),
                "bbox_adjustment_candidate_count": summary.get("bbox_adjustment_candidate_count"),
            },
            ensure_ascii=False,
        )
    )
    return 0 if summary.get("phase_verdict_hint") in ("GO", "CONDITIONAL_GO") else 1


if __name__ == "__main__":
    raise SystemExit(main())
