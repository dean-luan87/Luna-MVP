#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Gate Taxonomy and Requirement Framework Planning v1 (planning-only)."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any, Dict

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.gate_taxonomy_and_requirement_framework_planning_v1 import (
    run_gate_taxonomy_and_requirement_framework_planning_v1,
)

DEFAULT_OUTPUT_WORKSPACE_ROOT = REPO_ROOT
DEFAULT_OUTPUT_ROOT = (
    DEFAULT_OUTPUT_WORKSPACE_ROOT / "_eval_out" / "gate_taxonomy_and_requirement_framework_planning_v1_smoke_v0"
)

# Historical inputs may remain under Luna-Workspace-Min (read-only).
DEFAULT_INPUT_WORKSPACE_ROOT = Path("/Users/luanlei/Desktop/Luna-Workspace-Min")


def _write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Gate Taxonomy and Requirement Framework Planning v1")
    parser.add_argument("--output-root", default=str(DEFAULT_OUTPUT_ROOT))

    # Roadmap decision is in Luna-Core.
    parser.add_argument(
        "--post-file-stat-roadmap-decision-root",
        default=str(DEFAULT_OUTPUT_WORKSPACE_ROOT / "_eval_out" / "post_file_stat_roadmap_decision_v1_smoke_v0"),
    )

    # File stat/existence outputs are in Luna-Core.
    parser.add_argument(
        "--file-stat-guarded-closure-root",
        default=str(DEFAULT_OUTPUT_WORKSPACE_ROOT / "_eval_out" / "controlled_frame_file_stat_guarded_closure_v1_smoke_v0"),
    )
    parser.add_argument(
        "--file-existence-check-guarded-closure-root",
        default=str(
            DEFAULT_OUTPUT_WORKSPACE_ROOT / "_eval_out" / "controlled_frame_file_existence_check_guarded_closure_v1_smoke_v0"
        ),
    )

    # Historical inputs remain in Luna-Workspace-Min (read-only).
    parser.add_argument(
        "--file-metadata-boundary-closure-root",
        default=str(DEFAULT_INPUT_WORKSPACE_ROOT / "_eval_out" / "controlled_frame_file_metadata_boundary_closure_v1_smoke_v0"),
    )
    parser.add_argument(
        "--controlled-frame-sample-closure-root",
        default=str(DEFAULT_INPUT_WORKSPACE_ROOT / "_eval_out" / "controlled_frame_sample_closure_v1_smoke_v0"),
    )
    parser.add_argument(
        "--controlled-frame-input-closure-root",
        default=str(DEFAULT_INPUT_WORKSPACE_ROOT / "_eval_out" / "controlled_frame_input_closure_v1_smoke_v0"),
    )
    parser.add_argument(
        "--crossing-decision-closure-root",
        default=str(DEFAULT_INPUT_WORKSPACE_ROOT / "_eval_out" / "crossing_decision_closure_v1_smoke_v0"),
    )
    parser.add_argument(
        "--safety-constitution-root",
        default=str(DEFAULT_INPUT_WORKSPACE_ROOT / "_eval_out" / "luna_safety_constitution_policy_v1_smoke_v0"),
    )
    parser.add_argument(
        "--map-location-readonly-context-root",
        default=str(DEFAULT_INPUT_WORKSPACE_ROOT / "_eval_out" / "map_location_readonly_context_policy_v1_smoke_v0"),
    )
    parser.add_argument(
        "--minimal-runtime-integration-closure-root",
        default=str(DEFAULT_INPUT_WORKSPACE_ROOT / "_eval_out" / "minimal_runtime_integration_closure_v1_smoke_v0"),
    )
    parser.add_argument(
        "--ocr-final-closure-root",
        default=str(DEFAULT_INPUT_WORKSPACE_ROOT / "_eval_out" / "ocr_mainline_final_closure_v1_smoke_v0"),
    )

    # Optional roots (best-effort)
    parser.add_argument(
        "--ocr-activation-governance-policy-root",
        default=str(DEFAULT_INPUT_WORKSPACE_ROOT / "_eval_out" / "ocr_activation_governance_policy_v1_smoke_v0"),
    )
    parser.add_argument(
        "--basic-navigation-loop-vision-strengthening-closure-root",
        default=str(DEFAULT_INPUT_WORKSPACE_ROOT / "_eval_out" / "basic_navigation_loop_vision_strengthening_closure_v1_smoke_v0"),
    )
    parser.add_argument(
        "--visual-ocr-map-task-feedback-dryrun-root",
        default=str(DEFAULT_INPUT_WORKSPACE_ROOT / "_eval_out" / "visual_ocr_map_task_feedback_dryrun_v1_smoke_v0"),
    )
    parser.add_argument(
        "--midplatform-perception-orchestration-policy-root",
        default=str(DEFAULT_INPUT_WORKSPACE_ROOT / "_eval_out" / "midplatform_perception_orchestration_policy_v1_smoke_v0"),
    )
    parser.add_argument(
        "--task-aware-visual-focus-policy-root",
        default=str(DEFAULT_INPUT_WORKSPACE_ROOT / "_eval_out" / "task_aware_visual_focus_policy_v1_smoke_v0"),
    )
    parser.add_argument(
        "--world-observation-and-entity-feature-policy-root",
        default=str(DEFAULT_INPUT_WORKSPACE_ROOT / "_eval_out" / "world_observation_and_entity_feature_policy_v1_smoke_v0"),
    )
    parser.add_argument(
        "--selective-tracking-adapter-policy-root",
        default=str(DEFAULT_INPUT_WORKSPACE_ROOT / "_eval_out" / "selective_tracking_adapter_policy_v1_smoke_v0"),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    result = run_gate_taxonomy_and_requirement_framework_planning_v1(
        post_file_stat_roadmap_decision_root=args.post_file_stat_roadmap_decision_root,
        file_stat_guarded_closure_root=args.file_stat_guarded_closure_root,
        file_existence_check_guarded_closure_root=args.file_existence_check_guarded_closure_root,
        file_metadata_boundary_closure_root=args.file_metadata_boundary_closure_root,
        controlled_frame_sample_closure_root=args.controlled_frame_sample_closure_root,
        controlled_frame_input_closure_root=args.controlled_frame_input_closure_root,
        crossing_decision_closure_root=args.crossing_decision_closure_root,
        safety_constitution_root=args.safety_constitution_root,
        map_location_readonly_context_root=args.map_location_readonly_context_root,
        minimal_runtime_integration_closure_root=args.minimal_runtime_integration_closure_root,
        ocr_final_closure_root=args.ocr_final_closure_root,
        ocr_activation_governance_policy_root=args.ocr_activation_governance_policy_root,
        basic_navigation_loop_vision_strengthening_closure_root=args.basic_navigation_loop_vision_strengthening_closure_root,
        visual_ocr_map_task_feedback_dryrun_root=args.visual_ocr_map_task_feedback_dryrun_root,
        midplatform_perception_orchestration_policy_root=args.midplatform_perception_orchestration_policy_root,
        task_aware_visual_focus_policy_root=args.task_aware_visual_focus_policy_root,
        world_observation_and_entity_feature_policy_root=args.world_observation_and_entity_feature_policy_root,
        selective_tracking_adapter_policy_root=args.selective_tracking_adapter_policy_root,
    )

    output_root = Path(args.output_root).expanduser().resolve()
    output_root.mkdir(parents=True, exist_ok=True)

    for name in (
        "summary",
        "input_root_matrix",
        "luna_gate_taxonomy_planning_policy",
        "gate_constitution",
        "gate_type_taxonomy",
        "gate_level_model",
        "gate_decision_vocabulary",
        "gate_requirement_framework",
        "gate_input_output_contract_template",
        "gate_authority_and_veto_policy",
        "gate_dependency_graph",
        "gate_failure_recovery_policy",
        "gate_audit_trace_requirement",
        "gate_verifier_requirement_template",
        "gate_consolidation_risk_register",
        "future_governance_handoff_plan",
        "no_runtime_boundary_report",
        "no_write_boundary_report",
        "no_action_boundary_report",
        "governance_debt_register",
        "next_phase_recommendation",
    ):
        _write_json(output_root / f"{name}.json", result[name])

    _write_json(output_root / "verifier_report.json", {"verifier": "PENDING", "phase": "planning", "source_chain": result["summary"].get("source_chain")})

    print(
        json.dumps(
            {
                "output_root": str(output_root),
                "planning_scope": result["summary"]["planning_scope"],
                "final_decision": result["summary"]["final_decision"],
                "recommended_next_phase": result["summary"]["recommended_next_phase"],
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

