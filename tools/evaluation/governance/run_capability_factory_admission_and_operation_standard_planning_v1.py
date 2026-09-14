#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Capability Factory Admission and Operation Standard Planning v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.capability_factory_admission_and_operation_standard_planning_v1 import (
    run_capability_factory_admission_and_operation_standard_planning_v1,
)

DEFAULT_REQ_POST = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "ocr_provider_authorization_request_post_dryrun_review"
)
DEFAULT_REQ_DRYRUN = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "ocr_provider_authorization_request_dryrun"
)
DEFAULT_AUTH_PLANNING = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/ocr_provider_authorization_planning"
)
DEFAULT_FACTORY_POST = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "controlled_provider_readiness_harness_factory_registration_post_dryrun_review"
)
DEFAULT_HARNESS = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/controlled_provider_readiness_harness"
)
DEFAULT_VISION_VOICE_POST = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "vision_voice_provider_harness_adoption_post_dryrun_review"
)
DEFAULT_VALIDATION_FACTORY = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/luna_validation_factory_consolidation"
)
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "capability_factory_admission_and_operation_standard_planning"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    (
        "capability_factory_standard_planning_policy",
        "capability_factory_standard_planning_policy_v1.json",
    ),
    ("source_phase_rule_inventory", "source_phase_rule_inventory_v1.json"),
    ("candidate_standard_plan", "candidate_standard_plan_v1.json"),
    ("artifact_standard_plan", "artifact_standard_plan_v1.json"),
    ("lifecycle_standard_plan", "lifecycle_standard_plan_v1.json"),
    ("boundary_standard_plan", "boundary_standard_plan_v1.json"),
    ("evidence_standard_plan", "evidence_standard_plan_v1.json"),
    ("approval_grant_standard_plan", "approval_grant_standard_plan_v1.json"),
    ("sandbox_rollback_standard_plan", "sandbox_rollback_standard_plan_v1.json"),
    ("provider_machine_standard_plan", "provider_machine_standard_plan_v1.json"),
    (
        "upstream_downstream_transfer_standard_plan",
        "upstream_downstream_transfer_standard_plan_v1.json",
    ),
    (
        "factory_role_responsibility_standard_plan",
        "factory_role_responsibility_standard_plan_v1.json",
    ),
    ("factory_standard_contract_outline", "factory_standard_contract_outline_v1.json"),
    ("factory_standard_adoption_plan", "factory_standard_adoption_plan_v1.json"),
    ("compression_impact_assessment", "compression_impact_assessment_v1.json"),
    ("non_claims_register", "non_claims_register_v1.json"),
    (
        "capability_factory_standard_planning_decision",
        "capability_factory_standard_planning_decision_v1.json",
    ),
)


def _write(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=DEFAULT_OUTPUT)
    p.add_argument(
        "--ocr-provider-authorization-request-post-dryrun-review-root",
        default=DEFAULT_REQ_POST,
    )
    p.add_argument(
        "--ocr-provider-authorization-request-dryrun-root",
        default=DEFAULT_REQ_DRYRUN,
    )
    p.add_argument(
        "--ocr-provider-authorization-planning-root",
        default=DEFAULT_AUTH_PLANNING,
    )
    p.add_argument(
        "--controlled-provider-readiness-harness-factory-registration-post-dryrun-review-root",
        default=DEFAULT_FACTORY_POST,
    )
    p.add_argument(
        "--controlled-provider-readiness-harness-root",
        default=DEFAULT_HARNESS,
    )
    p.add_argument(
        "--vision-voice-provider-harness-adoption-post-dryrun-review-root",
        default=DEFAULT_VISION_VOICE_POST,
    )
    p.add_argument(
        "--luna-validation-factory-consolidation-root",
        default=DEFAULT_VALIDATION_FACTORY,
    )
    args = p.parse_args()

    result = run_capability_factory_admission_and_operation_standard_planning_v1(
        ocr_provider_authorization_request_post_dryrun_review_root=(
            args.ocr_provider_authorization_request_post_dryrun_review_root
        ),
        ocr_provider_authorization_request_dryrun_root=args.ocr_provider_authorization_request_dryrun_root,
        ocr_provider_authorization_planning_root=args.ocr_provider_authorization_planning_root,
        controlled_provider_readiness_harness_factory_registration_post_dryrun_review_root=(
            args.controlled_provider_readiness_harness_factory_registration_post_dryrun_review_root
        ),
        controlled_provider_readiness_harness_root=args.controlled_provider_readiness_harness_root,
        vision_voice_provider_harness_adoption_post_dryrun_review_root=(
            args.vision_voice_provider_harness_adoption_post_dryrun_review_root
        ),
        luna_validation_factory_consolidation_root=args.luna_validation_factory_consolidation_root,
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
                "standard_id": sm.get("standard_id"),
            },
            ensure_ascii=False,
        )
    )
    return 0 if sm.get("boundary_ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
