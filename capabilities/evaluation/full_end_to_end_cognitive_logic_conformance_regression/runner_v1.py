"""User-terminal runner for the full E2E cognitive-logic regression.

This runner writes only a transient summary under ``_eval_out``.  It reuses
the verified Action-boundary composition for operational coverage and invokes
the canonical Cognitive State Formation engine for observed contrast inputs.
"""

from __future__ import annotations

import json
from dataclasses import asdict, is_dataclass, replace
from pathlib import Path
from typing import Any, Dict

from capabilities.midplatform.core.a_route_orchestration.a_route_orchestration_engine_v1 import (
    ARouteOrchestrationEngineV1,
)
from capabilities.midplatform.core.a_route_orchestration.a_route_orchestration_core_types_v1 import (
    ARouteIngressRefsV1,
)
from capabilities.midplatform.core.observation_gateway.observation_gateway_engine_v1 import (
    ObservationGatewayEngineV1,
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
from capabilities.midplatform.core.cognitive_flow.integration.action_admission_safety_and_execution_boundary_closure.engine_v1 import (
    build_action_admission_safety_run_v1,
)

from .fixtures_v1 import ContrastSpecV1, build_replay_inputs_v1, get_contrast_specs_v1
from .verifier_v1 import _cognitive_checks


PHASE = "Phase-P1-Luna-Full-End-To-End-Cognitive-Logic-Conformance-Regression-v1-001"
OUTPUT_DIR = Path("_eval_out/full_end_to_end_cognitive_logic_conformance_regression_v1")


def _jsonable(value: Any) -> Any:
    if is_dataclass(value):
        return {key: _jsonable(item) for key, item in asdict(value).items()}
    if isinstance(value, dict):
        return {str(key): _jsonable(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [_jsonable(item) for item in value]
    return value


def _semantic_snapshot(
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
        # The raw signature remains available for traceability, but is not a
        # semantic contrast field because it contains execution/identity data.
        "decision_candidate_signature": decision_candidate_signature,
        "decision_candidate_semantic_projection": decision_candidate_semantic_projection,
        "candidate_only": bool(proof and proof.candidate_only),
        "causal_truth": False,
        "world_truth_declared": bool(proof and proof.world_truth_declared),
    }


def _run_contrast(spec: ContrastSpecV1) -> Dict[str, Any]:
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
    decision_candidate_signature = None
    decision_candidate_semantic_projection = None
    if proof and proof.sufficiency_status == "SUFFICIENT" and proof.stop_ref:
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
            constraint_refs=(DecisionSourceRefV1("Cognitive State Formation Governance", proof.sufficiency_ref or "", "SUFFICIENCY"),),
            evidence_refs=tuple(DecisionSourceRefV1("Observation Gateway Governance", ref, "EVIDENCE") for ref in proof.ingress_refs),
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
        if decision.decision_candidates:
            candidate = decision.decision_candidates[0]
            decision_candidate_signature = f"{candidate.option_id}:{decision_input.options[0].option_statement}"
            option = next(
                item for item in decision_input.options if item.option_id == candidate.option_id
            )
            decision_candidate_semantic_projection = {
                "option_statement": option.option_statement,
                "decision_state": candidate.decision_state,
                "utility_score_candidate": candidate.utility_score_candidate,
                "risk_score_candidate": candidate.risk_score_candidate,
                "confirmation_requirement": candidate.confirmation_requirement,
                "eligibility_candidate": candidate.eligibility_candidate,
                "veto_reasons": list(candidate.veto_reasons),
                "reversibility": candidate.reversibility,
            }
    return {
        "contrast_id": spec.contrast_id,
        "category": spec.category,
        "scenario_id": spec.scenario_id,
        "input": {
            "gateway_request": _jsonable(gateway_request),
            "a_route_request": _jsonable(route_request),
        },
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
        "execution_proof": {
            "engine": "ARouteOrchestrationEngineV1→CognitiveStateFormationEngineV1.run_case",
            "execution_ref": proof.execution_ref if proof else None,
            "runtime_executed": proof.runtime_executed if proof else False,
            "owner_ref": proof.owner_ref if proof else None,
            "cognitive_transition_refs": list(proof.cognitive_transition_refs) if proof else [],
        },
        "semantic_snapshot": _semantic_snapshot(
            proof,
            decision_candidate_signature,
            decision_candidate_semantic_projection,
        ),
        "gateway_admission_ref": gateway.replay_admission.gateway_admission_ref if gateway.replay_admission else None,
        "observation_gateway_admitted": gateway.admission_state == "ADMITTED_OBSERVATION",
        "a_route_execution_ref": proof.execution_ref if proof else None,
        "field_output_refs": list(proof.field_refs) if proof else [],
        "hypothesis_refs": list(proof.hypothesis_refs) if proof else [],
        "current_world_ref": proof.current_world_ref if proof else None,
        "sufficiency_ref": proof.sufficiency_ref if proof else None,
        "information_gap_ref": proof.information_gap_ref if proof else None,
        "reobservation_ref": proof.reobservation_ref if proof else None,
        "stop_ref": proof.stop_ref if proof else None,
        "evidence_relevance": list(proof.conditioned_evidence_relevance) if proof else [],
        "relation_interpretations": list(proof.relation_interpretation_candidates) if proof else [],
        "decision_candidate_signature": decision_candidate_signature,
        "decision_candidate_semantic_projection": decision_candidate_semantic_projection,
        "validation_errors": validation_errors,
        "forbidden_behaviors": {
            "model_invocation": False,
            "provider_invocation": False,
            "live_observation_execution": False,
            "action_execution": False,
            "field_mutation": bool(proof and proof.field_mutation),
            "world_truth_declared": False,
            "memory_mutation": False,
            "experience_mutation": False,
            "learning_mutation": False,
        },
    }


def _pair(results: list[Dict[str, Any]], left: str, right: str, assertion_ids: list[str]) -> Dict[str, Any]:
    by_id = {item["contrast_id"]: item for item in results}
    lhs = by_id[left]
    rhs = by_id[right]
    left_snapshot = lhs["semantic_snapshot"]
    right_snapshot = rhs["semantic_snapshot"]
    changed = {
        key: left_snapshot.get(key) != right_snapshot.get(key)
        for key in (
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
    }
    return {
        "left": left,
        "right": right,
        "changed_semantic_fields": [key for key, value in changed.items() if value],
        "same_field": lhs["input_semantics"]["field_refs"] == rhs["input_semantics"]["field_refs"],
        "same_evidence": lhs["input_semantics"]["evidence_refs"] == rhs["input_semantics"]["evidence_refs"],
        "assertion_ids": assertion_ids,
    }


def _operational_result(source: Dict[str, Any]) -> Dict[str, Any]:
    checks = []
    for case in source.get("cases") or []:
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
                all(value is False for value in (case.get("forbidden_behaviors") or {}).values()),
            ]
        )
    return {
        "result": "PASS" if checks and all(checks) else "FAIL",
        "case_count": len(source.get("cases") or []),
        "checks_evaluated": len(checks),
        "source_phase": source.get("phase"),
    }


def build_runner_summary_v1() -> Dict[str, Any]:
    source = build_action_admission_safety_run_v1()
    contrast_results = [_run_contrast(spec) for spec in get_contrast_specs_v1()]
    capability_gaps = []
    operational = _operational_result(source)
    pairs = [
        _pair(contrast_results, "role-owner", "role-visitor", ["role_changes_attention", "role_changes_relation_interpretation", "role_changes_evidence_relevance"]),
        _pair(contrast_results, "task-document", "task-exit", ["task_changes_information_need", "task_changes_sufficiency_threshold", "task_changes_stop_condition"]),
        _pair(contrast_results, "role-task-owner", "role-task-visitor", ["role_task_change_can_change_hypothesis", "role_task_change_can_change_current_world_candidate", "role_task_change_can_change_decision_candidate"]),
        _pair(contrast_results, "goal-locate", "goal-operational-state", ["same_evidence_can_have_different_relevance", "task_changes_sufficiency_threshold", "task_changes_stop_condition"]),
        _pair(contrast_results, "task-document", "irrelevant-clutter", ["irrelevant_change_does_not_change_field_cognition"]),
    ]
    cognitive_probe = {
        "contrast_results": contrast_results,
        "contrast_case_results": pairs,
        "operational_source": {"cases": source.get("cases") or []},
    }
    cognitive_result = "PASS" if all(item["passed"] for item in _cognitive_checks(cognitive_probe)) else "FAIL"
    return {
        "phase": PHASE,
        "shared_contract": "docs/architecture/luna_cognitive_logic_conformance_test_contract_v1.md",
        "operational": operational,
        "operational_result": operational["result"],
        "cognitive_logic_result": cognitive_result,
        "final_decision": "GO" if operational["result"] == "PASS" and cognitive_result == "PASS" else "NOT_GO",
        "operational_source": {
            "phase": source.get("phase"),
            "cases": source.get("cases") or [],
        },
        "contrast_results": contrast_results,
        "contrast_case_results": pairs,
        "capability_gaps": capability_gaps,
        "assertion_policy": {
            "operational_result": "PASS only when operational checks pass",
            "cognitive_logic_result": "PASS only when every required assertion is evidenced by observed output",
            "final_decision": "GO only when operational_result=PASS and cognitive_logic_result=PASS",
        },
        "forbidden_behaviors": {
            "model_invocation": False,
            "provider_invocation": False,
            "live_observation_execution": False,
            "action_execution": False,
            "runtime_executor_invocation": False,
            "field_mutation": False,
            "world_truth_declared": False,
            "memory_mutation": False,
            "experience_mutation": False,
            "learning_mutation": False,
        },
        "status": "WAITING_FOR_USER_TERMINAL_VERIFICATION",
    }


def main() -> int:
    summary = build_runner_summary_v1()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUTPUT_DIR / "runner_summary_v1.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(summary, indent=2, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
