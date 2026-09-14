from __future__ import annotations

import argparse
import dataclasses
import json
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional


def repo_root_from(path: Path) -> Path:
    for candidate in (path.resolve(), *path.resolve().parents):
        if all((candidate / marker).exists() for marker in ("capabilities", "docs", "README.md")):
            return candidate
    raise RuntimeError("repository root sentinel not found")


ROOT = repo_root_from(Path(__file__))
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from capabilities.midplatform.core.a_route_orchestration.integration.a_route_product_loop_integration_engine_v1 import (  # noqa: E402
    ARouteProductLoopIntegrationEngineV1,
)
from capabilities.midplatform.core.a_route_orchestration.integration.run_a_route_runtime_product_loop_controlled_integration_v1 import (  # noqa: E402
    _check_case as _check_frozen_s0_case,
)
from capabilities.midplatform.core.a_route_orchestration.integration.a_route_product_loop_integration_fixture_v1 import (  # noqa: E402
    build_fixture_cases,
)
from capabilities.midplatform.core.a_route_orchestration.integration.a_route_product_loop_integration_core_types_v1 import (  # noqa: E402
    ProductLoopInputV1,
)
from capabilities.midplatform.core.a_route_orchestration.integration.a_route_real_user_input_adapter_v1 import (  # noqa: E402
    adapt_user_input,
)
from capabilities.midplatform.core.a_route_orchestration.integration.a_route_real_user_input_adapter_types_v1 import (  # noqa: E402
    RealUserInputTraceV1,
)
from capabilities.midplatform.core.a_route_orchestration.integration.a_route_real_user_input_fixture_v1 import (  # noqa: E402
    S1FixtureCaseV1,
    build_s1_fixture_cases,
)


OUT_DIR = ROOT / "_eval_out/a_route_s1_real_user_input_controlled_replacement_v1"
S0_GUARDS = {
    "provider_invocation": False,
    "model_call": False,
    "camera_execution": False,
    "ocr_execution": False,
    "slam_execution": False,
    "audio_execution": False,
    "real_runtime_execution": False,
    "database_write": False,
    "vector_store_write": False,
    "embedding_execution": False,
    "scheduler_execution": False,
    "device_control": False,
    "field_state_direct_mutation": False,
    "context_direct_mutation": False,
    "intent_mutation": False,
    "decision_mutation": False,
    "memory_mutation": False,
    "learning_execution": False,
    "self_mutation": False,
    "personality_mutation": False,
    "emotion_engine_execution": False,
    "b_route_execution": False,
    "semantic_compression_execution": False,
    "cross_user_transfer": False,
    "real_side_effect": False,
}


