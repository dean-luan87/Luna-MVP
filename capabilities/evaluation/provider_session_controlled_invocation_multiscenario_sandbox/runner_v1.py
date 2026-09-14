"""User-terminal runner for the synthetic Provider session sandbox."""

from __future__ import annotations

import json
from pathlib import Path

from .engine_v1 import ProviderSessionControlledInvocationEvaluationEngineV1


OUTPUT_DIR = Path("_eval_out/provider_session_controlled_invocation_multiscenario_sandbox_v1")


def main() -> None:
    summary = ProviderSessionControlledInvocationEvaluationEngineV1().run()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output = OUTPUT_DIR / "runner_summary_v1.json"
    output.write_text(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps({"output": str(output), "case_count": len(summary["cases"])}, ensure_ascii=False))


if __name__ == "__main__":
    main()
