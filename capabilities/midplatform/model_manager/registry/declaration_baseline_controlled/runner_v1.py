"""Controlled declaration-baseline runner."""

from __future__ import annotations

import json
from pathlib import Path

from .validator_v1 import validate_declaration_baseline_v1


def run_declaration_baseline_v1(root: Path) -> dict:
    return validate_declaration_baseline_v1(root)


def main() -> None:
    root = Path(__file__).resolve().parents[5]
    result = run_declaration_baseline_v1(root)
    output_dir = root / "_eval_out/capability_model_provider_governance_declaration_baseline_v1"
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "declaration_baseline_summary_v1.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

