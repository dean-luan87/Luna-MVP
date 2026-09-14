#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Midplatform Whitebox Inspection Integration Planning v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.midplatform_whitebox_inspection_integration_planning_v1 import (
    run_midplatform_whitebox_inspection_integration_planning_v1,
)

DEFAULT_OCR_EXEC = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "ocr_real_dependency_real_minimal_controlled_execution"
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
DEFAULT_OCR_FACTORY = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "ocr_real_dependency_authorization_via_factory_standard_dryrun_and_review"
)
DEFAULT_MINIMAL_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "ocr_real_dependency_minimal_controlled_execution_dryrun_and_review"
)
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_whitebox_inspection_integration_planning"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    ("whitebox_inspection_integration_planning_policy", "whitebox_inspection_integration_planning_policy_v1.json"),
    ("existing_detection_chain_input_review", "existing_detection_chain_input_review_v1.json"),
    ("whitebox_engineering_role_definition", "whitebox_engineering_role_definition_v1.json"),
    ("validation_engineering_absorption_mapping", "validation_engineering_absorption_mapping_v1.json"),
    ("constitution_health_validation_whitebox_mapping", "constitution_health_validation_whitebox_mapping_v1.json"),
    ("factory_authorization_whitebox_mapping", "factory_authorization_whitebox_mapping_v1.json"),
    ("evidence_boundary_traceback_whitebox_mapping", "evidence_boundary_traceback_whitebox_mapping_v1.json"),
    ("global_to_local_inspection_principle", "global_to_local_inspection_principle_v1.json"),
    ("whitebox_inspection_layer_model", "whitebox_inspection_layer_model_v1.json"),
    ("whitebox_drilldown_policy", "whitebox_drilldown_policy_v1.json"),
    ("ocr_real_dep_as_local_evidence_mapping", "ocr_real_dep_as_local_evidence_mapping_v1.json"),
    ("no_parallel_whitebox_policy", "no_parallel_whitebox_policy_v1.json"),
    ("whitebox_integration_dryrun_plan", "whitebox_integration_dryrun_plan_v1.json"),
    ("non_claims_register", "non_claims_register_v1.json"),
    ("whitebox_inspection_integration_planning_decision", "whitebox_inspection_integration_planning_decision_v1.json"),
)


def _write(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=DEFAULT_OUTPUT)
    p.add_argument("--ocr-execution-root", default=DEFAULT_OCR_EXEC)
    p.add_argument("--validation-separation-dryrun-root", default=DEFAULT_VAL)
    p.add_argument("--constitution-explanation-dryrun-root", default=DEFAULT_CONST)
    p.add_argument("--auth-extension-dryrun-root", default=DEFAULT_AUTH_EXT)
    p.add_argument("--ocr-via-factory-dryrun-root", default=DEFAULT_OCR_FACTORY)
    p.add_argument("--minimal-dryrun-root", default=DEFAULT_MINIMAL_DR)
    args = p.parse_args()

    result = run_midplatform_whitebox_inspection_integration_planning_v1(
        ocr_real_dependency_real_minimal_controlled_execution_root=args.ocr_execution_root,
        midplatform_validation_engineering_separation_dryrun_and_review_root=args.validation_separation_dryrun_root,
        midplatform_constitution_governance_explanation_dryrun_and_review_root=args.constitution_explanation_dryrun_root,
        capability_factory_authorization_standard_extension_dryrun_and_review_root=args.auth_extension_dryrun_root,
        ocr_real_dependency_authorization_via_factory_standard_dryrun_and_review_root=args.ocr_via_factory_dryrun_root,
        ocr_real_dependency_minimal_controlled_execution_dryrun_and_review_root=args.minimal_dryrun_root,
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
                "integration_not_rebuild": True,
            },
            ensure_ascii=False,
        )
    )
    return 0 if sm.get("planning_pass") else 1


if __name__ == "__main__":
    raise SystemExit(main())
