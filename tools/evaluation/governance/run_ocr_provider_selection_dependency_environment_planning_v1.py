#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run OCR Provider Selection / Dependency / Environment Planning v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.ocr_provider_selection_dependency_environment_planning_v1 import (
    run_ocr_provider_selection_dependency_environment_planning_v1,
)

DEFAULT_ROADMAP = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "ocr_controlled_provider_authorization_roadmap_decision"
)
DEFAULT_POST_REVIEW = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/ocr_controlled_provider_post_dryrun_review"
)
DEFAULT_DRYRUN = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/ocr_controlled_provider_dryrun"
)
DEFAULT_CANONICAL = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "model_registry_canonicalization_post_dryrun_review"
)
DEFAULT_HEALTH = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "health_management_layer_integration_post_dryrun_review"
)
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "ocr_provider_selection_dependency_environment_planning"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    (
        "ocr_provider_selection_dependency_environment_planning_policy",
        "ocr_provider_selection_dependency_environment_planning_policy_v1.json",
    ),
    ("authorization_roadmap_input_review", "authorization_roadmap_input_review_v1.json"),
    ("ocr_provider_candidate_inventory", "ocr_provider_candidate_inventory_v1.json"),
    ("ocr_provider_selection_criteria", "ocr_provider_selection_criteria_v1.json"),
    ("paddleocr_dependency_readiness_plan", "paddleocr_dependency_readiness_plan_v1.json"),
    ("rapidocr_dependency_readiness_plan", "rapidocr_dependency_readiness_plan_v1.json"),
    ("external_ocr_dependency_readiness_plan", "external_ocr_dependency_readiness_plan_v1.json"),
    ("local_environment_readiness_plan", "local_environment_readiness_plan_v1.json"),
    ("model_file_and_cache_readiness_plan", "model_file_and_cache_readiness_plan_v1.json"),
    ("provider_capability_comparison_matrix", "provider_capability_comparison_matrix_v1.json"),
    ("provider_cost_latency_resource_matrix", "provider_cost_latency_resource_matrix_v1.json"),
    ("provider_health_binding_plan", "provider_health_binding_plan_v1.json"),
    ("provider_fallback_strategy_plan", "provider_fallback_strategy_plan_v1.json"),
    ("provider_security_and_boundary_plan", "provider_security_and_boundary_plan_v1.json"),
    ("provider_selection_dryrun_plan", "provider_selection_dryrun_plan_v1.json"),
    ("ocr_provider_selection_non_claims_register", "ocr_provider_selection_non_claims_register_v1.json"),
    ("ocr_provider_selection_planning_decision", "ocr_provider_selection_planning_decision_v1.json"),
)


def _write(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=DEFAULT_OUTPUT)
    p.add_argument(
        "--ocr-controlled-provider-authorization-roadmap-decision-root",
        default=DEFAULT_ROADMAP,
    )
    p.add_argument("--ocr-controlled-provider-post-dryrun-review-root", default=DEFAULT_POST_REVIEW)
    p.add_argument("--ocr-controlled-provider-dryrun-root", default=DEFAULT_DRYRUN)
    p.add_argument("--model-registry-canonicalization-post-dryrun-review-root", default=DEFAULT_CANONICAL)
    p.add_argument(
        "--health-management-layer-integration-post-dryrun-review-root",
        default=DEFAULT_HEALTH,
    )
    args = p.parse_args()

    result = run_ocr_provider_selection_dependency_environment_planning_v1(
        ocr_controlled_provider_authorization_roadmap_decision_root=(
            args.ocr_controlled_provider_authorization_roadmap_decision_root
        ),
        ocr_controlled_provider_post_dryrun_review_root=args.ocr_controlled_provider_post_dryrun_review_root,
        ocr_controlled_provider_dryrun_root=args.ocr_controlled_provider_dryrun_root,
        model_registry_canonicalization_post_dryrun_review_root=args.model_registry_canonicalization_post_dryrun_review_root,
        health_management_layer_integration_post_dryrun_review_root=(
            args.health_management_layer_integration_post_dryrun_review_root
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
