#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Provider Harness Generalization Roadmap Decision v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.provider_harness_generalization_roadmap_decision_v1 import (
    run_provider_harness_generalization_roadmap_decision_v1,
)

DEFAULT_POST = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "vision_voice_provider_harness_adoption_post_dryrun_review"
)
DEFAULT_DRYRUN = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "vision_voice_provider_harness_adoption_dryrun"
)
DEFAULT_HARNESS = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/controlled_provider_readiness_harness"
)
DEFAULT_FACTORY = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/luna_validation_factory_consolidation"
)
DEFAULT_PRIOR_ROADMAP = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/ocr_provider_next_roadmap_decision"
)
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/provider_harness_generalization_roadmap_decision"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    ("provider_harness_generalization_roadmap_policy", "provider_harness_generalization_roadmap_policy_v1.json"),
    ("vision_voice_post_review_input_review", "vision_voice_post_review_input_review_v1.json"),
    (
        "controlled_provider_readiness_harness_generalization_review",
        "controlled_provider_readiness_harness_generalization_review_v1.json",
    ),
    (
        "route_a_return_ocr_authorization_assessment",
        "route_a_return_ocr_authorization_assessment_v1.json",
    ),
    (
        "route_b_validation_factory_registration_assessment",
        "route_b_validation_factory_registration_assessment_v1.json",
    ),
    (
        "route_c_future_consumer_adoption_assessment",
        "route_c_future_consumer_adoption_assessment_v1.json",
    ),
    (
        "route_d_visual_context_governance_return_assessment",
        "route_d_visual_context_governance_return_assessment_v1.json",
    ),
    (
        "provider_harness_generalization_route_selection_matrix",
        "provider_harness_generalization_route_selection_matrix_v1.json",
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
        "--vision-voice-provider-harness-adoption-post-dryrun-review-root",
        default=DEFAULT_POST,
    )
    p.add_argument(
        "--vision-voice-provider-harness-adoption-dryrun-root",
        default=DEFAULT_DRYRUN,
    )
    p.add_argument("--controlled-provider-readiness-harness-root", default=DEFAULT_HARNESS)
    p.add_argument("--luna-validation-factory-consolidation-root", default=DEFAULT_FACTORY)
    p.add_argument("--ocr-provider-next-roadmap-decision-root", default=DEFAULT_PRIOR_ROADMAP)
    args = p.parse_args()

    result = run_provider_harness_generalization_roadmap_decision_v1(
        vision_voice_provider_harness_adoption_post_dryrun_review_root=(
            args.vision_voice_provider_harness_adoption_post_dryrun_review_root
        ),
        vision_voice_provider_harness_adoption_dryrun_root=args.vision_voice_provider_harness_adoption_dryrun_root,
        controlled_provider_readiness_harness_root=args.controlled_provider_readiness_harness_root,
        luna_validation_factory_consolidation_root=args.luna_validation_factory_consolidation_root,
        ocr_provider_next_roadmap_decision_root=args.ocr_provider_next_roadmap_decision_root,
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
