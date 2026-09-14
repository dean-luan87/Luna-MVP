"""Fail-closed verifier for relation-bearing Field Event admission."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict


ROOT = Path(__file__).resolve().parents[3]
OUTPUT = (
    ROOT
    / "_eval_out/real_visual_relation_to_field_semantic_event_admission_integration_v1/runner_summary_v1.json"
)
PHASE = (
    "Phase-P1-Luna-Relation-Candidate-To-Field-Semantic-Event-Admission-"
    "Integration-v1-001"
)
RELATION_KIND = "ENTITY_TO_FIELD_OBSERVATION_RELATION"
TARGET_BINDING_STATUS = "EVALUATION_CANDIDATE_CANONICAL_OWNER_UNAVAILABLE"


def _check(checks: Dict[str, bool], name: str, value: bool) -> None:
    checks[name] = bool(value)


def _cases(summary: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    return {str(item.get("case_id")): item for item in summary.get("cases", [])}


def _verify(summary: Dict[str, Any]) -> Dict[str, Any]:
    checks: Dict[str, bool] = {}
    cases = _cases(summary)
    positive = cases.get("ENTITY_FIELD_RELATION_SEMANTIC_EVENT_ADMITTED", {})
    relation = dict(positive.get("relation_candidate") or {})
    projection = dict(positive.get("projection") or {})
    event = dict(positive.get("field_event_candidate") or {})
    payload = dict(event.get("payload") or {})
    admission = dict(positive.get("admission") or {})
    admitted_payload = dict(
        dict(admission.get("reducer_input_candidate") or {}).get("payload") or {}
    )
    behavior = dict(positive.get("behavior") or {})

    required = {
        "ENTITY_FIELD_RELATION_SEMANTIC_EVENT_ADMITTED",
        "RELATION_EVENT_NOT_FIELD_TRUTH",
        "OBSERVED_IN_FIELD_NOT_BELONGS_TO_FIELD",
        "RELATION_EVENT_NOT_PERSISTENT_RELATION",
        "RELATION_EVENT_DOES_NOT_RESOLVE_IDENTITY",
        "RELATION_EVENT_NOT_SOURCE_DIVERSITY",
        "UNRESOLVED_FIELD_REF_NOT_ADMITTED",
    }
    _check(checks, "phase", summary.get("phase") == PHASE)
    _check(checks, "required_cases", required <= set(cases))
    _check(checks, "real_provider_invoked", summary.get("provider_invoked") is True)
    _check(checks, "real_model_invoked", summary.get("model_invoked") is True)
    _check(
        checks,
        "provider_real_execution_verified",
        summary.get("provider_real_execution_verified") is True,
    )
    _check(
        checks,
        "recorded_provider_result_not_used",
        summary.get("recorded_provider_result_used") is False,
    )
    _check(checks, "runtime_observation_present", bool(summary.get("runtime_observation_ref")))
    _check(checks, "real_evidence_present", int(summary.get("real_visual_evidence_count") or 0) > 0)
    _check(checks, "entity_candidate_present", int(summary.get("entity_candidate_count") or 0) > 0)
    _check(checks, "relation_candidate_present", int(summary.get("relation_candidate_count") or 0) > 0)
    _check(checks, "relation_candidate_contract_present", bool(relation.get("relation_id")))
    _check(checks, "relation_semantic_projection_present", bool(projection.get("projection_ref")))
    _check(checks, "relation_semantic_kind_explicit", payload.get("relation_semantic_kind") == RELATION_KIND)
    _check(checks, "field_event_candidate_present", event.get("event_id") is not None)
    _check(checks, "field_event_candidate_contract_reused", event.get("event_type") == "entity_field_relation_observed")
    _check(checks, "admission_executed", bool(positive.get("admission")))
    _check(checks, "admitted_event_present", admission.get("admission_status") == "admitted_event")
    _check(checks, "admitted_event_reducer_eligible", admission.get("reducer_eligible") is True)
    _check(checks, "relation_candidate_ref_preserved", behavior.get("relation_candidate_ref_preserved") is True)
    _check(checks, "relation_candidate_payload_matches", relation.get("relation_id") == payload.get("relation_candidate_ref") and relation.get("subject_ref") == payload.get("subject_ref") and relation.get("predicate") == payload.get("predicate") and relation.get("object_ref") == payload.get("object_ref"))
    _check(checks, "subject_ref_matches_entity", behavior.get("subject_ref_matches_entity") is True)
    _check(checks, "predicate_observed_in_field", payload.get("predicate") == "OBSERVED_IN_FIELD")
    _check(checks, "object_ref_matches_field", payload.get("object_ref") == summary.get("field_ref"))
    _check(checks, "relation_lineage_preserved", behavior.get("field_event_lineage_preserved") is True)
    _check(checks, "admitted_payload_lineage_preserved", all(
        admitted_payload.get(key) == payload.get(key)
        for key in (
            "relation_candidate_ref",
            "subject_ref",
            "predicate",
            "object_ref",
            "entity_candidate_ref",
            "runtime_observation_ref",
            "evidence_refs",
            "source_detection_refs",
            "subject_binding_ref",
        )
    ))
    _check(checks, "candidate_only", payload.get("candidate_only") is True and summary.get("candidate_only") is True)
    _check(checks, "fact_admission_false", payload.get("fact_admitted") is False and admission.get("fact_admitted") is False)
    _check(checks, "truth_declared_false", payload.get("truth_declared") is False and summary.get("truth_declared") is False)
    _check(checks, "persistent_relation_false", payload.get("persistent_relation_declared") is False and summary.get("persistent_relation_declared") is False)
    _check(checks, "identity_unresolved", payload.get("identity_resolution_status") == "UNRESOLVED" and summary.get("identity_resolution_status") == "UNRESOLVED")
    _check(checks, "target_binding_unresolved", payload.get("target_binding_status") == TARGET_BINDING_STATUS and summary.get("target_binding_status") == TARGET_BINDING_STATUS)
    _check(checks, "relation_event_not_field_truth", behavior.get("event_admission_not_field_truth") is True and summary.get("field_truth_declared") is False)
    _check(checks, "relation_event_not_world_truth", behavior.get("event_admission_not_world_truth") is True and summary.get("world_truth_declared") is False)
    _check(checks, "observed_in_field_not_belongs_to_field", behavior.get("observed_in_field_not_belongs_to_field") is True)
    _check(checks, "relation_event_not_persistent_relation", behavior.get("persistent_relation_not_declared") is True)
    _check(checks, "relation_event_does_not_resolve_identity", behavior.get("identity_unresolved") is True)
    _check(checks, "relation_event_not_source_diversity", summary.get("relation_candidates_are_not_sources") is True and summary.get("evidence_source_count") == 1)
    _check(checks, "evidence_sufficiency_unchanged", summary.get("evidence_sufficiency_contract") == {"minimum_event_count": 2, "source_diversity_requirement": 2})
    _check(checks, "unresolved_field_ref_not_admitted", cases.get("UNRESOLVED_FIELD_REF_NOT_ADMITTED", {}).get("admission", {}).get("admission_status") == "rejected_event")
    _check(checks, "field_reducer_not_invoked", summary.get("field_state_reducer_invoked") is False)
    _check(checks, "a_route_not_invoked", summary.get("a_route_invoked") is False)
    _check(checks, "policy_trace_gap_preserved", summary.get("policy_trace_compatibility_gap") is True)
    _check(checks, "cross_field_meaning_not_reused", summary.get("field_truth_declared") is False)
    _check(checks, "validation_errors_empty", not summary.get("validation_errors"))
    forbidden = dict(summary.get("forbidden_behaviors") or {})
    for name in (
        "field_truth_promotion",
        "world_truth_declared",
        "field_mutation",
        "decision_execution",
        "task_execution",
        "action_execution",
        "device_control",
        "camera_control",
        "movement_control",
        "ocr_invocation",
        "slam_invocation",
        "memory_mutation",
        "pcn_mutation",
    ):
        _check(checks, f"no_{name}", forbidden.get(name) is False)
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
