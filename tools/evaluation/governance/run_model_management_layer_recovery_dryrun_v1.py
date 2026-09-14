#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Model Management Layer Recovery DryRun v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.model_management_layer_recovery_dryrun_v1 import (
    run_model_management_layer_recovery_dryrun_v1,
)

WS = "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out"
DEFAULT_OUTPUT = f"{WS}/model_management_layer_recovery_dryrun"


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=DEFAULT_OUTPUT)
    p.add_argument(
        "--model-management-layer-recovery-planning-root",
        default=f"{WS}/model_management_layer_recovery_planning",
    )
    p.add_argument(
        "--task-response-candidate-midplatform-integration-post-dryrun-review-root",
        default=f"{WS}/task_response_candidate_midplatform_integration_post_dryrun_review",
    )
    p.add_argument(
        "--luna-validation-factory-consolidation-root",
        default=f"{WS}/luna_validation_factory_consolidation",
    )
    args = p.parse_args()

    result = run_model_management_layer_recovery_dryrun_v1(
        model_management_layer_recovery_planning_root=args.model_management_layer_recovery_planning_root,
        task_response_candidate_midplatform_integration_post_dryrun_review_root=(
            args.task_response_candidate_midplatform_integration_post_dryrun_review_root
        ),
        luna_validation_factory_consolidation_root=args.luna_validation_factory_consolidation_root,
        output_root=args.output_root,
    )

    out_root = Path(result["output_root"])
    for filename, payload in result["artifacts"].items():
        path = out_root / filename
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    sm = result["artifacts"]["summary.json"]
    print(
        json.dumps(
            {
                "output_root": str(out_root),
                "boundary_ok": sm.get("boundary_ok"),
                "final_decision": sm.get("final_decision"),
                "model_entries": sm.get("model_registry_entry_count"),
                "skill_entries": sm.get("skill_registry_entry_count"),
            },
            ensure_ascii=False,
        )
    )
    return 0 if sm.get("boundary_ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
