#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Midplatform Candidate Evidence Flow Integration Planning v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.midplatform_candidate_evidence_flow_integration_planning_v1 import (
    run_midplatform_candidate_evidence_flow_integration_planning_v1,
)

DEFAULT_DC_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_decision_center_module_dryrun_and_review"
)
DEFAULT_TEMPLATE = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_module_definition_template_planning"
)
DEFAULT_CORE = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/midplatform_core_architecture_resume"
)
DEFAULT_VAL = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_validation_engineering_separation_dryrun_and_review"
)
DEFAULT_WHITEBOX = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_whitebox_inspection_integration_dryrun_and_review"
)
DEFAULT_HEALTH = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "health_management_layer_integration_post_dryrun_review"
)
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_candidate_evidence_flow_integration_planning"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    (
        "candidate_evidence_flow_integration_planning_policy",
        "candidate_evidence_flow_integration_planning_policy_v1.json",
    ),
    ("upstream_decision_center_input_review", "upstream_decision_center_input_review_v1.json"),
    ("module_template_compliance_review", "module_template_compliance_review_v1.json"),
    ("candidate_evidence_flow_module_definition", "candidate_evidence_flow_module_definition_v1.json"),
    ("upstream_candidate_intake_contract", "upstream_candidate_intake_contract_v1.json"),
    ("domain_config_intake_contract", "domain_config_intake_contract_v1.json"),
    ("evidence_pack_binding_contract", "evidence_pack_binding_contract_v1.json"),
    ("validation_result_binding_contract", "validation_result_binding_contract_v1.json"),
    ("health_signal_binding_contract", "health_signal_binding_contract_v1.json"),
    ("whitebox_visibility_binding_contract", "whitebox_visibility_binding_contract_v1.json"),
    ("issue_trace_violation_binding_contract", "issue_trace_violation_binding_contract_v1.json"),
    ("decision_request_assembly_contract", "decision_request_assembly_contract_v1.json"),
    ("candidate_evidence_flow_integrity_policy", "candidate_evidence_flow_integrity_policy_v1.json"),
    (
        "stale_missing_conflicting_evidence_policy",
        "stale_missing_conflicting_evidence_policy_v1.json",
    ),
    ("candidate_evidence_flow_boundary_matrix", "candidate_evidence_flow_boundary_matrix_v1.json"),
    ("candidate_evidence_flow_dryrun_plan", "candidate_evidence_flow_dryrun_plan_v1.json"),
    ("non_claims_register", "non_claims_register_v1.json"),
    (
        "candidate_evidence_flow_integration_planning_decision",
        "candidate_evidence_flow_integration_planning_decision_v1.json",
    ),
)


def _write(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=DEFAULT_OUTPUT)
    p.add_argument("--decision-center-dryrun-root", default=DEFAULT_DC_DR)
    p.add_argument("--template-planning-root", default=DEFAULT_TEMPLATE)
    p.add_argument("--core-resume-root", default=DEFAULT_CORE)
    p.add_argument("--validation-dryrun-root", default=DEFAULT_VAL)
    p.add_argument("--whitebox-dryrun-root", default=DEFAULT_WHITEBOX)
    p.add_argument("--health-post-dryrun-root", default=DEFAULT_HEALTH)
    args = p.parse_args()

    result = run_midplatform_candidate_evidence_flow_integration_planning_v1(
        midplatform_decision_center_module_dryrun_and_review_root=args.decision_center_dryrun_root,
        midplatform_module_definition_template_planning_root=args.template_planning_root,
        midplatform_core_architecture_resume_root=args.core_resume_root,
        midplatform_validation_engineering_separation_dryrun_and_review_root=args.validation_dryrun_root,
        midplatform_whitebox_inspection_integration_dryrun_and_review_root=args.whitebox_dryrun_root,
        health_management_layer_integration_post_dryrun_review_root=args.health_post_dryrun_root,
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
                "flow_integration_not_decision": True,
            },
            ensure_ascii=False,
        )
    )
    return 0 if sm.get("planning_pass") else 1


if __name__ == "__main__":
    raise SystemExit(main())
