#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Vision OCR Navigation Task Mainline Resume Planning v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.luna_constitution_capability_bus_governance_baseline_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as CB_DR_FINAL,
    NEXT_PHASE_GO as CB_DR_NEXT,
)
from capabilities.governance.luna_constitution_capability_bus_governance_baseline_planning_v1 import (
    HEALTH_OVERSIGHT_PRINCIPLE,
)
from capabilities.governance.vision_ocr_navigation_task_mainline_resume_v1 import (
    BOUNDARY_FALSE,
    BOUNDARY_TRUE,
    CANDIDATE_FLOW_STEPS,
    CAPABILITY_BUS_BINDING_CONFIRMATIONS,
    DECISION_CENTER_BINDING_CONFIRMATIONS,
    DRIVE_SIGNAL_BINDING_CONFIRMATIONS,
    EVIDENCE_FLOW_ITEMS,
    FINAL_DECISION_GO,
    FIRST_PERSON_VISION_ITEMS,
    II_BINDING_CONFIRMATIONS,
    MAINLINE_RESUME_CONFIRMATIONS,
    NAVIGATION_TASK_ITEMS,
    NEXT_PHASE_GO,
    NON_CLAIMS,
    OCR_CHAIN_ITEMS,
    PHASE_ID,
    RUNTIME_DEFERMENT_ITEMS,
    SAFETY_PRIORITY_CONFIRMATIONS,
    SCOPE,
    TASK_ROUTE_FLOW_ITEMS,
    UPSTREAM_CB_DR_FINAL,
    UPSTREAM_CB_DR_NEXT,
)

MIN_CHECKS = 201

