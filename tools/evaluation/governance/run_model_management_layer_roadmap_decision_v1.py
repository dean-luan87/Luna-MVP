#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Model Management Layer Roadmap Decision v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.model_management_layer_roadmap_decision_v1 import (
    run_model_management_layer_roadmap_decision_v1,
)

DEFAULT_POST_REVIEW = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "model_management_layer_recovery_post_dryrun_review"
)
DEFAULT_DRYRUN = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/model_management_layer_recovery_dryrun"
)
DEFAULT_PLANNING = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/model_management_layer_recovery_planning"
)
DEFAULT_GAP = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/midplatform_module_gap_and_roadmap_planning"
)
DEFAULT_BACKBONE = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/midplatform_backbone_definition_alignment"
)
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/model_management_layer_roadmap_decision"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    ("model_management_roadmap_decision_policy", "model_management_roadmap_decision_policy_v1.json"),
    ("model_management_post_review_input_review", "model_management_post_review_input_review_v1.json"),
    ("route_a_vision_ocr_voice_optimization_assessment", "route_a_vision_ocr_voice_optimization_assessment_v1.json"),
    (
        "route_b_lite_model_registry_canonicalization_assessment",
        "route_b_lite_model_registry_canonicalization_assessment_v1.json",
    ),
    ("route_c_health_management_integration_assessment", "route_c_health_management_integration_assessment_v1.json"),
    ("route_d_skill_registry_expansion_assessment", "route_d_skill_registry_expansion_assessment_v1.json"),
    ("model_management_route_selection_matrix", "model_management_route_selection_matrix_v1.json"),
    ("selected_route_preconditions", "selected_route_preconditions_v1.json"),
    ("deferred_routes_register", "deferred_routes_register_v1.json"),
    ("next_phase_readiness_decision", "next_phase_readiness_decision_v1.json"),
    ("model_registry_versioning_policy", "model_registry_versioning_policy_v1.json"),
    ("non_claims_register", "non_claims_register_v1.json"),
)

MD_OUTPUT = ("model_registry_version_note_v0.md", "model_registry_version_note_v0_md")


def _write(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=DEFAULT_OUTPUT)
    p.add_argument("--model-management-layer-recovery-post-dryrun-review-root", default=DEFAULT_POST_REVIEW)
    p.add_argument("--model-management-layer-recovery-dryrun-root", default=DEFAULT_DRYRUN)
    p.add_argument("--model-management-layer-recovery-planning-root", default=DEFAULT_PLANNING)
    p.add_argument("--midplatform-module-gap-and-roadmap-planning-root", default=DEFAULT_GAP)
    p.add_argument("--midplatform-backbone-definition-alignment-root", default=DEFAULT_BACKBONE)
    args = p.parse_args()

    result = run_model_management_layer_roadmap_decision_v1(
        model_management_layer_recovery_post_dryrun_review_root=(
            args.model_management_layer_recovery_post_dryrun_review_root
        ),
        model_management_layer_recovery_dryrun_root=args.model_management_layer_recovery_dryrun_root,
        model_management_layer_recovery_planning_root=args.model_management_layer_recovery_planning_root,
        midplatform_module_gap_and_roadmap_planning_root=args.midplatform_module_gap_and_roadmap_planning_root,
        midplatform_backbone_definition_alignment_root=args.midplatform_backbone_definition_alignment_root,
        review_output_root=args.output_root,
    )

    out = Path(args.output_root)
    for key, fname in OUTPUT_FILES:
        _write(out / fname, result[key])

    md_fname, md_key = MD_OUTPUT
    (out / md_fname).write_text(result[md_key] + "\n", encoding="utf-8")

    sm = result["summary"]
    print(
        json.dumps(
            {
                "output_root": str(out),
                "boundary_ok": sm.get("boundary_ok"),
                "final_decision": sm.get("final_decision"),
                "recommended_next_phase": sm.get("recommended_next_phase"),
                "selected_route": sm.get("selected_route"),
                "selected_registry_baseline_version": sm.get("selected_registry_baseline_version"),
                "selected_schema_version": sm.get("selected_schema_version"),
            },
            ensure_ascii=False,
        )
    )
    return 0 if sm.get("boundary_ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
