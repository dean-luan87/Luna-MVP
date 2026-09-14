#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run OCR Real Dependency Formal Execution Request Generation Planning v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.ocr_real_dependency_formal_execution_request_generation_planning_v1 import (
    run_ocr_real_dependency_formal_execution_request_generation_planning_v1,
)

DEFAULT_ROADMAP = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "ocr_real_dependency_execution_request_generation_roadmap_decision"
)
DEFAULT_DRYRUN = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "ocr_real_dependency_execution_authorization_dryrun_and_review"
)
DEFAULT_PLAN = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "ocr_real_dependency_execution_authorization_planning"
)
DEFAULT_OCR_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "ocr_real_dependency_authorization_via_factory_standard_dryrun_and_review"
)
DEFAULT_VAL_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_validation_engineering_separation_dryrun_and_review"
)
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "ocr_real_dependency_formal_execution_request_generation_planning"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    (
        "formal_execution_request_generation_planning_policy",
        "formal_execution_request_generation_planning_policy_v1.json",
    ),
    (
        "execution_request_generation_roadmap_input_review",
        "execution_request_generation_roadmap_input_review_v1.json",
    ),
    (
        "formal_execution_request_artifact_schema",
        "formal_execution_request_artifact_schema_v1.json",
    ),
    (
        "formal_execution_request_generation_precondition",
        "formal_execution_request_generation_precondition_v1.json",
    ),
    (
        "formal_execution_request_field_source_map",
        "formal_execution_request_field_source_map_v1.json",
    ),
    (
        "formal_execution_request_validation_rule",
        "formal_execution_request_validation_rule_v1.json",
    ),
    (
        "formal_execution_request_versioning_policy",
        "formal_execution_request_versioning_policy_v1.json",
    ),
    (
        "formal_execution_request_signature_approval_placeholder",
        "formal_execution_request_signature_approval_placeholder_v1.json",
    ),
    (
        "formal_execution_request_storage_boundary_plan",
        "formal_execution_request_storage_boundary_plan_v1.json",
    ),
    (
        "formal_execution_request_send_boundary_plan",
        "formal_execution_request_send_boundary_plan_v1.json",
    ),
    (
        "formal_execution_request_evidence_binding_plan",
        "formal_execution_request_evidence_binding_plan_v1.json",
    ),
    (
        "formal_execution_request_validation_gate_binding_plan",
        "formal_execution_request_validation_gate_binding_plan_v1.json",
    ),
    (
        "formal_execution_request_blocked_path_matrix",
        "formal_execution_request_blocked_path_matrix_v1.json",
    ),
    ("formal_execution_request_dryrun_plan", "formal_execution_request_dryrun_plan_v1.json"),
    ("non_claims_register", "non_claims_register_v1.json"),
    (
        "formal_execution_request_generation_planning_decision",
        "formal_execution_request_generation_planning_decision_v1.json",
    ),
)


def _write(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=DEFAULT_OUTPUT)
    p.add_argument(
        "--ocr-real-dependency-execution-request-generation-roadmap-decision-root",
        default=DEFAULT_ROADMAP,
    )
    p.add_argument(
        "--ocr-real-dependency-execution-authorization-dryrun-and-review-root",
        default=DEFAULT_DRYRUN,
    )
    p.add_argument(
        "--ocr-real-dependency-execution-authorization-planning-root",
        default=DEFAULT_PLAN,
    )
    p.add_argument(
        "--ocr-real-dependency-authorization-via-factory-standard-dryrun-and-review-root",
        default=DEFAULT_OCR_DR,
    )
    p.add_argument(
        "--midplatform-validation-engineering-separation-dryrun-and-review-root",
        default=DEFAULT_VAL_DR,
    )
    args = p.parse_args()

    result = run_ocr_real_dependency_formal_execution_request_generation_planning_v1(
        ocr_real_dependency_execution_request_generation_roadmap_decision_root=(
            args.ocr_real_dependency_execution_request_generation_roadmap_decision_root
        ),
        ocr_real_dependency_execution_authorization_dryrun_and_review_root=(
            args.ocr_real_dependency_execution_authorization_dryrun_and_review_root
        ),
        ocr_real_dependency_execution_authorization_planning_root=(
            args.ocr_real_dependency_execution_authorization_planning_root
        ),
        ocr_real_dependency_authorization_via_factory_standard_dryrun_and_review_root=(
            args.ocr_real_dependency_authorization_via_factory_standard_dryrun_and_review_root
        ),
        midplatform_validation_engineering_separation_dryrun_and_review_root=(
            args.midplatform_validation_engineering_separation_dryrun_and_review_root
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
