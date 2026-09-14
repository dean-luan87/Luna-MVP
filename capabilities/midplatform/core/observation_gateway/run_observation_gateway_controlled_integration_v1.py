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

from capabilities.midplatform.core.observation_gateway.observation_gateway_engine_v1 import (  # noqa: E402
    ObservationGatewayEngineV1,
)
from capabilities.midplatform.core.observation_gateway.observation_gateway_fixture_v1 import (  # noqa: E402
    get_observation_gateway_fixtures_v1,
)
from capabilities.midplatform.core.observation_gateway.observation_gateway_ownership_guard_v1 import (  # noqa: E402
    CANONICAL_OWNER,
)
from capabilities.midplatform.core.observation_gateway.observation_gateway_static_validators_v1 import (  # noqa: E402
    validate_evidence,
    validate_ingress,
    validate_negative_guards,
    validate_observation,
    validate_trace,
)

OUTPUT_DIR = REPO_ROOT / "_eval_out/a_route_perception_observation_gateway_controlled_integration_v1"


def build_case_result(case: Any, output: Any) -> Dict[str, Any]:
    error_codes = [error.code for error in output.errors]
    checks = {
        "admission_state_expected": output.admission_state == case.expected_admission_state,
        "route_status_expected": output.route_status == case.expected_route_status,
        "error_expected": (case.expected_error_code in error_codes) if case.expected_error_code else not error_codes,
        "route_ready_expected": bool(output.route_refs) == case.expected_route_ready,
        "evidence_count_expected": len(output.evidence) == case.expected_evidence_count,
        "ingress_contract": output.ingress is None or validate_ingress(output.ingress),
        "evidence_contract": all(validate_evidence(item) for item in output.evidence),
        "observation_contract": output.observation is None or validate_observation(output.observation),
        "candidate_non_truth": output.observation is None or (output.observation.candidate_only and output.observation.truth_declared is False),
        "multi_evidence_preserved": len(output.evidence) == case.expected_evidence_count,
        "correction_lineage": bool(output.trace.correction_lineage) == case.expected_correction_lineage,
        "contradiction_lineage": bool(output.trace.contradiction_lineage) == case.expected_contradiction_lineage,
        "trace_provenance": validate_trace(output.trace),
        "negative_guards": validate_negative_guards(output.negative_guards),
        "deferred_ref_expected": (case.expected_deferred_ref in output.deferred_refs) if case.expected_deferred_ref else True,
        "no_downstream_mutation": all(value is False for name, value in vars(output.negative_guards).items() if name not in {"synthetic_only", "controlled_integration_only"}),
    }
    return {
        "case_id": case.case_id,
        "title": case.title,
        "admission_state": output.admission_state,
        "route_status": output.route_status,
        "route_refs": list(output.route_refs),
        "error_codes": error_codes,
        "evidence_ids": [item.evidence_id for item in output.evidence],
        "observation_id": output.observation.observation_id if output.observation else "",
        "routing_targets": list(output.observation.routing_targets) if output.observation else [],
        "checks": checks,
        "all_checks_passed": all(checks.values()),
    }


def build_runner_result() -> Dict[str, Any]:
    engine = ObservationGatewayEngineV1()
    case_results: List[Dict[str, Any]] = []
    traces: List[Dict[str, Any]] = []
    for case in get_observation_gateway_fixtures_v1():
        output = engine.run_case(case.request)
        case_results.append(build_case_result(case, output))
        traces.append({
            "case_id": case.case_id,
            "root_trace_id": output.trace.root_trace_id,
            "a_route_ingress_ref": output.trace.a_route_ingress_ref,
            "observation_trace_ref": output.trace.observation_trace_ref,
            "evidence_trace_refs": list(output.trace.evidence_trace_refs),
            "provider_trace_refs": list(output.trace.provider_trace_refs),
            "source_input_refs": list(output.trace.source_input_refs),
            "provenance_refs": list(output.trace.provenance_refs),
            "correction_lineage": list(output.trace.correction_lineage),
            "contradiction_lineage": list(output.trace.contradiction_lineage),
            "temporal_lineage": list(output.trace.temporal_lineage),
            "reverse_lookup_path": list(output.trace.reverse_lookup_path),
            "authority_granted": output.trace.authority_granted,
        })
    passed = sum(1 for item in case_results if item["all_checks_passed"])
    summary = {
        "phase": "Phase-Luna-A-Route-Perception-Observation-Gateway-Controlled-Integration-v1-001",
        "canonical_owner": CANONICAL_OWNER,
        "scenario_count": len(case_results),
        "passed_case_count": passed,
        "failed_case_count": len(case_results) - passed,
        "runtime_execution": False,
        "database_write": False,
        "vector_store_write": False,
        "embedding_execution": False,
        "model_call": False,
        "scheduler_execution": False,
        "device_control": False,
        "real_side_effect": False,
        "source_owner_mutation": False,
        "observation_is_world_truth": False,
        "ocr_evidence_is_fact": False,
        "visual_detection_is_fact": False,
        "slam_geometry_is_semantic_truth": False,
        "emotion_engine_execution": False,
        "b_route_execution": False,
        "semantic_compression_execution": False,
        "synthetic_only": True,
        "controlled_integration_only": True,
        "status": "OBSERVATION_GATEWAY_CONTROLLED_INTEGRATION_RESULT_CANDIDATE_READY",
    }
    return {"summary": summary, "case_results": case_results, "trace": {"trace_id": "observation-gateway-trace-v1", "case_traces": traces, "candidate_only": True}}


def write_outputs(payload: Dict[str, Any]) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUTPUT_DIR / "observation_gateway_result_v1.json").write_text(json.dumps(payload["summary"], indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (OUTPUT_DIR / "observation_gateway_case_results_v1.json").write_text(json.dumps(payload["case_results"], indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (OUTPUT_DIR / "observation_gateway_trace_v1.json").write_text(json.dumps(payload["trace"], indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> int:
    write_outputs(build_runner_result())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
