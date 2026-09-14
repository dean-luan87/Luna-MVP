"""Fail-closed verifier for the candidate-only FPO compatibility seam."""

from __future__ import annotations

from capabilities.evaluation.common.independent_proof_v1 import independent_case_proof
from capabilities.evaluation.perception_routing_admission_compatibility_controlled.engine_v1 import PerceptionRoutingAdmissionCompatibilityEvaluationEngineV1

import argparse
import json
from pathlib import Path
from typing import Any


OUTPUT_DIR = Path("_eval_out/perception_routing_admission_compatibility_v1")
REQUIRED_CASES = {
    "SINGLE_ROUTING_CANDIDATE_COMPATIBLE",
    "MULTIPLE_ROUTING_CANDIDATES",
    "SAME_CLASS_MULTIPLE_ROUTES",
    "SAME_CAPABILITY_MULTIPLE_DEMANDS",
    "NO_ROUTING_CANDIDATE",
    "INVALID_ROUTING_CANDIDATE",
    "LINEAGE_MISMATCH",
    "MISSING_REQUIRED_TARGET_FIELD",
    "HISTORICAL_REQUEST_REQUIRES_PROVIDER_FIELD",
    "HISTORICAL_REQUEST_REQUIRES_MODEL_FIELD",
    "CAPABILITY_ADMITTED_BUT_RUNTIME_NOT_AUTO_ADMITTED",
    "SCENARIO12_SIGNAGE",
    "SCENARIO12_HUMAN_FLOW",
    "SCENARIO12_BOTH",
    "DETERMINISTIC_REPLAY",
    "MALFORMED_INPUT_SHAPE",
    "UNSUPPORTED_OBSERVATION_CLASS",
}


def verify(summary):
    proof = independent_case_proof(
        summary,
        lambda: PerceptionRoutingAdmissionCompatibilityEvaluationEngineV1().run(),
        source="R09 routing admission compatibility; canonical fixture + independent engine invocation",
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
            "recomputed_source": "fresh PerceptionRoutingAdmissionCompatibilityEvaluationEngineV1().run()",
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Verify candidate-only Perception Routing admission compatibility."
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
