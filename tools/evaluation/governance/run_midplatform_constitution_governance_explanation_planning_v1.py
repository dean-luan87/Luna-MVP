#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Midplatform Constitution Governance Explanation Planning v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.midplatform_constitution_governance_explanation_planning_v1 import (
    run_midplatform_constitution_governance_explanation_planning_v1,
)

DEFAULT_HIERARCHY_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_constitution_governance_hierarchy_dryrun_and_review"
)
DEFAULT_HIERARCHY_PLAN = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_constitution_governance_hierarchy_planning"
)
DEFAULT_AUTH_EXT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "capability_factory_authorization_standard_extension_planning"
)
DEFAULT_FACTORY_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "capability_factory_admission_and_operation_standard_dryrun_and_review"
)
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_constitution_governance_explanation_planning"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    (
        "constitution_governance_explanation_planning_policy",
        "constitution_governance_explanation_planning_policy_v1.json",
    ),
    ("constitution_hierarchy_input_review", "constitution_hierarchy_input_review_v1.json"),
    (
        "constitution_layer_relationship_explanation",
        "constitution_layer_relationship_explanation_v1.json",
    ),
    (
        "constitution_jurisdiction_and_conflict_rule",
        "constitution_jurisdiction_and_conflict_rule_v1.json",
    ),
    ("constitution_generation_logic", "constitution_generation_logic_v1.json"),
    ("constitution_amendment_logic", "constitution_amendment_logic_v1.json"),
    (
        "system_vs_personalized_constitution_rule",
        "system_vs_personalized_constitution_rule_v1.json",
    ),
    ("hive_constitution_authority_rule", "hive_constitution_authority_rule_v1.json"),
    (
        "local_luna_constitution_consumption_boundary",
        "local_luna_constitution_consumption_boundary_v1.json",
    ),
    ("constitution_survival_mechanism_link", "constitution_survival_mechanism_link_v1.json"),
    (
        "constitution_violation_alarm_and_penalty_rule",
        "constitution_violation_alarm_and_penalty_rule_v1.json",
    ),
    ("constitution_change_candidate_lifecycle", "constitution_change_candidate_lifecycle_v1.json"),
    ("constitution_governance_decision_tree", "constitution_governance_decision_tree_v1.json"),
    (
        "constitution_explanation_non_claims_register",
        "constitution_explanation_non_claims_register_v1.json",
    ),
    (
        "constitution_governance_explanation_planning_decision",
        "constitution_governance_explanation_planning_decision_v1.json",
    ),
)


def _write(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=DEFAULT_OUTPUT)
    p.add_argument(
        "--midplatform-constitution-governance-hierarchy-dryrun-and-review-root",
        default=DEFAULT_HIERARCHY_DR,
    )
    p.add_argument(
        "--midplatform-constitution-governance-hierarchy-planning-root",
        default=DEFAULT_HIERARCHY_PLAN,
    )
    p.add_argument(
        "--capability-factory-authorization-standard-extension-planning-root",
        default=DEFAULT_AUTH_EXT,
    )
    p.add_argument(
        "--capability-factory-admission-and-operation-standard-dryrun-and-review-root",
        default=DEFAULT_FACTORY_DR,
    )
    args = p.parse_args()

    result = run_midplatform_constitution_governance_explanation_planning_v1(
        midplatform_constitution_governance_hierarchy_dryrun_and_review_root=(
            args.midplatform_constitution_governance_hierarchy_dryrun_and_review_root
        ),
        midplatform_constitution_governance_hierarchy_planning_root=(
            args.midplatform_constitution_governance_hierarchy_planning_root
        ),
        capability_factory_authorization_standard_extension_planning_root=(
            args.capability_factory_authorization_standard_extension_planning_root
        ),
        capability_factory_admission_and_operation_standard_dryrun_and_review_root=(
            args.capability_factory_admission_and_operation_standard_dryrun_and_review_root
        ),
        output_root=args.output_root,
    )

    out = Path(args.output_root)
    for key, fname in OUTPUT_FILES:
        _write(out / fname, result[key])

    sm = result["summary"]
    print(
        json.dumps(
            {
                "output_root": str(out),
                "boundary_ok": sm.get("boundary_ok"),
                "final_decision": sm.get("final_decision"),
                "recommended_next_phase": sm.get("recommended_next_phase"),
            },
            ensure_ascii=False,
        )
    )
    return 0 if sm.get("boundary_ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
