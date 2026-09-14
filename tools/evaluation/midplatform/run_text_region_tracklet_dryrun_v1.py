#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase-Text-Region-Tracklet-DryRun-v1-001 runner."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

WRITES = [
    ("text_region_tracklet_dryrun_v1_summary.json", "summary"),
    ("tracklet_better_frame_artifact_intake_matrix.json", "artifact_intake"),
    ("text_region_tracklet_rule_matrix_v1.json", "rule_matrix"),
    ("text_region_tracklet_candidate_schema_v1.json", "tracklet_schema"),
    ("text_region_tracklet_candidate_collection_v1.json", "tracklet_collection"),
    ("text_region_projected_region_matrix_v1.json", "projected_matrix"),
    ("text_region_tracklet_frame_coverage_report_v1.json", "frame_coverage"),
    ("text_region_bbox_continuity_report_v1.json", "bbox_continuity"),
    ("text_region_drift_risk_report_v1.json", "drift_risk"),
    ("text_region_quality_context_carryover_report_v1.json", "quality_carryover"),
    ("text_region_tracklet_crop_readiness_report_v1.json", "crop_readiness"),
    ("text_region_tracklet_same_frame_blocker_carryover_report_v1.json", "same_frame_carryover"),
    ("text_region_future_multiframe_crop_plan_v1.json", "future_crop_plan"),
    ("text_region_tracklet_source_chain_report_v1.json", "source_chain_report"),
    ("text_region_tracklet_boundary_report_v1.json", "boundary"),
    ("text_region_tracklet_metrics_candidate_report_v1.json", "metrics"),
    ("text_region_tracklet_benchmark_link_report_v1.json", "benchmark_link"),
    ("text_region_tracklet_system_health_link_report_v1.json", "health_link"),
    ("text_region_tracklet_no_write_boundary_report_v1.json", "no_write"),
    ("text_region_tracklet_simulation_context_report_v1.json", "sim_report"),
    ("text_region_tracklet_non_claims_report_v1.json", "non_claims"),
    ("text_region_tracklet_open_followups_v1.json", "followups"),
    ("text_region_tracklet_audit_report_v1.json", "audit"),
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

    from capabilities.midplatform.text_region_tracklet_dryrun_v1 import (
        run_text_region_tracklet_dryrun_v1,
    )

    result = run_text_region_tracklet_dryrun_v1(
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

    (out / "text_region_tracklet_notes.md").write_text(
        "\n".join(
            [
                "# Text Region Tracklet DryRun v1",
                "",
                f"- Phase: {summary.get('phase')}",
                f"- tracklet candidates: {summary.get('tracklet_candidate_count')}",
                f"- frame artifacts observed: {summary.get('frame_artifact_count_observed')}",
                f"- projection only (not detection); same-frame blocker still active",
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
                "tracklet_candidate_count": summary.get("tracklet_candidate_count"),
            },
            ensure_ascii=False,
        )
    )
    return 0 if summary.get("phase_verdict_hint") in ("GO", "CONDITIONAL_GO") else 1


if __name__ == "__main__":
    raise SystemExit(main())
