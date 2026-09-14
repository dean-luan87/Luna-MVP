#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Luna Validation Factory Consolidation v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.luna_validation_factory_consolidation_v1 import (
    run_luna_validation_factory_consolidation_v1,
)

DEFAULT_OUTPUT_ROOT = REPO_ROOT / "_eval_out" / "luna_validation_factory_consolidation_v1_smoke_v0"
EVAL_BASE = Path("/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out")

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    ("luna_validation_factory_consolidation_policy", "luna_validation_factory_consolidation_policy_v1.json"),
    ("validation_factory_module_registry", "validation_factory_module_registry_v1.json"),
    ("batch_preflight_harness_registry_review", "batch_preflight_harness_registry_review_v1.json"),
    ("single_chain_trial_validation_harness_registry_review", "single_chain_trial_validation_harness_registry_review_v1.json"),
    ("controlled_trial_authorization_harness_contract", "controlled_trial_authorization_harness_contract_v1.json"),
    ("candidate_output_contract", "candidate_output_contract_v1.json"),
    ("no_runtime_boundary_audit_contract", "no_runtime_boundary_audit_contract_v1.json"),
    ("controlled_trial_post_execution_review_harness_contract", "controlled_trial_post_execution_review_harness_contract_v1.json"),
    ("validation_factory_usage_guide", "validation_factory_usage_guide_v1.json"),
    ("validation_factory_anti_recursion_rules", "validation_factory_anti_recursion_rules_v1.json"),
    ("validation_factory_future_adoption_matrix", "validation_factory_future_adoption_matrix_v1.json"),
    ("vision_sample_frame_integrated_consumer_review", "vision_sample_frame_integrated_consumer_review_v1.json"),
    ("validation_factory_non_claims_register", "validation_factory_non_claims_register_v1.json"),
    ("validation_factory_consolidation_decision", "validation_factory_consolidation_decision_v1.json"),
)


def _write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=str(DEFAULT_OUTPUT_ROOT))
    p.add_argument("--eval-base", default=str(EVAL_BASE))
    args = p.parse_args()
    base = Path(args.eval_base)

    result = run_luna_validation_factory_consolidation_v1(
        main_project_structure_migration_final_closure_root=str(base / "main_project_structure_migration_final_closure"),
        b0_harness_adoption_and_reusable_contract_closure_root=str(
            base / "b0_harness_adoption_and_reusable_contract_closure"
        ),
        single_chain_trial_validation_harness_validation_closure_root=str(
            base / "single_chain_trial_validation_harness_validation_closure"
        ),
        vision_sample_frame_single_chain_plan_and_dryrun_root=str(
            base / "vision_sample_frame_single_chain_plan_and_dryrun"
        ),
        vision_sample_frame_single_chain_controlled_trial_dryrun_and_review_root=str(
            base / "vision_sample_frame_single_chain_controlled_trial_dryrun_and_review"
        ),
        vision_sample_frame_single_chain_controlled_trial_execution_authorization_planning_root=str(
            base / "vision_sample_frame_single_chain_controlled_trial_execution_authorization_planning"
        ),
        vision_sample_frame_single_chain_controlled_trial_execution_authorization_dryrun_and_review_root=str(
            base / "vision_sample_frame_single_chain_controlled_trial_execution_authorization_dryrun_and_review"
        ),
        vision_sample_frame_single_chain_controlled_trial_execution_authorization_request_planning_root=str(
            base / "vision_sample_frame_single_chain_controlled_trial_execution_authorization_request_planning"
        ),
        consolidation_output_root=args.output_root,
    )
    out = Path(args.output_root)
    for key, fname in OUTPUT_FILES:
        _write_json(out / fname, result[key])
    s = result["summary"]
    print(
        json.dumps(
            {
                "phase": s.get("phase"),
                "boundary_ok": s.get("boundary_ok"),
                "final_decision": s.get("final_decision"),
                "recommended_next_phase": s.get("recommended_next_phase"),
            },
            ensure_ascii=False,
        )
    )
    return 0 if s.get("boundary_ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
