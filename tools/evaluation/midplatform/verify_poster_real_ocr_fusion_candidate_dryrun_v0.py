#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for Poster Real OCR Fusion Candidate DryRun v0."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, List


FORBIDDEN_NEXT_STEPS = frozenset({"world_model_write", "scene_delta_write", "navigation"})


def _find_ws_root() -> Path:
    here = Path(__file__).resolve()
    for parent in here.parents:
        if (parent / "capabilities" / "midplatform").is_dir():
            if str(parent) not in sys.path:
                sys.path.insert(0, str(parent))
            return parent
    return here.parents[3]


def _require_abs(p: str, label: str) -> Path:
    pp = Path(p).expanduser()
    if not pp.is_absolute():
        raise SystemExit(f"ERROR: {label} must be absolute, got: {p}")
    return pp.resolve()


def _read_json(p: Path) -> Any:
    return json.loads(p.read_text(encoding="utf-8"))


def _write_json(path: Path, obj: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    _find_ws_root()
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke-root", required=True)
    args = ap.parse_args()

    root = _require_abs(args.smoke_root, "--smoke-root")
    blockers: List[str] = []

    paths = {
        "summary": root / "poster_real_ocr_fusion_candidate_dryrun_summary.json",
        "candidate": root / "poster_real_ocr_fusion_candidate.json",
        "input": root / "poster_real_ocr_fusion_input_matrix.json",
        "visual": root / "poster_real_ocr_fusion_visual_context_matrix.json",
        "hypothesis": root / "poster_real_ocr_fusion_hypothesis_matrix.json",
        "reading": root / "poster_real_ocr_fusion_reading_order_guard.json",
        "ttl": root / "poster_real_ocr_fusion_ttl_commercial_risk_report.json",
        "review": root / "poster_real_ocr_fusion_review_requirement_report.json",
        "chain": root / "poster_real_ocr_fusion_source_chain_report.json",
        "metrics": root / "poster_real_ocr_fusion_metrics_candidate_report.json",
        "benchmark": root / "poster_real_ocr_fusion_benchmark_link_report.json",
        "health": root / "poster_real_ocr_fusion_system_health_link_report.json",
        "boundary": root / "poster_real_ocr_fusion_no_write_boundary_report.json",
        "sim": root / "poster_real_ocr_fusion_simulation_context_report.json",
        "non_claims": root / "poster_real_ocr_fusion_non_claims_report.json",
        "followups": root / "poster_real_ocr_fusion_open_followups.json",
        "audit": root / "poster_real_ocr_fusion_audit_report.json",
    }

    for label, p in paths.items():
        if not p.is_file():
            blockers.append(f"missing:{label}")

    if blockers:
        _write_json(
            root / "poster_real_ocr_fusion_verifier_report.json",
            {"verdict": "NO_GO", "blockers": blockers, "checks_passed": 0},
        )
        print(json.dumps({"verdict": "NO_GO", "blockers": blockers}, ensure_ascii=False))
        return 2

    summary = _read_json(paths["summary"])
    candidate = _read_json(paths["candidate"])
    input_m = _read_json(paths["input"])
    visual = _read_json(paths["visual"])
    hypothesis = _read_json(paths["hypothesis"])
    reading = _read_json(paths["reading"])
    ttl = _read_json(paths["ttl"])
    review = _read_json(paths["review"])
    chain = _read_json(paths["chain"])
    metrics = _read_json(paths["metrics"])
    benchmark = _read_json(paths["benchmark"])
    health = _read_json(paths["health"])
    boundary = _read_json(paths["boundary"])
    sim = _read_json(paths["sim"])
    non_claims = _read_json(paths["non_claims"])
    followups = _read_json(paths["followups"])
    audit = _read_json(paths["audit"])

    if summary.get("dryrun_scope") != "fusion_candidate_dryrun_only":
        blockers.append("dryrun_scope")
    if summary.get("fusion_candidate_generated") is not True:
        blockers.append("fusion_candidate_generated")
    if summary.get("fusion_candidate_count") != 1:
        blockers.append("fusion_candidate_count")
    if summary.get("fusion_committed") is not False:
        blockers.append("fusion_committed")
    if summary.get("semantic_join_committed") is not False:
        blockers.append("semantic_join_committed")
    if summary.get("scene_delta_candidate_generated") is not False:
        blockers.append("scene_delta")
    if summary.get("ocr_reinvoked") is not False:
        blockers.append("ocr_reinvoked")
    if summary.get("rapidocr_reinvoked") is not False:
        blockers.append("rapidocr_reinvoked")

    if candidate.get("candidate_scope") != "dryrun_only":
        blockers.append("candidate_scope")
    if candidate.get("fact_status") != "not_fact":
        blockers.append("candidate_fact")
    if candidate.get("write_allowed") is not False:
        blockers.append("candidate_write")
    if candidate.get("requires_review") is not True:
        blockers.append("requires_review")
    hyp = candidate.get("candidate_hypothesis") if isinstance(candidate.get("candidate_hypothesis"), dict) else {}
    if hyp.get("brand_identity_confirmed") is not False:
        blockers.append("brand_confirmed")
    if hyp.get("qr_decoded") is not False:
        blockers.append("qr_decoded")

    in_rows = input_m.get("rows") if isinstance(input_m.get("rows"), list) else []
    if input_m.get("text_input_region_count") != 4 and len(in_rows) != 4:
        blockers.append("input_region_count")
    for row in in_rows:
        if not isinstance(row, dict):
            continue
        lin = row.get("lineage") if isinstance(row.get("lineage"), dict) else {}
        for key in (
            "layout_region_ref",
            "ocr_plan_ref",
            "real_ocr_execution_ref",
            "readonly_consumer_ref",
            "reference_update_ref",
            "reference_closure_ref",
        ):
            if not lin.get(key):
                blockers.append(f"lineage_missing:{row.get('source_region_id')}:{key}")

    vis_rows = visual.get("rows") if isinstance(visual.get("rows"), list) else []
    if visual.get("visual_context_count") != 4 and len(vis_rows) != 4:
        blockers.append("visual_context_count")
    for vr in vis_rows:
        if isinstance(vr, dict) and vr.get("consumed_as_text") is not False:
            blockers.append("visual_consumed_as_text")

    hyp_rows = hypothesis.get("rows") if isinstance(hypothesis.get("rows"), list) else []
    if not any(
        isinstance(h, dict) and h.get("hypothesis_type") == "review_required_before_any_fact" for h in hyp_rows
    ):
        blockers.append("review_hypothesis_missing")
    for h in hyp_rows:
        if not isinstance(h, dict):
            continue
        step = str(h.get("allowed_next_step") or "")
        if step in FORBIDDEN_NEXT_STEPS or "world_model" in step:
            blockers.append(f"forbidden_next_step:{step}")

    if reading.get("cross_region_text_joined") is not False:
        blockers.append("cross_region_joined")
    if reading.get("semantic_join_committed") is not False:
        blockers.append("semantic_join_reading")
    if reading.get("fusion_fact_allowed") is not False:
        blockers.append("fusion_fact_allowed")

    if ttl.get("ttl_required_region_count") != 2:
        blockers.append("ttl_count")
    if ttl.get("commercial_claim_status") != "candidate_only":
        blockers.append("commercial_claim")
    if ttl.get("temporal_claim_status") != "candidate_only":
        blockers.append("temporal_claim")

    if review.get("auto_approve_allowed") is not False:
        blockers.append("auto_approve")
    if review.get("scene_delta_candidate_allowed_in_this_phase") is not False:
        blockers.append("scene_delta_allowed")

    if metrics.get("fusion_committed") is not False:
        blockers.append("metrics_fusion_committed")
    if metrics.get("benchmark_score_generated") is not False:
        blockers.append("benchmark_score")

    if benchmark.get("benchmark_score_generated") is not False:
        blockers.append("benchmark_link_score")
    if benchmark.get("current_phase_updates_benchmark_values") is not False:
        blockers.append("benchmark_update")

    if health.get("provider_health_runtime_checked") is not False:
        blockers.append("health_runtime")

    if boundary.get("boundary_ok") is not True:
        blockers.append("boundary_ok")
    if boundary.get("violations") != []:
        blockers.append("violations")

    if sim.get("simulation_profile_id") != "developer_full":
        blockers.append("sim_profile")

    if non_claims.get("not_fusion_fact") is not True:
        blockers.append("non_claims_fusion")
    if non_claims.get("not_benchmark") is not True:
        blockers.append("non_claims_benchmark")

    items = followups.get("items") if isinstance(followups.get("items"), list) else []
    if len(items) < 1:
        blockers.append("followups_empty")

    audit_checks = [
        ("visual_symbol_registry_invoked", False),
        ("scene_delta_candidate_generated", False),
        ("midplatform_fact_written", False),
        ("scene_delta_written", False),
        ("world_model_written", False),
        ("navigation_decision_invoked", False),
        ("runtime_routing_changed", False),
    ]
    for key, expected in audit_checks:
        if audit.get(key) != expected:
            blockers.append(f"audit:{key}")

    if blockers:
        verdict = "NO_GO"
    elif summary.get("phase_verdict_hint") == "CONDITIONAL_GO":
        verdict = "CONDITIONAL_GO"
    else:
        verdict = str(summary.get("phase_verdict_hint") or "GO")

    report = {
        "schema_version": "poster_real_ocr_fusion_verifier_report_v0",
        "verdict": verdict,
        "blockers": blockers,
        "checks_passed": 59 - len(blockers),
        "phase_verdict_hint": summary.get("phase_verdict_hint"),
    }
    _write_json(root / "poster_real_ocr_fusion_verifier_report.json", report)
    print(json.dumps({"verdict": verdict, "blockers": blockers}, ensure_ascii=False))
    return 0 if verdict in ("GO", "CONDITIONAL_GO") else 2


if __name__ == "__main__":
    raise SystemExit(main())
