#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Health Management Layer Integration DryRun v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.health_management_layer_integration_dryrun_v1 import (
    run_health_management_layer_integration_dryrun_v1,
)

DEFAULT_PLANNING = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/health_management_layer_integration_planning"
)
DEFAULT_CANONICAL_POST = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/model_registry_canonicalization_post_dryrun_review"
)
DEFAULT_RECOVERY_DRYRUN = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/model_management_layer_recovery_dryrun"
)
DEFAULT_MM_POST = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/model_management_layer_recovery_post_dryrun_review"
)
DEFAULT_BACKBONE = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/midplatform_backbone_definition_alignment"
)
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/health_management_layer_integration_dryrun"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    ("health_management_dryrun_policy", "health_management_dryrun_policy_v1.json"),
    ("health_management_planning_input_review", "health_management_planning_input_review_v1.json"),
    ("model_health_state_consumption_result", "model_health_state_consumption_result_v1.json"),
    ("model_switching_candidate_consumption_result", "model_switching_candidate_consumption_result_v1.json"),
    ("software_health_signal_candidate_samples", "software_health_signal_candidate_samples_v1.json"),
    ("hardware_health_signal_candidate_samples", "hardware_health_signal_candidate_samples_v1.json"),
    ("system_health_signal_candidate_samples", "system_health_signal_candidate_samples_v1.json"),
    ("fallback_candidate_samples", "fallback_candidate_samples_v1.json"),
    ("degradation_candidate_samples", "degradation_candidate_samples_v1.json"),
    ("survival_drive_candidate_samples", "survival_drive_candidate_samples_v1.json"),
    ("recovery_plan_candidate_samples", "recovery_plan_candidate_samples_v1.json"),
    ("health_to_drive_bridge_dryrun_result", "health_to_drive_bridge_dryrun_result_v1.json"),
    ("health_runtime_boundary_audit", "health_runtime_boundary_audit_v1.json"),
    ("health_metric_reserved_dryrun_review", "health_metric_reserved_dryrun_review_v1.json"),
    ("health_management_blocked_path_result", "health_management_blocked_path_result_v1.json"),
    ("health_management_dryrun_readiness_decision", "health_management_dryrun_readiness_decision_v1.json"),
    ("non_claims_register", "non_claims_register_v1.json"),
)


def _write(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=DEFAULT_OUTPUT)
    p.add_argument("--health-management-layer-integration-planning-root", default=DEFAULT_PLANNING)
    p.add_argument(
        "--model-registry-canonicalization-post-dryrun-review-root",
        default=DEFAULT_CANONICAL_POST,
    )
    p.add_argument("--model-management-layer-recovery-dryrun-root", default=DEFAULT_RECOVERY_DRYRUN)
    p.add_argument(
        "--model-management-layer-recovery-post-dryrun-review-root",
        default=DEFAULT_MM_POST,
    )
    p.add_argument("--midplatform-backbone-definition-alignment-root", default=DEFAULT_BACKBONE)
    args = p.parse_args()

    result = run_health_management_layer_integration_dryrun_v1(
        health_management_layer_integration_planning_root=(
            args.health_management_layer_integration_planning_root
        ),
        model_registry_canonicalization_post_dryrun_review_root=(
            args.model_registry_canonicalization_post_dryrun_review_root
        ),
        model_management_layer_recovery_dryrun_root=args.model_management_layer_recovery_dryrun_root,
        model_management_layer_recovery_post_dryrun_review_root=(
            args.model_management_layer_recovery_post_dryrun_review_root
        ),
        midplatform_backbone_definition_alignment_root=args.midplatform_backbone_definition_alignment_root,
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
                "software_signal_count": sm.get("software_signal_count"),
            },
            ensure_ascii=False,
        )
    )
    return 0 if sm.get("boundary_ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
