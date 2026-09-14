"""Module runner for the controlled authoritative mechanical phase."""

from __future__ import annotations

import json
from pathlib import Path

from .engine_v1 import ProviderBindingRuntimeAllocationExecutionEvaluationEngineV1


OUTPUT_PATH = Path("_eval_out/provider_binding_runtime_allocation_execution_instance_v1/runner_summary_v1.json")


def main() -> int:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    summary = ProviderBindingRuntimeAllocationExecutionEvaluationEngineV1().run()
    OUTPUT_PATH.write_text(json.dumps(summary, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps({"output": str(OUTPUT_PATH), "status": summary["status"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
