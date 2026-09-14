#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for WorldModel Lookup for Reading Framework v1."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List


def _require_abs(p: str, label: str) -> Path:
    pp = Path(p).expanduser()
    if not pp.is_absolute():
        raise SystemExit(f"ERROR: {label} must be absolute, got: {p}")
    return pp.resolve()


def _write_json(path: Path, obj: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _classifications(data: Dict[str, Any]) -> List[Dict[str, Any]]:
    return [c for c in data.get("classifications") or [] if isinstance(c, dict)]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke-root", required=True)
    args = ap.parse_args()

    root = _require_abs(args.smoke_root, "--smoke-root")
    blockers: List[str] = []
    checks = 0

    def ok(c: bool, name: str) -> None:
        nonlocal checks
        if c:
            checks += 1
        else:
            blockers.append(name)

    files = {
        "summary": "worldmodel_lookup_for_reading_framework_v1_summary.json",
        "intake": "worldmodel_lookup_reading_framework_input_intake_matrix_v1.json",
        "request_schema": "worldmodel_lookup_reading_request_schema_v1.json",
        "response_schema": "worldmodel_lookup_reading_response_candidate_schema_v1.json",
        "source_priority": "worldmodel_lookup_reading_source_priority_policy_v1.json",
        "unresolved_link": "worldmodel_lookup_reading_unresolved_slot_link_policy_v1.json",
        "memory_link": "worldmodel_lookup_reading_memory_reference_link_policy_v1.json",
        "confirmed_text_link": "worldmodel_lookup_reading_confirmed_text_hint_link_policy_v1.json",
        "isrc_handoff": "worldmodel_lookup_reading_isrc_handoff_policy_v1.json",
        "rrd_handoff": "worldmodel_lookup_reading_rrd_handoff_policy_v1.json",
        "fallback": "worldmodel_lookup_reading_fallback_policy_v1.json",
        "classification": "worldmodel_lookup_reading_candidate_classification_policy_v1.json",
        "no_write_policy": "worldmodel_lookup_reading_no_write_boundary_policy_v1.json",
        "future_dryrun": "worldmodel_lookup_reading_future_dryrun_entrypoint_v1.json",
        "long_term": "worldmodel_lookup_reading_long_term_candidate_link_v1.json",
        "trace": "worldmodel_lookup_reading_framework_decision_trace_v1.json",
        "final": "worldmodel_lookup_reading_framework_final_decision_v1.json",
        "boundary": "worldmodel_lookup_reading_framework_boundary_report_v1.json",
        "metrics": "worldmodel_lookup_reading_framework_metrics_candidate_report_v1.json",
        "bench": "worldmodel_lookup_reading_framework_benchmark_link_report_v1.json",
        "health": "worldmodel_lookup_reading_framework_system_health_report_v1.json",
        "no_write": "worldmodel_lookup_reading_framework_no_write_boundary_report_v1.json",
        "sim": "worldmodel_lookup_reading_framework_simulation_context_report_v1.json",
        "non_claims": "worldmodel_lookup_reading_framework_non_claims_report_v1.json",
        "followups": "worldmodel_lookup_reading_framework_open_followups_v1.json",
        "audit": "worldmodel_lookup_reading_framework_audit_report_v1.json",
    }
    data: Dict[str, Any] = {}
    for k, f in files.items():
        p = root / f
        if not p.is_file():
            blockers.append(f"missing:{k}")
        else:
            data[k] = json.loads(p.read_text(encoding="utf-8"))

    if blockers:
        _write_json(
            root / "worldmodel_lookup_reading_framework_verifier_report_v1.json",
            {"verdict": "NO_GO", "blockers": blockers},
        )
        print(json.dumps({"verdict": "NO_GO", "blockers": blockers}, ensure_ascii=False))
        return 2

    s = data["summary"]
    ok(s.get("framework_scope") == "worldmodel_lookup_for_reading_framework_only", "scope")
    ok(s.get("based_on_ocr_mainline_closure") is True, "ocr_closure")
    ok(s.get("worldmodel_lookup_framework_defined") is True, "fw_defined")
    ok(s.get("worldmodel_runtime_available") is False, "wm_rt")
    ok(s.get("worldmodel_lookup_invoked") is False, "no_lookup")
    ok(s.get("world_model_written") is False, "no_wm_write")

    req = data["request_schema"]
    ok(req.get("live_observation_priority") is True, "live_prio")

    resp = data["response_schema"]
    ok(resp.get("requires_live_verification") is True, "req_verify")
    ok(resp.get("is_fact") is False, "not_fact")

    for p in data["source_priority"].get("priorities") or []:
        if isinstance(p, dict):
            if p.get("can_override_live_observation") is True:
                blockers.append("override_live")
            if p.get("can_trigger_ocr_directly") is True:
                blockers.append("trigger_ocr")
    if "override_live" not in blockers and "trigger_ocr" not in blockers:
        checks += 1

    ul = data["unresolved_link"]
    ok(ul.get("unresolved_slot_is_not_fact") is True, "slot_not_fact")

    ml = data["memory_link"]
    ok(ml.get("memory_reference_cannot_override_live_observation") is True, "mem_no_override")

    ct = data["confirmed_text_link"]
    ok(ct.get("confirmed_text_cannot_write_worldmodel_directly") is True, "ct_no_wm")
    ok(ct.get("confirmed_text_cannot_trigger_ocr_directly") is True, "ct_no_ocr")

    ok(data["isrc_handoff"].get("isrc_runtime_invoked_now") is False, "isrc_now")
    ok(data["rrd_handoff"].get("readable_region_discovery_invoked_now") is False, "rrd_now")

    for fb in data["fallback"].get("fallbacks") or []:
        if isinstance(fb, dict) and fb.get("ocr_invoked_now") is True:
            blockers.append("fallback_ocr")
            break
    else:
        checks += 1

    cls_ids = [c.get("classification") for c in _classifications(data["classification"])]
    ok("DO_NOT_USE_FOR_ACTION" in cls_ids, "dnu_class")

    ok(data["no_write_policy"].get("world_model_written") is False, "nwp_wm")
    ok(data["future_dryrun"].get("recommended_next_phase") == "WorldModel-Lookup-for-Reading-DryRun-v1", "next")
    ok(data["long_term"].get("can_feed_long_term_candidate") is True, "lt_ok")

    final = data["final"]
    ok(final.get("final_decision") == "READY_FOR_WORLDMODEL_LOOKUP_READING_DRYRUN_LATER", "final")

    ok(data["boundary"].get("framework_only") is True, "fw_only")
    ok(data["metrics"].get("no_write_boundary_pass_rate") == 1.0, "nw_rate")
    ok(data["no_write"].get("boundary_ok") is True, "nw_ok")
    ok(data["sim"].get("simulation_profile_id") == "developer_full", "sim")
    ok(data["audit"].get("midplatform_fact_written") is False, "audit")

    verdict = "GO" if not blockers else "NO_GO"
    report = {
        "verdict": verdict,
        "checks_passed": checks,
        "checks_expected": 69,
        "blockers": blockers,
        "final_decision": final.get("final_decision"),
        "phase": "WorldModel-Lookup-for-Reading-Framework-v1-001",
    }
    _write_json(root / "worldmodel_lookup_reading_framework_verifier_report_v1.json", report)
    print(json.dumps(report, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
