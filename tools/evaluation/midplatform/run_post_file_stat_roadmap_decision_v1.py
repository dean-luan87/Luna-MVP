#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Post File Stat Roadmap Decision v1."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any, Dict

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.midplatform.post_file_stat_roadmap_decision_v1 import run_post_file_stat_roadmap_decision_v1

DEFAULT_OUTPUT_WORKSPACE_ROOT = REPO_ROOT
DEFAULT_OUTPUT_ROOT = DEFAULT_OUTPUT_WORKSPACE_ROOT / "_eval_out" / "post_file_stat_roadmap_decision_v1_smoke_v0"

# Historical inputs may remain under Luna-Workspace-Min (read-only).
DEFAULT_INPUT_WORKSPACE_ROOT = Path("/Users/luanlei/Desktop/Luna-Workspace-Min")


def _write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Post File Stat Roadmap Decision v1")
    parser.add_argument("--output-root", default=str(DEFAULT_OUTPUT_ROOT))

    # Stat chain outputs are in Luna-Core.
    parser.add_argument(
        "--file-stat-guarded-closure-root",
        default=str(DEFAULT_OUTPUT_WORKSPACE_ROOT / "_eval_out" / "controlled_frame_file_stat_guarded_closure_v1_smoke_v0"),
    )
    parser.add_argument(
        "--file-stat-guarded-post-review-root",
        default=str(DEFAULT_OUTPUT_WORKSPACE_ROOT / "_eval_out" / "controlled_frame_file_stat_guarded_post_dryrun_review_v1_smoke_v0"),
    )
    parser.add_argument(
        "--file-stat-guarded-dryrun-root",
        default=str(DEFAULT_OUTPUT_WORKSPACE_ROOT / "_eval_out" / "controlled_frame_file_stat_guarded_dryrun_v1_smoke_v0"),
    )
    parser.add_argument(
        "--file-stat-guarded-planning-root",
        default=str(DEFAULT_OUTPUT_WORKSPACE_ROOT / "_eval_out" / "controlled_frame_file_stat_guarded_planning_v1_smoke_v0"),
    )

    # Post file existence check roadmap decision is in Luna-Core.
    parser.add_argument(
        "--post-file-existence-check-roadmap-decision-root",
        default=str(DEFAULT_OUTPUT_WORKSPACE_ROOT / "_eval_out" / "post_file_existence_check_roadmap_decision_v1_smoke_v0"),
    )

    # Existence-check chain outputs are in Luna-Core.
    parser.add_argument(
        "--file-existence-check-guarded-closure-root",
        default=str(DEFAULT_OUTPUT_WORKSPACE_ROOT / "_eval_out" / "controlled_frame_file_existence_check_guarded_closure_v1_smoke_v0"),
    )
    parser.add_argument(
        "--file-existence-check-guarded-post-review-root",
        default=str(DEFAULT_OUTPUT_WORKSPACE_ROOT / "_eval_out" / "controlled_frame_file_existence_check_guarded_post_dryrun_review_v1_smoke_v0"),
    )
    parser.add_argument(
        "--file-existence-check-guarded-dryrun-root",
        default=str(DEFAULT_OUTPUT_WORKSPACE_ROOT / "_eval_out" / "controlled_frame_file_existence_check_guarded_dryrun_v1_smoke_v0"),
    )
    parser.add_argument(
        "--file-existence-check-guarded-planning-root",
        default=str(DEFAULT_OUTPUT_WORKSPACE_ROOT / "_eval_out" / "controlled_frame_file_existence_check_guarded_planning_v1_smoke_v0"),
    )

    # Historical inputs remain in Luna-Workspace-Min (read-only).
    parser.add_argument(
        "--file-metadata-boundary-closure-root",
        default=str(DEFAULT_INPUT_WORKSPACE_ROOT / "_eval_out" / "controlled_frame_file_metadata_boundary_closure_v1_smoke_v0"),
    )
    parser.add_argument(
        "--file-metadata-boundary-post-review-root",
        default=str(DEFAULT_INPUT_WORKSPACE_ROOT / "_eval_out" / "controlled_frame_file_metadata_boundary_post_dryrun_review_v1_smoke_v0"),
    )
    parser.add_argument(
        "--file-metadata-boundary-dryrun-root",
        default=str(DEFAULT_INPUT_WORKSPACE_ROOT / "_eval_out" / "controlled_frame_file_metadata_boundary_dryrun_v1_smoke_v0"),
    )
    parser.add_argument(
        "--file-metadata-boundary-planning-root",
        default=str(DEFAULT_INPUT_WORKSPACE_ROOT / "_eval_out" / "controlled_frame_file_metadata_boundary_planning_v1_smoke_v0"),
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
        "--map-location-readonly-context-root",
        default=str(DEFAULT_INPUT_WORKSPACE_ROOT / "_eval_out" / "map_location_readonly_context_policy_v1_smoke_v0"),
    )
    parser.add_argument(
        "--safety-constitution-root",
        default=str(DEFAULT_INPUT_WORKSPACE_ROOT / "_eval_out" / "luna_safety_constitution_policy_v1_smoke_v0"),
    )
    parser.add_argument(
        "--minimal-runtime-integration-closure-root",
        default=str(DEFAULT_INPUT_WORKSPACE_ROOT / "_eval_out" / "minimal_runtime_integration_closure_v1_smoke_v0"),
    )
    parser.add_argument(
        "--ocr-final-closure-root",
        default=str(DEFAULT_INPUT_WORKSPACE_ROOT / "_eval_out" / "ocr_mainline_final_closure_v1_smoke_v0"),
    )

    # Optional roots
    parser.add_argument(
        "--vision-frame-trace-stream-registry-root",
        default=str(DEFAULT_INPUT_WORKSPACE_ROOT / "_eval_out" / "vision_frame_trace_stream_registry_smoke_v0"),
    )
    parser.add_argument(
        "--vision-frame-input-governance-root",
        default=str(DEFAULT_INPUT_WORKSPACE_ROOT / "_eval_out" / "vision_frame_input_governance_smoke_v0"),
    )
    parser.add_argument(
        "--vision-roi-proposal-stub-root",
        default=str(DEFAULT_INPUT_WORKSPACE_ROOT / "_eval_out" / "vision_roi_proposal_stub_smoke_v0"),
    )
    parser.add_argument(
        "--system-health-hardware-profile-root",
        default=str(DEFAULT_INPUT_WORKSPACE_ROOT / "_eval_out" / "hardware_profile_capability_registry_v1_smoke_v0"),
    )
    parser.add_argument(
        "--simulation-lab-profile-root",
        default=str(DEFAULT_INPUT_WORKSPACE_ROOT / "_eval_out" / "luna_simulation_lab_v0"),
    )
    parser.add_argument(
        "--privacy-governance-docs-root",
        default=str(DEFAULT_INPUT_WORKSPACE_ROOT / "_eval_out" / "privacy_governance_docs_v0"),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    result = run_post_file_stat_roadmap_decision_v1(
        file_stat_guarded_closure_root=args.file_stat_guarded_closure_root,
        file_stat_guarded_post_review_root=args.file_stat_guarded_post_review_root,
        file_stat_guarded_dryrun_root=args.file_stat_guarded_dryrun_root,
        file_stat_guarded_planning_root=args.file_stat_guarded_planning_root,
        post_file_existence_check_roadmap_decision_root=args.post_file_existence_check_roadmap_decision_root,
        file_existence_check_guarded_closure_root=args.file_existence_check_guarded_closure_root,
        file_existence_check_guarded_post_review_root=args.file_existence_check_guarded_post_review_root,
        file_existence_check_guarded_dryrun_root=args.file_existence_check_guarded_dryrun_root,
        file_existence_check_guarded_planning_root=args.file_existence_check_guarded_planning_root,
        file_metadata_boundary_closure_root=args.file_metadata_boundary_closure_root,
        file_metadata_boundary_post_review_root=args.file_metadata_boundary_post_review_root,
        file_metadata_boundary_dryrun_root=args.file_metadata_boundary_dryrun_root,
        file_metadata_boundary_planning_root=args.file_metadata_boundary_planning_root,
        controlled_frame_sample_closure_root=args.controlled_frame_sample_closure_root,
        controlled_frame_input_closure_root=args.controlled_frame_input_closure_root,
        map_location_readonly_context_root=args.map_location_readonly_context_root,
        safety_constitution_root=args.safety_constitution_root,
        minimal_runtime_integration_closure_root=args.minimal_runtime_integration_closure_root,
        ocr_final_closure_root=args.ocr_final_closure_root,
        vision_frame_trace_stream_registry_root=args.vision_frame_trace_stream_registry_root,
        vision_frame_input_governance_root=args.vision_frame_input_governance_root,
        vision_roi_proposal_stub_root=args.vision_roi_proposal_stub_root,
        system_health_hardware_profile_root=args.system_health_hardware_profile_root,
        simulation_lab_profile_root=args.simulation_lab_profile_root,
        privacy_governance_docs_root=args.privacy_governance_docs_root,
    )

    output_root = Path(args.output_root).expanduser().resolve()
    output_root.mkdir(parents=True, exist_ok=True)

    for name in (
        "summary",
        "input_root_matrix",
        "current_file_stat_status_summary",
        "completed_capability_summary",
        "route_option_matrix",
        "priority_ranking",
        "recommended_next_phase_decision",
        "deferred_real_file_operation_register",
        "gate_taxonomy_decision_register",
        "deferred_midplatform_governance_register",
        "deferred_resilience_distributed_midplatform_register",
        "deferred_worldmodel_memory_library_emotion_register",
        "boundary_freeze",
        "governance_debt_roadmap_register",
        "non_claims_register",
        "post_file_stat_roadmap_decision",
        "next_phase_recommendation",
        "no_file_operation_boundary_report",
        "no_runtime_boundary_report",
        "no_write_boundary_report",
    ):
        _write_json(output_root / f"{name}.json", result[name])

    # placeholder; verifier writes its own report
    _write_json(output_root / "verifier_report.json", {"verifier": "PENDING", "phase": "roadmap_decision", "source_chain": result["summary"].get("source_chain")})

    print(
        json.dumps(
            {
                "output_root": str(output_root),
                "decision_scope": result["summary"]["decision_scope"],
                "final_decision": result["summary"]["final_decision"],
                "recommended_next_phase": result["summary"]["recommended_next_phase"],
                "selected_route": result["summary"]["selected_route"],
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

