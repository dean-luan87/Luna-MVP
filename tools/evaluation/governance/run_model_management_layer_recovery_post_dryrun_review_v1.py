#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Model Management Layer Recovery Post-DryRun Review v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.model_management_layer_recovery_post_dryrun_review_v1 import (
    run_model_management_layer_recovery_post_dryrun_review_v1,
)

DEFAULT_DRYRUN = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/model_management_layer_recovery_dryrun"
)
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "model_management_layer_recovery_post_dryrun_review"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    ("model_management_dryrun_input_review", "model_management_dryrun_input_review_v1.json"),
    ("model_registry_review", "model_registry_review_v1.json"),
    ("skill_registry_review", "skill_registry_review_v1.json"),
    ("model_capability_descriptor_review", "model_capability_descriptor_review_v1.json"),
    ("model_health_state_candidate_review", "model_health_state_candidate_review_v1.json"),
    ("model_switching_candidate_review", "model_switching_candidate_review_v1.json"),
    ("model_output_contract_review", "model_output_contract_review_v1.json"),
    ("model_runtime_boundary_review", "model_runtime_boundary_review_v1.json"),
    ("model_provider_governance_review", "model_provider_governance_review_v1.json"),
    ("model_management_blocked_path_review", "model_management_blocked_path_review_v1.json"),
    ("model_management_recovery_closure_decision", "model_management_recovery_closure_decision_v1.json"),
    ("next_model_optimization_readiness_decision", "next_model_optimization_readiness_decision_v1.json"),
    ("non_claims_register", "non_claims_register_v1.json"),
)


def _write(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=DEFAULT_OUTPUT)
    p.add_argument("--model-management-layer-recovery-dryrun-root", default=DEFAULT_DRYRUN)
    args = p.parse_args()

    result = run_model_management_layer_recovery_post_dryrun_review_v1(
        model_management_layer_recovery_dryrun_root=args.model_management_layer_recovery_dryrun_root,
        review_output_root=args.output_root,
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
                "governance_skeleton_consumable": sm.get("governance_skeleton_consumable"),
            },
            ensure_ascii=False,
        )
    )
    return 0 if sm.get("boundary_ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
