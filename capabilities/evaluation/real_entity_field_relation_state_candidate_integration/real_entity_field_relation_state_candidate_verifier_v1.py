"""Fail-closed verifier for Entity↔Field relation state candidates."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict


ROOT = Path(__file__).resolve().parents[3]
OUTPUT = ROOT / "_eval_out/real_entity_field_relation_state_candidate_integration_v1/runner_summary_v1.json"
PHASE = "Phase-P1-Luna-Entity-Field-Relation-State-Candidate-Integration-v1-001"
STATE_TYPE = "entity_field_observation_relation_state"
EVENT_TYPE = "entity_field_relation_observed"
RELATION_KIND = "ENTITY_TO_FIELD_OBSERVATION_RELATION"
PREDICATE = "OBSERVED_IN_FIELD"


def _check(checks: Dict[str, bool], name: str, value: bool) -> None:
    checks[name] = bool(value)


def _verify(summary: Dict[str, Any]) -> Dict[str, Any]:
    checks: Dict[str, bool] = {}
    real = dict(summary.get("real_single_source") or {})
    controlled = dict(summary.get("controlled_multi_source") or {})
    real_reducer = dict(real.get("reducer_result") or {})
    controlled_reducer = dict(controlled.get("reducer_result") or {})
    real_candidate = dict(real.get("typed_relation_state_candidate") or {})
    controlled_candidate = dict(controlled.get("typed_relation_state_candidate") or {})
    real_value = dict(real_candidate)
    controlled_value = dict(controlled_candidate)
    controlled_events = list(controlled.get("admitted_events") or [])
    controlled_payloads = [
        dict(event.get("payload") or {}) for event in controlled_events
    ]

    _check(checks, "phase", summary.get("phase") == PHASE)
    _check(checks, "required_cases", bool(real) and bool(controlled))
    _check(checks, "real_provider_invoked", summary.get("provider_invoked") is True)
    _check(checks, "real_model_invoked", summary.get("model_invoked") is True)
    _check(checks, "provider_real_execution_verified", summary.get("provider_real_execution_verified") is True)
    _check(checks, "recorded_provider_result_not_used", summary.get("recorded_provider_result_used") is False)
    _check(checks, "runtime_observation_present", bool(summary.get("runtime_observation_ref")))
    _check(checks, "state_type_mapping", summary.get("state_type") == STATE_TYPE)
    _check(checks, "event_type_mapping", summary.get("event_type") == EVENT_TYPE)
    _check(checks, "evidence_sufficiency_unchanged", summary.get("evidence_sufficiency_contract") == {"minimum_event_count": 2, "source_diversity_requirement": 2})
    _check(checks, "real_single_source_insufficient_evidence", summary.get("real_single_source_insufficient_evidence") is True)
    _check(checks, "real_single_source_not_typed_supported_state", not bool(real_candidate))
    _check(checks, "controlled_fixture_explicit", controlled.get("source_mode") == "CONTROLLED_MULTI_SOURCE_SEMANTIC_REDUCER_TEST")
    _check(checks, "controlled_multi_source_sufficient", summary.get("controlled_multi_source_sufficient") is True)
    _check(checks, "controlled_reducer_candidate_present", bool(controlled_reducer.get("field_state_candidate")))
    _check(checks, "typed_relation_value_created", controlled.get("behavior", {}).get("typed_relation_value_created") is True)
    _check(checks, "typed_relation_value_not_opaque_payload", controlled.get("behavior", {}).get("typed_relation_value_not_opaque_payload") is True)
    _check(checks, "subject_ref_preserved", bool(controlled_payloads) and controlled_value.get("subject_ref") == controlled_payloads[0].get("subject_ref") and all(payload.get("subject_ref") == controlled_value.get("subject_ref") for payload in controlled_payloads))
    _check(checks, "predicate_observed_in_field", controlled_value.get("predicate") == PREDICATE)
    _check(checks, "object_ref_is_field", controlled_value.get("object_ref") == summary.get("field_ref") and all(payload.get("object_ref") == summary.get("field_ref") for payload in controlled_payloads))
    _check(checks, "relation_candidate_ref_preserved", bool(controlled_value.get("relation_candidate_ref")) and controlled_value.get("relation_candidate_ref") == summary.get("relation_candidate_ref") and all(payload.get("relation_candidate_ref") == controlled_value.get("relation_candidate_ref") for payload in controlled_payloads))
    _check(checks, "relation_kind_preserved", controlled_value.get("relation_semantic_kind") == RELATION_KIND)
    _check(checks, "candidate_only", controlled_value.get("candidate_only") is True and controlled_value.get("fact_admitted") is False and summary.get("candidate_only") is True)
    _check(checks, "truth_not_declared", controlled_value.get("truth_declared") is False and summary.get("truth_declared") is False)
    _check(checks, "persistent_relation_not_declared", controlled_value.get("persistent_relation_declared") is False and summary.get("persistent_relation_declared") is False)
    _check(checks, "identity_unresolved", controlled_value.get("identity_resolution_status") == "UNRESOLVED")
    _check(checks, "observed_in_field_not_belongs_to_field", controlled_value.get("predicate") != "BELONGS_TO_FIELD" and controlled_value.get("predicate") != "BELONGS_TO")
    _check(checks, "relation_candidates_not_source_diversity", summary.get("relation_candidates_are_not_sources") is True and summary.get("entity_candidates_are_not_sources") is True and summary.get("subject_bindings_are_not_sources") is True)
    _check(checks, "field_truth_not_promoted", summary.get("field_truth_promotion") is False and summary.get("fact_admitted") is False)
    _check(checks, "world_truth_not_declared", summary.get("world_truth_declared") is False)
    _check(checks, "field_mutation_not_executed", summary.get("field_mutation") is False)
    _check(checks, "memory_pcn_not_mutated", summary.get("memory_mutation") is False and summary.get("pcn_mutation") is False)
    _check(checks, "a_route_not_invoked", summary.get("a_route_invoked") is False)
    _check(checks, "policy_trace_gap_preserved", summary.get("policy_trace_compatibility_gap") is True)
    forbidden = dict(summary.get("forbidden_behaviors") or {})
    for name in (
        "field_truth_promotion",
        "world_truth_declared",
        "field_mutation",
        "memory_mutation",
        "pcn_mutation",
        "a_route_invocation",
        "decision_execution",
        "task_execution",
        "action_execution",
        "device_control",
        "camera_control",
        "movement_control",
    ):
        _check(checks, f"no_{name}", forbidden.get(name) is False)
    _check(checks, "validation_errors_empty", not summary.get("validation_errors"))

    passed = all(checks.values())
    return {
        "phase": PHASE,
        "checks": checks,
        "all_checks_passed": passed,
        "failed_checks": [name for name, value in checks.items() if not value],
        "operational_result": "PASS" if passed else "FAIL",
        "cognitive_logic_result": "PASS" if passed else "FAIL",
        "final_decision": "GO" if passed else "NO-GO",
    }


def main() -> None:
    if not OUTPUT.exists():
        raise FileNotFoundError(f"Runner summary not found: {OUTPUT}")
    summary = json.loads(OUTPUT.read_text(encoding="utf-8"))
    print(json.dumps(_verify(summary), ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
