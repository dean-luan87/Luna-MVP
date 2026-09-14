"""Fail-closed verifier for controlled A-Route Need formation."""

from __future__ import annotations

from capabilities.evaluation.common.independent_proof_v1 import independent_case_proof
from capabilities.evaluation.a_route_information_need_formation.engine_v1 import ARouteInformationNeedFormationEvaluationEngineV1

import argparse
import json
from pathlib import Path
from typing import Any, Dict


PHASE = "Phase-P1-Luna-A-Route-Information-Need-Formation-v1-001"


def _check(checks: Dict[str, bool], name: str, value: Any) -> None:
    checks[name] = bool(value)


def verify(summary):
    proof = independent_case_proof(
        summary,
        lambda: ARouteInformationNeedFormationEvaluationEngineV1().run(),
        source="R01 information need formation; canonical fixture + independent engine invocation",
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
            "recomputed_source": "fresh ARouteInformationNeedFormationEvaluationEngineV1().run()",
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Verify controlled A-Route Need formation.")
    parser.add_argument("--summary", type=Path, default=Path("_eval_out/a_route_information_need_formation_v1/runner_summary_v1.json"))
    parser.add_argument("--output", type=Path, default=Path("_eval_out/a_route_information_need_formation_v1/verifier_result_v1.json"))
    args = parser.parse_args()
    result = verify(json.loads(args.summary.read_text(encoding="utf-8")))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
