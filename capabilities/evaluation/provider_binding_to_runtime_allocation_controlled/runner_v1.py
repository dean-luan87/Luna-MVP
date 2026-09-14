"""User-terminal runner for the controlled Provider Binding phase."""

from __future__ import annotations

import json
from pathlib import Path

from .engine_v1 import ProviderBindingToRuntimeAllocationEvaluationEngineV1


OUTPUT_PATH = Path("_eval_out/provider_binding_to_runtime_allocation_v1/runner_summary_v1.json")


def main() -> int:
    summary = ProviderBindingToRuntimeAllocationEvaluationEngineV1().run()
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(
        json.dumps(summary, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    print(json.dumps({"output": str(OUTPUT_PATH), "status": summary["status"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
