#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Scenario Model Capability Roadmap Current State Inventory DryRunAndReview v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.layered_governance_mapping_v1 import ADDENDUM_ID
from capabilities.governance.layered_capability_stack_standard_v1 import STANDARD_ID
from capabilities.governance.scenario_model_capability_roadmap_current_state_inventory_dryrun_and_review_v1 import (
    BLOCKED_PATHS,
    BOUNDARY_FALSE,
    BOUNDARY_TRUE,
    CAPABILITY_DOMAIN_IDS,
    DOMAIN_REVIEW_FIELDS,
    EXTERNAL_CANDIDATE_REGISTER_FIELDS,
    FINAL_DECISION_GO,
    MIDPLATFORM_BINDING_FIELDS,
    MODULE_PROFILE_FIELDS,
    NEXT_PHASE_GO,
    NON_CLAIMS,
    PHASE_ID,
    ROADMAP_RISKS,
    SCOPE,
)
from capabilities.governance.scenario_model_capability_roadmap_current_state_inventory_planning_v1 import (
    FINAL_DECISION_GO as PLANNING_FINAL_GO,
    PHASE_ID as PLANNING_PHASE_ID,
)

MIN_CHECKS = 218

REQUIRED = (
    "scenario_model_capability_roadmap_inventory_dryrun_review_policy_v1.json",
    "planning_input_review_v1.json",
    "scenario_model_capability_roadmap_candidate_v1.json",
    "capability_domain_inventory_review_v1.json",
    "current_model_asset_inventory_review_v1.json",
    "goal_stage_to_capability_domain_review_v1.json",
    "vision_scene_understanding_roadmap_review_v1.json",
    "ocr_text_reading_roadmap_review_v1.json",
    "tts_voice_output_roadmap_review_v1.json",
    "asr_voice_input_roadmap_review_v1.json",
    "map_navigation_roadmap_review_v1.json",
    "spatiotemporal_world_continuity_roadmap_review_v1.json",
    "memory_personal_continuity_roadmap_review_v1.json",
    "emotion_engine_roadmap_review_v1.json",
    "evolutionary_recursion_roadmap_review_v1.json",
    "provider_model_management_roadmap_review_v1.json",
    "output_gate_chain_roadmap_review_v1.json",
    "health_whitebox_validation_governance_roadmap_review_v1.json",
    "model_source_strategy_review_v1.json",
    "candidate_register_review_v1.json",
    "module_local_model_profile_contract_review_v1.json",
    "midplatform_model_governance_binding_contract_review_v1.json",
    "model_input_output_contract_review_v1.json",
    "model_quality_acceptance_criteria_review_v1.json",
    "model_versioning_replacement_policy_review_v1.json",
    "current_gap_and_next_action_review_v1.json",
    "roadmap_risk_register_review_v1.json",
    "roadmap_boundary_audit_v1.json",
    "roadmap_blocked_path_result_v1.json",
    "roadmap_closure_decision_v1.json",
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
            "scenario_model_capability_roadmap_current_state_inventory_dryrun_and_review"
        ),
    )
    p.add_argument(
        "--planning-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "scenario_model_capability_roadmap_current_state_inventory_planning"
        ),
    )
    p.add_argument(
        "--closure-review-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "first_person_scene_understanding_output_chain_closure_review"
        ),
    )
    args = p.parse_args()
    root = Path(args.output_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in REQUIRED:
        ok(f"file.{f}", (root / f).is_file())

    plan_vr = _load(Path(args.planning_root) / "verifier_report.json")
    plan_sm = _load(Path(args.planning_root) / "summary.json")
    closure_vr = _load(Path(args.closure_review_root) / "verifier_report.json")

    ok("upstream.plan_go", plan_vr.get("verifier") == "GO")
    ok("upstream.plan_final", plan_sm.get("final_decision") == PLANNING_FINAL_GO)
    ok("upstream.closure_pending", plan_sm.get("closure_pending") is False)
    ok("upstream.closure_go", closure_vr.get("verifier") == "GO")

    summary = _load(root / "summary.json")
    candidate = _load(root / "scenario_model_capability_roadmap_candidate_v1.json")
    domain_review = _load(root / "capability_domain_inventory_review_v1.json")
    asset_review = _load(root / "current_model_asset_inventory_review_v1.json")
    goal_review = _load(root / "goal_stage_to_capability_domain_review_v1.json")
    vision = _load(root / "vision_scene_understanding_roadmap_review_v1.json")
    ocr = _load(root / "ocr_text_reading_roadmap_review_v1.json")
    tts = _load(root / "tts_voice_output_roadmap_review_v1.json")
    asr = _load(root / "asr_voice_input_roadmap_review_v1.json")
    nav = _load(root / "map_navigation_roadmap_review_v1.json")
    st = _load(root / "spatiotemporal_world_continuity_roadmap_review_v1.json")
    memory = _load(root / "memory_personal_continuity_roadmap_review_v1.json")
    emotion = _load(root / "emotion_engine_roadmap_review_v1.json")
    evolution = _load(root / "evolutionary_recursion_roadmap_review_v1.json")
    provider = _load(root / "provider_model_management_roadmap_review_v1.json")
    output_g = _load(root / "output_gate_chain_roadmap_review_v1.json")
    health = _load(root / "health_whitebox_validation_governance_roadmap_review_v1.json")
    source = _load(root / "model_source_strategy_review_v1.json")
    cand = _load(root / "candidate_register_review_v1.json")
    module_r = _load(root / "module_local_model_profile_contract_review_v1.json")
    mid_r = _load(root / "midplatform_model_governance_binding_contract_review_v1.json")
    io_r = _load(root / "model_input_output_contract_review_v1.json")
    qual_r = _load(root / "model_quality_acceptance_criteria_review_v1.json")
    ver_r = _load(root / "model_versioning_replacement_policy_review_v1.json")
    gap_r = _load(root / "current_gap_and_next_action_review_v1.json")
    risk_r = _load(root / "roadmap_risk_register_review_v1.json")
    boundary = _load(root / "roadmap_boundary_audit_v1.json")
    blocked = _load(root / "roadmap_blocked_path_result_v1.json")
    closure = _load(root / "roadmap_closure_decision_v1.json")
    next_route = _load(root / "next_route_readiness_decision_v1.json")
    planning_in = _load(root / "planning_input_review_v1.json")

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("scope") == SCOPE)
    ok("summary.pass", summary.get("dryrun_and_review_pass") is True)
    ok("summary.domains12", summary.get("capability_domain_count") == 12)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)

    for field in BOUNDARY_TRUE:
        ok(f"true.{field}", summary.get(field) is True)
    for field in BOUNDARY_FALSE:
        ok(f"false.{field}", summary.get(field) is False)

    ok("planning_in.pass", planning_in.get("review_pass") is True)

    ok("candidate.roadmap_id", candidate.get("roadmap_id") == "scenario_model_capability_roadmap_current_state_inventory_v1")
    ok("candidate.type", candidate.get("roadmap_type") == "model_capability_roadmap_with_current_state_inventory")
    ok("candidate.source", candidate.get("planning_source_phase") == PLANNING_PHASE_ID)
    ok("candidate.domains12", candidate.get("capability_domain_count") == 12)
    ok("candidate.goals6", candidate.get("goal_stage_count") >= 6)
    ok("candidate.asset_inv", candidate.get("includes_current_asset_inventory") is True)
    ok("candidate.gap_matrix", candidate.get("includes_gap_next_action_matrix") is True)
    ok("candidate.module_profile", candidate.get("includes_module_local_model_profile_contract") is True)
    ok("candidate.mid_binding", candidate.get("includes_midplatform_governance_binding_contract") is True)
    ok("candidate.not_selected", candidate.get("model_selected_now") is False)
    ok("candidate.not_invoked", candidate.get("model_invoked_now") is False)
    ok("candidate.no_runtime", candidate.get("runtime_enabled_now") is False)
    ok("candidate.candidate_only", candidate.get("candidate_only") is True)

    ok("domain_review.pass", domain_review.get("review_pass") is True)
    ok("domain_review.count12", domain_review.get("domain_count") == 12)
    ok("domain_review.all_present", domain_review.get("all_domains_present") is True)
    for did in CAPABILITY_DOMAIN_IDS:
        dr = next(
            (d for d in (domain_review.get("domain_reviews") or []) if d.get("capability_domain_id") == did),
            {},
        )
        ok(f"domain.{did[:16]}.struct", dr.get("structure_pass") is True)
    for field in DOMAIN_REVIEW_FIELDS:
        ok(f"domain.field.{field[:12]}", field in (domain_review.get("required_fields") or []))

    ok("asset_review.pass", asset_review.get("review_pass") is True)
    ok("goal_review.pass", goal_review.get("review_pass") is True)
    ok("goal_review.ge6", goal_review.get("goal_stage_count_ge_6") is True)

    for review, name in (
        (vision, "vision"), (ocr, "ocr"), (tts, "tts"), (asr, "asr"), (nav, "nav"),
        (st, "st"), (memory, "memory"), (emotion, "emotion"), (evolution, "evolution"),
        (provider, "provider"), (output_g, "output"), (health, "health"),
    ):
        ok(f"{name}.review_pass", review.get("review_pass") is True)

    ok("source.review_pass", source.get("review_pass") is True)
    ok("cand.review_pass", cand.get("review_pass") is True)
    ok("module.review_pass", module_r.get("review_pass") is True)
    ok("mid.review_pass", mid_r.get("review_pass") is True)
    ok("io.review_pass", io_r.get("review_pass") is True)
    ok("qual.review_pass", qual_r.get("review_pass") is True)
    ok("ver.review_pass", ver_r.get("review_pass") is True)
    ok("gap.review_pass", gap_r.get("review_pass") is True)
    ok("risk.review_pass", risk_r.get("review_pass") is True)

    for field in MODULE_PROFILE_FIELDS:
        ok(f"module.field.{field[:12]}", field in (module_r.get("required_fields") or []))
    for field in MIDPLATFORM_BINDING_FIELDS:
        ok(f"mid.field.{field[:12]}", field in (mid_r.get("required_fields") or []))

    ok("mid.stack", mid_r.get("required_fields") is not None)
    ok("boundary.audit", boundary.get("audit_pass") is True)
    for field in BOUNDARY_FALSE:
        ok(f"boundary.{field[:12]}", boundary.get("boundary_fields", {}).get(field) is False)

    ok("blocked.all", blocked.get("all_blocked") is True)
    ok("blocked.count15", blocked.get("blocked_count") == 15)
    for path in BLOCKED_PATHS:
        ok(
            f"blocked.{path[:18]}",
            any(
                b.get("path_id") == path and b.get("status") == "blocked"
                for b in (blocked.get("blocked_paths") or [])
            ),
        )

    ok("closure.pass", closure.get("dryrun_and_review_pass") is True)
    ok("closure.final", closure.get("final_decision") == FINAL_DECISION_GO)
    ok("closure.next", closure.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("next.ready", next_route.get("ready_for_model_profile_registry_planning") is True)
    ok("next.phase", next_route.get("selected_next_phase") == NEXT_PHASE_GO)

    for risk in ROADMAP_RISKS:
        ok(f"risk.{risk[:16]}", risk_r.get("review_pass") is True)

    for claim in NON_CLAIMS:
        ok(f"non_claim.{claim[:18]}", claim in (_load(root / "non_claims_register_v1.json").get("non_claims") or []))

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
