"""Fail-closed verifier for Field relation state -> A-Route assimilation."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict


ROOT = Path(__file__).resolve().parents[3]
OUTPUT = ROOT / "_eval_out/real_field_relation_state_to_a_route_assimilation_integration_v1/runner_summary_v1.json"
PHASE = "Phase-P1-Luna-Field-Relation-State-To-ARoute-Assimilation-Integration-v1-001"
STATE_TYPE = "entity_field_observation_relation_state"
PREDICATE = "OBSERVED_IN_FIELD"
RELATION_KIND = "ENTITY_TO_FIELD_OBSERVATION_RELATION"
FIELD_REF = "field:visual-frame:v1"


def _check(checks: Dict[str, bool], name: str, value: bool) -> None:
    checks[name] = bool(value)


def _verify(summary: Dict[str, Any]) -> Dict[str, Any]:
    checks: Dict[str, bool] = {}
    candidate = dict(summary.get("field_state_candidate") or {})
    value = dict(candidate.get("candidate_value") or {})
    adapter = dict(summary.get("adapter_result") or {})
    semantic_candidates = list(summary.get("typed_semantic_candidates") or [])
    semantic = dict(semantic_candidates[0] or {}) if semantic_candidates else {}
    current_world_refs = set(summary.get("current_world_relation_interpretation_refs") or ())
    route = dict(summary.get("a_route_result") or {})
    proof = dict(summary.get("cognitive_execution") or {})
    negative_cases = dict(summary.get("negative_cases") or {})
    forbidden = dict(summary.get("forbidden_behaviors") or {})

    _check(checks, "phase", summary.get("phase") == PHASE)
    _check(checks, "controlled_fixture_explicit", summary.get("source_mode") == "CONTROLLED_FIELD_RELATION_STATE_ASSIMILATION_TEST")
    _check(checks, "provider_not_reinvoked", summary.get("provider_invoked") is False and summary.get("model_invoked") is False)
    _check(checks, "recorded_provider_result_not_used", summary.get("recorded_provider_result_used") is False)
    _check(checks, "field_state_candidate_present", candidate.get("state_candidate_id") is not None)
    _check(checks, "field_state_type_accepted", candidate.get("state_type") == STATE_TYPE)
    _check(checks, "adapter_accepted", adapter.get("accepted") is True)
    _check(checks, "relation_semantic_projection_created", bool(semantic))
    _check(checks, "relation_ref_preserved", semantic.get("relation_candidate_ref") == value.get("relation_candidate_ref"))
    _check(checks, "subject_ref_preserved", semantic.get("subject_ref") == value.get("subject_ref"))
    _check(checks, "predicate_preserved", semantic.get("predicate") == PREDICATE and value.get("predicate") == PREDICATE)
    _check(checks, "object_ref_preserved", semantic.get("object_ref") == value.get("object_ref") == FIELD_REF)
    _check(checks, "relation_kind_preserved", semantic.get("relation_semantic_kind") == RELATION_KIND)
    _check(checks, "field_state_ref_preserved", semantic.get("field_state_candidate_ref") == candidate.get("state_candidate_id"))
    _check(checks, "evidence_lineage_preserved", tuple(semantic.get("evidence_refs") or ()) == tuple(value.get("evidence_refs") or ()))
    _check(checks, "source_lineage_preserved", tuple(semantic.get("source_refs") or ()) == tuple(value.get("source_refs") or ()))
    _check(checks, "provenance_lineage_preserved", set(value.get("provenance_refs") or ()).issubset(set(semantic.get("provenance_refs") or ())))
    _check(checks, "candidate_boundary_preserved", semantic.get("candidate_only") is True and semantic.get("fact_admitted") is False and semantic.get("truth_declared") is False)
    _check(checks, "persistence_boundary_preserved", semantic.get("persistent_relation_declared") is False)
    _check(checks, "identity_unresolved", semantic.get("identity_resolution_status") == "UNRESOLVED")
    _check(checks, "a_route_result_present", bool(route))
    _check(checks, "a_route_errors_empty", not route.get("errors"))
    _check(checks, "a_route_typed_consumption", bool(route.get("cognitive_execution", {}).get("relation_interpretation_semantic_candidates")))
    _check(checks, "current_world_relation_ref_present", bool(proof.get("current_world_ref")) and bool(current_world_refs) and semantic.get("relation_interpretation_ref") in current_world_refs)
    _check(checks, "current_world_handoff_preserved", semantic.get("relation_interpretation_ref") in set(proof.get("current_world_relation_interpretation_refs") or ()))
    _check(checks, "observed_in_field_not_belongs_to_field", semantic.get("predicate") not in {"BELONGS_TO_FIELD", "BELONGS_TO"})
    _check(checks, "no_semantic_strengthening", "belongs" not in str(semantic.get("interpretation_candidate", "")).lower() and "owned" not in str(semantic.get("interpretation_candidate", "")).lower())
    _check(checks, "a_route_read_only", summary.get("field_mutation") is False and summary.get("field_truth_promotion") is False)
    _check(checks, "no_truth_or_identity_promotion", summary.get("world_truth_declared") is False and summary.get("identity_resolution_status") == "UNRESOLVED")
    _check(checks, "policy_trace_gap_preserved", summary.get("policy_trace_compatibility_gap") is True)
    _check(checks, "negative_guards_fail_closed", bool(negative_cases) and all(item.get("accepted") is False and item.get("semantic_candidate_created") is False for item in negative_cases.values()))
    _check(checks, "no_raw_shortcut", forbidden.get("raw_yolo_direct_a_route_relation") is False and forbidden.get("raw_relation_direct_a_route_typed_assimilation") is False)
    for name in (
        "field_mutation",
        "field_truth_promotion",
        "world_truth_declared",
        "memory_mutation",
        "pcn_mutation",
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
