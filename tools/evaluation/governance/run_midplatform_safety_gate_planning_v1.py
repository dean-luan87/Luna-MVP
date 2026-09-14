#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Midplatform Safety Gate Planning v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.midplatform_safety_gate_planning_v1 import (
    run_midplatform_safety_gate_planning_v1,
)

DEFAULT_UO_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_user_output_constitution_dryrun_and_review"
)
DEFAULT_OUTPUT_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_output_plane_integration_dryrun_and_review"
)
DEFAULT_OUTPUT_PLAN = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_output_plane_integration_planning"
)
DEFAULT_TEMPLATE = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_module_definition_template_planning"
)
DEFAULT_CONSTITUTION_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_constitution_governance_explanation_dryrun_and_review"
)
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/midplatform_safety_gate_planning"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    ("safety_gate_planning_policy", "safety_gate_planning_policy_v1.json"),
    ("user_output_constitution_input_review", "user_output_constitution_input_review_v1.json"),
    ("safety_gate_module_definition", "safety_gate_module_definition_v1.json"),
    (
        "safety_gate_constraint_bundle_intake_contract",
        "safety_gate_constraint_bundle_intake_contract_v1.json",
    ),
    (
        "safety_gate_user_output_candidate_intake_contract",
        "safety_gate_user_output_candidate_intake_contract_v1.json",
    ),
    ("safety_gate_result_candidate_contract", "safety_gate_result_candidate_contract_v1.json"),
    ("safety_gate_action_taxonomy", "safety_gate_action_taxonomy_v1.json"),
    ("safety_gate_rule_application_plan", "safety_gate_rule_application_plan_v1.json"),
    ("safety_gate_uncertainty_risk_policy", "safety_gate_uncertainty_risk_policy_v1.json"),
    ("safety_gate_channel_boundary_plan", "safety_gate_channel_boundary_plan_v1.json"),
    ("safety_gate_refusal_hold_degrade_plan", "safety_gate_refusal_hold_degrade_plan_v1.json"),
    ("safety_gate_traceability_plan", "safety_gate_traceability_plan_v1.json"),
    ("safety_gate_downstream_handoff_plan", "safety_gate_downstream_handoff_plan_v1.json"),
    (
        "safety_gate_no_raw_constitution_binding_policy",
        "safety_gate_no_raw_constitution_binding_policy_v1.json",
    ),
    ("safety_gate_boundary_matrix", "safety_gate_boundary_matrix_v1.json"),
    ("safety_gate_dryrun_plan", "safety_gate_dryrun_plan_v1.json"),
    ("non_claims_register", "non_claims_register_v1.json"),
    ("safety_gate_planning_decision", "safety_gate_planning_decision_v1.json"),
)


def _write(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=DEFAULT_OUTPUT)
    p.add_argument("--user-output-constitution-dryrun-root", default=DEFAULT_UO_DR)
    p.add_argument("--output-plane-dryrun-root", default=DEFAULT_OUTPUT_DR)
    p.add_argument("--output-plane-planning-root", default=DEFAULT_OUTPUT_PLAN)
    p.add_argument("--template-planning-root", default=DEFAULT_TEMPLATE)
    p.add_argument("--constitution-dryrun-root", default=DEFAULT_CONSTITUTION_DR)
    args = p.parse_args()

    result = run_midplatform_safety_gate_planning_v1(
        midplatform_user_output_constitution_dryrun_and_review_root=args.user_output_constitution_dryrun_root,
        midplatform_output_plane_integration_dryrun_and_review_root=args.output_plane_dryrun_root,
        midplatform_output_plane_integration_planning_root=args.output_plane_planning_root,
        midplatform_module_definition_template_planning_root=args.template_planning_root,
        midplatform_constitution_governance_explanation_dryrun_and_review_root=args.constitution_dryrun_root,
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
                "planning_pass": sm.get("planning_pass"),
                "final_decision": sm.get("final_decision"),
                "recommended_next_phase": sm.get("recommended_next_phase"),
                "bundle_only_gate": True,
            },
            ensure_ascii=False,
        )
    )
    return 0 if sm.get("planning_pass") else 1


if __name__ == "__main__":
    raise SystemExit(main())
