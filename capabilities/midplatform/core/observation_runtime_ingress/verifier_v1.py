"""Read-only verifier for the real observation ingress runner output."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, Iterable


DEFAULT_SUMMARY = Path("_eval_out/real_observation_runtime_ingress_v1/runner_summary_v1.json")


def _checks(items: Iterable[Dict[str, Any]]) -> Dict[str, bool]:
    return {item["check_id"]: item.get("passed") is True for item in items}


def verify(summary: Dict[str, Any]) -> Dict[str, Any]:
    positives = [*summary.get("positive_cases", []), summary.get("missing_information_case", {})]
    negatives = summary.get("negative_cases", [])
    checks: Dict[str, bool] = {
        "positive_case_count": summary.get("positive_case_count") == 3,
        "negative_case_count": summary.get("negative_case_count") == 2,
        "live_runtime_mode": summary.get("execution_mode") == "LIVE_RUNTIME",
        "no_provider_or_model_invocation": summary.get("provider_invocation") is False and summary.get("model_invocation") is False,
        "no_downstream_execution": all(summary.get(name) is False for name in ("decision_execution", "task_execution", "action_execution", "runtime_executor_invocation")),
        "no_illegal_mutation_or_truth": all(summary.get(name) is False for name in ("field_mutation", "world_truth_declared")),
    }
    for case in positives:
        checks[f"positive:{case.get('case_id')}:runner_checks"] = bool(case.get("all_checks_passed")) and all(_checks(case.get("checks", [])).values())
        checks[f"positive:{case.get('case_id')}:trace_to_cognition"] = bool(case.get("gateway_admission_ref") and case.get("runtime_observation_ref") and case.get("a_route_execution_ref") and case.get("current_world_ref") and case.get("hypothesis_refs"))
    missing = summary.get("missing_information_case", {})
    checks["missing_information:gap"] = bool(missing.get("information_gap_ref")) and missing.get("sufficiency_status") == "INSUFFICIENT" and missing.get("stop_ref") is None
    for case in negatives:
        checks[f"negative:{case.get('case_id')}:rejected"] = bool(case.get("all_checks_passed")) and case.get("admission_state") == "REJECTED" and case.get("a_route_invoked") is False
    failed = [name for name, passed in checks.items() if not passed]
    return {
        "phase": summary.get("phase"),
        "check_count": len(checks),
        "all_checks_passed": not failed,
        "failed_checks": failed,
        "operational_result": "PASS" if not failed else "FAIL",
        "cognitive_logic_result": "NOT_INDEPENDENTLY_EXERCISED",
        "final_decision": "GO" if not failed else "NOT_GO",
        "checks": checks,
    }


def main() -> int:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_SUMMARY
    summary = json.loads(path.read_text(encoding="utf-8"))
    result = verify(summary)
    print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True))
    return 0 if result["all_checks_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
