#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase-SystemHealthCenter-Governance-001 verifier."""

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
    ap.add_argument("--governance-root", required=True)
    ap.add_argument("--verifier-output-root", default="")
    args = ap.parse_args()

    root = Path(args.governance_root).expanduser().resolve()
    vout = (
        Path(args.verifier_output_root).expanduser().resolve()
        if args.verifier_output_root.strip()
        else (root.parent / "system_health_center_governance_verify_v0").resolve()
    )
    vout.mkdir(parents=True, exist_ok=True)

    blockers: List[str] = []

    def req(name: str) -> Path:
        p = root / name
        if not p.is_file():
            blockers.append(f"missing:{name}")
        return p

    sum_p = req("system_health_center_governance_summary.json")
    mod_p = req("system_health_module_health_report_schema.json")
    fc_p = req("system_health_failure_class_enum.json")
    ra_p = req("system_health_recovery_action_enum.json")
    om_p = req("system_health_operating_mode_enum.json")
    mask_p = req("system_health_capability_mask_schema.json")
    agg_p = req("system_health_aggregation_policy.json")
    rec_p = req("system_health_recovery_decision_policy.json")
    sim_p = req("system_health_simulation_lab_link_report.json")
    ex_p = req("system_health_example_module_reports.json")
    bnd_p = req("system_health_governance_boundary_report.json")
    snap_p = req("system_health_snapshot_schema.json")
    plan_p = req("system_health_recovery_action_plan_schema.json")
    wb_p = req("system_health_whitebox_audit_link_policy.json")
    nc_p = req("system_health_governance_non_claims_report.json")
    fu_p = req("system_health_governance_open_followups.json")
    aud_p = req("system_health_governance_audit_report.json")

    if not blockers:
        sm = _read_json(sum_p)
        for k, val in (
            ("governance_scope", "contract_only"),
            ("runtime_execution", False),
            ("recovery_action_committed", False),
            ("routing_changed", False),
        ):
            if sm.get(k) != val:
                blockers.append(f"summary_{k}_wrong")

        mod = _read_json(mod_p)
        hs = set(mod.get("health_status_enum") or [])
        for s in ("HEALTHY", "WARNING", "DEGRADED", "FAILED", "QUARANTINED"):
            if s not in hs:
                blockers.append(f"missing_health_status:{s}")

        fc = _read_json(fc_p)
        fc_set = {x.get("failure_class") for x in fc.get("failure_classes") or []}
        for f in ("SIGSEGV", "OOM", "TIMEOUT", "DEADLINE_MISS", "VOICE_NOTICE_EXPIRED", "FRAME_DELAY"):
            if f not in fc_set:
                blockers.append(f"missing_failure_class:{f}")

        ra = _read_json(ra_p)
        act_set = {x.get("action_id") for x in ra.get("actions") or []}
        for a in ("RETRY", "REDUCE_BATCH_SIZE", "FALLBACK_PROVIDER", "QUARANTINE_PROVIDER", "SAFE_FREEZE"):
            if a not in act_set:
                blockers.append(f"missing_recovery_action:{a}")

        om = _read_json(om_p)
        mode_set = {x.get("mode") for x in om.get("modes") or []}
        for m in ("NORMAL", "DEGRADED", "MINIMUM_OPERATIONAL", "SAFE_FREEZE", "RECOVERY_PENDING"):
            if m not in mode_set:
                blockers.append(f"missing_operating_mode:{m}")

        mask = _read_json(mask_p)
        ex = mask.get("example") or {}
        if ex.get("scene_delta", {}).get("write_allowed") is not False:
            blockers.append("mask_scene_delta_write_not_false")
        if ex.get("world_model", {}).get("write_allowed") is not False:
            blockers.append("mask_world_model_write_not_false")
        if ex.get("navigation", {}).get("decision_allowed") is not False:
            blockers.append("mask_navigation_decision_not_false")

        rec = _read_json(rec_p)
        pol = rec.get("policies") or {}
        if "paddleocr_sigsegv" not in pol:
            blockers.append("missing_paddleocr_sigsegv_rule")
        if "voice_notice_expired" not in pol:
            blockers.append("missing_voice_notice_expired_rule")
        if "vision_frame_delay" not in pol:
            blockers.append("missing_vision_frame_delay_rule")

        sim = _read_json(sim_p)
        crash = next((p for p in sim.get("profiles") or [] if p.get("simulation_profile_id") == "crash_recovery"), None)
        if not crash or "SIGSEGV" not in (crash.get("failure_classes") or []):
            blockers.append("crash_recovery_sigsegv_mapping_missing")
        stcm = next((p for p in sim.get("profiles") or [] if p.get("simulation_profile_id") == "stcm_deadline_stress"), None)
        if not stcm or "DEADLINE_MISS" not in (stcm.get("failure_classes") or []):
            blockers.append("stcm_deadline_mapping_missing")
        voice = next((p for p in sim.get("profiles") or [] if p.get("simulation_profile_id") == "voice_notice_expiry"), None)
        if not voice or "VOICE_NOTICE_EXPIRED" not in (voice.get("failure_classes") or []):
            blockers.append("voice_notice_expiry_mapping_missing")

        examples = _read_json(ex_p)
        if (examples.get("example_count") or 0) < 6:
            blockers.append("example_count_lt_6")

        bnd = _read_json(bnd_p)
        if bnd.get("health_center_does_not_replace_gate") is not True:
            blockers.append("boundary_gate_replacement_not_denied")

        plan = _read_json(plan_p)
        if plan.get("action_commit_status_default") != "planned_only":
            blockers.append("plan_commit_status_default_wrong")

        nc = _read_json(nc_p)
        if nc.get("not_runtime_health_center") is not True:
            blockers.append("non_claims_no_runtime_missing")
        if nc.get("no_crash_recovery_verified_claim") is not True:
            blockers.append("non_claims_no_crash_recovery_verified_missing")

        if not (_read_json(fu_p).get("items") or []):
            blockers.append("open_followups_empty")

        aud = _read_json(aud_p)
        for k, val in (
            ("module_restart_invoked", False),
            ("recovery_action_committed", False),
            ("ocr_invoked", False),
            ("vision_provider_invoked", False),
            ("voice_runtime_invoked", False),
            ("taskchain_modified", False),
            ("routing_changed", False),
            ("midplatform_fact_written", False),
            ("scene_delta_written", False),
            ("world_model_written", False),
            ("navigation_decision_invoked", False),
        ):
            if aud.get(k) != val:
                blockers.append(f"audit_{k}_wrong")

    verdict = "GO" if not blockers else "NO_GO"
    report: Dict[str, Any] = {
        "schema": "system_health_governance_verifier_report_v0",
        "phase": "SystemHealthCenter-Governance-001",
        "governance_root": str(root),
        "verdict": verdict,
        "blockers": blockers,
        "verifier_output_root": str(vout),
    }
    _write_json(vout / "system_health_governance_verifier_report.json", report)
    print(json.dumps({"verdict": verdict, "blockers": blockers, "verifier_output_root": str(vout)}, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
