#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Governance Constraint Module Legacy Extraction DryRun v1."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.governance_constraint_module_legacy_extraction_dryrun_v1 import (
    run_governance_constraint_module_legacy_extraction_dryrun_v1,
)

DEFAULT_OUTPUT_ROOT = (
    REPO_ROOT / "_eval_out" / "governance_constraint_module_legacy_extraction_dryrun_v1_smoke_v0"
)
DEFAULT_PLANNING_ROOT = (
    REPO_ROOT / "_eval_out" / "governance_constraint_module_legacy_extraction_planning_v1_smoke_v0"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    ("legacy_extraction_dryrun_policy", "legacy_extraction_dryrun_policy_v1.json"),
    ("legacy_chain_inventory_consumption_dryrun", "legacy_chain_inventory_consumption_dryrun_v1.json"),
    ("phase_to_constraint_mapping_dryrun", "phase_to_constraint_mapping_dryrun_v1.json"),
    ("canonical_frozen_field_extraction_dryrun", "canonical_frozen_field_extraction_dryrun_v1.json"),
    ("phase_mode_lifecycle_contract_dryrun", "phase_mode_lifecycle_contract_dryrun_v1.json"),
    ("domain_constraint_extraction_dryrun", "domain_constraint_extraction_dryrun_v1.json"),
    ("constraint_inheritance_policy_dryrun", "constraint_inheritance_policy_dryrun_v1.json"),
    ("legacy_absorption_policy_dryrun", "legacy_absorption_policy_dryrun_v1.json"),
    ("constraint_module_output_plan_dryrun", "constraint_module_output_plan_dryrun_v1.json"),
    ("legacy_extraction_dryrun_readiness_decision", "legacy_extraction_dryrun_readiness_decision_v1.json"),
)


def _write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run Governance Constraint Module Legacy Extraction DryRun v1"
    )
    parser.add_argument("--output-root", default=str(DEFAULT_OUTPUT_ROOT))
    parser.add_argument(
        "--governance-constraint-module-legacy-extraction-planning-root",
        default=str(DEFAULT_PLANNING_ROOT),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    output_root = Path(args.output_root)
    result = run_governance_constraint_module_legacy_extraction_dryrun_v1(
        governance_constraint_module_legacy_extraction_planning_root=args.governance_constraint_module_legacy_extraction_planning_root,
    )
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
