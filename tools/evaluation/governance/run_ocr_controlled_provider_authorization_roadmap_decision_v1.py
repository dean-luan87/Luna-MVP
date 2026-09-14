#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run OCR Controlled Provider Authorization Roadmap Decision v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.ocr_controlled_provider_authorization_roadmap_decision_v1 import (
    run_ocr_controlled_provider_authorization_roadmap_decision_v1,
)

DEFAULT_POST_REVIEW = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/ocr_controlled_provider_post_dryrun_review"
)
DEFAULT_DRYRUN = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/ocr_controlled_provider_dryrun"
)
DEFAULT_PLANNING = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/ocr_controlled_provider_planning"
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
    "ocr_controlled_provider_authorization_roadmap_decision"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    ("ocr_authorization_roadmap_decision_policy", "ocr_authorization_roadmap_decision_policy_v1.json"),
    ("ocr_post_dryrun_review_input_review", "ocr_post_dryrun_review_input_review_v1.json"),
    ("route_a_provider_authorization_planning_assessment", "route_a_provider_authorization_planning_assessment_v1.json"),
    (
        "route_b_provider_selection_dependency_environment_assessment",
        "route_b_provider_selection_dependency_environment_assessment_v1.json",
    ),
    ("route_c_controlled_trial_planning_assessment", "route_c_controlled_trial_planning_assessment_v1.json"),
    ("route_d_defer_ocr_provider_assessment", "route_d_defer_ocr_provider_assessment_v1.json"),
    ("ocr_authorization_route_selection_matrix", "ocr_authorization_route_selection_matrix_v1.json"),
    ("selected_route_preconditions", "selected_route_preconditions_v1.json"),
    ("deferred_routes_register", "deferred_routes_register_v1.json"),
    ("next_phase_readiness_decision", "next_phase_readiness_decision_v1.json"),
    ("non_claims_register", "non_claims_register_v1.json"),
)


def _write(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=DEFAULT_OUTPUT)
    p.add_argument("--ocr-controlled-provider-post-dryrun-review-root", default=DEFAULT_POST_REVIEW)
    p.add_argument("--ocr-controlled-provider-dryrun-root", default=DEFAULT_DRYRUN)
    p.add_argument("--ocr-controlled-provider-planning-root", default=DEFAULT_PLANNING)
    p.add_argument("--model-registry-canonicalization-post-dryrun-review-root", default=DEFAULT_CANONICAL)
    p.add_argument(
        "--health-management-layer-integration-post-dryrun-review-root",
        default=DEFAULT_HEALTH,
    )
    args = p.parse_args()

    result = run_ocr_controlled_provider_authorization_roadmap_decision_v1(
        ocr_controlled_provider_post_dryrun_review_root=args.ocr_controlled_provider_post_dryrun_review_root,
        ocr_controlled_provider_dryrun_root=args.ocr_controlled_provider_dryrun_root,
        ocr_controlled_provider_planning_root=args.ocr_controlled_provider_planning_root,
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
                "selected_route": sm.get("selected_route"),
            },
            ensure_ascii=False,
        )
    )
    return 0 if sm.get("boundary_ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
