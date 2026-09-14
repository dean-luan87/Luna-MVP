#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Model-SLAM readiness chain recovery repair v1."""

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

from capabilities.midplatform.model_slam_readiness_chain_recovery_repair_items_v1 import (
    DEFAULT_OUTPUT,
    PASS_FLAG,
)
from capabilities.midplatform.model_slam_readiness_chain_recovery_repair_v1 import (
    run_model_slam_readiness_chain_recovery_repair_v1,
)

OUTPUT_FILES = (
    ("model_slam_readiness_chain_recovery_repair_report", "model_slam_readiness_chain_recovery_repair_report_v1.json"),
    ("batch_detection_input_review", "batch_detection_input_review_v1.json"),
    ("group_m_safe_candidate_execution_matrix", "group_m_safe_candidate_execution_matrix_v1.json"),
    ("model_workflow_protocol_reuse_review_repair_review", "model_workflow_protocol_reuse_review_repair_review_v1.json"),
    ("model_adapter_priority_sequence_planning_repair_review", "model_adapter_priority_sequence_planning_repair_review_v1.json"),
    ("slam_spatial_mapping_model_smoke_io_repair_review", "slam_spatial_mapping_model_smoke_io_repair_review_v1.json"),
    ("slam_spatial_mapping_adapter_skeleton_repair_review", "slam_spatial_mapping_adapter_skeleton_repair_review_v1.json"),
    ("slam_spatial_mapping_task_collaboration_planning_repair_review", "slam_spatial_mapping_task_collaboration_planning_repair_review_v1.json"),
    ("slam_spatial_mapping_task_collaboration_revalidation_repair_review", "slam_spatial_mapping_task_collaboration_revalidation_repair_review_v1.json"),
    ("per_stage_original_rerun_results", "per_stage_original_rerun_results_v1.json"),
    ("per_stage_final_decision_alignment_review", "per_stage_final_decision_alignment_review_v1.json"),
    ("per_stage_no_model_execution_review", "per_stage_no_model_execution_review_v1.json"),
    ("per_stage_no_sensor_execution_review", "per_stage_no_sensor_execution_review_v1.json"),
    ("per_stage_no_world_model_assembly_review", "per_stage_no_world_model_assembly_review_v1.json"),
    ("per_stage_no_task_reasoning_review", "per_stage_no_task_reasoning_review_v1.json"),
    ("verifier_locator_repair_review", "verifier_locator_repair_review_v1.json"),
    ("schema_output_repair_review", "schema_output_repair_review_v1.json"),
    ("downstream_expectation_repair_review", "downstream_expectation_repair_review_v1.json"),
    ("canonical_checkpoint_scan_only_after_recovery_repair", "canonical_checkpoint_scan_only_after_recovery_repair_v1.json"),
    ("canonical_checkpoint_topdown_after_recovery_repair", "canonical_checkpoint_topdown_after_recovery_repair_v1.json"),
    ("no_issue_review_created_review", "no_issue_review_created_review_v1.json"),
    ("no_gap_review_created_review", "no_gap_review_created_review_v1.json"),
    ("no_rerun_review_created_review", "no_rerun_review_created_review_v1.json"),
    ("no_protocol_change_review", "no_protocol_change_review_v1.json"),
    ("no_model_execution_review", "no_model_execution_review_v1.json"),
    ("no_sensor_execution_review", "no_sensor_execution_review_v1.json"),
    ("no_world_model_assembly_review", "no_world_model_assembly_review_v1.json"),
    ("owner_constraint_compliance_review", "owner_constraint_compliance_review_v1.json"),
    ("file_size_governance_review", "file_size_governance_review_v1.json"),
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
    result = run_model_slam_readiness_chain_recovery_repair_v1(output_root=args.output_root)
    out = Path(args.output_root)
    out.mkdir(parents=True, exist_ok=True)
    for key, fname in OUTPUT_FILES:
        (out / fname).write_text(
            json.dumps(result[key], ensure_ascii=False, indent=2, default=_default) + "\n",
            encoding="utf-8",
        )
    (out / "model_slam_readiness_chain_recovery_repair_report_v1.md").write_text(
        result["model_slam_readiness_chain_recovery_repair_report_md"] + "\n",
        encoding="utf-8",
    )
    verify_proc = __import__("subprocess").run(
        [sys.executable, str(REPO_ROOT / "tools/evaluation/midplatform/verify_model_slam_readiness_chain_recovery_repair_v1.py"), "--output-root", str(out)],
        capture_output=True,
        text=True,
    )
    s = result["summary"]
    print(
        json.dumps(
            {
                "output_root": str(out),
                PASS_FLAG: s.get(PASS_FLAG),
                "group_m_all_go_readable": s.get("group_m_all_go_readable"),
                "go_stage_count_after_repair": s.get("go_stage_count_after_repair"),
                "verifier_exit_code": verify_proc.returncode,
                "final_decision": s.get("final_decision"),
                "recommended_next_phase": s.get("recommended_next_phase"),
            },
            ensure_ascii=False,
        )
    )
    return 0 if s.get(PASS_FLAG) and verify_proc.returncode == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
