#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for Source Validation v2 after EP v3."""

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


def _read_json(p: Path):
    return json.loads(p.read_text(encoding="utf-8"))


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
        "summary": "source_validation_v2_after_ep_v3_summary.json",
        "intake": "source_validation_v2_candidate_intake_matrix.json",
        "rules": "source_validation_v2_rule_matrix.json",
        "chain": "source_validation_v2_source_chain_completeness_report.json",
        "same_frame": "source_validation_v2_same_frame_consensus_blocker_report.json",
        "strategy_repeat": "source_validation_v2_strategy_repeat_validation_report.json",
        "noisy": "source_validation_v2_noisy_segment_blocker_report.json",
        "external": "source_validation_v2_external_support_missing_report.json",
        "entity": "source_validation_v2_entity_validation_boundary_report.json",
        "decision": "source_validation_v2_decision_matrix.json",
        "routing": "source_validation_v2_routing_report.json",
        "future": "source_validation_v2_future_validation_plan.json",
        "review": "source_validation_v2_review_policy_readiness_report.json",
        "slot": "source_validation_v2_unresolved_slot_readiness_report.json",
        "boundary": "source_validation_v2_boundary_report.json",
        "metrics": "source_validation_v2_metrics_candidate_report.json",
        "bench": "source_validation_v2_benchmark_link_report.json",
        "health": "source_validation_v2_system_health_link_report.json",
        "no_write": "source_validation_v2_no_write_boundary_report.json",
        "sim": "source_validation_v2_simulation_context_report.json",
        "non_claims": "source_validation_v2_non_claims_report.json",
        "followups": "source_validation_v2_open_followups.json",
        "audit": "source_validation_v2_audit_report.json",
    }
    data = {}
    for k, f in files.items():
        p = root / f
        if not p.is_file():
            blockers.append(f"missing:{k}")
        else:
            data[k] = _read_json(p)

    if blockers:
        _write_json(
            root / "source_validation_v2_verifier_report.json",
            {"verdict": "NO_GO", "checks_passed": 0, "blockers": blockers},
        )
        print(json.dumps({"verdict": "NO_GO", "blockers": blockers}, ensure_ascii=False))
        return 2

    s = data["summary"]
    intake = data["intake"]
    rules = data["rules"]
    chain = data["chain"]
    same_frame = data["same_frame"]
    strategy_repeat = data["strategy_repeat"]
    noisy = data["noisy"]
    external = data["external"]
    entity = data["entity"]
    decision = data["decision"]
    routing = data["routing"]
    slot = data["slot"]
    boundary = data["boundary"]
    metrics = data["metrics"]
    bench = data["bench"]
    health = data["health"]
    no_write = data["no_write"]
    sim = data["sim"]
    audit = data["audit"]

    ok(True, "summary_exists")
    ok(s.get("validation_scope") == "source_validation_v2_dryrun_only", "scope")
    ok(s.get("based_on_semantic_candidate_v3") is True, "based_sem")
    ok(s.get("based_on_evidence_pack_v3") is True, "based_ep")
    ok(s.get("semantic_candidate_v3_count_observed") == 4, "sem4")
    ok(s.get("evidence_pack_v3_count_observed") == 4, "ep4")
    ok(s.get("source_validation_evaluated") is True, "evaluated")
    ok(s.get("source_validation_passed_count") == 0, "passed0")
    ok(s.get("entity_confirmed_count") == 0, "no_entity_confirmed")
    ok(s.get("map_poi_checked") is False, "no_map")
    ok(s.get("visual_symbol_registry_checked") is False, "no_vsr")
    ok(s.get("multiframe_checked") is False, "no_mf")
    ok(s.get("repeated_observation_checked") is False, "no_rep")
    ok(s.get("user_confirmation_checked") is False, "no_user")

    ok(intake.get("row_count") == 4 or len(intake.get("rows") or []) == 4, "intake_4")
    for row in intake.get("rows") or []:
        if isinstance(row, dict):
            ok(row.get("entity_confirmed") is False, "intake_entity_false")
            ok(row.get("intake_status") == "accepted", "intake_accepted")
            break

    rule_ids = {r.get("rule_id") for r in rules.get("rules") or [] if isinstance(r, dict)}
    ok("same_frame_same_region_blocks_independent_consensus" in rule_ids, "rule_same_frame")
    ok("repeated_strategy_output_not_consensus" in rule_ids, "rule_repeat")
    ok("noisy_segment_blocks_entity_confirmation" in rule_ids, "rule_noisy")

    for row in chain.get("rows") or []:
        if isinstance(row, dict):
            ok(row.get("source_chain_complete_for_dryrun") is True, "chain_complete")
            break

    ok(same_frame.get("independent_consensus_allowed") is False, "no_consensus")
    ok(same_frame.get("consensus_status") == "blocked", "consensus_blocked")

    ok(strategy_repeat.get("repeated_output_not_consensus") is True, "repeat_not_consensus")
    ok(strategy_repeat.get("independent_validation_weight") == 0, "weight0")

    for row in noisy.get("rows") or []:
        if isinstance(row, dict):
            ok(row.get("correction_committed") is False, "no_correction")
            ok(row.get("completion_committed") is False, "no_completion")
            ok(row.get("noisy_segment_blocks_entity_confirmation") is True, "noisy_blocks")
            break

    ok(external.get("map_poi_checked") is False, "ext_map")
    ok(external.get("visual_symbol_registry_checked") is False, "ext_vsr")

    for row in entity.get("rows") or []:
        if isinstance(row, dict):
            ok(row.get("entity_confirmed") is False, "entity_false")
            ok(row.get("entity_confirmation_allowed") is False, "entity_no_confirm")
            break

    validated_for_fact = False
    for row in decision.get("rows") or []:
        if isinstance(row, dict):
            ok(row.get("validation_passed") is False, "decision_not_passed")
            st = str(row.get("validation_status") or "")
            if st == "validated_for_fact":
                validated_for_fact = True
            break
    ok(not validated_for_fact, "no_validated_for_fact")

    for row in decision.get("rows") or []:
        if isinstance(row, dict) and row.get("validation_status"):
            statuses = {str(r.get("validation_status")) for r in decision.get("rows") or [] if isinstance(r, dict)}
            ok("validated_for_fact" not in statuses, "no_validated_status")
            break

    ok(routing.get("validation_passed_count") == 0, "routing_passed0")
    ok(routing.get("fact_write_allowed_count") == 0, "routing_no_fact")

    ok(data["future"].get("phases"), "future_plan")
    ok(len(data["future"].get("phases") or []) >= 5, "future_phases")

    ok(data["review"].get("decision_commit_allowed_now") is False, "review_no_commit")

    ok(slot.get("slot_generation_allowed_now") is False, "no_slot_now")

    ok(boundary.get("world_model_attach_allowed") is False, "boundary_no_wm")
    ok(boundary.get("scene_delta_candidate_allowed") is False, "boundary_no_sd")

    ok(metrics.get("fact_write_allowed_count") == 0, "metrics_no_fact")

    ok(bench.get("benchmark_score_generated") is False, "bench_no_score")

    ok(health.get("provider_health_runtime_checked") is False, "health_no_runtime")

    ok(no_write.get("boundary_ok") is True, "no_write_ok")
    ok(no_write.get("violations") == [], "no_write_violations")

    ok(sim.get("simulation_profile_id") == "developer_full", "sim_profile")

    ok(data["non_claims"].get("dryrun_not_validation_passed") is True, "non_claims_dryrun")
    ok(len(data["followups"].get("items") or []) >= 5, "followups")

    ok(audit.get("world_model_attach_executed") is False, "audit_no_wm")
    ok(audit.get("scene_delta_candidate_generated") is False, "audit_no_sd")
    ok(audit.get("midplatform_fact_written") is False, "audit_no_fact")
    ok(audit.get("world_model_written") is False, "audit_no_wm_write")
    ok(audit.get("navigation_decision_invoked") is False, "audit_no_nav")
    ok(audit.get("runtime_routing_changed") is False, "audit_no_routing")

    verdict = "GO" if not blockers else "NO_GO"
    report = {
        "verdict": verdict,
        "checks_passed": checks,
        "checks_expected": 70,
        "blockers": blockers,
        "phase": "Source-Validation-v2-after-EP-v3-001",
    }
    _write_json(root / "source_validation_v2_verifier_report.json", report)
    print(json.dumps(report, ensure_ascii=False))
    return 0 if verdict in ("GO", "CONDITIONAL_GO") else 2


if __name__ == "__main__":
    raise SystemExit(main())
