#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Vision / OCR / Voice Controlled Optimization DryRun v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.vision_ocr_voice_controlled_optimization_dryrun_v1 import (
    run_vision_ocr_voice_controlled_optimization_dryrun_v1,
)

DEFAULT_PLANNING = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "vision_ocr_voice_controlled_optimization_planning"
)
DEFAULT_ROADMAP = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/post_health_management_roadmap_decision"
)
DEFAULT_HEALTH_POST = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "health_management_layer_integration_post_dryrun_review"
)
DEFAULT_CANONICAL_POST = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "model_registry_canonicalization_post_dryrun_review"
)
DEFAULT_MM_POST = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "model_management_layer_recovery_post_dryrun_review"
)
DEFAULT_TASK_POST = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "task_response_candidate_midplatform_integration_post_dryrun_review"
)
DEFAULT_FACTORY = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/luna_validation_factory_consolidation"
)
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "vision_ocr_voice_controlled_optimization_dryrun"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    (
        "vision_ocr_voice_controlled_optimization_dryrun_policy",
        "vision_ocr_voice_controlled_optimization_dryrun_policy_v1.json",
    ),
    (
        "controlled_optimization_planning_input_review",
        "controlled_optimization_planning_input_review_v1.json",
    ),
    ("vision_readiness_candidate_result", "vision_readiness_candidate_result_v1.json"),
    ("ocr_readiness_candidate_result", "ocr_readiness_candidate_result_v1.json"),
    ("voice_readiness_candidate_result", "voice_readiness_candidate_result_v1.json"),
    ("cross_chain_dependency_dryrun_result", "cross_chain_dependency_dryrun_result_v1.json"),
    ("model_registry_binding_dryrun_result", "model_registry_binding_dryrun_result_v1.json"),
    ("health_management_binding_dryrun_result", "health_management_binding_dryrun_result_v1.json"),
    ("constitution_boundary_dryrun_result", "constitution_boundary_dryrun_result_v1.json"),
    ("midplatform_candidate_flow_dryrun_result", "midplatform_candidate_flow_dryrun_result_v1.json"),
    (
        "controlled_provider_readiness_dryrun_matrix",
        "controlled_provider_readiness_dryrun_matrix_v1.json",
    ),
    ("no_runtime_boundary_audit", "no_runtime_boundary_audit_v1.json"),
    ("blocked_path_result", "blocked_path_result_v1.json"),
    ("phased_optimization_readiness_decision", "phased_optimization_readiness_decision_v1.json"),
    ("non_claims_register", "non_claims_register_v1.json"),
)


def _write(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=DEFAULT_OUTPUT)
    p.add_argument(
        "--vision-ocr-voice-controlled-optimization-planning-root",
        default=DEFAULT_PLANNING,
    )
    p.add_argument("--post-health-management-roadmap-decision-root", default=DEFAULT_ROADMAP)
    p.add_argument(
        "--health-management-layer-integration-post-dryrun-review-root",
        default=DEFAULT_HEALTH_POST,
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
        "--task-response-candidate-midplatform-integration-post-dryrun-review-root",
        default=DEFAULT_TASK_POST,
    )
    p.add_argument("--luna-validation-factory-consolidation-root", default=DEFAULT_FACTORY)
    args = p.parse_args()

    result = run_vision_ocr_voice_controlled_optimization_dryrun_v1(
        vision_ocr_voice_controlled_optimization_planning_root=(
            args.vision_ocr_voice_controlled_optimization_planning_root
        ),
        post_health_management_roadmap_decision_root=args.post_health_management_roadmap_decision_root,
        health_management_layer_integration_post_dryrun_review_root=(
            args.health_management_layer_integration_post_dryrun_review_root
        ),
        model_registry_canonicalization_post_dryrun_review_root=(
            args.model_registry_canonicalization_post_dryrun_review_root
        ),
        model_management_layer_recovery_post_dryrun_review_root=(
            args.model_management_layer_recovery_post_dryrun_review_root
        ),
        task_response_candidate_midplatform_integration_post_dryrun_review_root=(
            args.task_response_candidate_midplatform_integration_post_dryrun_review_root
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
            },
            ensure_ascii=False,
        )
    )
    return 0 if sm.get("boundary_ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
