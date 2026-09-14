# -*- coding: utf-8 -*-
"""Field simulation core v1."""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple

from capabilities.midplatform.field_simulation_candidate_generator_v1 import (
    generate_field_simulation_candidates,
)
from capabilities.midplatform.field_simulation_input_view_builder_v1 import (
    build_field_simulation_input_view,
)
from capabilities.midplatform.field_simulation_plan_builder_v1 import (
    build_field_simulation_plan_candidate,
)
from capabilities.midplatform.field_simulation_readiness_assembler_v1 import (
    assemble_field_simulation_readiness_candidate,
    assemble_field_simulation_skeleton_result,
)
from capabilities.midplatform.field_simulation_static_validators_v1 import (
    validate_field_simulation_candidate,
    validate_field_simulation_input_view,
    validate_field_simulation_plan_candidate,
    validate_field_simulation_readiness_candidate,
    validate_no_action_no_fact_boundary,
    validate_simulation_eligibility_candidate,
)
from capabilities.midplatform.simulation_eligibility_evaluator_v1 import (
    evaluate_simulation_eligibility,
)


def _evaluate_skeleton_case(
    case: Dict[str, Any],
    candidates: List[Dict[str, Any]],
    eligibility: Dict[str, Any],
    readiness: Dict[str, Any],
    skeleton_result: Dict[str, Any],
) -> bool:
    if case.get("optional_meta") and case.get("case_id") == "no_action_no_fact_boundary":
        ok, _ = validate_no_action_no_fact_boundary(candidates)
        return ok

    if case.get("optional_meta"):
        return True

    statuses = tuple(case.get("expect_status") or ("generated",))

    if case.get("expect_all_blocked"):
        if any(c.get("simulation_status") in ("generated", "generated_degraded") for c in candidates):
            return False
        return any(c.get("simulation_status") in statuses for c in candidates)

    mode = case.get("expect_mode")
    if mode:
        mode_cands = [c for c in candidates if c.get("mode") == mode]
        if not mode_cands:
            return False
        if not any(c.get("simulation_status") in statuses for c in mode_cands):
            return False
        if case.get("expect_no_action"):
            if not all(c.get("no_action_output") is True for c in mode_cands):
                return False

    if case.get("expect_short_horizon_blocked"):
        sh = [c for c in candidates if c.get("mode") == "short_horizon_motion_projection"]
        if sh and sh[0].get("simulation_status") not in ("blocked_insufficient_input",):
            return False

    if case.get("expect_traceability_min"):
        if len(skeleton_result.get("traceability_refs") or []) < case["expect_traceability_min"]:
            return False

    if case.get("expect_no_action_no_fact"):
        ok, _ = validate_no_action_no_fact_boundary(candidates)
        return ok

    return True


def run_simulation_skeleton_case(
    case: Dict[str, Any],
    *,
    dryrun_result: Dict[str, Any],
    hardened_result: Optional[Dict[str, Any]],
    reusable_case: Optional[Dict[str, Any]],
) -> Dict[str, Any]:
    input_view = build_field_simulation_input_view(
        dryrun_result=dryrun_result,
        hardened_result=hardened_result,
        reusable_case=reusable_case,
    )
    eligibility = evaluate_simulation_eligibility(input_view, dryrun_result, reusable_case)
    plan = build_field_simulation_plan_candidate(
        input_view=input_view, eligibility=eligibility, reusable_case=reusable_case,
    )
    candidates = generate_field_simulation_candidates(
        input_view=input_view, plan=plan, eligibility=eligibility,
    )
    readiness = assemble_field_simulation_readiness_candidate(
        plan=plan, eligibility=eligibility, simulation_candidates=candidates,
    )
    skeleton_result = assemble_field_simulation_skeleton_result(
        input_view=input_view,
        eligibility=eligibility,
        plan=plan,
        simulation_candidates=candidates,
        readiness=readiness,
        case_id=case["case_id"],
    )

    for c in candidates:
        validate_field_simulation_candidate(c)
    validate_field_simulation_input_view(input_view)
    validate_simulation_eligibility_candidate(eligibility)
    validate_field_simulation_plan_candidate(plan)
    validate_field_simulation_readiness_candidate(readiness)

    passed = _evaluate_skeleton_case(case, candidates, eligibility, readiness, skeleton_result)
    return {
        "case_id": case["case_id"],
        "source_case_id": case["source_case_id"],
        "case_passed": passed,
        "input_view": input_view,
        "eligibility": eligibility,
        "plan": plan,
        "simulation_candidates": candidates,
        "readiness": readiness,
        "skeleton_result": skeleton_result,
    }


def run_all_simulation_skeleton_cases(
    *,
    cases: Tuple[Dict[str, Any], ...],
    indexed_upstream: Dict[str, Dict[str, Any]],
) -> Tuple[List[Dict[str, Any]], bool]:
    results: List[Dict[str, Any]] = []
    all_passed = True
    for case in cases:
        upstream = indexed_upstream.get(case["source_case_id"])
        if not upstream:
            results.append({"case_id": case["case_id"], "case_passed": False, "error": "upstream_not_found"})
            all_passed = False
            continue
        row = run_simulation_skeleton_case(
            case,
            dryrun_result=upstream["dryrun"],
            hardened_result=upstream.get("hardened"),
            reusable_case=upstream.get("reusable"),
        )
        results.append(row)
        if not row.get("case_passed") and not case.get("optional_meta"):
            all_passed = False
    return results, all_passed
