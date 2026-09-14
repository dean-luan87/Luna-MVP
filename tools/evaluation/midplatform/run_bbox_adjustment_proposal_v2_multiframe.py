#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase-BBox-Adjustment-Proposal-v2-Multiframe-001 runner."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

WRITES = [
    ("bbox_adjustment_proposal_v2_multiframe_summary.json", "summary"),
    ("bbox_adjustment_candidate_intake_matrix_v2.json", "intake_matrix"),
    ("bbox_adjustment_rule_matrix_v2.json", "rule_matrix"),
    ("bbox_adjustment_proposal_schema_v2.json", "proposal_schema"),
    ("bbox_adjustment_proposal_collection_v2.json", "proposal_collection"),
    ("bbox_adjustment_bounds_check_report_v2.json", "bounds_check"),
    ("bbox_adjustment_dedup_grouping_report_v2.json", "dedup"),
    ("bbox_adjustment_delta_report_v2.json", "delta"),
    ("bbox_adjustment_risk_report_v2.json", "risk"),
    ("bbox_adjustment_future_recrop_readiness_report_v2.json", "recrop_readiness"),
    ("bbox_adjustment_future_reocr_plan_v2.json", "future_reocr"),
    ("bbox_adjustment_source_chain_report_v2.json", "source_chain"),
    ("bbox_adjustment_semantic_sv_blocker_carryover_report_v2.json", "semantic_sv_blocker"),
    ("bbox_adjustment_boundary_report_v2.json", "boundary"),
    ("bbox_adjustment_metrics_candidate_report_v2.json", "metrics"),
    ("bbox_adjustment_benchmark_link_report_v2.json", "benchmark_link"),
    ("bbox_adjustment_system_health_link_report_v2.json", "health_link"),
    ("bbox_adjustment_no_write_boundary_report_v2.json", "no_write"),
    ("bbox_adjustment_simulation_context_report_v2.json", "sim_report"),
    ("bbox_adjustment_non_claims_report_v2.json", "non_claims"),
    ("bbox_adjustment_open_followups_v2.json", "followups"),
    ("bbox_adjustment_audit_report_v2.json", "audit"),
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
        "text_detector_root": _require_abs(args.text_detector_root, "td"),
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

    from capabilities.midplatform.bbox_adjustment_proposal_v2_multiframe import (
        run_bbox_adjustment_proposal_v2_multiframe,
    )

    result = run_bbox_adjustment_proposal_v2_multiframe(
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

    (out / "bbox_adjustment_notes.md").write_text(
        "\n".join(
            [
                "# BBox Adjustment Proposal v2 Multiframe",
                "",
                f"- Phase: {summary.get('phase')}",
                f"- candidates: {summary.get('bbox_adjustment_candidate_count_observed')}",
                f"- proposals: {summary.get('bbox_adjustment_proposal_count')}",
                f"- deduplicated: {summary.get('deduplicated_proposal_count')}",
                f"- ready for future re-crop: {summary.get('proposal_ready_for_future_recrop_count')}",
                "",
                "Proposal only; no crop, no OCR, no facts.",
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
                "bbox_adjustment_proposal_count": summary.get("bbox_adjustment_proposal_count"),
                "deduplicated_proposal_count": summary.get("deduplicated_proposal_count"),
            },
            ensure_ascii=False,
        )
    )
    return 0 if summary.get("phase_verdict_hint") in ("GO", "CONDITIONAL_GO") else 1


if __name__ == "__main__":
    raise SystemExit(main())
