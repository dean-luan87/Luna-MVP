#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Seed Core Drive Signal Contract DryRunAndReview v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.seed_core_drive_signal_contract_dryrun_and_review_v1 import (
    run_seed_core_drive_signal_contract_dryrun_and_review_v1,
)

DEFAULT_PLANNING = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/seed_core_drive_signal_contract_planning"
)
DEFAULT_SC_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "seed_core_pluggable_layer_architecture_dryrun_and_review"
)
DEFAULT_CZ_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_cognitive_zoning_architecture_dryrun_and_review"
)
DEFAULT_VNEXT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/midplatform_vnext_architecture_realignment_planning"
)
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "seed_core_drive_signal_contract_dryrun_and_review"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    ("drive_signal_contract_dryrun_review_policy", "drive_signal_contract_dryrun_review_policy_v1.json"),
    (
        "drive_signal_contract_planning_input_review",
        "drive_signal_contract_planning_input_review_v1.json",
    ),
    ("seed_core_drive_signal_model_candidate", "seed_core_drive_signal_model_candidate_v1.json"),
    ("sample_drive_signal_candidate", "sample_drive_signal_candidate_v1.json"),
    ("sample_seed_core_signal_candidate", "sample_seed_core_signal_candidate_v1.json"),
    ("sample_seed_core_hint_candidate", "sample_seed_core_hint_candidate_v1.json"),
    ("seed_core_signal_taxonomy_review", "seed_core_signal_taxonomy_review_v1.json"),
    ("survival_drive_signal_dryrun_review", "survival_drive_signal_dryrun_review_v1.json"),
    ("task_drive_signal_dryrun_review", "task_drive_signal_dryrun_review_v1.json"),
    ("resource_governance_signal_dryrun_review", "resource_governance_signal_dryrun_review_v1.json"),
    ("health_management_signal_dryrun_review", "health_management_signal_dryrun_review_v1.json"),
    ("system_optimization_signal_dryrun_review", "system_optimization_signal_dryrun_review_v1.json"),
    (
        "autonomous_world_observation_signal_dryrun_review",
        "autonomous_world_observation_signal_dryrun_review_v1.json",
    ),
    ("emotion_engine_signal_dryrun_review", "emotion_engine_signal_dryrun_review_v1.json"),
    ("evolutionary_recursion_signal_dryrun_review", "evolutionary_recursion_signal_dryrun_review_v1.json"),
    ("drive_signal_priority_policy_review", "drive_signal_priority_policy_review_v1.json"),
    ("drive_signal_conflict_policy_review", "drive_signal_conflict_policy_review_v1.json"),
    ("drive_signal_zone_handoff_review", "drive_signal_zone_handoff_review_v1.json"),
    (
        "drive_signal_information_integration_handoff_review",
        "drive_signal_information_integration_handoff_review_v1.json",
    ),
    (
        "drive_signal_decision_center_boundary_review",
        "drive_signal_decision_center_boundary_review_v1.json",
    ),
    (
        "drive_signal_controlled_runtime_boundary_review",
        "drive_signal_controlled_runtime_boundary_review_v1.json",
    ),
    ("drive_signal_traceability_review", "drive_signal_traceability_review_v1.json"),
    ("drive_signal_boundary_audit", "drive_signal_boundary_audit_v1.json"),
    ("drive_signal_blocked_path_result", "drive_signal_blocked_path_result_v1.json"),
    ("drive_signal_closure_decision", "drive_signal_closure_decision_v1.json"),
    ("next_route_readiness_decision", "next_route_readiness_decision_v1.json"),
    ("non_claims_register", "non_claims_register_v1.json"),
)


def _write(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=DEFAULT_OUTPUT)
    p.add_argument("--drive-signal-planning-root", default=DEFAULT_PLANNING)
    p.add_argument("--seed-core-pluggable-dryrun-root", default=DEFAULT_SC_DR)
    p.add_argument("--cognitive-zoning-dryrun-root", default=DEFAULT_CZ_DR)
    p.add_argument("--vnext-realignment-root", default=DEFAULT_VNEXT)
    args = p.parse_args()

    result = run_seed_core_drive_signal_contract_dryrun_and_review_v1(
        seed_core_drive_signal_contract_planning_root=args.drive_signal_planning_root,
        seed_core_pluggable_layer_architecture_dryrun_and_review_root=args.seed_core_pluggable_dryrun_root,
        midplatform_cognitive_zoning_architecture_dryrun_and_review_root=args.cognitive_zoning_dryrun_root,
        midplatform_vnext_architecture_realignment_planning_root=args.vnext_realignment_root,
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
            },
            ensure_ascii=False,
        )
    )
    return 0 if sm.get("dryrun_and_review_pass") else 1


if __name__ == "__main__":
    raise SystemExit(main())
