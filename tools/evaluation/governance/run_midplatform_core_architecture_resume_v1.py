#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Midplatform Core Architecture Resume v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.midplatform_core_architecture_resume_v1 import (
    run_midplatform_core_architecture_resume_v1,
)

DEFAULT_WHITEBOX_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_whitebox_inspection_integration_dryrun_and_review"
)
DEFAULT_VAL = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_validation_engineering_separation_dryrun_and_review"
)
DEFAULT_CONST = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_constitution_governance_explanation_dryrun_and_review"
)
DEFAULT_AUTH_EXT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "capability_factory_authorization_standard_extension_dryrun_and_review"
)
DEFAULT_OCR_EXEC = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "ocr_real_dependency_real_minimal_controlled_execution"
)
DEFAULT_OCR_READY = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "ocr_real_dependency_real_minimal_controlled_execution_final_ready_check"
)
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/midplatform_core_architecture_resume"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    ("midplatform_core_architecture_resume_policy", "midplatform_core_architecture_resume_policy_v1.json"),
    ("upstream_governance_input_review", "upstream_governance_input_review_v1.json"),
    ("midplatform_core_role_definition", "midplatform_core_role_definition_v1.json"),
    ("midplatform_boundary_definition", "midplatform_boundary_definition_v1.json"),
    ("midplatform_object_flow_model", "midplatform_object_flow_model_v1.json"),
    (
        "candidate_evidence_validation_decision_response_flow",
        "candidate_evidence_validation_decision_response_flow_v1.json",
    ),
    ("decision_center_role_plan", "decision_center_role_plan_v1.json"),
    (
        "constitution_health_validation_consumption_plan",
        "constitution_health_validation_consumption_plan_v1.json",
    ),
    ("factory_validation_market_flow_plan", "factory_validation_market_flow_plan_v1.json"),
    ("domain_config_consumption_plan", "domain_config_consumption_plan_v1.json"),
    (
        "task_response_candidate_integration_plan",
        "task_response_candidate_integration_plan_v1.json",
    ),
    ("evidence_and_traceability_flow_plan", "evidence_and_traceability_flow_plan_v1.json"),
    ("failure_route_and_escalation_plan", "failure_route_and_escalation_plan_v1.json"),
    ("midplatform_runtime_boundary_matrix", "midplatform_runtime_boundary_matrix_v1.json"),
    ("next_mainline_route_decision", "next_mainline_route_decision_v1.json"),
    ("non_claims_register", "non_claims_register_v1.json"),
    (
        "midplatform_core_architecture_resume_decision",
        "midplatform_core_architecture_resume_decision_v1.json",
    ),
)


def _write(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=DEFAULT_OUTPUT)
    p.add_argument("--whitebox-dryrun-root", default=DEFAULT_WHITEBOX_DR)
    p.add_argument("--validation-separation-dryrun-root", default=DEFAULT_VAL)
    p.add_argument("--constitution-explanation-dryrun-root", default=DEFAULT_CONST)
    p.add_argument("--auth-extension-dryrun-root", default=DEFAULT_AUTH_EXT)
    p.add_argument("--ocr-execution-root", default=DEFAULT_OCR_EXEC)
    p.add_argument("--ocr-final-ready-check-root", default=DEFAULT_OCR_READY)
    args = p.parse_args()

    result = run_midplatform_core_architecture_resume_v1(
        midplatform_whitebox_inspection_integration_dryrun_and_review_root=args.whitebox_dryrun_root,
        midplatform_validation_engineering_separation_dryrun_and_review_root=args.validation_separation_dryrun_root,
        midplatform_constitution_governance_explanation_dryrun_and_review_root=args.constitution_explanation_dryrun_root,
        capability_factory_authorization_standard_extension_dryrun_and_review_root=args.auth_extension_dryrun_root,
        ocr_real_dependency_real_minimal_controlled_execution_root=args.ocr_execution_root,
        ocr_real_dependency_real_minimal_controlled_execution_final_ready_check_root=args.ocr_final_ready_check_root,
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
                "resume_pass": sm.get("resume_pass"),
                "final_decision": sm.get("final_decision"),
                "recommended_next_phase": sm.get("recommended_next_phase"),
                "mainline_restored": True,
                "ocr_sealed": True,
            },
            ensure_ascii=False,
        )
    )
    return 0 if sm.get("resume_pass") else 1


if __name__ == "__main__":
    raise SystemExit(main())
