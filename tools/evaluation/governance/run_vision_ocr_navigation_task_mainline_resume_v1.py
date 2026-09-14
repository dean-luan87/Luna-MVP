#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Vision OCR Navigation Task Mainline Resume Planning v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.vision_ocr_navigation_task_mainline_resume_v1 import (
    run_vision_ocr_navigation_task_mainline_resume_v1,
)

DEFAULT_CB_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "luna_constitution_capability_bus_governance_baseline_dryrun_and_review"
)
DEFAULT_II_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_information_integration_layer_dryrun_and_review"
)
DEFAULT_DS_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "seed_core_drive_signal_contract_dryrun_and_review"
)
DEFAULT_SC_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "seed_core_pluggable_layer_architecture_dryrun_and_review"
)
DEFAULT_CZ_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_cognitive_zoning_architecture_dryrun_and_review"
)
DEFAULT_PROVIDER_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "provider_abstraction_standard_alignment_dryrun_and_review"
)
DEFAULT_CR_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_controlled_runtime_dryrun_and_review"
)
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "vision_ocr_navigation_task_mainline_resume"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    (
        "vision_ocr_navigation_task_mainline_resume_policy",
        "vision_ocr_navigation_task_mainline_resume_policy_v1.json",
    ),
    ("constitution_bus_governance_input_review", "constitution_bus_governance_input_review_v1.json"),
    ("mainline_resume_scope_definition", "mainline_resume_scope_definition_v1.json"),
    ("first_person_vision_chain_reentry_plan", "first_person_vision_chain_reentry_plan_v1.json"),
    ("ocr_context_chain_reentry_plan", "ocr_context_chain_reentry_plan_v1.json"),
    ("navigation_task_chain_reentry_plan", "navigation_task_chain_reentry_plan_v1.json"),
    (
        "capability_bus_binding_for_vision_ocr_navigation",
        "capability_bus_binding_for_vision_ocr_navigation_v1.json",
    ),
    (
        "seed_core_drive_signal_binding_for_navigation",
        "seed_core_drive_signal_binding_for_navigation_v1.json",
    ),
    (
        "information_integration_binding_for_navigation",
        "information_integration_binding_for_navigation_v1.json",
    ),
    (
        "decision_center_binding_for_navigation",
        "decision_center_binding_for_navigation_v1.json",
    ),
    (
        "controlled_runtime_deferment_for_vision_ocr_navigation",
        "controlled_runtime_deferment_for_vision_ocr_navigation_v1.json",
    ),
    ("vision_ocr_navigation_candidate_flow", "vision_ocr_navigation_candidate_flow_v1.json"),
    ("vision_ocr_navigation_evidence_flow", "vision_ocr_navigation_evidence_flow_v1.json"),
    ("task_route_context_flow", "task_route_context_flow_v1.json"),
    (
        "safety_survival_navigation_priority_policy",
        "safety_survival_navigation_priority_policy_v1.json",
    ),
    ("mainline_resume_boundary_matrix", "mainline_resume_boundary_matrix_v1.json"),
    ("mainline_resume_next_phase_plan", "mainline_resume_next_phase_plan_v1.json"),
    ("non_claims_register", "non_claims_register_v1.json"),
    (
        "vision_ocr_navigation_task_mainline_resume_decision",
        "vision_ocr_navigation_task_mainline_resume_decision_v1.json",
    ),
)


def _write(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=DEFAULT_OUTPUT)
    p.add_argument("--constitution-bus-dryrun-root", default=DEFAULT_CB_DR)
    p.add_argument("--information-integration-dryrun-root", default=DEFAULT_II_DR)
    p.add_argument("--drive-signal-dryrun-root", default=DEFAULT_DS_DR)
    p.add_argument("--seed-core-pluggable-dryrun-root", default=DEFAULT_SC_DR)
    p.add_argument("--cognitive-zoning-dryrun-root", default=DEFAULT_CZ_DR)
    p.add_argument("--provider-abstraction-dryrun-root", default=DEFAULT_PROVIDER_DR)
    p.add_argument("--controlled-runtime-dryrun-root", default=DEFAULT_CR_DR)
    args = p.parse_args()

    result = run_vision_ocr_navigation_task_mainline_resume_v1(
        luna_constitution_capability_bus_governance_baseline_dryrun_and_review_root=args.constitution_bus_dryrun_root,
        midplatform_information_integration_layer_dryrun_and_review_root=args.information_integration_dryrun_root,
        seed_core_drive_signal_contract_dryrun_and_review_root=args.drive_signal_dryrun_root,
        seed_core_pluggable_layer_architecture_dryrun_and_review_root=args.seed_core_pluggable_dryrun_root,
        midplatform_cognitive_zoning_architecture_dryrun_and_review_root=args.cognitive_zoning_dryrun_root,
        provider_abstraction_standard_alignment_dryrun_and_review_root=args.provider_abstraction_dryrun_root,
        midplatform_controlled_runtime_dryrun_and_review_root=args.controlled_runtime_dryrun_root,
        output_root=args.output_root,
    )

    out = Path(args.output_root)
    for key, fname in OUTPUT_FILES:
        _write(out / fname, result[key])

    sm = result["summary"]
    print(
        json.dumps(
            {
                "output_root": str(out),
                "planning_pass": sm.get("planning_pass"),
                "final_decision": sm.get("final_decision"),
                "recommended_next_phase": sm.get("recommended_next_phase"),
            },
            ensure_ascii=False,
        )
    )
    return 0 if sm.get("planning_pass") else 1


if __name__ == "__main__":
    raise SystemExit(main())
