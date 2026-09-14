#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase-ROI-Crop-Execution-DryRun-v1-001 runner."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

WRITES = [
    ("roi_crop_execution_dryrun_v1_summary.json", "summary"),
    ("roi_crop_candidate_intake_matrix_v1.json", "intake_matrix"),
    ("roi_crop_execution_policy_v1.json", "execution_policy"),
    ("roi_crop_artifact_schema_v1.json", "artifact_schema"),
    ("roi_crop_artifact_collection_v1.json", "artifact_collection"),
    ("roi_crop_bbox_validation_report_v1.json", "bbox_validation"),
    ("roi_crop_source_resolution_report_v1.json", "source_resolution"),
    ("roi_crop_execution_trace_v1.json", "execution_trace"),
    ("roi_crop_mixed_region_handling_report_v1.json", "mixed_region"),
    ("roi_crop_better_frame_deferred_report_v1.json", "deferred_report"),
    ("roi_crop_to_ocr_request_reference_plan_v1.json", "ocr_ref_plan"),
    ("roi_crop_boundary_report_v1.json", "boundary"),
    ("roi_crop_source_chain_report_v1.json", "source_chain"),
    ("roi_crop_metrics_candidate_report_v1.json", "metrics"),
    ("roi_crop_benchmark_link_report_v1.json", "benchmark_link"),
    ("roi_crop_system_health_link_report_v1.json", "health_link"),
    ("roi_crop_no_write_boundary_report_v1.json", "no_write"),
    ("roi_crop_simulation_context_report_v1.json", "sim_report"),
    ("roi_crop_non_claims_report_v1.json", "non_claims"),
    ("roi_crop_open_followups_v1.json", "followups"),
    ("roi_crop_audit_report_v1.json", "audit"),
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
    args = ap.parse_args()

    out = _require_abs(args.output_root, "--output-root")
    roots = {
        "roi_retry_root": _require_abs(args.roi_retry_root, "roi_retry"),
        "source_validation_root": _require_abs(args.source_validation_root, "sv"),
        "mixed_batch_v2_root": _require_abs(args.mixed_batch_v2_root, "v2"),
        "linebox_sq_root": _require_abs(args.linebox_sq_root, "linebox"),
        "adapter_v1_root": _require_abs(args.adapter_v1_root, "adapter"),
        "review_queue_runtime_root": _require_abs(args.review_queue_runtime_root, "runtime"),
        "review_policy_v1_root": _require_abs(args.review_policy_v1_root, "policy"),
        "semantic_v1_root": _require_abs(args.semantic_v1_root, "semantic"),
        "benchmark_smoke_root": _require_abs(args.benchmark_smoke_root, "bench"),
        "system_health_root": _require_abs(args.system_health_root, "health"),
        "simulation_root": _require_abs(args.simulation_root, "sim"),
    }

    from capabilities.midplatform.roi_crop_execution_dryrun_v1 import run_roi_crop_execution_dryrun_v1

    result = run_roi_crop_execution_dryrun_v1(
        output_root=str(out),
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
    )

    summary = result["summary"]
    summary["output_root"] = str(out)
    summary["input_roots"] = {k: str(v) for k, v in roots.items()}
    if result.get("errs"):
        summary["errors"] = result["errs"]

    coll = dict(result["artifact_collection"])
    coll.pop("artifacts_full", None)
    result["artifact_collection"] = coll

    for fname, key in WRITES:
        _write_json(out / fname, result[key])

    (out / "roi_crop_notes.md").write_text(
        "\n".join(
            [
                "# ROI Crop Execution DryRun v1",
                "",
                f"- Phase: {summary.get('phase')}",
                f"- proposal_count_observed: {summary.get('proposal_count_observed')}",
                f"- crop_executed_count: {summary.get('crop_executed_count')}",
                f"- crop_deferred_count: {summary.get('crop_deferred_count')}",
                f"- phase_verdict_hint: {summary.get('phase_verdict_hint')}",
                "",
                "Crop dry-run only; no OCRRequest, no provider, no fact write.",
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
                "crop_executed_count": summary.get("crop_executed_count"),
                "crop_deferred_count": summary.get("crop_deferred_count"),
                "errors": result.get("errs", []),
            },
            ensure_ascii=False,
        )
    )
    return 0 if summary.get("phase_verdict_hint") in ("GO", "CONDITIONAL_GO") else 1


if __name__ == "__main__":
    raise SystemExit(main())
