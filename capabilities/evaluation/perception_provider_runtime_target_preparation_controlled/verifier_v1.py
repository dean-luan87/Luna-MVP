"""Static/contract verifier for Provider Runtime Target Preparation."""

from __future__ import annotations

from capabilities.evaluation.common.independent_proof_v1 import independent_case_proof
from capabilities.evaluation.perception_provider_runtime_target_preparation_controlled.engine_v1 import ProviderRuntimeTargetPreparationEvaluationEngineV1

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List


OUTPUT_DIR = Path("_eval_out/perception_provider_runtime_target_preparation_v1")
REQUIRED_CASES = {
    "SINGLE_COMPATIBILITY_SINGLE_PROVIDER",
    "SINGLE_COMPATIBILITY_MULTIPLE_PROVIDERS",
    "MULTIPLE_COMPATIBILITY_CANDIDATES",
    "SAME_PROVIDER_CLASS_TWO_PROVIDER_CANDIDATES",
    "SAME_PROVIDER_MULTIPLE_DEMANDS",
    "SAME_CAPABILITY_MULTIPLE_PROVIDERS",
    "NO_COMPATIBILITY_CANDIDATE",
    "NO_PROVIDER_MAPPING",
    "NO_MATCHING_PROVIDER",
    "PROVIDER_UNAVAILABLE",
    "PROVIDER_NOT_ADMITTED",
    "INVALID_COMPATIBILITY_CANDIDATE",
    "LINEAGE_MISMATCH",
    "DUPLICATE_PROVIDER_CANDIDATE",
    "MODEL_REF_OPTIONAL",
    "NO_MODEL_INFERENCE",
    "NO_EXECUTION_INSTANCE_CREATION",
    "NO_PROVIDER_BINDING",
    "NO_GATEWAY_ADMISSION",
    "SCENARIO12_SIGNAGE",
    "SCENARIO12_HUMAN_FLOW",
    "SCENARIO12_BOTH",
    "DETERMINISTIC_REPLAY",
    "MALFORMED_INPUT_SHAPE",
}


def verify(summary):
    proof = independent_case_proof(
        summary,
        lambda: ProviderRuntimeTargetPreparationEvaluationEngineV1().run(),
        source="R10 provider runtime target preparation; canonical fixture + independent engine invocation",
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
            "recomputed_source": "fresh ProviderRuntimeTargetPreparationEvaluationEngineV1().run()",
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Verify controlled Provider runtime target preparation.")
    parser.add_argument("--output-root", type=Path, default=OUTPUT_DIR)
    args = parser.parse_args()
    summary_path = args.output_root / "runner_summary_v1.json"
    report = verify(json.loads(summary_path.read_text(encoding="utf-8")))
    args.output_root.mkdir(parents=True, exist_ok=True)
    (args.output_root / "verification_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
