#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run OCR Controlled Provider Planning v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.ocr_controlled_provider_planning_v1 import run_ocr_controlled_provider_planning_v1

DEFAULT_POST_REVIEW = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "vision_ocr_voice_controlled_optimization_post_dryrun_review"
)
DEFAULT_VOV_DRYRUN = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "vision_ocr_voice_controlled_optimization_dryrun"
)
DEFAULT_CANONICAL_POST = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "model_registry_canonicalization_post_dryrun_review"
)
DEFAULT_MM_POST = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "model_management_layer_recovery_post_dryrun_review"
)
DEFAULT_HEALTH_POST = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "health_management_layer_integration_post_dryrun_review"
)
DEFAULT_TASK_POST = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "task_response_candidate_midplatform_integration_post_dryrun_review"
)
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/ocr_controlled_provider_planning"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    ("ocr_controlled_provider_planning_policy", "ocr_controlled_provider_planning_policy_v1.json"),
    (
        "upstream_controlled_optimization_review_input_review",
        "upstream_controlled_optimization_review_input_review_v1.json",
    ),
    ("ocr_controlled_provider_scope", "ocr_controlled_provider_scope_v1.json"),
    ("ocr_provider_candidate_registry_plan", "ocr_provider_candidate_registry_plan_v1.json"),
    ("ocr_provider_admission_gate_plan", "ocr_provider_admission_gate_plan_v1.json"),
    ("ocr_request_candidate_contract", "ocr_request_candidate_contract_v1.json"),
    ("ocr_roi_candidate_contract", "ocr_roi_candidate_contract_v1.json"),
    ("ocr_result_candidate_contract", "ocr_result_candidate_contract_v1.json"),
    ("ocr_evidence_pack_candidate_contract", "ocr_evidence_pack_candidate_contract_v1.json"),
    ("ocr_timeout_fallback_plan", "ocr_timeout_fallback_plan_v1.json"),
    ("ocr_health_binding_plan", "ocr_health_binding_plan_v1.json"),
    ("ocr_constitution_boundary_plan", "ocr_constitution_boundary_plan_v1.json"),
    ("ocr_midplatform_flow_binding_plan", "ocr_midplatform_flow_binding_plan_v1.json"),
    ("ocr_no_runtime_boundary_matrix", "ocr_no_runtime_boundary_matrix_v1.json"),
    ("ocr_controlled_provider_dryrun_plan", "ocr_controlled_provider_dryrun_plan_v1.json"),
    ("ocr_controlled_provider_non_claims_register", "ocr_controlled_provider_non_claims_register_v1.json"),
    ("ocr_controlled_provider_planning_decision", "ocr_controlled_provider_planning_decision_v1.json"),
)


def _write(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=DEFAULT_OUTPUT)
    p.add_argument(
        "--vision-ocr-voice-controlled-optimization-post-dryrun-review-root",
        default=DEFAULT_POST_REVIEW,
    )
    p.add_argument(
        "--vision-ocr-voice-controlled-optimization-dryrun-root",
        default=DEFAULT_VOV_DRYRUN,
    )
    p.add_argument(
        "--model-registry-canonicalization-post-dryrun-review-root",
        default=DEFAULT_CANONICAL_POST,
    )
    p.add_argument(
        "--model-management-layer-recovery-post-dryrun-review-root",
        default=DEFAULT_MM_POST,
    )
    p.add_argument(
        "--health-management-layer-integration-post-dryrun-review-root",
        default=DEFAULT_HEALTH_POST,
    )
    p.add_argument(
        "--task-response-candidate-midplatform-integration-post-dryrun-review-root",
        default=DEFAULT_TASK_POST,
    )
    args = p.parse_args()

    result = run_ocr_controlled_provider_planning_v1(
        vision_ocr_voice_controlled_optimization_post_dryrun_review_root=(
            args.vision_ocr_voice_controlled_optimization_post_dryrun_review_root
        ),
        vision_ocr_voice_controlled_optimization_dryrun_root=(
            args.vision_ocr_voice_controlled_optimization_dryrun_root
        ),
        model_registry_canonicalization_post_dryrun_review_root=(
            args.model_registry_canonicalization_post_dryrun_review_root
        ),
        model_management_layer_recovery_post_dryrun_review_root=(
            args.model_management_layer_recovery_post_dryrun_review_root
        ),
        health_management_layer_integration_post_dryrun_review_root=(
            args.health_management_layer_integration_post_dryrun_review_root
        ),
        task_response_candidate_midplatform_integration_post_dryrun_review_root=(
            args.task_response_candidate_midplatform_integration_post_dryrun_review_root
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
