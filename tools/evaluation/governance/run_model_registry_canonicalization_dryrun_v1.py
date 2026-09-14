#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Model Registry Canonicalization DryRun v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.model_registry_canonicalization_dryrun_v1 import (
    run_model_registry_canonicalization_dryrun_v1,
)

DEFAULT_PLANNING = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/model_registry_canonicalization_planning"
)
DEFAULT_ROADMAP = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/model_management_layer_roadmap_decision"
)
DEFAULT_RECOVERY_DRYRUN = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/model_management_layer_recovery_dryrun"
)
DEFAULT_FACTORY = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/luna_validation_factory_consolidation"
)
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/model_registry_canonicalization_dryrun"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    ("model_registry_canonicalization_dryrun_policy", "model_registry_canonicalization_dryrun_policy_v1.json"),
    ("canonicalization_planning_input_review", "canonicalization_planning_input_review_v1.json"),
    ("model_registry_canonical_v0_candidate", "model_registry_canonical_v0_candidate.json"),
    ("model_registry_schema_v0_validation_result", "model_registry_schema_v0_validation_result_v1.json"),
    ("canonical_entry_validation_matrix", "canonical_entry_validation_matrix_v1.json"),
    ("model_domain_taxonomy_validation", "model_domain_taxonomy_validation_v1.json"),
    ("provider_type_taxonomy_validation", "provider_type_taxonomy_validation_v1.json"),
    ("runtime_mode_taxonomy_validation", "runtime_mode_taxonomy_validation_v1.json"),
    ("capability_tag_taxonomy_validation", "capability_tag_taxonomy_validation_v1.json"),
    ("model_input_output_contract_binding_result", "model_input_output_contract_binding_result_v1.json"),
    ("model_health_and_fallback_binding_result", "model_health_and_fallback_binding_result_v1.json"),
    ("skill_registry_relationship_validation", "skill_registry_relationship_validation_v1.json"),
    ("candidate_output_contract_binding_result", "candidate_output_contract_binding_result_v1.json"),
    ("version_policy_validation_result", "version_policy_validation_result_v1.json"),
    ("model_registry_runtime_boundary_audit", "model_registry_runtime_boundary_audit_v1.json"),
    ("model_registry_blocked_path_result", "model_registry_blocked_path_result_v1.json"),
    (
        "model_registry_canonicalization_dryrun_readiness_decision",
        "model_registry_canonicalization_dryrun_readiness_decision_v1.json",
    ),
    ("non_claims_register", "non_claims_register_v1.json"),
)


def _write(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=DEFAULT_OUTPUT)
    p.add_argument("--model-registry-canonicalization-planning-root", default=DEFAULT_PLANNING)
    p.add_argument("--model-management-layer-roadmap-decision-root", default=DEFAULT_ROADMAP)
    p.add_argument("--model-management-layer-recovery-dryrun-root", default=DEFAULT_RECOVERY_DRYRUN)
    p.add_argument("--luna-validation-factory-consolidation-root", default=DEFAULT_FACTORY)
    args = p.parse_args()

    result = run_model_registry_canonicalization_dryrun_v1(
        model_registry_canonicalization_planning_root=args.model_registry_canonicalization_planning_root,
        model_management_layer_roadmap_decision_root=args.model_management_layer_roadmap_decision_root,
        model_management_layer_recovery_dryrun_root=args.model_management_layer_recovery_dryrun_root,
        luna_validation_factory_consolidation_root=args.luna_validation_factory_consolidation_root,
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
                "canonical_entry_count": sm.get("canonical_entry_count"),
            },
            ensure_ascii=False,
        )
    )
    return 0 if sm.get("boundary_ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
