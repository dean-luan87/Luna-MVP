"""Controlled artifact runner for the governance verification backbone."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .engine_v1 import GovernanceVerificationBackboneEvaluationEngineV1


OUTPUT_DIR = Path("_eval_out/governance_verification_backbone_core_rules_v1")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run controlled governance backbone evaluation.")
    parser.add_argument("--output-root", type=Path, default=OUTPUT_DIR)
    args = parser.parse_args()
    summary = GovernanceVerificationBackboneEvaluationEngineV1().run()
    args.output_root.mkdir(parents=True, exist_ok=True)
    output = args.output_root / "runner_summary_v1.json"
    output.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({"phase": summary["phase"], "status": summary["status"], "output": str(output)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
