#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase-Better-Frame-Extraction-DryRun-v1-001 runner."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

WRITES = [
    ("better_frame_extraction_dryrun_v1_summary.json", "summary"),
    ("better_frame_multiframe_window_intake_matrix.json", "window_intake"),
    ("better_frame_extraction_rule_matrix.json", "rule_matrix"),
    ("better_frame_candidate_frame_reference_schema.json", "frame_ref_schema"),
    ("better_frame_candidate_frame_reference_collection.json", "frame_ref_collection"),
    ("better_frame_materialization_plan.json", "materialization_plan"),
    ("better_frame_artifact_collection.json", "artifact_collection"),
    ("better_frame_extraction_trace.json", "extraction_trace"),
    ("better_frame_quality_placeholder_report.json", "quality_placeholder"),
    ("better_frame_region_coverage_hint_report.json", "region_coverage"),
    ("better_frame_candidate_diversity_report.json", "diversity"),
    ("better_frame_same_frame_blocker_carryover_report.json", "same_frame_carryover"),
    ("better_frame_future_tracklet_crop_plan.json", "future_tracklet_crop"),
    ("better_frame_source_chain_report.json", "source_chain_report"),
    ("better_frame_boundary_report.json", "boundary"),
    ("better_frame_metrics_candidate_report.json", "metrics"),
    ("better_frame_benchmark_link_report.json", "benchmark_link"),
    ("better_frame_system_health_link_report.json", "health_link"),
    ("better_frame_no_write_boundary_report.json", "no_write"),
    ("better_frame_simulation_context_report.json", "sim_report"),
    ("better_frame_non_claims_report.json", "non_claims"),
    ("better_frame_open_followups.json", "followups"),
    ("better_frame_audit_report.json", "audit"),
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
    ap.add_argument("--p0-video-path", required=True)
    args = ap.parse_args()

    out = _require_abs(args.output_root, "--output-root")
    frames_dir = out / "frames"
    out.mkdir(parents=True, exist_ok=True)
    frames_dir.mkdir(parents=True, exist_ok=True)

    roots = {
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
        "p0_video_path": _require_abs(args.p0_video_path, "p0_video"),
    }

    from capabilities.midplatform.better_frame_extraction_dryrun_v1 import (
        run_better_frame_extraction_dryrun_v1,
    )

    result = run_better_frame_extraction_dryrun_v1(
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
        p0_video_path=str(roots["p0_video_path"]),
        frames_output_dir=str(frames_dir),
    )

    summary = result["summary"]
    summary["output_root"] = str(out)
    summary["frames_output_dir"] = str(frames_dir)
    summary["input_roots"] = {k: str(v) for k, v in roots.items()}

    for fname, key in WRITES:
        _write_json(out / fname, result[key])

    (out / "better_frame_notes.md").write_text(
        "\n".join(
            [
                "# Better Frame Extraction DryRun v1",
                "",
                f"- Phase: {summary.get('phase')}",
                f"- candidate frame refs: {summary.get('candidate_frame_reference_count')}",
                f"- artifacts generated: {summary.get('frame_artifact_generated_count')}",
                f"- same-frame blocker still active",
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
                "candidate_frame_reference_count": summary.get("candidate_frame_reference_count"),
                "frame_artifact_generated_count": summary.get("frame_artifact_generated_count"),
            },
            ensure_ascii=False,
        )
    )
    return 0 if summary.get("phase_verdict_hint") in ("GO", "CONDITIONAL_GO") else 1


if __name__ == "__main__":
    raise SystemExit(main())
