#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase-Semantic-Candidate-v2-ROIAware-001 runner."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

WRITES = [
    ("semantic_candidate_v2_roiaware_summary.json", "summary"),
    ("semantic_v2_evidence_pack_intake_matrix.json", "intake_matrix"),
    ("semantic_v2_roiaware_rule_matrix.json", "rule_matrix"),
    ("semantic_candidate_v2_roiaware_schema.json", "schema_doc"),
    ("semantic_candidate_v2_roiaware_collection.json", "collection"),
    ("semantic_v2_risk_consumption_report.json", "risk_consumption"),
    ("semantic_v2_low_information_guard_report.json", "low_information_guard"),
    ("semantic_v2_repeated_same_text_diagnostic_report.json", "repeated_diag"),
    ("semantic_v2_blocking_matrix.json", "blocking_matrix"),
    ("semantic_v2_interpretation_basis_report.json", "interpretation_basis"),
    ("semantic_v2_source_chain_report.json", "source_chain_report"),
    ("semantic_v2_routing_report.json", "routing"),
    ("semantic_v2_future_review_validation_plan.json", "future_plan"),
    ("semantic_v2_boundary_report.json", "boundary"),
    ("semantic_v2_metrics_candidate_report.json", "metrics"),
    ("semantic_v2_benchmark_link_report.json", "benchmark_link"),
    ("semantic_v2_system_health_link_report.json", "health_link"),
    ("semantic_v2_no_write_boundary_report.json", "no_write"),
    ("semantic_v2_simulation_context_report.json", "sim_report"),
    ("semantic_v2_non_claims_report.json", "non_claims"),
    ("semantic_v2_open_followups.json", "followups"),
    ("semantic_v2_audit_report.json", "audit"),
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
    ap.add_argument("--evidence-pack-v2-root", required=True)
    ap.add_argument("--roi-ocr-gated-submission-root", required=True)
    ap.add_argument("--roi-ocrrequest-reference-root", required=True)
    ap.add_argument("--roi-crop-rerun-root", required=True)
    ap.add_argument("--better-frame-root", required=True)
    ap.add_argument("--roi-retry-root", required=True)
    ap.add_argument("--source-validation-root", required=True)
    ap.add_argument("--adapter-v1-root", required=True)
    ap.add_argument("--mixed-batch-v2-root", required=True)
    ap.add_argument("--linebox-sq-root", required=True)
    ap.add_argument("--review-queue-runtime-root", required=True)
    ap.add_argument("--review-policy-v1-root", required=True)
    ap.add_argument("--semantic-v1-root", required=True)
    ap.add_argument("--benchmark-smoke-root", required=True)
    ap.add_argument("--system-health-root", required=True)
    ap.add_argument("--simulation-root", required=True)
    args = ap.parse_args()

    out = _require_abs(args.output_root, "--output-root")
    roots = {
        "evidence_pack_v2_root": _require_abs(args.evidence_pack_v2_root, "epv2"),
        "roi_ocr_gated_submission_root": _require_abs(args.roi_ocr_gated_submission_root, "ocr"),
        "roi_ocrrequest_reference_root": _require_abs(args.roi_ocrrequest_reference_root, "ref"),
        "roi_crop_rerun_root": _require_abs(args.roi_crop_rerun_root, "rerun"),
        "better_frame_root": _require_abs(args.better_frame_root, "bf"),
        "roi_retry_root": _require_abs(args.roi_retry_root, "retry"),
        "source_validation_root": _require_abs(args.source_validation_root, "sv"),
        "adapter_v1_root": _require_abs(args.adapter_v1_root, "adapter"),
        "mixed_batch_v2_root": _require_abs(args.mixed_batch_v2_root, "v2"),
        "linebox_sq_root": _require_abs(args.linebox_sq_root, "linebox"),
        "review_queue_runtime_root": _require_abs(args.review_queue_runtime_root, "rq"),
        "review_policy_v1_root": _require_abs(args.review_policy_v1_root, "policy"),
        "semantic_v1_root": _require_abs(args.semantic_v1_root, "semantic"),
        "benchmark_smoke_root": _require_abs(args.benchmark_smoke_root, "bench"),
        "system_health_root": _require_abs(args.system_health_root, "health"),
        "simulation_root": _require_abs(args.simulation_root, "sim"),
    }

    from capabilities.midplatform.semantic_candidate_v2_roiaware import run_semantic_candidate_v2_roiaware

    result = run_semantic_candidate_v2_roiaware(
        evidence_pack_v2_root=str(roots["evidence_pack_v2_root"]),
        roi_ocr_gated_submission_root=str(roots["roi_ocr_gated_submission_root"]),
        roi_ocrrequest_reference_root=str(roots["roi_ocrrequest_reference_root"]),
        roi_crop_rerun_root=str(roots["roi_crop_rerun_root"]),
        better_frame_root=str(roots["better_frame_root"]),
        roi_retry_root=str(roots["roi_retry_root"]),
        source_validation_root=str(roots["source_validation_root"]),
        adapter_v1_root=str(roots["adapter_v1_root"]),
        mixed_batch_v2_root=str(roots["mixed_batch_v2_root"]),
        linebox_sq_root=str(roots["linebox_sq_root"]),
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

    for fname, key in WRITES:
        _write_json(out / fname, result[key])

    (out / "semantic_v2_notes.md").write_text(
        "\n".join(
            [
                "# Semantic Candidate v2 ROIAware",
                "",
                f"- Phase: {summary.get('phase')}",
                f"- semantic_candidate_v2_count: {summary.get('semantic_candidate_v2_count')}",
                f"- diagnostic_semantic_generated_count: {summary.get('diagnostic_semantic_generated_count')}",
                f"- phase_verdict_hint: {summary.get('phase_verdict_hint')}",
                "",
                "Risk-aware dry-run only; no strong semantic, no entity, no LLM.",
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
                "semantic_candidate_v2_count": summary.get("semantic_candidate_v2_count"),
            },
            ensure_ascii=False,
        )
    )
    return 0 if summary.get("phase_verdict_hint") in ("GO", "CONDITIONAL_GO") else 1


if __name__ == "__main__":
    raise SystemExit(main())
