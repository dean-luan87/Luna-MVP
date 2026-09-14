"""Module runner for controlled runtime-admission order adjudication."""

from __future__ import annotations

import json
from pathlib import Path

from .engine_v1 import build_runtime_admission_order_summary_v1


OUTPUT_DIR = Path("_eval_out/perception_routing_admission_order_adjudication_v1")


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output = OUTPUT_DIR / "runner_summary_v1.json"
    output.write_text(
        json.dumps(build_runtime_admission_order_summary_v1(), indent=2, sort_keys=True),
        encoding="utf-8",
    )
    print(output)


if __name__ == "__main__":
    main()

