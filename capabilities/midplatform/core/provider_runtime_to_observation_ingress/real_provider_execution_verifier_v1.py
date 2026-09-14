"""Read-only verifier for the real provider execution integration."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict


DEFAULT_SUMMARY = Path("_eval_out/real_provider_execution_integration_v1/runner_summary_v1.json")


def verify(summary: Dict[str, Any]) -> Dict[str, Any]:
    provider_result = summary.get("provider_runtime_result") or {}
    provider_native = summary.get("provider_native_result") or {}
    forbidden = summary.get("forbidden_behaviors") or {}
    checks = {
        "live_runtime_required": summary.get("execution_mode") == "LIVE_RUNTIME",
        "real_execution_attempted": summary.get("provider_real_execution_attempted") is True,
        "real_execution_verified": summary.get("provider_real_execution_verified") is True,
        "provider_invoked_from_runtime": summary.get("provider_invoked") is True and provider_native.get("invocation_performed") is True,
        "model_invocation_derived": summary.get("model_invoked") is True and provider_result.get("model_invoked") is True,
        "recorded_result_not_used": summary.get("recorded_provider_result_used") is False,
        "provider_request_result_identity": bool(summary.get("provider_request_ref") and provider_result.get("provider_request_ref") == summary.get("provider_request_ref") and provider_result.get("execution_instance_ref")),
        "provider_provenance_retained": bool(summary.get("provenance_refs") and set(summary.get("provenance_refs", ())).issubset(set(provider_result.get("provenance_refs", ())))),
        "provider_result_success_or_empty": summary.get("provider_status") in {"SUCCESS", "EMPTY_SUCCESS"},
        "runtime_observation_present": bool(summary.get("runtime_observation_ref")),
        "gateway_admitted": bool(summary.get("gateway_admission_ref")),
        "evidence_or_empty_success": bool(summary.get("evidence_refs")) or summary.get("provider_status") == "EMPTY_SUCCESS",
        "cognition_reached": bool(summary.get("a_route_execution_ref") and summary.get("sufficiency_ref")),
        "provider_not_truth": provider_result.get("truth_declared") is False and not provider_native.get("semantic_interpretation", False),
        "no_downstream_execution": all(forbidden.get(name) is False for name in ("decision_execution", "task_execution", "action_execution", "runtime_executor_invocation", "device_control", "external_side_effect")),
        "no_illegal_mutation": all(forbidden.get(name) is False for name in ("field_mutation", "world_truth_declared")),
        "no_validation_errors": summary.get("validation_errors") == [],
    }
    failed = [key for key, passed in checks.items() if not passed]
    return {
        "phase": summary.get("phase"),
        "all_checks_passed": not failed,
        "failed_checks": failed,
        "operational_result": "PASS" if not failed else "FAIL",
        "provider_real_execution_verified": summary.get("provider_real_execution_verified"),
        "final_decision": "GO" if not failed else "NOT_GO",
        "checks": checks,
    }


def main() -> int:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_SUMMARY
    result = verify(json.loads(path.read_text(encoding="utf-8")))
    print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True))
    return 0 if result["all_checks_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
