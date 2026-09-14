#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Health Management Layer Integration Planning v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.health_management_layer_integration_planning_v1 import (
    run_health_management_layer_integration_planning_v1,
)

DEFAULT_POST_REVIEW = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "model_registry_canonicalization_post_dryrun_review"
)
DEFAULT_CANONICAL_DRYRUN = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/model_registry_canonicalization_dryrun"
)
DEFAULT_MM_POST = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "model_management_layer_recovery_post_dryrun_review"
)
DEFAULT_BACKBONE = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/midplatform_backbone_definition_alignment"
)
DEFAULT_CLEANUP = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/midplatform_structure_cleanup_planning"
)
DEFAULT_ROADMAP = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/model_management_layer_roadmap_decision"
)
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/health_management_layer_integration_planning"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    ("health_management_integration_planning_policy", "health_management_integration_planning_policy_v1.json"),
    ("model_registry_canonical_input_review", "model_registry_canonical_input_review_v1.json"),
    ("health_management_layer_scope", "health_management_layer_scope_v1.json"),
    ("software_health_management_contract", "software_health_management_contract_v1.json"),
    ("hardware_health_management_contract", "hardware_health_management_contract_v1.json"),
    ("system_monitor_contract", "system_monitor_contract_v1.json"),
    ("health_signal_candidate_contract", "health_signal_candidate_contract_v1.json"),
    ("model_health_to_fallback_candidate_plan", "model_health_to_fallback_candidate_plan_v1.json"),
    ("hardware_health_to_degradation_candidate_plan", "hardware_health_to_degradation_candidate_plan_v1.json"),
    ("system_monitor_to_survival_drive_candidate_plan", "system_monitor_to_survival_drive_candidate_plan_v1.json"),
    ("health_to_drive_layer_bridge_plan", "health_to_drive_layer_bridge_plan_v1.json"),
    ("health_runtime_boundary_matrix", "health_runtime_boundary_matrix_v1.json"),
    ("health_management_dryrun_plan", "health_management_dryrun_plan_v1.json"),
    ("health_metric_reserved_policy", "health_metric_reserved_policy_v1.json"),
    ("health_metric_future_definition_plan", "health_metric_future_definition_plan_v1.json"),
    ("health_management_non_claims_register", "health_management_non_claims_register_v1.json"),
    ("health_management_integration_planning_decision", "health_management_integration_planning_decision_v1.json"),
)


def _write(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=DEFAULT_OUTPUT)
    p.add_argument(
        "--model-registry-canonicalization-post-dryrun-review-root",
        default=DEFAULT_POST_REVIEW,
    )
    p.add_argument("--model-registry-canonicalization-dryrun-root", default=DEFAULT_CANONICAL_DRYRUN)
    p.add_argument(
        "--model-management-layer-recovery-post-dryrun-review-root",
        default=DEFAULT_MM_POST,
    )
    p.add_argument("--midplatform-backbone-definition-alignment-root", default=DEFAULT_BACKBONE)
    p.add_argument("--midplatform-structure-cleanup-planning-root", default=DEFAULT_CLEANUP)
    p.add_argument("--model-management-layer-roadmap-decision-root", default=DEFAULT_ROADMAP)
    args = p.parse_args()

    result = run_health_management_layer_integration_planning_v1(
        model_registry_canonicalization_post_dryrun_review_root=(
            args.model_registry_canonicalization_post_dryrun_review_root
        ),
        model_registry_canonicalization_dryrun_root=args.model_registry_canonicalization_dryrun_root,
        model_management_layer_recovery_post_dryrun_review_root=(
            args.model_management_layer_recovery_post_dryrun_review_root
        ),
        midplatform_backbone_definition_alignment_root=args.midplatform_backbone_definition_alignment_root,
        midplatform_structure_cleanup_planning_root=args.midplatform_structure_cleanup_planning_root,
        model_management_layer_roadmap_decision_root=args.model_management_layer_roadmap_decision_root,
        planning_output_root=args.output_root,
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
