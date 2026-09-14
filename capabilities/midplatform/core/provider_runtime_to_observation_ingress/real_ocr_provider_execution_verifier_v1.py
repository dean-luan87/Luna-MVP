"""Read-only verifier for the real OCR provider execution integration."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict


DEFAULT_SUMMARY = Path("_eval_out/real_ocr_provider_execution_integration_v1/runner_summary_v1.json")


def verify(summary: Dict[str, Any]) -> Dict[str, Any]:
    request = summary.get("provider_runtime_request") or {}
    result = summary.get("provider_runtime_result") or {}
    native = summary.get("provider_native_result") or {}
    payload = ((summary.get("details") or {}).get("runtime_observation") or {}).get("output_candidate") or {}
    gateway = (summary.get("details") or {}).get("gateway") or {}
    evidence = (gateway.get("evidence") or []) if isinstance(gateway, dict) else []
    forbidden = summary.get("forbidden_behaviors") or {}
    status = summary.get("provider_status")
    empty = status == "EMPTY_SUCCESS"
    checks = {
        "live_runtime_required": summary.get("execution_mode") == "LIVE_RUNTIME",
        "real_execution_attempted": summary.get("provider_real_execution_attempted") is True,
        "real_execution_verified": summary.get("provider_real_execution_verified") is True,
        "provider_invoked_from_runtime": summary.get("provider_invoked") is True and native.get("provider_invoked") is True,
        "model_invocation_derived": summary.get("model_invoked") is True and result.get("model_invoked") is True,
        "recorded_result_not_used": summary.get("recorded_provider_result_used") is False,
        "canonical_ocr_identity": (
            summary.get("selected_provider") == "ocr_v1"
            and summary.get("selected_provider_ref") == "provider:ocr_v1"
            and summary.get("provider_ref") == "provider:ocr_v1"
            and summary.get("model_ref") == "model:ocr_v1"
            and summary.get("capability_ref") == "text_recognition"
            and request.get("provider_ref") == "provider:ocr_v1"
            and request.get("model_ref") == "model:ocr_v1"
        ),
        "provider_request_result_identity": (
            bool(summary.get("provider_request_ref"))
            and result.get("provider_request_ref") == summary.get("provider_request_ref")
            and result.get("execution_instance_ref") == summary.get("execution_instance_ref")
            and result.get("provider_ref") == request.get("provider_ref")
            and result.get("capability_ref") == request.get("capability_ref")
        ),
        "provider_provenance_retained": bool(
            summary.get("provenance_refs")
            and set(summary.get("provenance_refs", ())).issubset(set(result.get("provenance_refs", ())))
        ),
        "provider_result_success_or_empty": status in {"SUCCESS", "EMPTY_SUCCESS"},
        "runtime_observation_present": bool(summary.get("runtime_observation_ref")),
        "gateway_admitted": bool(summary.get("gateway_admission_ref")) and gateway.get("admission_state") == "ADMITTED_OBSERVATION",
        "text_evidence_or_valid_empty_success": (
            bool(summary.get("evidence_refs"))
            and (
                (empty and any(item.get("evidence_type") == "ocr_empty_success" for item in evidence if isinstance(item, dict)))
                or (not empty and any(item.get("evidence_type") == "ocr_text_evidence" for item in evidence if isinstance(item, dict)))
            )
        ),
        "empty_success_semantics": (
            (not empty)
            or (
                summary.get("empty_result") is True
                and result.get("empty_result") is True
                and payload.get("empty_result") is True
                and payload.get("text_candidates") == []
            )
        ),
        "ocr_candidate_only": result.get("candidate_only") is True and result.get("truth_declared") is False and payload.get("candidate_only") is True,
        "a_route_reached": bool(summary.get("a_route_execution_ref")),
        "cognitive_state_reached": summary.get("cognitive_state_reached") is True,
        "sufficiency_or_gap_stop_structurally_present": bool(summary.get("sufficiency_ref")) and bool(summary.get("stop_ref") or summary.get("information_gap_ref")),
        "no_downstream_execution": all(forbidden.get(name) is False for name in ("decision_execution", "task_execution", "action_execution", "runtime_executor_invocation", "device_control")),
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
        "checks": checks,
    }


def main() -> int:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_SUMMARY
    result = verify(json.loads(path.read_text(encoding="utf-8")))
    print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True))
    return 0 if result["all_checks_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
