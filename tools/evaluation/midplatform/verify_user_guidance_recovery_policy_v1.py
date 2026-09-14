#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for User Guidance Recovery Policy v1."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import List


def _require_abs(p: str, label: str) -> Path:
    pp = Path(p).expanduser()
    if not pp.is_absolute():
        raise SystemExit(f"ERROR: {label} must be absolute, got: {p}")
    return pp.resolve()


def _write_json(path: Path, obj: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


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
        "summary": "user_guidance_recovery_policy_v1_summary.json",
        "readiness": "ocr_input_readiness_scope_v1.json",
        "activation": "ocr_activation_recovery_level_policy_v1.json",
        "criticality": "user_guidance_task_criticality_matrix_v1.json",
        "taxonomy": "ocr_input_failure_reason_taxonomy_v1.json",
        "repairability": "ocr_repairability_classification_policy_v1.json",
        "ug_actions": "user_guidance_action_candidate_policy_v1.json",
        "sys_actions": "system_self_adjustment_candidate_policy_v1.json",
        "ext_actions": "external_assistance_candidate_policy_v1.json",
        "not_worth": "ocr_not_recoverable_or_not_worth_policy_v1.json",
        "current": "user_guidance_current_case_recovery_decision_v1.json",
        "hardware": "ocr_guidance_hardware_placeholder_contract_v1.json",
        "stc": "ocr_guidance_stc_vision_capture_link_report_v1.json",
        "boundary": "user_guidance_recovery_boundary_report_v1.json",
        "metrics": "user_guidance_recovery_metrics_candidate_report_v1.json",
        "bench": "user_guidance_recovery_benchmark_link_report_v1.json",
        "health": "user_guidance_recovery_system_health_link_report_v1.json",
        "no_write": "user_guidance_recovery_no_write_boundary_report_v1.json",
        "sim": "user_guidance_recovery_simulation_context_report_v1.json",
        "non_claims": "user_guidance_recovery_non_claims_report_v1.json",
        "followups": "user_guidance_recovery_open_followups_v1.json",
        "audit": "user_guidance_recovery_audit_report_v1.json",
    }
    data = {}
    for k, f in files.items():
        p = root / f
        if not p.is_file():
            blockers.append(f"missing:{k}")
        else:
            data[k] = json.loads(p.read_text(encoding="utf-8"))

    if blockers:
        _write_json(
            root / "user_guidance_recovery_verifier_report_v1.json",
            {"verdict": "NO_GO", "checks_passed": 0, "blockers": blockers},
        )
        print(json.dumps({"verdict": "NO_GO", "blockers": blockers}, ensure_ascii=False))
        return 2

    s = data["summary"]
    readiness = data["readiness"]
    activation = data["activation"]
    criticality = data["criticality"]
    taxonomy = data["taxonomy"]
    repair = data["repairability"]
    ug = data["ug_actions"]
    sys_a = data["sys_actions"]
    ext = data["ext_actions"]
    not_worth = data["not_worth"]
    current = data["current"]
    hardware = data["hardware"]
    stc = data["stc"]
    boundary = data["boundary"]
    metrics = data["metrics"]
    bench = data["bench"]
    health = data["health"]
    no_write = data["no_write"]
    sim = data["sim"]
    audit = data["audit"]

    ok(True, "summary_exists")
    ok(s.get("policy_scope") == "user_guidance_recovery_policy_only", "scope")
    ok(s.get("based_on_ocr_v2_result") is True, "based_ocr_v2")
    ok(s.get("ocr_input_readiness_scope_defined") is True, "readiness_defined")
    ok(s.get("view_condition_scope_defined") is True, "view_scope")
    ok(s.get("distance_scope_defined") is True, "distance_scope")
    ok(s.get("region_localization_scope_defined") is True, "region_scope")
    ok(s.get("bbox_geometry_scope_defined") is True, "bbox_scope")
    ok(s.get("text_readability_scope_defined") is True, "readability_scope")
    ok(s.get("repairability_policy_defined") is True, "repair_defined")
    ok(s.get("hardware_control_placeholder_defined") is True, "hw_defined")
    ok(s.get("runtime_tts_invoked") is False, "no_tts")
    ok(s.get("runtime_guidance_action_committed") is False, "no_ug_action")
    ok(s.get("hardware_action_invoked") is False, "no_hw")

    ok(readiness.get("threshold_is_policy_placeholder") is True, "placeholder")
    ok("view_condition_scope" in readiness, "readiness_view")
    ok("distance_scope" in readiness, "readiness_distance")
    ok("region_localization_scope" in readiness, "readiness_region")
    ok("bbox_geometry_scope" in readiness, "readiness_bbox")
    ok("text_readability_scope" in readiness, "readiness_text")

    levels = {lv.get("level") for lv in activation.get("levels") or [] if isinstance(lv, dict)}
    for lid in ("OCR-L0", "OCR-L1", "OCR-L2", "OCR-L3", "OCR-L4", "OCR-L5"):
        ok(lid in levels, lid)

    rows = criticality.get("rows") or []
    by_type = {r.get("task_type"): r for r in rows if isinstance(r, dict)}
    ok(by_type.get("generic_environment_text", {}).get("ocr_needed") is False, "generic_no_ocr")
    ok(by_type.get("long_notice", {}).get("static_assisted_reading_required") is True, "long_static")
    shop = by_type.get("shop_name_confirmation", {})
    ok(
        "visual" in str(shop.get("default_world_model_path", "")).lower()
        or "logo" in str(shop.get("default_world_model_path", "")).lower(),
        "shop_visual_first",
    )

    reason_codes = {r.get("reason_code") for r in taxonomy.get("reasons") or [] if isinstance(r, dict)}
    ok("repeated_empty_after_internal_retry" in reason_codes, "reason_retry_empty")

    cats = {c.get("category") for c in repair.get("categories") or [] if isinstance(c, dict)}
    ok("user_repairable" in cats, "cat_user")
    ok("system_repairable" in cats, "cat_system")
    ok("externally_repairable" in cats, "cat_external")
    ok("not_recoverable_or_not_worth_ocr" in cats, "cat_not_worth")

    ug_ids = {a.get("action_id") for a in ug.get("actions") or [] if isinstance(a, dict)}
    ok("ask_user_move_closer" in ug_ids, "ug_closer")
    ok("ask_user_center_text" in ug_ids, "ug_center")

    sys_ids = {a.get("action_id") for a in sys_a.get("actions") or [] if isinstance(a, dict)}
    ok("request_zoom" in sys_ids, "sys_zoom")
    ok("request_autofocus" in sys_ids, "sys_af")

    ext_ids = {a.get("action_id") for a in ext.get("actions") or [] if isinstance(a, dict)}
    ok("request_nearby_person_read_short_text" in ext_ids, "ext_read")

    stops = {x.get("stop_reason") for x in not_worth.get("stops") or [] if isinstance(x, dict)}
    ok("repeated_empty_after_internal_retry_limit" in stops, "stop_retry")

    ok(current.get("user_guidance_recovery_recommended") is True, "ug_recommended")
    ok(current.get("runtime_action_committed") is False, "current_no_action")
    ok(current.get("tts_invoked") is False, "current_no_tts")

    ok("zoom_available" in hardware, "hw_zoom_field")
    ok("autofocus_available" in hardware, "hw_af_field")
    ok(hardware.get("hardware_capability_unknown_allowed") is True, "hw_unknown_ok")

    ok(stc.get("stc_link_required") is True, "stc_link")
    ok(boundary.get("policy_only") is True, "boundary_policy")
    ok(boundary.get("ocr_invoked") is False, "boundary_no_ocr")
    ok(metrics.get("runtime_action_committed_count") == 0, "metrics_no_action")
    ok(bench.get("benchmark_score_generated") is False, "bench_no_score")
    ok(health.get("recovery_action_committed") is False, "health_no_recovery")
    ok(no_write.get("boundary_ok") is True, "no_write_ok")
    ok(no_write.get("violations") == [], "no_write_violations")
    ok(sim.get("simulation_profile_id") == "developer_full", "sim_profile")
    ok(len(data["followups"].get("items") or []) >= 5, "followups")
    ok(audit.get("world_model_written") is False, "audit_no_wm")
    ok(audit.get("midplatform_fact_written") is False, "audit_no_fact")
    ok(audit.get("runtime_routing_changed") is False, "audit_no_routing")

    verdict = "GO" if not blockers else "NO_GO"
    report = {
        "verdict": verdict,
        "checks_passed": checks,
        "checks_expected": 69,
        "blockers": blockers,
        "phase": "User-Guidance-Recovery-Policy-v1-001",
    }
    _write_json(root / "user_guidance_recovery_verifier_report_v1.json", report)
    print(json.dumps(report, ensure_ascii=False))
    return 0 if verdict in ("GO", "CONDITIONAL_GO") else 2


if __name__ == "__main__":
    raise SystemExit(main())
