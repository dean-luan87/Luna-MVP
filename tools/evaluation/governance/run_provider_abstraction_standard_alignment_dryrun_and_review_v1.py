#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Provider Abstraction Standard Alignment DryRunAndReview v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.provider_abstraction_standard_alignment_dryrun_and_review_v1 import (
    run_provider_abstraction_standard_alignment_dryrun_and_review_v1,
)

DEFAULT_PLANNING = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "provider_abstraction_standard_alignment_planning"
)
DEFAULT_FMIS_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_frontend_model_influence_simulation_dryrun_and_review"
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
DEFAULT_TEMPLATE = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_module_definition_template_planning"
)
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "provider_abstraction_standard_alignment_dryrun_and_review"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    (
        "provider_abstraction_standard_alignment_dryrun_review_policy",
        "provider_abstraction_standard_alignment_dryrun_review_policy_v1.json",
    ),
    ("provider_abstraction_planning_input_review", "provider_abstraction_planning_input_review_v1.json"),
    ("provider_abstraction_standard_candidate", "provider_abstraction_standard_candidate_v1.json"),
    ("provider_candidate_contract_sample", "provider_candidate_contract_sample_v1.json"),
    ("provider_adapter_boundary_sample", "provider_adapter_boundary_sample_v1.json"),
    ("provider_readiness_binding_sample", "provider_readiness_binding_sample_v1.json"),
    ("provider_selection_authorization_sample", "provider_selection_authorization_sample_v1.json"),
    ("provider_switch_policy_sample", "provider_switch_policy_sample_v1.json"),
    ("domain_provider_alignment_matrix_candidate", "domain_provider_alignment_matrix_candidate_v1.json"),
    ("ocr_provider_alignment_dryrun_review", "ocr_provider_alignment_dryrun_review_v1.json"),
    ("vision_provider_alignment_dryrun_review", "vision_provider_alignment_dryrun_review_v1.json"),
    ("voice_asr_provider_alignment_dryrun_review", "voice_asr_provider_alignment_dryrun_review_v1.json"),
    ("voice_tts_provider_alignment_dryrun_review", "voice_tts_provider_alignment_dryrun_review_v1.json"),
    ("map_provider_alignment_dryrun_review", "map_provider_alignment_dryrun_review_v1.json"),
    (
        "library_hive_memory_provider_alignment_dryrun_review",
        "library_hive_memory_provider_alignment_dryrun_review_v1.json",
    ),
    ("legacy_provider_reference_absorption_marker", "legacy_provider_reference_absorption_marker_v1.json"),
    ("provider_abstraction_consistency_rule_review", "provider_abstraction_consistency_rule_review_v1.json"),
    ("provider_abstraction_boundary_audit", "provider_abstraction_boundary_audit_v1.json"),
    ("provider_abstraction_blocked_path_result", "provider_abstraction_blocked_path_result_v1.json"),
    ("provider_abstraction_closure_decision", "provider_abstraction_closure_decision_v1.json"),
    ("next_route_readiness_decision", "next_route_readiness_decision_v1.json"),
    ("non_claims_register", "non_claims_register_v1.json"),
)


def _write(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=DEFAULT_OUTPUT)
    p.add_argument("--planning-root", default=DEFAULT_PLANNING)
    p.add_argument("--fmis-dryrun-root", default=DEFAULT_FMIS_DR)
    p.add_argument("--tts-runtime-dryrun-root", default=DEFAULT_TTS_DR)
    p.add_argument("--tts-runtime-planning-root", default=DEFAULT_TTS_PLAN)
    p.add_argument("--ocr-auth-dryrun-root", default=DEFAULT_OCR_AUTH)
    p.add_argument("--harness-post-review-root", default=DEFAULT_HARNESS)
    p.add_argument("--template-planning-root", default=DEFAULT_TEMPLATE)
    args = p.parse_args()

    result = run_provider_abstraction_standard_alignment_dryrun_and_review_v1(
        provider_abstraction_standard_alignment_planning_root=args.planning_root,
        midplatform_frontend_model_influence_simulation_dryrun_and_review_root=args.fmis_dryrun_root,
        midplatform_tts_runtime_dryrun_and_review_root=args.tts_runtime_dryrun_root,
        midplatform_tts_runtime_planning_root=args.tts_runtime_planning_root,
        ocr_real_dependency_authorization_via_factory_standard_dryrun_and_review_root=args.ocr_auth_dryrun_root,
        controlled_provider_readiness_harness_factory_registration_post_dryrun_review_root=args.harness_post_review_root,
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
                "dryrun_and_review_pass": sm.get("dryrun_and_review_pass"),
                "final_decision": sm.get("final_decision"),
                "recommended_next_phase": sm.get("recommended_next_phase"),
                "domains_aligned": sm.get("domains_aligned"),
                "domain_count": sm.get("domain_count"),
            },
            ensure_ascii=False,
        )
    )
    return 0 if sm.get("dryrun_and_review_pass") else 1


if __name__ == "__main__":
    raise SystemExit(main())
