#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for CrossModal Vision OCR TestBoard metrics collector v0."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Set


REQUIRED_GROUPS = {
    "OCR Output Metrics",
    "Case Outcome Metrics",
    "Risk Coverage Metrics",
    "Boundary Metrics",
    "Poster Layout Metrics",
}


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


def _metric_value(matrix: Dict[str, Any], name: str) -> Any:
    rows = matrix.get("rows") if isinstance(matrix.get("rows"), list) else []
    for r in rows:
        if isinstance(r, dict) and r.get("metric_name") == name:
            return r.get("value")
    return None


def main() -> int:
    _find_ws_root()
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke-root", required=True)
    ap.add_argument("--schema-root", required=True)
    ap.add_argument("--v0-closure-root", required=True)
    ap.add_argument("--poster-governance-root", required=True)
    args = ap.parse_args()

    root = _require_abs(args.smoke_root, "--smoke-root")
    schema_root = _require_abs(args.schema_root, "--schema-root")
    v0_root = _require_abs(args.v0_closure_root, "--v0-closure-root")
    poster_root = _require_abs(args.poster_governance_root, "--poster-governance-root")
    blockers: List[str] = []

    if not (schema_root / "cross_modal_vision_ocr_testboard_metrics_schema.json").is_file():
        blockers.append("schema_root_missing")
    if not (v0_root / "cross_modal_vision_ocr_testboard_v0_closure_summary.json").is_file():
        blockers.append("v0_closure_root_missing")
    if not (poster_root / "poster_layout_governance_summary.json").is_file():
        blockers.append("poster_governance_root_missing")

    paths = {
        "summary": root / "cross_modal_vision_ocr_testboard_metrics_collection_summary.json",
        "matrix": root / "cross_modal_vision_ocr_testboard_metrics_value_matrix.json",
        "boundary": root / "cross_modal_vision_ocr_testboard_boundary_metrics_report.json",
        "poster": root / "cross_modal_vision_ocr_testboard_poster_metrics_report.json",
        "guard": root / "cross_modal_vision_ocr_testboard_metrics_interpretation_guard_report.json",
        "audit": root / "cross_modal_vision_ocr_testboard_metrics_collector_audit_report.json",
    }
    for label, p in paths.items():
        if not p.is_file():
            blockers.append(f"missing:{label}")

    if blockers:
        _write_json(
            root / "cross_modal_vision_ocr_testboard_metrics_collector_verifier_report.json",
            {"verdict": "NO_GO", "blockers": blockers},
        )
        print(json.dumps({"verdict": "NO_GO", "blockers": blockers}, ensure_ascii=False))
        return 2

    summary = _read_json(paths["summary"])
    matrix = _read_json(paths["matrix"])
    boundary = _read_json(paths["boundary"])
    poster = _read_json(paths["poster"])
    guard = _read_json(paths["guard"])
    aud = _read_json(paths["audit"])

    if summary.get("collection_scope") != "readonly_smoke":
        blockers.append("collection_scope")
    if summary.get("runtime_execution") is not False:
        blockers.append("runtime_execution")

    groups: Set[str] = set()
    rows = matrix.get("rows") if isinstance(matrix.get("rows"), list) else []
    for r in rows:
        if isinstance(r, dict):
            groups.add(str(r.get("metric_group")))
    for g in REQUIRED_GROUPS:
        if g not in groups:
            blockers.append(f"missing_group:{g}")

    if _metric_value(matrix, "no_write_boundary_pass_rate") != 1.0:
        blockers.append("no_write_boundary_pass_rate")
    for vk in (
        "midplatform_fact_write_violation_count",
        "scene_delta_write_violation_count",
        "world_model_write_violation_count",
        "navigation_decision_violation_count",
        "auto_approval_violation_count",
    ):
        if _metric_value(matrix, vk) != 0:
            blockers.append(vk)

    if poster.get("full_image_ocr_allowed") is not False:
        blockers.append("poster_full_image_ocr")
    if poster.get("ocr_strategy") != "segment_first":
        blockers.append("poster_ocr_strategy")
    if int(poster.get("visual_symbol_region_count") or 0) < 1:
        blockers.append("poster_visual_symbol_count")

    if _metric_value(matrix, "performance_metrics_available") is not False:
        blockers.append("performance_metrics_available")

    if not paths["guard"].is_file() or guard.get("metrics_are_not_benchmark") is not True:
        blockers.append("interpretation_guard")

    if summary.get("benchmark_result_claimed") is not False:
        blockers.append("benchmark_claimed")
    if summary.get("model_selection_claimed") is not False:
        blockers.append("model_selection_claimed")

    for key in (
        "ocr_invoked",
        "vision_provider_invoked",
        "midplatform_fact_written",
        "scene_delta_written",
        "world_model_written",
        "navigation_decision_invoked",
        "auto_approve_invoked",
    ):
        if aud.get(key) is not False:
            blockers.append(f"audit_{key}")

    verdict = "GO" if not blockers else "NO_GO"
    rep: Dict[str, Any] = {
        "schema": "cross_modal_vision_ocr_testboard_metrics_collector_verifier_report_v0",
        "phase": "CrossModal-Vision-OCR-TestBoard-Metrics-Collector-Smoke-001",
        "smoke_root": str(root),
        "verdict": verdict,
        "blockers": blockers,
    }
    _write_json(root / "cross_modal_vision_ocr_testboard_metrics_collector_verifier_report.json", rep)
    print(json.dumps({"smoke_root": str(root), "verdict": verdict, "blockers": blockers}, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
