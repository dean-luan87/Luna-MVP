"""Verifier for controlled minimum relevant Self/External view behavior."""

from __future__ import annotations

from capabilities.evaluation.common.independent_proof_v1 import independent_case_proof
from capabilities.evaluation.a_route_minimum_relevant_cognitive_view.engine_v1 import ARouteMinimumRelevantCognitiveViewEvaluationEngineV1

import argparse
import json
from pathlib import Path
from typing import Any, Dict, Iterable


def _check(checks: Dict[str, bool], name: str, value: bool) -> None:
    checks[name] = bool(value)


def _result(case: Dict[str, Any]) -> Dict[str, Any]:
    return case.get("result") or {}


def _case(cases: Iterable[Dict[str, Any]], case_id: str) -> Dict[str, Any]:
    return next(item for item in cases if item.get("case_id") == case_id)


def verify(summary):
    proof = independent_case_proof(
        summary,
        lambda: ARouteMinimumRelevantCognitiveViewEvaluationEngineV1().run(),
        source="R02 minimum relevant cognitive view; canonical fixture + independent engine invocation",
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
            "recomputed_source": "fresh ARouteMinimumRelevantCognitiveViewEvaluationEngineV1().run()",
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Verify controlled minimum cognitive view evaluation.")
    parser.add_argument("summary", nargs="?", default="_eval_out/a_route_minimum_relevant_cognitive_view_v1/runner_summary_v1.json")
    args = parser.parse_args()
    summary = json.loads(Path(args.summary).read_text(encoding="utf-8"))
    print(json.dumps(verify(summary), ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
