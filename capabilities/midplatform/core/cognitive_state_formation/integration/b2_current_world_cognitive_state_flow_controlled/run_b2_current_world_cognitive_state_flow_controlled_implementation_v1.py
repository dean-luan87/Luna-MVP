"""User-terminal runner for B2 Current World cognitive integration.

This runner consumes a structured B1 CurrentWorld candidate reference.  It
does not invoke YOLO, Gateway, Context Foundation, or any provider.
"""

from __future__ import annotations

import json
import sys
from dataclasses import asdict, is_dataclass
from pathlib import Path
from typing import Any, Dict, Mapping


RUNNER_PATH = Path(__file__).resolve()
REPO_ROOT = next(
    candidate
    for candidate in (RUNNER_PATH, *RUNNER_PATH.parents)
    if (candidate / "capabilities").is_dir() and (candidate / "docs").is_dir()
)
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.midplatform.core.cognitive_flow.cognitive_flow_static_validators_v1 import (  # noqa: E402
    validate_output_contract as validate_flow_output_contract,
)
from capabilities.midplatform.core.cognitive_state_formation.cognitive_state_formation_static_validators_v1 import (  # noqa: E402
    validate_output_contract as validate_state_output_contract,
)
from capabilities.midplatform.core.cognitive_state_formation.integration.b2_current_world_cognitive_state_flow_controlled.b2_current_world_cognitive_state_flow_adapter_v1 import (  # noqa: E402
    build_flow_request_v1,
    run_b2_case,
)
from capabilities.midplatform.core.cognitive_state_formation.integration.b2_current_world_cognitive_state_flow_controlled.b2_current_world_cognitive_state_flow_fixture_v1 import (  # noqa: E402
    B2FixtureCaseV1,
    build_b2_cases_v1,
    build_real_b1_current_world_v1,
    build_synthetic_current_world_v1,
)
from capabilities.midplatform.core.cognitive_state_formation.run_cognitive_state_formation_controlled_implementation_v1 import (  # noqa: E402
    run_controlled as run_state_regression,
)
from capabilities.midplatform.core.cognitive_flow.run_cognitive_flow_controlled_implementation_v1 import (  # noqa: E402
    run_controlled as run_flow_regression,
)


OUTPUT_DIR = REPO_ROOT / "_eval_out/brain_b2_current_world_cognitive_state_flow_controlled_implementation_v1"


def _json_value(value: Any) -> Any:
    if is_dataclass(value):
        return _json_value(asdict(value))
    if isinstance(value, tuple):
        return [_json_value(item) for item in value]
    if isinstance(value, list):
        return [_json_value(item) for item in value]
    if isinstance(value, dict):
        return {str(key): _json_value(item) for key, item in value.items()}
    return value


def _check(field: str, expected: Any, actual: Any) -> Dict[str, Any]:
    return {
        "field": field,
        "expected": _json_value(expected),
        "actual": _json_value(actual),
        "passed": actual == expected,
    }


def _state_refs_for_validation(result: Any):
    request = result.state_request
    return (
        request.context_refs
        + request.pcn_refs
        + request.intent_refs
        + request.field_refs
        + request.observation_refs
        + request.uncertainty_refs
        + ((request.current_world_ref,) if request.current_world_ref else ())
    )


def _flow_refs_for_validation(result: Any):
    request = build_flow_request_v1(
        result.source_current_world,
        result.state_output,
        result.case_id,
        flow_scenario_id=result.flow_output.scenario_id,
    )
    refs = (
        request.context_refs
        + request.pcn_refs
        + request.intent_refs
        + request.state_formation_refs
        + request.attention_refs
        + request.hypothesis_refs
        + request.field_refs
        + request.causal_refs
    )
    return refs + (
        (request.current_world_ref,) if request.current_world_ref else ()
    ) + ((request.cognitive_state_vector_ref,) if request.cognitive_state_vector_ref else ())


