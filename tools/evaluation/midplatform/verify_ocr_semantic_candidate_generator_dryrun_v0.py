#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for OCR Semantic Candidate Generator DryRun v0."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, List


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


def _is_false(v: Any) -> bool:
    return v is False


def main() -> int:
    _find_ws_root()
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke-root", required=True)
    args = ap.parse_args()

    root = _require_abs(args.smoke_root, "--smoke-root")
    blockers: List[str] = []
    checks_passed = 0

    def ok(cond: bool, name: str) -> None:
        nonlocal checks_passed
        if cond:
            checks_passed += 1
        else:
            blockers.append(name)

    paths = {
        "summary": root / "ocr_semantic_candidate_generator_summary.json",
        "collection": root / "ocr_semantic_candidate_collection.json",
        "poster_matrix": root / "ocr_semantic_candidate_poster_matrix.json",
        "rv_empty": root / "ocr_semantic_candidate_realvideo_empty_matrix.json",
        "type_report": root / "ocr_semantic_candidate_type_classification_report.json",
        "enhancement": root / "ocr_semantic_candidate_enhancement_report.json",
        "basis": root / "ocr_semantic_candidate_interpretation_basis_report.json",
        "gov": root / "ocr_semantic_candidate_governance_routing_report.json",
        "raw": root / "ocr_semantic_candidate_raw_text_preservation_report.json",
        "empty_guard": root / "ocr_semantic_candidate_empty_text_guard_report.json",
        "quality": root / "ocr_semantic_candidate_quality_risk_report.json",
        "wm": root / "ocr_semantic_candidate_world_model_attach_placeholder_carryover_report.json",
        "chain": root / "ocr_semantic_candidate_source_chain_report.json",
        "metrics": root / "ocr_semantic_candidate_metrics_candidate_report.json",
        "benchmark": root / "ocr_semantic_candidate_benchmark_link_report.json",
        "health": root / "ocr_semantic_candidate_system_health_link_report.json",
        "boundary": root / "ocr_semantic_candidate_no_write_boundary_report.json",
        "sim": root / "ocr_semantic_candidate_simulation_context_report.json",
        "non_claims": root / "ocr_semantic_candidate_non_claims_report.json",
        "followups": root / "ocr_semantic_candidate_open_followups.json",
        "audit": root / "ocr_semantic_candidate_audit_report.json",
    }

    for label, p in paths.items():
        if not p.is_file():
            blockers.append(f"missing:{label}")

    if blockers:
        _write_json(
            root / "ocr_semantic_candidate_verifier_report.json",
            {"verdict": "NO_GO", "blockers": blockers, "checks_passed": 0},
        )
        print(json.dumps({"verdict": "NO_GO", "blockers": blockers}, ensure_ascii=False))
        return 2

    summary = _read_json(paths["summary"])
    collection = _read_json(paths["collection"])
    poster_matrix = _read_json(paths["poster_matrix"])
    rv_empty = _read_json(paths["rv_empty"])
    type_report = _read_json(paths["type_report"])
    enhancement = _read_json(paths["enhancement"])
    basis = _read_json(paths["basis"])
    gov = _read_json(paths["gov"])
    raw = _read_json(paths["raw"])
    empty_guard = _read_json(paths["empty_guard"])
    quality = _read_json(paths["quality"])
    wm = _read_json(paths["wm"])
    chain = _read_json(paths["chain"])
    metrics = _read_json(paths["metrics"])
    benchmark = _read_json(paths["benchmark"])
    health = _read_json(paths["health"])
    boundary = _read_json(paths["boundary"])
    sim = _read_json(paths["sim"])
    non_claims = _read_json(paths["non_claims"])
    followups = _read_json(paths["followups"])
    audit = _read_json(paths["audit"])

    ok(summary.get("generator_scope") == "semantic_candidate_dryrun_only", "generator_scope")
    ok(summary.get("input_pack_count") == 14, "input_pack_count")
    ok(summary.get("semantic_candidate_count") == 14, "semantic_candidate_count")
    ok(summary.get("poster_semantic_candidate_count") == 4, "poster_semantic_candidate_count")
    ok(summary.get("realvideo_semantic_candidate_count") == 10, "realvideo_semantic_candidate_count")
    ok(_is_false(summary.get("semantic_model_invoked")), "summary_semantic_model")
    ok(_is_false(summary.get("raw_text_overwritten")), "summary_raw_overwrite")
    ok(_is_false(summary.get("completion_committed")), "summary_completion")
    ok(_is_false(summary.get("correction_committed")), "summary_correction")

    ok(collection.get("candidate_count") == 14, "candidate_count")
    ok(collection.get("semantic_candidate_not_fact") is True, "collection_not_fact")
    candidates = collection.get("candidates") if isinstance(collection.get("candidates"), list) else []
    for c in candidates:
        if not isinstance(c, dict):
            blockers.append("candidate_invalid")
            break
        if c.get("semantic_candidate_not_fact") is not True:
            blockers.append(f"not_fact:{c.get('semantic_candidate_id')}")
            break
        if c.get("raw_ocr_text_preserved") is not True:
            blockers.append(f"raw_preserved:{c.get('semantic_candidate_id')}")
            break
    else:
        checks_passed += 1

    ok(poster_matrix.get("poster_semantic_candidate_count") == 4, "poster_matrix_count")
    poster_rows = poster_matrix.get("rows") if isinstance(poster_matrix.get("rows"), list) else []
    for row in poster_rows:
        if not isinstance(row, dict):
            continue
        st = row.get("semantic_type_candidate")
        if st == "price_discount_text" and row.get("requires_ttl") is not True:
            blockers.append("price_discount_ttl")
            break
        if st == "temporal_notice_text" and row.get("requires_ttl") is not True:
            blockers.append("temporal_notice_ttl")
            break
    else:
        checks_passed += 1

    ok(rv_empty.get("realvideo_empty_candidate_count") == 10, "rv_empty_count")
    ok(rv_empty.get("empty_text_is_not_no_text_fact") is True, "rv_empty_guard")
    ok(rv_empty.get("no_text_fact_generated") is False, "no_text_fact_generated")

    ok(type_report.get("type_registry_used") is True, "type_registry_used")
    ok(type_report.get("fact_write_default_false_count") == 14, "fact_write_default")

    ok(enhancement.get("completion_committed_count") == 0, "completion_committed_count")
    ok(enhancement.get("correction_committed_count") == 0, "correction_committed_count")
    ok(enhancement.get("raw_text_overwritten") is False, "enhancement_raw_overwrite")

    basis_rows = basis.get("rows") if isinstance(basis.get("rows"), list) else []
    for row in basis_rows:
        if not isinstance(row, dict):
            blockers.append("basis_row_invalid")
            break
        if not row.get("ocr_text_ref"):
            blockers.append(f"missing_ocr_text_ref:{row.get('semantic_candidate_id')}")
            break
        if not row.get("image_coordinate_ref"):
            blockers.append(f"missing_image_ref:{row.get('semantic_candidate_id')}")
            break
    else:
        checks_passed += 1

    gov_rows = gov.get("rows") if isinstance(gov.get("rows"), list) else []
    for row in gov_rows:
        if not isinstance(row, dict):
            continue
        if row.get("world_model_attach_allowed") is not False:
            blockers.append("wm_attach_allowed")
            break
        if row.get("scene_delta_candidate_allowed") is not False:
            blockers.append("scene_delta_allowed")
            break
    else:
        checks_passed += 1

    ok(raw.get("raw_text_preservation_rate") == 1.0, "raw_preservation_rate")
    ok(empty_guard.get("no_world_model_write_from_empty_text") is True, "empty_wm_guard")
    ok(quality.get("world_model_write_blocked_count") == 14, "wm_write_blocked")
    ok(wm.get("wm_attach_placeholder_count") == 14, "wm_placeholder_count")
    ok(_is_false(wm.get("world_model_attach_executed")), "wm_executed")
    ok(chain.get("source_chain_preserved") is True, "source_chain_preserved")
    ok(_is_false(metrics.get("semantic_model_invoked")), "metrics_semantic_model")
    ok(benchmark.get("benchmark_score_generated") is False, "benchmark_score")
    ok(health.get("provider_health_runtime_checked") is False, "provider_health")
    ok(boundary.get("boundary_ok") is True, "boundary_ok")
    ok(boundary.get("violations") == [], "boundary_violations")
    ok(sim.get("simulation_profile_id") == "developer_full", "sim_profile")
    ok(non_claims.get("no_semantic_model_execution") is True, "non_claims_semantic")
    ok(non_claims.get("no_real_world_model_attach_candidate") is True, "non_claims_wm")
    ok(isinstance(followups.get("items"), list) and len(followups.get("items", [])) >= 8, "followups")
    ok(audit.get("ocr_semantic_candidate_generator_dryrun_executed") is True, "audit_executed")
    ok(_is_false(audit.get("llm_invoked")), "audit_llm")
    ok(_is_false(audit.get("vlm_invoked")), "audit_vlm")
    ok(_is_false(audit.get("raw_text_overwritten")), "audit_raw_overwrite")
    ok(_is_false(audit.get("completion_committed")), "audit_completion")
    ok(_is_false(audit.get("correction_committed")), "audit_correction")
    ok(_is_false(audit.get("world_model_attach_executed")), "audit_wm")
    ok(_is_false(audit.get("scene_delta_candidate_generated")), "audit_scene_delta")
    ok(_is_false(audit.get("midplatform_fact_written")), "audit_midplatform")
    ok(_is_false(audit.get("world_model_written")), "audit_world_model")
    ok(_is_false(audit.get("navigation_decision_invoked")), "audit_navigation")
    ok(_is_false(audit.get("runtime_routing_changed")), "audit_routing")

    verdict = "GO" if not blockers else "NO_GO"
    report = {
        "schema_version": "ocr_semantic_candidate_verifier_report_v0",
        "verdict": verdict,
        "blockers": blockers,
        "checks_passed": checks_passed,
        "smoke_root": str(root),
    }
    _write_json(root / "ocr_semantic_candidate_verifier_report.json", report)
    print(json.dumps({"verdict": verdict, "blockers": blockers, "checks_passed": checks_passed}, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
