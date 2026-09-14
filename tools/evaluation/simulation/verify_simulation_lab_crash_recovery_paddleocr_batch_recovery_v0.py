#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase-SimulationLab-CrashRecovery-PaddleOCR-BatchRecovery-001 verifier."""

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


CONTRACT_FIELDS = (
    "exit_code",
    "signal",
    "batch_size",
    "failed_sample_refs",
)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--phase-root", required=True)
    ap.add_argument("--verifier-output-root", default="")
    args = ap.parse_args()

    root = Path(args.phase_root).expanduser().resolve()
    vout = (
        Path(args.verifier_output_root).expanduser().resolve()
        if args.verifier_output_root.strip()
        else (root.parent / "simulation_lab_crash_recovery_paddleocr_batch_recovery_verify_v0").resolve()
    )
    vout.mkdir(parents=True, exist_ok=True)

    blockers: List[str] = []

    def req(name: str) -> Path:
        p = root / name
        if not p.is_file():
            blockers.append(f"missing:{name}")
        return p

    sum_p = req("simulation_lab_crash_recovery_paddleocr_batch_recovery_summary.json")
    contract_p = req("simulation_lab_crash_recovery_paddleocr_contract.json")
    cmd_p = root / "simulation_lab_crash_recovery_paddleocr_child_command_suggestion.md"
    if not cmd_p.is_file():
        blockers.append("missing:child_command_suggestion")
    merge_p = req("simulation_lab_crash_recovery_paddleocr_child_summary_merge_report.json")
    class_p = req("simulation_lab_crash_recovery_paddleocr_crash_signal_classification_report.json")
    action_p = req("simulation_lab_crash_recovery_paddleocr_recovery_action_matrix.json")
    merged_p = req("simulation_lab_crash_recovery_paddleocr_merged_simulation_summary.json")
    rv_p = req("simulation_lab_crash_recovery_paddleocr_real_values_link_report.json")
    bnd_p = req("simulation_lab_crash_recovery_paddleocr_boundary_report.json")
    nc_p = req("simulation_lab_crash_recovery_paddleocr_non_claims_report.json")
    fu_p = req("simulation_lab_crash_recovery_paddleocr_open_followups.json")
    aud_p = req("simulation_lab_crash_recovery_paddleocr_audit_report.json")

    if not blockers:
        sm = _read_json(sum_p)
        for k, val in (
            ("simulation_profile_id", "crash_recovery"),
            ("run_model_default", False),
            ("child_execution_invoked_by_this_phase", False),
            ("ocr_accuracy_evaluated", False),
            ("provider_comparison_claimed", False),
            ("benchmark_result_claimed", False),
        ):
            if sm.get(k) != val:
                blockers.append(f"summary_{k}_wrong")

        contract = _read_json(contract_p)
        for f in CONTRACT_FIELDS:
            if f not in contract and f not in (contract.get("field_descriptions") or {}):
                if f not in contract:
                    blockers.append(f"contract_missing_{f}")
        template = contract
        for f in ("exit_code", "signal", "batch_size", "failed_sample_refs", "rss_peak_mb"):
            if f not in template:
                blockers.append(f"contract_field_absent:{f}")

        if cmd_p.is_file():
            text = cmd_p.read_text(encoding="utf-8")
            if "run_paddleocr_labeled_set_batch_recovery_v0.py" not in text:
                blockers.append("command_suggestion_missing_runner")
            if "--execute-child" in text.lower():
                blockers.append("command_auto_execute_forbidden")

        merge = _read_json(merge_p)
        if merge.get("child_summary_provided"):
            if merge.get("required_fields_present") is not True:
                blockers.append("merge_required_fields_not_present")
            if merge.get("simulation_profile_id_matches") is not True:
                blockers.append("merge_profile_mismatch")

        cls = _read_json(class_p)
        rules = cls.get("classification_rules") or []
        has_139 = any(
            isinstance(r, dict) and ("139" in str(r.get("condition", "")) or r.get("classified_as") == "SIGSEGV")
            for r in rules
        )
        if not has_139:
            blockers.append("classification_rule_139_sigsegv_missing")

        action = _read_json(action_p)
        for row in action.get("rows") or []:
            if row.get("routing_changed") is not False:
                blockers.append("action_matrix_routing_changed")

        bnd = _read_json(bnd_p)
        if bnd.get("boundary_ok") is not True:
            blockers.append("boundary_not_ok")
        if bnd.get("violations"):
            blockers.append("boundary_violations_non_empty")

        rv = _read_json(rv_p)
        if rv.get("current_phase_updates_t2_values") is not False:
            blockers.append("rv_updates_t2_wrong")
        if rv.get("benchmark_score_generated") is not False:
            blockers.append("benchmark_score_generated_wrong")

        nc = _read_json(nc_p)
        if nc.get("not_provider_superiority") is not True:
            blockers.append("non_claims_provider_missing")

        aud = _read_json(aud_p)
        if aud.get("child_execution_invoked_by_this_phase") is not False:
            blockers.append("audit_child_execution_invoked")
        for k in (
            "ocr_routing_changed",
            "runtime_routing_changed",
            "midplatform_fact_written",
            "scene_delta_written",
            "world_model_written",
            "navigation_decision_invoked",
        ):
            if aud.get(k) is not False:
                blockers.append(f"audit_{k}_wrong")

        if not (_read_json(fu_p).get("items") or []):
            blockers.append("open_followups_empty")

    verdict = "GO" if not blockers else "NO_GO"
    if not blockers:
        sm = _read_json(sum_p)
        if sm.get("child_summary_provided") is not True and sm.get("recovery_status") == "pending_child_execution":
            verdict = "GO"

    report: Dict[str, Any] = {
        "schema": "simulation_lab_crash_recovery_paddleocr_verifier_report_v0",
        "phase": "SimulationLab-CrashRecovery-PaddleOCR-BatchRecovery-001",
        "phase_root": str(root),
        "verdict": verdict,
        "blockers": blockers,
        "verifier_output_root": str(vout),
    }
    _write_json(vout / "simulation_lab_crash_recovery_paddleocr_verifier_report.json", report)
    print(json.dumps({"verdict": verdict, "blockers": blockers, "verifier_output_root": str(vout)}, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
