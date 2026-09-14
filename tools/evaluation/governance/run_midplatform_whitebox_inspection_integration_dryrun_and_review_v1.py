#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Midplatform Whitebox Inspection Integration DryRunAndReview v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.midplatform_whitebox_inspection_integration_dryrun_and_review_v1 import (
    run_midplatform_whitebox_inspection_integration_dryrun_and_review_v1,
)

DEFAULT_PLANNING = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_whitebox_inspection_integration_planning"
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
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_whitebox_inspection_integration_dryrun_and_review"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    (
        "whitebox_inspection_integration_dryrun_review_policy",
        "whitebox_inspection_integration_dryrun_review_policy_v1.json",
    ),
    (
        "whitebox_integration_planning_input_review",
        "whitebox_integration_planning_input_review_v1.json",
    ),
    ("whitebox_inspection_model_candidate", "whitebox_inspection_model_candidate_v1.json"),
    ("whitebox_visibility_domain_review", "whitebox_visibility_domain_review_v1.json"),
    (
        "validation_engineering_absorption_review",
        "validation_engineering_absorption_review_v1.json",
    ),
    (
        "constitution_health_validation_mapping_review",
        "constitution_health_validation_mapping_review_v1.json",
    ),
    ("factory_authorization_mapping_review", "factory_authorization_mapping_review_v1.json"),
    (
        "evidence_boundary_traceback_mapping_review",
        "evidence_boundary_traceback_mapping_review_v1.json",
    ),
    ("global_to_local_principle_review", "global_to_local_principle_review_v1.json"),
    ("whitebox_layer_model_review", "whitebox_layer_model_review_v1.json"),
    ("whitebox_drilldown_policy_review", "whitebox_drilldown_policy_review_v1.json"),
    ("ocr_real_dep_local_evidence_review", "ocr_real_dep_local_evidence_review_v1.json"),
    ("no_parallel_whitebox_review", "no_parallel_whitebox_review_v1.json"),
    ("whitebox_boundary_audit", "whitebox_boundary_audit_v1.json"),
    ("whitebox_blocked_path_result", "whitebox_blocked_path_result_v1.json"),
    ("whitebox_integration_closure_decision", "whitebox_integration_closure_decision_v1.json"),
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
    p.add_argument("--ocr-execution-root", default=DEFAULT_OCR_EXEC)
    p.add_argument("--validation-separation-dryrun-root", default=DEFAULT_VAL)
    p.add_argument("--constitution-explanation-dryrun-root", default=DEFAULT_CONST)
    p.add_argument("--auth-extension-dryrun-root", default=DEFAULT_AUTH_EXT)
    args = p.parse_args()

    result = run_midplatform_whitebox_inspection_integration_dryrun_and_review_v1(
        midplatform_whitebox_inspection_integration_planning_root=args.planning_root,
        ocr_real_dependency_real_minimal_controlled_execution_root=args.ocr_execution_root,
        midplatform_validation_engineering_separation_dryrun_and_review_root=args.validation_separation_dryrun_root,
        midplatform_constitution_governance_explanation_dryrun_and_review_root=args.constitution_explanation_dryrun_root,
        capability_factory_authorization_standard_extension_dryrun_and_review_root=args.auth_extension_dryrun_root,
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
                "model_candidate_generated": True,
                "no_parallel_whitebox": True,
            },
            ensure_ascii=False,
        )
    )
    return 0 if sm.get("dryrun_and_review_pass") else 1


if __name__ == "__main__":
    raise SystemExit(main())
