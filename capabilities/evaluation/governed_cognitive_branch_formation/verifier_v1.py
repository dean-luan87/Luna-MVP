"""Verifier for candidate-only governed cognitive branch formation."""

from __future__ import annotations

from capabilities.evaluation.common.independent_proof_v1 import independent_case_proof
from capabilities.evaluation.governed_cognitive_branch_formation.engine_v1 import GovernedCognitiveBranchFormationEvaluationEngineV1

import argparse
import json
from pathlib import Path
from typing import Any, Dict, Iterable


def _case(cases: Iterable[Dict[str, Any]], case_id: str) -> Dict[str, Any]:
    return next(item for item in cases if item.get("case_id") == case_id)


def _check(checks: Dict[str, bool], name: str, value: object) -> None:
    checks[name] = bool(value)


def _branches(case: Dict[str, Any]) -> list[Dict[str, Any]]:
    return list((case.get("result") or {}).get("branches") or [])


def verify(summary):
    proof = independent_case_proof(
        summary,
        lambda: GovernedCognitiveBranchFormationEvaluationEngineV1().run(),
        source="R06 governed branch formation; canonical fixture + independent engine invocation",
        compare_top_level=("phase", "source_mode"),
    )
    failed = sorted(name for name, passed in proof.items() if not passed)
    return {
        "phase": summary.get("phase"),
        "checks": proof,
        "failed_checks": failed,
        "all_checks_passed": not failed,
        "cognitive_logic_result": "PASS" if not failed else "FAIL",
        "operational_result": "PASS" if not failed else "FAIL",
        "final_decision": "GO" if not failed else "NO-GO",
        "proof_provenance": {
            "expected_source": "canonical fixture + independent engine invocation",
            "observed_source": "runner summary artifact",
            "recomputed_source": "fresh GovernedCognitiveBranchFormationEvaluationEngineV1().run()",
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify governed cognitive branch formation.")
    parser.add_argument("summary", nargs="?", default="_eval_out/governed_cognitive_branch_formation_v1/runner_summary_v1.json")
    args = parser.parse_args()
    result = verify(json.loads(Path(args.summary).read_text(encoding="utf-8")))
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if result["all_checks_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())


__all__ = ["verify", "main"]
