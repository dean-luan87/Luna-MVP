#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase-CrossModal-Vision-OCR-TestBoard-Benchmark-Collector-Real-Values-Smoke-001 verifier."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List


def _read_json(p: Path) -> Any:
    return json.loads(p.read_text(encoding="utf-8"))


def _write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


REQUIRED_SOURCES = (
    "benchmark_planning",
    "v1_track_closures",
    "regression_comparison",
    "metrics_schema",
    "public_facility_runtime_dryrun",
    "poster_track_b_closure",
    "realvideo_roi_to_ocr_reference",
    "simulation_lab_developer_full",
)

T2_METRICS = (
    "text_recall_proxy",
    "provider_latency_ms",
    "per_case_latency_ms",
    "memory_peak_mb",
    "cpu_peak_percent",
    "crash_count",
    "timeout_count",
    "provider_error_count",
)

VIOLATION_METRICS = (
    "fact_write_violation_count",
    "scene_delta_write_violation_count",
    "world_model_write_violation_count",
    "navigation_decision_violation_count",
    "auto_approval_violation_count",
    "runtime_routing_violation_count",
)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke-root", required=True)
    ap.add_argument("--verifier-output-root", default="")
    args = ap.parse_args()

    root = Path(args.smoke_root).expanduser().resolve()
    vout = (
        Path(args.verifier_output_root).expanduser().resolve()
        if args.verifier_output_root.strip()
        else (root.parent / "cross_modal_vision_ocr_benchmark_real_values_smoke_verify_v0").resolve()
    )
    vout.mkdir(parents=True, exist_ok=True)

    blockers: List[str] = []

    def req(name: str) -> Path:
        p = root / name
        if not p.is_file():
            blockers.append(f"missing:{name}")
        return p

    sum_p = req("cross_modal_vision_ocr_benchmark_real_values_smoke_summary.json")
    vm_p = req("cross_modal_vision_ocr_benchmark_real_values_metric_value_matrix.json")
    src_p = req("cross_modal_vision_ocr_benchmark_real_values_source_artifact_matrix.json")
    miss_p = req("cross_modal_vision_ocr_benchmark_real_values_missing_metric_report.json")
    bnd_p = req("cross_modal_vision_ocr_benchmark_real_values_boundary_metrics_report.json")
    func_p = req("cross_modal_vision_ocr_benchmark_real_values_functional_smoke_report.json")
    qual_p = req("cross_modal_vision_ocr_benchmark_real_values_quality_performance_placeholder_report.json")
    guard_p = req("cross_modal_vision_ocr_benchmark_real_values_interpretation_guard_report.json")
    car_p = req("cross_modal_vision_ocr_benchmark_real_values_regression_carryover_report.json")
    sim_p = req("cross_modal_vision_ocr_benchmark_real_values_simulation_context_report.json")
    nc_p = req("cross_modal_vision_ocr_benchmark_real_values_non_claims_report.json")
    fu_p = req("cross_modal_vision_ocr_benchmark_real_values_open_followups.json")
    aud_p = req("cross_modal_vision_ocr_benchmark_real_values_smoke_audit_report.json")

    if not blockers:
        sm = _read_json(sum_p)
        for k, val in (
            ("collection_scope", "readonly_real_values_smoke"),
            ("real_values_collected", True),
            ("t0_boundary_values_collected", True),
            ("t1_functional_values_collected", True),
            ("t2_quality_performance_values_collected", False),
            ("benchmark_result_claimed", False),
            ("model_selection_claimed", False),
        ):
            if sm.get(k) != val:
                blockers.append(f"summary_{k}_wrong")

        vm = _read_json(vm_p)
        by_name = {r.get("metric_name"): r for r in vm.get("rows") or [] if isinstance(r, dict)}
        nwp = by_name.get("no_write_boundary_pass_rate")
        if not nwp or nwp.get("value") != 1.0:
            blockers.append("no_write_boundary_pass_rate_not_1")
        for vn in VIOLATION_METRICS:
            row = by_name.get(vn)
            if not row or row.get("value") != 0:
                blockers.append(f"{vn}_not_zero")
        for tn in T2_METRICS:
            row = by_name.get(tn)
            if not row or row.get("collection_status") != "not_collected":
                blockers.append(f"t2_{tn}_not_not_collected")

        src = _read_json(src_p)
        for sname in REQUIRED_SOURCES:
            rows = [r for r in src.get("rows") or [] if r.get("source_name") == sname]
            if not rows or rows[0].get("artifact_read_ok") is not True:
                blockers.append(f"source_not_ok:{sname}")

        miss = _read_json(miss_p)
        for entry in miss.get("entries") or []:
            if entry.get("tier") == "T2" and entry.get("is_blocker"):
                blockers.append("t2_missing_marked_blocker")

        bnd = _read_json(bnd_p)
        if bnd.get("boundary_status") != "pass":
            blockers.append("boundary_status_not_pass")

        func = _read_json(func_p)
        for k, val in (
            ("public_facility_candidate_count", 6),
            ("public_facility_correction_candidate_count", 3),
            ("poster_text_region_count", 4),
            ("poster_visual_symbol_region_count", 4),
        ):
            if func.get(k) != val:
                blockers.append(f"functional_{k}_wrong")
        if (func.get("realvideo_roi_reference_count") or 0) < 50:
            blockers.append("realvideo_roi_reference_count_lt_50")
        if (func.get("realvideo_ocr_request_reference_count") or 0) < 10:
            blockers.append("realvideo_ocr_request_reference_count_lt_10")

        qual = _read_json(qual_p)
        if qual.get("benchmark_score") is not None:
            blockers.append("benchmark_score_not_null")
        if qual.get("benchmark_claim_allowed") is not False:
            blockers.append("benchmark_claim_allowed_not_false")

        guard = _read_json(guard_p)
        if guard.get("empty_text_not_always_failure") is not True:
            blockers.append("guard_empty_text_missing")
        if guard.get("provider_distribution_not_model_selection") is not True:
            blockers.append("guard_provider_distribution_missing")

        car = _read_json(car_p)
        if car.get("v1_track_closures_status") != "closed_for_evaluation":
            blockers.append("carryover_v1_status_wrong")

        sim = _read_json(sim_p)
        if sim.get("simulation_profile_id") != "developer_full":
            blockers.append("sim_profile_wrong")
        if sim.get("run_model") is not False:
            blockers.append("sim_run_model_not_false")

        nc = _read_json(nc_p)
        if nc.get("not_benchmark_phase") is not True:
            blockers.append("non_claims_not_benchmark_missing")

        if not (_read_json(fu_p).get("items") or []):
            blockers.append("open_followups_empty")

        aud = _read_json(aud_p)
        for k, val in (
            ("ocr_invoked", False),
            ("ocr_request_submitted", False),
            ("vision_provider_invoked", False),
            ("t2_quality_performance_values_collected", False),
            ("provider_comparison_claimed", False),
            ("midplatform_fact_written", False),
            ("scene_delta_written", False),
            ("world_model_written", False),
            ("navigation_decision_invoked", False),
            ("runtime_routing_changed", False),
        ):
            if aud.get(k) != val:
                blockers.append(f"audit_{k}_wrong")

    verdict = "GO" if not blockers else "NO_GO"
    report: Dict[str, Any] = {
        "schema": "cross_modal_vision_ocr_benchmark_real_values_smoke_verifier_report_v0",
        "phase": "CrossModal-Vision-OCR-TestBoard-Benchmark-Collector-Real-Values-Smoke-001",
        "smoke_root": str(root),
        "verdict": verdict,
        "blockers": blockers,
        "verifier_output_root": str(vout),
    }
    _write_json(vout / "cross_modal_vision_ocr_benchmark_real_values_smoke_verifier_report.json", report)
    print(json.dumps({"verdict": verdict, "blockers": blockers, "verifier_output_root": str(vout)}, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
