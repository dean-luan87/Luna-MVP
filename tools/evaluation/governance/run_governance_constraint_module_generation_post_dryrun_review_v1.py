#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Governance Constraint Module Generation Post-DryRun Review v1."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.governance_constraint_module_generation_post_dryrun_review_v1 import (
    run_governance_constraint_module_generation_post_dryrun_review_v1,
)

DEFAULT_OUTPUT_ROOT = (
    REPO_ROOT / "_eval_out" / "governance_constraint_module_generation_post_dryrun_review_v1_smoke_v0"
)
DEFAULT_DRYRUN_ROOT = (
    REPO_ROOT / "_eval_out" / "governance_constraint_module_generation_dryrun_v1_smoke_v0"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    (
        "governance_constraint_module_generation_post_dryrun_review_policy",
        "governance_constraint_module_generation_post_dryrun_review_policy_v1.json",
    ),
    (
        "module_generation_dryrun_completeness_review",
        "module_generation_dryrun_completeness_review_v1.json",
    ),
    ("module_non_generation_review", "module_non_generation_review_v1.json"),
    ("future_consumption_simulation_review", "future_consumption_simulation_review_v1.json"),
    (
        "domain_differentiation_preservation_review",
        "domain_differentiation_preservation_review_v1.json",
    ),
    ("frozen_field_non_enforcement_review", "frozen_field_non_enforcement_review_v1.json"),
    ("verifier_baseline_non_integration_review", "verifier_baseline_non_integration_review_v1.json"),
    ("phase_template_non_modification_review", "phase_template_non_modification_review_v1.json"),
    ("legacy_absorption_non_rewrite_review", "legacy_absorption_non_rewrite_review_v1.json"),
    ("non_claims_and_forbidden_shortcut_review", "non_claims_and_forbidden_shortcut_review_v1.json"),
    ("mainline_resume_block_review", "mainline_resume_block_review_v1.json"),
    (
        "governance_constraint_module_generation_post_dryrun_review_readiness_decision",
        "governance_constraint_module_generation_post_dryrun_review_readiness_decision_v1.json",
    ),
)


def _write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run Governance Constraint Module Generation Post-DryRun Review v1"
    )
    parser.add_argument("--output-root", default=str(DEFAULT_OUTPUT_ROOT))
    parser.add_argument(
        "--governance-constraint-module-generation-dryrun-root",
        default=str(DEFAULT_DRYRUN_ROOT),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    output_root = Path(args.output_root)
    result = run_governance_constraint_module_generation_post_dryrun_review_v1(
        governance_constraint_module_generation_dryrun_root=args.governance_constraint_module_generation_dryrun_root,
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
