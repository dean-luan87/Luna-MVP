"""Independent verifier for the consolidated synthetic regression summary."""

from __future__ import annotations

from typing import Any, Dict

from .cross_module_checks_v1 import EXPECTED_CROSS_MODULE_CASE_COUNT
from .manifest_v1 import CHILD_MODULES, DOCUMENT_FILES, PHASE


def _child_checks_ok(child: Dict[str, Any], required_checks: tuple[str, ...]) -> bool:
    return child.get("runner_passed") is True and child.get("verifier_passed") is True and all(child.get("verifier_checks", {}).get(name) is True for name in required_checks)


def verify_summary(summary: Dict[str, Any]) -> Dict[str, bool]:
    children = summary.get("child_results", {})
    child_regressions_ok = summary.get("child_regressions_ok") is True and all(
        _child_checks_ok(children.get(spec.module_id, {}), spec.required_checks) for spec in CHILD_MODULES
    )
    checks = {
        "child_regressions_ok": child_regressions_ok,
        "authority_continuity_ok": summary.get("authority_continuity_ok") is True,
        "responsibility_continuity_ok": summary.get("responsibility_continuity_ok") is True,
        "reference_continuity_ok": summary.get("reference_continuity_ok") is True,
        "version_domain_continuity_ok": summary.get("version_domain_continuity_ok") is True,
        "invalidation_continuity_ok": summary.get("invalidation_continuity_ok") is True,
        "constraint_continuity_ok": summary.get("constraint_continuity_ok") is True,
        "candidate_binding_admission_execution_separation_ok": summary.get("candidate_admission_execution_separation_ok") is True,
        "runtime_provider_separation_ok": summary.get("candidate_admission_execution_separation_ok") is True and summary.get("provider_invocation_observed") is False,
        "provider_result_evidence_separation_ok": summary.get("source_state_return_continuity_ok") is True,
        "evidence_world_truth_separation_ok": summary.get("world_truth_declared") is False,
        "action_result_task_separation_ok": summary.get("source_state_return_continuity_ok") is True,
        "outcome_brain_separation_ok": summary.get("outcome_brain_boundary_ok") is True,
        "a_local_semantic_authority_ok": summary.get("authority_continuity_ok") is True,
        "brain_global_authority_ok": summary.get("authority_continuity_ok") is True,
        "action_admission_owner_ok": summary.get("responsibility_continuity_ok") is True,
        "capability_binding_owner_ok": _child_checks_ok(children.get("CAPABILITY_MODEL_PROVIDER_BINDING", {}), ("capability_binding_owner_ok",)),
        "provider_binding_owner_ok": _child_checks_ok(children.get("CAPABILITY_MODEL_PROVIDER_BINDING", {}), ("provider_binding_owner_ok",)),
        "field_transition_owner_ok": summary.get("source_state_return_continuity_ok") is True,
        "loop_mechanical_only_ok": summary.get("loop_mechanical_boundary_ok") is True,
        "failure_return_owner_ok": summary.get("failure_return_continuity_ok") is True,
        "cross_concern_isolation_ok": any(case.get("case_id") == "cross_concern_isolation" and case.get("passed") is True for case in summary.get("cross_module_cases", ())),
        "trace_provenance_ok": summary.get("trace_provenance_ok") is True,
        "attempt_freshness_ok": summary.get("attempt_freshness_ok") is True,
        "no_stale_child_artifact_ok": summary.get("no_stale_child_artifact_ok") is True,
        "legacy_active_bypass_count_zero": summary.get("active_bypass_count") == 0 and summary.get("active_bypass_ids") == [],
        "no_runtime_execution": summary.get("runtime_execution_observed") is False,
        "no_model_loading": summary.get("model_loading_observed") is False,
        "no_provider_invocation": summary.get("provider_invocation_observed") is False,
        "no_observation_execution": summary.get("observation_execution_observed") is False,
        "no_action_execution": summary.get("action_execution_observed") is False,
        "no_source_mutation": summary.get("source_mutation_observed") is False,
        "no_world_truth": summary.get("world_truth_declared") is False,
        "negative_guards_ok": summary.get("candidate_admission_execution_separation_ok") is True and summary.get("source_mutation_observed") is False and summary.get("world_truth_declared") is False,
        "source_set_ok": summary.get("phase") == PHASE and summary.get("child_module_count") == len(CHILD_MODULES) and summary.get("cross_module_case_count") == EXPECTED_CROSS_MODULE_CASE_COUNT,
        "documentation_set_ok": summary.get("documentation_set_ok") is True and len(DOCUMENT_FILES) == 11,
    }
    checks["all_checks_passed"] = all(checks.values()) and summary.get("all_regressions_passed") is True
    return checks


if __name__ == "__main__":
    raise SystemExit("Verifier requires a current consolidated JSON summary supplied by the user terminal.")
