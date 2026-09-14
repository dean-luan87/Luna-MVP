#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Controlled Provider Readiness Harness Validation Factory Registration Planning v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.controlled_provider_readiness_harness_factory_registration_planning_v1 import (
    run_controlled_provider_readiness_harness_factory_registration_planning_v1,
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
    "controlled_provider_readiness_harness_factory_registration_planning"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    (
        "controlled_provider_harness_factory_registration_planning_policy",
        "controlled_provider_harness_factory_registration_planning_policy_v1.json",
    ),
    (
        "provider_harness_generalization_roadmap_input_review",
        "provider_harness_generalization_roadmap_input_review_v1.json",
    ),
    (
        "validation_factory_existing_registry_review",
        "validation_factory_existing_registry_review_v1.json",
    ),
    (
        "controlled_provider_harness_registry_entry_plan",
        "controlled_provider_harness_registry_entry_plan_v1.json",
    ),
    (
        "validation_factory_contract_extension_plan",
        "validation_factory_contract_extension_plan_v1.json",
    ),
    (
        "provider_harness_factory_interface_plan",
        "provider_harness_factory_interface_plan_v1.json",
    ),
    (
        "provider_harness_consumer_mapping_plan",
        "provider_harness_consumer_mapping_plan_v1.json",
    ),
    (
        "provider_harness_boundary_policy_plan",
        "provider_harness_boundary_policy_plan_v1.json",
    ),
    (
        "provider_harness_anti_recursion_rule_plan",
        "provider_harness_anti_recursion_rule_plan_v1.json",
    ),
    (
        "validation_factory_registration_dryrun_plan",
        "validation_factory_registration_dryrun_plan_v1.json",
    ),
    ("deferred_consumer_register", "deferred_consumer_register_v1.json"),
    ("factory_registration_planning_decision", "factory_registration_planning_decision_v1.json"),
    ("non_claims_register", "non_claims_register_v1.json"),
)


def _write(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=DEFAULT_OUTPUT)
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

    result = run_controlled_provider_readiness_harness_factory_registration_planning_v1(
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
                "proposed_seventh_module": sm.get("proposed_seventh_module"),
            },
            ensure_ascii=False,
        )
    )
    return 0 if sm.get("boundary_ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
