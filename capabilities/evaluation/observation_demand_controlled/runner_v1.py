"""User-terminal runner for controlled Observation Demand formation."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .engine_v1 import ObservationDemandEvaluationEngineV1


OUTPUT_DIR = Path("_eval_out/observation_demand_v1")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run controlled Observation Demand formation.")
    parser.add_argument("--output-root", type=Path, default=OUTPUT_DIR)
    args = parser.parse_args()
    summary = ObservationDemandEvaluationEngineV1().run()
    args.output_root.mkdir(parents=True, exist_ok=True)
    output = json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True)
    (args.output_root / "runner_summary_v1.json").write_text(output + "\n", encoding="utf-8")
    print(output)


if __name__ == "__main__":
    main()


__all__ = ["main", "OUTPUT_DIR"]
