#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for OCR Activation Governance Policy v1."""

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
        "summary": "ocr_activation_governance_policy_v1_summary.json",
        "gate": "ocr_activation_gate_decision_table_v1.json",
        "dual": "ocr_dual_trigger_activation_policy_v1.json",
        "default_off": "ocr_default_off_world_modeling_policy_v1.json",
        "visual": "ocr_visual_semantic_first_routing_policy_v1.json",
        "dyn_static": "ocr_dynamic_vs_static_reading_gate_v1.json",
        "readiness": "ocr_readiness_gate_policy_v1.json",
        "freshness": "ocr_stc_freshness_gate_policy_v1.json",
        "expired_principle": "ocr_expired_information_value_principle_v1.json",
        "stale_routing": "ocr_stale_observation_long_term_routing_policy_v1.json",
        "expired": "ocr_expired_observation_candidate_policy_v1.json",
        "hint": "ocr_world_change_hint_candidate_policy_v1.json",
        "user_env": "ocr_user_environment_context_candidate_policy_v1.json",
        "user_profile": "ocr_user_profile_context_candidate_policy_v1.json",
        "emotional": "ocr_emotional_context_background_candidate_policy_v1.json",
        "retry": "ocr_retry_recovery_routing_policy_v1.json",
        "current": "ocr_activation_current_case_decision_dryrun_v1.json",
        "boundary": "ocr_activation_governance_boundary_report_v1.json",
        "metrics": "ocr_activation_governance_metrics_candidate_report_v1.json",
        "bench": "ocr_activation_governance_benchmark_link_report_v1.json",
        "health": "ocr_activation_governance_system_health_link_report_v1.json",
        "no_write": "ocr_activation_governance_no_write_boundary_report_v1.json",
        "sim": "ocr_activation_governance_simulation_context_report_v1.json",
        "non_claims": "ocr_activation_governance_non_claims_report_v1.json",
        "followups": "ocr_activation_governance_open_followups_v1.json",
        "audit": "ocr_activation_governance_audit_report_v1.json",
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
            root / "ocr_activation_governance_verifier_report_v1.json",
            {"verdict": "NO_GO", "checks_passed": 0, "blockers": blockers},
        )
        print(json.dumps({"verdict": "NO_GO", "blockers": blockers}, ensure_ascii=False))
        return 2

    s = data["summary"]
    gate = data["gate"]
    dual = data["dual"]
    default_off = data["default_off"]
    visual = data["visual"]
    dyn_static = data["dyn_static"]
    readiness = data["readiness"]
    freshness = data["freshness"]
    expired_principle = data["expired_principle"]
    stale_routing = data["stale_routing"]
    expired = data["expired"]
    hint = data["hint"]
    user_env = data["user_env"]
    user_profile = data["user_profile"]
    emotional = data["emotional"]
    retry = data["retry"]
    current = data["current"]
    boundary = data["boundary"]
    metrics = data["metrics"]
    bench = data["bench"]
    health = data["health"]
    no_write = data["no_write"]
    sim = data["sim"]
    audit = data["audit"]

    ok(True, "summary_exists")
    ok(s.get("policy_scope") == "ocr_activation_governance_policy_only", "scope")
    ok(s.get("based_on_stc_sampling_guidance_policy") is True, "based_stc")
    ok(s.get("based_on_user_guidance_recovery_policy") is True, "based_ug")
    ok(s.get("ocr_default_off_for_world_modeling") is True, "default_off")
    ok(s.get("dual_trigger_activation_defined") is True, "dual_defined")
    ok(s.get("safety_trigger_gate_defined") is True, "safety_gate")
    ok(s.get("task_trigger_gate_defined") is True, "task_gate")
    ok(s.get("ocr_self_activation_allowed") is False, "no_self_activation")
    ok(s.get("action_freshness_policy_defined") is True, "action_freshness")
    ok(s.get("world_model_historical_value_policy_defined") is True, "wm_historical")
    ok(s.get("expired_information_value_principle_defined") is True, "expired_principle_def")
    ok(s.get("four_value_dimensions_policy_defined") is True, "four_value_def")
    ok(s.get("user_profile_context_value_policy_defined") is True, "profile_value_def")
    ok(s.get("emotional_context_value_policy_defined") is True, "emotional_value_def")
    ok(s.get("stale_observation_long_term_routing_defined") is True, "stale_routing_def")
    ok(s.get("expired_observation_candidate_policy_defined") is True, "expired_def")
    ok(s.get("world_change_hint_candidate_policy_defined") is True, "hint_def")
    ok(s.get("user_environment_context_candidate_policy_defined") is True, "user_env_def")
    ok(s.get("user_profile_context_candidate_policy_defined") is True, "user_profile_def")
    ok(s.get("emotional_context_background_candidate_policy_defined") is True, "emotional_def")

    decisions = {r.get("gate_decision") for r in gate.get("rows") or [] if isinstance(r, dict)}
    for gd in (
        "OCR_NOT_ACTIVATED",
        "SAFETY_SHORT_MARKER_SCAN",
        "TASK_SHORT_TEXT_CONFIRMATION",
        "EXPIRED_OBSERVATION_TO_WORLD_HINT",
    ):
        ok(gd in decisions, gd)

    safety = dual.get("safety_trigger") or {}
    task = dual.get("task_trigger") or {}
    ok(safety.get("default_background_enabled") is True, "safety_bg")
    ok(task.get("midplatform_pre_activation_required") is True, "mp_pre_activation")

    ok("generic_environment_text" in (default_off.get("forbidden_default_use") or []), "generic_forbidden")
    visual_rows = {r.get("scene_type"): r for r in visual.get("rows") or [] if isinstance(r, dict)}
    shop = visual_rows.get("shop_name_confirmation", {})
    ok(
        "visual" in str(shop.get("first_path", "")).lower()
        or "logo" in str(shop.get("first_path", "")).lower()
        or "poi" in str(shop.get("first_path", "")).lower(),
        "shop_visual_first",
    )

    static_types = dyn_static.get("static_required_types") or []
    ok("long_notice" in static_types, "long_notice_static")
    ok(len(readiness.get("dimensions") or []) >= 5, "readiness5")

    ok(freshness.get("stale_blocks_action") is True, "stale_blocks_action")
    ok(freshness.get("stale_blocks_action_freshness_only") is True, "stale_blocks_freshness_only")
    ok(freshness.get("stale_allows_world_hint_candidate") is True, "stale_allows_hint")
    ok(freshness.get("stale_allows_user_profile_context_candidate") is True, "stale_allows_profile")
    ok(freshness.get("stale_allows_emotional_context_background_candidate") is True, "stale_allows_emotional")

    dims = expired_principle.get("four_value_dimensions") or []
    dim_ids = {d.get("dimension_id") for d in dims if isinstance(d, dict)}
    for did in (
        "action_freshness",
        "world_historical_value",
        "user_profile_context_value",
        "emotional_context_value",
    ):
        ok(did in dim_ids, did)

    routes = stale_routing.get("routing_targets") or []
    for rt in (
        "expired_observation_candidate",
        "world_change_hint_candidate",
        "user_environment_context_candidate",
        "user_profile_context_candidate",
        "emotional_context_background_candidate",
    ):
        ok(rt in routes, rt)
    ok(stale_routing.get("anti_pattern") == "do_not_simply_discard_stale", "no_discard_antipattern")

    candidates = expired.get("candidates") or []
    ok(any(c.get("cannot_use_for_action") is True for c in candidates if isinstance(c, dict)), "cannot_action")
    ok(any(c.get("can_feed_world_model_candidate") is True for c in candidates if isinstance(c, dict)), "can_wm_cand")
    ok(any(c.get("can_feed_user_profile_context") is True for c in candidates if isinstance(c, dict)), "can_profile")
    ok(any(c.get("source_chain") is True for c in candidates if isinstance(c, dict)), "meta_source_chain")

    hints = hint.get("hints") or []
    ok(any(h.get("fact_write_allowed_now") is False for h in hints if isinstance(h, dict)), "hint_no_fact")

    ok(retry.get("repeated_empty_routes_to") == "USER_GUIDANCE_RECOVERY", "retry_ug")
    ok(retry.get("stale_but_useful_routes_to") == "EXPIRED_OBSERVATION_TO_WORLD_HINT", "stale_hint_route")

    ok(current.get("ocr_activation_decision") == "USER_GUIDANCE_RECOVERY", "current_ug")
    ok(current.get("expired_observation_candidate_allowed") is True, "expired_allowed")
    ok(current.get("world_change_hint_candidate_allowed") is True, "hint_allowed")
    ok(current.get("user_environment_context_candidate_allowed") is True, "user_env_allowed")
    ok(current.get("user_profile_context_candidate_allowed") is True, "user_profile_allowed")
    ok(current.get("emotional_context_background_candidate_allowed") is True, "emotional_allowed")
    ok(current.get("stale_blocks_action_freshness_only") is True, "stale_freshness_only")

    ok(len(user_env.get("contexts") or []) >= 3, "user_env_contexts")
    ok(len(user_profile.get("contexts") or []) >= 2, "user_profile_contexts")
    ok(len(emotional.get("backgrounds") or []) >= 3, "emotional_backgrounds")

    ok(boundary.get("policy_only") is True, "policy_only")
    ok(metrics.get("no_write_boundary_pass_rate") == 1.0, "metrics_pass")
    ok(bench.get("benchmark_score_generated") is False, "bench_no_score")
    ok(health.get("recovery_action_committed") is False, "health_no_recovery")
    ok(no_write.get("boundary_ok") is True, "no_write_ok")
    ok(no_write.get("violations") == [], "no_violations")
    ok(sim.get("simulation_profile_id") == "developer_full", "sim_profile")
    ok(len(data["followups"].get("items") or []) >= 5, "followups")
    ok(audit.get("midplatform_fact_written") is False, "audit_no_fact")
    ok(audit.get("world_model_written") is False, "audit_no_wm")
    ok(audit.get("scene_delta_candidate_generated") is False, "audit_no_scene")
    ok(audit.get("navigation_decision_invoked") is False, "audit_no_nav")
    ok(audit.get("runtime_routing_changed") is False, "audit_no_routing")

    verdict = "GO" if not blockers else "NO_GO"
    report = {
        "verdict": verdict,
        "checks_passed": checks,
        "checks_expected": 85,
        "blockers": blockers,
        "phase": "OCR-Activation-Governance-Policy-v1-001",
    }
    _write_json(root / "ocr_activation_governance_verifier_report_v1.json", report)
    print(json.dumps(report, ensure_ascii=False))
    return 0 if verdict in ("GO", "CONDITIONAL_GO") else 2


if __name__ == "__main__":
    raise SystemExit(main())
