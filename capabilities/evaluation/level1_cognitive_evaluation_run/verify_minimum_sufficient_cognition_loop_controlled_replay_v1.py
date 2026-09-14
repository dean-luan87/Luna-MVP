"""User-terminal fail-closed Verifier for the two-case cognition loop."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List

from capabilities.evaluation.level1_cognitive_evaluation_run.archive_v1 import (
    read_evaluation_run_record_v1,
)
from capabilities.evaluation.level1_cognitive_evaluation_run.governance_v1 import (
    GOVERNANCE_ASSERTION_IDS,
)
from capabilities.midplatform.core.execution_mode_v1 import CONTROLLED_REPLAY_RUNTIME


def _case_checks(case: Dict[str, Any], *, repository_root: Path) -> Dict[str, bool]:
    checks: Dict[str, bool] = {}
    proofs = []
    archive_path = repository_root / str(case.get("archive_location", ""))
    if archive_path.is_file():
        try:
            record = read_evaluation_run_record_v1(archive_path)
            metadata = record.bounded_metadata
            proofs = list(metadata.get("canonical_cognition_proofs") or [])
            replay_inputs = list(metadata.get("replay_inputs") or [])
            trace = metadata.get("whitebox_trace") or {}
            profile = metadata.get("whitebox_profile") or {}
            plane_a = metadata.get("plane_a_result") or {}
            plane_g = metadata.get("plane_g_result") or {}
            checks["archive_contract_valid"] = True
            checks["archive_identity_matches"] = record.evaluation_run.evaluation_run_id == case.get("evaluation_run_id")
            checks["archive_is_not_eval_output"] = "_eval_out" not in str(archive_path)
            checks["archive_immutable"] = record.immutable_by_identity and record.append_or_supersede_only
            checks["whitebox_v1_payload_present"] = bool(trace.get("trace_id") and trace.get("nodes") and profile.get("execution_profile_id"))
            checks["whitebox_profile_links_trace"] = profile.get("cognitive_trace_ref") == trace.get("trace_id")
            checks["whitebox_transitions_linked"] = tuple(trace.get("transition_refs") or ()) == tuple(case.get("cognitive_transition_refs") or ())
            checks["plane_a_passed"] = plane_a.get("status") == "PASS"
            checks["plane_g_compliant"] = plane_g.get("compliance_status") == "COMPLIANT"
            checks["plane_g_assertions_complete"] = set(
                item.get("assertion_id") for item in plane_g.get("assertion_results") or ()
            ) == set(GOVERNANCE_ASSERTION_IDS)
            checks["plane_g_assertions_pass"] = all(
                item.get("status") == "PASS" and item.get("passed") is True
                for item in plane_g.get("assertion_results") or ()
            )
            checks["replay_inputs_archived"] = len(replay_inputs) == case.get("cognitive_cycle_count")
        except (OSError, KeyError, TypeError, ValueError, json.JSONDecodeError):
            checks["archive_contract_valid"] = False
    else:
        checks["archive_contract_valid"] = False
    proofs = proofs or list(case.get("canonical_cognition_proofs") or [])
    checks["controlled_replay_mode"] = case.get("execution_mode") == CONTROLLED_REPLAY_RUNTIME
    checks["cognition_executed"] = case.get("cognition_execution") is True and case.get("runtime_executed") is True
    checks["canonical_owner"] = all(
        proof.get("owner_ref") == "Cognitive State Formation Governance" for proof in proofs
    ) and bool(proofs)
    checks["transition_proof_present"] = case.get("cognitive_transition_count", 0) >= 1 and bool(case.get("cognitive_transition_refs"))
    checks["whitebox_refs_present"] = bool(case.get("whitebox_trace_ref")) and bool(case.get("whitebox_profile_ref"))
    checks["no_forbidden_capabilities"] = all(
        case.get(key) is False
        for key in (
            "model_invocation",
            "provider_invocation",
            "live_observation_execution",
            "action_execution",
            "field_mutation",
            "world_truth_declared",
            "memory_promotion",
            "knowledge_promotion",
            "experience_promotion",
        )
    )
    checks["unavailable_metrics_explicit"] = bool(case.get("unavailable_metrics"))

    if case.get("case_id") == "sufficient-and-stop":
        sufficiency = case.get("sufficiency") or []
        checks["case_a_one_cycle"] = case.get("cognitive_cycle_count") == 1
        checks["case_a_sufficient"] = len(sufficiency) == 1 and sufficiency[0].get("status") == "SUFFICIENT"
        checks["case_a_stop_present"] = len(case.get("stop_refs") or []) == 1 and bool(case.get("stop_reasons") or [])
        checks["case_a_no_gap"] = not case.get("information_gap_refs")
        checks["case_a_no_reobservation"] = not case.get("reobservation_refs") and not case.get("next_cycle_ingress_refs")
        checks["case_a_no_unnecessary_observation"] = case.get("unnecessary_observation") is False
    else:
        sufficiency = case.get("sufficiency") or []
        checks["case_b_two_cycles"] = case.get("cognitive_cycle_count") == 2
        checks["case_b_cycle_1_insufficient"] = len(sufficiency) >= 1 and sufficiency[0].get("status") == "INSUFFICIENT"
        checks["case_b_cycle_2_sufficient"] = len(sufficiency) == 2 and sufficiency[1].get("status") == "SUFFICIENT"
        checks["case_b_gap_present"] = len(case.get("information_gap_refs") or []) == 1
        checks["case_b_reobservation_present"] = len(case.get("reobservation_refs") or []) == 1
        checks["case_b_next_cycle_present"] = len(case.get("next_cycle_ingress_refs") or []) == 1
        checks["case_b_revision_present"] = len(case.get("hypothesis_revision_refs") or []) == 1
        checks["case_b_final_stop_present"] = len(case.get("stop_refs") or []) == 1 and bool(case.get("stop_reasons") or [])
        if len(proofs) == 2 and len(replay_inputs) == 2:
            checks["case_b_gap_to_reobservation"] = proofs[0].get("reobservation_information_gap_ref") == proofs[0].get("information_gap_ref")
            checks["case_b_replay_linked_to_gap"] = (
                replay_inputs[1].get("prior_information_gap_ref") == proofs[0].get("information_gap_ref")
                and replay_inputs[1].get("prior_reobservation_ref") == proofs[0].get("reobservation_ref")
                and replay_inputs[1].get("prior_next_cycle_ingress_ref") == proofs[0].get("next_cycle_ingress_ref")
            )
            checks["case_b_revision_linked"] = proofs[1].get("hypothesis_revision_ref") is not None and proofs[1].get("hypothesis_revision_information_gap_ref") == proofs[0].get("information_gap_ref") and proofs[1].get("hypothesis_revision_reobservation_ref") == proofs[0].get("reobservation_ref")
            checks["case_b_stop_after_sufficiency"] = proofs[1].get("sufficiency_status") == "SUFFICIENT" and proofs[1].get("stop_ref") is not None
        else:
            checks["case_b_gap_to_reobservation"] = False
            checks["case_b_replay_linked_to_gap"] = False
            checks["case_b_revision_linked"] = False
            checks["case_b_stop_after_sufficiency"] = False
    return checks


def verify_summary_v1(summary: Dict[str, Any], *, repository_root: Path) -> Dict[str, Any]:
    case_results = list(summary.get("case_results") or [])
    checks: Dict[str, bool] = {
        "exactly_two_cases": len(case_results) == 2,
        "phase_validation_clean": not summary.get("phase_validation_errors"),
        "all_cases_archived": summary.get("all_cases_archived") is True,
        "all_cases_governance_compliant": summary.get("all_cases_governance_compliant") is True,
        "phase_forbidden_capabilities_false": all(
            summary.get(key) is False
            for key in (
                "model_invocation",
                "provider_invocation",
                "live_observation_execution",
                "action_execution",
                "field_mutation",
                "world_truth_declared",
                "memory_promotion",
                "knowledge_promotion",
                "experience_promotion",
            )
        ),
    }
    for index, case in enumerate(case_results, start=1):
        for name, passed in _case_checks(case, repository_root=repository_root).items():
            checks[f"case_{index}:{name}"] = passed
    issues: List[str] = [name for name, passed in checks.items() if not passed]
    return {
        "phase": "Phase-P1-Luna-Level1-Minimum-Sufficient-Cognition-Loop-Controlled-Replay-v1-001",
        "checks": checks,
        "issues": issues,
        "all_checks_passed": not issues,
        "status": "WAITING_FOR_USER_TERMINAL_VERIFICATION",
    }


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit(
            "usage: python -m capabilities.evaluation.level1_cognitive_evaluation_run.verify_minimum_sufficient_cognition_loop_controlled_replay_v1 <runner_summary.json>"
        )
    summary = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    result = verify_summary_v1(summary, repository_root=Path.cwd())
    print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True))
    return 0 if result["all_checks_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
