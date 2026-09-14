#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Controlled Provider Readiness Harness Validation Factory Registration DryRun v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.controlled_provider_readiness_harness_factory_registration_dryrun_v1 import (
    run_controlled_provider_readiness_harness_factory_registration_dryrun_v1,
)

DEFAULT_PLANNING = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "controlled_provider_readiness_harness_factory_registration_planning"
)
DEFAULT_ROADMAP = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/provider_harness_generalization_roadmap_decision"
)
DEFAULT_HARNESS = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/controlled_provider_readiness_harness"
)
DEFAULT_FACTORY = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/luna_validation_factory_consolidation"
)
DEFAULT_POST = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "vision_voice_provider_harness_adoption_post_dryrun_review"
)
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "controlled_provider_readiness_harness_factory_registration_dryrun"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    (
        "controlled_provider_harness_factory_registration_dryrun_policy",
        "controlled_provider_harness_factory_registration_dryrun_policy_v1.json",
    ),
    (
        "factory_registration_planning_input_review",
        "factory_registration_planning_input_review_v1.json",
    ),
    ("validation_factory_registry_candidate", "validation_factory_registry_candidate_v1.json"),
    (
        "controlled_provider_harness_registry_entry_candidate",
        "controlled_provider_harness_registry_entry_candidate_v1.json",
    ),
    (
        "validation_factory_contract_extension_dryrun_result",
        "validation_factory_contract_extension_dryrun_result_v1.json",
    ),
    (
        "provider_harness_factory_interface_dryrun_result",
        "provider_harness_factory_interface_dryrun_result_v1.json",
    ),
    (
        "provider_harness_consumer_mapping_dryrun_result",
        "provider_harness_consumer_mapping_dryrun_result_v1.json",
    ),
    (
        "provider_harness_boundary_policy_dryrun_result",
        "provider_harness_boundary_policy_dryrun_result_v1.json",
    ),
    (
        "provider_harness_anti_recursion_dryrun_result",
        "provider_harness_anti_recursion_dryrun_result_v1.json",
    ),
    (
        "deferred_consumer_register_dryrun_result",
        "deferred_consumer_register_dryrun_result_v1.json",
    ),
    (
        "validation_factory_registration_no_runtime_audit",
        "validation_factory_registration_no_runtime_audit_v1.json",
    ),
    (
        "validation_factory_registration_blocked_path_result",
        "validation_factory_registration_blocked_path_result_v1.json",
    ),
    (
        "validation_factory_registration_readiness_decision",
        "validation_factory_registration_readiness_decision_v1.json",
    ),
    ("non_claims_register", "non_claims_register_v1.json"),
)


def _write(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=DEFAULT_OUTPUT)
    p.add_argument(
        "--controlled-provider-readiness-harness-factory-registration-planning-root",
        default=DEFAULT_PLANNING,
    )
    p.add_argument(
        "--provider-harness-generalization-roadmap-decision-root",
        default=DEFAULT_ROADMAP,
    )
    p.add_argument("--controlled-provider-readiness-harness-root", default=DEFAULT_HARNESS)
    p.add_argument("--luna-validation-factory-consolidation-root", default=DEFAULT_FACTORY)
    p.add_argument(
        "--vision-voice-provider-harness-adoption-post-dryrun-review-root",
        default=DEFAULT_POST,
    )
    args = p.parse_args()

    result = run_controlled_provider_readiness_harness_factory_registration_dryrun_v1(
        controlled_provider_readiness_harness_factory_registration_planning_root=(
            args.controlled_provider_readiness_harness_factory_registration_planning_root
        ),
        provider_harness_generalization_roadmap_decision_root=(
            args.provider_harness_generalization_roadmap_decision_root
        ),
        controlled_provider_readiness_harness_root=args.controlled_provider_readiness_harness_root,
        luna_validation_factory_consolidation_root=args.luna_validation_factory_consolidation_root,
        vision_voice_provider_harness_adoption_post_dryrun_review_root=(
            args.vision_voice_provider_harness_adoption_post_dryrun_review_root
        ),
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
                "boundary_ok": sm.get("boundary_ok"),
                "final_decision": sm.get("final_decision"),
                "recommended_next_phase": sm.get("recommended_next_phase"),
                "module_count": sm.get("module_count"),
            },
            ensure_ascii=False,
        )
    )
    return 0 if sm.get("boundary_ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
