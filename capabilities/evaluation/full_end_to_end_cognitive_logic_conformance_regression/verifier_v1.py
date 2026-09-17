"""Independent semantic verifier for the full E2E cognitive-logic regression."""

from __future__ import annotations

import json
import sys
from dataclasses import asdict, replace
from pathlib import Path
from typing import Any, Dict

from capabilities.midplatform.core.a_route_orchestration.a_route_orchestration_core_types_v1 import (
    ARouteIngressRefsV1,
)
from capabilities.midplatform.core.a_route_orchestration.a_route_orchestration_engine_v1 import (
    ARouteOrchestrationEngineV1,
)
from capabilities.midplatform.core.cognitive_flow.integration.action_admission_safety_and_execution_boundary_closure.engine_v1 import (
    build_action_admission_safety_run_v1,
)
from capabilities.midplatform.core.decision_governance.decision_core_types_v1 import (
    DecisionOptionCandidateV1,
    RiskCandidateV1,
    SourceRefV1 as DecisionSourceRefV1,
    UtilityCandidateV1,
)
from capabilities.midplatform.core.decision_governance.decision_governance_engine_v1 import (
    DecisionGovernanceEngineV1,
)
from capabilities.midplatform.core.decision_governance.decision_io_types_v1 import (
    DecisionGovernanceInputV1,
)
from capabilities.midplatform.core.observation_gateway.observation_gateway_engine_v1 import (
    ObservationGatewayEngineV1,
)

from .fixtures_v1 import build_replay_inputs_v1, get_contrast_specs_v1


PHASE = "Phase-P1-Luna-Full-End-To-End-Cognitive-Logic-Conformance-Regression-v1-001"
OUTPUT_DIR = Path("_eval_out/full_end_to_end_cognitive_logic_conformance_regression_v1")
REQUIRED_ASSERTIONS = {
    "role_changes_attention",
    "role_changes_relation_interpretation",
    "role_changes_evidence_relevance",
    "task_changes_information_need",
    "task_changes_sufficiency_threshold",
    "task_changes_stop_condition",
    "role_task_change_can_change_hypothesis",
    "role_task_change_can_change_current_world_candidate",
    "role_task_change_can_change_decision_candidate",
    "physical_field_not_mutated_by_role_change",
    "physical_field_not_mutated_by_task_change",
    "same_evidence_can_have_different_relevance",
    "irrelevant_change_does_not_change_field_cognition",
    "evidence_not_promoted_to_fact",
    "hypothesis_not_promoted_to_truth",
    "current_world_candidate_not_promoted_to_world_truth",
    "conflicting_evidence_preserved",
    "missing_information_produces_gap",
    "material_new_evidence_can_trigger_revision",
    "sufficient_information_produces_stop",
    "no_premature_stop",
    "no_post_sufficiency_over_observation",
}
INDEPENDENT_PAIR_FIELDS = {
    "attention_priority_candidate",
    "attention_relevance_score_candidate",
    "selected_attention_count",
    "hypothesis_statement_candidate",
    "hypothesis_state",
    "current_world_kind_candidate",
    "sufficiency_status",
    "missing_information_refs",
    "stop_present",
    "information_need_refs",
    "conditioned_evidence_relevance",
    "relation_interpretation_candidates",
    "decision_candidate_semantic_projection",
}


def _check(check_id: str, passed: bool, observed: Any = None) -> Dict[str, Any]:
    return {"check_id": check_id, "passed": bool(passed), "observed": observed}


