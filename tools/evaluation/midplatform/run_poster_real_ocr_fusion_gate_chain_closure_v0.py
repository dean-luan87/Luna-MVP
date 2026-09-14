#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase-Poster-Real-OCR-Fusion-Gate-Chain-Closure-001 runner."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


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
    ap.add_argument("--poster-fusion-candidate-dryrun-root", required=True)
    ap.add_argument("--poster-fusion-review-queue-root", required=True)
    ap.add_argument("--poster-fusion-ttl-gate-root", required=True)
    ap.add_argument("--poster-fusion-policy-gate-root", required=True)
    ap.add_argument("--poster-reference-closure-root", required=True)
    ap.add_argument("--poster-readonly-consumer-root", required=True)
    ap.add_argument("--poster-gated-execution-root", required=True)
    ap.add_argument("--benchmark-real-values-smoke-root", required=True)
    ap.add_argument("--system-health-governance-root", required=True)
    ap.add_argument("--simulation-lab-harness-root", required=True)
    args = ap.parse_args()

    out = _require_abs(args.output_root, "--output-root")
    out.mkdir(parents=True, exist_ok=True)

    from capabilities.midplatform.poster_real_ocr_fusion_gate_chain_closure_v0 import (
        run_poster_real_ocr_fusion_gate_chain_closure_v0,
    )

    roots = {
        "dryrun": _require_abs(args.poster_fusion_candidate_dryrun_root, "dryrun"),
        "review_queue": _require_abs(args.poster_fusion_review_queue_root, "review-queue"),
        "ttl_gate": _require_abs(args.poster_fusion_ttl_gate_root, "ttl-gate"),
        "policy_gate": _require_abs(args.poster_fusion_policy_gate_root, "policy-gate"),
        "closure": _require_abs(args.poster_reference_closure_root, "closure"),
        "consumer": _require_abs(args.poster_readonly_consumer_root, "consumer"),
        "gated": _require_abs(args.poster_gated_execution_root, "gated"),
        "bench": _require_abs(args.benchmark_real_values_smoke_root, "bench"),
        "health": _require_abs(args.system_health_governance_root, "health"),
        "sim": _require_abs(args.simulation_lab_harness_root, "sim"),
    }

    (
        summary,
        phase_matrix,
        lineage_report,
        decision_matrix,
        blocking_rollup,
        review_approval,
        ttl_closure,
        policy_closure,
        commercial_temporal,
        visual_boundary,
        scene_delta_non_eligibility,
        metrics,
        benchmark_link,
        health_link,
        boundary,
        sim_report,
        non_claims,
        followups,
        audit,
        errs,
    ) = run_poster_real_ocr_fusion_gate_chain_closure_v0(
        poster_fusion_candidate_dryrun_root=str(roots["dryrun"]),
        poster_fusion_review_queue_root=str(roots["review_queue"]),
        poster_fusion_ttl_gate_root=str(roots["ttl_gate"]),
        poster_fusion_policy_gate_root=str(roots["policy_gate"]),
        poster_reference_closure_root=str(roots["closure"]),
        poster_readonly_consumer_root=str(roots["consumer"]),
        poster_gated_execution_root=str(roots["gated"]),
        benchmark_real_values_smoke_root=str(roots["bench"]),
        system_health_governance_root=str(roots["health"]),
        simulation_lab_harness_root=str(roots["sim"]),
        output_root=str(out),
    )

    summary["input_roots"] = {k: str(v) for k, v in roots.items()}
    if errs:
        summary["errors"] = errs

    _write_json(out / "poster_real_ocr_fusion_gate_chain_closure_summary.json", summary)
    _write_json(out / "poster_real_ocr_fusion_gate_chain_phase_matrix.json", phase_matrix)
    _write_json(out / "poster_real_ocr_fusion_gate_chain_lineage_report.json", lineage_report)
    _write_json(out / "poster_real_ocr_fusion_gate_chain_decision_matrix.json", decision_matrix)
    _write_json(out / "poster_real_ocr_fusion_gate_chain_blocking_reasons_rollup.json", blocking_rollup)
    _write_json(out / "poster_real_ocr_fusion_gate_chain_review_approval_closure_report.json", review_approval)
    _write_json(out / "poster_real_ocr_fusion_gate_chain_ttl_closure_report.json", ttl_closure)
    _write_json(out / "poster_real_ocr_fusion_gate_chain_policy_closure_report.json", policy_closure)
    _write_json(out / "poster_real_ocr_fusion_gate_chain_commercial_temporal_closure_report.json", commercial_temporal)
    _write_json(out / "poster_real_ocr_fusion_gate_chain_visual_symbol_boundary_report.json", visual_boundary)
    _write_json(out / "poster_real_ocr_fusion_gate_chain_scene_delta_non_eligibility_report.json", scene_delta_non_eligibility)
    _write_json(out / "poster_real_ocr_fusion_gate_chain_metrics_closure_candidate_report.json", metrics)
    _write_json(out / "poster_real_ocr_fusion_gate_chain_benchmark_link_report.json", benchmark_link)
    _write_json(out / "poster_real_ocr_fusion_gate_chain_system_health_link_report.json", health_link)
    _write_json(out / "poster_real_ocr_fusion_gate_chain_no_write_boundary_report.json", boundary)
    _write_json(out / "poster_real_ocr_fusion_gate_chain_simulation_context_report.json", sim_report)
    _write_json(out / "poster_real_ocr_fusion_gate_chain_non_claims_report.json", non_claims)
    _write_json(out / "poster_real_ocr_fusion_gate_chain_open_followups.json", followups)
    _write_json(out / "poster_real_ocr_fusion_gate_chain_audit_report.json", audit)

    (out / "poster_real_ocr_fusion_gate_chain_notes.md").write_text(
        "\n".join(
            [
                "# Poster Real OCR Fusion Gate Chain Closure",
                "",
                f"- Phase: {summary.get('phase')}",
                f"- closure_scope: {summary.get('closure_scope')}",
                f"- gate_chain_status: {summary.get('gate_chain_status')}",
                f"- fusion_candidate_count: {summary.get('fusion_candidate_count')}",
                f"- phase_verdict_hint: {summary.get('phase_verdict_hint')}",
                "",
                "Gate chain closure only; no approval, no Scene Delta, no writes.",
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
                "errors": errs,
            },
            ensure_ascii=False,
        )
    )
    return 0 if summary.get("phase_verdict_hint") in ("GO", "CONDITIONAL_GO") else 1


if __name__ == "__main__":
    raise SystemExit(main())
