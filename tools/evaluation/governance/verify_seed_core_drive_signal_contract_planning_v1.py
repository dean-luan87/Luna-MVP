#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Seed Core Drive Signal Contract Planning v1."""

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
    SEED_CORE_COMPONENTS,
)
from capabilities.governance.seed_core_drive_signal_contract_planning_v1 import (
    AUTONOMOUS_OBSERVATION_CONFIRMATIONS,
    AUTONOMOUS_OBSERVATION_COVERAGE,
    BOUNDARY_FALSE,
    BOUNDARY_TRUE,
    CONFLICT_OUTPUT_REQUIREMENTS,
    CONFLICT_TYPES,
    DECISION_BOUNDARY_CONFIRMATIONS,
    DRIVE_SIGNAL_CANDIDATE_FIELDS,
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
    SEED_CORE_HINT_CANDIDATE_FIELDS,
    SEED_CORE_SIGNAL_CANDIDATE_FIELDS,
    SIGNAL_TAXONOMY,
    SIGNAL_TAXONOMY_CONFIRMATIONS,
    SURVIVAL_DRIVE_CONFIRMATIONS,
    SURVIVAL_DRIVE_COVERAGE,
    SYSTEM_OPTIMIZATION_CONFIRMATIONS,
    SYSTEM_OPTIMIZATION_COVERAGE,
    TASK_DRIVE_CONFIRMATIONS,
    TASK_DRIVE_COVERAGE,
    TRACEABILITY_FIELDS,
    UPSTREAM_SC_DR_FINAL,
    UPSTREAM_SC_DR_NEXT,
    ZONE_HANDOFF_PLAN,
)
from capabilities.governance.seed_core_pluggable_layer_architecture_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as SC_DR_FINAL,
    NEXT_PHASE_GO as SC_DR_NEXT,
)

MIN_CHECKS = 340

