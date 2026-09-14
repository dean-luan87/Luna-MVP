#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run OCR Provider Authorization Return Roadmap Decision v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.ocr_provider_authorization_return_roadmap_decision_v1 import (
    run_ocr_provider_authorization_return_roadmap_decision_v1,
)

DEFAULT_FACTORY_POST = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "controlled_provider_readiness_harness_factory_registration_post_dryrun_review"
)
DEFAULT_FACTORY_DRYRUN = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "controlled_provider_readiness_harness_factory_registration_dryrun"
)
DEFAULT_ROADMAP = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/provider_harness_generalization_roadmap_decision"
)
DEFAULT_REAL_POST = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "ocr_provider_real_dependency_check_post_dryrun_review"
)
DEFAULT_SEL_POST = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "ocr_provider_selection_dependency_environment_post_dryrun_review"
)
DEFAULT_OCR_POST = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/ocr_controlled_provider_post_dryrun_review"
)
DEFAULT_HARNESS = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/controlled_provider_readiness_harness"
)
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/ocr_provider_authorization_return_roadmap_decision"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    ("ocr_authorization_return_roadmap_policy", "ocr_authorization_return_roadmap_policy_v1.json"),
    (
        "factory_registration_post_review_input_review",
        "factory_registration_post_review_input_review_v1.json",
    ),
    ("ocr_provider_chain_readiness_review", "ocr_provider_chain_readiness_review_v1.json"),
    (
        "route_a_ocr_provider_authorization_planning_assessment",
        "route_a_ocr_provider_authorization_planning_assessment_v1.json",
    ),
    (
        "route_b_real_dependency_check_authorization_assessment",
        "route_b_real_dependency_check_authorization_assessment_v1.json",
    ),
    (
        "route_c_provider_selection_finalize_assessment",
        "route_c_provider_selection_finalize_assessment_v1.json",
    ),
    (
        "route_d_return_to_visual_context_governance_assessment",
        "route_d_return_to_visual_context_governance_assessment_v1.json",
    ),
    (
        "ocr_authorization_return_route_selection_matrix",
        "ocr_authorization_return_route_selection_matrix_v1.json",
    ),
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
    p.add_argument(
        "--controlled-provider-readiness-harness-factory-registration-post-dryrun-review-root",
        default=DEFAULT_FACTORY_POST,
    )
    p.add_argument(
        "--controlled-provider-readiness-harness-factory-registration-dryrun-root",
        default=DEFAULT_FACTORY_DRYRUN,
    )
    p.add_argument(
        "--provider-harness-generalization-roadmap-decision-root",
        default=DEFAULT_ROADMAP,
    )
    p.add_argument(
        "--ocr-provider-real-dependency-check-post-dryrun-review-root",
        default=DEFAULT_REAL_POST,
    )
    p.add_argument(
        "--ocr-provider-selection-dependency-environment-post-dryrun-review-root",
        default=DEFAULT_SEL_POST,
    )
    p.add_argument("--ocr-controlled-provider-post-dryrun-review-root", default=DEFAULT_OCR_POST)
    p.add_argument("--controlled-provider-readiness-harness-root", default=DEFAULT_HARNESS)
    args = p.parse_args()

    result = run_ocr_provider_authorization_return_roadmap_decision_v1(
        controlled_provider_readiness_harness_factory_registration_post_dryrun_review_root=(
            args.controlled_provider_readiness_harness_factory_registration_post_dryrun_review_root
        ),
        controlled_provider_readiness_harness_factory_registration_dryrun_root=(
            args.controlled_provider_readiness_harness_factory_registration_dryrun_root
        ),
        provider_harness_generalization_roadmap_decision_root=(
            args.provider_harness_generalization_roadmap_decision_root
        ),
        ocr_provider_real_dependency_check_post_dryrun_review_root=(
            args.ocr_provider_real_dependency_check_post_dryrun_review_root
        ),
        ocr_provider_selection_dependency_environment_post_dryrun_review_root=(
            args.ocr_provider_selection_dependency_environment_post_dryrun_review_root
        ),
        ocr_controlled_provider_post_dryrun_review_root=args.ocr_controlled_provider_post_dryrun_review_root,
        controlled_provider_readiness_harness_root=args.controlled_provider_readiness_harness_root,
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
