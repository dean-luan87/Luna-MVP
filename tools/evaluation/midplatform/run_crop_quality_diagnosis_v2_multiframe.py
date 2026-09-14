#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase-Crop-Quality-Diagnosis-v2-Multiframe-001 runner."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

WRITES = [
    ("crop_quality_diagnosis_v2_multiframe_summary.json", "summary"),
    ("crop_quality_diagnosis_v2_intake_matrix.json", "intake_matrix"),
    ("crop_quality_diagnosis_v2_rule_matrix.json", "rule_matrix"),
    ("crop_quality_geometry_diagnosis_report_v2.json", "geometry"),
    ("crop_quality_bbox_type_comparison_report_v2.json", "bbox_comparison"),
    ("crop_quality_frame_offset_diagnosis_report_v2.json", "frame_offset"),
    ("crop_quality_brightness_blur_report_v2.json", "brightness_blur"),
    ("crop_quality_projection_drift_diagnosis_report_v2.json", "projection_drift"),
    ("crop_quality_empty_result_pattern_report_v2.json", "empty_pattern"),
    ("crop_quality_visual_existence_report_v2.json", "visual_existence"),
    ("crop_quality_root_cause_hypothesis_report_v2.json", "root_cause"),
    ("crop_quality_diagnosis_decision_matrix_v2.json", "decision_matrix"),
    ("crop_quality_future_fix_plan_v2.json", "future_fix_plan"),
    ("crop_quality_semantic_sv_blocker_carryover_report_v2.json", "semantic_sv_blocker"),
    ("crop_quality_source_chain_report_v2.json", "source_chain"),
    ("crop_quality_boundary_report_v2.json", "boundary"),
    ("crop_quality_metrics_candidate_report_v2.json", "metrics"),
    ("crop_quality_benchmark_link_report_v2.json", "benchmark_link"),
    ("crop_quality_system_health_link_report_v2.json", "health_link"),
    ("crop_quality_no_write_boundary_report_v2.json", "no_write"),
    ("crop_quality_simulation_context_report_v2.json", "sim_report"),
    ("crop_quality_non_claims_report_v2.json", "non_claims"),
    ("crop_quality_open_followups_v2.json", "followups"),
    ("crop_quality_audit_report_v2.json", "audit"),
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

    from capabilities.midplatform.crop_quality_diagnosis_v2_multiframe import (
        run_crop_quality_diagnosis_v2_multiframe,
    )

    result = run_crop_quality_diagnosis_v2_multiframe(
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

    (out / "crop_quality_notes.md").write_text(
        "\n".join(
            [
                "# Crop Quality Diagnosis v2 Multiframe",
                "",
                f"- Phase: {summary.get('phase')}",
                f"- EP v4 observed: {summary.get('evidence_pack_v4_count_observed')}",
                f"- empty OCR: {summary.get('empty_ocr_result_count_observed')}",
                f"- small_crop_risk_count: {summary.get('small_crop_risk_count')}",
                f"- root_cause_confirmed: {summary.get('root_cause_confirmed')}",
                "",
                "Diagnosis only; no OCR, no new crop, hypotheses not confirmed.",
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
                "evidence_pack_v4_count_observed": summary.get("evidence_pack_v4_count_observed"),
                "small_crop_risk_count": summary.get("small_crop_risk_count"),
            },
            ensure_ascii=False,
        )
    )
    return 0 if summary.get("phase_verdict_hint") in ("GO", "CONDITIONAL_GO") else 1


if __name__ == "__main__":
    raise SystemExit(main())
