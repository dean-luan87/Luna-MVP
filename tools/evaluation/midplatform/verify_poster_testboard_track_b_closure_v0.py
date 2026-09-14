#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase-Poster-TestBoard-Closure-001 verifier."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List


def _read_json(p: Path) -> Any:
    return json.loads(p.read_text(encoding="utf-8"))


def _write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


REQUIRED_PHASES = (
    "OCR-Poster-Layout-Segmentation-Governance-001",
    "OCR-Poster-Region-OCR-Plan-Stub-001",
    "OCR-Poster-VisualSymbolEvidence-Stub-001",
    "CrossModal-Poster-OCR-ReferenceOnly-001",
)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--closure-root", required=True)
    ap.add_argument("--verifier-output-root", default="")
    args = ap.parse_args()

    root = Path(args.closure_root).expanduser().resolve()
    vout = (
        Path(args.verifier_output_root).expanduser().resolve()
        if args.verifier_output_root.strip()
        else (root.parent / "poster_testboard_track_b_closure_verify_v0").resolve()
    )
    vout.mkdir(parents=True, exist_ok=True)

    blockers: List[str] = []

    def req(name: str) -> Path:
        p = root / name
        if not p.is_file():
            blockers.append(f"missing:{name}")
        return p

    sum_p = req("poster_testboard_track_b_closure_summary.json")
    pm_p = req("poster_testboard_track_b_phase_matrix.json")
    lin_p = req("poster_testboard_track_b_lineage_matrix.json")
    sep_p = req("poster_testboard_track_b_track_separation_report.json")
    bnd_p = req("poster_testboard_track_b_no_write_boundary_matrix.json")
    cap_p = req("poster_testboard_track_b_capability_closure_report.json")
    nc_p = req("poster_testboard_track_b_non_claims_report.json")
    fu_p = req("poster_testboard_track_b_open_followups.json")
    met_p = req("poster_testboard_track_b_metrics_snapshot_report.json")
    sim_p = req("poster_testboard_track_b_simulation_context_report.json")
    aud_p = req("poster_testboard_track_b_closure_audit_report.json")

    if blockers:
        verdict = "NO_GO"
        rep = {
            "schema": "poster_testboard_track_b_closure_verifier_report_v0",
            "phase": "Poster-TestBoard-Closure-001",
            "verdict": verdict,
            "closure_root": str(root),
            "verifier_output_root": str(vout),
            "blockers": sorted(set(blockers)),
        }
        _write_json(vout / "poster_testboard_track_b_closure_verifier_report.json", rep)
        print(json.dumps({"verifier_output_root": str(vout), "verdict": verdict, "blockers": blockers}, ensure_ascii=False))
        return 2

    sm = _read_json(sum_p)
    if sm.get("track_status") != "closed_for_evaluation":
        blockers.append("track_status_not_closed_for_evaluation")
    if sm.get("phase_count") != 4:
        blockers.append("phase_count_not_4")
    if sm.get("all_required_phases_go") is not True:
        blockers.append("all_required_phases_go_not_true")
    for k, val in (
        ("full_image_ocr_allowed", False),
        ("ocr_strategy", "segment_first"),
        ("reference_status", "reference_only"),
    ):
        if sm.get(k) != val:
            blockers.append(f"summary_{k}_wrong")

    pm = _read_json(pm_p)
    rows = {r.get("phase_name"): r for r in (pm.get("rows") or []) if isinstance(r, dict)}
    for pname in REQUIRED_PHASES:
        if pname not in rows:
            blockers.append(f"phase_matrix_missing:{pname}")
            continue
        r = rows[pname]
        if r.get("verifier_verdict") != "GO":
            blockers.append(f"phase_verdict_not_go:{pname}")
        if r.get("blockers"):
            blockers.append(f"phase_blockers_nonempty:{pname}")

    lin = _read_json(lin_p)
    for k, val in (
        ("text_region_count", 4),
        ("visual_symbol_region_count", 4),
        ("planned_ocr_region_count", 4),
        ("visual_symbol_item_count", 4),
        ("reference_candidate_count", 1),
    ):
        if lin.get(k) != val:
            blockers.append(f"lineage_{k}_not_{val}")

    sep = _read_json(sep_p)
    for k, val in (
        ("overlap_count", 0),
        ("visual_regions_in_ocr_plan", False),
        ("logo_qr_in_text_plan", False),
        ("semantic_join_allowed", False),
    ):
        if sep.get(k) is not val:
            blockers.append(f"separation_{k}_wrong")

    bnd = _read_json(bnd_p)
    if bnd.get("boundary_ok") is not True:
        blockers.append("boundary_ok_not_true")
    if bnd.get("violations"):
        blockers.append("boundary_violations_nonempty")

    nc = _read_json(nc_p)
    for flag in ("no_real_poster_ocr_claim", "no_qr_decode_claim", "no_brand_identity_claim"):
        if nc.get(flag) is not True:
            blockers.append(f"non_claims_{flag}_not_true")

    sim = _read_json(sim_p)
    if sim.get("simulation_profile_id") != "developer_full":
        blockers.append("simulation_profile_id_not_developer_full")
    if sim.get("run_model") is not False:
        blockers.append("simulation_run_model_not_false")

    audit = _read_json(aud_p)
    audit_checks = (
        ("ocr_invoked", False),
        ("qr_decoder_invoked", False),
        ("brand_database_invoked", False),
        ("visual_symbol_registry_invoked", False),
        ("fusion_invoked", False),
        ("semantic_join_invoked", False),
        ("midplatform_fact_written", False),
        ("scene_delta_written", False),
        ("world_model_written", False),
        ("navigation_decision_invoked", False),
        ("runtime_routing_changed", False),
    )
    for k, val in audit_checks:
        if audit.get(k) is not val:
            blockers.append(f"audit_{k}_wrong")

    verdict = "NO_GO" if blockers else "GO"
    rep = {
        "schema": "poster_testboard_track_b_closure_verifier_report_v0",
        "phase": "Poster-TestBoard-Closure-001",
        "verdict": verdict,
        "closure_root": str(root),
        "verifier_output_root": str(vout),
        "blockers": sorted(set(blockers)),
    }
    _write_json(vout / "poster_testboard_track_b_closure_verifier_report.json", rep)
    print(json.dumps({"verifier_output_root": str(vout), "verdict": verdict, "blockers": rep["blockers"]}, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
