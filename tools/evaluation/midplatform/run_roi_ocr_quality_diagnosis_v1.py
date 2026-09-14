#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase-ROI-OCR-Quality-Diagnosis-v1-001 runner."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

WRITES = [
    ("roi_ocr_quality_diagnosis_v1_summary.json", "summary"),
    ("roi_ocr_quality_diagnosis_intake_matrix_v1.json", "intake_matrix"),
    ("roi_ocr_quality_diagnosis_rule_matrix_v1.json", "rule_matrix"),
    ("roi_ocr_repeated_text_analysis_report_v1.json", "repeated_analysis"),
    ("roi_ocr_crop_diversity_analysis_report_v1.json", "crop_diversity"),
    ("roi_ocr_crop_geometry_diagnosis_report_v1.json", "crop_geometry"),
    ("roi_ocr_source_frame_reuse_diagnosis_report_v1.json", "frame_reuse"),
    ("roi_ocr_linebox_source_diagnosis_report_v1.json", "linebox_diag"),
    ("roi_ocr_provider_output_diagnosis_report_v1.json", "provider_diag"),
    ("roi_ocr_root_cause_hypothesis_matrix_v1.json", "hypotheses"),
    ("roi_ocr_quality_diagnosis_decision_matrix_v1.json", "decision_matrix"),
    ("roi_ocr_quality_future_fix_plan_v1.json", "future_fix"),
    ("roi_ocr_quality_diagnosis_boundary_report_v1.json", "boundary"),
    ("roi_ocr_quality_source_chain_report_v1.json", "source_chain_report"),
    ("roi_ocr_quality_metrics_candidate_report_v1.json", "metrics"),
    ("roi_ocr_quality_benchmark_link_report_v1.json", "benchmark_link"),
    ("roi_ocr_quality_system_health_link_report_v1.json", "health_link"),
    ("roi_ocr_quality_no_write_boundary_report_v1.json", "no_write"),
    ("roi_ocr_quality_simulation_context_report_v1.json", "sim_report"),
    ("roi_ocr_quality_non_claims_report_v1.json", "non_claims"),
    ("roi_ocr_quality_open_followups_v1.json", "followups"),
    ("roi_ocr_quality_audit_report_v1.json", "audit"),
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
    ap.add_argument("--semantic-v2-root", required=True)
    ap.add_argument("--evidence-pack-v2-root", required=True)
    ap.add_argument("--roi-ocr-gated-submission-root", required=True)
    ap.add_argument("--roi-ocrrequest-reference-root", required=True)
    ap.add_argument("--roi-crop-rerun-root", required=True)
    ap.add_argument("--better-frame-root", required=True)
    ap.add_argument("--roi-retry-root", required=True)
    ap.add_argument("--source-validation-root", required=True)
    ap.add_argument("--linebox-sq-root", required=True)
    ap.add_argument("--mixed-batch-v2-root", required=True)
    ap.add_argument("--adapter-v1-root", required=True)
    ap.add_argument("--benchmark-smoke-root", required=True)
    ap.add_argument("--system-health-root", required=True)
    ap.add_argument("--simulation-root", required=True)
    args = ap.parse_args()

    out = _require_abs(args.output_root, "--output-root")
    roots = {
        "semantic_v2_root": _require_abs(args.semantic_v2_root, "sem"),
        "evidence_pack_v2_root": _require_abs(args.evidence_pack_v2_root, "ep"),
        "roi_ocr_gated_submission_root": _require_abs(args.roi_ocr_gated_submission_root, "ocr"),
        "roi_ocrrequest_reference_root": _require_abs(args.roi_ocrrequest_reference_root, "ref"),
        "roi_crop_rerun_root": _require_abs(args.roi_crop_rerun_root, "crop"),
        "better_frame_root": _require_abs(args.better_frame_root, "bf"),
        "roi_retry_root": _require_abs(args.roi_retry_root, "retry"),
        "source_validation_root": _require_abs(args.source_validation_root, "sv"),
        "linebox_sq_root": _require_abs(args.linebox_sq_root, "linebox"),
        "mixed_batch_v2_root": _require_abs(args.mixed_batch_v2_root, "v2"),
        "adapter_v1_root": _require_abs(args.adapter_v1_root, "adapter"),
        "benchmark_smoke_root": _require_abs(args.benchmark_smoke_root, "bench"),
        "system_health_root": _require_abs(args.system_health_root, "health"),
        "simulation_root": _require_abs(args.simulation_root, "sim"),
    }

    from capabilities.midplatform.roi_ocr_quality_diagnosis_v1 import run_roi_ocr_quality_diagnosis_v1

    result = run_roi_ocr_quality_diagnosis_v1(
        semantic_v2_root=str(roots["semantic_v2_root"]),
        evidence_pack_v2_root=str(roots["evidence_pack_v2_root"]),
        roi_ocr_gated_submission_root=str(roots["roi_ocr_gated_submission_root"]),
        roi_ocrrequest_reference_root=str(roots["roi_ocrrequest_reference_root"]),
        roi_crop_rerun_root=str(roots["roi_crop_rerun_root"]),
        better_frame_root=str(roots["better_frame_root"]),
        roi_retry_root=str(roots["roi_retry_root"]),
        source_validation_root=str(roots["source_validation_root"]),
        linebox_sq_root=str(roots["linebox_sq_root"]),
        mixed_batch_v2_root=str(roots["mixed_batch_v2_root"]),
        adapter_v1_root=str(roots["adapter_v1_root"]),
        benchmark_smoke_root=str(roots["benchmark_smoke_root"]),
        system_health_root=str(roots["system_health_root"]),
        simulation_root=str(roots["simulation_root"]),
    )

    summary = result["summary"]
    summary["output_root"] = str(out)
    summary["input_roots"] = {k: str(v) for k, v in roots.items()}

    for fname, key in WRITES:
        _write_json(out / fname, result[key])

    (out / "roi_ocr_quality_notes.md").write_text(
        "\n".join(
            [
                "# ROI OCR Quality Diagnosis v1",
                "",
                f"- Phase: {summary.get('phase')}",
                f"- suspected_root_cause_count: {summary.get('suspected_root_cause_count')}",
                f"- root_cause_confirmed: {summary.get('root_cause_confirmed')}",
                f"- phase_verdict_hint: {summary.get('phase_verdict_hint')}",
                "",
                "Diagnosis only; no OCR, no new crop, no confirmed root cause.",
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
                "suspected_root_cause_count": summary.get("suspected_root_cause_count"),
            },
            ensure_ascii=False,
        )
    )
    return 0 if summary.get("phase_verdict_hint") in ("GO", "CONDITIONAL_GO") else 1


if __name__ == "__main__":
    raise SystemExit(main())
