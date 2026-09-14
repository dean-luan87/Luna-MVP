#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase-CrossModal-Vision-OCR-TestBoard-v1-Track-Closures-001 verifier."""

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


REQUIRED_SOURCES = (
    "v1_planning",
    "poster_track_b_closure",
    "metrics_schema",
    "metrics_collector",
    "realvideo_case_registry",
    "realvideo_frame_sample",
    "realvideo_roi_to_ocr_reference",
    "regression_comparison",
    "simulation_lab_minimal_harness",
)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--closures-root", required=True)
    ap.add_argument("--verifier-output-root", default="")
    args = ap.parse_args()

    root = Path(args.closures_root).expanduser().resolve()
    vout = (
        Path(args.verifier_output_root).expanduser().resolve()
        if args.verifier_output_root.strip()
        else (root.parent / "cross_modal_vision_ocr_testboard_v1_track_closures_verify_v0").resolve()
    )
    vout.mkdir(parents=True, exist_ok=True)

    blockers: List[str] = []

    def req(name: str) -> Path:
        p = root / name
        if not p.is_file():
            blockers.append(f"missing:{name}")
        return p

    sum_p = req("cross_modal_vision_ocr_testboard_v1_track_closures_summary.json")
    tm_p = req("cross_modal_vision_ocr_testboard_v1_track_closure_matrix.json")
    src_p = req("cross_modal_vision_ocr_testboard_v1_track_closures_source_phase_matrix.json")
    bnd_p = req("cross_modal_vision_ocr_testboard_v1_track_closures_boundary_matrix.json")
    cov_p = req("cross_modal_vision_ocr_testboard_v1_coverage_closure_report.json")
    cap_p = req("cross_modal_vision_ocr_testboard_v1_capability_closure_report.json")
    car_p = req("cross_modal_vision_ocr_testboard_v1_regression_carryover_report.json")
    risk_p = req("cross_modal_vision_ocr_testboard_v1_regression_risk_report.json")
    nc_p = req("cross_modal_vision_ocr_testboard_v1_non_claims_report.json")
    fu_p = req("cross_modal_vision_ocr_testboard_v1_open_followups.json")
    met_p = req("cross_modal_vision_ocr_testboard_v1_metrics_track_c_closure_report.json")
    rv_p = req("cross_modal_vision_ocr_testboard_v1_realvideo_track_a_closure_report.json")
    post_p = req("cross_modal_vision_ocr_testboard_v1_poster_track_b_closure_link_report.json")
    sim_p = req("cross_modal_vision_ocr_testboard_v1_track_closures_simulation_context_report.json")
    aud_p = req("cross_modal_vision_ocr_testboard_v1_track_closures_audit_report.json")

    if not blockers:
        sm = _read_json(sum_p)
        for k, val in (
            ("closure_scope", "evaluation_track_closure"),
            ("v1_status", "closed_for_evaluation"),
            ("track_a_realvideo_status", "closed_for_reference_evaluation"),
            ("track_b_poster_status", "closed_for_evaluation"),
            ("track_c_metrics_status", "closed_for_smoke_metrics"),
        ):
            if sm.get(k) != val:
                blockers.append(f"summary_{k}_wrong")
        for k, val in (("benchmark_result_claimed", False), ("production_readiness_claimed", False)):
            if sm.get(k) is not val:
                blockers.append(f"summary_{k}_wrong")

        tm = _read_json(tm_p)
        by_track = {r.get("track_name"): r for r in (tm.get("rows") or []) if isinstance(r, dict)}
        for tname in ("Track A RealVideo", "Track B Poster", "Track C Metrics"):
            if tname not in by_track:
                blockers.append(f"track_missing:{tname}")
            elif not by_track[tname].get("all_required_phases_go"):
                blockers.append(f"track_not_all_go:{tname}")

        src = _read_json(src_p)
        by_src = {r.get("source_name"): r for r in (src.get("rows") or []) if isinstance(r, dict)}
        for name in REQUIRED_SOURCES:
            if name not in by_src:
                blockers.append(f"source_missing:{name}")
            elif by_src[name].get("source_status") != "ok":
                blockers.append(f"source_status:{name}")

        bnd = _read_json(bnd_p)
        if bnd.get("boundary_ok") is not True:
            blockers.append("boundary_ok_not_true")
        if bnd.get("violations"):
            blockers.append("boundary_violations_nonempty")

        cov = _read_json(cov_p)
        if cov.get("v0_case_count") != 10:
            blockers.append("v0_case_count_not_10")
        if int(cov.get("v1_realvideo_case_count") or 0) < 16:
            blockers.append("v1_realvideo_case_count_lt_16")
        if int(cov.get("frame_sample_count") or 0) < 1:
            blockers.append("frame_sample_count_lt_1")
        if int(cov.get("roi_reference_count") or 0) < 1:
            blockers.append("roi_reference_count_lt_1")
        if int(cov.get("ocr_request_reference_count") or 0) < 1:
            blockers.append("ocr_request_reference_count_lt_1")

        cap = _read_json(cap_p)
        if "realvideo_ocr_execution" not in (cap.get("not_completed") or []):
            blockers.append("capability_missing_realvideo_ocr_not_completed")

        car = _read_json(car_p)
        if car.get("all_boundary_ok") is not True:
            blockers.append("carryover_all_boundary_ok_not_true")
        for k, val in (
            ("write_capability_added", False),
            ("production_readiness_added", False),
            ("no_write_boundary_regression", False),
            ("routing_regression", False),
            ("benchmark_claim_regression", False),
        ):
            if car.get(k) is not val:
                blockers.append(f"carryover_{k}_wrong")

        met = _read_json(met_p)
        if met.get("benchmark_result_claimed") is not False:
            blockers.append("metrics_benchmark_claimed_not_false")

        rv = _read_json(rv_p)
        for k, val in (
            ("ocr_request_submitted", False),
            ("ocr_evidence_generated", False),
        ):
            if rv.get(k) is not val:
                blockers.append(f"realvideo_{k}_wrong")

        post = _read_json(post_p)
        if post.get("poster_track_b_closed") is not True:
            blockers.append("poster_track_b_closed_not_true")
        if post.get("real_poster_ocr_claim") is not False:
            blockers.append("real_poster_ocr_claim_not_false")

        risk = _read_json(risk_p)
        for k, val in (
            ("no_write_boundary_regression", False),
            ("routing_regression", False),
            ("benchmark_claim_regression", False),
        ):
            if risk.get(k) is not val:
                blockers.append(f"risk_{k}_not_false")

        nc = _read_json(nc_p)
        if nc.get("no_benchmark_claim") is not True:
            blockers.append("non_claims_no_benchmark_not_true")
        if nc.get("no_production_readiness_claim") is not True:
            blockers.append("non_claims_no_production_not_true")

        sim = _read_json(sim_p)
        if sim.get("simulation_profile_id") != "developer_full":
            blockers.append("simulation_profile_id_not_developer_full")
        if sim.get("run_model") is not False:
            blockers.append("simulation_run_model_not_false")

        audit = _read_json(aud_p)
        audit_checks = (
            ("ocr_invoked", False),
            ("ocr_request_submitted", False),
            ("vision_provider_invoked", False),
            ("fusion_invoked", False),
            ("scene_delta_candidate_generated", False),
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
    rep: Dict[str, Any] = {
        "schema": "cross_modal_vision_ocr_testboard_v1_track_closures_verifier_report_v0",
        "phase": "CrossModal-Vision-OCR-TestBoard-v1-Track-Closures-001",
        "verdict": verdict,
        "closures_root": str(root),
        "verifier_output_root": str(vout),
        "blockers": sorted(set(blockers)),
    }
    _write_json(vout / "cross_modal_vision_ocr_testboard_v1_track_closures_verifier_report.json", rep)
    print(json.dumps({"verifier_output_root": str(vout), "verdict": verdict, "blockers": rep["blockers"]}, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
