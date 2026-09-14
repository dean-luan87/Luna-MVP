#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Model Management Layer Recovery Planning v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.model_management_layer_recovery_planning_v1 import (
    run_model_management_layer_recovery_planning_v1,
)

WS = "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out"
DEFAULT_OUTPUT = f"{WS}/model_management_layer_recovery_planning"

DEFAULT_INPUTS = {
    "task_response_candidate_midplatform_integration_post_dryrun_review_root": (
        f"{WS}/task_response_candidate_midplatform_integration_post_dryrun_review"
    ),
    "midplatform_post_backbone_roadmap_decision_root": f"{WS}/midplatform_post_backbone_roadmap_decision",
    "midplatform_module_gap_and_roadmap_planning_root": f"{WS}/midplatform_module_gap_and_roadmap_planning",
    "midplatform_structure_cleanup_planning_root": f"{WS}/midplatform_structure_cleanup_planning",
    "midplatform_backbone_definition_alignment_root": f"{WS}/midplatform_backbone_definition_alignment",
    "luna_validation_factory_consolidation_root": f"{WS}/luna_validation_factory_consolidation",
}

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    ("model_management_recovery_planning_policy", "model_management_recovery_planning_policy_v1.json"),
    ("upstream_task_response_review_input_review", "upstream_task_response_review_input_review_v1.json"),
    ("model_management_layer_scope", "model_management_layer_scope_v1.json"),
    ("model_registry_contract_planning", "model_registry_contract_planning_v1.json"),
    ("skill_registry_contract_planning", "skill_registry_contract_planning_v1.json"),
    ("model_capability_descriptor_contract", "model_capability_descriptor_contract_v1.json"),
    ("model_health_state_contract", "model_health_state_contract_v1.json"),
    ("model_switching_and_degradation_policy", "model_switching_and_degradation_policy_v1.json"),
    ("model_output_contract_integration_plan", "model_output_contract_integration_plan_v1.json"),
    ("model_runtime_boundary_matrix", "model_runtime_boundary_matrix_v1.json"),
    ("model_provider_governance_mapping", "model_provider_governance_mapping_v1.json"),
    ("validation_factory_model_layer_integration_plan", "validation_factory_model_layer_integration_plan_v1.json"),
    ("model_management_recovery_dryrun_plan", "model_management_recovery_dryrun_plan_v1.json"),
    ("model_management_non_claims_register", "model_management_non_claims_register_v1.json"),
    ("model_management_recovery_planning_decision", "model_management_recovery_planning_decision_v1.json"),
)


def _write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=DEFAULT_OUTPUT)
    for key, default in DEFAULT_INPUTS.items():
        p.add_argument(f"--{key.replace('_', '-')}", default=default)
    args = p.parse_args()

    result = run_model_management_layer_recovery_planning_v1(
        task_response_candidate_midplatform_integration_post_dryrun_review_root=(
            args.task_response_candidate_midplatform_integration_post_dryrun_review_root
        ),
        midplatform_post_backbone_roadmap_decision_root=args.midplatform_post_backbone_roadmap_decision_root,
        midplatform_module_gap_and_roadmap_planning_root=args.midplatform_module_gap_and_roadmap_planning_root,
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
