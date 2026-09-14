#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for CrossModal Vision OCR TestBoard v1 planning."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List


REQUIRED_TRACK_IDS = frozenset(
    {"TVOCR_V1_A_REAL_VIDEO", "TVOCR_V1_B_POSTER_LAYOUT", "TVOCR_V1_C_BENCHMARK_PERFORMANCE"}
)


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


def _phase_in_roadmap(roadmap: Dict[str, Any], phase_substr: str) -> bool:
    tracks = roadmap.get("tracks") if isinstance(roadmap.get("tracks"), dict) else {}
    for phases in tracks.values():
        if not isinstance(phases, list):
            continue
        for ph in phases:
            if isinstance(ph, dict) and phase_substr in str(ph.get("phase_id", "")):
                return True
    return False


def main() -> int:
    _find_ws_root()
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke-root", required=True)
    args = ap.parse_args()

    root = _require_abs(args.smoke_root, "--smoke-root")
    blockers: List[str] = []

    paths = {
        "summary": root / "cross_modal_vision_ocr_testboard_v1_planning_summary.json",
        "tracks": root / "cross_modal_vision_ocr_testboard_v1_track_matrix.json",
        "roadmap": root / "cross_modal_vision_ocr_testboard_v1_phase_roadmap.json",
        "non_goals": root / "cross_modal_vision_ocr_testboard_v1_non_goals_report.json",
        "risks": root / "cross_modal_vision_ocr_testboard_v1_risk_register.json",
        "gate": root / "cross_modal_vision_ocr_testboard_v1_gate_policy.json",
        "execution": root / "cross_modal_vision_ocr_testboard_v1_execution_order.json",
        "audit": root / "cross_modal_vision_ocr_testboard_v1_planning_audit_report.json",
    }

    for label, p in paths.items():
        if not p.is_file():
            blockers.append(f"missing:{label}")

    if blockers:
        rep = {
            "schema": "cross_modal_vision_ocr_testboard_v1_planning_verifier_report_v0",
            "phase": "Phase-CrossModal-Vision-OCR-TestBoard-v1-Planning-001",
            "smoke_root": str(root),
            "verdict": "NO_GO",
            "blockers": blockers,
        }
        _write_json(root / "cross_modal_vision_ocr_testboard_v1_planning_verifier_report.json", rep)
        print(json.dumps({"smoke_root": str(root), "verdict": "NO_GO", "blockers": blockers}, ensure_ascii=False))
        return 2

    summary = _read_json(paths["summary"])
    tracks_doc = _read_json(paths["tracks"])
    roadmap = _read_json(paths["roadmap"])
    non_goals = _read_json(paths["non_goals"])
    risks_doc = _read_json(paths["risks"])
    gate = _read_json(paths["gate"])
    aud = _read_json(paths["audit"])

    if summary.get("based_on_v0_status") != "closed_for_v0":
        blockers.append("based_on_v0_status_not_closed")
    if summary.get("v1_scope_locked") is not True:
        blockers.append("v1_scope_locked_false")

    track_list = tracks_doc.get("tracks") if isinstance(tracks_doc.get("tracks"), list) else []
    if len(track_list) != 3:
        blockers.append("track_matrix_not_3")
    track_ids = {t.get("track_id") for t in track_list if isinstance(t, dict)}
    if track_ids != REQUIRED_TRACK_IDS:
        blockers.append("track_ids_incomplete")

    if not _phase_in_roadmap(roadmap, "Poster-Layout-Segmentation-Governance"):
        blockers.append("roadmap_missing_poster_governance")
    if not _phase_in_roadmap(roadmap, "RealVideo-CaseRegistry"):
        blockers.append("roadmap_missing_real_video_registry")
    if not _phase_in_roadmap(roadmap, "Metrics-Schema"):
        blockers.append("roadmap_missing_metrics_schema")

    explicit_ng = non_goals.get("explicit_non_goals") if isinstance(non_goals.get("explicit_non_goals"), list) else []
    ng_blob = " ".join(str(x) for x in explicit_ng).lower()
    wp = non_goals.get("write_policy") if isinstance(non_goals.get("write_policy"), dict) else {}
    if wp.get("midplatform_fact_write") is not False and "fact" not in ng_blob:
        blockers.append("non_goals_no_fact_write")
    if wp.get("scene_delta_write") is not False and "scene delta" not in ng_blob:
        blockers.append("non_goals_no_scene_delta")
    if wp.get("navigation_decision") is not False and "navigation" not in ng_blob:
        blockers.append("non_goals_no_navigation")

    risks = risks_doc.get("risks") if isinstance(risks_doc.get("risks"), list) else []
    risk_ids = {r.get("risk_id") for r in risks if isinstance(r, dict)}
    if "poster_layout_complexity" not in risk_ids:
        blockers.append("risk_missing_poster_layout_complexity")
    if "reading_order_uncertainty" not in risk_ids:
        blockers.append("risk_missing_reading_order_uncertainty")

    default_gate = gate.get("default_for_all_v1_phases") if isinstance(gate.get("default_for_all_v1_phases"), dict) else {}
    if default_gate.get("write_allowed") is not False:
        blockers.append("gate_write_allowed_not_false")
    poster_gate = (
        gate.get("track_policies", {}).get("TVOCR_V1_B_POSTER_LAYOUT", {})
        if isinstance(gate.get("track_policies"), dict)
        else {}
    )
    if poster_gate.get("full_image_ocr_allowed_default") is not False:
        blockers.append("poster_full_image_ocr_not_false")

    audit_checks = (
        ("no_runtime_execution", True),
        ("no_ocr_invoked", True),
        ("no_vision_provider_invoked", True),
        ("midplatform_fact_written", False),
        ("scene_delta_written", False),
        ("world_model_written", False),
        ("navigation_decision_invoked", False),
        ("auto_approve_invoked", False),
        ("approval_granted", False),
    )
    for key, expected in audit_checks:
        if aud.get(key) != expected:
            blockers.append(f"audit_{key}_mismatch")

    verdict = "GO" if not blockers else "NO_GO"
    rep: Dict[str, Any] = {
        "schema": "cross_modal_vision_ocr_testboard_v1_planning_verifier_report_v0",
        "phase": "Phase-CrossModal-Vision-OCR-TestBoard-v1-Planning-001",
        "smoke_root": str(root),
        "verdict": verdict,
        "blockers": blockers,
    }
    _write_json(root / "cross_modal_vision_ocr_testboard_v1_planning_verifier_report.json", rep)
    print(json.dumps({"smoke_root": str(root), "verdict": verdict, "blockers": blockers}, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
