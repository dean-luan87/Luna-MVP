#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase-CrossModal-Vision-OCR-TestBoard-Benchmark-Collector-Real-Values-Planning-001 verifier."""

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


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--planning-root", required=True)
    ap.add_argument("--verifier-output-root", default="")
    args = ap.parse_args()

    root = Path(args.planning_root).expanduser().resolve()
    vout = (
        Path(args.verifier_output_root).expanduser().resolve()
        if args.verifier_output_root.strip()
        else (root.parent / "cross_modal_vision_ocr_benchmark_real_values_planning_verify_v0").resolve()
    )
    vout.mkdir(parents=True, exist_ok=True)

    blockers: List[str] = []

    def req(name: str) -> Path:
        p = root / name
        if not p.is_file():
            blockers.append(f"missing:{name}")
        return p

    sum_p = req("cross_modal_vision_ocr_benchmark_real_values_planning_summary.json")
    tier_p = req("cross_modal_vision_ocr_benchmark_metric_tier_matrix.json")
    src_p = req("cross_modal_vision_ocr_benchmark_real_values_source_map.json")
    gate_p = req("cross_modal_vision_ocr_benchmark_collector_gate_policy.json")
    interp_p = req("cross_modal_vision_ocr_benchmark_metric_interpretation_policy.json")
    gt_p = req("cross_modal_vision_ocr_benchmark_ground_truth_requirement_report.json")
    sim_p = req("cross_modal_vision_ocr_benchmark_simulation_profile_binding_plan.json")
    contract_p = req("cross_modal_vision_ocr_benchmark_real_values_collector_output_contract.json")
    reg_p = req("cross_modal_vision_ocr_benchmark_regression_link_report.json")
    nc_p = req("cross_modal_vision_ocr_benchmark_non_claims_report.json")
    fu_p = req("cross_modal_vision_ocr_benchmark_open_followups.json")
    aud_p = req("cross_modal_vision_ocr_benchmark_real_values_planning_audit_report.json")

    if not blockers:
        sm = _read_json(sum_p)
        for k, val in (
            ("planning_scope", "benchmark_real_values_planning_only"),
            ("runtime_execution", False),
            ("benchmark_values_collected", False),
            ("benchmark_result_claimed", False),
            ("model_selection_claimed", False),
            ("production_readiness_claimed", False),
        ):
            if sm.get(k) != val:
                blockers.append(f"summary_{k}_wrong")

        tier = _read_json(tier_p)
        tiers = {r.get("tier") for r in tier.get("rows") or [] if isinstance(r, dict)}
        for t in ("T0", "T1", "T2"):
            if t not in tiers:
                blockers.append(f"missing_tier:{t}")
        names = {r.get("metric_name") for r in tier.get("rows") or [] if isinstance(r, dict)}
        if "no_write_boundary_pass_rate" not in names:
            blockers.append("missing_metric:no_write_boundary_pass_rate")
        else:
            t0_rows = [r for r in tier.get("rows") or [] if r.get("metric_name") == "no_write_boundary_pass_rate"]
            if t0_rows and t0_rows[0].get("tier") != "T0":
                blockers.append("no_write_boundary_pass_rate_not_t0")
        if "text_recall_proxy" not in names:
            blockers.append("missing_metric:text_recall_proxy")
        else:
            t2_rows = [r for r in tier.get("rows") or [] if r.get("metric_name") == "text_recall_proxy"]
            if t2_rows and t2_rows[0].get("tier") != "T2":
                blockers.append("text_recall_proxy_not_t2")

        gate = _read_json(gate_p)
        for k, val in (
            ("real_values_collection_allowed", False),
            ("benchmark_claim_allowed", False),
            ("provider_comparison_allowed", False),
        ):
            if gate.get(k) != val:
                blockers.append(f"gate_{k}_wrong")

        interp = _read_json(interp_p)
        rules = interp.get("rules") or {}
        if rules.get("empty_text_not_always_failure") is not True:
            blockers.append("interp_empty_text_rule_missing")
        if rules.get("smoke_collector_not_provider_selection") is not True:
            blockers.append("interp_smoke_not_provider_selection_missing")

        gt = _read_json(gt_p)
        if gt.get("current_v1_has_ground_truth") is not False:
            blockers.append("gt_current_v1_has_ground_truth_not_false")
        tr_rows = [r for r in gt.get("rows") or [] if r.get("metric_name") == "text_recall_proxy"]
        if not tr_rows or tr_rows[0].get("requires_ground_truth") is not True:
            blockers.append("text_recall_proxy_requires_gt_not_true")

        sim = _read_json(sim_p)
        pids = {p.get("profile_id") for p in sim.get("profiles") or [] if isinstance(p, dict)}
        for pid in ("developer_full", "crash_recovery"):
            if pid not in pids:
                blockers.append(f"missing_profile:{pid}")

        contract = _read_json(contract_p)
        if contract.get("current_phase_generates_values") is not False:
            blockers.append("contract_current_phase_generates_values_not_false")

        reg = _read_json(reg_p)
        for k, val in (
            ("v1_track_closures_status", "closed_for_evaluation"),
            ("regression_all_boundary_ok", True),
            ("write_capability_added", False),
            ("production_readiness_added", False),
            ("benchmark_added", False),
        ):
            if reg.get(k) != val:
                blockers.append(f"regression_link_{k}_wrong")

        nc = _read_json(nc_p)
        if nc.get("not_benchmark_phase") is not True:
            blockers.append("non_claims_not_benchmark_missing")
        if nc.get("no_provider_comparison") is not True:
            blockers.append("non_claims_no_provider_comparison_missing")

        fu = _read_json(fu_p)
        if not (fu.get("items") or []):
            blockers.append("open_followups_empty")

        aud = _read_json(aud_p)
        for k, val in (
            ("ocr_invoked", False),
            ("ocr_request_submitted", False),
            ("vision_provider_invoked", False),
            ("benchmark_values_collected", False),
            ("model_selection_claimed", False),
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
        "schema": "cross_modal_vision_ocr_benchmark_real_values_planning_verifier_report_v0",
        "phase": "CrossModal-Vision-OCR-TestBoard-Benchmark-Collector-Real-Values-Planning-001",
        "planning_root": str(root),
        "verdict": verdict,
        "blockers": blockers,
        "verifier_output_root": str(vout),
    }
    _write_json(vout / "cross_modal_vision_ocr_benchmark_real_values_planning_verifier_report.json", report)
    print(json.dumps({"verdict": verdict, "blockers": blockers, "verifier_output_root": str(vout)}, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
