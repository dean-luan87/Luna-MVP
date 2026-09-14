#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run OCR Module Model Profile + Governance Binding DryRunAndReview v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.ocr_module_model_profile_governance_binding_dryrun_and_review_v1 import (
    run_ocr_module_model_profile_governance_binding_dryrun_and_review_v1,
)

DEFAULT_PLAN = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "ocr_module_model_profile_governance_binding_planning"
)
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "ocr_module_model_profile_governance_binding_dryrun_and_review"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    (
        "ocr_module_model_profile_governance_binding_dryrun_review_policy",
        "ocr_module_model_profile_governance_binding_dryrun_review_policy_v1.json",
    ),
    ("planning_input_review", "planning_input_review_v1.json"),
    ("governance_standard_reuse_review", "governance_standard_reuse_review_v1.json"),
    (
        "ocr_module_model_profile_governance_binding_candidate",
        "ocr_module_model_profile_governance_binding_candidate_v1.json",
    ),
    ("ocr_module_definition_review", "ocr_module_definition_review_v1.json"),
    ("ocr_capability_stack_review", "ocr_capability_stack_review_v1.json"),
    ("ocr_layered_governance_mapping_review", "ocr_layered_governance_mapping_review_v1.json"),
    ("ocr_module_local_model_profile_review", "ocr_module_local_model_profile_review_v1.json"),
    ("ocr_model_profile_registry_refs_review", "ocr_model_profile_registry_refs_review_v1.json"),
    ("ocr_model_role_assignment_review", "ocr_model_role_assignment_review_v1.json"),
    ("ocr_input_contract_review", "ocr_input_contract_review_v1.json"),
    ("ocr_output_contract_review", "ocr_output_contract_review_v1.json"),
    ("ocr_quality_acceptance_review", "ocr_quality_acceptance_review_v1.json"),
    ("ocr_health_validation_whitebox_review", "ocr_health_validation_whitebox_review_v1.json"),
    ("ocr_provider_runtime_boundary_review", "ocr_provider_runtime_boundary_review_v1.json"),
    ("ocr_fallback_replacement_review", "ocr_fallback_replacement_review_v1.json"),
    ("ocr_module_internal_self_check_review", "ocr_module_internal_self_check_review_v1.json"),
    ("ocr_midplatform_interaction_check_review", "ocr_midplatform_interaction_check_review_v1.json"),
    ("ocr_midplatform_governance_binding_review", "ocr_midplatform_governance_binding_review_v1.json"),
    ("ocr_information_integration_handoff_review", "ocr_information_integration_handoff_review_v1.json"),
    ("ocr_decision_center_handoff_review", "ocr_decision_center_handoff_review_v1.json"),
    ("ocr_gate_chain_boundary_review", "ocr_gate_chain_boundary_review_v1.json"),
    (
        "ocr_memory_worldmodel_admission_boundary_review",
        "ocr_memory_worldmodel_admission_boundary_review_v1.json",
    ),
    ("ocr_module_qualification_check_review", "ocr_module_qualification_check_review_v1.json"),
    ("ocr_non_runtime_boundary_audit", "ocr_non_runtime_boundary_audit_v1.json"),
    ("ocr_blocked_path_result", "ocr_blocked_path_result_v1.json"),
    ("ocr_module_closure_decision", "ocr_module_closure_decision_v1.json"),
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

    result = run_ocr_module_model_profile_governance_binding_dryrun_and_review_v1(
        ocr_module_model_profile_governance_binding_planning_root=args.planning_root,
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