REQUIRED = (
    "vision_ocr_navigation_task_mainline_resume_policy_v1.json",
    "constitution_bus_governance_input_review_v1.json",
    "mainline_resume_scope_definition_v1.json",
    "first_person_vision_chain_reentry_plan_v1.json",
    "ocr_context_chain_reentry_plan_v1.json",
    "navigation_task_chain_reentry_plan_v1.json",
    "capability_bus_binding_for_vision_ocr_navigation_v1.json",
    "seed_core_drive_signal_binding_for_navigation_v1.json",
    "information_integration_binding_for_navigation_v1.json",
    "decision_center_binding_for_navigation_v1.json",
    "controlled_runtime_deferment_for_vision_ocr_navigation_v1.json",
    "vision_ocr_navigation_candidate_flow_v1.json",
    "vision_ocr_navigation_evidence_flow_v1.json",
    "task_route_context_flow_v1.json",
    "safety_survival_navigation_priority_policy_v1.json",
    "mainline_resume_boundary_matrix_v1.json",
    "mainline_resume_next_phase_plan_v1.json",
    "non_claims_register_v1.json",
    "vision_ocr_navigation_task_mainline_resume_decision_v1.json",
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
            "vision_ocr_navigation_task_mainline_resume"
        ),
    )
    p.add_argument(
        "--constitution-bus-dryrun-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "luna_constitution_capability_bus_governance_baseline_dryrun_and_review"
        ),
    )
    args = p.parse_args()
    root = Path(args.output_root)
    cb_dr_root = Path(args.constitution_bus_dryrun_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in REQUIRED:
        ok(f"file.{f}", (root / f).is_file())

    cb_dr_vr = _load(cb_dr_root / "verifier_report.json")
    cb_dr_sm = _load(cb_dr_root / "summary.json")

    ok("upstream.cb_dr_go", cb_dr_vr.get("verifier") == "GO")
    ok("upstream.cb_dr_final", cb_dr_sm.get("final_decision") == UPSTREAM_CB_DR_FINAL)
    ok("upstream.cb_dr_final_expected", cb_dr_sm.get("final_decision") == CB_DR_FINAL)
    ok("upstream.cb_dr_next", cb_dr_sm.get("recommended_next_phase") == UPSTREAM_CB_DR_NEXT)
    ok("upstream.cb_dr_next_expected", cb_dr_sm.get("recommended_next_phase") == CB_DR_NEXT)

    summary = _load(root / "summary.json")
    policy = _load(root / "vision_ocr_navigation_task_mainline_resume_policy_v1.json")
    input_review = _load(root / "constitution_bus_governance_input_review_v1.json")
    scope = _load(root / "mainline_resume_scope_definition_v1.json")
    vision = _load(root / "first_person_vision_chain_reentry_plan_v1.json")
    ocr = _load(root / "ocr_context_chain_reentry_plan_v1.json")
    navigation = _load(root / "navigation_task_chain_reentry_plan_v1.json")
    bus_binding = _load(root / "capability_bus_binding_for_vision_ocr_navigation_v1.json")
    drive_binding = _load(root / "seed_core_drive_signal_binding_for_navigation_v1.json")
    ii_binding = _load(root / "information_integration_binding_for_navigation_v1.json")
    decision_binding = _load(root / "decision_center_binding_for_navigation_v1.json")
    runtime_def = _load(root / "controlled_runtime_deferment_for_vision_ocr_navigation_v1.json")
    candidate_flow = _load(root / "vision_ocr_navigation_candidate_flow_v1.json")
    evidence_flow = _load(root / "vision_ocr_navigation_evidence_flow_v1.json")
    task_route = _load(root / "task_route_context_flow_v1.json")
    safety = _load(root / "safety_survival_navigation_priority_policy_v1.json")
    boundary = _load(root / "mainline_resume_boundary_matrix_v1.json")
    next_plan = _load(root / "mainline_resume_next_phase_plan_v1.json")
    resume_decision = _load(root / "vision_ocr_navigation_task_mainline_resume_decision_v1.json")
    non_claims = _load(root / "non_claims_register_v1.json")

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("scope") == SCOPE)
    ok("summary.pass", summary.get("planning_pass") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("summary.baseline_closed", summary.get("luna_2_0_governance_baseline_closed") is True)

    for field in BOUNDARY_TRUE:
        ok(f"true.{field}", summary.get(field) is True)
    for field in BOUNDARY_FALSE:
        ok(f"false.{field}", summary.get(field) is False)

    ok("policy.not_runtime", policy.get("planning_not_runtime_not_execute") is True)
    ok("policy.mainline", policy.get("mainline") == "first_person_vision_ocr_navigation_task")

    ok("input.pass", input_review.get("review_pass") is True)
    ok("input.cb_go", input_review.get("constitution_bus_dryrun_verifier") == "GO")
    ok("input.cb_final", input_review.get("constitution_bus_dryrun_final_decision") == UPSTREAM_CB_DR_FINAL)
    ok("input.ii_go", input_review.get("information_integration_dryrun_verifier") == "GO")
    ok("input.ds_go", input_review.get("drive_signal_dryrun_verifier") == "GO")
    ok("input.sc_go", input_review.get("seed_core_pluggable_dryrun_verifier") == "GO")
    ok("input.cz_go", input_review.get("cognitive_zoning_dryrun_verifier") == "GO")
    ok("input.provider_go", input_review.get("provider_abstraction_verifier") == "GO")
    ok("input.cr_go", input_review.get("controlled_runtime_verifier") == "GO")
    ok("input.health_written", input_review.get("health_oversight_written") is True)
    ok("input.health_principle", input_review.get("health_oversight_external_principle") == HEALTH_OVERSIGHT_PRINCIPLE)
    ok("input.no_leakage", input_review.get("no_runtime_leakage_in_upstream") is True)

    ok("scope.count8", scope.get("confirmation_count") == 8)
    for conf in MAINLINE_RESUME_CONFIRMATIONS:
        ok(f"scope.{conf[:18]}", conf in (scope.get("confirmations") or []))

    ok("vision.count8", vision.get("item_count") == 8)
    ok("vision.candidate", vision.get("candidate_only") is True)
    for item in FIRST_PERSON_VISION_ITEMS:
        ok(f"vision.{item[:18]}", item in (vision.get("chain_items") or []))

    ok("ocr.count8", ocr.get("item_count") == 8)
    ok("ocr.candidate", ocr.get("candidate_only") is True)
    for item in OCR_CHAIN_ITEMS:
        ok(f"ocr.{item[:18]}", item in (ocr.get("chain_items") or []))

    ok("nav.count8", navigation.get("item_count") == 8)
    ok("nav.candidate", navigation.get("candidate_only") is True)
    for item in NAVIGATION_TASK_ITEMS:
        ok(f"nav.{item[:18]}", item in (navigation.get("chain_items") or []))

    ok("bus.count7", bus_binding.get("confirmation_count") == 7)
    ok("bus.health_principle", bus_binding.get("health_oversight_principle") == HEALTH_OVERSIGHT_PRINCIPLE)
    for conf in CAPABILITY_BUS_BINDING_CONFIRMATIONS:
        ok(f"bus.{conf[:18]}", conf in (bus_binding.get("confirmations") or []))

    ok("drive.count7", drive_binding.get("confirmation_count") == 7)
    for conf in DRIVE_SIGNAL_BINDING_CONFIRMATIONS:
        ok(f"drive.{conf[:18]}", conf in (drive_binding.get("confirmations") or []))

    ok("ii.count6", ii_binding.get("confirmation_count") == 6)
    for conf in II_BINDING_CONFIRMATIONS:
        ok(f"ii.{conf[:18]}", conf in (ii_binding.get("confirmations") or []))

    ok("decision.count5", decision_binding.get("confirmation_count") == 5)
    for conf in DECISION_CENTER_BINDING_CONFIRMATIONS:
        ok(f"decision.{conf[:18]}", conf in (decision_binding.get("confirmations") or []))

    ok("runtime.count8", runtime_def.get("item_count") == 8)
    ok("runtime.deferred", runtime_def.get("controlled_runtime_still_deferred") is True)
    for item in RUNTIME_DEFERMENT_ITEMS:
        ok(f"runtime.{item[:18]}", item in (runtime_def.get("deferred_items") or []))

    ok("flow.count7", candidate_flow.get("step_count") == 7)
    ok("flow.candidate", candidate_flow.get("candidate_only") is True)
    ok("flow.no_runtime", candidate_flow.get("no_runtime_now") is True)
    for step in CANDIDATE_FLOW_STEPS:
        ok(f"flow.{step[:18]}", step in (candidate_flow.get("flow_steps") or []))

    ok("evidence.count7", evidence_flow.get("item_count") == 7)
    ok("evidence.not_fact", evidence_flow.get("not_fact_by_default") is True)
    for item in EVIDENCE_FLOW_ITEMS:
        ok(f"evidence.{item[:18]}", item in (evidence_flow.get("evidence_items") or []))

    ok("route.count8", task_route.get("item_count") == 8)
    for item in TASK_ROUTE_FLOW_ITEMS:
        ok(f"route.{item[:18]}", item in (task_route.get("flow_items") or []))

    ok("safety.count6", safety.get("confirmation_count") == 6)
    for conf in SAFETY_PRIORITY_CONFIRMATIONS:
        ok(f"safety.{conf[:18]}", conf in (safety.get("confirmations") or []))

    ok("boundary.pass", boundary.get("boundary_pass") is True)
    for field in BOUNDARY_FALSE:
        ok(f"boundary.{field}", boundary.get("boundary_fields", {}).get(field) is False)

    ok("next.phase", next_plan.get("next_phase") == NEXT_PHASE_GO)
    ok("next.controlled", next_plan.get("controlled_first") == "candidate flow before runtime")

    ok("decision.pass", resume_decision.get("planning_pass") is True)
    ok("decision.final", resume_decision.get("final_decision") == FINAL_DECISION_GO)
    ok("decision.next", resume_decision.get("recommended_next_phase") == NEXT_PHASE_GO)

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
