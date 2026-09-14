#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Luna Safety Constitution Policy v1."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any, Dict

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.luna_safety_constitution_policy_v1 import run_luna_safety_constitution_policy_v1


DEFAULT_WORKSPACE_ROOT = Path("/Users/luanlei/Desktop/Luna-Workspace-Min")
DEFAULT_OUTPUT_ROOT = DEFAULT_WORKSPACE_ROOT / "_eval_out" / "luna_safety_constitution_policy_v1_smoke_v0"


def _write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Luna Safety Constitution Policy v1")
    parser.add_argument("--output-root", default=str(DEFAULT_OUTPUT_ROOT))
    parser.add_argument(
        "--post-controlled-frame-roadmap-decision-root",
        default=str(DEFAULT_WORKSPACE_ROOT / "_eval_out" / "post_controlled_frame_input_roadmap_decision_v1_smoke_v0"),
    )
    parser.add_argument(
        "--controlled-frame-input-closure-root",
        default=str(DEFAULT_WORKSPACE_ROOT / "_eval_out" / "controlled_frame_input_closure_v1_smoke_v0"),
    )
    parser.add_argument(
        "--map-location-readonly-context-root",
        default=str(DEFAULT_WORKSPACE_ROOT / "_eval_out" / "map_location_readonly_context_policy_v1_smoke_v0"),
    )
    parser.add_argument(
        "--vision-strengthening-closure-root",
        default=str(DEFAULT_WORKSPACE_ROOT / "_eval_out" / "basic_navigation_loop_vision_strengthening_closure_v1_smoke_v0"),
    )
    parser.add_argument(
        "--safety-task-arbitration-policy-root",
        default=str(DEFAULT_WORKSPACE_ROOT / "_eval_out" / "safety_task_arbitration_policy_v1_smoke_v0"),
    )
    parser.add_argument(
        "--minimal-runtime-integration-closure-root",
        default=str(DEFAULT_WORKSPACE_ROOT / "_eval_out" / "minimal_runtime_integration_closure_v1_smoke_v0"),
    )
    parser.add_argument(
        "--ocr-final-closure-root",
        default=str(DEFAULT_WORKSPACE_ROOT / "_eval_out" / "ocr_mainline_final_closure_v1_smoke_v0"),
    )
    parser.add_argument(
        "--voice-command-ownership-gate-policy-root",
        default=str(DEFAULT_WORKSPACE_ROOT / "_eval_out" / "voice_command_ownership_gate_policy_v1_smoke_v0"),
    )
    parser.add_argument(
        "--voice-interruption-governance-dryrun-root",
        default=str(DEFAULT_WORKSPACE_ROOT / "_eval_out" / "voice_interruption_governance_dryrun_v1_smoke_v0"),
    )
    parser.add_argument(
        "--minimal-runtime-controlled-output-definition-root",
        default=str(DEFAULT_WORKSPACE_ROOT / "_eval_out" / "minimal_runtime_integration_controlled_output_definition_v1_smoke_v0"),
    )
    parser.add_argument(
        "--minimal-runtime-text-only-output-post-review-root",
        default=str(DEFAULT_WORKSPACE_ROOT / "_eval_out" / "minimal_runtime_integration_text_only_output_post_trial_review_v1_smoke_v0"),
    )
    parser.add_argument(
        "--task-manager-runtime-root",
        default=str(DEFAULT_WORKSPACE_ROOT / "_eval_out" / "task_manager_runtime_dryrun_v1_smoke_v0"),
    )
    parser.add_argument(
        "--midplatform-task-state-runtime-root",
        default=str(DEFAULT_WORKSPACE_ROOT / "_eval_out" / "midplatform_task_state_runtime_dryrun_v1_smoke_v0"),
    )
    parser.add_argument(
        "--gps-route-context-dryrun-root",
        default=str(DEFAULT_WORKSPACE_ROOT / "_eval_out" / "gps_route_context_dryrun_v1_smoke_v0"),
    )
    parser.add_argument(
        "--ocr-ttl-gate-root",
        default=str(DEFAULT_WORKSPACE_ROOT / "_eval_out" / "ocr_ttl_gate_v1_smoke_v0"),
    )
    parser.add_argument(
        "--ocr-source-validation-dryrun-root",
        default=str(DEFAULT_WORKSPACE_ROOT / "_eval_out" / "ocr_source_validation_dryrun_v1_smoke_v0"),
    )
    parser.add_argument(
        "--ocr-evidence-pack-reference-root",
        default=str(DEFAULT_WORKSPACE_ROOT / "_eval_out" / "ocr_evidence_pack_spatiotemporal_semantic_contract_v0"),
    )
    parser.add_argument(
        "--worldmodel-lookup-framework-root",
        default=str(DEFAULT_WORKSPACE_ROOT / "_eval_out" / "worldmodel_lookup_for_reading_framework_v1_smoke_v0"),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    result = run_luna_safety_constitution_policy_v1(
        post_controlled_frame_roadmap_decision_root=args.post_controlled_frame_roadmap_decision_root,
        controlled_frame_input_closure_root=args.controlled_frame_input_closure_root,
        map_location_readonly_context_root=args.map_location_readonly_context_root,
        vision_strengthening_closure_root=args.vision_strengthening_closure_root,
        safety_task_arbitration_policy_root=args.safety_task_arbitration_policy_root,
        minimal_runtime_integration_closure_root=args.minimal_runtime_integration_closure_root,
        ocr_final_closure_root=args.ocr_final_closure_root,
        voice_command_ownership_gate_policy_root=args.voice_command_ownership_gate_policy_root,
        voice_interruption_governance_dryrun_root=args.voice_interruption_governance_dryrun_root,
        minimal_runtime_controlled_output_definition_root=args.minimal_runtime_controlled_output_definition_root,
        minimal_runtime_text_only_output_post_review_root=args.minimal_runtime_text_only_output_post_review_root,
        task_manager_runtime_root=args.task_manager_runtime_root,
        midplatform_task_state_runtime_root=args.midplatform_task_state_runtime_root,
        gps_route_context_dryrun_root=args.gps_route_context_dryrun_root,
        ocr_ttl_gate_root=args.ocr_ttl_gate_root,
        ocr_source_validation_dryrun_root=args.ocr_source_validation_dryrun_root,
        ocr_evidence_pack_reference_root=args.ocr_evidence_pack_reference_root,
        worldmodel_lookup_framework_root=args.worldmodel_lookup_framework_root,
    )
    output_root = Path(args.output_root)
    for name in (
        "summary",
        "input_root_matrix",
        "luna_safety_constitution_policy",
        "global_safety_principles",
        "high_risk_domain_matrix",
        "evidence_boundary_policy",
        "uncertainty_output_policy",
        "user_instruction_boundary_policy",
        "action_authority_boundary_policy",
        "crossing_safety_inheritance_policy",
        "future_survival_constitution_upgrade_path",
        "safety_constitution_scenario_matrix",
        "safety_constitution_boundary_matrix",
        "governance_debt_register",
        "next_phase_recommendation",
        "no_runtime_boundary_report",
        "no_write_boundary_report",
    ):
        _write_json(output_root / f"{name}.json", result[name])
    print(
        json.dumps(
            {
                "output_root": str(output_root),
                "policy_scope": result["summary"]["policy_scope"],
                "final_decision": result["summary"]["final_decision"],
                "recommended_next_phase": result["summary"]["recommended_next_phase"],
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
