#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase-Evidence-Pack-Adapter-v3-BBoxExpansion-001 runner."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

WRITES = [
    ("evidence_pack_adapter_v3_bbox_expansion_summary.json", "summary"),
    ("evidence_pack_v3_expanded_roi_result_intake_matrix.json", "intake_matrix"),
    ("evidence_pack_v3_bbox_expansion_schema.json", "schema_doc"),
    ("evidence_pack_v3_bbox_expansion_collection.json", "collection"),
    ("evidence_pack_v3_bbox_expansion_alignment_matrix.json", "alignment_matrix"),
    ("evidence_pack_v3_strategy_preservation_report.json", "strategy_preservation"),
    ("evidence_pack_v3_raw_text_preservation_report.json", "raw_text_preservation"),
    ("evidence_pack_v3_text_item_confidence_preservation_report.json", "text_preservation"),
    ("evidence_pack_v3_bbox_coordinate_attachment_report.json", "coordinate_attachment"),
    ("evidence_pack_v3_strategy_output_risk_report.json", "strategy_output_risk"),
    ("evidence_pack_v3_strategy_comparison_candidate_report.json", "strategy_comparison"),
    ("evidence_pack_v3_provider_metadata_report.json", "provider_metadata_report"),
    ("evidence_pack_v3_source_chain_report.json", "source_chain_report"),
    ("evidence_pack_v3_semantic_readiness_report.json", "semantic_readiness"),
    ("evidence_pack_v3_source_validation_v2_readiness_report.json", "source_validation_readiness"),
    ("evidence_pack_v3_boundary_report.json", "boundary"),
    ("evidence_pack_v3_metrics_candidate_report.json", "metrics"),
    ("evidence_pack_v3_benchmark_link_report.json", "benchmark_link"),
    ("evidence_pack_v3_system_health_link_report.json", "health_link"),
    ("evidence_pack_v3_no_write_boundary_report.json", "no_write"),
    ("evidence_pack_v3_simulation_context_report.json", "sim_report"),
    ("evidence_pack_v3_non_claims_report.json", "non_claims"),
    ("evidence_pack_v3_open_followups.json", "followups"),
    ("evidence_pack_v3_audit_report.json", "audit"),
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
    ap.add_argument("--ocrrequest-gated-submission-v2-root", required=True)
    ap.add_argument("--roi-ocrrequest-reference-v2-root", required=True)
    ap.add_argument("--roi-crop-v2-root", required=True)
    ap.add_argument("--roi-bbox-expansion-root", required=True)
    ap.add_argument("--roi-crop-diversity-root", required=True)
    ap.add_argument("--roi-ocr-quality-diagnosis-root", required=True)
    ap.add_argument("--semantic-v2-root", required=True)
    ap.add_argument("--evidence-pack-v2-root", required=True)
    ap.add_argument("--roi-ocr-gated-submission-v1-root", required=True)
    ap.add_argument("--roi-ocrrequest-reference-v1-root", required=True)
    ap.add_argument("--roi-crop-rerun-v1-root", required=True)
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
        "ocrrequest_gated_submission_v2_root": _require_abs(args.ocrrequest_gated_submission_v2_root, "ocr_v2"),
        "roi_ocrrequest_reference_v2_root": _require_abs(args.roi_ocrrequest_reference_v2_root, "ref_v2"),
        "roi_crop_v2_root": _require_abs(args.roi_crop_v2_root, "crop_v2"),
        "roi_bbox_expansion_root": _require_abs(args.roi_bbox_expansion_root, "bbox_exp"),
        "roi_crop_diversity_root": _require_abs(args.roi_crop_diversity_root, "diversity"),
        "roi_ocr_quality_diagnosis_root": _require_abs(args.roi_ocr_quality_diagnosis_root, "diag"),
        "semantic_v2_root": _require_abs(args.semantic_v2_root, "semantic_v2"),
        "evidence_pack_v2_root": _require_abs(args.evidence_pack_v2_root, "ep_v2"),
        "roi_ocr_gated_submission_v1_root": _require_abs(args.roi_ocr_gated_submission_v1_root, "gs_v1"),
        "roi_ocrrequest_reference_v1_root": _require_abs(args.roi_ocrrequest_reference_v1_root, "ref_v1"),
        "roi_crop_rerun_v1_root": _require_abs(args.roi_crop_rerun_v1_root, "rerun_v1"),
        "better_frame_root": _require_abs(args.better_frame_root, "bf"),
        "roi_retry_root": _require_abs(args.roi_retry_root, "retry"),
        "linebox_sq_root": _require_abs(args.linebox_sq_root, "linebox"),
        "mixed_batch_v2_root": _require_abs(args.mixed_batch_v2_root, "mixed"),
        "benchmark_smoke_root": _require_abs(args.benchmark_smoke_root, "bench"),
        "system_health_root": _require_abs(args.system_health_root, "health"),
        "simulation_root": _require_abs(args.simulation_root, "sim"),
    }

    from capabilities.midplatform.evidence_pack_adapter_v3_bbox_expansion import run_evidence_pack_adapter_v3_bbox_expansion

    result = run_evidence_pack_adapter_v3_bbox_expansion(
        ocrrequest_gated_submission_v2_root=str(roots["ocrrequest_gated_submission_v2_root"]),
        roi_ocrrequest_reference_v2_root=str(roots["roi_ocrrequest_reference_v2_root"]),
        roi_crop_v2_root=str(roots["roi_crop_v2_root"]),
        roi_bbox_expansion_root=str(roots["roi_bbox_expansion_root"]),
        roi_crop_diversity_root=str(roots["roi_crop_diversity_root"]),
        roi_ocr_quality_diagnosis_root=str(roots["roi_ocr_quality_diagnosis_root"]),
        semantic_v2_root=str(roots["semantic_v2_root"]),
        evidence_pack_v2_root=str(roots["evidence_pack_v2_root"]),
        roi_ocr_gated_submission_v1_root=str(roots["roi_ocr_gated_submission_v1_root"]),
        roi_ocrrequest_reference_v1_root=str(roots["roi_ocrrequest_reference_v1_root"]),
        roi_crop_rerun_v1_root=str(roots["roi_crop_rerun_v1_root"]),
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

    (out / "evidence_pack_v3_notes.md").write_text(
        "\n".join(
            [
                "# Evidence Pack Adapter v2 ROIRef",
                "",
                f"- Phase: {summary.get('phase')}",
                f"- evidence_pack_v3_count: {summary.get('evidence_pack_v3_count')}",
                f"- phase_verdict_hint: {summary.get('phase_verdict_hint')}",
                "",
                "Adapter only; no OCR, no semantic, no fact writes.",
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
                "evidence_pack_v3_count": summary.get("evidence_pack_v3_count"),
            },
            ensure_ascii=False,
        )
    )
    return 0 if summary.get("phase_verdict_hint") in ("GO", "CONDITIONAL_GO") else 1


if __name__ == "__main__":
    raise SystemExit(main())
