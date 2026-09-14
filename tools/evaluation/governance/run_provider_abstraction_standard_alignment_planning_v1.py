#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Provider Abstraction Standard Alignment Planning v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.provider_abstraction_standard_alignment_planning_v1 import (
    run_provider_abstraction_standard_alignment_planning_v1,
)

DEFAULT_ROADMAP = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_post_output_chain_simulation_roadmap_decision"
)
DEFAULT_TTS_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/midplatform_tts_runtime_dryrun_and_review"
)
DEFAULT_TTS_PLAN = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/midplatform_tts_runtime_planning"
)
DEFAULT_OCR_AUTH = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "ocr_real_dependency_authorization_via_factory_standard_dryrun_and_review"
)
DEFAULT_HARNESS = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "controlled_provider_readiness_harness_factory_registration_post_dryrun_review"
)
DEFAULT_REGISTRY = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "model_registry_canonicalization_post_dryrun_review"
)
DEFAULT_TEMPLATE = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_module_definition_template_planning"
)
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "provider_abstraction_standard_alignment_planning"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    (
        "provider_abstraction_standard_alignment_policy",
        "provider_abstraction_standard_alignment_policy_v1.json",
    ),
    ("post_output_chain_roadmap_input_review", "post_output_chain_roadmap_input_review_v1.json"),
    ("provider_abstraction_standard", "provider_abstraction_standard_v1.json"),
    ("provider_candidate_contract", "provider_candidate_contract_v1.json"),
    ("provider_adapter_boundary_contract", "provider_adapter_boundary_contract_v1.json"),
    ("provider_readiness_binding_contract", "provider_readiness_binding_contract_v1.json"),
    ("provider_selection_authorization_policy", "provider_selection_authorization_policy_v1.json"),
    ("provider_switch_policy", "provider_switch_policy_v1.json"),
    ("domain_provider_alignment_matrix", "domain_provider_alignment_matrix_v1.json"),
    ("ocr_provider_alignment_plan", "ocr_provider_alignment_plan_v1.json"),
    ("vision_provider_alignment_plan", "vision_provider_alignment_plan_v1.json"),
    ("voice_asr_provider_alignment_plan", "voice_asr_provider_alignment_plan_v1.json"),
    ("voice_tts_provider_alignment_plan", "voice_tts_provider_alignment_plan_v1.json"),
    ("map_provider_alignment_plan", "map_provider_alignment_plan_v1.json"),
    (
        "library_hive_memory_provider_alignment_plan",
        "library_hive_memory_provider_alignment_plan_v1.json",
    ),
    ("legacy_provider_reference_absorption_plan", "legacy_provider_reference_absorption_plan_v1.json"),
    (
        "provider_abstraction_consistency_rule_matrix",
        "provider_abstraction_consistency_rule_matrix_v1.json",
    ),
    ("provider_abstraction_boundary_matrix", "provider_abstraction_boundary_matrix_v1.json"),
    ("provider_abstraction_dryrun_plan", "provider_abstraction_dryrun_plan_v1.json"),
    ("non_claims_register", "non_claims_register_v1.json"),
    (
        "provider_abstraction_standard_alignment_planning_decision",
        "provider_abstraction_standard_alignment_planning_decision_v1.json",
    ),
)


def _write(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=DEFAULT_OUTPUT)
    p.add_argument("--roadmap-root", default=DEFAULT_ROADMAP)
    p.add_argument("--tts-dryrun-root", default=DEFAULT_TTS_DR)
    p.add_argument("--tts-planning-root", default=DEFAULT_TTS_PLAN)
    p.add_argument("--ocr-auth-dryrun-root", default=DEFAULT_OCR_AUTH)
    p.add_argument("--harness-post-review-root", default=DEFAULT_HARNESS)
    p.add_argument("--model-registry-post-review-root", default=DEFAULT_REGISTRY)
    p.add_argument("--template-planning-root", default=DEFAULT_TEMPLATE)
    args = p.parse_args()

    result = run_provider_abstraction_standard_alignment_planning_v1(
        midplatform_post_output_chain_simulation_roadmap_decision_root=args.roadmap_root,
        midplatform_tts_runtime_dryrun_and_review_root=args.tts_dryrun_root,
        midplatform_tts_runtime_planning_root=args.tts_planning_root,
        ocr_real_dependency_authorization_via_factory_standard_dryrun_and_review_root=args.ocr_auth_dryrun_root,
        controlled_provider_readiness_harness_factory_registration_post_dryrun_review_root=args.harness_post_review_root,
        model_registry_canonicalization_post_dryrun_review_root=args.model_registry_post_review_root,
        midplatform_module_definition_template_planning_root=args.template_planning_root,
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
                "standard_id": sm.get("standard_id", "provider_abstraction_standard_v1"),
            },
            ensure_ascii=False,
        )
    )
    return 0 if sm.get("planning_pass") else 1


if __name__ == "__main__":
    raise SystemExit(main())

