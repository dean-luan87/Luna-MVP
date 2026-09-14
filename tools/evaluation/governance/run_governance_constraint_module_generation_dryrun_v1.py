#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Governance Constraint Module Generation DryRun v1."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.governance_constraint_module_generation_dryrun_v1 import (
    run_governance_constraint_module_generation_dryrun_v1,
)

DEFAULT_OUTPUT_ROOT = (
    REPO_ROOT / "_eval_out" / "governance_constraint_module_generation_dryrun_v1_smoke_v0"
)
DEFAULT_PLANNING_ROOT = (
    REPO_ROOT / "_eval_out" / "governance_constraint_module_generation_planning_v1_smoke_v0"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    (
        "governance_constraint_module_generation_dryrun_policy",
        "governance_constraint_module_generation_dryrun_policy_v1.json",
    ),
    (
        "canonical_phase_contract_consumption_dryrun",
        "canonical_phase_contract_consumption_dryrun_v1.json",
    ),
    (
        "domain_constraint_registry_consumption_dryrun",
        "domain_constraint_registry_consumption_dryrun_v1.json",
    ),
    (
        "phase_inheritance_matrix_consumption_dryrun",
        "phase_inheritance_matrix_consumption_dryrun_v1.json",
    ),
    (
        "canonical_frozen_fields_consumption_dryrun",
        "canonical_frozen_fields_consumption_dryrun_v1.json",
    ),
    (
        "phase_mode_lifecycle_consumption_dryrun",
        "phase_mode_lifecycle_consumption_dryrun_v1.json",
    ),
    (
        "constraint_required_fields_consumption_dryrun",
        "constraint_required_fields_consumption_dryrun_v1.json",
    ),
    (
        "verifier_baseline_consumption_dryrun",
        "verifier_baseline_consumption_dryrun_v1.json",
    ),
    (
        "non_claims_and_forbidden_shortcut_library_consumption_dryrun",
        "non_claims_and_forbidden_shortcut_library_consumption_dryrun_v1.json",
    ),
    (
        "constraint_extension_rule_consumption_dryrun",
        "constraint_extension_rule_consumption_dryrun_v1.json",
    ),
    (
        "legacy_absorption_policy_consumption_dryrun",
        "legacy_absorption_policy_consumption_dryrun_v1.json",
    ),
    (
        "governance_constraint_module_generation_dryrun_readiness_decision",
        "governance_constraint_module_generation_dryrun_readiness_decision_v1.json",
    ),
)


def _write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Governance Constraint Module Generation DryRun v1")
    parser.add_argument("--output-root", default=str(DEFAULT_OUTPUT_ROOT))
    parser.add_argument(
        "--governance-constraint-module-generation-planning-root",
        default=str(DEFAULT_PLANNING_ROOT),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    output_root = Path(args.output_root)
    result = run_governance_constraint_module_generation_dryrun_v1(
        governance_constraint_module_generation_planning_root=args.governance_constraint_module_generation_planning_root,
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