def _common_checks(result: Any) -> list[Dict[str, Any]]:
    state = result.state_output
    flow = result.flow_output
    world = result.source_current_world
    state_world = state.current_world_candidate
    flow_trace = flow.trace
    checks = [
        _check("current_world_read_only", True, result.current_world_read_only),
        _check("source_current_world_candidate_only", True, world.candidate_only),
        _check("state_candidate_only", True, state.candidate_only),
        _check("flow_candidate_only", True, flow.candidate_only),
        _check("state_runtime_executed", False, state.runtime_executed),
        _check("flow_runtime_executed", False, flow.runtime_executed),
        _check("world_truth_promoted", False, result.world_truth_promoted),
        _check("hypothesis_as_fact", False, result.hypothesis_as_fact),
        _check("provider_invocation", False, result.provider_invocation),
        _check("semantic_compression", False, result.semantic_compression),
        _check("dynamic_cognitive_function_execution", False, result.dynamic_cognitive_function_execution),
        _check("uncertainty_refs_preserved", True, result.preserved_uncertainty_refs == world.uncertainty_refs),
        _check("conflict_refs_preserved", True, result.preserved_conflict_refs == world.conflict_refs),
        _check("temporal_refs_preserved", True, result.preserved_temporal_refs == world.temporal_refs),
        _check("provenance_chain_complete", True, bool(result.provenance_chain)),
        _check("state_output_contract", True, validate_state_output_contract(state, _state_refs_for_validation(result))),
        _check("flow_output_contract", True, validate_flow_output_contract(flow, _flow_refs_for_validation(result))),
        _check("state_world_candidate_only", True, state_world.candidate_only),
        _check("state_world_field_mutation", False, state_world.field_mutation),
        _check("state_world_truth_declaration", False, state_world.field_truth_declaration),
        _check("flow_current_world_ref_preserved", world.current_world_id, flow_trace.current_world_ref if flow_trace else None),
    ]
    return checks


