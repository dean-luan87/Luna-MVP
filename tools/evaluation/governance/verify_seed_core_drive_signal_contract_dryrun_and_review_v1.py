#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Seed Core Drive Signal Contract DryRunAndReview v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.midplatform_cognitive_zoning_architecture_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as CZ_DR_FINAL,
)
from capabilities.governance.midplatform_vnext_architecture_realignment_planning_v1 import (
    COGNITIVE_ZONES,
)
from capabilities.governance.seed_core_drive_signal_contract_dryrun_and_review_v1 import (
    AUTONOMOUS_OBSERVATION_CONFIRMATIONS,
    AUTONOMOUS_OBSERVATION_COVERAGE,
    BLOCKED_PATHS,
    BOUNDARY_FALSE,
    BOUNDARY_TRUE,
    CONFLICT_OUTPUT_REQUIREMENTS,
    CONFLICT_TYPES,
    DECISION_BOUNDARY_CONFIRMATIONS,
    EMOTION_ENGINE_CONFIRMATIONS,
    EMOTION_ENGINE_COVERAGE,
    EVOLUTIONARY_RECURSION_CONFIRMATIONS,
    EVOLUTIONARY_RECURSION_COVERAGE,
    FINAL_DECISION_GO,
    HEALTH_MANAGEMENT_CONFIRMATIONS,
    HEALTH_MANAGEMENT_COVERAGE,
    INTEGRATION_PLAN_CONFIRMATIONS,
    NEXT_PHASE_GO,
    NON_CLAIMS,
    PHASE_ID,
    PRIORITY_CONFIRMATIONS,
    PRIORITY_LEVELS,
    RESOURCE_GOVERNANCE_CONFIRMATIONS,
    RESOURCE_GOVERNANCE_COVERAGE,
    RUNTIME_BOUNDARY_CONFIRMATIONS,
    SCOPE,
    SIGNAL_TAXONOMY,
    SIGNAL_TAXONOMY_CONFIRMATIONS,
    SURVIVAL_DRIVE_CONFIRMATIONS,
    SURVIVAL_DRIVE_COVERAGE,
    SYSTEM_OPTIMIZATION_CONFIRMATIONS,
    SYSTEM_OPTIMIZATION_COVERAGE,
    TASK_DRIVE_CONFIRMATIONS,
    TASK_DRIVE_COVERAGE,
    TRACEABILITY_FIELDS,
    UPSTREAM_PLANNING_FINAL,
    UPSTREAM_PLANNING_NEXT,
    ZONE_HANDOFF_PLAN,
)
from capabilities.governance.seed_core_drive_signal_contract_planning_v1 import (
    DRIVE_SIGNAL_CANDIDATE_FIELDS,
    FINAL_DECISION_GO as PLANNING_FINAL,
    NEXT_PHASE_GO as PLANNING_NEXT,
    SEED_CORE_HINT_CANDIDATE_FIELDS,
    SEED_CORE_SIGNAL_CANDIDATE_FIELDS,
)
from capabilities.governance.seed_core_pluggable_layer_architecture_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as SC_DR_FINAL,
)

MIN_CHECKS = 390

REQUIRED = (
    "drive_signal_contract_dryrun_review_policy_v1.json",
    "drive_signal_contract_planning_input_review_v1.json",
    "seed_core_drive_signal_model_candidate_v1.json",
    "sample_drive_signal_candidate_v1.json",
    "sample_seed_core_signal_candidate_v1.json",
    "sample_seed_core_hint_candidate_v1.json",
    "seed_core_signal_taxonomy_review_v1.json",
    "survival_drive_signal_dryrun_review_v1.json",
    "task_drive_signal_dryrun_review_v1.json",
    "resource_governance_signal_dryrun_review_v1.json",
    "health_management_signal_dryrun_review_v1.json",
    "system_optimization_signal_dryrun_review_v1.json",
    "autonomous_world_observation_signal_dryrun_review_v1.json",
    "emotion_engine_signal_dryrun_review_v1.json",
    "evolutionary_recursion_signal_dryrun_review_v1.json",
    "drive_signal_priority_policy_review_v1.json",
    "drive_signal_conflict_policy_review_v1.json",
    "drive_signal_zone_handoff_review_v1.json",
    "drive_signal_information_integration_handoff_review_v1.json",
    "drive_signal_decision_center_boundary_review_v1.json",
    "drive_signal_controlled_runtime_boundary_review_v1.json",
    "drive_signal_traceability_review_v1.json",
    "drive_signal_boundary_audit_v1.json",
    "drive_signal_blocked_path_result_v1.json",
    "drive_signal_closure_decision_v1.json",
    "next_route_readiness_decision_v1.json",
    "non_claims_register_v1.json",
    "summary.json",
)


