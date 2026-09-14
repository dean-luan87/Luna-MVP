#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Task Response Candidate Midplatform Integration Planning v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.task_response_candidate_midplatform_integration_planning_v1 import (
    run_task_response_candidate_midplatform_integration_planning_v1,
)

WS = "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out"
DEFAULT_OUTPUT_ROOT = f"{WS}/task_response_candidate_midplatform_integration_planning"

DEFAULT_INPUTS = {
    "midplatform_post_backbone_roadmap_decision_root": f"{WS}/midplatform_post_backbone_roadmap_decision",
    "midplatform_minimal_backbone_post_dryrun_review_root": f"{WS}/midplatform_minimal_backbone_post_dryrun_review",
    "midplatform_minimal_backbone_dryrun_root": f"{WS}/midplatform_minimal_backbone_dryrun",
    "midplatform_structure_cleanup_planning_root": f"{WS}/midplatform_structure_cleanup_planning",
    "midplatform_backbone_definition_alignment_root": f"{WS}/midplatform_backbone_definition_alignment",
    "luna_validation_factory_consolidation_root": f"{WS}/luna_validation_factory_consolidation",
}

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    ("task_response_candidate_integration_planning_policy", "task_response_candidate_integration_planning_policy_v1.json"),
    ("post_backbone_roadmap_input_review", "post_backbone_roadmap_input_review_v1.json"),
    ("task_response_candidate_scope", "task_response_candidate_scope_v1.json"),
    ("task_response_candidate_input_contract", "task_response_candidate_input_contract_v1.json"),
    ("task_response_candidate_output_contract", "task_response_candidate_output_contract_v1.json"),
    ("task_layer_integration_plan", "task_layer_integration_plan_v1.json"),
    ("input_output_layer_integration_plan", "input_output_layer_integration_plan_v1.json"),
    ("constitution_overlay_for_task_response", "constitution_overlay_for_task_response_v1.json"),
    ("output_arbitration_for_task_response", "output_arbitration_for_task_response_v1.json"),
    ("runtime_boundary_for_task_response", "runtime_boundary_for_task_response_v1.json"),
    ("task_response_candidate_flow_plan", "task_response_candidate_flow_plan_v1.json"),
    ("task_response_candidate_blocked_path_matrix", "task_response_candidate_blocked_path_matrix_v1.json"),
    ("task_response_candidate_dryrun_plan", "task_response_candidate_dryrun_plan_v1.json"),
    ("task_response_integration_non_claims_register", "task_response_integration_non_claims_register_v1.json"),
    ("task_response_integration_readiness_decision", "task_response_integration_readiness_decision_v1.json"),
)


def _write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=DEFAULT_OUTPUT_ROOT)
    for key, default in DEFAULT_INPUTS.items():
        p.add_argument(f"--{key.replace('_', '-')}", default=default)
    args = p.parse_args()

    result = run_task_response_candidate_midplatform_integration_planning_v1(
        midplatform_post_backbone_roadmap_decision_root=args.midplatform_post_backbone_roadmap_decision_root,
        midplatform_minimal_backbone_post_dryrun_review_root=args.midplatform_minimal_backbone_post_dryrun_review_root,
        midplatform_minimal_backbone_dryrun_root=args.midplatform_minimal_backbone_dryrun_root,
        midplatform_structure_cleanup_planning_root=args.midplatform_structure_cleanup_planning_root,
        midplatform_backbone_definition_alignment_root=args.midplatform_backbone_definition_alignment_root,
        luna_validation_factory_consolidation_root=args.luna_validation_factory_consolidation_root,
        output_root=args.output_root,
    )

    out_root = Path(args.output_root)
    for key, filename in OUTPUT_FILES:
        _write_json(out_root / filename, result[key])

    summary = result["summary"]
    print(
        json.dumps(
            {
                "output_root": str(out_root),
                "boundary_ok": summary.get("boundary_ok"),
                "final_decision": summary.get("final_decision"),
                "recommended_next_phase": summary.get("recommended_next_phase"),
            },
            ensure_ascii=False,
        )
    )
    return 0 if summary.get("boundary_ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
