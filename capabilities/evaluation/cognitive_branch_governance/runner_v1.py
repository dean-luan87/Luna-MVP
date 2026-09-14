"""User-terminal Runner for controlled candidate-only Branch Governance."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .engine_v1 import CognitiveBranchGovernanceEvaluationEngineV1


OUTPUT_DIR = Path("_eval_out/cognitive_branch_governance_v1")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run controlled Cognitive Branch Governance.")
    parser.parse_args()
    summary = CognitiveBranchGovernanceEvaluationEngineV1().run()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output = json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True)
    (OUTPUT_DIR / "runner_summary_v1.json").write_text(output + "\n", encoding="utf-8")
    print(output)


if __name__ == "__main__":
    main()