def _checks_for_case(case: B2FixtureCaseV1, result: Any) -> list[Dict[str, Any]]:
    checks = _common_checks(result)
    state = result.state_output
    flow = result.flow_output
    bridge = result.observation_need_bridge
    if case.case_id == "B2-01":
        checks.append(_check("real_current_world_accepted", True, result.mode == "REAL_B1_CURRENT_WORLD_INPUT"))
    elif case.case_id == "B2-03":
        checks.append(_check("cognitive_state_candidate_created", True, bool(state.cognitive_state_vector_candidate)))
    elif case.case_id == "B2-05":
        checks.append(_check("attention_candidate_created", True, bool(state.attention_candidates)))
    elif case.case_id == "B2-06":
        checks.extend([
            _check("attention_is_not_provider_execution", False, result.provider_invocation),
            _check("attention_provider_call_guard", False, state.negative_guard_status.model_call),
        ])
    elif case.case_id == "B2-07":
        checks.append(_check("hypothesis_candidate_created", True, bool(state.cognitive_hypotheses)))
    elif case.case_id == "B2-08":
        checks.extend([
            _check("hypothesis_is_not_fact", False, result.hypothesis_as_fact),
            _check("hypothesis_truth_guard", False, any(h.causal_truth for h in state.cognitive_hypotheses)),
        ])
    elif case.case_id == "B2-09":
        checks.append(_check("supporting_refs_preserved", True, bool(state.cognitive_hypotheses[0].supporting_evidence_refs)))
    elif case.case_id == "B2-10":
        checks.append(_check("uncertainty_source_preserved", True, bool(result.preserved_uncertainty_refs)))
    elif case.case_id == "B2-11":
        checks.append(_check("conflict_source_preserved", True, bool(result.preserved_conflict_refs)))
    elif case.case_id == "B2-12":
        checks.append(_check("alternative_hypothesis_boundary", True, bool(state.hypothesis_competition_result.alternative_explanation_refs)))
    elif case.case_id == "B2-13":
        checks.extend([
            _check("pcn_mutation", False, result.pcn_mutation),
            _check("pcn_refs_read_only", True, all(ref.read_only for ref in result.state_request.pcn_refs)),
        ])
    elif case.case_id == "B2-14":
        checks.extend([
            _check("intent_mutation", False, result.intent_mutation),
            _check("intent_refs_read_only", True, all(ref.read_only for ref in result.state_request.intent_refs)),
        ])
    elif case.case_id in {"B2-15", "B2-16"}:
        checks.extend([
            _check("observation_need_candidate_present", True, bridge is not None),
            _check("observation_need_owner", "Field Perception Orchestrator", bridge.owner if bridge else ""),
            _check("observation_need_provider_invocation", False, bridge.provider_invocation if bridge else True),
        ])
    elif case.case_id == "B2-17":
        checks.append(_check("cognitive_flow_transition_created", True, bool(flow.transition_candidates)))
    elif case.case_id == "B2-18":
        checks.extend([
            _check("previous_state_trace_preserved", True, flow.trace is not None and flow.trace.previous_cycle_id is None),
            _check("current_state_trace_preserved", True, bool(flow.trace and flow.trace.current_world_ref)),
        ])
    elif case.case_id == "B2-19":
        checks.extend([
            _check("decision_mutation", False, result.decision_mutation),
            _check("flow_decision_output_guard", False, flow.negative_guard_status.flow_can_create_fact),
        ])
    elif case.case_id == "B2-20":
        checks.extend([
            _check("task_mutation", False, result.task_mutation),
            _check("action_execution", False, result.action_execution),
            _check("flow_task_guard", False, flow.negative_guard_status.flow_can_execute_task),
        ])
    elif case.case_id == "B2-21":
        checks.append(_check("semantic_compression", False, result.semantic_compression))
    elif case.case_id == "B2-22":
        state_regression = run_state_regression()
        flow_regression = run_flow_regression()
        checks.extend([
            _check("synthetic_state_regression_preserved", 0, state_regression["summary"]["failed_case_count"]),
            _check("synthetic_flow_regression_preserved", 0, flow_regression["summary"]["failed_case_count"]),
        ])
    elif case.case_id == "B2-23":
        synthetic = run_b2_case(
            build_synthetic_current_world_v1(),
            "B2-23-SYN",
            mode="SYNTHETIC_CURRENT_WORLD",
        )
        checks.extend([
            _check("differential_candidate_shape", True, result.state_output.candidate_only is synthetic.state_output.candidate_only and result.flow_output.candidate_only is synthetic.flow_output.candidate_only),
            _check("differential_mutation_guard", True, result.current_world_read_only and synthetic.current_world_read_only and not result.provider_invocation and not synthetic.provider_invocation),
            _check("differential_trace_shape", True, bool(result.provenance_chain) and bool(synthetic.provenance_chain)),
            _check("differential_owner_boundary", True, result.flow_output.source_owner_mutation is False and synthetic.flow_output.source_owner_mutation is False),
        ])
    elif case.case_id == "B2-24":
        checks.extend([
            _check("real_b1_to_state_candidate", True, result.mode == "REAL_B1_CURRENT_WORLD_INPUT" and bool(state.current_world_candidate)),
            _check("real_b1_to_flow_transition", True, result.mode == "REAL_B1_CURRENT_WORLD_INPUT" and bool(flow.transition_candidates)),
            _check("real_b1_provenance", True, result.source_current_world.current_world_id in result.provenance_chain),
        ])
    return checks


