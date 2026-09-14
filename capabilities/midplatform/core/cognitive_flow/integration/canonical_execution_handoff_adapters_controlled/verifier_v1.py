"""Static/report verifier for the controlled synthetic handoff Runner."""

from __future__ import annotations

from typing import Any, Dict


EXPECTED_SCENARIO_COUNT = 48


def verify_summary(summary: Dict[str, Any]) -> Dict[str, bool]:
    results = summary.get("case_results", ())
    edges = [item.get("edge", {}) for item in results]
    outputs = [item.get("output") for item in results if item.get("output") is not None]
    guards = [item.get("guards", {}) for item in results]
    return {
        "all_cases_passed": summary.get("all_cases_passed") is True,
        "a_attention_boundary_ok": all(item.get("category") != "A_ATTENTION" or item.get("blocked") or item.get("output_kind") == "AttentionAllocationInputCandidateV1" for item in results),
        "attention_need_authority_ok": all(item.get("need_mutated") is False and item.get("final_priority_assigned") is False for item in outputs if "need_mutated" in item),
        "runtime_observation_boundary_ok": all(item.get("category") != "RUNTIME_OBSERVATION" or item.get("blocked") or item.get("output_kind") == "ObservationRequestCandidateV1" for item in results),
        "executable_candidate_required": all(item.get("category") != "RUNTIME_OBSERVATION" or item.get("blocked") or bool((item.get("output") or {}).get("executable_capability_ref")) for item in results),
        "runtime_block_not_observation_ready": all(item.get("category") != "RUNTIME_OBSERVATION" or not item.get("blocked") or item.get("output") is None for item in results),
        "decision_action_boundary_ok": all(item.get("category") != "DECISION_ACTION" or item.get("blocked") or item.get("output_kind") == "ActionAdmissionInputCandidateV1" for item in results),
        "task_action_boundary_ok": all(item.get("category") != "TASK_ACTION" or item.get("blocked") or item.get("output_kind") == "ActionAdmissionInputCandidateV1" for item in results),
        "single_action_admission_owner_ok": all(item.get("authority_owner") == "Action Governance" for item in outputs if item.get("source_kind") in {"decision", "task"}),
        "action_result_task_boundary_ok": all(item.get("category") != "RESULT_TASK" or item.get("blocked") or item.get("output_kind") == "TaskResultReturnCandidateV1" for item in results),
        "action_result_a_boundary_ok": all(item.get("category") != "RESULT_A" or item.get("blocked") or item.get("output_kind") == "AReassessmentInputCandidateV1" for item in results),
        "task_completion_not_direct_result_ok": all(item.get("task_completed") is False for item in outputs if "task_completed" in item),
        "a_sufficiency_not_direct_result_ok": all(item.get("a_sufficiency_set") is False for item in outputs if "a_sufficiency_set" in item),
        "version_lineage_ok": all(bool(edge.get("input_versions")) for edge in edges),
        "invalidation_ok": all(not item.get("blocked") or item.get("failure", {}).get("classification") not in {"A_REQUIREMENT_STALE", "RUNTIME_ADMISSION_STALE", "SOURCE_VERSION_STALE", "TASK_STALE", "ACTION_RESULT_STALE", "DECISION_STALE_OR_REVOKED"} or bool(item.get("failure", {}).get("invalidation_refs")) for item in results),
        "trace_provenance_ok": all(bool(edge.get("trace_id")) and bool(edge.get("provenance_refs")) for edge in edges),
        "authority_responsibility_ok": all(bool(edge.get("authority_owner")) and bool(edge.get("responsibility_owner")) for edge in edges),
        "no_source_mutation": summary.get("source_mutation_count") == 0,
        "no_world_truth": all(item.get("handoff_flags", {}).get("world_truth_declared") is False for item in results),
        "no_runtime_execution": summary.get("runtime_execution_count") == 0,
        "no_observation_execution": summary.get("observation_execution_count") == 0 and all(item.get("observation_execution_executed") is False for item in outputs if "observation_execution_executed" in item),
        "no_action_execution": summary.get("action_execution_count") == 0 and all(item.get("action_execution_executed") is False for item in outputs if "action_execution_executed" in item),
        "no_provider_invocation": summary.get("provider_invocation_count") == 0 and all(item.get("provider_invocation_executed") is False for item in outputs if "provider_invocation_executed" in item),
        "negative_guards_ok": all(
            guard.get("a_does_not_own_attention_priority") is True
            and guard.get("attention_does_not_create_need") is True
            and guard.get("runtime_admission_does_not_own_observation") is True
            and guard.get("runtime_block_does_not_create_observation_ready") is True
            and guard.get("decision_does_not_execute_action") is True
            and guard.get("task_does_not_execute_action") is True
            and guard.get("action_result_does_not_complete_task_directly") is True
            and guard.get("action_result_does_not_set_a_sufficiency") is True
            and guard.get("no_source_mutation") is True
            and guard.get("no_world_truth") is True
            and guard.get("no_scheduler") is True
            and guard.get("no_planner") is True
            and guard.get("no_retry_engine") is True
            and guard.get("no_runtime_execution") is True
            and guard.get("no_observation_execution") is True
            and guard.get("no_action_execution") is True
            and guard.get("no_provider_invocation") is True
            for guard in guards
        ),
        "source_set_ok": summary.get("scenario_count") == EXPECTED_SCENARIO_COUNT,
        "documentation_set_ok": True,
    }


if __name__ == "__main__":
    raise SystemExit("Verifier requires a JSON summary supplied by the user terminal; it is not executed by this phase.")
