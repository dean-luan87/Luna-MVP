#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run model-SLAM readiness chain batch detection and recovery plan v1."""

from __future__ import annotations

import dataclasses
import json
import sys
from argparse import ArgumentParser
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.midplatform.model_slam_readiness_chain_batch_detection_and_recovery_plan_v1 import (
    run_model_slam_readiness_chain_batch_detection_and_recovery_plan_v1,
)
from capabilities.midplatform.model_slam_readiness_chain_batch_detection_items_v1 import (
    DEFAULT_OUTPUT,
    PASS_FLAG,
)

OUTPUT_FILES = (
    ("model_slam_readiness_chain_batch_detection_report", "model_slam_readiness_chain_batch_detection_report_v1.json"),
    ("group_m_stage_inventory", "group_m_stage_inventory_v1.json"),
    ("group_m_checkpoint_status_matrix", "group_m_checkpoint_status_matrix_v1.json"),
    ("group_m_runner_verifier_locator_matrix", "group_m_runner_verifier_locator_matrix_v1.json"),
    ("group_m_gap_classification", "group_m_gap_classification_v1.json"),
    ("model_workflow_reuse_review_diagnostic", "model_workflow_reuse_review_diagnostic_v1.json"),
    ("model_adapter_priority_sequence_diagnostic", "model_adapter_priority_sequence_diagnostic_v1.json"),
    ("slam_p0_smoke_io_diagnostic", "slam_p0_smoke_io_diagnostic_v1.json"),
    ("slam_p0_adapter_skeleton_diagnostic", "slam_p0_adapter_skeleton_diagnostic_v1.json"),
    ("slam_p0_task_collaboration_planning_diagnostic", "slam_p0_task_collaboration_planning_diagnostic_v1.json"),
    ("slam_p0_revalidation_diagnostic", "slam_p0_revalidation_diagnostic_v1.json"),
    ("verifier_locator_gap_matrix", "verifier_locator_gap_matrix_v1.json"),
    ("schema_output_gap_matrix", "schema_output_gap_matrix_v1.json"),
    ("downstream_expectation_gap_matrix", "downstream_expectation_gap_matrix_v1.json"),
    ("evidence_traceability_gap_matrix", "evidence_traceability_gap_matrix_v1.json"),
    ("model_execution_leakage_review", "model_execution_leakage_review_v1.json"),
    ("safe_model_slam_readiness_repair_candidates", "safe_model_slam_readiness_repair_candidates_v1.json"),
    ("stages_requiring_individual_repair", "stages_requiring_individual_repair_v1.json"),
    ("group_m_recovery_plan", "group_m_recovery_plan_v1.json"),
    ("no_model_execution_review", "no_model_execution_review_v1.json"),
    ("no_sensor_execution_review", "no_sensor_execution_review_v1.json"),
    ("no_world_model_assembly_review", "no_world_model_assembly_review_v1.json"),
    ("no_task_reasoning_review", "no_task_reasoning_review_v1.json"),
    ("no_issue_review_created_review", "no_issue_review_created_review_v1.json"),
    ("no_protocol_change_review", "no_protocol_change_review_v1.json"),
    ("owner_constraint_compliance_review", "owner_constraint_compliance_review_v1.json"),
    ("summary", "summary.json"),
)


def _default(obj: Any) -> Any:
    if dataclasses.is_dataclass(obj):
        return dataclasses.asdict(obj)
    if isinstance(obj, tuple):
        return list(obj)
    return str(obj)


def main() -> int:
    parser = ArgumentParser()
    parser.add_argument("--output-root", default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    result = run_model_slam_readiness_chain_batch_detection_and_recovery_plan_v1(output_root=args.output_root)
    out = Path(args.output_root)
    out.mkdir(parents=True, exist_ok=True)
    for key, fname in OUTPUT_FILES:
        (out / fname).write_text(
            json.dumps(result[key], ensure_ascii=False, indent=2, default=_default) + "\n",
            encoding="utf-8",
        )
    (out / "model_slam_readiness_chain_batch_detection_report_v1.md").write_text(
        result["model_slam_readiness_chain_batch_detection_report_md"] + "\n",
        encoding="utf-8",
    )
    s = result["summary"]
    print(
        json.dumps(
            {
                "output_root": str(out),
                PASS_FLAG: s.get(PASS_FLAG),
                "go_stage_count": s.get("go_stage_count"),
                "first_failed_stage_key": s.get("first_failed_stage_key"),
                "safe_readiness_repair_candidate_count": s.get("safe_readiness_repair_candidate_count"),
                "ready_for_slam_readiness_repair": s.get("ready_for_slam_readiness_repair"),
                "final_decision": s.get("final_decision"),
                "recommended_next_phase": s.get("recommended_next_phase"),
            },
            ensure_ascii=False,
        )
    )
    return 0 if s.get(PASS_FLAG) else 1


if __name__ == "__main__":
    raise SystemExit(main())
