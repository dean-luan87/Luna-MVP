#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase-OCRRequest-Gated-Submission-from-ROI-v2-BBoxExpansion-001 runner."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

WRITES = [
    ("ocrrequest_gated_submission_v2_bbox_expansion_summary.json", "summary"),
    ("ocrrequest_v2_bbox_expansion_submission_intake_matrix.json", "intake_matrix"),
    ("ocrrequest_v2_bbox_expansion_submission_gate_policy.json", "gate_policy"),
    ("ocrrequest_v2_bbox_expansion_submission_plan.json", "submission_plan"),
    ("ocrrequest_v2_bbox_expansion_bridge_invocation_trace.json", "bridge_trace"),
    ("ocrrequest_v2_direct_provider_bypass_audit.json", "bypass_audit"),
    ("expanded_roi_ocr_result_collection_v2.json", "result_collection"),
    ("expanded_roi_ocr_result_matrix_v2.json", "result_matrix"),
    ("expanded_roi_ocr_strategy_output_comparison_candidate_v2.json", "strategy_comparison"),
    ("expanded_roi_ocr_low_information_guard_v2.json", "low_information_guard"),
    ("expanded_roi_ocr_source_chain_report_v2.json", "source_chain_report"),
    ("expanded_roi_ocr_provider_summary_v2.json", "provider_summary"),
    ("expanded_roi_ocr_no_evidence_pack_boundary_v2.json", "no_evidence_pack_boundary"),
    ("expanded_roi_ocr_future_adapter_plan_v3.json", "future_adapter_plan"),
    ("expanded_roi_ocr_boundary_report_v2.json", "boundary"),
    ("expanded_roi_ocr_metrics_candidate_v2.json", "metrics"),
    ("expanded_roi_ocr_benchmark_link_v2.json", "benchmark_link"),
    ("expanded_roi_ocr_system_health_link_v2.json", "health_link"),
    ("expanded_roi_ocr_no_write_boundary_v2.json", "no_write"),
    ("expanded_roi_ocr_simulation_context_v2.json", "sim_report"),
    ("expanded_roi_ocr_non_claims_report_v2.json", "non_claims"),
    ("expanded_roi_ocr_open_followups_v2.json", "followups"),
    ("expanded_roi_ocr_audit_report_v2.json", "audit"),
]


def _find_ws_root() -> Path:
    here = Path(__file__).resolve()
    for parent in here.parents:
        if (parent / "capabilities" / "ocr_runtime").is_dir():
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


def _apply_rapidocr_env() -> None:
    os.environ["LUNA_ENABLE_OCR_MAINLINE_BRIDGE_V0"] = "true"
    os.environ["LUNA_ENABLE_OCR_REAL_PROVIDER_V0"] = "true"
    os.environ["LUNA_ENABLE_RAPIDOCR_RUNTIME_PROVIDER_V0"] = "true"
    os.environ["LUNA_ENABLE_OCR_STUB_PROVIDER_V0"] = "true"
    os.environ["LUNA_ENABLE_PADDLEOCR_RUNTIME_PROVIDER_V0"] = "false"
    os.environ["LUNA_OCR_SUBMISSION_EVAL_ONLY"] = "true"
    os.environ.setdefault("LUNA_OCR_LIGHTWEIGHT_MAX_EDGE_PX", "512")


def _prepare_governance(ws: Path, out: Path, gov_arg: str) -> Path:
    gov_src = (
        Path(gov_arg).expanduser()
        if gov_arg.strip()
        else (ws / "configs/ocr/ocr_image_input_governance_lightweight_normalized_smoke_v0.example.json")
    )
    if not gov_src.is_absolute():
        gov_src = (ws / gov_src).resolve()
    gov = out / "roi_gated_submission_v2_governance.json"
    if gov_src.is_file():
        gov.write_text(gov_src.read_text(encoding="utf-8"), encoding="utf-8")
    else:
        fallback = ws / "configs/ocr/ocr_image_input_governance_v0.example.json"
        gov.write_text(fallback.read_text(encoding="utf-8"), encoding="utf-8")
    return _require_abs(str(gov), "governance under output-root")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output-root", required=True)
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
    ap.add_argument("--workspace-root", default=str(WS_ROOT))
    ap.add_argument("--governance-config", default="")
    args = ap.parse_args()

    _apply_rapidocr_env()
    out = _require_abs(args.output_root, "--output-root")
    out.mkdir(parents=True, exist_ok=True)
    ws = _require_abs(args.workspace_root, "--workspace-root")
    gov = _prepare_governance(ws, out, args.governance_config)
    work_root = out / "_work" / "submissions"

    roots = {
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

    cap_path = ws / "capabilities/ocr_runtime/ocrrequest_gated_submission_from_roi_v2_bbox_expansion.py"

    from capabilities.ocr_runtime.ocrrequest_gated_submission_from_roi_v2_bbox_expansion import (
        run_ocrrequest_gated_submission_from_roi_v2_bbox_expansion,
    )

    result = run_ocrrequest_gated_submission_from_roi_v2_bbox_expansion(
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
        workspace_root=str(ws),
        governance_config_path=str(gov),
        submission_work_root=str(work_root),
        capability_path=str(cap_path),
    )

    summary = result["summary"]
    summary["output_root"] = str(out)
    summary["input_roots"] = {k: str(v) for k, v in roots.items()}

    for fname, key in WRITES:
        _write_json(out / fname, result[key])

    (out / "expanded_roi_ocr_notes.md").write_text(
        "\n".join(
            [
                "# OCRRequest Gated Submission from ROI v2 BBoxExpansion",
                "",
                f"- Phase: {summary.get('phase')}",
                f"- references: {summary.get('ocrrequest_reference_v2_count_observed')}",
                f"- submitted: {summary.get('ocrrequest_submitted_count')}",
                f"- success: {summary.get('ocrrequest_success_count')}",
                f"- phase_verdict_hint: {summary.get('phase_verdict_hint')}",
                "",
                "Expanded ROI crops only; bridge-only provider; not_fact.",
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
                "ocrrequest_submitted_count": summary.get("ocrrequest_submitted_count"),
                "ocrrequest_success_count": summary.get("ocrrequest_success_count"),
            },
            ensure_ascii=False,
        )
    )
    return 0 if summary.get("phase_verdict_hint") in ("GO", "CONDITIONAL_GO") else 1


if __name__ == "__main__":
    raise SystemExit(main())
