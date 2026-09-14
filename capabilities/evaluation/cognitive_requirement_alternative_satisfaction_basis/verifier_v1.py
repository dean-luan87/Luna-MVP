"""Fail-closed verifier for controlled alternative satisfaction basis semantics."""

from __future__ import annotations

from capabilities.evaluation.common.independent_proof_v1 import independent_case_proof
from capabilities.evaluation.cognitive_requirement_alternative_satisfaction_basis.engine_v1 import CognitiveRequirementAlternativeSatisfactionBasisEvaluationEngineV1

import argparse
import json
from pathlib import Path
from typing import Any

from .fixtures_v1 import (
    BASIS_A,
    LEGACY_COVERAGE_REF,
    LEGACY_REQUIREMENT_REF,
    REQUIREMENT_REF,
    SOURCE_MODE,
)


PHASE = "Phase-Cognitive-Requirement-Alternative-Satisfaction-Basis-Controlled-Implementation-v1-001"


def _check(checks: dict[str, bool], name: str, value: Any) -> None:
    checks[name] = bool(value)


def verify(summary):
    proof = independent_case_proof(
        summary,
        lambda: CognitiveRequirementAlternativeSatisfactionBasisEvaluationEngineV1().run(),
        source="R05 alternative satisfaction basis; canonical fixture + independent engine invocation",
        compare_top_level=("phase", "source_mode", "sandbox_regressions", "negative_guards"),
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
            "recomputed_source": "fresh CognitiveRequirementAlternativeSatisfactionBasisEvaluationEngineV1().run()",
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Verify alternative satisfaction basis semantics."
    )
    parser.add_argument(
        "--summary",
        type=Path,
        default=Path(
            "_eval_out/cognitive_requirement_alternative_satisfaction_basis_v1/runner_summary_v1.json"
        ),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "_eval_out/cognitive_requirement_alternative_satisfaction_basis_v1/verifier_result_v1.json"
        ),
    )
    args = parser.parse_args()
    result = verify(json.loads(args.summary.read_text(encoding="utf-8")))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()


__all__ = ["verify", "main"]
