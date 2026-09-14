#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Luna Project Structure Governance and Modularization Planning v1 (planning-only)."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any, Dict

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.luna_project_structure_governance_and_modularization_planning_v1 import (
    run_luna_project_structure_governance_and_modularization_planning_v1,
)

DEFAULT_OUTPUT_ROOT = (
    REPO_ROOT / "_eval_out" / "luna_project_structure_governance_and_modularization_planning_v1_smoke_v0"
)

# Historical inputs may remain under Luna-Workspace-Min (read-only).
DEFAULT_INPUT_WORKSPACE_ROOT = Path("/Users/luanlei/Desktop/Luna-Workspace-Min")


def _write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Luna Project Structure Governance and Modularization Planning v1")
    parser.add_argument("--output-root", default=str(DEFAULT_OUTPUT_ROOT))
    parser.add_argument("--repo-root", default=str(REPO_ROOT))

    # Inputs in Luna-Core
    parser.add_argument(
        "--gate-taxonomy-planning-root",
        default=str(REPO_ROOT / "_eval_out" / "gate_taxonomy_and_requirement_framework_planning_v1_smoke_v0"),
    )
    parser.add_argument(
        "--post-file-stat-roadmap-decision-root",
        default=str(REPO_ROOT / "_eval_out" / "post_file_stat_roadmap_decision_v1_smoke_v0"),
    )
    parser.add_argument(
        "--file-stat-guarded-closure-root",
        default=str(REPO_ROOT / "_eval_out" / "controlled_frame_file_stat_guarded_closure_v1_smoke_v0"),
    )
    parser.add_argument(
        "--file-existence-check-guarded-closure-root",
        default=str(REPO_ROOT / "_eval_out" / "controlled_frame_file_existence_check_guarded_closure_v1_smoke_v0"),
    )

    # Historical inputs in Luna-Workspace-Min (read-only)
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

    # Optional roots
    parser.add_argument(
        "--basic-navigation-loop-vision-strengthening-closure-root",
        default=str(DEFAULT_INPUT_WORKSPACE_ROOT / "_eval_out" / "basic_navigation_loop_vision_strengthening_closure_v1_smoke_v0"),
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
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    result = run_luna_project_structure_governance_and_modularization_planning_v1(
        repo_root=args.repo_root,
        gate_taxonomy_planning_root=args.gate_taxonomy_planning_root,
        post_file_stat_roadmap_decision_root=args.post_file_stat_roadmap_decision_root,
        file_stat_guarded_closure_root=args.file_stat_guarded_closure_root,
        file_existence_check_guarded_closure_root=args.file_existence_check_guarded_closure_root,
        file_metadata_boundary_closure_root=args.file_metadata_boundary_closure_root,
        controlled_frame_sample_closure_root=args.controlled_frame_sample_closure_root,
        controlled_frame_input_closure_root=args.controlled_frame_input_closure_root,
        crossing_decision_closure_root=args.crossing_decision_closure_root,
        safety_constitution_root=args.safety_constitution_root,
        basic_navigation_loop_vision_strengthening_closure_root=args.basic_navigation_loop_vision_strengthening_closure_root,
        map_location_readonly_context_root=args.map_location_readonly_context_root,
        minimal_runtime_integration_closure_root=args.minimal_runtime_integration_closure_root,
        ocr_final_closure_root=args.ocr_final_closure_root,
    )

    output_root = Path(args.output_root).expanduser().resolve()
    output_root.mkdir(parents=True, exist_ok=True)

    for name in (
        "summary",
        "input_root_matrix",
        "luna_project_structure_governance_planning_policy",
        "current_project_structure_audit",
        "target_project_structure_model",
        "module_domain_taxonomy",
        "module_versioning_and_changelog_policy",
        "document_reorganization_policy",
        "midplatform_organ_system_model",
        "developer_backend_extraction_plan",
        "hardware_management_consolidation_plan",
        "future_module_placeholder_plan",
        "module_consolidation_candidate_register",
        "client_boundary_policy",
        "project_governance_debt_register",
        "next_phase_recommendation",
        "no_runtime_boundary_report",
        "no_write_boundary_report",
        "no_action_boundary_report",
        "no_file_operation_boundary_report",
    ):
        _write_json(output_root / f"{name}.json", result[name])

    _write_json(
        output_root / "verifier_report.json",
        {"verifier": "PENDING", "phase": "planning", "source_chain": result["summary"].get("source_chain")},
    )

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