def _load(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument(
        "--output-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "seed_core_drive_signal_contract_dryrun_and_review"
        ),
    )
    p.add_argument(
        "--drive-signal-planning-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "seed_core_drive_signal_contract_planning"
        ),
    )
    p.add_argument(
        "--seed-core-pluggable-dryrun-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "seed_core_pluggable_layer_architecture_dryrun_and_review"
        ),
    )
    p.add_argument(
        "--cognitive-zoning-dryrun-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "midplatform_cognitive_zoning_architecture_dryrun_and_review"
        ),
    )
    args = p.parse_args()
    root = Path(args.output_root)
    plan_root = Path(args.drive_signal_planning_root)
    sc_dr_root = Path(args.seed_core_pluggable_dryrun_root)
    cz_dr_root = Path(args.cognitive_zoning_dryrun_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in REQUIRED:
        ok(f"file.{f}", (root / f).is_file())

    plan_vr = _load(plan_root / "verifier_report.json")
    plan_sm = _load(plan_root / "summary.json")
    sc_dr_vr = _load(sc_dr_root / "verifier_report.json")
    sc_dr_sm = _load(sc_dr_root / "summary.json")
    cz_dr_vr = _load(cz_dr_root / "verifier_report.json")

    ok("upstream.planning_go", plan_vr.get("verifier") == "GO")
    ok("upstream.planning_final", plan_sm.get("final_decision") == UPSTREAM_PLANNING_FINAL)
    ok("upstream.planning_final_expected", plan_sm.get("final_decision") == PLANNING_FINAL)
    ok("upstream.planning_next", plan_sm.get("recommended_next_phase") == UPSTREAM_PLANNING_NEXT)
    ok("upstream.planning_next_expected", plan_sm.get("recommended_next_phase") == PLANNING_NEXT)
    ok("upstream.sc_dr_go", sc_dr_vr.get("verifier") == "GO")
    ok("upstream.sc_dr_final", sc_dr_sm.get("final_decision") == SC_DR_FINAL)
    ok("upstream.cz_dr_go", cz_dr_vr.get("verifier") == "GO")

    summary = _load(root / "summary.json")
    policy = _load(root / "drive_signal_contract_dryrun_review_policy_v1.json")
    input_review = _load(root / "drive_signal_contract_planning_input_review_v1.json")
    model = _load(root / "seed_core_drive_signal_model_candidate_v1.json")
    sample_drive = _load(root / "sample_drive_signal_candidate_v1.json")
    sample_seed = _load(root / "sample_seed_core_signal_candidate_v1.json")
    sample_hint = _load(root / "sample_seed_core_hint_candidate_v1.json")
    taxonomy = _load(root / "seed_core_signal_taxonomy_review_v1.json")
    survival = _load(root / "survival_drive_signal_dryrun_review_v1.json")
    task = _load(root / "task_drive_signal_dryrun_review_v1.json")
    resource = _load(root / "resource_governance_signal_dryrun_review_v1.json")
    health = _load(root / "health_management_signal_dryrun_review_v1.json")
    optimization = _load(root / "system_optimization_signal_dryrun_review_v1.json")
    observation = _load(root / "autonomous_world_observation_signal_dryrun_review_v1.json")
    emotion = _load(root / "emotion_engine_signal_dryrun_review_v1.json")
    evolution = _load(root / "evolutionary_recursion_signal_dryrun_review_v1.json")
    priority = _load(root / "drive_signal_priority_policy_review_v1.json")
    conflict = _load(root / "drive_signal_conflict_policy_review_v1.json")
    handoff = _load(root / "drive_signal_zone_handoff_review_v1.json")
    integration = _load(root / "drive_signal_information_integration_handoff_review_v1.json")
    decision = _load(root / "drive_signal_decision_center_boundary_review_v1.json")
    runtime_bound = _load(root / "drive_signal_controlled_runtime_boundary_review_v1.json")
    traceability = _load(root / "drive_signal_traceability_review_v1.json")
    boundary_audit = _load(root / "drive_signal_boundary_audit_v1.json")
    blocked = _load(root / "drive_signal_blocked_path_result_v1.json")
    closure = _load(root / "drive_signal_closure_decision_v1.json")
    next_route = _load(root / "next_route_readiness_decision_v1.json")
    non_claims = _load(root / "non_claims_register_v1.json")

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("scope") == SCOPE)
    ok("summary.pass", summary.get("dryrun_and_review_pass") is True)
    ok("summary.simulated_go", summary.get("system_level_simulated_go") is True)
    ok("summary.model_gen", summary.get("seed_core_drive_signal_model_candidate_generated") is True)
    ok("summary.sample_drive", summary.get("sample_drive_signal_candidate_generated") is True)
    ok("summary.sample_seed", summary.get("sample_seed_core_signal_candidate_generated") is True)
    ok("summary.sample_hint", summary.get("sample_seed_core_hint_candidate_generated") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)

    for field in BOUNDARY_TRUE:
        ok(f"true.{field}", summary.get(field) is True)
    for field in BOUNDARY_FALSE:
        ok(f"false.{field}", summary.get(field) is False)

    ok("policy.dryrun_only", policy.get("dryrun_not_runtime_not_execute") is True)
    ok("input.pass", input_review.get("review_pass") is True)
    ok("input.seed7", input_review.get("seed_core_7_components_validated") is True)
    ok("input.evo_proposal", input_review.get("emotion_engine_and_evolutionary_recursion_proposal_only") is True)

    ok("model.id", model.get("model_id") == "seed_core_drive_signal_contract_v1")
    ok("model.type", model.get("model_type") == "seed_core_signal_contract_model")
    ok("model.contract_only", model.get("signal_contract_only") is True)
    ok("model.candidate", model.get("candidate_only") is True)
    ok("model.no_execute", model.get("does_not_execute_drive") is True)
    ok("model.no_decide", model.get("does_not_decide") is True)
    ok("model.no_provider", model.get("does_not_invoke_provider") is True)
    ok("model.no_runtime", model.get("does_not_enable_runtime") is True)
    ok("model.no_memory", model.get("does_not_write_memory") is True)
    ok("model.no_wm", model.get("does_not_write_worldmodel") is True)
    ok("model.runtime_false", model.get("seed_core_runtime_enabled_now") is False)

    for field in DRIVE_SIGNAL_CANDIDATE_FIELDS:
        ok(f"sample_drive.{field[:18]}", field in sample_drive)
    ok("sample_drive.candidate", sample_drive.get("candidate_only") is True)
    ok("sample_drive.not_decision", sample_drive.get("not_decision") is True)
    ok("sample_drive.not_action", sample_drive.get("not_action") is True)
    ok("sample_drive.not_output", sample_drive.get("not_user_output") is True)
    ok("sample_drive.runtime_false", sample_drive.get("runtime_enable_allowed") is False)

    for field in SEED_CORE_SIGNAL_CANDIDATE_FIELDS:
        ok(f"sample_seed.{field[:18]}", field in sample_seed)
    ok("sample_seed.runtime_false", sample_seed.get("runtime_enable_allowed") is False)

    for field in SEED_CORE_HINT_CANDIDATE_FIELDS:
        ok(f"sample_hint.{field[:18]}", field in sample_hint)
    ok("sample_hint.non_binding", sample_hint.get("non_binding") is True)
    ok("sample_hint.decision_req", sample_hint.get("decision_required") is True)

    ok("tax.pass", taxonomy.get("dryrun_and_review_pass") is True)
    ok("tax.count16", taxonomy.get("signal_type_count") == 16)
    for sig in SIGNAL_TAXONOMY:
        ok(f"tax.{sig[:18]}", sig in (taxonomy.get("signal_types") or []))
    for conf in SIGNAL_TAXONOMY_CONFIRMATIONS:
        ok(f"tax.conf.{conf[:18]}", conf in (taxonomy.get("confirmations") or []))

    for review, cov, conf, name in (
        (survival, SURVIVAL_DRIVE_COVERAGE, SURVIVAL_DRIVE_CONFIRMATIONS, "survival"),
        (task, TASK_DRIVE_COVERAGE, TASK_DRIVE_CONFIRMATIONS, "task"),
        (resource, RESOURCE_GOVERNANCE_COVERAGE, RESOURCE_GOVERNANCE_CONFIRMATIONS, "resource"),
        (health, HEALTH_MANAGEMENT_COVERAGE, HEALTH_MANAGEMENT_CONFIRMATIONS, "health"),
        (optimization, SYSTEM_OPTIMIZATION_COVERAGE, SYSTEM_OPTIMIZATION_CONFIRMATIONS, "opt"),
        (observation, AUTONOMOUS_OBSERVATION_COVERAGE, AUTONOMOUS_OBSERVATION_CONFIRMATIONS, "obs"),
        (emotion, EMOTION_ENGINE_COVERAGE, EMOTION_ENGINE_CONFIRMATIONS, "emotion"),
        (evolution, EVOLUTIONARY_RECURSION_COVERAGE, EVOLUTIONARY_RECURSION_CONFIRMATIONS, "evo"),
    ):
        ok(f"{name}.pass", review.get("dryrun_and_review_pass") is True)
        for c in cov:
            ok(f"{name}.cov.{c[:18]}", c in (review.get("coverage") or []))
        for c in conf:
            ok(f"{name}.conf.{c[:18]}", c in (review.get("confirmations") or []))
    ok("evo.proposal_only", evolution.get("proposal_only") is True)

    ok("priority.pass", priority.get("dryrun_and_review_pass") is True)
    ok("priority.count9", priority.get("level_count") == 9)
    for pl in PRIORITY_LEVELS:
        ok(f"priority.{pl['rank']}", any(
            p.get("rank") == pl["rank"] for p in (priority.get("priority_levels") or [])
        ))
    for conf in PRIORITY_CONFIRMATIONS:
        ok(f"priority.conf.{conf[:18]}", conf in (priority.get("confirmations") or []))

    ok("conflict.pass", conflict.get("dryrun_and_review_pass") is True)
    ok("conflict.count7", conflict.get("conflict_count") == 7)
    for ct in CONFLICT_TYPES:
        ok(f"conflict.{ct['conflict_id'][:18]}", any(
            c.get("conflict_id") == ct["conflict_id"] for c in (conflict.get("conflict_types") or [])
        ))
    for req in CONFLICT_OUTPUT_REQUIREMENTS:
        ok(f"conflict.req.{req[:18]}", req in (conflict.get("output_requirements") or []))

    ok("handoff.pass", handoff.get("dryrun_and_review_pass") is True)
    ok("handoff.count8", handoff.get("zone_count") == 8)
    for zone_name in COGNITIVE_ZONES:
        ok(f"handoff.zone.{zone_name[:18]}", zone_name in (handoff.get("cognitive_zones") or []))
    for zh in ZONE_HANDOFF_PLAN:
        ok(f"handoff.{zh['zone'][:18]}", any(
            h.get("zone") == zh["zone"] for h in (handoff.get("zone_handoffs") or [])
        ))

    ok("integration.pass", integration.get("dryrun_and_review_pass") is True)
    for conf in INTEGRATION_PLAN_CONFIRMATIONS:
        ok(f"integration.{conf[:18]}", conf in (integration.get("confirmations") or []))

    ok("decision.pass", decision.get("dryrun_and_review_pass") is True)
    for conf in DECISION_BOUNDARY_CONFIRMATIONS:
        ok(f"decision.{conf[:18]}", conf in (decision.get("confirmations") or []))

    ok("runtime.pass", runtime_bound.get("dryrun_and_review_pass") is True)
    for conf in RUNTIME_BOUNDARY_CONFIRMATIONS:
        ok(f"runtime.{conf[:18]}", conf in (runtime_bound.get("confirmations") or []))

    ok("trace.pass", traceability.get("dryrun_and_review_pass") is True)
    ok("trace.preserve", traceability.get("all_signals_must_preserve") is True)
    for field in TRACEABILITY_FIELDS:
        ok(f"trace.{field[:18]}", field in (traceability.get("required_fields") or []))

    ok("audit.pass", boundary_audit.get("audit_pass") is True)
    for field in BOUNDARY_FALSE:
        ok(f"audit.{field}", boundary_audit.get("boundary_fields", {}).get(field) is False)

    ok("blocked.all", blocked.get("all_blocked") is True)
    ok("blocked.count17", blocked.get("blocked_count") == 17)
    blocked_ids = [b.get("path_id") for b in (blocked.get("blocked_paths") or [])]
    for path in BLOCKED_PATHS:
        ok(f"blocked.{path[:18]}", path in blocked_ids)

    ok("closure.pass", closure.get("dryrun_and_review_pass") is True)
    ok("closure.final", closure.get("final_decision") == FINAL_DECISION_GO)
    ok("closure.next", closure.get("recommended_next_phase") == NEXT_PHASE_GO)

    ok("next.ready", next_route.get("ready_for_information_integration_layer_planning") is True)
    ok("next.phase", next_route.get("selected_next_phase") == NEXT_PHASE_GO)

    for claim in NON_CLAIMS:
        ok(f"non_claim.{claim[:18]}", claim in (non_claims.get("non_claims") or []))

    total = len(checks)
    passed = sum(1 for c in checks if c["passed"])
    min_checks = MIN_CHECKS if MIN_CHECKS else total
    verifier = "GO" if passed == total and passed >= min_checks else "NO_GO"
    report = {
        "phase": PHASE_ID,
        "verifier": verifier,
        "checks_passed": passed,
        "checks_total": total,
        "min_checks": min_checks,
        "dryrun_and_review_pass": summary.get("dryrun_and_review_pass"),
        "final_decision": summary.get("final_decision"),
        "recommended_next_phase": summary.get("recommended_next_phase"),
        "checks": checks,
    }
    (root / "verifier_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps({"verifier": verifier, "checks_passed": passed, "checks_total": total}))
    return 0 if verifier == "GO" else 1


if __name__ == "__main__":
    raise SystemExit(main())
