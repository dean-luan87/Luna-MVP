"""Read-only verifier for provider-result to observation ingress."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict


DEFAULT_SUMMARY = Path("_eval_out/provider_runtime_to_observation_ingress_v1/runner_summary_v1.json")


def _case_checks(case: Dict[str, Any]) -> bool:
    return bool(case.get("all_checks_passed")) and all(item.get("passed") is True for item in case.get("checks", []))


def verify(summary: Dict[str, Any]) -> Dict[str, Any]:
    positives = summary.get("positive_cases", [])
    negatives = summary.get("negative_cases", [])
    reobservation = summary.get("reobservation_case", {})
    checks = {
        "positive_case_count": summary.get("positive_case_count") == 3 and len(positives) == 3,
        "negative_case_count": summary.get("negative_case_count") == 3 and len(negatives) == 3,
        "live_runtime_mode": summary.get("execution_mode") == "LIVE_RUNTIME",
        "provider_contract_verified": summary.get("provider_runtime_contract_verified") is True,
        "provider_real_execution_not_claimed": summary.get("provider_real_execution_verified") is False,
        "no_provider_or_model_invocation": summary.get("provider_invocation") is False and summary.get("model_invocation") is False,
        "no_live_observation_execution": summary.get("live_observation_execution") is False,
        "no_downstream_execution": all(summary.get(name) is False for name in ("decision_execution", "task_execution", "action_execution", "runtime_executor_invocation", "device_control")),
        "no_illegal_mutation_or_truth": summary.get("field_mutation") is False and summary.get("world_truth_declared") is False,
        "positive_cases_valid": all(_case_checks(case) for case in positives),
        "reobservation_request_candidate": _case_checks(reobservation) and bool(reobservation.get("next_cycle_ingress_ref") and reobservation.get("reobservation_request_ref")) and any(item.get("check_id") == "reobservation_provider_request_candidate" and item.get("passed") is True for item in reobservation.get("checks", [])),
        "negative_cases_valid": all(bool(case.get("all_checks_passed")) and all(item.get("passed") is True for item in case.get("checks", [])) for case in negatives),
        "unavailable_no_fake_evidence": bool(negatives and negatives[0].get("runtime_observation_ref") is None and negatives[0].get("evidence_refs") == []),
        "unresolved_capability_no_provider_request": bool(negatives and negatives[-1].get("provider_request_ref") is None),
    }
    failed = [key for key, value in checks.items() if not value]
    return {
        "phase": summary.get("phase"),
        "all_checks_passed": not failed,
        "failed_checks": failed,
        "operational_result": "PASS" if not failed else "FAIL",
        "provider_runtime_contract_verified": summary.get("provider_runtime_contract_verified"),
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
