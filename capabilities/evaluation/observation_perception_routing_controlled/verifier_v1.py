"""Fail-closed verifier for candidate-only perception routing formation."""

from __future__ import annotations

from capabilities.evaluation.common.independent_proof_v1 import independent_case_proof
from capabilities.evaluation.observation_perception_routing_controlled.engine_v1 import PerceptionRoutingEvaluationEngineV1

import argparse
import json
from pathlib import Path
from typing import Any


OUTPUT_DIR = Path("_eval_out/observation_perception_routing_v1")
REQUIRED_CASES = {
    "SINGLE_DEMAND_SINGLE_CAPABILITY_SINGLE_ROUTE",
    "SINGLE_DEMAND_MULTIPLE_CAPABILITY_CANDIDATES",
    "TWO_INDEPENDENT_DEMANDS",
    "SAME_DEMAND_SAME_CLASS_TWO_CANDIDATES",
    "SAME_CAPABILITY_SUPPORTS_TWO_DEMANDS",
    "NO_OBSERVATION_DEMAND",
    "NO_CAPABILITY_REQUIREMENT",
    "NO_MATCHING_CAPABILITY",
    "CAPABILITY_UNAVAILABLE",
    "CAPABILITY_NOT_ADMITTED",
    "INVALID_RESOLUTION_CANDIDATE",
    "DEMAND_CAPABILITY_LINEAGE_MISMATCH",
    "SCENARIO_12_SIGNAGE",
    "SCENARIO_12_HUMAN_FLOW",
    "SCENARIO_12_BOTH_STRATEGIES",
    "DETERMINISTIC_REPLAY",
    "MALFORMED_INPUT_SHAPE",
}


def verify(summary):
    proof = independent_case_proof(
        summary,
        lambda: PerceptionRoutingEvaluationEngineV1().run(),
        source="R08 observation perception routing; canonical fixture + independent engine invocation",
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
            "recomputed_source": "fresh PerceptionRoutingEvaluationEngineV1().run()",
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Verify controlled Perception Routing Candidate formation."
    )
    parser.add_argument("--smoke-root", type=Path, default=OUTPUT_DIR)
    args = parser.parse_args()
    summary = json.loads(
        (args.smoke_root / "runner_summary_v1.json").read_text(encoding="utf-8")
    )
    report = verify(summary)
    (args.smoke_root / "verifier_report_v1.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()


__all__ = ["OUTPUT_DIR", "REQUIRED_CASES", "verify", "main"]
