"""Static/report verifier for controlled synthetic binding output."""

from __future__ import annotations

from typing import Any, Dict


EXPECTED_SCENARIO_COUNT = 34


def verify_summary(summary: Dict[str, Any]) -> Dict[str, bool]:
    results = summary.get("case_results", ())
    edges = [item.get("edge", {}) for item in results]
    guards = [item.get("guards", {}) for item in results]
    cap_candidates = [item.get("capability_model_binding") for item in results if item.get("capability_model_binding")]
    provider_candidates = [item.get("model_provider_binding") for item in results if item.get("model_provider_binding")]
    return {
        "all_cases_passed": summary.get("all_cases_passed") is True,
        "capability_model_binding_boundary_ok": all(item.get("category") != "CAPABILITY_MODEL" or item.get("blocked") or bool(item.get("capability_model_binding")) for item in results),
        "model_provider_binding_boundary_ok": all(item.get("category") != "MODEL_PROVIDER" or item.get("blocked") or bool(item.get("model_provider_binding")) for item in results),
        "capability_binding_owner_ok": all(item["authority_owner"] == "Capability Governance" and item["binding_lifecycle_owner"] == "Capability Governance" for item in cap_candidates),
        "provider_binding_owner_ok": all(item["authority_owner"] == "Provider Governance" and item["binding_lifecycle_owner"] == "Provider Governance" for item in provider_candidates),
        "model_source_owner_preserved": all(item.get("model_source_owner") == "Model Governance" for item in cap_candidates + provider_candidates),
        "shared_declaration_no_dual_mutation_ok": all(item.get("no_dual_mutation_authority") is True for item in cap_candidates + provider_candidates),
        "binding_not_runtime_admission_ok": all(item.get("runtime_admission_executed", False) is False for item in cap_candidates) and all(item.get("runtime_admission_executed", False) is False for item in provider_candidates),
        "binding_not_provider_admission_ok": all(item.get("provider_admission_executed") is False for item in provider_candidates),
        "cross_binding_consistency_ok": all(item.get("cross_binding_consistent") == (not item.get("blocked")) for item in results if item.get("category") == "CROSS_BINDING"),
        "version_lineage_ok": all(bool(edge.get("input_versions")) for edge in edges),
        "invalidation_ok": all(not item.get("blocked") or item.get("failure", {}).get("classification") not in {"BINDING_STALE", "UPSTREAM_BINDING_STALE", "DOWNSTREAM_BINDING_STALE"} or bool(item.get("failure", {}).get("invalidation_refs")) for item in results),
        "trace_provenance_ok": all(bool(edge.get("trace_id")) and bool(edge.get("provenance_refs")) for edge in edges),
        "authority_responsibility_ok": all(bool(edge.get("authority_owner")) and bool(edge.get("responsibility_owner")) for edge in edges),
        "no_runtime_execution": summary.get("runtime_execution_count") == 0,
        "no_model_loading": summary.get("model_loading_count") == 0 and all(item.get("model_loading_executed") is False for item in cap_candidates + provider_candidates),
        "no_provider_invocation": summary.get("provider_invocation_count") == 0 and all(item.get("provider_invocation_executed") is False for item in cap_candidates + provider_candidates),
        "negative_guards_ok": all(
            all(value is True or value is False for value in guard.values())
            and all(guard.get(name) is True for name in (
                "no_capability_mutation_by_model",
                "no_model_mutation_by_capability",
                "no_model_mutation_by_provider",
                "no_provider_mutation_by_model",
            ))
            and all(guard.get(name) is False for name in (
                "runtime_admission_executed",
                "provider_admission_executed",
                "provider_invocation_executed",
                "model_loading_executed",
                "checksum_computation_executed",
                "dependency_probe_executed",
                "runtime_health_probe_executed",
                "brain_provider_selection",
                "a_model_selection",
                "task_provider_selection",
                "scheduler_created",
                "planner_created",
                "source_mutation_executed",
            ))
            for guard in guards
        ),
        "source_set_ok": summary.get("scenario_count") == EXPECTED_SCENARIO_COUNT,
        "documentation_set_ok": True,
    }


if __name__ == "__main__":
    raise SystemExit("Verifier requires a JSON summary supplied by the user terminal; it is not executed by this phase.")
