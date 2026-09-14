"""User-terminal runner for the controlled Evidence -> Field integration."""

from __future__ import annotations

import json
from pathlib import Path

from .engine_v1 import EvidenceContextFieldCurrentWorldControlledEngineV1


OUTPUT_DIR = Path("_eval_out/evidence_context_field_current_world_controlled_v1")


def main() -> None:
    summary = EvidenceContextFieldCurrentWorldControlledEngineV1().run()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output = OUTPUT_DIR / "runner_summary_v1.json"
    output.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({"output": str(output), "case_count": summary["controlled_case_count"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
