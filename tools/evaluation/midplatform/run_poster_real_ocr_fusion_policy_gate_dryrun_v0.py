#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase-Poster-Real-OCR-Fusion-Policy-Gate-DryRun-001 runner."""

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
    ap.add_argument("--poster-fusion-ttl-gate-root", required=True)
    ap.add_argument("--poster-fusion-review-queue-root", required=True)
    ap.add_argument("--poster-fusion-candidate-dryrun-root", required=True)
    ap.add_argument("--poster-reference-closure-root", required=True)
    ap.add_argument("--benchmark-real-values-smoke-root", required=True)
    ap.add_argument("--system-health-governance-root", required=True)
    ap.add_argument("--simulation-lab-harness-root", required=True)
    args = ap.parse_args()

    out = _require_abs(args.output_root, "--output-root")
    out.mkdir(parents=True, exist_ok=True)

    from capabilities.midplatform.poster_real_ocr_fusion_policy_gate_dryrun_v0 import (
        run_poster_real_ocr_fusion_policy_gate_dryrun_v0,
    )

    roots = {
        "ttl_gate": _require_abs(args.poster_fusion_ttl_gate_root, "ttl-gate"),
        "review_queue": _require_abs(args.poster_fusion_review_queue_root, "review-queue"),
        "dryrun": _require_abs(args.poster_fusion_candidate_dryrun_root, "dryrun"),
        "closure": _require_abs(args.poster_reference_closure_root, "closure"),
        "bench": _require_abs(args.benchmark_real_values_smoke_root, "bench"),
        "health": _require_abs(args.system_health_governance_root, "health"),
        "sim": _require_abs(args.simulation_lab_harness_root, "sim"),
    }

    (
        summary,
        gate_candidate,
        requirement_matrix,
        decision_matrix,
        ttl_carryover,
        review_carryover,
        commercial_temporal,
        visual_symbol,
        scene_delta_eligibility,
        source_chain,
        metrics,
        benchmark_link,
        health_link,
        boundary,
        sim_report,
        non_claims,
        followups,
        audit,
        errs,
    ) = run_poster_real_ocr_fusion_policy_gate_dryrun_v0(
        poster_fusion_ttl_gate_root=str(roots["ttl_gate"]),
        poster_fusion_review_queue_root=str(roots["review_queue"]),
        poster_fusion_candidate_dryrun_root=str(roots["dryrun"]),
        poster_reference_closure_root=str(roots["closure"]),
        benchmark_real_values_smoke_root=str(roots["bench"]),
        system_health_governance_root=str(roots["health"]),
        simulation_lab_harness_root=str(roots["sim"]),
        output_root=str(out),
    )

    summary["input_roots"] = {k: str(v) for k, v in roots.items()}
    if errs:
        summary["errors"] = errs

    _write_json(out / "poster_real_ocr_fusion_policy_gate_dryrun_summary.json", summary)
    _write_json(out / "poster_real_ocr_fusion_policy_gate_candidate.json", gate_candidate)
    _write_json(out / "poster_real_ocr_fusion_policy_requirement_matrix.json", requirement_matrix)
    _write_json(out / "poster_real_ocr_fusion_policy_gate_decision_matrix.json", decision_matrix)
    _write_json(out / "poster_real_ocr_fusion_policy_ttl_carryover_report.json", ttl_carryover)
    _write_json(out / "poster_real_ocr_fusion_policy_review_queue_carryover_report.json", review_carryover)
    _write_json(out / "poster_real_ocr_fusion_policy_commercial_temporal_report.json", commercial_temporal)
    _write_json(out / "poster_real_ocr_fusion_policy_visual_symbol_report.json", visual_symbol)
    _write_json(out / "poster_real_ocr_fusion_policy_scene_delta_eligibility_report.json", scene_delta_eligibility)
    _write_json(out / "poster_real_ocr_fusion_policy_source_chain_report.json", source_chain)
    _write_json(out / "poster_real_ocr_fusion_policy_metrics_candidate_report.json", metrics)
    _write_json(out / "poster_real_ocr_fusion_policy_benchmark_link_report.json", benchmark_link)
    _write_json(out / "poster_real_ocr_fusion_policy_system_health_link_report.json", health_link)
    _write_json(out / "poster_real_ocr_fusion_policy_no_write_boundary_report.json", boundary)
    _write_json(out / "poster_real_ocr_fusion_policy_simulation_context_report.json", sim_report)
    _write_json(out / "poster_real_ocr_fusion_policy_non_claims_report.json", non_claims)
    _write_json(out / "poster_real_ocr_fusion_policy_open_followups.json", followups)
    _write_json(out / "poster_real_ocr_fusion_policy_audit_report.json", audit)

    (out / "poster_real_ocr_fusion_policy_notes.md").write_text(
        "\n".join(
            [
                "# Poster Real OCR Fusion Policy Gate DryRun",
                "",
                f"- Phase: {summary.get('phase')}",
                f"- gate_scope: {summary.get('gate_scope')}",
                f"- policy_candidate_count: {summary.get('policy_candidate_count')}",
                f"- policy_gate_hold_count: {summary.get('policy_gate_hold_count')}",
                f"- policy_gate_passed_count: {summary.get('policy_gate_passed_count')}",
                f"- phase_verdict_hint: {summary.get('phase_verdict_hint')}",
                "",
                "Policy gate dry-run only; no approval, no Scene Delta, no writes.",
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
