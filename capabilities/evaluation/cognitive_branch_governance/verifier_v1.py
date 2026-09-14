"""Verifier for candidate-only Cognitive Branch Governance."""

from __future__ import annotations

from capabilities.evaluation.common.independent_proof_v1 import independent_case_proof
from capabilities.evaluation.cognitive_branch_governance.engine_v1 import CognitiveBranchGovernanceEvaluationEngineV1

import argparse
import json
from pathlib import Path
from typing import Any, Dict, Iterable


def _case(cases: Iterable[Dict[str, Any]], case_id: str) -> Dict[str, Any]:
    return next(item for item in cases if item.get("case_id") == case_id)


def _check(checks: Dict[str, bool], name: str, value: object) -> None:
    checks[name] = bool(value)


def _decisions(case: Dict[str, Any]) -> list[Dict[str, Any]]:
    return list((case.get("result") or {}).get("governance_decisions") or [])


def _statuses(case: Dict[str, Any]) -> tuple[str, ...]:
    return tuple(item.get("governance_status") for item in _decisions(case))


def _decision_pairs(case: Dict[str, Any]) -> tuple[tuple[str, str], ...]:
    return tuple(
        (item.get("branch_ref"), item.get("governance_status"))
        for item in _decisions(case)
    )


def verify(summary):
    proof = independent_case_proof(
        summary,
        lambda: CognitiveBranchGovernanceEvaluationEngineV1().run(),
        source="R04 cognitive branch governance; canonical fixture + independent engine invocation",
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
            "recomputed_source": "fresh CognitiveBranchGovernanceEvaluationEngineV1().run()",
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify controlled Cognitive Branch Governance.")
    parser.add_argument("summary", nargs="?", default="_eval_out/cognitive_branch_governance_v1/runner_summary_v1.json")
    args = parser.parse_args()
    result = verify(json.loads(Path(args.summary).read_text(encoding="utf-8")))
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if result["all_checks_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())


__all__ = ["verify", "main"]
