#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify First Person Vision Navigation Candidate Flow Planning v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.first_person_vision_navigation_candidate_flow_planning_v1 import (
    BOUNDARY_FALSE,
    BOUNDARY_TRUE,
    DRIVE_OBSERVATION_PRIORITY_CONFIRMATIONS,
    FINAL_DECISION_GO,
    II_HANDOFF_CONFIRMATIONS,
    MAP_LOCATION_FIELDS,
    NAVIGATION_TASK_FIELDS,
    NEXT_PHASE_GO,
    NON_CLAIMS,
    OCR_RESULT_FIELDS,
    OBSTACLE_FIELDS,
    PERCEPTION_ZONE_CONFIRMATIONS,
    PHASE_ID,
    REQUIRED_OBSERVATION_FIELDS,
    RISK_CONTEXT_FIELDS,
    ROUTE_CONTEXT_FIELDS,
    SCENE_CONTEXT_FIELDS,
    SIGNAGE_CONTEXT_FIELDS,
    SCOPE,
    TASK_ROUTE_PROGRESS_FIELDS,
    TEXT_REGION_FIELDS,
    TRACEABILITY_FIELDS,
    UPSTREAM_MAINLINE_FINAL,
    UPSTREAM_MAINLINE_NEXT,
    VISUAL_EVIDENCE_FIELDS,
    VISUAL_OBSERVATION_FIELDS,
    VISUAL_OCR_MAP_BINDING_CONFIRMATIONS,
)
from capabilities.governance.vision_ocr_navigation_task_mainline_resume_v1 import (
    FINAL_DECISION_GO as MAINLINE_FINAL,
    NEXT_PHASE_GO as MAINLINE_NEXT,
)

MIN_CHECKS = 275

