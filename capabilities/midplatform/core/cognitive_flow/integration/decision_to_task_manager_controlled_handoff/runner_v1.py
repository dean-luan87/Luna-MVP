"""Runner for the controlled Decision-to-Task Manager handoff."""

from __future__ import annotations

import json
from pathlib import Path

from .engine_v1 import build_decision_task_run_v1


OUTPUT_DIR = Path("_eval_out/decision_to_task_manager_controlled_handoff_v1")


def main() -> int:
    summary = build_decision_task_run_v1()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output = OUTPUT_DIR / "runner_summary_v1.json"
    output.write_text(json.dumps(summary, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

