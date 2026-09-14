#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for Poster Real OCR Gated Execution v0."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Set


FORBIDDEN_REGIONS = frozenset(
    {"logo_area", "qr_area", "product_or_decoration_area", "background_or_decoration_area"}
)


def _find_ws_root() -> Path:
    here = Path(__file__).resolve()
    for parent in here.parents:
        if (parent / "capabilities" / "ocr_runtime").is_dir():
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


def _eq_false(val: Any) -> bool:
    return val is False or val == False  # noqa: E712


def main() -> int:
    _find_ws_root()
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke-root", required=True)
    args = ap.parse_args()

    root = _require_abs(args.smoke_root, "--smoke-root")
    blockers: List[str] = []

    paths = {
        "summary": root / "poster_real_ocr_gated_execution_summary.json",
        "plan": root / "poster_real_ocr_execution_plan.json",
        "excluded": root / "poster_real_ocr_excluded_visual_region_guard_report.json",
        "provider": root / "poster_real_ocr_provider_gate_report.json",
        "matrix": root / "poster_real_ocr_result_matrix.json",
        "evidence": root / "poster_layout_text_evidence_candidate.json",
        "reading": root / "poster_real_ocr_reading_order_guard_report.json",
        "ttl": root / "poster_real_ocr_ttl_commercial_risk_report.json",
        "metrics": root / "poster_real_ocr_metrics_binding_report.json",
        "benchmark": root / "poster_real_ocr_benchmark_link_report.json",
        "health": root / "poster_real_ocr_system_health_link_report.json",
        "boundary": root / "poster_real_ocr_no_write_boundary_report.json",
        "sim": root / "poster_real_ocr_simulation_context_report.json",
        "non_claims": root / "poster_real_ocr_non_claims_report.json",
        "audit": root / "poster_real_ocr_audit_report.json",
    }

    for label, p in paths.items():
        if not p.is_file():
            blockers.append(f"missing:{label}")

    if blockers:
        _write_json(
            root / "poster_real_ocr_verifier_report.json",
            {"verdict": "NO_GO", "blockers": blockers, "checks_passed": 0},
        )
        print(json.dumps({"verdict": "NO_GO", "blockers": blockers}, ensure_ascii=False))
        return 2

    summary = _read_json(paths["summary"])
    plan = _read_json(paths["plan"])
    excluded = _read_json(paths["excluded"])
    provider = _read_json(paths["provider"])
    matrix = _read_json(paths["matrix"])
    evidence = _read_json(paths["evidence"])
    reading = _read_json(paths["reading"])
    ttl = _read_json(paths["ttl"])
    metrics = _read_json(paths["metrics"])
    benchmark = _read_json(paths["benchmark"])
    health = _read_json(paths["health"])
    boundary = _read_json(paths["boundary"])
    sim = _read_json(paths["sim"])
    non_claims = _read_json(paths["non_claims"])
    audit = _read_json(paths["audit"])

    if summary.get("execution_scope") != "gated_real_ocr_smoke":
        blockers.append("execution_scope")
    if not _eq_false(summary.get("full_image_ocr_allowed")):
        blockers.append("summary_full_image")
    if summary.get("planned_text_region_count") != 4:
        blockers.append("planned_text_region_count")
    if summary.get("visual_symbol_region_ocr_count") != 0:
        blockers.append("visual_symbol_region_ocr_count")
    if summary.get("paddleocr_invoked") is not False:
        blockers.append("paddleocr_invoked")
    if summary.get("qr_decoder_invoked") is not False:
        blockers.append("qr_decoder")
    if summary.get("brand_database_invoked") is not False:
        blockers.append("brand_database")

    rows = plan.get("rows") if isinstance(plan.get("rows"), list) else []
    if len(rows) != 4:
        blockers.append("plan_row_count")
    plan_ids: Set[str] = set()
    for row in rows:
        if not isinstance(row, dict):
            continue
        rid = str(row.get("source_region_id") or "")
        plan_ids.add(rid)
        if rid in FORBIDDEN_REGIONS:
            blockers.append(f"forbidden_in_plan:{rid}")
        if not _eq_false(row.get("full_image_ocr_allowed")):
            blockers.append("plan_full_image")
    for forbidden in FORBIDDEN_REGIONS:
        if forbidden in plan_ids:
            blockers.append(f"contains:{forbidden}")

    if excluded.get("all_visual_regions_absent_from_ocr_execution_plan") is not True:
        blockers.append("visual_absent_from_plan")
    if excluded.get("excluded_region_count") != 4:
        blockers.append("excluded_region_count")

    if not _eq_false(provider.get("full_image_ocr_allowed")):
        blockers.append("provider_full_image")
    if provider.get("direct_provider_bypass_allowed") is not False:
        blockers.append("direct_bypass")

    mrows = matrix.get("rows") if isinstance(matrix.get("rows"), list) else []
    for mr in mrows:
        if not isinstance(mr, dict):
            continue
        tj = str(mr.get("text_joined") or "")
        if tj == "MOCK_TEXT":
            blockers.append("mock_text_substitution")
        if mr.get("direct_provider_bypass") is not False:
            blockers.append("matrix_direct_bypass")

    if evidence.get("fact_status") != "not_fact":
        blockers.append("evidence_fact_status")
    if evidence.get("write_allowed") is not False:
        blockers.append("evidence_write")

    if reading.get("semantic_join_invoked") is not False:
        blockers.append("semantic_join")
    if reading.get("force_semantic_join_allowed") is not False:
        blockers.append("force_semantic_join")

    if ttl.get("price_or_promo_area_ttl_required") is not True:
        blockers.append("promo_ttl")
    if ttl.get("time_location_area_ttl_required") is not True:
        blockers.append("time_ttl")

    if not paths["metrics"].is_file():
        blockers.append("metrics_missing")
    if benchmark.get("ocr_accuracy_computed") is not False:
        blockers.append("ocr_accuracy")
    if benchmark.get("benchmark_score_generated") is not False:
        blockers.append("benchmark_score")

    if health.get("system_health_governance_available") is not True:
        blockers.append("health_governance")
    if health.get("provider_health_runtime_checked") is not False:
        blockers.append("health_runtime_checked")

    if boundary.get("boundary_ok") is not True:
        blockers.append("boundary_ok")
    if boundary.get("violations") != []:
        blockers.append("boundary_violations")

    if sim.get("simulation_profile_id") != "developer_full":
        blockers.append("sim_profile")

    if non_claims.get("not_benchmark") is not True:
        blockers.append("non_claims_benchmark")
    if non_claims.get("not_provider_superiority") is not True:
        blockers.append("non_claims_provider")

    audit_flags = [
        ("full_image_ocr_invoked", False),
        ("visual_region_ocr_invoked", False),
        ("semantic_join_invoked", False),
        ("fusion_invoked", False),
        ("midplatform_fact_written", False),
        ("scene_delta_written", False),
        ("world_model_written", False),
        ("navigation_decision_invoked", False),
        ("runtime_routing_changed", False),
        ("benchmark_result_claimed", False),
        ("provider_comparison_claimed", False),
        ("no_mock_text_substitution", True),
    ]
    for key, expected in audit_flags:
        if audit.get(key) != expected:
            blockers.append(f"audit:{key}")

    if blockers:
        verdict = "NO_GO"
    elif summary.get("phase_verdict_hint") == "CONDITIONAL_GO":
        verdict = "CONDITIONAL_GO"
    else:
        verdict = str(summary.get("phase_verdict_hint") or "GO")

    report = {
        "schema_version": "poster_real_ocr_verifier_report_v0",
        "verdict": verdict,
        "blockers": blockers,
        "checks_passed": 54 - len(blockers),
        "phase_verdict_hint": summary.get("phase_verdict_hint"),
    }
    _write_json(root / "poster_real_ocr_verifier_report.json", report)
    print(json.dumps({"verdict": verdict, "blockers": blockers}, ensure_ascii=False))
    return 0 if verdict in ("GO", "CONDITIONAL_GO") else 2


if __name__ == "__main__":
    raise SystemExit(main())
