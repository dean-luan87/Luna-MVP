#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase-OCRRequest-Gated-Submission-from-ROI-v1-001 runner."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

WRITES = [
    ("ocrrequest_gated_submission_from_roi_v1_summary.json", "summary"),
    ("ocrrequest_roi_submission_intake_matrix_v1.json", "intake_matrix"),
    ("ocrrequest_roi_submission_gate_policy_v1.json", "gate_policy"),
    ("ocrrequest_roi_submission_plan_v1.json", "submission_plan"),
    ("ocrrequest_roi_bridge_invocation_trace_v1.json", "bridge_trace"),
    ("ocrrequest_roi_direct_provider_bypass_audit_v1.json", "bypass_audit"),
    ("roi_ocr_result_collection_v1.json", "result_collection"),
    ("roi_ocr_result_matrix_v1.json", "result_matrix"),
    ("roi_ocr_empty_nonempty_guard_report_v1.json", "empty_nonempty_guard"),
    ("roi_ocr_source_chain_report_v1.json", "source_chain_report"),
    ("roi_ocr_provider_summary_report_v1.json", "provider_summary"),
    ("roi_ocr_no_evidence_pack_boundary_report_v1.json", "no_evidence_pack_boundary"),
    ("roi_ocr_future_adapter_plan_v1.json", "future_adapter_plan"),
    ("roi_ocr_boundary_report_v1.json", "boundary"),
    ("roi_ocr_metrics_candidate_report_v1.json", "metrics"),
    ("roi_ocr_benchmark_link_report_v1.json", "benchmark_link"),
    ("roi_ocr_system_health_link_report_v1.json", "health_link"),
    ("roi_ocr_no_write_boundary_report_v1.json", "no_write"),
    ("roi_ocr_simulation_context_report_v1.json", "sim_report"),
    ("roi_ocr_non_claims_report_v1.json", "non_claims"),
    ("roi_ocr_open_followups_v1.json", "followups"),
    ("roi_ocr_audit_report_v1.json", "audit"),
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
    gov = out / "roi_gated_submission_governance.json"
    if gov_src.is_file():
        gov.write_text(gov_src.read_text(encoding="utf-8"), encoding="utf-8")
    else:
        fallback = ws / "configs/ocr/ocr_image_input_governance_v0.example.json"
        gov.write_text(fallback.read_text(encoding="utf-8"), encoding="utf-8")
    return _require_abs(str(gov), "governance under output-root")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output-root", required=True)
    ap.add_argument("--roi-ocrrequest-reference-root", required=True)
    ap.add_argument("--roi-crop-rerun-root", required=True)
    ap.add_argument("--better-frame-root", required=True)
    ap.add_argument("--roi-retry-root", required=True)
    ap.add_argument("--source-validation-root", required=True)
    ap.add_argument("--mixed-batch-v2-root", required=True)
    ap.add_argument("--linebox-sq-root", required=True)
    ap.add_argument("--adapter-v1-root", required=True)
    ap.add_argument("--review-queue-runtime-root", required=True)
    ap.add_argument("--review-policy-v1-root", required=True)
    ap.add_argument("--semantic-v1-root", required=True)
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
        "roi_ocrrequest_reference_root": _require_abs(args.roi_ocrrequest_reference_root, "ref"),
        "roi_crop_rerun_root": _require_abs(args.roi_crop_rerun_root, "rerun"),
        "better_frame_root": _require_abs(args.better_frame_root, "bf"),
        "roi_retry_root": _require_abs(args.roi_retry_root, "retry"),
        "source_validation_root": _require_abs(args.source_validation_root, "sv"),
        "mixed_batch_v2_root": _require_abs(args.mixed_batch_v2_root, "v2"),
        "linebox_sq_root": _require_abs(args.linebox_sq_root, "linebox"),
        "adapter_v1_root": _require_abs(args.adapter_v1_root, "adapter"),
        "review_queue_runtime_root": _require_abs(args.review_queue_runtime_root, "rq"),
        "review_policy_v1_root": _require_abs(args.review_policy_v1_root, "policy"),
        "semantic_v1_root": _require_abs(args.semantic_v1_root, "semantic"),
        "benchmark_smoke_root": _require_abs(args.benchmark_smoke_root, "bench"),
        "system_health_root": _require_abs(args.system_health_root, "health"),
        "simulation_root": _require_abs(args.simulation_root, "sim"),
    }

    cap_path = ws / "capabilities/ocr_runtime/ocrrequest_gated_submission_from_roi_v1.py"

    from capabilities.ocr_runtime.ocrrequest_gated_submission_from_roi_v1 import (
        run_ocrrequest_gated_submission_from_roi_v1,
    )

    result = run_ocrrequest_gated_submission_from_roi_v1(
        roi_ocrrequest_reference_root=str(roots["roi_ocrrequest_reference_root"]),
        roi_crop_rerun_root=str(roots["roi_crop_rerun_root"]),
        better_frame_root=str(roots["better_frame_root"]),
        roi_retry_root=str(roots["roi_retry_root"]),
        source_validation_root=str(roots["source_validation_root"]),
        mixed_batch_v2_root=str(roots["mixed_batch_v2_root"]),
        linebox_sq_root=str(roots["linebox_sq_root"]),
        adapter_v1_root=str(roots["adapter_v1_root"]),
        review_queue_runtime_root=str(roots["review_queue_runtime_root"]),
        review_policy_v1_root=str(roots["review_policy_v1_root"]),
        semantic_v1_root=str(roots["semantic_v1_root"]),
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

    (out / "roi_ocr_notes.md").write_text(
        "\n".join(
            [
                "# OCRRequest Gated Submission from ROI v1",
                "",
                f"- Phase: {summary.get('phase')}",
                f"- submitted: {summary.get('ocrrequest_submitted_count')}",
                f"- success: {summary.get('ocrrequest_success_count')}",
                f"- phase_verdict_hint: {summary.get('phase_verdict_hint')}",
                "",
                "Gated submission via ocr_mainline_bridge only.",
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
