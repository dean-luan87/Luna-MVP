"""Verifier for the controlled Evidence -> Field / Current World seam."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Mapping

from capabilities.midplatform.protocol_manager.module.governance_verification_backbone_v1 import (
    compute_unified_final_decision,
)

from .fixtures_v1 import (
    EVALUATION_MARKER,
    build_evidence_context_field_current_world_cases_v1,
)


DEFAULT_SUMMARY = Path(
    "_eval_out/evidence_context_field_current_world_controlled_v1/runner_summary_v1.json"
)


def _mapping(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _list(value: Any) -> list[dict[str, Any]]:
    return [item for item in value if isinstance(item, dict)] if isinstance(value, list) else []


def _check(checks: dict[str, bool], name: str, value: bool) -> None:
    checks[name] = bool(value)


def _contains_no_semantic_payload(value: Any) -> bool:
    text = json.dumps(value, ensure_ascii=False, sort_keys=True)
    forbidden = (
        "exit_found",
        "sign_detected",
        "person_count",
        "road_open",
        "object_detected",
        "text_recognized",
    )
    return not any(token in text for token in forbidden)


def verify(summary: Mapping[str, Any]) -> dict[str, Any]:
    checks: dict[str, bool] = {}
    expected_cases = build_evidence_context_field_current_world_cases_v1()
    items = {
        _mapping(item).get("case_id"): _mapping(item)
        for item in _list(summary.get("cases"))
    }
    _check(checks, "required_cases_present", {case.case_id for case in expected_cases} <= set(items))
    _check(checks, "controlled_marker", summary.get("source_mode") == EVALUATION_MARKER)
    _check(checks, "case_count_at_least_90", int(summary.get("controlled_case_count", 0)) >= 90)
    _check(checks, "governance_backbone_reused", summary.get("governance_backbone_reused") is True)
    _check(checks, "canonical_reducer_owner", summary.get("canonical_field_reducer_owner") == "Field State Reducer")
    _check(checks, "reducer_unique_mutation_authority", summary.get("reducer_unique_mutation_authority") is True)
    _check(checks, "bridge_has_no_semantic_authority", summary.get("bridge_semantic_authority") is False)
    _check(
        checks,
        "global_negative_guards",
        all(summary.get(name) is False for name in (
            "field_state_persisted",
            "current_world_mutated",
            "truth_declared",
            "world_truth_declared",
            "memory_mutated",
            "experience_mutated",
            "decision_executed",
            "task_executed",
            "action_executed",
            "provider_invoked",
            "model_invoked",
            "network_called",
            "subprocess_started",
            "thread_started",
            "socket_used",
            "gateway_called",
            "observation_demand_created",
        )) and summary.get("synthetic_only") is True and summary.get("controlled") is True,
    )

    for case in expected_cases:
        item = items.get(case.case_id, {})
        preflight = _mapping(item.get("governance_preflight"))
        postflight = _mapping(item.get("governance_postflight"))
        formation = _mapping(item.get("field_event_formation"))
        event_candidate = _mapping(item.get("field_event_candidate"))
        admission = _mapping(item.get("field_event_admission"))
        reducer = _mapping(item.get("reducer_result"))
        field_state = _mapping(item.get("field_state"))
        field_states = _list(item.get("field_states"))
        context = _mapping(item.get("context"))
        world = _mapping(item.get("current_world"))

        _check(checks, f"{case.case_id}:preflight", preflight.get("status") == case.expected_preflight_status)
        if case.expected_preflight_status != "PASS":
            _check(
                checks,
                f"{case.case_id}:governance_hard_stop",
                item.get("business_engine_executed") is False
                and not event_candidate
                and not admission
                and not reducer
                and not field_state,
            )
            continue

        _check(checks, f"{case.case_id}:business_engine_executed", item.get("business_engine_executed") is True)
        _check(checks, f"{case.case_id}:candidate_status", item.get("candidate_status") == case.expected_candidate_status)
        _check(checks, f"{case.case_id}:admission_status", item.get("admission_status") == case.expected_admission_status)
        _check(checks, f"{case.case_id}:reducer_status", item.get("reducer_status") == case.expected_reducer_status)
        _check(checks, f"{case.case_id}:field_state_presence", bool(field_state) == case.expected_field_state_present)
        _check(checks, f"{case.case_id}:context_presence", bool(context) == case.expected_context_present)
        _check(checks, f"{case.case_id}:postflight", postflight.get("status") == case.expected_postflight_status)
        _check(checks, f"{case.case_id}:nullable_projection_safe", all(isinstance(value, (dict, list, type(None))) for value in (item.get("field_event_formation"), item.get("field_event_admission"), item.get("reducer_result"), item.get("field_state"), item.get("current_world"))))

        if case.expected_candidate_status == "FIELD_EVENT_CANDIDATE_FORMED":
            _check(checks, f"{case.case_id}:candidate_valid", formation.get("formation_status") == "FIELD_EVENT_CANDIDATE_FORMED" and event_candidate.get("event_id") and event_candidate.get("candidate_only") is not False)
        if case.expected_admission_status == "admitted_event":
            _check(checks, f"{case.case_id}:admitted_reducer_eligible", admission.get("admission_status") == "admitted_event" and admission.get("reducer_eligible") is True)
        if case.expected_admission_status == "REQUIRES_ADMISSION":
            _check(checks, f"{case.case_id}:non_admitted_not_reduced", not reducer and item.get("event_count") == 0 and not field_state)
        if case.expected_reducer_status == "NO_UPDATE":
            _check(checks, f"{case.case_id}:unknown_no_update", not reducer and item.get("field_state_count") == 0 and world.get("world_stability_candidate") == "UNKNOWN")
        if case.conflict:
            conflict_result = _mapping(reducer.get("reduction_summary"))
            _check(checks, f"{case.case_id}:conflict_preserved", conflict_result.get("conflict_status") in {"unresolved", "conflicted"} and len(field_states) == 1)
            _check(checks, f"{case.case_id}:no_winner_fabrication", "winner" not in json.dumps(reducer, sort_keys=True).lower())
        if case.correction:
            candidate = _mapping(reducer.get("field_state_candidate"))
            _check(checks, f"{case.case_id}:correction_lineage", bool(candidate.get("owner_correction_refs")) and f"correction:controlled:{case.case_id}" in candidate.get("owner_correction_refs", []))
        if case.temporary_overlay:
            overlay = _mapping(reducer.get("reduction_summary"))
            _check(checks, f"{case.case_id}:overlay_governed", overlay.get("overlay_status") in {"temporary_overlay_candidate", "overlay_expired"})
        if case.reopened:
            _check(checks, f"{case.case_id}:reopen_is_new_event", "event:prior:" not in event_candidate.get("event_id", "") and _mapping(event_candidate.get("payload")).get("supersedes_ref") == f"event:prior:{case.case_id}")
        if case.duplicate_event:
            replay = _mapping(item.get("replay_admission"))
            _check(checks, f"{case.case_id}:duplicate_replay", replay.get("admission_status") == "duplicate_event" and replay.get("reason_code") == "ADMISSION_DUPLICATE_EVENT_ID")

    valid = _mapping(items.get("VALID_EVIDENCE_FORMS_FIELD_EVENT_CANDIDATE"))
    state = _mapping(valid.get("field_state"))
    event = _mapping(valid.get("field_event_candidate"))
    candidate = _mapping(valid.get("reducer_result")).get("field_state_candidate")
    _check(checks, "field_state_is_reducer_projection", state.get("produced_by") == "field_state_reducer" and state.get("candidate_only") is True and state.get("state_mutation_executed") is False)
    _check(checks, "field_state_preserves_event_and_evidence", bool(state.get("source_chain")) and bool(state.get("evidence_refs")) and event.get("event_id") in state.get("source_chain", ()))
    _check(checks, "field_state_candidate_is_not_truth", _mapping(candidate).get("candidate_only") is True and _mapping(candidate).get("fact_admitted") is False)
    optional_evidence = _list(_mapping(items.get("MODEL_NULL_REMAINS_OPTIONAL")).get("evidence"))
    _check(checks, "model_null_optional", bool(optional_evidence) and optional_evidence[0].get("source_model_ref") is None)
    explicit_evidence = _list(_mapping(items.get("EXPLICIT_MODEL_CARRY_FORWARD")).get("evidence"))
    _check(checks, "explicit_model_carried_forward", bool(explicit_evidence) and explicit_evidence[0].get("source_model_ref") == "model:controlled:explicit")
    _check(checks, "context_is_reference_only", all(_mapping(item.get("context")).get(name) is not True for item in items.values() for name in ("state_mutation", "fact_write_executed", "truth_declared")))
    _check(checks, "current_world_is_candidate_only", all(not _mapping(item.get("current_world")) or (_mapping(item.get("current_world")).get("candidate_only") is True and _mapping(item.get("current_world")).get("field_mutation") is False and _mapping(item.get("current_world")).get("field_truth_declaration") is False) for item in items.values()))
    _check(checks, "opaque_payload_and_no_interpretation", all(_contains_no_semantic_payload(item.get("evidence")) and _contains_no_semantic_payload(item.get("field_event_candidate")) for item in items.values()))

    signage = _mapping(items.get("SCENARIO12_SIGNAGE_FIELD_CANDIDATE"))
    flow = _mapping(items.get("SCENARIO12_FLOW_FIELD_CANDIDATE"))
    independent = _mapping(items.get("SCENARIO12_INDEPENDENT_FIELD_LINEAGE"))
    _check(checks, "scenario12_signage_path", bool(_mapping(signage.get("field_state"))) and _mapping(signage.get("field_state")).get("candidate_only") is True)
    _check(checks, "scenario12_flow_path", bool(_mapping(flow.get("field_state"))) and _mapping(flow.get("field_state")).get("candidate_only") is True)
    _check(checks, "scenario12_independent_lineage", independent.get("event_count") == 2 and independent.get("field_state_count") == 2 and len({_mapping(value).get("state_id") for value in _list(independent.get("field_states"))}) == 2)
    _check(checks, "scenario12_no_automerged_semantics", _contains_no_semantic_payload(independent) and independent.get("field_ref") == "field:scenario12:independent")

    phase_preflight = all(
        _mapping(item.get("governance_preflight")).get("status") == case.expected_preflight_status
        for case in expected_cases
        for item in (items.get(case.case_id, {}),)
    )
    phase_postflight = all(
        _mapping(item.get("governance_postflight")).get("status") == case.expected_postflight_status
        for case in expected_cases
        if case.expected_preflight_status == "PASS"
        for item in (items.get(case.case_id, {}),)
    )
    failed = [name for name, passed in checks.items() if not passed]
    cognitive = "PASS" if not failed else "FAIL"
    operational = "PASS" if not failed else "FAIL"
    final_decision = compute_unified_final_decision(
        functional_checks_passed=not failed,
        contract_failures=tuple(failed),
        governance_preflight="PASS" if phase_preflight else "GOVERNANCE_PREFLIGHT_BLOCKED",
        governance_postflight="PASS" if phase_postflight else "GOVERNANCE_POSTFLIGHT_BLOCKED",
        cognitive_logic_result=cognitive,
        operational_result=operational,
    )
    return {
        "check_count": len(checks),
        "passed_count": sum(1 for value in checks.values() if value),
        "failed_checks": failed,
        "all_checks_passed": not failed,
        "contract_failures": failed,
        "governance_preflight": "PASS" if phase_preflight else "GOVERNANCE_PREFLIGHT_BLOCKED",
        "governance_postflight": "PASS" if phase_postflight else "GOVERNANCE_POSTFLIGHT_BLOCKED",
        "cognitive_logic_result": cognitive,
        "operational_result": operational,
        "final_decision": final_decision,
        "status": "VERIFIED_ARTIFACT_RESULT",
    }


def main() -> int:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_SUMMARY
    result = verify(json.loads(path.read_text(encoding="utf-8")))
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if result["final_decision"] == "GO" else 1


if __name__ == "__main__":
    raise SystemExit(main())
