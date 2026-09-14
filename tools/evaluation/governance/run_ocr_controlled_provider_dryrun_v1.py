#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run OCR Controlled Provider DryRun v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.ocr_controlled_provider_dryrun_v1 import run_ocr_controlled_provider_dryrun_v1

DEFAULT_PLANNING = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/ocr_controlled_provider_planning"
)
DEFAULT_VOV_POST = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "vision_ocr_voice_controlled_optimization_post_dryrun_review"
)
DEFAULT_VISION_TRIAL = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "vision_sample_frame_single_chain_controlled_trial_post_execution_review"
)
DEFAULT_TASK_POST = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "task_response_candidate_midplatform_integration_post_dryrun_review"
)
DEFAULT_HEALTH_POST = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "health_management_layer_integration_post_dryrun_review"
)
DEFAULT_CANONICAL_POST = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "model_registry_canonicalization_post_dryrun_review"
)
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/ocr_controlled_provider_dryrun"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    ("ocr_controlled_provider_dryrun_policy", "ocr_controlled_provider_dryrun_policy_v1.json"),
    ("ocr_controlled_provider_planning_input_review", "ocr_controlled_provider_planning_input_review_v1.json"),
    ("ocr_provider_readiness_candidate_samples", "ocr_provider_readiness_candidate_samples_v1.json"),
    ("ocr_request_candidate_samples", "ocr_request_candidate_samples_v1.json"),
    ("ocr_roi_candidate_samples", "ocr_roi_candidate_samples_v1.json"),
    ("ocr_result_candidate_samples", "ocr_result_candidate_samples_v1.json"),
    ("ocr_evidence_pack_candidate_samples", "ocr_evidence_pack_candidate_samples_v1.json"),
    ("ocr_candidate_chain_trace", "ocr_candidate_chain_trace_v1.json"),
    ("ocr_timeout_fallback_branch_result", "ocr_timeout_fallback_branch_result_v1.json"),
    ("ocr_low_confidence_branch_result", "ocr_low_confidence_branch_result_v1.json"),
    ("ocr_empty_result_branch_result", "ocr_empty_result_branch_result_v1.json"),
    ("ocr_unsupported_region_branch_result", "ocr_unsupported_region_branch_result_v1.json"),
    ("ocr_runtime_boundary_violation_branch_result", "ocr_runtime_boundary_violation_branch_result_v1.json"),
    ("ocr_health_binding_dryrun_result", "ocr_health_binding_dryrun_result_v1.json"),
    ("ocr_constitution_boundary_dryrun_result", "ocr_constitution_boundary_dryrun_result_v1.json"),
    ("ocr_midplatform_flow_binding_dryrun_result", "ocr_midplatform_flow_binding_dryrun_result_v1.json"),
    ("ocr_no_runtime_boundary_audit", "ocr_no_runtime_boundary_audit_v1.json"),
    ("ocr_blocked_path_result", "ocr_blocked_path_result_v1.json"),
    ("ocr_controlled_provider_dryrun_readiness_decision", "ocr_controlled_provider_dryrun_readiness_decision_v1.json"),
    ("non_claims_register", "non_claims_register_v1.json"),
)


def _write(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=DEFAULT_OUTPUT)
    p.add_argument("--ocr-controlled-provider-planning-root", default=DEFAULT_PLANNING)
    p.add_argument(
        "--vision-ocr-voice-controlled-optimization-post-dryrun-review-root",
        default=DEFAULT_VOV_POST,
    )
    p.add_argument(
        "--vision-sample-frame-single-chain-controlled-trial-post-execution-review-root",
        default=DEFAULT_VISION_TRIAL,
    )
    p.add_argument(
        "--task-response-candidate-midplatform-integration-post-dryrun-review-root",
        default=DEFAULT_TASK_POST,
    )
    p.add_argument(
        "--health-management-layer-integration-post-dryrun-review-root",
        default=DEFAULT_HEALTH_POST,
    )
    p.add_argument(
        "--model-registry-canonicalization-post-dryrun-review-root",
        default=DEFAULT_CANONICAL_POST,
    )
    args = p.parse_args()

    result = run_ocr_controlled_provider_dryrun_v1(
        ocr_controlled_provider_planning_root=args.ocr_controlled_provider_planning_root,
        vision_ocr_voice_controlled_optimization_post_dryrun_review_root=(
            args.vision_ocr_voice_controlled_optimization_post_dryrun_review_root
        ),
        vision_sample_frame_single_chain_controlled_trial_post_execution_review_root=(
            args.vision_sample_frame_single_chain_controlled_trial_post_execution_review_root
        ),
        task_response_candidate_midplatform_integration_post_dryrun_review_root=(
            args.task_response_candidate_midplatform_integration_post_dryrun_review_root
        ),
        health_management_layer_integration_post_dryrun_review_root=(
            args.health_management_layer_integration_post_dryrun_review_root
        ),
        model_registry_canonicalization_post_dryrun_review_root=(
            args.model_registry_canonicalization_post_dryrun_review_root
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
