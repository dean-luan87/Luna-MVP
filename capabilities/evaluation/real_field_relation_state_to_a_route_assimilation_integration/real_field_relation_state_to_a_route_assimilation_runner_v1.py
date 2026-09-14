"""Runner for the controlled Field relation state -> A-Route handoff."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .engine_v1 import FieldRelationStateToARouteAssimilationEngineV1


ROOT = Path(__file__).resolve().parents[3]
OUTPUT_DIR = ROOT / "_eval_out/real_field_relation_state_to_a_route_assimilation_integration_v1"


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run controlled read-only Field relation state assimilation through A-Route."
    )
    parser.parse_args()
    summary = FieldRelationStateToARouteAssimilationEngineV1().run()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output = json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True)
    (OUTPUT_DIR / "runner_summary_v1.json").write_text(output + "\n", encoding="utf-8")
    print(output)


if __name__ == "__main__":
    main()
