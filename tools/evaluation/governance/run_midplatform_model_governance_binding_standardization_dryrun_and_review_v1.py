#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Midplatform Model Governance Binding Standardization DryRunAndReview v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.midplatform_model_governance_binding_standardization_dryrun_and_review_v1 import (
    run_midplatform_model_governance_binding_standardization_dryrun_and_review_v1,
)

DEFAULT_PLAN = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_model_governance_binding_standardization_planning"
)
DEFAULT_ML_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "module_local_model_profile_standardization_dryrun_and_review"
)
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_model_governance_binding_standardization_dryrun_and_review"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    (
        "midplatform_model_governance_binding_standardization_dryrun_review_policy",
        "midplatform_model_governance_binding_standardization_dryrun_review_policy_v1.json",
    ),
    ("planning_input_review", "planning_input_review_v1.json"),
    ("governance_standard_reuse_review", "governance_standard_reuse_review_v1.json"),
    (
        "midplatform_model_governance_binding_standard_candidate",
        "midplatform_model_governance_binding_standard_candidate_v1.json",
    ),
    (
        "midplatform_model_governance_binding_schema_review",
        "midplatform_model_governance_binding_schema_review_v1.json",
    ),
    ("constitution_bus_binding_policy_review", "constitution_bus_binding_policy_review_v1.json"),
    ("capability_bus_binding_policy_review", "capability_bus_binding_policy_review_v1.json"),
    ("provider_abstraction_binding_policy_review", "provider_abstraction_binding_policy_review_v1.json"),
    ("validation_binding_policy_review", "validation_binding_policy_review_v1.json"),
    ("health_oversight_binding_policy_review", "health_oversight_binding_policy_review_v1.json"),
    ("whitebox_trace_binding_policy_review", "whitebox_trace_binding_policy_review_v1.json"),
    (
        "information_integration_binding_policy_review",
        "information_integration_binding_policy_review_v1.json",
    ),
    ("decision_center_binding_policy_review", "decision_center_binding_policy_review_v1.json"),
    ("gate_chain_binding_policy_review", "gate_chain_binding_policy_review_v1.json"),
    ("controlled_runtime_binding_policy_review", "controlled_runtime_binding_policy_review_v1.json"),
    (
        "memory_worldmodel_admission_binding_policy_review",
        "memory_worldmodel_admission_binding_policy_review_v1.json",
    ),
    (
        "model_governance_binding_by_capability_layer_review",
        "model_governance_binding_by_capability_layer_review_v1.json",
    ),
    (
        "model_governance_binding_by_module_domain_review",
        "model_governance_binding_by_module_domain_review_v1.json",
    ),
    (
        "vision_model_governance_binding_template_review",
        "vision_model_governance_binding_template_review_v1.json",
    ),
    ("ocr_model_governance_binding_template_review", "ocr_model_governance_binding_template_review_v1.json"),
    ("tts_model_governance_binding_template_review", "tts_model_governance_binding_template_review_v1.json"),
    ("asr_model_governance_binding_template_review", "asr_model_governance_binding_template_review_v1.json"),
    (
        "map_navigation_model_governance_binding_template_review",
        "map_navigation_model_governance_binding_template_review_v1.json",
    ),
    (
        "world_continuity_model_governance_binding_template_review",
        "world_continuity_model_governance_binding_template_review_v1.json",
    ),
    (
        "memory_emotion_evolution_model_governance_binding_template_review",
        "memory_emotion_evolution_model_governance_binding_template_review_v1.json",
    ),
    (
        "dual_validation_to_midplatform_binding_handoff_policy_review",
        "dual_validation_to_midplatform_binding_handoff_policy_review_v1.json",
    ),
    ("non_compliance_handling_deferment_review", "non_compliance_handling_deferment_review_v1.json"),
    (
        "midplatform_model_governance_binding_non_runtime_boundary_audit",
        "midplatform_model_governance_binding_non_runtime_boundary_audit_v1.json",
    ),
    (
        "midplatform_model_governance_binding_blocked_path_result",
        "midplatform_model_governance_binding_blocked_path_result_v1.json",
    ),
    (
        "midplatform_model_governance_binding_closure_decision",
        "midplatform_model_governance_binding_closure_decision_v1.json",
    ),
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
    p.add_argument("--module-local-dryrun-root", default=DEFAULT_ML_DR)
    args = p.parse_args()

    result = run_midplatform_model_governance_binding_standardization_dryrun_and_review_v1(
        midplatform_model_governance_binding_standardization_planning_root=args.planning_root,
        module_local_model_profile_standardization_dryrun_and_review_root=args.module_local_dryrun_root,
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
                "template_count": sm.get("template_count"),
                "binding_policy_count": sm.get("binding_policy_count"),
                "final_decision": sm.get("final_decision"),
                "recommended_next_phase": sm.get("recommended_next_phase"),
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
