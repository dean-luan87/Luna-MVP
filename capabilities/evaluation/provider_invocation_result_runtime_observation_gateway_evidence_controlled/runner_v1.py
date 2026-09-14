"""User-terminal runner for the controlled execution-to-evidence seam."""

from __future__ import annotations

import json
from pathlib import Path

from .engine_v1 import ProviderInvocationObservationGatewayEvidenceEvaluationEngineV1


OUTPUT_DIR = Path("_eval_out/provider_invocation_result_runtime_observation_gateway_evidence_controlled_v1")


def main() -> None:
    summary = ProviderInvocationObservationGatewayEvidenceEvaluationEngineV1().run()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output = OUTPUT_DIR / "runner_summary_v1.json"
    output.write_text(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output), "case_count": summary["controlled_case_count"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