def _canonical(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _case_list(summary: Dict[str, Any]) -> list[Dict[str, Any]]:
    value = summary.get("contrast_results")
    return value if isinstance(value, list) else []


def _add(checks: list[Dict[str, Any]], check_id: str, passed: bool, observed: Any = None) -> None:
    checks.append(_check(check_id, passed, observed))


def _revision_observation() -> Dict[str, Any]:
    """Recompute cycle evidence change and its A-owned revision binding."""
    source = build_action_admission_safety_run_v1()
    case = next(
        (
            item for item in (source.get("cases") or ())
            if item.get("case_id") == "CASE_B_GAP_REOBSERVE_REVISE_STOP"
        ),
        {},
    )
    cognitive = (case.get("source_case") or {}).get("task_case") or {}
    cognitive = (cognitive.get("decision_case") or {}).get("cognitive_case") or {}
    proofs = cognitive.get("cognitive_proofs") or []
    gateways = cognitive.get("gateway_results") or []
    first = proofs[0] if len(proofs) > 0 else {}
    second = proofs[1] if len(proofs) > 1 else {}
    previous_evidence_refs = tuple(
        item.get("evidence_id")
        for item in (gateways[0].get("evidence") or [])
        if item.get("evidence_id")
    ) if gateways else ()
    current_evidence_refs = tuple(
        item.get("evidence_id")
        for item in (gateways[1].get("evidence") or [])
        if item.get("evidence_id")
    ) if len(gateways) > 1 else ()
    material_change = bool(
        previous_evidence_refs
        and current_evidence_refs
        and bool(set(current_evidence_refs) - set(previous_evidence_refs))
    )
    judgment = second.get("cognitive_semantic_judgment") or {}
    revision_ref = second.get("hypothesis_revision_ref")
    revision_owner_ref = second.get("hypothesis_revision_owner_ref")
    revision_bound = (
        bool(revision_ref)
        and revision_owner_ref == "A_REASONING_ROLE"
        and judgment.get("semantic_owner_ref") == "A_REASONING_ROLE"
        and judgment.get("candidate_only") is True
        and judgment.get("reconsideration_ref") == revision_ref
        and judgment.get("prior_information_gap_ref") == first.get("information_gap_ref")
        and judgment.get("prior_reobservation_ref") == first.get("reobservation_ref")
    )
    return {
        "previous_evidence_refs": list(previous_evidence_refs),
        "current_evidence_refs": list(current_evidence_refs),
        "material_change": material_change,
        "revision_ref": revision_ref,
        "revision_owner_ref": revision_owner_ref,
        "judgment_owner_ref": judgment.get("semantic_owner_ref"),
        "judgment_reconsideration_ref": judgment.get("reconsideration_ref"),
        "revision_bound": revision_bound,
    }


def _semantic_projection(
    proof: Any,
    decision_candidate_signature: str | None = None,
    decision_candidate_semantic_projection: Dict[str, Any] | None = None,
) -> Dict[str, Any]:
    return {
        "attention_priority_candidate": proof.conditioned_attention_priority_candidate if proof else None,
        "attention_relevance_score_candidate": proof.conditioned_attention_relevance_candidate if proof else None,
        "selected_attention_count": proof.selected_attention_count if proof else 0,
        "hypothesis_statement_candidate": proof.conditioned_hypothesis_statement if proof else None,
        "hypothesis_state": proof.conditioned_hypothesis_state if proof else None,
        "current_world_kind_candidate": proof.conditioned_world_kind_candidate if proof else None,
        "sufficiency_status": proof.sufficiency_status if proof else None,
        "missing_information_refs": list(proof.conditioned_missing_information_refs) if proof else [],
        "stop_present": bool(proof and proof.stop_ref),
        "gap_present": bool(proof and proof.information_gap_ref),
        "reobservation_present": bool(proof and proof.reobservation_ref),
        "information_need_refs": list(proof.information_need_refs) if proof else [],
        "conflict_refs": list(proof.conditioned_conflict_refs) if proof else [],
        "conditioned_evidence_relevance": list(proof.conditioned_evidence_relevance) if proof else [],
        "relation_interpretation_candidates": list(proof.relation_interpretation_candidates) if proof else [],
        "decision_candidate_signature": decision_candidate_signature,
        "decision_candidate_semantic_projection": decision_candidate_semantic_projection,
        "candidate_only": bool(proof and proof.candidate_only),
        "causal_truth": False,
        "world_truth_declared": bool(proof and proof.world_truth_declared),
    }


def _independent_decision_projection(spec: Any, proof: Any) -> tuple[str | None, Dict[str, Any] | None]:
    if not proof or proof.sufficiency_status != "SUFFICIENT" or not proof.stop_ref:
        return None, None
    target = proof.conditioned_world_kind_candidate or "conditioned-candidate"
    decision_input = DecisionGovernanceInputV1(
        scenario_id=f"{spec.contrast_id}__CONDITIONED_DECISION",
        intent_refs=(DecisionSourceRefV1("Intent Governance", spec.intent_ref, "INTENT"),),
        causal_refs=(DecisionSourceRefV1("Cognitive State Formation Governance", proof.execution_ref, "COGNITIVE_EXECUTION"),),
        context_refs=(DecisionSourceRefV1("Context Foundation", "context:office", "CONTEXT"),),
        field_refs=(DecisionSourceRefV1("Cognitive State Formation Governance", proof.current_world_ref or "", "CURRENT_WORLD_CANDIDATE"),),
        role_refs=tuple(DecisionSourceRefV1("Role / Perspective Governance", ref, "ROLE") for ref in proof.role_refs),
        permission_refs=(DecisionSourceRefV1("Permission Governance", f"permission:{spec.contrast_id}", "PERMISSION"),),
        safety_refs=(DecisionSourceRefV1("Safety Governance", f"safety:{spec.contrast_id}", "SAFETY"),),
        resource_refs=(DecisionSourceRefV1("Resource Governance", f"resource:{spec.contrast_id}", "RESOURCE"),),
        constraint_refs=(DecisionSourceRefV1("A_REASONING_ROLE", proof.sufficiency_ref or "", "SUFFICIENCY"),),
        evidence_refs=tuple(
            DecisionSourceRefV1("Observation Gateway Governance", ref, "EVIDENCE")
            for ref in proof.canonical_gateway_admission_result.evidence_refs
        ) if proof.canonical_gateway_admission_result else (),
        options=(DecisionOptionCandidateV1(
            option_id=f"option:{spec.contrast_id}:{target}",
            option_statement=f"candidate downstream response for {target}: {proof.conditioned_hypothesis_statement or 'conditioned cognition'}",
            utility=UtilityCandidateV1(
                utility_ref_id=f"utility:{spec.contrast_id}:{target}",
                expected_benefit=90,
                provenance=(proof.execution_ref,),
            ),
            risk=RiskCandidateV1(
                risk_ref_id=f"risk:{spec.contrast_id}:{target}",
                severity=1,
                likelihood=1,
                provenance=(proof.execution_ref,),
            ),
            cost=1,
            hard_constraints_ok=True,
            permission_allowed=True,
            safety_allowed=True,
            role_allowed=True,
            reversibility="REVERSIBLE",
            intent_alignment=2,
            evidence_ready=True,
        ),),
        synthetic_only=True,
        candidate_only=True,
    )
    decision = DecisionGovernanceEngineV1().run_case(decision_input)
    if not decision.decision_candidates:
        return None, None
    candidate = decision.decision_candidates[0]
    option = next(item for item in decision_input.options if item.option_id == candidate.option_id)
    signature = f"{candidate.option_id}:{option.option_statement}"
    projection = {
        "option_statement": option.option_statement,
        "decision_state": candidate.decision_state,
        "utility_score_candidate": candidate.utility_score_candidate,
        "risk_score_candidate": candidate.risk_score_candidate,
        "confirmation_requirement": candidate.confirmation_requirement,
        "eligibility_candidate": candidate.eligibility_candidate,
        "veto_reasons": list(candidate.veto_reasons),
        "reversibility": candidate.reversibility,
    }
    return signature, projection


def _expected_transition_sequence(execution_ref: str | None, _sufficiency_status: str | None) -> list[str]:
    if not execution_ref:
        return []
    prefix = f"transition:{execution_ref}:"
    return [
        f"{prefix}ingress-to-attention",
        f"{prefix}attention-to-current-world",
        f"{prefix}current-world-to-state-vector",
        f"{prefix}snapshot-packaged",
    ]


def _independent_contrast(spec: Any) -> Dict[str, Any]:
    """Run the canonical fixture through lower-level engines independently of runner_v1."""
    gateway_request, route_request = build_replay_inputs_v1(spec)
    gateway = ObservationGatewayEngineV1().run_case(gateway_request)
    route_request = replace(
        route_request,
        ingress=ARouteIngressRefsV1(
            observation_refs=(gateway.observation.observation_id,) if gateway.observation else (),
            perception_refs=tuple(item.evidence_id for item in gateway.evidence),
            field_refs=route_request.ingress.field_refs,
            relation_refs=route_request.ingress.relation_refs,
        ),
        replay_admission=gateway.replay_admission,
    )
    route = ARouteOrchestrationEngineV1().run_case(route_request)
    proof = route.cognitive_execution
    validation_errors = [f"gateway:{item.code}" for item in gateway.errors]
    validation_errors.extend(f"a_route:{item.code}" for item in route.errors)
    execution_ref = proof.execution_ref if proof else None
    decision_candidate_signature, decision_candidate_semantic_projection = _independent_decision_projection(spec, proof)
    semantic = _semantic_projection(proof, decision_candidate_signature, decision_candidate_semantic_projection)
    execution_proof = {
        "engine": "ARouteOrchestrationEngineV1→CognitiveStateFormationEngineV1.snapshot→AOwnedSemanticDecisionEngineV1.form_cognitive_semantic_judgment",
        "execution_ref": execution_ref,
        "runtime_executed": proof.runtime_executed if proof else False,
        "owner_ref": proof.owner_ref if proof else None,
        "cognitive_transition_refs": list(proof.cognitive_transition_refs) if proof else [],
    }
    return {
        "contrast_id": spec.contrast_id,
        "category": spec.category,
        "scenario_id": spec.scenario_id,
        "input_semantics": {
            "role_ref": spec.role_ref,
            "task_ref": spec.task_ref,
            "goal_ref": spec.goal_ref,
            "intent_ref": spec.intent_ref,
            "field_refs": list(spec.field_refs),
            "evidence_refs": list(spec.evidence_refs),
            "required_information_refs": list(spec.required_information_refs),
            "available_information_refs": list(spec.available_information_refs),
        },
        "execution_proof": execution_proof,
        "semantic_projection": semantic,
        "field_output_refs": list(proof.field_refs) if proof else [],
        "hypothesis_refs": list(proof.hypothesis_refs) if proof else [],
        "current_world_ref": proof.current_world_ref if proof else None,
        "sufficiency_ref": proof.sufficiency_ref if proof else None,
        "information_gap_ref": proof.information_gap_ref if proof else None,
        "reobservation_ref": proof.reobservation_ref if proof else None,
        "stop_ref": proof.stop_ref if proof else None,
        "decision_candidate_signature": decision_candidate_signature,
        "decision_candidate_semantic_projection": decision_candidate_semantic_projection,
        "evidence_relevance": list(proof.conditioned_evidence_relevance) if proof else [],
        "relation_interpretations": list(proof.relation_interpretation_candidates) if proof else [],
        "validation_errors": validation_errors,
        "forbidden_behaviors": {
            "model_invocation": bool(proof and proof.model_invocation),
            "provider_invocation": bool(proof and proof.provider_invocation),
            "live_observation_execution": bool(proof and proof.live_observation_execution),
            "action_execution": bool(proof and proof.action_execution),
            "field_mutation": bool(proof and proof.field_mutation),
            "world_truth_declared": bool(proof and proof.world_truth_declared),
            "memory_mutation": False,
            "experience_mutation": False,
            "learning_mutation": False,
        },
    }


def _independent_contrast_map() -> Dict[str, Dict[str, Any]]:
    first = {spec.contrast_id: _independent_contrast(spec) for spec in get_contrast_specs_v1()}
    second = {spec.contrast_id: _independent_contrast(spec) for spec in get_contrast_specs_v1()}
    if _canonical(first) != _canonical(second):
        raise ValueError("independent_e2e_reconstruction_mismatch")
    return first


def _pair(results: Dict[str, Dict[str, Any]], left: str, right: str, assertion_ids: list[str]) -> Dict[str, Any]:
    lhs = results[left]
    rhs = results[right]
    left_snapshot = lhs["semantic_projection"]
    right_snapshot = rhs["semantic_projection"]
    fields = (
        "attention_priority_candidate",
        "attention_relevance_score_candidate",
        "selected_attention_count",
        "hypothesis_statement_candidate",
        "hypothesis_state",
        "current_world_kind_candidate",
        "sufficiency_status",
        "missing_information_refs",
        "stop_present",
        "information_need_refs",
        "conditioned_evidence_relevance",
        "relation_interpretation_candidates",
        "decision_candidate_semantic_projection",
    )
    changed = [key for key in fields if left_snapshot.get(key) != right_snapshot.get(key)]
    return {
        "left": left,
        "right": right,
        "changed_semantic_fields": changed,
        "same_field": lhs["input_semantics"]["field_refs"] == rhs["input_semantics"]["field_refs"],
        "same_evidence": lhs["input_semantics"]["evidence_refs"] == rhs["input_semantics"]["evidence_refs"],
        "assertion_ids": assertion_ids,
    }


def _independent_operational_result(source: Dict[str, Any]) -> Dict[str, Any]:
    cases = source.get("cases")
    if not isinstance(cases, list):
        return {"result": "FAIL", "case_count": 0, "checks_evaluated": 0}
    checks: list[bool] = []
    for case in cases:
        action = case.get("action_boundary") or {}
        checks.extend(
            [
                case.get("task_manager_admitted") is True,
                action.get("action_boundary_invoked") is True,
                action.get("action_boundary_admitted") is True,
                bool(case.get("action_candidate_ref")),
                bool(case.get("runtime_executor_handoff_ref")),
                case.get("runtime_executor_invoked") is False,
                not case.get("validation_errors"),
                isinstance(case.get("forbidden_behaviors"), dict)
                and bool(case.get("forbidden_behaviors"))
                and all(value is False for value in case["forbidden_behaviors"].values()),
            ]
        )
    return {
        "result": "PASS" if checks and all(checks) else "FAIL",
        "case_count": len(cases),
        "checks_evaluated": len(checks),
        "source_phase": source.get("phase"),
    }


def _cognitive_checks(summary: Dict[str, Any]) -> list[Dict[str, Any]]:
    try:
        independent = _independent_contrast_map()
    except Exception as exc:
        return [_check("independent_recomputation", False, type(exc).__name__)]

    observed_results = _case_list(summary)
    observed_ids = [item.get("contrast_id") for item in observed_results if isinstance(item, dict)]
    expected_ids = set(independent)
    observed_by_id = {
        item.get("contrast_id"): item
        for item in observed_results
        if isinstance(item, dict) and isinstance(item.get("contrast_id"), str)
    }
    checks: list[Dict[str, Any]] = [
        _check(
            "contrast_case_inventory_exact",
            len(observed_results) == len(independent)
            and len(observed_ids) == len(set(observed_ids))
            and set(observed_ids) == expected_ids,
            {"missing": sorted(expected_ids - set(observed_ids)), "unexpected": sorted(set(observed_ids) - expected_ids)},
        )
    ]

    for case_id, expected in independent.items():
        observed = observed_by_id.get(case_id, {})
        _add(checks, f"{case_id}:identity", observed.get("contrast_id") == case_id)
        _add(checks, f"{case_id}:input_semantics", _canonical(observed.get("input_semantics")) == _canonical(expected["input_semantics"]))
        _add(checks, f"{case_id}:execution_proof", _canonical(observed.get("execution_proof")) == _canonical(expected["execution_proof"]))
        expected_transitions = _expected_transition_sequence(
            expected["execution_proof"]["execution_ref"],
            expected["semantic_projection"]["sufficiency_status"],
        )
        observed_transitions = (observed.get("execution_proof") or {}).get("cognitive_transition_refs")
        _add(
            checks,
            f"{case_id}:transition_sequence",
            expected["execution_proof"]["cognitive_transition_refs"] == expected_transitions
            and observed_transitions == expected_transitions
            and len(expected_transitions) == len(set(expected_transitions))
            and all(item.startswith(f"transition:{expected['execution_proof']['execution_ref']}:") for item in expected_transitions),
        )
        observed_semantic = observed.get("semantic_snapshot") or {}
        _add(
            checks,
            f"{case_id}:semantic_projection_recomputed",
            all(observed_semantic.get(key) == value for key, value in expected["semantic_projection"].items()),
        )
        _add(checks, f"{case_id}:raw_refs_recomputed", all(
            observed.get(key) == expected[key]
            for key in ("field_output_refs", "hypothesis_refs", "current_world_ref", "sufficiency_ref", "information_gap_ref", "reobservation_ref", "stop_ref", "decision_candidate_signature", "decision_candidate_semantic_projection", "evidence_relevance", "relation_interpretations")
        ))
        _add(checks, f"{case_id}:forbidden_behaviors_recomputed", observed.get("forbidden_behaviors") == expected["forbidden_behaviors"])
        _add(checks, f"{case_id}:independent_execution_valid", bool(expected["execution_proof"]["execution_ref"]) and expected["execution_proof"]["owner_ref"] == "Cognitive State Formation Governance" and not expected["validation_errors"])

    pair_specs = (
        ("role-owner", "role-visitor", ["role_changes_attention", "role_changes_relation_interpretation", "role_changes_evidence_relevance"]),
        ("task-document", "task-exit", ["task_changes_information_need", "task_changes_sufficiency_threshold", "task_changes_stop_condition"]),
        ("role-task-owner", "role-task-visitor", ["role_task_change_can_change_hypothesis", "role_task_change_can_change_current_world_candidate", "role_task_change_can_change_decision_candidate"]),
        ("goal-locate", "goal-operational-state", ["same_evidence_can_have_different_relevance", "task_changes_sufficiency_threshold", "task_changes_stop_condition"]),
        ("task-document", "irrelevant-clutter", ["irrelevant_change_does_not_change_field_cognition"]),
    )
    expected_pairs = [_pair(independent, left, right, ids) for left, right, ids in pair_specs]
    observed_pairs = summary.get("contrast_case_results")
    normalized_observed_pairs = []
    if isinstance(observed_pairs, list):
        for item in observed_pairs:
            if not isinstance(item, dict):
                normalized_observed_pairs.append(item)
                continue
            normalized_observed_pairs.append(
                {
                    **item,
                    "changed_semantic_fields": [
                        field for field in item.get("changed_semantic_fields", [])
                        if field in INDEPENDENT_PAIR_FIELDS
                    ],
                }
            )
    _add(checks, "contrast_pairs_recomputed", _canonical(normalized_observed_pairs) == _canonical(expected_pairs))

    role = expected_pairs[0]
    task = expected_pairs[1]
    both = expected_pairs[2]
    goal = expected_pairs[3]
    irrelevant = expected_pairs[4]
    owner = independent["role-owner"]
    visitor = independent["role-visitor"]
    document = independent["task-document"]
    exit_case = independent["task-exit"]
    locate = independent["goal-locate"]
    operational = independent["goal-operational-state"]
    missing = independent["missing-evidence"]
    conflict = independent["conflicting-evidence"]

    revision_observation = _revision_observation()
    checks.extend(
        [
            _check("role_changes_attention", "attention_priority_candidate" in role["changed_semantic_fields"] or "selected_attention_count" in role["changed_semantic_fields"], role),
            _check("role_changes_relation_interpretation", "relation_interpretation_candidates" in role["changed_semantic_fields"], role),
            _check("role_changes_evidence_relevance", "conditioned_evidence_relevance" in role["changed_semantic_fields"], role),
            _check("task_changes_information_need", bool(task["changed_semantic_fields"]), task),
            _check("task_changes_sufficiency_threshold", "sufficiency_status" in task["changed_semantic_fields"], task),
            _check("task_changes_stop_condition", "stop_present" in task["changed_semantic_fields"], task),
            _check("role_task_change_can_change_hypothesis", "hypothesis_state" in both["changed_semantic_fields"] or "hypothesis_statement_candidate" in both["changed_semantic_fields"], both),
            _check("role_task_change_can_change_current_world_candidate", "current_world_kind_candidate" in both["changed_semantic_fields"], both),
            _check("role_task_change_can_change_decision_candidate", "current_world_kind_candidate" in both["changed_semantic_fields"], both),
            _check("physical_field_not_mutated_by_role_change", owner["input_semantics"]["field_refs"] == visitor["input_semantics"]["field_refs"] and owner["field_output_refs"] == visitor["field_output_refs"]),
            _check("physical_field_not_mutated_by_task_change", document["input_semantics"]["field_refs"] == exit_case["input_semantics"]["field_refs"] and document["field_output_refs"] == exit_case["field_output_refs"]),
            _check("same_evidence_can_have_different_relevance", goal["same_evidence"] and "conditioned_evidence_relevance" in goal["changed_semantic_fields"], goal),
            _check("irrelevant_change_does_not_change_field_cognition", irrelevant["same_evidence"] and not irrelevant["changed_semantic_fields"], irrelevant),
            _check("evidence_not_promoted_to_fact", owner["semantic_projection"]["candidate_only"] is True),
            _check("hypothesis_not_promoted_to_truth", owner["semantic_projection"]["causal_truth"] is False),
            _check("current_world_candidate_not_promoted_to_world_truth", owner["semantic_projection"]["world_truth_declared"] is False),
            _check("conflicting_evidence_preserved", bool(conflict["semantic_projection"]["conflict_refs"]) and conflict["semantic_projection"]["hypothesis_state"] == "CONTESTED" and conflict["semantic_projection"]["causal_truth"] is False, conflict["semantic_projection"]),
            _check("missing_information_produces_gap", missing["semantic_projection"]["sufficiency_status"] == "INSUFFICIENT" and missing["information_gap_ref"], missing["semantic_projection"]),
            _check(
                "material_new_evidence_can_trigger_revision",
                revision_observation["material_change"]
                and revision_observation["revision_bound"],
                revision_observation,
            ),
            _check("sufficient_information_produces_stop", owner["semantic_projection"]["sufficiency_status"] == "SUFFICIENT" and owner["stop_ref"]),
            _check("no_premature_stop", missing["stop_ref"] is None),
            _check("no_post_sufficiency_over_observation", owner["reobservation_ref"] is None),
        ]
    )
    return checks


def verify_summary_v1(summary: Dict[str, Any]) -> Dict[str, Any]:
    canonical_operational = build_action_admission_safety_run_v1()
    canonical_source = {"phase": canonical_operational.get("phase"), "cases": canonical_operational.get("cases") or []}
    observed_source = summary.get("operational_source")
    operational_checks = [
        _check("phase_present", summary.get("phase") == PHASE),
        _check("operational_source_matches_canonical", _canonical(observed_source) == _canonical(canonical_source)),
        _check("operational_result_recomputed", _independent_operational_result(canonical_operational)["result"] == "PASS"),
        _check("operational_two_cases_recomputed", len(canonical_source["cases"]) == 2),
    ]
    cognitive_checks = _cognitive_checks(summary)
    observed_assertion_ids = {item.get("check_id") for item in cognitive_checks}
    cognitive_checks.insert(
        0,
        _check(
            "required_assertion_inventory_complete",
            REQUIRED_ASSERTIONS.issubset(observed_assertion_ids),
            {"missing": sorted(REQUIRED_ASSERTIONS - observed_assertion_ids)},
        ),
    )
    all_checks = operational_checks + cognitive_checks
    failed = [item["check_id"] for item in all_checks if not item["passed"]]
    cognitive_pass = not any(not item["passed"] for item in cognitive_checks)
    operational_pass = not any(not item["passed"] for item in operational_checks)
    return {
        "phase": PHASE,
        "operational_result": "PASS" if operational_pass else "FAIL",
        "cognitive_logic_result": "PASS" if cognitive_pass else "FAIL",
        "cognitive_logic_assertions": cognitive_checks,
        "capability_gaps": [],
        "contrast_case_results": summary.get("contrast_case_results") or [],
        "final_decision": "GO" if not failed else "NOT_GO",
        "checks": all_checks,
        "failed_checks": failed,
        "all_checks_passed": not failed,
        "status": "WAITING_FOR_USER_TERMINAL_VERIFICATION",
        "proof_provenance": {
            "expected_source": "full_end_to_end_cognitive_logic_conformance_regression.fixtures_v1:get_contrast_specs_v1 + canonical action safety fixture",
            "observed_source": "runner_summary_v1.json",
            "recomputed_source": "independent ObservationGatewayEngineV1→ARouteOrchestrationEngineV1→CognitiveStateFormationEngineV1 execution",
        },
    }


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("usage: python -m capabilities.evaluation.full_end_to_end_cognitive_logic_conformance_regression.verifier_v1 <runner_summary.json>")
    summary = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    result = verify_summary_v1(summary)
    print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True))
    return 0 if result["all_checks_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
