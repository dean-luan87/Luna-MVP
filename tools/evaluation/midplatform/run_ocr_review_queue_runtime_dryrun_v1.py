#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase-OCR-Review-Queue-Runtime-DryRun-v1-001 runner."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

WRITES = [
    ("ocr_review_queue_runtime_dryrun_v1_summary.json", "summary"),
    ("ocr_review_queue_runtime_item_schema_v1.json", "item_schema"),
    ("ocr_review_queue_runtime_intake_report.json", "intake"),
    ("ocr_review_queue_runtime_classification_matrix.json", "classification"),
    ("ocr_review_queue_runtime_priority_policy_v1.json", "priority_policy"),
    ("ocr_review_queue_runtime_priority_sort_report.json", "priority_sort"),
    ("ocr_review_queue_runtime_state_transition_plan.json", "state_plan"),
    ("ocr_review_queue_runtime_state_transition_trace.json", "state_trace"),
    ("ocr_review_queue_runtime_dequeue_dryrun_report.json", "dequeue"),
    ("ocr_review_queue_runtime_handler_dryrun_matrix.json", "handler_matrix"),
    ("ocr_review_queue_runtime_decision_placeholder_report.json", "placeholders"),
    ("ocr_review_queue_runtime_boundary_report.json", "boundary"),
    ("ocr_review_queue_runtime_source_chain_report.json", "source_chain"),
    ("ocr_review_queue_runtime_metrics_candidate_report.json", "metrics"),
    ("ocr_review_queue_runtime_benchmark_link_report.json", "benchmark_link"),
    ("ocr_review_queue_runtime_system_health_link_report.json", "health_link"),
    ("ocr_review_queue_runtime_no_write_boundary_report.json", "no_write"),
    ("ocr_review_queue_runtime_simulation_context_report.json", "sim_report"),
    ("ocr_review_queue_runtime_non_claims_report.json", "non_claims"),
    ("ocr_review_queue_runtime_open_followups.json", "followups"),
    ("ocr_review_queue_runtime_audit_report.json", "audit"),
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
    ap.add_argument("--review-policy-v1-root", required=True)
    ap.add_argument("--semantic-v1-root", required=True)
    ap.add_argument("--adapter-v1-root", required=True)
    ap.add_argument("--mixed-batch-v2-root", required=True)
    ap.add_argument("--worldmodel-unresolved-slot-root", required=True)
    ap.add_argument("--benchmark-smoke-root", required=True)
    ap.add_argument("--system-health-root", required=True)
    ap.add_argument("--simulation-root", required=True)
    args = ap.parse_args()

    out = _require_abs(args.output_root, "--output-root")
    roots = {
        "review_policy_v1_root": _require_abs(args.review_policy_v1_root, "policy"),
        "semantic_v1_root": _require_abs(args.semantic_v1_root, "semantic"),
        "adapter_v1_root": _require_abs(args.adapter_v1_root, "adapter"),
        "mixed_batch_v2_root": _require_abs(args.mixed_batch_v2_root, "v2"),
        "worldmodel_unresolved_slot_root": _require_abs(args.worldmodel_unresolved_slot_root, "wm"),
        "benchmark_smoke_root": _require_abs(args.benchmark_smoke_root, "bench"),
        "system_health_root": _require_abs(args.system_health_root, "health"),
        "simulation_root": _require_abs(args.simulation_root, "sim"),
    }

    from capabilities.midplatform.ocr_review_queue_runtime_dryrun_v1 import run_ocr_review_queue_runtime_dryrun_v1

    result = run_ocr_review_queue_runtime_dryrun_v1(
        output_root=str(out),
        review_policy_v1_root=str(roots["review_policy_v1_root"]),
        semantic_v1_root=str(roots["semantic_v1_root"]),
        adapter_v1_root=str(roots["adapter_v1_root"]),
        mixed_batch_v2_root=str(roots["mixed_batch_v2_root"]),
        worldmodel_unresolved_slot_root=str(roots["worldmodel_unresolved_slot_root"]),
        benchmark_smoke_root=str(roots["benchmark_smoke_root"]),
        system_health_root=str(roots["system_health_root"]),
        simulation_root=str(roots["simulation_root"]),
    )

    summary = result["summary"]
    summary["output_root"] = str(out)
    summary["input_roots"] = {k: str(v) for k, v in roots.items()}
    if result.get("errs"):
        summary["errors"] = result["errs"]

    for fname, key in WRITES:
        _write_json(out / fname, result[key])

    (out / "ocr_review_queue_runtime_notes.md").write_text(
        "\n".join(
            [
                "# OCR Review Queue Runtime DryRun v1",
                "",
                f"- Phase: {summary.get('phase')}",
                f"- queue_candidate_count: {summary.get('queue_candidate_count')}",
                f"- runtime_queue_item_count: {summary.get('runtime_queue_item_count')}",
                f"- phase_verdict_hint: {summary.get('phase_verdict_hint')}",
                "",
                "Enqueue / sort / state transition / dequeue simulation only.",
                "",
            ]
        ),
        encoding="utf-8",
    )

    print(
        json.dumps(
            {"output_root": str(out), "phase_verdict_hint": summary.get("phase_verdict_hint"), "errors": result.get("errs", [])},
            ensure_ascii=False,
        )
    )
    return 0 if summary.get("phase_verdict_hint") in ("GO", "CONDITIONAL_GO") else 1


if __name__ == "__main__":
    raise SystemExit(main())
