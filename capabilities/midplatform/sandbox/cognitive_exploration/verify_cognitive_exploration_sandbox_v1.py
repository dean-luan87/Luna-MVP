"""User-terminal contract verifier for the controlled sandbox."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict

from .cognitive_exploration_sandbox_static_validators_v1 import check_trace_contract


DEFAULT_TRACE = Path(
    "_eval_out/controlled_cognitive_exploration_sandbox_v1_smoke_v0/cognitive_trace.json"
)
DEFAULT_REPORT = Path(
    "_eval_out/controlled_cognitive_exploration_sandbox_v1_smoke_v0/verification_report.json"
)


def verify(trace: Dict[str, Any]) -> Dict[str, Any]:
    checks, failed = check_trace_contract(trace)
    observations = [
        observation
        for scenario in trace.get("scenarios", [])
        for observation in scenario.get("cognitive_logic_observations", [])
    ]
    return {
        "phase": trace.get("phase_id"),
        "all_checks_passed": not failed,
        "failed_checks": failed,
        "checks": checks,
        "contract_failures": failed,
        "cognitive_logic_observations": observations,
        "cognitive_logic_result": "REVIEW_REQUIRED_NOT_A_VERDICT",
        "operational_result": "PASS" if not failed else "FAIL",
        "final_decision": "TRACE_REVIEW_REQUIRED" if not failed else "NO-GO",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify the controlled cognitive sandbox trace.")
    parser.add_argument("trace", nargs="?", default=str(DEFAULT_TRACE))
    parser.add_argument("--report", default=str(DEFAULT_REPORT))
    args = parser.parse_args()
    result = verify(json.loads(Path(args.trace).read_text(encoding="utf-8")))
    report_path = Path(args.report)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(
        json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if result["all_checks_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())


__all__ = ["verify", "main"]
