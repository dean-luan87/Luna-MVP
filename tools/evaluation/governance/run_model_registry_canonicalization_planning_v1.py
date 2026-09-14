#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Model Registry Canonicalization Planning v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.model_registry_canonicalization_planning_v1 import (
    run_model_registry_canonicalization_planning_v1,
)

DEFAULT_ROADMAP = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/model_management_layer_roadmap_decision"
)
DEFAULT_POST_REVIEW = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "model_management_layer_recovery_post_dryrun_review"
)
DEFAULT_DRYRUN = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/model_management_layer_recovery_dryrun"
)
DEFAULT_RECOVERY_PLANNING = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/model_management_layer_recovery_planning"
)
DEFAULT_FACTORY = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/luna_validation_factory_consolidation"
)
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/model_registry_canonicalization_planning"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    ("model_registry_canonicalization_planning_policy", "model_registry_canonicalization_planning_policy_v1.json"),
    ("roadmap_decision_input_review", "roadmap_decision_input_review_v1.json"),
    ("model_registry_version_input_review", "model_registry_version_input_review_v1.json"),
    ("model_registry_schema_v0_planning", "model_registry_schema_v0_planning_v1.json"),
    ("model_registry_canonical_v0_table_plan", "model_registry_canonical_v0_table_plan_v1.json"),
    ("model_registry_entry_normalization_rules", "model_registry_entry_normalization_rules_v1.json"),
    ("model_domain_taxonomy_v0", "model_domain_taxonomy_v0.json"),
    ("provider_type_taxonomy_v0", "provider_type_taxonomy_v0.json"),
    ("runtime_mode_taxonomy_v0", "runtime_mode_taxonomy_v0.json"),
    ("capability_tag_taxonomy_v0", "capability_tag_taxonomy_v0.json"),
    ("model_input_output_contract_binding", "model_input_output_contract_binding_v1.json"),
    ("model_health_and_fallback_binding", "model_health_and_fallback_binding_v1.json"),
    ("skill_registry_relationship_plan", "skill_registry_relationship_plan_v1.json"),
    ("candidate_output_contract_binding_plan", "candidate_output_contract_binding_plan_v1.json"),
    ("version_upgrade_and_deprecation_policy", "version_upgrade_and_deprecation_policy_v1.json"),
    ("canonical_registry_generation_dryrun_plan", "canonical_registry_generation_dryrun_plan_v1.json"),
    (
        "model_registry_canonicalization_non_claims_register",
        "model_registry_canonicalization_non_claims_register_v1.json",
    ),
    ("model_registry_canonicalization_planning_decision", "model_registry_canonicalization_planning_decision_v1.json"),
)


def _write(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=DEFAULT_OUTPUT)
    p.add_argument("--model-management-layer-roadmap-decision-root", default=DEFAULT_ROADMAP)
    p.add_argument("--model-management-layer-recovery-post-dryrun-review-root", default=DEFAULT_POST_REVIEW)
    p.add_argument("--model-management-layer-recovery-dryrun-root", default=DEFAULT_DRYRUN)
    p.add_argument("--model-management-layer-recovery-planning-root", default=DEFAULT_RECOVERY_PLANNING)
    p.add_argument("--luna-validation-factory-consolidation-root", default=DEFAULT_FACTORY)
    args = p.parse_args()

    result = run_model_registry_canonicalization_planning_v1(
        model_management_layer_roadmap_decision_root=args.model_management_layer_roadmap_decision_root,
        model_management_layer_recovery_post_dryrun_review_root=(
            args.model_management_layer_recovery_post_dryrun_review_root
        ),
        model_management_layer_recovery_dryrun_root=args.model_management_layer_recovery_dryrun_root,
        model_management_layer_recovery_planning_root=args.model_management_layer_recovery_planning_root,
        luna_validation_factory_consolidation_root=args.luna_validation_factory_consolidation_root,
        planning_output_root=args.output_root,
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
                "canonical_entry_count_planned": sm.get("canonical_entry_count_planned"),
            },
            ensure_ascii=False,
        )
    )
    return 0 if sm.get("boundary_ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
