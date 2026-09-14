#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Meta-verifier for Vision Scene Delta write candidate dry-run smoke output."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

SUMMARY_SCHEMA_VERSION = "scene_delta_write_candidate_dryrun_from_vision_summary_v0"


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


def _walk_forbidden_tree(obj: Any, nav_hit: List[bool], co_hit: List[bool]) -> None:
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k == "navigation_action":
                nav_hit[0] = True
            if k == "label" and str(v or "") == "confirmed_object":
                co_hit[0] = True
            _walk_forbidden_tree(v, nav_hit, co_hit)
    elif isinstance(obj, list):
        for x in obj:
            _walk_forbidden_tree(x, nav_hit, co_hit)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke-root", required=True)
    args = ap.parse_args()

    root = _require_abs(args.smoke_root, "--smoke-root")
    blockers: List[str] = []
    soft: List[str] = []

    sum_p = root / "scene_delta_write_candidate_dryrun_from_vision_summary.json"
    comp_p = root / "scene_delta_write_candidate_from_vision_field_completeness_report.json"
    map_p = root / "scene_delta_write_candidate_from_vision_mapping_matrix.json"
    risk_p = root / "scene_delta_write_candidate_from_vision_risk_report.json"
    nw_p = root / "scene_delta_write_candidate_from_vision_no_write_audit_report.json"

    for label, p in (
        ("dryrun_summary", sum_p),
        ("field_completeness", comp_p),
        ("mapping_matrix", map_p),
        ("risk_report", risk_p),
        ("no_write_audit", nw_p),
    ):
        if not p.is_file():
            blockers.append(f"missing:{label}")

    verdict = "NO_GO"
    if blockers:
        rep = {
            "schema": "scene_delta_write_candidate_dryrun_from_vision_verifier_report_v0",
            "phase": "Phase-MidPlatform-Scene-Delta-Write-Candidate-DryRun-Verifier-From-Vision-001",
            "smoke_root": str(root),
            "verdict": verdict,
            "blockers": blockers,
            "soft_notes": [],
        }
        _write_json(root / "scene_delta_write_candidate_dryrun_from_vision_verifier_report.json", rep)
        print(json.dumps({"smoke_root": str(root), "verdict": verdict, "blockers": blockers}, ensure_ascii=False))
        return 2

    summary: Dict[str, Any] = _read_json(sum_p)
    nw: Dict[str, Any] = _read_json(nw_p)

    if str(summary.get("schema_version") or "") != SUMMARY_SCHEMA_VERSION:
        blockers.append("summary_schema_version_mismatch")
    if not str(summary.get("source_candidate_id") or "").strip():
        blockers.append("source_candidate_id_missing")
    if str(summary.get("source_type") or "") != "vision_recognition_evidence":
        blockers.append("source_type_must_be_vision_recognition_evidence")
    if int(summary.get("evidence_count") or 0) < 1:
        blockers.append("evidence_count_ge_1")

    if summary.get("write_would_be_allowed") is not False:
        blockers.append("write_would_be_allowed_must_be_false")
    if summary.get("executor_invoked") is not False:
        blockers.append("executor_invoked_must_be_false")
    if summary.get("database_write_invoked") is not False:
        blockers.append("summary_database_write_invoked_must_be_false")

    for k, must in (
        ("scene_delta_written", False),
        ("midplatform_fact_written", False),
        ("world_model_written", False),
        ("ai_interpretation_invoked", False),
        ("navigation_decision_invoked", False),
        ("database_write_invoked", False),
        ("external_bus_invoked", False),
        ("real_vision_provider_invoked", False),
        ("yolo_invoked", False),
        ("supervision_mainline_invoked", False),
        ("vlm_invoked", False),
        ("ocr_invoked", False),
    ):
        if nw.get(k) is not must:
            blockers.append(f"no_write_audit:{k}")

    if nw.get("dry_run_executed") is not True:
        blockers.append("dry_run_executed_must_be_true")
    if nw.get("scene_delta_executor_invoked") is not False:
        blockers.append("scene_delta_executor_invoked_must_be_false")

    in_root = str(summary.get("input_write_candidate_root") or "").strip()
    cand_path = Path(in_root) / "scene_delta_write_candidate_from_vision.json" if in_root else None
    gate_path = Path(in_root) / "scene_delta_write_candidate_vision_gate_stub.json" if in_root else None

    if not cand_path or not cand_path.is_file():
        blockers.append("cannot_load_source_write_candidate")
    else:
        cand = _read_json(cand_path)
        items = cand.get("evidence_items") if isinstance(cand.get("evidence_items"), list) else []
        for i, it in enumerate(items):
            if isinstance(it, dict) and str(it.get("fact_status") or "") == "confirmed_fact":
                blockers.append(f"forbidden_confirmed_fact_at_{i}")
        nav_h, co_h = [False], [False]
        _walk_forbidden_tree(cand, nav_h, co_h)
        if nav_h[0]:
            blockers.append("forbidden_navigation_action_in_candidate_tree")
        if co_h[0]:
            blockers.append("forbidden_confirmed_object_label")

    if not gate_path or not gate_path.is_file():
        blockers.append("cannot_load_gate_stub")
    else:
        gate = _read_json(gate_path)
        if str(gate.get("gate_status") or "") != "not_evaluated":
            blockers.append("gate_status_must_remain_not_evaluated")

    if not blockers:
        verdict = "GO"
        comp = _read_json(comp_p)
        if isinstance(comp, dict) and comp.get("overall_complete") is False:
            verdict = "CONDITIONAL_GO"
            soft.append("field_completeness_gaps")
    else:
        verdict = "NO_GO"

    rep = {
        "schema": "scene_delta_write_candidate_dryrun_from_vision_verifier_report_v0",
        "phase": "Phase-MidPlatform-Scene-Delta-Write-Candidate-DryRun-Verifier-From-Vision-001",
        "smoke_root": str(root),
        "verdict": verdict,
        "blockers": blockers,
        "soft_notes": soft,
        "dry_run_id": summary.get("dry_run_id"),
    }
    _write_json(root / "scene_delta_write_candidate_dryrun_from_vision_verifier_report.json", rep)
    print(json.dumps({"smoke_root": str(root), "verdict": verdict, "blockers": blockers}, ensure_ascii=False))
    if verdict == "NO_GO":
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
