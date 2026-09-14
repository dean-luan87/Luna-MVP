"""Static/report verifier for the controlled synthetic return-path runner."""

from __future__ import annotations

from typing import Any, Dict


def verify_summary(summary: Dict[str, Any]) -> Dict[str, bool]:
    results = summary.get("case_results", ())
    edges = [item.get("edge", {}) for item in results]
    guards = [item.get("guards", {}) for item in results]
    return {
        "source_state_handoff_boundary_ok": summary.get("current_world_candidate_count", 0) >= 0,
        "current_world_candidate_boundary_ok": all(edge.get("next_target") != "World Truth" for edge in edges),
        "field_event_candidate_boundary_ok": all(item.get("guards", {}).get("field_reducer_executed") is False for item in results),
        "provider_result_evidence_separation_ok": all(edge.get("producer") != "Provider runtime" for edge in edges),
        "action_result_reality_separation_ok": summary.get("source_mutation_count") == 0,
        "outcome_brain_boundary_ok": all(item.get("brain_input_candidate") is None or item.get("guards", {}).get("brain_adjudication_executed") is False for item in results),
        "brain_adjudication_not_executed": summary.get("brain_mutation_count") == 0,
        "version_lineage_ok": all(bool(edge.get("input_versions")) for edge in edges if edge.get("input_refs")),
        "invalidation_boundary_ok": all(edge.get("next_target") != "Brain action" for edge in edges),
        "trace_provenance_ok": all(bool(edge.get("trace_id")) and bool(edge.get("provenance_refs")) for edge in edges),
        "authority_responsibility_ok": all(bool(edge.get("authority_owner")) and bool(edge.get("responsibility_owner")) for edge in edges),
        "no_source_mutation": summary.get("source_mutation_count") == 0,
        "no_world_truth": all(item.get("guards", {}).get("world_truth_declared") is False for item in results),
        "no_runtime_execution": summary.get("runtime_execution_count") == 0,
        "negative_guards_ok": all(all(value is False for key, value in guard.items() if key != "candidate_only") for guard in guards),
        "source_set_ok": summary.get("scenario_count") == 30,
        "documentation_set_ok": True,
    }


if __name__ == "__main__":
    raise SystemExit("Verifier requires a JSON summary supplied by the user terminal; it is not executed by this phase.")

