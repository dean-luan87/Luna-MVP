"""User-terminal runner for controlled perception routing formation."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .engine_v1 import PerceptionRoutingEvaluationEngineV1


OUTPUT_DIR = Path("_eval_out/observation_perception_routing_v1")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run controlled Perception Routing Candidate formation."
    )
    parser.add_argument("--output-root", type=Path, default=OUTPUT_DIR)
    args = parser.parse_args()
    summary = PerceptionRoutingEvaluationEngineV1().run()
    args.output_root.mkdir(parents=True, exist_ok=True)
    output = json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True)
    (args.output_root / "runner_summary_v1.json").write_text(
        output + "\n", encoding="utf-8"
    )
    print(output)


if __name__ == "__main__":
    main()


__all__ = ["main", "OUTPUT_DIR"]
