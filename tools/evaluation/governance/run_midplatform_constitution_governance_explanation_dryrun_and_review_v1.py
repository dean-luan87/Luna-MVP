#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Midplatform Constitution Governance Explanation DryRunAndReview v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.midplatform_constitution_governance_explanation_dryrun_and_review_v1 import (
    run_midplatform_constitution_governance_explanation_dryrun_and_review_v1,
)

DEFAULT_EXPLAIN_PLAN = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_constitution_governance_explanation_planning"
)
DEFAULT_HIERARCHY_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_constitution_governance_hierarchy_dryrun_and_review"
)
DEFAULT_AUTH_EXT_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "capability_factory_authorization_standard_extension_dryrun_and_review"
)
DEFAULT_FACTORY_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "capability_factory_admission_and_operation_standard_dryrun_and_review"
)
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_constitution_governance_explanation_dryrun_and_review"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    (
        "constitution_governance_explanation_dryrun_and_review_policy",
        "constitution_governance_explanation_dryrun_and_review_policy_v1.json",
    ),
    (
        "constitution_explanation_planning_input_review",
        "constitution_explanation_planning_input_review_v1.json",
    ),
    ("constitution_layer_relationship_review", "constitution_layer_relationship_review_v1.json"),
    ("constitution_jurisdiction_conflict_review", "constitution_jurisdiction_conflict_review_v1.json"),
    ("constitution_generation_logic_review", "constitution_generation_logic_review_v1.json"),
    ("constitution_amendment_logic_review", "constitution_amendment_logic_review_v1.json"),
    (
        "system_vs_personalized_constitution_review",
        "system_vs_personalized_constitution_review_v1.json",
    ),
    ("hive_constitution_authority_review", "hive_constitution_authority_review_v1.json"),
    (
        "local_luna_constitution_consumption_boundary_review",
        "local_luna_constitution_consumption_boundary_review_v1.json",
    ),
    (
        "constitution_survival_mechanism_link_review",
        "constitution_survival_mechanism_link_review_v1.json",
    ),
    (
        "constitution_violation_alarm_penalty_review",
        "constitution_violation_alarm_penalty_review_v1.json",
    ),
    (
        "constitution_change_candidate_lifecycle_review",
        "constitution_change_candidate_lifecycle_review_v1.json",
    ),
    (
        "constitution_governance_decision_tree_review",
        "constitution_governance_decision_tree_review_v1.json",
    ),
    ("constitution_explanation_boundary_audit", "constitution_explanation_boundary_audit_v1.json"),
    (
        "constitution_explanation_blocked_path_result",
        "constitution_explanation_blocked_path_result_v1.json",
    ),
    ("constitution_explanation_closure_decision", "constitution_explanation_closure_decision_v1.json"),
    ("next_route_readiness_decision", "next_route_readiness_decision_v1.json"),
    ("non_claims_register", "non_claims_register_v1.json"),
)


def _write(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=DEFAULT_OUTPUT)
    p.add_argument(
        "--midplatform-constitution-governance-explanation-planning-root",
        default=DEFAULT_EXPLAIN_PLAN,
    )
    p.add_argument(
        "--midplatform-constitution-governance-hierarchy-dryrun-and-review-root",
        default=DEFAULT_HIERARCHY_DR,
    )
    p.add_argument(
        "--capability-factory-authorization-standard-extension-dryrun-and-review-root",
        default=DEFAULT_AUTH_EXT_DR,
    )
    p.add_argument(
        "--capability-factory-admission-and-operation-standard-dryrun-and-review-root",
        default=DEFAULT_FACTORY_DR,
    )
    args = p.parse_args()

    result = run_midplatform_constitution_governance_explanation_dryrun_and_review_v1(
        midplatform_constitution_governance_explanation_planning_root=(
            args.midplatform_constitution_governance_explanation_planning_root
        ),
        midplatform_constitution_governance_hierarchy_dryrun_and_review_root=(
            args.midplatform_constitution_governance_hierarchy_dryrun_and_review_root
        ),
        capability_factory_authorization_standard_extension_dryrun_and_review_root=(
            args.capability_factory_authorization_standard_extension_dryrun_and_review_root
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
                "dryrun_and_review_pass": sm.get("dryrun_and_review_pass"),
                "final_decision": sm.get("final_decision"),
                "recommended_next_phase": sm.get("recommended_next_phase"),
            },
            ensure_ascii=False,
        )
    )
    return 0 if sm.get("boundary_ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
