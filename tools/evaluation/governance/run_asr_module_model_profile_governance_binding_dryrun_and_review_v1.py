#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run ASR Module Model Profile + Governance Binding DryRunAndReview v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.asr_module_model_profile_governance_binding_dryrun_and_review_v1 import (
    run_asr_module_model_profile_governance_binding_dryrun_and_review_v1,
)

DEFAULT_PLAN = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "asr_module_model_profile_governance_binding_planning"
)
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "asr_module_model_profile_governance_binding_dryrun_and_review"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    (
        "asr_module_model_profile_governance_binding_dryrun_review_policy",
        "asr_module_model_profile_governance_binding_dryrun_review_policy_v1.json",
    ),
    ("planning_input_review", "planning_input_review_v1.json"),
    ("governance_standard_reuse_review", "governance_standard_reuse_review_v1.json"),
    (
        "asr_module_model_profile_governance_binding_candidate",
        "asr_module_model_profile_governance_binding_candidate_v1.json",
    ),
    ("asr_module_definition_review", "asr_module_definition_review_v1.json"),
    ("asr_capability_stack_review", "asr_capability_stack_review_v1.json"),
    ("asr_layered_governance_mapping_review", "asr_layered_governance_mapping_review_v1.json"),
    ("asr_module_local_model_profile_review", "asr_module_local_model_profile_review_v1.json"),
    ("asr_model_profile_registry_refs_review", "asr_model_profile_registry_refs_review_v1.json"),
    ("asr_model_role_assignment_review", "asr_model_role_assignment_review_v1.json"),
    ("asr_input_contract_review", "asr_input_contract_review_v1.json"),
    ("asr_output_contract_review", "asr_output_contract_review_v1.json"),
    ("asr_quality_acceptance_review", "asr_quality_acceptance_review_v1.json"),
    ("asr_health_validation_whitebox_review", "asr_health_validation_whitebox_review_v1.json"),
    ("asr_provider_runtime_boundary_review", "asr_provider_runtime_boundary_review_v1.json"),
    ("asr_fallback_replacement_review", "asr_fallback_replacement_review_v1.json"),
    ("asr_module_internal_self_check_review", "asr_module_internal_self_check_review_v1.json"),
    ("asr_midplatform_interaction_check_review", "asr_midplatform_interaction_check_review_v1.json"),
    ("asr_midplatform_governance_binding_review", "asr_midplatform_governance_binding_review_v1.json"),
    ("asr_information_integration_handoff_review", "asr_information_integration_handoff_review_v1.json"),
    ("asr_decision_center_handoff_review", "asr_decision_center_handoff_review_v1.json"),
    ("asr_privacy_identity_boundary_review", "asr_privacy_identity_boundary_review_v1.json"),
    (
        "asr_memory_worldmodel_admission_boundary_review",
        "asr_memory_worldmodel_admission_boundary_review_v1.json",
    ),
    ("asr_module_qualification_check_review", "asr_module_qualification_check_review_v1.json"),
    ("asr_non_runtime_boundary_audit", "asr_non_runtime_boundary_audit_v1.json"),
    ("asr_blocked_path_result", "asr_blocked_path_result_v1.json"),
    ("asr_module_closure_decision", "asr_module_closure_decision_v1.json"),
    ("next_route_readiness_decision", "next_route_readiness_decision_v1.json"),
    ("non_claims_register", "non_claims_register_v1.json"),
)


def _write(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=DEFAULT_OUTPUT)
    p.add_argument("--planning-root", default=DEFAULT_PLAN)
    args = p.parse_args()

    result = run_asr_module_model_profile_governance_binding_dryrun_and_review_v1(
        asr_module_model_profile_governance_binding_planning_root=args.planning_root,
        output_root=args.output_root,
    )

    out_root = Path(args.output_root)
    for key, fname in OUTPUT_FILES:
        _write(out_root / fname, result[key])

    sm = result["summary"]
    print(
        json.dumps(
            {
                "output_root": str(out_root),
                "dryrun_and_review_pass": sm.get("dryrun_and_review_pass"),
                "qualification_mode": sm.get("qualification_mode"),
                "final_decision": sm.get("final_decision"),
                "recommended_next_phase": sm.get("recommended_next_phase"),
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
