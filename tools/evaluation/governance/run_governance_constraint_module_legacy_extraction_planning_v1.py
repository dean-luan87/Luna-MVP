#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Governance Constraint Module Legacy Extraction Planning v1."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.governance_constraint_module_legacy_extraction_planning_v1 import (
    run_governance_constraint_module_legacy_extraction_planning_v1,
)

DEFAULT_OUTPUT_ROOT = (
    REPO_ROOT / "_eval_out" / "governance_constraint_module_legacy_extraction_planning_v1_smoke_v0"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    ("legacy_extraction_planning_policy", "legacy_extraction_planning_policy_v1.json"),
    ("legacy_governance_chain_inventory", "legacy_governance_chain_inventory_v1.json"),
    ("legacy_phase_to_constraint_source_matrix", "legacy_phase_to_constraint_source_matrix_v1.json"),
    ("canonical_frozen_field_extraction_plan", "canonical_frozen_field_extraction_plan_v1.json"),
    ("phase_mode_lifecycle_contract_extraction_plan", "phase_mode_lifecycle_contract_extraction_plan_v1.json"),
    ("domain_constraint_extraction_plan", "domain_constraint_extraction_plan_v1.json"),
    ("governance_constraint_inheritance_policy_plan", "governance_constraint_inheritance_policy_plan_v1.json"),
    ("legacy_absorption_policy_plan", "legacy_absorption_policy_plan_v1.json"),
    ("governance_constraint_module_output_plan", "governance_constraint_module_output_plan_v1.json"),
    ("legacy_extraction_planning_readiness_decision", "legacy_extraction_planning_readiness_decision_v1.json"),
)


def _write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run Governance Constraint Module Legacy Extraction Planning v1"
    )
    parser.add_argument("--output-root", default=str(DEFAULT_OUTPUT_ROOT))
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    output_root = Path(args.output_root)
    result = run_governance_constraint_module_legacy_extraction_planning_v1()
    for key, filename in OUTPUT_FILES:
        _write_json(output_root / filename, result[key])

    summary = result["summary"]
    print(
        json.dumps(
            {
                "phase": summary.get("phase"),
                "boundary_ok": summary.get("boundary_ok"),
                "final_decision": summary.get("final_decision"),
                "recommended_next_phase": summary.get("recommended_next_phase"),
                "violations": summary.get("violations"),
            },
            ensure_ascii=False,
        )
    )
    return 0 if summary.get("boundary_ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
