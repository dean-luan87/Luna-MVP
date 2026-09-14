#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Midplatform User Output Constitution DryRunAndReview v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.midplatform_user_output_constitution_dryrun_and_review_v1 import (
    run_midplatform_user_output_constitution_dryrun_and_review_v1,
)

DEFAULT_PLANNING = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_user_output_constitution_planning"
)
DEFAULT_OUTPUT_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_output_plane_integration_dryrun_and_review"
)
DEFAULT_CONSTITUTION_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_constitution_governance_explanation_dryrun_and_review"
)
DEFAULT_TEMPLATE = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_module_definition_template_planning"
)
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_user_output_constitution_dryrun_and_review"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    ("user_output_constitution_dryrun_review_policy", "user_output_constitution_dryrun_review_policy_v1.json"),
    ("user_output_constitution_planning_input_review", "user_output_constitution_planning_input_review_v1.json"),
    ("user_output_constitution_candidate", "user_output_constitution_candidate_v1.json"),
    ("user_output_scope_jurisdiction_review", "user_output_scope_jurisdiction_review_v1.json"),
    ("user_output_admission_rule_dryrun_review", "user_output_admission_rule_dryrun_review_v1.json"),
    ("user_output_safety_rule_dryrun_review", "user_output_safety_rule_dryrun_review_v1.json"),
    ("user_output_fact_uncertainty_rule_dryrun_review", "user_output_fact_uncertainty_rule_dryrun_review_v1.json"),
    ("user_output_privacy_rule_dryrun_review", "user_output_privacy_rule_dryrun_review_v1.json"),
    ("user_output_channel_rule_dryrun_review", "user_output_channel_rule_dryrun_review_v1.json"),
    (
        "user_output_tone_personalization_boundary_review",
        "user_output_tone_personalization_boundary_review_v1.json",
    ),
    (
        "user_output_refusal_hold_degrade_rule_review",
        "user_output_refusal_hold_degrade_rule_review_v1.json",
    ),
    (
        "user_output_explainability_traceability_review",
        "user_output_explainability_traceability_review_v1.json",
    ),
    ("user_output_conflict_policy_review", "user_output_conflict_policy_review_v1.json"),
    ("constitution_resolver_binding_review", "constitution_resolver_binding_review_v1.json"),
    ("constitution_constraint_bundle_candidate", "constitution_constraint_bundle_candidate_v1.json"),
    ("constitution_change_propagation_review", "constitution_change_propagation_review_v1.json"),
    ("downstream_impact_boundary_review", "downstream_impact_boundary_review_v1.json"),
    ("user_output_speech_display_boundary_review", "user_output_speech_display_boundary_review_v1.json"),
    (
        "user_output_memory_worldmodel_taskstate_boundary_review",
        "user_output_memory_worldmodel_taskstate_boundary_review_v1.json",
    ),
    ("user_output_constitution_boundary_audit", "user_output_constitution_boundary_audit_v1.json"),
    ("user_output_constitution_blocked_path_result", "user_output_constitution_blocked_path_result_v1.json"),
    ("user_output_constitution_closure_decision", "user_output_constitution_closure_decision_v1.json"),
    ("next_route_readiness_decision", "next_route_readiness_decision_v1.json"),
    ("non_claims_register", "non_claims_register_v1.json"),
)


def _write(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=DEFAULT_OUTPUT)
    p.add_argument("--planning-root", default=DEFAULT_PLANNING)
    p.add_argument("--output-plane-dryrun-root", default=DEFAULT_OUTPUT_DR)
    p.add_argument("--constitution-dryrun-root", default=DEFAULT_CONSTITUTION_DR)
    p.add_argument("--template-planning-root", default=DEFAULT_TEMPLATE)
    args = p.parse_args()

    result = run_midplatform_user_output_constitution_dryrun_and_review_v1(
        midplatform_user_output_constitution_planning_root=args.planning_root,
        midplatform_output_plane_integration_dryrun_and_review_root=args.output_plane_dryrun_root,
        midplatform_constitution_governance_explanation_dryrun_and_review_root=args.constitution_dryrun_root,
        midplatform_module_definition_template_planning_root=args.template_planning_root,
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
                "dryrun_and_review_pass": sm.get("dryrun_and_review_pass"),
                "final_decision": sm.get("final_decision"),
                "recommended_next_phase": sm.get("recommended_next_phase"),
                "resolver_to_bundle_chain": True,
            },
            ensure_ascii=False,
        )
    )
    return 0 if sm.get("dryrun_and_review_pass") else 1


if __name__ == "__main__":
    raise SystemExit(main())
