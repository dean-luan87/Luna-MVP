"""User-terminal runner for controlled Strategy Coordination."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .engine_v1 import StrategyCoordinationEvaluationEngineV1


OUTPUT_DIR = Path("_eval_out/strategy_coordination_v1")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run controlled Strategy Coordination.")
    parser.parse_args()
    summary = StrategyCoordinationEvaluationEngineV1().run()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output = json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True)
    (OUTPUT_DIR / "runner_summary_v1.json").write_text(output + "\n", encoding="utf-8")
    print(output)


if __name__ == "__main__":
    main()


__all__ = ["main", "OUTPUT_DIR"]