def jsonable(value: Any) -> Any:
    if dataclasses.is_dataclass(value):
        return {key: jsonable(item) for key, item in dataclasses.asdict(value).items()}
    if isinstance(value, dict):
        return {key: jsonable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [jsonable(item) for item in value]
    return value


def _check(name: str, actual: Any, expected: Any) -> Dict[str, Any]:
    return {"check": name, "expected": expected, "actual": actual, "passed": actual == expected}


def _s0_case_result(engine: ARouteProductLoopIntegrationEngineV1, case: Any) -> Dict[str, Any]:
    """Use the frozen S0 Runner's canonical check implementation unchanged."""

    return _check_frozen_s0_case(engine, case)


def _synthetic_equivalent(case_id: str, source_ref: str) -> ProductLoopInputV1:
    return ProductLoopInputV1(
        scenario_id=case_id,
        title="synthetic equivalent input",
        ingress_kind="USER_INPUT",
        source_ref=source_ref,
        requires_action=False,
    )


def _differential_checks(adapter_result: Any, synthetic_result: Any, real_result: Any) -> List[Dict[str, Any]]:
    real_stages = tuple(stage.stage_id for stage in real_result.stages)
    synthetic_stages = tuple(stage.stage_id for stage in synthetic_result.stages)
    real_guards = dict(real_result.guards)
    synthetic_guards = dict(synthetic_result.guards)
    real_trace_contract = (tuple(real_result.trace.stage_trace_refs), tuple(real_result.trace.handoff_trace_refs), real_result.trace.provenance_grants_authority)
    synthetic_trace_contract = (tuple(synthetic_result.trace.stage_trace_refs), tuple(synthetic_result.trace.handoff_trace_refs), synthetic_result.trace.provenance_grants_authority)
    return [
        _check("contract_outputs", (real_result.state, real_result.output.output_kind if real_result.output else "", real_result.feedback.route if real_result.feedback else ""), (synthetic_result.state, synthetic_result.output.output_kind if synthetic_result.output else "", synthetic_result.feedback.route if synthetic_result.feedback else "")),
        _check("trace_provenance", real_trace_contract, synthetic_trace_contract),
        _check("state_transitions", real_stages, synthetic_stages),
        _check("negative_guards", real_guards, synthetic_guards),
        _check("unrelated_module_behavior", real_result.candidate_only and real_result.synthetic_only, True),
        _check("adapter_contract", adapter_result.accepted and adapter_result.record.truth_declared is False and adapter_result.record.semantic_interpretation_performed is False, True),
    ]


def _s1_case_result(engine: ARouteProductLoopIntegrationEngineV1, case: S1FixtureCaseV1) -> Dict[str, Any]:
    first = adapt_user_input(case.input_text, ingress_kind=case.ingress_kind, sensitivity=case.sensitivity, correction_ref=case.correction_ref, cycle_ref=case.case_id)
    if case.duplicate_probe and first.accepted:
        duplicate = adapt_user_input(case.input_text, ingress_kind=case.ingress_kind, sensitivity=case.sensitivity, correction_ref=case.correction_ref, cycle_ref=case.case_id, seen_input_ids=(first.record.input_id,))
        checks = [
            _check("first_accepts", first.accepted, True),
            _check("duplicate_rejected", duplicate.accepted, False),
            _check("duplicate_flag", duplicate.duplicate, True),
            _check("duplicate_code", duplicate.rejection_code, "DUPLICATE_INPUT"),
        ]
        return {"scenario_id": case.case_id, "title": case.title, "checks": checks, "all_checks_passed": all(item["passed"] for item in checks), "actual": {"first": jsonable(first), "duplicate": jsonable(duplicate)}}

    checks = [
        _check("accepted", first.accepted, case.expected_accepted),
        _check("rejection_code", first.rejection_code, case.expected_rejection_code),
    ]
    if case.expected_accepted:
        checks.extend([
            _check("normalized_content", first.record.normalized_content, case.expected_normalized),
            _check("ingress_kind", first.record.ingress_kind, case.ingress_kind),
            _check("sensitivity", first.record.sensitivity, case.sensitivity),
            _check("correction_ref", first.record.correction_ref, case.correction_ref),
            _check("candidate_only", first.record.candidate_only, True),
            _check("truth_declared", first.record.truth_declared, False),
            _check("direct_field_mutation", first.record.direct_field_mutation, False),
            _check("direct_intent_ref", first.record.direct_intent_ref, ""),
            _check("direct_task_ref", first.record.direct_task_ref, ""),
        ])
        loop_result = engine.run_case(first.product_loop_input)
        checks.extend([
            _check("downstream_state", loop_result.state, "COMPLETED"),
            _check("downstream_output", loop_result.output.output_kind if loop_result.output else "", "RESPONSE"),
            _check("downstream_guards", all(loop_result.guards.get(key) is False for key in S0_GUARDS), True),
        ])
        if case.ingress_kind == "USER_CORRECTION":
            checks.append(_check("correction_lineage", tuple(loop_result.trace.correction_lineage), (case.correction_ref,)))
        trace = _trace_for(first, loop_result)
        if case.differential_probe:
            synthetic_input = _synthetic_equivalent(case.case_id, f"synthetic:{case.case_id}")
            synthetic_result = engine.run_case(synthetic_input)
            checks.extend(_differential_checks(first, synthetic_result, loop_result))
            actual = {"adapter": jsonable(first), "loop": jsonable(loop_result), "synthetic_equivalent": jsonable(synthetic_result), "differential": _differential_checks(first, synthetic_result, loop_result), "trace": trace}
        elif case.case_id == "S1-11":
            adapter_trace = trace["adapter_trace"]
            checks.extend([
                _check("trace_input_id", adapter_trace["input_id"], first.record.input_id),
                _check("trace_raw_input_ref", adapter_trace["raw_input_ref"], first.record.raw_input_ref),
                _check("trace_authority", adapter_trace["provenance_grants_authority"], False),
            ])
            actual = {"adapter": jsonable(first), "loop": jsonable(loop_result), "trace": trace}
        else:
            actual = {"adapter": jsonable(first), "loop": jsonable(loop_result), "trace": trace}
    else:
        actual = {"adapter": jsonable(first)}
    return {"scenario_id": case.case_id, "title": case.title, "checks": checks, "all_checks_passed": all(item["passed"] for item in checks), "actual": actual}


def _trace_for(adapter_result: Any, loop_result: Any) -> Dict[str, Any]:
    record = adapter_result.record
    product_ref = adapter_result.product_loop_input.source_ref if adapter_result.product_loop_input else ""
    trace = RealUserInputTraceV1(
        input_id=record.input_id,
        product_loop_input_ref=product_ref,
        adapter_record_ref=record.input_id,
        raw_input_ref=record.raw_input_ref,
        trace_ref=record.trace_ref,
        provenance_refs=record.provenance_refs,
        reverse_lookup=(("product_loop_input", (record.input_id,)), (record.input_id, (record.raw_input_ref, record.trace_ref))),
    )
    return {"adapter_trace": jsonable(trace), "product_loop_trace": jsonable(loop_result.trace) if loop_result else None}


def run(*, input_text: Optional[str] = None, ingress_kind: str = "USER_INPUT") -> Dict[str, Any]:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    engine = ARouteProductLoopIntegrationEngineV1()
    s0_results = [_s0_case_result(engine, case) for case in build_fixture_cases()]
    s1_results = [_s1_case_result(engine, case) for case in build_s1_fixture_cases()]
    traces: List[Dict[str, Any]] = [item["actual"]["trace"] for item in s1_results if "trace" in item.get("actual", {})]
    real_case = None
    mode = "SYNTHETIC_REGRESSION"
    if input_text is not None:
        mode = "REAL_USER_INPUT_CONTROLLED"
        adapter_result = adapt_user_input(input_text, ingress_kind=ingress_kind, session_ref="cli:s1", cycle_ref="real-user-input")
        loop_result = engine.run_case(adapter_result.product_loop_input) if adapter_result.accepted else None
        real_case = {"scenario_id": "S1-REAL", "title": "user-provided real input", "checks": [{"check": "accepted", "expected": True, "actual": adapter_result.accepted, "passed": adapter_result.accepted}], "all_checks_passed": adapter_result.accepted, "actual": {"adapter": jsonable(adapter_result), "loop": jsonable(loop_result) if loop_result else None}}
        traces.append(_trace_for(adapter_result, loop_result))
    all_case_results = s1_results + ([real_case] if real_case else [])
    summary = {
        "mode": mode,
        "overall_loop_mode": "HYBRID_S1" if input_text is not None else "SYNTHETIC_REGRESSION",
        "real_components": ["USER_INPUT"] if input_text is not None else [],
        "synthetic_components": ["all_remaining_s0_components"],
        "scenario_count": len(all_case_results),
        "s1_scenario_count": len(s1_results),
        "s0_scenario_count": len(s0_results),
        "s0_all_cases_passed": all(item["all_checks_passed"] for item in s0_results),
        "s0_failed_case_ids": [item["scenario_id"] for item in s0_results if not item["all_checks_passed"]],
        "all_cases_passed": all(item["all_checks_passed"] for item in all_case_results) and all(item["all_checks_passed"] for item in s0_results),
        "failed_case_ids": [item["scenario_id"] for item in all_case_results if not item["all_checks_passed"]] + [item["scenario_id"] for item in s0_results if not item["all_checks_passed"]],
        "provider_invocation": False,
        "model_call": False,
        "real_runtime_execution": False,
        "database_write": False,
        "device_control": False,
        "source_owner_mutation": False,
        "synthetic_only_downstream": True,
        "controlled_integration_only": True,
    }
    (OUT_DIR / "a_route_s1_real_user_input_result_v1.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    (OUT_DIR / "a_route_s1_real_user_input_case_results_v1.json").write_text(json.dumps(all_case_results, ensure_ascii=False, indent=2), encoding="utf-8")
    (OUT_DIR / "a_route_s1_s0_regression_case_results_v1.json").write_text(json.dumps(s0_results, ensure_ascii=False, indent=2), encoding="utf-8")
    (OUT_DIR / "a_route_s1_real_user_input_trace_v1.json").write_text(json.dumps(traces, ensure_ascii=False, indent=2), encoding="utf-8")
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description="S1 controlled real user input replacement")
    parser.add_argument("--input", dest="input_text", default=None, help="user-provided text; omitted runs S1 plus S0 regression")
    parser.add_argument("--ingress-type", default="USER_INPUT", choices=("USER_INPUT", "USER_CORRECTION"))
    args = parser.parse_args()
    summary = run(input_text=args.input_text, ingress_kind=args.ingress_type)
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if summary["all_cases_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
