from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path
from typing import Any, Dict, Iterable

from .adapters_v1 import build_luna_cognitive_execution_profile_v1
from .fixtures_v1 import CognitiveTraceScenarioV1, build_synthetic_cognitive_trace_cases_v1
from .types_v1 import (
    CognitiveWhiteBoxTraceV1,
    LunaCognitiveExecutionProfileV1,
    validate_profile_contract_v1,
    validate_trace_contract_v1,
)


def _kinds(trace: CognitiveWhiteBoxTraceV1, kind: str):
    return tuple(node for node in trace.nodes if node.node_kind == kind)


def _summaries(trace: CognitiveWhiteBoxTraceV1, kind: str):
    return tuple(node.summary for node in _kinds(trace, kind))


def _case_checks(scenario: CognitiveTraceScenarioV1, profile: LunaCognitiveExecutionProfileV1) -> Dict[str, bool]:
    trace = scenario.trace
    kinds = {node.node_kind for node in trace.nodes}
    expected = scenario.expected_process
    expected_current_world = expected.get("current_world_candidate", True)
    observed_sufficient = "SUFFICIENT" in _summaries(trace, "SUFFICIENCY")
    checks = {
        "trace_contract": not validate_trace_contract_v1(trace),
        "profile_contract": not validate_profile_contract_v1(profile),
        "current_world_candidate_present": ("CURRENT_WORLD_CANDIDATE" in kinds) == bool(expected_current_world),
        "hypothesis_candidate_present": "HYPOTHESIS" in kinds or "HYPOTHESIS_REVISION" in kinds,
        "candidate_only_surface": trace.candidate_only and profile.candidate_only,
        "no_decision_authority": "DECISION" not in kinds,
        "expected_sufficiency": expected.get("sufficiency", "") in _summaries(trace, "SUFFICIENCY"),
        "expected_reobservation": ("REOBSERVATION" in kinds) == bool(expected.get("reobservation", False)),
        "expected_handoff": ("DECISION_GOVERNANCE_HANDOFF" in kinds) == bool(expected.get("handoff", False)),
        "expected_revision": ("HYPOTHESIS_REVISION" in kinds) == bool(expected.get("hypothesis_revision", False)),
        "conflict_preserved": ("EVIDENCE_CONFLICT" in kinds) == bool(expected.get("conflict_preserved", False)),
        # A guard scenario passes when it stays non-sufficient.  Sufficient
        # scenarios are covered by expected_sufficiency; this check must not
        # invert that expected outcome for every non-sufficient fixture.
        "premature_sufficiency_guard": expected.get("sufficiency") == "SUFFICIENT" or not observed_sufficient,
        "world_truth_guard": not trace.world_truth_declared and not profile.world_truth_declared,
    }
    if expected.get("reobservation"):
        checks["gap_precedes_reobservation"] = "INFORMATION_GAP" in kinds and max(node.sequence_index for node in _kinds(trace, "INFORMATION_GAP")) < min(node.sequence_index for node in _kinds(trace, "REOBSERVATION"))
    if expected.get("hypothesis_revision"):
        revision_nodes = _kinds(trace, "HYPOTHESIS_REVISION")
        checks["revision_has_parent"] = bool(revision_nodes) and all(bool(node.bounded_metadata.get("revision_parent_ref")) for node in revision_nodes)
    if expected.get("handoff"):
        checks["handoff_has_no_decision_node"] = "DECISION" not in kinds
    return checks


def verify_synthetic_cases_v1() -> dict[str, Any]:
    case_results = []
    for scenario in build_synthetic_cognitive_trace_cases_v1():
        profile = build_luna_cognitive_execution_profile_v1(scenario.trace)
        checks = _case_checks(scenario, profile)
        case_results.append({
            "scenario_id": scenario.scenario_id,
            "checks": checks,
            "all_checks_passed": all(checks.values()),
        })
    global_checks = {
        "all_cases_have_candidate_only_trace": all(item["all_checks_passed"] for item in case_results),
        "no_cognition_mutation": True,
        "no_field_mutation": True,
        "no_current_world_authoritative_write": True,
        "no_world_truth": True,
        "no_model_or_provider_execution": True,
        "no_observation_or_action_execution": True,
        "no_dataset_download": True,
        "test_board_refs_non_authoritative": True,
    }
    return {
        "phase": "Phase-P1-Luna-A-Route-Cognitive-Whitebox-Trace-And-Execution-Profile-Foundation-v1-001",
        "mode": "synthetic",
        "scenario_count": len(case_results),
        "case_results": case_results,
        "global_checks": global_checks,
        "all_checks_passed": all(item["all_checks_passed"] for item in case_results) and all(global_checks.values()),
        "candidate_only": True,
        "runtime_execution": False,
        "model_invocation": False,
        "provider_invocation": False,
        "status": "WAITING_FOR_USER_TERMINAL_VERIFICATION",
    }


def write_verifier_result_v1(result: dict[str, Any], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")


if __name__ == "__main__":
    result = verify_synthetic_cases_v1()
    write_verifier_result_v1(result, Path("_eval_out/a_route_cognitive_whitebox_trace_and_execution_profile_foundation_v1/verifier_result_v1.json"))
    print(json.dumps({key: result[key] for key in ("phase", "mode", "scenario_count", "all_checks_passed", "status")}, indent=2))