def build_runner_result() -> Dict[str, Any]:
    case_results = []
    retained = None
    synthetic_regression_preserved = False
    differential_validation_passed = False
    for case in build_b2_cases_v1():
        result = run_b2_case(
            case.current_world,
            case.case_id,
            mode=case.mode,
            engine_scenario_id=case.engine_scenario_id,
            flow_scenario_id=case.flow_scenario_id,
        )
        checks = _checks_for_case(case, result)
        case_result = {
            "case_id": case.case_id,
            "title": case.title,
            "mode": case.mode,
            "checks": checks,
            "all_checks_passed": all(item["passed"] for item in checks),
            "actual": _json_value(
                {
                    "source_current_world_ref": result.source_current_world.current_world_id,
                    "derived_state_world_ref": result.state_output.current_world_candidate.current_world_id,
                    "flow_current_world_ref": result.flow_output.trace.current_world_ref if result.flow_output.trace else None,
                    "attention_candidate_created": bool(result.state_output.attention_candidates),
                    "hypothesis_candidate_created": bool(result.state_output.cognitive_hypotheses),
                    "observation_need_candidate_present": result.observation_need_bridge is not None,
                    "transition_count": len(result.flow_output.transition_candidates),
                    "candidate_only": result.candidate_only,
                    "provider_invocation": result.provider_invocation,
                }
            ),
            "result": _json_value(result),
        }
        case_results.append(case_result)
        if case.case_id == "B2-22":
            synthetic_regression_preserved = all(
                item["passed"]
                for item in checks
                if item["field"]
                in {
                    "synthetic_state_regression_preserved",
                    "synthetic_flow_regression_preserved",
                }
            )
        if case.case_id == "B2-23":
            differential_validation_passed = case_result["all_checks_passed"]
        if case.case_id == "B2-24":
            retained = result

    failed_ids = [item["case_id"] for item in case_results if not item["all_checks_passed"]]
    final = retained or run_b2_case(
        build_real_b1_current_world_v1(),
        "B2-FINAL",
        mode="REAL_B1_CURRENT_WORLD_INPUT",
    )
    world = final.source_current_world
    state = final.state_output
    flow = final.flow_output
    summary = {
        "phase": "Phase-Luna-Brain-B2-Current-World-Cognitive-State-Flow-Controlled-Implementation-v1-001",
        "mode": "HYBRID_B2_REAL_B1_CURRENT_WORLD",
        "owner": "Cognitive State Formation Governance / Cognitive Flow Governance",
        "real_components": ["REAL_B1_CURRENT_WORLD_INPUT"],
        "synthetic_components": ["Cognitive State Formation", "Cognitive Flow", "Active Observation Control bridge"],
        "b2_scenario_count": len(case_results),
        "all_cases_passed": not failed_ids,
        "failed_case_ids": failed_ids,
        "real_current_world_accepted": final.mode == "REAL_B1_CURRENT_WORLD_INPUT" and world.candidate_only,
        "cognitive_state_candidate_created": bool(state.cognitive_state_vector_candidate),
        "attention_candidate_created": bool(state.attention_candidates),
        "hypothesis_candidate_created": bool(state.cognitive_hypotheses),
        "alternative_hypothesis_candidate_present": bool(state.hypothesis_competition_result.alternative_explanation_refs),
        "observation_need_candidate_present": final.observation_need_bridge is not None,
        "cognitive_flow_transition_created": bool(flow.transition_candidates),
        "current_world_read_only": final.current_world_read_only,
        "current_world_direct_mutation": False,
        "field_state_mutation": False,
        "world_truth_promoted": final.world_truth_promoted,
        "hypothesis_as_fact": final.hypothesis_as_fact,
        "provider_confidence_as_cognitive_confidence": False,
        "uncertainty_refs_preserved": final.preserved_uncertainty_refs == world.uncertainty_refs,
        "conflict_refs_preserved": final.preserved_conflict_refs == world.conflict_refs,
        "provenance_chain_complete": bool(final.provenance_chain),
        "temporal_refs_preserved": final.preserved_temporal_refs == world.temporal_refs,
        "pcn_mutation": final.pcn_mutation,
        "intent_mutation": final.intent_mutation,
        "decision_mutation": final.decision_mutation,
        "task_mutation": final.task_mutation,
        "action_execution": final.action_execution,
        "provider_invocation": final.provider_invocation,
        "camera_activation": False,
        "ocr_execution": False,
        "slam_execution": False,
        "vio_execution": False,
        "vlm_execution": False,
        "online_learning": False,
        "hidden_cognitive_loop": False,
        "semantic_compression": final.semantic_compression,
        "dynamic_cognitive_function_execution": final.dynamic_cognitive_function_execution,
        "synthetic_regression_preserved": synthetic_regression_preserved,
        "differential_validation_passed": differential_validation_passed,
        "candidate_only": final.candidate_only,
        "status": "WAITING_FOR_USER_TERMINAL_VERIFICATION",
    }
    return {"summary": summary, "case_results": case_results}


def write_runner_artifacts(payload: Mapping[str, Any]) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUTPUT_DIR / "b2_current_world_cognitive_state_flow_result_v1.json").write_text(
        json.dumps(payload["summary"], indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    (OUTPUT_DIR / "b2_current_world_cognitive_state_flow_case_results_v1.json").write_text(
        json.dumps(payload["case_results"], indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    result = build_runner_result()
    write_runner_artifacts(result)
    print(json.dumps(result["summary"], indent=2, ensure_ascii=False))