REQUIRED = (
    "first_person_vision_navigation_candidate_flow_policy_v1.json",
    "mainline_resume_input_review_v1.json",
    "perception_zone_candidate_flow_definition_v1.json",
    "visual_observation_candidate_contract_v1.json",
    "visual_evidence_candidate_contract_v1.json",
    "scene_context_candidate_contract_v1.json",
    "obstacle_candidate_contract_v1.json",
    "risk_context_candidate_contract_v1.json",
    "ocr_result_candidate_contract_v1.json",
    "text_region_candidate_contract_v1.json",
    "signage_context_candidate_contract_v1.json",
    "map_location_context_candidate_contract_v1.json",
    "route_context_candidate_contract_v1.json",
    "navigation_task_candidate_contract_v1.json",
    "task_route_progress_candidate_contract_v1.json",
    "required_observation_candidate_contract_v1.json",
    "visual_ocr_map_candidate_binding_policy_v1.json",
    "drive_signal_to_observation_priority_policy_v1.json",
    "candidate_to_information_integration_handoff_plan_v1.json",
    "candidate_evidence_traceability_policy_v1.json",
    "candidate_flow_boundary_matrix_v1.json",
    "candidate_flow_dryrun_plan_v1.json",
    "non_claims_register_v1.json",
    "first_person_vision_navigation_candidate_flow_planning_decision_v1.json",
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
            "first_person_vision_navigation_candidate_flow_planning"
        ),
    )
    p.add_argument(
        "--mainline-resume-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "vision_ocr_navigation_task_mainline_resume"
        ),
    )
    args = p.parse_args()
    root = Path(args.output_root)
    mainline_root = Path(args.mainline_resume_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in REQUIRED:
        ok(f"file.{f}", (root / f).is_file())

    mainline_vr = _load(mainline_root / "verifier_report.json")
    mainline_sm = _load(mainline_root / "summary.json")

    ok("upstream.mainline_go", mainline_vr.get("verifier") == "GO")
    ok("upstream.mainline_final", mainline_sm.get("final_decision") == UPSTREAM_MAINLINE_FINAL)
    ok("upstream.mainline_final_expected", mainline_sm.get("final_decision") == MAINLINE_FINAL)
    ok("upstream.mainline_next", mainline_sm.get("recommended_next_phase") == UPSTREAM_MAINLINE_NEXT)
    ok("upstream.mainline_next_expected", mainline_sm.get("recommended_next_phase") == MAINLINE_NEXT)

    summary = _load(root / "summary.json")
    policy = _load(root / "first_person_vision_navigation_candidate_flow_policy_v1.json")
    input_review = _load(root / "mainline_resume_input_review_v1.json")
    perception = _load(root / "perception_zone_candidate_flow_definition_v1.json")
    visual_obs = _load(root / "visual_observation_candidate_contract_v1.json")
    visual_ev = _load(root / "visual_evidence_candidate_contract_v1.json")
    scene = _load(root / "scene_context_candidate_contract_v1.json")
    obstacle = _load(root / "obstacle_candidate_contract_v1.json")
    risk = _load(root / "risk_context_candidate_contract_v1.json")
    ocr = _load(root / "ocr_result_candidate_contract_v1.json")
    text_region = _load(root / "text_region_candidate_contract_v1.json")
    signage = _load(root / "signage_context_candidate_contract_v1.json")
    map_loc = _load(root / "map_location_context_candidate_contract_v1.json")
    route = _load(root / "route_context_candidate_contract_v1.json")
    nav_task = _load(root / "navigation_task_candidate_contract_v1.json")
    progress = _load(root / "task_route_progress_candidate_contract_v1.json")
    req_obs = _load(root / "required_observation_candidate_contract_v1.json")
    binding = _load(root / "visual_ocr_map_candidate_binding_policy_v1.json")
    drive_pri = _load(root / "drive_signal_to_observation_priority_policy_v1.json")
    handoff = _load(root / "candidate_to_information_integration_handoff_plan_v1.json")
    trace = _load(root / "candidate_evidence_traceability_policy_v1.json")
    boundary = _load(root / "candidate_flow_boundary_matrix_v1.json")
    dryrun = _load(root / "candidate_flow_dryrun_plan_v1.json")
    planning_decision = _load(
        root / "first_person_vision_navigation_candidate_flow_planning_decision_v1.json"
    )
    non_claims = _load(root / "non_claims_register_v1.json")

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("scope") == SCOPE)
    ok("summary.pass", summary.get("planning_pass") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("summary.deferred", summary.get("vision_ocr_map_navigation_runtime_deferred") is True)

    for field in BOUNDARY_TRUE:
        ok(f"true.{field}", summary.get(field) is True)
    for field in BOUNDARY_FALSE:
        ok(f"false.{field}", summary.get(field) is False)

    ok("policy.not_runtime", policy.get("planning_not_runtime_not_execute") is True)
    ok("policy.contracts13", policy.get("candidate_contract_count") == 13)

    ok("input.pass", input_review.get("review_pass") is True)
    ok("input.mainline_go", input_review.get("mainline_resume_verifier") == "GO")
    ok("input.cb_go", input_review.get("constitution_bus_verifier") == "GO")
    ok("input.ii_go", input_review.get("information_integration_verifier") == "GO")
    ok("input.ds_go", input_review.get("drive_signal_verifier") == "GO")
    ok("input.provider_go", input_review.get("provider_abstraction_verifier") == "GO")
    ok("input.cr_go", input_review.get("controlled_runtime_verifier") == "GO")
    ok("input.deferred", input_review.get("vision_ocr_map_navigation_runtime_deferred") is True)
    ok("input.no_leakage", input_review.get("no_runtime_leakage_in_upstream") is True)

    ok("perception.zone", perception.get("zone") == "Perception Zone")
    ok("perception.count13", perception.get("output_type_count") == 13)
    for conf in PERCEPTION_ZONE_CONFIRMATIONS:
        ok(f"perception.{conf[:18]}", conf in (perception.get("confirmations") or []))

    for field in VISUAL_OBSERVATION_FIELDS:
        ok(f"visual_obs.{field[:18]}", field in (visual_obs.get("required_fields") or []))
    ok("visual_obs.candidate", visual_obs.get("defaults", {}).get("candidate_only") is True)
    ok("visual_obs.not_fact", visual_obs.get("defaults", {}).get("not_fact") is True)
    ok("visual_obs.runtime_false", visual_obs.get("defaults", {}).get("runtime_source") is False)

    for field in VISUAL_EVIDENCE_FIELDS:
        ok(f"visual_ev.{field[:18]}", field in (visual_ev.get("required_fields") or []))
    ok("visual_ev.validation", visual_ev.get("defaults", {}).get("validation_required") is True)

    for field in SCENE_CONTEXT_FIELDS:
        ok(f"scene.{field[:18]}", field in (scene.get("required_fields") or []))
    ok("scene.not_fact", scene.get("defaults", {}).get("not_fact") is True)

    for field in OBSTACLE_FIELDS:
        ok(f"obstacle.{field[:18]}", field in (obstacle.get("required_fields") or []))

    for field in RISK_CONTEXT_FIELDS:
        ok(f"risk.{field[:18]}", field in (risk.get("required_fields") or []))

    for field in OCR_RESULT_FIELDS:
        ok(f"ocr.{field[:18]}", field in (ocr.get("required_fields") or []))
    ok("ocr.not_fact", ocr.get("defaults", {}).get("not_fact") is True)

    for field in TEXT_REGION_FIELDS:
        ok(f"text.{field[:18]}", field in (text_region.get("required_fields") or []))

    for field in SIGNAGE_CONTEXT_FIELDS:
        ok(f"signage.{field[:18]}", field in (signage.get("required_fields") or []))

    for field in MAP_LOCATION_FIELDS:
        ok(f"map.{field[:18]}", field in (map_loc.get("required_fields") or []))
    ok("map.not_fact", map_loc.get("defaults", {}).get("not_fact") is True)

    for field in ROUTE_CONTEXT_FIELDS:
        ok(f"route.{field[:18]}", field in (route.get("required_fields") or []))

    for field in NAVIGATION_TASK_FIELDS:
        ok(f"nav.{field[:18]}", field in (nav_task.get("required_fields") or []))
    ok("nav.no_commit", nav_task.get("defaults", {}).get("task_state_commit_allowed") is False)

    for field in TASK_ROUTE_PROGRESS_FIELDS:
        ok(f"progress.{field[:18]}", field in (progress.get("required_fields") or []))

    for field in REQUIRED_OBSERVATION_FIELDS:
        ok(f"req_obs.{field[:18]}", field in (req_obs.get("required_fields") or []))

    ok("bind.count6", binding.get("confirmation_count") == 6)
    for conf in VISUAL_OCR_MAP_BINDING_CONFIRMATIONS:
        ok(f"bind.{conf[:18]}", conf in (binding.get("confirmations") or []))

    ok("drive.count6", drive_pri.get("confirmation_count") == 6)
    for conf in DRIVE_OBSERVATION_PRIORITY_CONFIRMATIONS:
        ok(f"drive.{conf[:18]}", conf in (drive_pri.get("confirmations") or []))

    ok("handoff.count5", handoff.get("confirmation_count") == 5)
    for conf in II_HANDOFF_CONFIRMATIONS:
        ok(f"handoff.{conf[:18]}", conf in (handoff.get("confirmations") or []))

    ok("trace.preserve", trace.get("all_candidates_must_preserve") is True)
    for field in TRACEABILITY_FIELDS:
        ok(f"trace.{field[:18]}", field in (trace.get("required_fields") or []))

    ok("boundary.pass", boundary.get("boundary_pass") is True)
    for field in BOUNDARY_FALSE:
        ok(f"boundary.{field}", boundary.get("boundary_fields", {}).get(field) is False)

    ok("dryrun.next", dryrun.get("next_phase") == NEXT_PHASE_GO)

    ok("decision.pass", planning_decision.get("planning_pass") is True)
    ok("decision.final", planning_decision.get("final_decision") == FINAL_DECISION_GO)
    ok("decision.next", planning_decision.get("recommended_next_phase") == NEXT_PHASE_GO)

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