REQUIRED = (
    "drive_signal_contract_planning_policy_v1.json",
    "seed_core_architecture_input_review_v1.json",
    "seed_core_signal_taxonomy_v1.json",
    "drive_signal_candidate_contract_v1.json",
    "seed_core_signal_candidate_contract_v1.json",
    "seed_core_hint_candidate_contract_v1.json",
    "survival_drive_signal_contract_v1.json",
    "task_drive_signal_contract_v1.json",
    "resource_governance_signal_contract_v1.json",
    "health_management_signal_contract_v1.json",
    "system_optimization_signal_contract_v1.json",
    "autonomous_world_observation_signal_contract_v1.json",
    "emotion_engine_signal_contract_v1.json",
    "evolutionary_recursion_signal_contract_v1.json",
    "drive_signal_priority_policy_v1.json",
    "drive_signal_conflict_policy_v1.json",
    "drive_signal_to_cognitive_zone_handoff_plan_v1.json",
    "drive_signal_to_information_integration_plan_v1.json",
    "drive_signal_to_decision_center_boundary_plan_v1.json",
    "drive_signal_to_controlled_runtime_boundary_plan_v1.json",
    "drive_signal_traceability_policy_v1.json",
    "drive_signal_boundary_matrix_v1.json",
    "drive_signal_dryrun_plan_v1.json",
    "non_claims_register_v1.json",
    "drive_signal_contract_planning_decision_v1.json",
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
    sc_dr_root = Path(args.seed_core_pluggable_dryrun_root)
    cz_dr_root = Path(args.cognitive_zoning_dryrun_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in REQUIRED:
        ok(f"file.{f}", (root / f).is_file())

    sc_dr_vr = _load(sc_dr_root / "verifier_report.json")
    sc_dr_sm = _load(sc_dr_root / "summary.json")
    cz_dr_vr = _load(cz_dr_root / "verifier_report.json")

    ok("upstream.sc_dr_go", sc_dr_vr.get("verifier") == "GO")
    ok("upstream.sc_dr_final", sc_dr_sm.get("final_decision") == UPSTREAM_SC_DR_FINAL)
    ok("upstream.sc_dr_final_expected", sc_dr_sm.get("final_decision") == SC_DR_FINAL)
    ok("upstream.sc_dr_next", sc_dr_sm.get("recommended_next_phase") == UPSTREAM_SC_DR_NEXT)
    ok("upstream.sc_dr_next_expected", sc_dr_sm.get("recommended_next_phase") == SC_DR_NEXT)
    ok("upstream.cz_dr_go", cz_dr_vr.get("verifier") == "GO")

    summary = _load(root / "summary.json")
    policy = _load(root / "drive_signal_contract_planning_policy_v1.json")
    input_review = _load(root / "seed_core_architecture_input_review_v1.json")
    taxonomy = _load(root / "seed_core_signal_taxonomy_v1.json")
    drive_contract = _load(root / "drive_signal_candidate_contract_v1.json")
    seed_signal = _load(root / "seed_core_signal_candidate_contract_v1.json")
    hint_contract = _load(root / "seed_core_hint_candidate_contract_v1.json")
    survival = _load(root / "survival_drive_signal_contract_v1.json")
    task = _load(root / "task_drive_signal_contract_v1.json")
    resource = _load(root / "resource_governance_signal_contract_v1.json")
    health = _load(root / "health_management_signal_contract_v1.json")
    optimization = _load(root / "system_optimization_signal_contract_v1.json")
    observation = _load(root / "autonomous_world_observation_signal_contract_v1.json")
    emotion = _load(root / "emotion_engine_signal_contract_v1.json")
    evolution = _load(root / "evolutionary_recursion_signal_contract_v1.json")
    priority = _load(root / "drive_signal_priority_policy_v1.json")
    conflict = _load(root / "drive_signal_conflict_policy_v1.json")
    handoff = _load(root / "drive_signal_to_cognitive_zone_handoff_plan_v1.json")
    integration = _load(root / "drive_signal_to_information_integration_plan_v1.json")
    decision = _load(root / "drive_signal_to_decision_center_boundary_plan_v1.json")
    runtime_bound = _load(root / "drive_signal_to_controlled_runtime_boundary_plan_v1.json")
    traceability = _load(root / "drive_signal_traceability_policy_v1.json")
    boundary = _load(root / "drive_signal_boundary_matrix_v1.json")
    dryrun_plan = _load(root / "drive_signal_dryrun_plan_v1.json")
    planning_decision = _load(root / "drive_signal_contract_planning_decision_v1.json")
    non_claims = _load(root / "non_claims_register_v1.json")

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("scope") == SCOPE)
    ok("summary.pass", summary.get("planning_pass") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)

    for field in BOUNDARY_TRUE:
        ok(f"true.{field}", summary.get(field) is True)
    for field in BOUNDARY_FALSE:
        ok(f"false.{field}", summary.get(field) is False)

    ok("policy.not_runtime", policy.get("planning_not_runtime_not_execute") is True)
    ok("policy.taxonomy16", policy.get("signal_taxonomy_count") == 16)

    ok("input.pass", input_review.get("review_pass") is True)
    ok("input.seed7", input_review.get("seed_core_7_components_validated") is True)
    ok("input.evo_proposal", input_review.get("emotion_engine_and_evolutionary_recursion_proposal_only") is True)
    ok("input.continuity", input_review.get("personal_continuity_validated") is True)
    ok("input.pluggable", input_review.get("pluggable_layer_validated") is True)
    ok("input.no_leakage", input_review.get("no_runtime_leakage_in_upstream") is True)

    ok("tax.count16", taxonomy.get("signal_type_count") == 16)
    for sig in SIGNAL_TAXONOMY:
        ok(f"tax.{sig[:18]}", sig in (taxonomy.get("signal_types") or []))
    for conf in SIGNAL_TAXONOMY_CONFIRMATIONS:
        ok(f"tax.conf.{conf[:18]}", conf in (taxonomy.get("confirmations") or []))

    for field in DRIVE_SIGNAL_CANDIDATE_FIELDS:
        ok(f"drive.field.{field[:18]}", field in (drive_contract.get("required_fields") or []))
    ok("drive.candidate", drive_contract.get("defaults", {}).get("candidate_only") is True)
    ok("drive.not_decision", drive_contract.get("defaults", {}).get("not_decision") is True)
    ok("drive.not_action", drive_contract.get("defaults", {}).get("not_action") is True)
    ok("drive.not_output", drive_contract.get("defaults", {}).get("not_user_output") is True)
    ok("drive.runtime_false", drive_contract.get("defaults", {}).get("runtime_enable_allowed") is False)

    for field in SEED_CORE_SIGNAL_CANDIDATE_FIELDS:
        ok(f"seed_sig.field.{field[:18]}", field in (seed_signal.get("required_fields") or []))
    ok("seed_sig.runtime_false", seed_signal.get("defaults", {}).get("runtime_enable_allowed") is False)

    for field in SEED_CORE_HINT_CANDIDATE_FIELDS:
        ok(f"hint.field.{field[:18]}", field in (hint_contract.get("required_fields") or []))
    ok("hint.non_binding", hint_contract.get("defaults", {}).get("non_binding") is True)
    ok("hint.decision_req", hint_contract.get("defaults", {}).get("decision_required") is True)

    for cov in SURVIVAL_DRIVE_COVERAGE:
        ok(f"survival.cov.{cov[:18]}", cov in (survival.get("coverage") or []))
    for conf in SURVIVAL_DRIVE_CONFIRMATIONS:
        ok(f"survival.conf.{conf[:18]}", conf in (survival.get("confirmations") or []))

    for cov in TASK_DRIVE_COVERAGE:
        ok(f"task.cov.{cov[:18]}", cov in (task.get("coverage") or []))
    for conf in TASK_DRIVE_CONFIRMATIONS:
        ok(f"task.conf.{conf[:18]}", conf in (task.get("confirmations") or []))

    for cov in RESOURCE_GOVERNANCE_COVERAGE:
        ok(f"resource.cov.{cov[:18]}", cov in (resource.get("coverage") or []))
    for conf in RESOURCE_GOVERNANCE_CONFIRMATIONS:
        ok(f"resource.conf.{conf[:18]}", conf in (resource.get("confirmations") or []))

    for cov in HEALTH_MANAGEMENT_COVERAGE:
        ok(f"health.cov.{cov[:18]}", cov in (health.get("coverage") or []))
    for conf in HEALTH_MANAGEMENT_CONFIRMATIONS:
        ok(f"health.conf.{conf[:18]}", conf in (health.get("confirmations") or []))

    for cov in SYSTEM_OPTIMIZATION_COVERAGE:
        ok(f"opt.cov.{cov[:18]}", cov in (optimization.get("coverage") or []))
    for conf in SYSTEM_OPTIMIZATION_CONFIRMATIONS:
        ok(f"opt.conf.{conf[:18]}", conf in (optimization.get("confirmations") or []))

    for cov in AUTONOMOUS_OBSERVATION_COVERAGE:
        ok(f"obs.cov.{cov[:18]}", cov in (observation.get("coverage") or []))
    for conf in AUTONOMOUS_OBSERVATION_CONFIRMATIONS:
        ok(f"obs.conf.{conf[:18]}", conf in (observation.get("confirmations") or []))

    for cov in EMOTION_ENGINE_COVERAGE:
        ok(f"emotion.cov.{cov[:18]}", cov in (emotion.get("coverage") or []))
    for conf in EMOTION_ENGINE_CONFIRMATIONS:
        ok(f"emotion.conf.{conf[:18]}", conf in (emotion.get("confirmations") or []))

    for cov in EVOLUTIONARY_RECURSION_COVERAGE:
        ok(f"evo.cov.{cov[:18]}", cov in (evolution.get("coverage") or []))
    for conf in EVOLUTIONARY_RECURSION_CONFIRMATIONS:
        ok(f"evo.conf.{conf[:18]}", conf in (evolution.get("confirmations") or []))
    ok("evo.proposal_only", evolution.get("proposal_only") is True)

    ok("priority.count9", priority.get("level_count") == 9)
    for pl in PRIORITY_LEVELS:
        ok(f"priority.{pl['rank']}", any(
            p.get("rank") == pl["rank"] for p in (priority.get("priority_levels") or [])
        ))
    for conf in PRIORITY_CONFIRMATIONS:
        ok(f"priority.conf.{conf[:18]}", conf in (priority.get("confirmations") or []))

    ok("conflict.count7", conflict.get("conflict_count") == 7)
    for ct in CONFLICT_TYPES:
        ok(f"conflict.{ct['conflict_id'][:18]}", any(
            c.get("conflict_id") == ct["conflict_id"] for c in (conflict.get("conflict_types") or [])
        ))
    for req in CONFLICT_OUTPUT_REQUIREMENTS:
        ok(f"conflict.req.{req[:18]}", req in (conflict.get("output_requirements") or []))

    ok("handoff.count8", handoff.get("zone_count") == 8)
    for zone_name in COGNITIVE_ZONES:
        ok(f"handoff.zone.{zone_name[:18]}", zone_name in (handoff.get("cognitive_zones") or []))
    for zh in ZONE_HANDOFF_PLAN:
        ok(f"handoff.{zh['zone'][:18]}", any(
            h.get("zone") == zh["zone"] for h in (handoff.get("zone_handoffs") or [])
        ))

    for conf in INTEGRATION_PLAN_CONFIRMATIONS:
        ok(f"integration.{conf[:18]}", conf in (integration.get("confirmations") or []))

    for conf in DECISION_BOUNDARY_CONFIRMATIONS:
        ok(f"decision.{conf[:18]}", conf in (decision.get("confirmations") or []))

    for conf in RUNTIME_BOUNDARY_CONFIRMATIONS:
        ok(f"runtime.{conf[:18]}", conf in (runtime_bound.get("confirmations") or []))

    ok("trace.preserve", traceability.get("all_signals_must_preserve") is True)
    for field in TRACEABILITY_FIELDS:
        ok(f"trace.{field[:18]}", field in (traceability.get("required_fields") or []))

    ok("boundary.pass", boundary.get("boundary_pass") is True)
    for field in BOUNDARY_FALSE:
        ok(f"boundary.{field}", boundary.get("boundary_fields", {}).get(field) is False)

    ok("dryrun.next", dryrun_plan.get("next_phase") == NEXT_PHASE_GO)

    ok("plan_decision.pass", planning_decision.get("planning_pass") is True)
    ok("plan_decision.final", planning_decision.get("final_decision") == FINAL_DECISION_GO)
    ok("plan_decision.next", planning_decision.get("recommended_next_phase") == NEXT_PHASE_GO)

    for comp in SEED_CORE_COMPONENTS:
        ok(f"policy.comp.{comp[:18]}", comp in (policy.get("seed_core_components") or []))

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
        "planning_pass": summary.get("planning_pass"),
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
