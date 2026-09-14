#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Post-Health Management Roadmap Decision v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.post_health_management_roadmap_decision_v1 import (
    run_post_health_management_roadmap_decision_v1,
)

DEFAULT_POST_REVIEW = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "health_management_layer_integration_post_dryrun_review"
)
DEFAULT_HEALTH_DRYRUN = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "health_management_layer_integration_dryrun"
)
DEFAULT_CANONICAL_POST = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "model_registry_canonicalization_post_dryrun_review"
)
DEFAULT_MM_POST = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "model_management_layer_recovery_post_dryrun_review"
)
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/post_health_management_roadmap_decision"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    ("post_health_roadmap_decision_policy", "post_health_roadmap_decision_policy_v1.json"),
    ("health_post_review_input_review", "health_post_review_input_review_v1.json"),
    (
        "route_a_vision_ocr_voice_controlled_optimization_assessment",
        "route_a_vision_ocr_voice_controlled_optimization_assessment_v1.json",
    ),
    (
        "route_b_health_metric_baseline_defer_assessment",
        "route_b_health_metric_baseline_defer_assessment_v1.json",
    ),
    (
        "route_c_hardware_lifespan_alert_defer_assessment",
        "route_c_hardware_lifespan_alert_defer_assessment_v1.json",
    ),
    (
        "route_d_robustness_baseline_defer_assessment",
        "route_d_robustness_baseline_defer_assessment_v1.json",
    ),
    ("post_health_route_selection_matrix", "post_health_route_selection_matrix_v1.json"),
    ("selected_route_preconditions", "selected_route_preconditions_v1.json"),
    (
        "deferred_health_metric_hardware_robustness_register",
        "deferred_health_metric_hardware_robustness_register_v1.json",
    ),
    ("next_phase_readiness_decision", "next_phase_readiness_decision_v1.json"),
    ("non_claims_register", "non_claims_register_v1.json"),
)


def _write(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=DEFAULT_OUTPUT)
    p.add_argument(
        "--health-management-layer-integration-post-dryrun-review-root",
        default=DEFAULT_POST_REVIEW,
    )
    p.add_argument(
        "--health-management-layer-integration-dryrun-root",
        default=DEFAULT_HEALTH_DRYRUN,
    )
    p.add_argument(
        "--model-registry-canonicalization-post-dryrun-review-root",
        default=DEFAULT_CANONICAL_POST,
    )
    p.add_argument(
        "--model-management-layer-recovery-post-dryrun-review-root",
        default=DEFAULT_MM_POST,
    )
    args = p.parse_args()

    result = run_post_health_management_roadmap_decision_v1(
        health_management_layer_integration_post_dryrun_review_root=(
            args.health_management_layer_integration_post_dryrun_review_root
        ),
        health_management_layer_integration_dryrun_root=args.health_management_layer_integration_dryrun_root,
        model_registry_canonicalization_post_dryrun_review_root=(
            args.model_registry_canonicalization_post_dryrun_review_root
        ),
        model_management_layer_recovery_post_dryrun_review_root=(
            args.model_management_layer_recovery_post_dryrun_review_root
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
                "selected_route": sm.get("selected_route"),
            },
            ensure_ascii=False,
        )
    )
    return 0 if sm.get("boundary_ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
