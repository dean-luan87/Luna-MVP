"""Fail-closed verifier for controlled typed Field relation conditioning."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict

from .types_v1 import OBSERVED_IN_FIELD, RELATION_KIND, SOURCE_MODE


PHASE = "Phase-P1-Luna-Typed-Field-Relation-Cognitive-Conditioning-Integration-v1-001"


def _check(checks: Dict[str, bool], name: str, value: Any) -> None:
    checks[name] = bool(value)


def verify(summary: Dict[str, Any]) -> Dict[str, Any]:
    checks: Dict[str, bool] = {}
    cases = {item.get("case_id"): item for item in summary.get("cases", ())}
    required = {
        "role-owner", "role-visitor", "task-seat", "task-exit",
        "goal-location", "goal-state", "role-task-owner", "role-task-visitor",
        "irrelevant-context-a", "irrelevant-context-b",
    }
    _check(checks, "phase", summary.get("phase") == PHASE)
    _check(checks, "controlled_fixture_explicit", summary.get("source_mode") == SOURCE_MODE)
    _check(checks, "no_provider_model_execution", summary.get("provider_invoked") is False and summary.get("model_invoked") is False)
    _check(checks, "recorded_provider_result_unused", summary.get("recorded_provider_result_used") is False)
    _check(checks, "required_cases", set(cases) == required)
    _check(checks, "typed_relation_semantics_stable", summary.get("typed_relation_semantics_same_across_cases") is True)
    _check(checks, "current_world_handoff", summary.get("current_world_handoff_observed") is True)
    _check(checks, "validation_errors_empty", not summary.get("validation_errors"))
    for case_id, item in cases.items():
        typed = item.get("typed_relation") or {}
        _check(checks, f"{case_id}:route_reached", item.get("route_status") in {"DEFERRED", "STOPPED"})
        _check(checks, f"{case_id}:subject_preserved", bool(typed.get("subject_ref")))
        _check(checks, f"{case_id}:predicate_observed_in_field", typed.get("predicate") == OBSERVED_IN_FIELD)
        _check(checks, f"{case_id}:object_field", typed.get("object_ref") == "field:visual-frame:v1")
        _check(checks, f"{case_id}:relation_kind", typed.get("relation_semantic_kind") == RELATION_KIND)
        _check(checks, f"{case_id}:evidence_lineage", bool(typed.get("evidence_refs")))
        _check(checks, f"{case_id}:source_lineage", bool(typed.get("source_refs")))
        _check(checks, f"{case_id}:provenance_lineage", bool(typed.get("provenance_refs")))
        _check(checks, f"{case_id}:candidate_only", typed.get("candidate_only") is True)
        _check(checks, f"{case_id}:no_fact", typed.get("fact_admitted") is False)
        _check(checks, f"{case_id}:no_truth", typed.get("truth_declared") is False)
        _check(checks, f"{case_id}:no_persistent_relation", typed.get("persistent_relation_declared") is False)
        _check(checks, f"{case_id}:identity_unresolved", typed.get("identity_resolution_status") == "UNRESOLVED")
        _check(checks, f"{case_id}:current_world_ref", bool(item.get("current_world_ref")) and item.get("relation_interpretation_ref") in item.get("current_world_relation_interpretation_refs", ()))
    contrasts = summary.get("contrast_results") or {}
    for name in (
        "SAME_TYPED_RELATION_DIFFERENT_ROLE",
        "SAME_TYPED_RELATION_DIFFERENT_TASK",
        "SAME_TYPED_RELATION_DIFFERENT_GOAL",
        "SAME_TYPED_RELATION_DIFFERENT_ROLE_AND_TASK",
        "SAME_TYPED_RELATION_IRRELEVANT_CONDITION_CHANGE",
    ):
        _check(checks, name, contrasts.get(name) is True)
    for name, value in (summary.get("negative_guards") or {}).items():
        _check(checks, f"negative:{name}", value is True)
    for name, value in {
        "candidate_only": summary.get("candidate_only"),
        "field_mutation": summary.get("field_mutation"),
        "field_truth_promotion": summary.get("field_truth_promotion"),
        "world_truth_declared": summary.get("world_truth_declared"),
        "memory_mutation": summary.get("memory_mutation"),
        "pcn_mutation": summary.get("pcn_mutation"),
        "decision_execution": summary.get("decision_execution"),
        "task_execution": summary.get("task_execution"),
        "action_execution": summary.get("action_execution"),
        "provider_model_reasoning": summary.get("provider_model_reasoning"),
        "cross_field_identity_resolution": summary.get("cross_field_identity_resolution"),
    }.items():
        _check(checks, f"boundary:{name}", value is (True if name == "candidate_only" else False))
    failed = [name for name, passed in checks.items() if not passed]
    return {
        "phase": summary.get("phase"),
        "check_count": len(checks),
        "all_checks_passed": not failed,
        "failed_checks": failed,
        "cognitive_logic_result": "PASS" if not failed else "FAIL",
        "operational_result": "PASS" if not failed else "FAIL",
        "final_decision": "GO" if not failed else "NO-GO",
        "validation_errors_empty": not summary.get("validation_errors"),
        "checks": checks,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Verify controlled typed Field relation conditioning.")
    parser.add_argument("summary", nargs="?", type=Path, default=Path("_eval_out/typed_field_relation_cognitive_conditioning_integration_v1/runner_summary_v1.json"))
    args = parser.parse_args()
    result = verify(json.loads(args.summary.read_text(encoding="utf-8")))
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    raise SystemExit(0 if result["all_checks_passed"] else 1)


if __name__ == "__main__":
    main()
