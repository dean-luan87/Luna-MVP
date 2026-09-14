"""User-terminal Runner for the controlled Brain closure integration."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

from .brain_cognitive_loop_closure_assimilation_engine_v1 import (
    build_brain_closure_run_v1,
)


OUTPUT_DIR = Path("_eval_out/brain_cognitive_loop_closure_assimilation_controlled_v1")


def _proof_summary(proof: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "execution_ref": proof.get("execution_ref"),
        "execution_mode": proof.get("execution_mode"),
        "owner_ref": proof.get("owner_ref"),
        "runtime_executed": proof.get("runtime_executed"),
        "cognitive_transition_refs": proof.get("cognitive_transition_refs", []),
        "current_world_ref": proof.get("current_world_ref"),
        "hypothesis_refs": proof.get("hypothesis_refs", []),
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
        "field_mutation": proof.get("field_mutation"),
        "world_truth_declared": proof.get("world_truth_declared"),
        "model_invocation": proof.get("model_invocation"),
        "provider_invocation": proof.get("provider_invocation"),
        "live_observation_execution": proof.get("live_observation_execution"),
        "action_execution": proof.get("action_execution"),
    }


def _case_summary(case: Dict[str, Any]) -> Dict[str, Any]:
    proofs = [_proof_summary(item) for item in case.get("cognitive_proofs", [])]
    return {
        "case_id": case.get("case_id"),
        "title": case.get("title"),
        "brain_request_ref": (case.get("brain_request") or {}).get("brain_request_ref"),
        "cognitive_loop_ref": (case.get("loop_instance") or {}).get("cognitive_loop_ref"),
        "lifecycle_owner_ref": (case.get("loop_instance") or {}).get("lifecycle_owner_ref"),
        "information_need_ref": (case.get("information_need") or {}).get("information_need_ref"),
        "information_need_responsibility_domain": (case.get("information_need") or {}).get("responsibility_domain"),
        "information_need_canonical_owner_status": (case.get("information_need") or {}).get("canonical_owner_status"),
        "execution_mode": proofs[0].get("execution_mode") if proofs else None,
        "cognition_execution": bool(proofs) and all(item.get("runtime_executed") is True for item in proofs),
        "runtime_executed": bool(proofs) and all(item.get("runtime_executed") is True for item in proofs),
        "cognitive_cycle_count": (case.get("loop_instance") or {}).get("cycle_count", 0),
        "cognitive_transition_count": sum(len(item.get("cognitive_transition_refs", [])) for item in proofs),
        "cognitive_transition_refs": [ref for item in proofs for ref in item.get("cognitive_transition_refs", [])],
        "proofs": proofs,
        "closure_candidate_ref": (case.get("closure_assessment") or {}).get("assessment_ref"),
        "closure_acceptance_ref": (case.get("closure_acceptance") or {}).get("decision_ref"),
        "closure_acceptance_owner_ref": (case.get("closure_acceptance") or {}).get("governing_owner_ref"),
        "brain_responsibility_domain": case.get("brain_responsibility_domain"),
        "brain_canonical_owner_status": case.get("brain_canonical_owner_status"),
        "lifecycle_closure_ref": (case.get("lifecycle_closure") or {}).get("lifecycle_closure_ref"),
        "closure_record_ref": (case.get("cognitive_outcome") or {}).get("closure_record_ref"),
        "cognitive_outcome_ref": (case.get("cognitive_outcome") or {}).get("outcome_ref"),
        "assimilation_candidate_ref": (case.get("assimilation_candidate") or {}).get("assimilation_ref"),
        "assimilation_candidate_only": (case.get("assimilation_candidate") or {}).get("candidate_only"),
        "negative_guards": case.get("negative_guards", {}),
        "validation_errors": case.get("validation_errors", []),
        "raw_case": case,
    }


def build_runner_summary_v1() -> Dict[str, Any]:
    run = build_brain_closure_run_v1()
    cases = [_case_summary(case) for case in run["cases"]]
    return {
        "phase": run["phase"],
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
