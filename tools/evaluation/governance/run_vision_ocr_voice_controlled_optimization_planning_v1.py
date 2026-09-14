#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Vision / OCR / Voice Controlled Optimization Planning v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.vision_ocr_voice_controlled_optimization_planning_v1 import (
    run_vision_ocr_voice_controlled_optimization_planning_v1,
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
DEFAULT_BACKBONE_POST = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/midplatform_minimal_backbone_post_dryrun_review"
)
DEFAULT_FACTORY = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/luna_validation_factory_consolidation"
)
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "vision_ocr_voice_controlled_optimization_planning"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    (
        "vision_ocr_voice_controlled_optimization_planning_policy",
        "vision_ocr_voice_controlled_optimization_planning_policy_v1.json",
    ),
    ("post_health_roadmap_input_review", "post_health_roadmap_input_review_v1.json"),
    ("vision_controlled_optimization_scope", "vision_controlled_optimization_scope_v1.json"),
    ("ocr_controlled_optimization_scope", "ocr_controlled_optimization_scope_v1.json"),
    ("voice_controlled_optimization_scope", "voice_controlled_optimization_scope_v1.json"),
    ("cross_chain_dependency_matrix", "cross_chain_dependency_matrix_v1.json"),
    ("model_registry_binding_plan", "model_registry_binding_plan_v1.json"),
    ("health_management_binding_plan", "health_management_binding_plan_v1.json"),
    ("constitution_boundary_plan", "constitution_boundary_plan_v1.json"),
    ("midplatform_candidate_flow_binding_plan", "midplatform_candidate_flow_binding_plan_v1.json"),
    ("controlled_provider_readiness_matrix", "controlled_provider_readiness_matrix_v1.json"),
    ("vision_controlled_provider_planning", "vision_controlled_provider_planning_v1.json"),
    ("ocr_controlled_provider_planning", "ocr_controlled_provider_planning_v1.json"),
    ("voice_controlled_provider_planning", "voice_controlled_provider_planning_v1.json"),
    ("no_runtime_boundary_matrix", "no_runtime_boundary_matrix_v1.json"),
    ("phased_optimization_roadmap", "phased_optimization_roadmap_v1.json"),
    ("vision_ocr_voice_non_claims_register", "vision_ocr_voice_non_claims_register_v1.json"),
    ("vision_ocr_voice_planning_decision", "vision_ocr_voice_planning_decision_v1.json"),
)


def _write(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=DEFAULT_OUTPUT)
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
    p.add_argument(
        "--midplatform-minimal-backbone-post-dryrun-review-root",
        default=DEFAULT_BACKBONE_POST,
    )
    p.add_argument("--luna-validation-factory-consolidation-root", default=DEFAULT_FACTORY)
    args = p.parse_args()

    result = run_vision_ocr_voice_controlled_optimization_planning_v1(
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
        midplatform_minimal_backbone_post_dryrun_review_root=args.midplatform_minimal_backbone_post_dryrun_review_root,
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
                "ocr_p0_first": sm.get("ocr_p0_first"),
            },
            ensure_ascii=False,
        )
    )
    return 0 if sm.get("boundary_ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
