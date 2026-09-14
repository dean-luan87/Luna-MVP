#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run TTS Module Model Profile + Governance Binding DryRunAndReview v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.tts_module_model_profile_governance_binding_dryrun_and_review_v1 import (
    run_tts_module_model_profile_governance_binding_dryrun_and_review_v1,
)

DEFAULT_PLAN = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "tts_module_model_profile_governance_binding_planning"
)
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "tts_module_model_profile_governance_binding_dryrun_and_review"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    (
        "tts_module_model_profile_governance_binding_dryrun_review_policy",
        "tts_module_model_profile_governance_binding_dryrun_review_policy_v1.json",
    ),
    ("planning_input_review", "planning_input_review_v1.json"),
    ("governance_standard_reuse_review", "governance_standard_reuse_review_v1.json"),
    (
        "tts_module_model_profile_governance_binding_candidate",
        "tts_module_model_profile_governance_binding_candidate_v1.json",
    ),
    ("tts_module_definition_review", "tts_module_definition_review_v1.json"),
    ("tts_capability_stack_review", "tts_capability_stack_review_v1.json"),
    ("tts_layered_governance_mapping_review", "tts_layered_governance_mapping_review_v1.json"),
    ("tts_module_local_model_profile_review", "tts_module_local_model_profile_review_v1.json"),
    ("tts_model_profile_registry_refs_review", "tts_model_profile_registry_refs_review_v1.json"),
    ("tts_model_role_assignment_review", "tts_model_role_assignment_review_v1.json"),
    ("tts_input_contract_review", "tts_input_contract_review_v1.json"),
    ("tts_output_contract_review", "tts_output_contract_review_v1.json"),
    ("tts_quality_acceptance_review", "tts_quality_acceptance_review_v1.json"),
    ("tts_health_validation_whitebox_review", "tts_health_validation_whitebox_review_v1.json"),
    ("tts_provider_runtime_boundary_review", "tts_provider_runtime_boundary_review_v1.json"),
    ("tts_fallback_replacement_review", "tts_fallback_replacement_review_v1.json"),
    ("tts_module_internal_self_check_review", "tts_module_internal_self_check_review_v1.json"),
    ("tts_midplatform_interaction_check_review", "tts_midplatform_interaction_check_review_v1.json"),
    ("tts_midplatform_governance_binding_review", "tts_midplatform_governance_binding_review_v1.json"),
    ("tts_speech_gate_handoff_review", "tts_speech_gate_handoff_review_v1.json"),
    ("tts_voice_output_plane_boundary_review", "tts_voice_output_plane_boundary_review_v1.json"),
    (
        "tts_memory_worldmodel_admission_boundary_review",
        "tts_memory_worldmodel_admission_boundary_review_v1.json",
    ),
    ("tts_module_qualification_check_review", "tts_module_qualification_check_review_v1.json"),
    ("tts_non_runtime_boundary_audit", "tts_non_runtime_boundary_audit_v1.json"),
    ("tts_blocked_path_result", "tts_blocked_path_result_v1.json"),
    ("tts_module_closure_decision", "tts_module_closure_decision_v1.json"),
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

    result = run_tts_module_model_profile_governance_binding_dryrun_and_review_v1(
        tts_module_model_profile_governance_binding_planning_root=args.planning_root,
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
