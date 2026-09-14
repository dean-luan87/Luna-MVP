"""User-terminal runner for controlled Provider runtime target preparation."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .engine_v1 import ProviderRuntimeTargetPreparationEvaluationEngineV1


OUTPUT_DIR = Path("_eval_out/perception_provider_runtime_target_preparation_v1")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run candidate-only Provider runtime target preparation."
    )
    parser.add_argument("--output-root", type=Path, default=OUTPUT_DIR)
    args = parser.parse_args()
    summary = ProviderRuntimeTargetPreparationEvaluationEngineV1().run()
    args.output_root.mkdir(parents=True, exist_ok=True)
    (args.output_root / "runner_summary_v1.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    print(json.dumps({"output": str(args.output_root / "runner_summary_v1.json"), "case_count": len(summary["cases"])}, ensure_ascii=False))


if __name__ == "__main__":
    main()
