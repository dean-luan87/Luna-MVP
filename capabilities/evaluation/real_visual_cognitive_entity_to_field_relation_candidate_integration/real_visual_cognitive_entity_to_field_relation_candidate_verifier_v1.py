"""Fail-closed verifier for candidate-only Entity-to-Field relations."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict


ROOT = Path(__file__).resolve().parents[3]
OUTPUT = (
    ROOT
    / "_eval_out/real_visual_cognitive_entity_to_field_relation_candidate_integration_v1/runner_summary_v1.json"
)
PHASE = "Phase-P1-Luna-Real-Cognitive-Entity-To-Field-Relation-Candidate-Integration-v1-001"


def _check(checks: Dict[str, bool], name: str, value: bool) -> None:
    checks[name] = bool(value)


def _cases(summary: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    return {str(item.get("case_id")): item for item in summary.get("cases", [])}


def _positive_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and value > 0


def _verify(summary: Dict[str, Any]) -> Dict[str, Any]:
    checks: Dict[str, bool] = {}
    cases = _cases(summary)
    positive = cases.get("ENTITY_OBSERVED_IN_FIELD_RELATION_CREATED", {})
    positive_entities = positive.get("entity_candidates") or []
    positive_relations = positive.get("relation_candidates") or []
    relation = dict(positive_relations[0]) if positive_relations else {}
    entity = dict(positive_entities[0]) if positive_entities else {}
    relation_traces = positive.get("relation_traces") or []
    relation_trace = dict(relation_traces[0]) if relation_traces else {}
    trace = dict(positive.get("semantic_trace") or {})
    trace_payload = dict(trace.get("payload") or {})
    behavior = dict(positive.get("behavior") or {})
    forbidden = dict(summary.get("forbidden_behaviors") or {})

    required = {
        "ENTITY_OBSERVED_IN_FIELD_RELATION_CREATED",
        "OBSERVED_IN_FIELD_NOT_BELONGS_TO_FIELD",
        "RELATION_CANDIDATE_NOT_FACT",
        "RELATION_CANDIDATE_NOT_PERSISTENT_RELATION",
        "RELATION_DOES_NOT_RESOLVE_ENTITY_IDENTITY",
        "ENTITY_CANDIDATE_NOT_SOURCE_DIVERSITY",
        "ENTITY_CANDIDATE_NOT_MEMORY_IDENTITY",
        "SAME_CLASS_ENTITIES_HAVE_INDEPENDENT_FIELD_RELATIONS",
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
    _check(checks, "real_evidence_present", _positive_number(summary.get("real_visual_evidence_count", 0)))
    _check(checks, "real_detection_present", _positive_number(summary.get("detection_count", 0)))
    dimensions = dict(summary.get("frame_dimensions") or {})
    _check(checks, "real_bbox_and_frame_lineage", bool(entity.get("attributes", {}).get("bbox_observation_geometry")) and _positive_number(dimensions.get("width")) and _positive_number(dimensions.get("height")))
    _check(checks, "field_context_candidate", summary.get("field_ref") == "field:visual-frame:v1" and summary.get("field_ref_resolution_status") == "CONTROLLED_CONTEXT_CANDIDATE")
    _check(checks, "relation_candidate_created", bool(relation.get("relation_id")))
    _check(checks, "canonical_relation_contract_reused", relation.get("candidate_only") is True and relation.get("fact_admitted") is False)
    _check(checks, "entity_to_field_mapping", relation.get("subject_ref") == entity.get("entity_id") and relation.get("object_ref") == summary.get("field_ref"))
    _check(checks, "observed_in_field_predicate", relation.get("predicate") == "OBSERVED_IN_FIELD")
    _check(
        checks,
        "relation_traceable",
        bool(
            relation.get("evidence_refs")
            and relation.get("trace_ref")
            and relation.get("provenance_refs")
            and relation_trace.get("trace_ref") == relation.get("trace_ref")
            and relation_trace.get("runtime_observation_ref")
            == summary.get("runtime_observation_ref")
            and relation_trace.get("evidence_refs")
            == relation.get("evidence_refs")
            and relation_trace.get("source_detection_refs")
            and all(
                detection_ref in (entity.get("provenance_refs") or ())
                for detection_ref in relation_trace.get("source_detection_refs")
            )
            and relation_trace.get("entity_candidate_ref")
            == entity.get("entity_id")
            and relation_trace.get("subject_binding_ref")
            in (positive.get("subject_binding_refs") or ())
            and relation_trace.get("relation_candidate_ref")
            == relation.get("relation_id")
            and relation_trace.get("field_ref_candidate")
            == summary.get("field_ref")
            and relation_trace.get("field_ref_resolution_status")
            == summary.get("field_ref_resolution_status")
            and trace_payload.get("relation_candidate_ref")
            == relation.get("relation_id")
        ),
    )
    _check(checks, "relation_candidate_not_belongs_to_field", behavior.get("observed_in_field_not_belongs_to_field") is True)
    _check(checks, "relation_candidate_not_fact", behavior.get("relation_candidate_not_fact") is True and summary.get("fact_admitted") is False)
    _check(checks, "relation_candidate_not_persistent_relation", behavior.get("relation_candidate_not_persistent_relation") is True and summary.get("persistent_relation_declared") is False)
    _check(checks, "relation_does_not_resolve_entity_identity", behavior.get("relation_does_not_resolve_entity_identity") is True and summary.get("identity_resolution_status") == "UNRESOLVED")
    _check(checks, "same_class_entities_have_independent_relations", cases.get("SAME_CLASS_ENTITIES_HAVE_INDEPENDENT_FIELD_RELATIONS", {}).get("behavior", {}).get("same_relation_ids_are_independent") is True)
    same_class_entities = cases.get("SAME_CLASS_ENTITIES_HAVE_INDEPENDENT_FIELD_RELATIONS", {}).get("entity_candidates", [])
    same_class_relations = cases.get("SAME_CLASS_ENTITIES_HAVE_INDEPENDENT_FIELD_RELATIONS", {}).get("relation_candidates", [])
    same_class_labels = [dict(item.get("attributes") or {}).get("class_candidate") for item in same_class_entities]
    _check(checks, "same_class_relations_preserve_class_pair", len(same_class_labels) >= 2 and same_class_labels[0] == same_class_labels[1])
    _check(checks, "same_class_entities_have_distinct_ids", len(same_class_entities) >= 2 and same_class_entities[0].get("entity_id") != same_class_entities[1].get("entity_id"))
    _check(checks, "same_class_relations_have_distinct_ids", len(same_class_relations) >= 2 and same_class_relations[0].get("relation_id") != same_class_relations[1].get("relation_id"))
    _check(checks, "cross_field_knowledge_not_meaning_reuse", summary.get("cross_field_knowledge_reuse_not_meaning_reuse") is True and behavior.get("cross_field_knowledge_not_meaning_reuse") is True)
    _check(checks, "no_field_conditioned_intrinsic_meaning", not any(key in entity.get("attributes", {}) for key in ("merchandise", "private_property", "office_supply", "ownership", "function")))
    _check(checks, "relation_confidence_not_inferred", summary.get("relation_confidence_status") == "UNAVAILABLE" and "confidence" not in relation)
    _check(checks, "relation_not_source_diversity", summary.get("relation_candidates_are_not_sources") is True and summary.get("evidence_source_count") == 1 and len(relation.get("evidence_refs") or []) == 1)
    _check(checks, "evidence_sufficiency_unchanged", summary.get("evidence_sufficiency_contract") == {"minimum_event_count": 2, "source_diversity_requirement": 2})
    _check(checks, "policy_trace_gap_preserved", summary.get("policy_trace_compatibility_gap") is True)
    _check(checks, "target_binding_unresolved", summary.get("semantic_target_resolved") is False and summary.get("target_binding_status") == "EVALUATION_CANDIDATE_CANONICAL_OWNER_UNAVAILABLE")
    _check(checks, "memory_and_pcn_not_mutated", summary.get("memory_mutation") is False and summary.get("pcn_mutation") is False)
    _check(checks, "candidate_only", summary.get("field_truth_declared") is False and summary.get("world_truth_declared") is False and summary.get("fact_admitted") is False)
    for name in ("field_truth_promotion", "world_truth_declared", "field_mutation", "decision_execution", "task_execution", "action_execution", "device_control", "camera_control", "movement_control", "memory_mutation", "pcn_mutation"):
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
