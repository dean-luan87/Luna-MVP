"""User-terminal runner for the controlled Runtime Grant phase."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .engine_v1 import RuntimeGrantPreExecutionAuthorizationEvaluationEngineV1


OUTPUT_DIR = Path("_eval_out/runtime_grant_pre_execution_authorization_v1")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run controlled Runtime Grant pre-execution authorization."
    )
    parser.add_argument("--output-root", type=Path, default=OUTPUT_DIR)
    args = parser.parse_args()
    summary = RuntimeGrantPreExecutionAuthorizationEvaluationEngineV1().run()
    args.output_root.mkdir(parents=True, exist_ok=True)
    output = args.output_root / "runner_summary_v1.json"
    output.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    print(json.dumps({"output": str(output), "status": summary["status"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
