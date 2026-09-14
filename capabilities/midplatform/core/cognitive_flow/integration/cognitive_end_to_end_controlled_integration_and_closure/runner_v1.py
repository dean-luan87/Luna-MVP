"""Runner for the two-case controlled end-to-end cognition baseline.

This module composes the previously verified Brain closure integration.  It
does not implement another cognition engine or create a Brain owner.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Iterable

from capabilities.midplatform.core.cognitive_flow.integration.brain_cognitive_loop_closure_assimilation_controlled.brain_cognitive_loop_closure_assimilation_engine_v1 import (
    build_brain_closure_run_v1,
)


PHASE = "Phase-P1-Luna-Cognitive-End-To-End-Controlled-Integration-And-Closure-v1-001"
OUTPUT_DIR = Path("_eval_out/cognitive_end_to_end_controlled_integration_and_closure_v1")
EXECUTION_INSTANCE_REF = "controlled-e2e-session"
EXPECTED_CASES = (
    "CASE_A_SUFFICIENT_STOP",
    "CASE_B_GAP_REOBSERVE_REVISE_STOP",
)


def _unique(values: Iterable[Any]) -> list[Any]:
    result: list[Any] = []
    for value in values:
        if value and value not in result:
            result.append(value)
    return result


def _proof_summary(proof: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "execution_ref": proof.get("execution_ref"),
        "execution_mode": proof.get("execution_mode"),
        "owner_ref": proof.get("owner_ref"),
        "runtime_executed": proof.get("runtime_executed"),
        "cognitive_transition_refs": proof.get("cognitive_transition_refs", []),
        "current_world_ref": proof.get("current_world_ref"),
        "hypothesis_refs": proof.get("hypothesis_refs", []),
        "current_world_availability": proof.get("current_world_availability"),
        "hypothesis_availability": proof.get("hypothesis_availability"),
        "sufficiency_ref": proof.get("sufficiency_ref"),
        "sufficiency_status": proof.get("sufficiency_status"),
        "sufficiency_owner_ref": proof.get("sufficiency_owner_ref"),
        "information_gap_ref": proof.get("information_gap_ref"),
        "information_gap_owner_ref": proof.get("information_gap_owner_ref"),
        "reobservation_ref": proof.get("reobservation_ref"),
        "reobservation_owner_ref": proof.get("reobservation_owner_ref"),
        "reobservation_information_gap_ref": proof.get("reobservation_information_gap_ref"),
        "next_cycle_ingress_ref": proof.get("next_cycle_ingress_ref"),
        "prior_next_cycle_ingress_ref": proof.get("prior_next_cycle_ingress_ref"),
        "hypothesis_revision_ref": proof.get("hypothesis_revision_ref"),
        "hypothesis_revision_owner_ref": proof.get("hypothesis_revision_owner_ref"),
        "hypothesis_revision_information_gap_ref": proof.get("hypothesis_revision_information_gap_ref"),
        "hypothesis_revision_reobservation_ref": proof.get("hypothesis_revision_reobservation_ref"),
        "stop_ref": proof.get("stop_ref"),
        "stop_reason": proof.get("stop_reason"),
        "stop_owner_ref": proof.get("stop_owner_ref"),
        "candidate_only": proof.get("candidate_only"),
        "field_mutation": proof.get("field_mutation"),
        "world_truth_declared": proof.get("world_truth_declared"),
        "model_invocation": proof.get("model_invocation"),
        "provider_invocation": proof.get("provider_invocation"),
        "live_observation_execution": proof.get("live_observation_execution"),
        "action_execution": proof.get("action_execution"),
    }


def _gateway_summary(gateway: Dict[str, Any]) -> Dict[str, Any]:
    admission = gateway.get("replay_admission") or {}
    return {
        "scenario_id": gateway.get("scenario_id"),
        "execution_mode": gateway.get("execution_mode"),
        "replay_input_ref": gateway.get("replay_input_ref"),
        "admission_state": gateway.get("admission_state"),
        "gateway_admission_ref": admission.get("gateway_admission_ref"),
        "admission_owner_ref": admission.get("owner_ref"),
        "evidence_refs": [item.get("evidence_id") for item in gateway.get("evidence", [])],
        "errors": gateway.get("errors", []),
    }


def _case_summary(case: Dict[str, Any]) -> Dict[str, Any]:
    request = case.get("brain_request") or {}
    need = case.get("information_need") or {}
    loop = case.get("loop_instance") or {}
    gateways = [_gateway_summary(item) for item in case.get("gateway_results", [])]
    proofs = [_proof_summary(item) for item in case.get("cognitive_proofs", [])]
    closure = case.get("closure_assessment") or {}
    acceptance = case.get("closure_acceptance") or {}
    assimilation = case.get("assimilation_candidate") or {}
    traceability = {
        "goal_ref": request.get("goal_ref"),
        "intent_ref": request.get("intent_ref"),
        "concern_ref": request.get("concern_ref"),
        "context_ref": request.get("context_ref"),
        "information_need_ref": need.get("information_need_ref"),
        "cognitive_loop_ref": loop.get("cognitive_loop_ref"),
        "gateway_admission_refs": _unique(item.get("gateway_admission_ref") for item in gateways),
        "a_route_execution_refs": _unique(item.get("execution_ref") for item in proofs),
        "evidence_refs": _unique(ref for item in gateways for ref in item.get("evidence_refs", [])),
        "hypothesis_refs": _unique(ref for item in proofs for ref in item.get("hypothesis_refs", [])),
        "current_world_refs": _unique(item.get("current_world_ref") for item in proofs),
        "sufficiency_refs": _unique(item.get("sufficiency_ref") for item in proofs),
        "information_gap_ref": next((item.get("information_gap_ref") for item in proofs if item.get("information_gap_ref")), None),
        "reobservation_ref": next((item.get("reobservation_ref") for item in proofs if item.get("reobservation_ref")), None),
        "hypothesis_revision_ref": next((item.get("hypothesis_revision_ref") for item in proofs if item.get("hypothesis_revision_ref")), None),
        "stop_ref": next((item.get("stop_ref") for item in reversed(proofs) if item.get("stop_ref")), None),
        "closure_candidate_ref": closure.get("assessment_ref"),
        "assimilation_candidate_ref": assimilation.get("assimilation_ref"),
    }
    return {
        "case_id": case.get("case_id"),
        "title": case.get("title"),
        "brain_request_ref": request.get("brain_request_ref"),
        "cognitive_loop_ref": loop.get("cognitive_loop_ref"),
        "lifecycle_owner_ref": loop.get("lifecycle_owner_ref"),
        "information_need_ref": need.get("information_need_ref"),
        "information_need_responsibility_domain": need.get("responsibility_domain"),
        "information_need_canonical_owner_status": need.get("canonical_owner_status"),
        "execution_mode": proofs[0].get("execution_mode") if proofs else None,
        "cognition_execution": bool(proofs) and all(item.get("runtime_executed") is True for item in proofs),
        "runtime_executed": bool(proofs) and all(item.get("runtime_executed") is True for item in proofs),
        "cognitive_cycle_count": loop.get("cycle_count", 0),
        "cognitive_transition_count": sum(len(item.get("cognitive_transition_refs", [])) for item in proofs),
        "cognitive_transition_refs": _unique(ref for item in proofs for ref in item.get("cognitive_transition_refs", [])),
        "gateways": gateways,
        "proofs": proofs,
        "traceability": traceability,
        "closure_candidate_ref": closure.get("assessment_ref"),
        "closure_acceptance_ref": acceptance.get("decision_ref"),
        "closure_acceptance_owner_ref": acceptance.get("governing_owner_ref"),
        "lifecycle_closure_ref": (case.get("lifecycle_closure") or {}).get("lifecycle_closure_ref"),
        "assimilation_candidate_ref": assimilation.get("assimilation_ref"),
        "assimilation_candidate_only": assimilation.get("candidate_only"),
        "brain_responsibility_domain": case.get("brain_responsibility_domain"),
        "brain_canonical_owner_status": case.get("brain_canonical_owner_status"),
        "negative_guards": case.get("negative_guards", {}),
        "forbidden_behaviors": {
            "model_invocation": all(item.get("model_invocation") is False for item in proofs),
            "provider_invocation": all(item.get("provider_invocation") is False for item in proofs),
            "live_observation_execution": all(item.get("live_observation_execution") is False for item in proofs),
            "field_mutation": all(item.get("field_mutation") is False for item in proofs),
            "world_truth_declared": all(item.get("world_truth_declared") is False for item in proofs),
            "memory_mutation": (case.get("assimilation_candidate") or {}).get("memory_mutation") is False,
            "experience_mutation": (case.get("assimilation_candidate") or {}).get("experience_mutation") is False,
            "learning_mutation": (case.get("assimilation_candidate") or {}).get("learning_executed") is False,
            "decision_execution": (case.get("assimilation_candidate") or {}).get("decision_created") is False,
            "task_execution": (case.get("assimilation_candidate") or {}).get("automatic_task_generation") is False,
            "action_execution": all(item.get("action_execution") is False for item in proofs)
            and (case.get("assimilation_candidate") or {}).get("action_executed") is False,
        },
        "validation_errors": case.get("validation_errors", []),
        "raw_case": case,
    }


def build_runner_summary_v1() -> Dict[str, Any]:
    run = build_brain_closure_run_v1(EXECUTION_INSTANCE_REF)
    cases = [_case_summary(case) for case in run["cases"]]
    return {
        "phase": PHASE,
        "source_integration_phase": run["phase"],
        "execution_instance_ref": run["execution_instance_ref"],
        "responsibility_domain": run["responsibility_domain"],
        "canonical_owner_status": run["canonical_owner_status"],
        "case_count": len(cases),
        "cases": cases,
        "negative_test": run["negative_test"],
        "negative_guards": run["negative_guards"],
        "negative_guard_coverage": run["negative_guard_coverage"],
        "deferred": run["deferred"],
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
