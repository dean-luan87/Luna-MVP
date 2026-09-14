from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List


def _resolve_repo_root() -> Path:
    current = Path(__file__).resolve()
    for candidate in current.parents:
        if (candidate / "capabilities").is_dir() and (candidate / "docs").is_dir():
            return candidate
    raise RuntimeError("Unable to locate repository root sentinel capabilities/ + docs/")


REPO_ROOT = _resolve_repo_root()
if __package__ in {None, ""} and str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.midplatform.core.a_route_orchestration.a_route_orchestration_engine_v1 import (  # noqa: E402
    ARouteOrchestrationEngineV1,
)
from capabilities.midplatform.core.a_route_orchestration.a_route_orchestration_fixture_v1 import (  # noqa: E402
    get_a_route_orchestration_fixtures_v1,
)
from capabilities.midplatform.core.a_route_orchestration.a_route_orchestration_ownership_guard_v1 import (  # noqa: E402
    CANONICAL_OWNER,
)
from capabilities.midplatform.core.a_route_orchestration.a_route_orchestration_static_validators_v1 import (  # noqa: E402
    validate_handoff,
    validate_negative_guards,
    validate_stage_result,
    validate_trace,
)

OUTPUT_DIR = REPO_ROOT / "_eval_out/a_route_orchestration_controlled_integration_v1"


def build_case_result(case: Any, output: Any) -> Dict[str, Any]:
    error_codes = [error.code for error in output.errors]
    execution_handoff = next((item for item in output.handoffs if item.handoff_id.endswith(":execution")), None)
    checks = {
        "lifecycle_expected": output.lifecycle_state == case.expected_lifecycle_state,
        "control_expected": output.control_state == case.expected_control_state,
        "error_expected": (case.expected_error_code in error_codes) if case.expected_error_code else not error_codes,
        "runtime_handoff_status_expected": (execution_handoff is not None and execution_handoff.status == case.expected_runtime_handoff_status) or (execution_handoff is None and case.expected_runtime_handoff_status in {"BLOCKED", "DEFERRED"}),
        "next_cycle_expected": bool(output.next_cycle_ingress_refs) == case.expected_next_cycle,
        "stage_result_contract": all(validate_stage_result(stage) for stage in output.stage_results),
        "handoff_status_contract": all(validate_handoff(handoff) for handoff in output.handoffs),
        "trace_continuity": validate_trace(output.trace, output.stage_results),
        "provenance_preserved": bool(output.trace.provenance_refs) and all(stage.provenance_refs for stage in output.stage_results),
        "negative_guards": validate_negative_guards(output.negative_guards),
        "candidate_only": output.candidate_only and output.synthetic_only,
        "narrow_owner": CANONICAL_OWNER == "A Route Orchestration Governance" and all(stage.producer_owner != CANONICAL_OWNER or stage.consumer_owner != CANONICAL_OWNER for stage in output.stage_results),
        "deferred_ref_expected": (case.expected_deferred_ref in output.deferred_refs) if case.expected_deferred_ref else True,
        "no_runtime_side_effect": output.negative_guards.real_side_effect is False,
    }
    return {
        "case_id": case.case_id,
        "title": case.title,
        "lifecycle_state": output.lifecycle_state,
        "control_state": output.control_state,
        "error_codes": error_codes,
        "handoff_statuses": {item.handoff_id: item.status for item in output.handoffs},
        "next_cycle_ingress_refs": list(output.next_cycle_ingress_refs),
        "deferred_refs": list(output.deferred_refs),
        "checks": checks,
        "all_checks_passed": all(checks.values()),
    }


def build_runner_result() -> Dict[str, Any]:
    engine = ARouteOrchestrationEngineV1()
    cases: List[Dict[str, Any]] = []
    traces: List[Dict[str, Any]] = []
    for case in get_a_route_orchestration_fixtures_v1():
        output = engine.run_case(case.request)
        cases.append(build_case_result(case, output))
        traces.append({
            "case_id": case.case_id,
            "root_cycle_trace_id": output.trace.root_cycle_trace_id,
            "cycle_id": output.trace.cycle_id,
            "previous_cycle_id": output.trace.previous_cycle_id,
            "source_owner_trace_refs": list(output.trace.source_owner_trace_refs),
            "stage_trace_refs": list(output.trace.stage_trace_refs),
            "handoff_trace_refs": list(output.trace.handoff_trace_refs),
            "provenance_refs": list(output.trace.provenance_refs),
            "error_refs": list(output.trace.error_refs),
            "reconsideration_lineage": list(output.trace.reconsideration_lineage),
            "reverse_lookup_path": list(output.trace.reverse_lookup_path),
            "authority_granted": output.trace.authority_granted,
        })
    passed = sum(1 for item in cases if item["all_checks_passed"])
    summary = {
        "phase": "Phase-Luna-A-Route-Orchestration-Backbone-Controlled-Integration-v1-001",
        "canonical_owner": CANONICAL_OWNER,
        "scenario_count": len(cases),
        "passed_case_count": passed,
        "failed_case_count": len(cases) - passed,
        "runtime_execution": False,
        "database_write": False,
        "model_call": False,
        "device_control": False,
        "source_owner_mutation": False,
        "emotion_engine_execution": False,
        "b_route_execution": False,
        "semantic_compression_execution": False,
        "synthetic_only": True,
        "candidate_only": True,
        "status": "A_ROUTE_ORCHESTRATION_CONTROLLED_INTEGRATION_RESULT_CANDIDATE_READY",
    }
    return {"summary": summary, "case_results": cases, "trace": {"trace_id": "a-route-orchestration-trace-v1", "case_traces": traces, "candidate_only": True}}


def write_outputs(payload: Dict[str, Any]) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUTPUT_DIR / "a_route_orchestration_result_v1.json").write_text(json.dumps(payload["summary"], indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (OUTPUT_DIR / "a_route_orchestration_case_results_v1.json").write_text(json.dumps(payload["case_results"], indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (OUTPUT_DIR / "a_route_orchestration_trace_v1.json").write_text(json.dumps(payload["trace"], indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> int:
    write_outputs(build_runner_result())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
