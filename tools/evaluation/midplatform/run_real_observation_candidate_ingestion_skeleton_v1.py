#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Real Observation Candidate Ingestion Skeleton v1."""

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

from capabilities.midplatform.field_first_minimal_real_model_adapter_integration_planning_v1 import (
    DEFAULT_OUTPUT as DEFAULT_PLANNING_ROOT,
)
from capabilities.midplatform.real_observation_candidate_ingestion_skeleton_v1 import (
    DEFAULT_OUTPUT,
    run_real_observation_candidate_ingestion_skeleton_v1,
)

OUTPUT_FILES = (
    ("real_observation_candidate_ingestion_skeleton_report", "real_observation_candidate_ingestion_skeleton_report_v1.json"),
    ("detector_output_mock_contract", "detector_output_mock_contract_v1.json"),
    ("supervision_normalized_detection_contract", "supervision_normalized_detection_contract_v1.json"),
    ("object_observation_candidate_contract", "object_observation_candidate_contract_v1.json"),
    ("detector_to_observation_ingestion_mapping", "detector_to_observation_ingestion_mapping_v1.json"),
    ("depth_missing_fallback_execution_policy", "depth_missing_fallback_execution_policy_v1.json"),
    ("real_observation_ingestion_mock_case_results", "real_observation_ingestion_mock_case_results_v1.json"),
    ("rejected_detection_policy", "rejected_detection_policy_v1.json"),
    ("field_first_core_readiness_review", "field_first_core_readiness_review_v1.json"),
    ("non_execution_boundary_review", "non_execution_boundary_review_v1.json"),
    ("prohibited_scope", "prohibited_scope_v1.json"),
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
    parser.add_argument("--planning-root", default=DEFAULT_PLANNING_ROOT)
    parser.add_argument("--output-root", default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    result = run_real_observation_candidate_ingestion_skeleton_v1(
        planning_root=args.planning_root,
        output_root=args.output_root,
    )
    out = Path(args.output_root)
    out.mkdir(parents=True, exist_ok=True)
    for key, fname in OUTPUT_FILES:
        (out / fname).write_text(json.dumps(result[key], ensure_ascii=False, indent=2, default=_default) + "\n", encoding="utf-8")
    (out / "real_observation_candidate_ingestion_skeleton_report_v1.md").write_text(
        result["real_observation_candidate_ingestion_skeleton_report_md"] + "\n", encoding="utf-8",
    )
    s = result["summary"]
    print(json.dumps({
        "output_root": str(out),
        "real_observation_candidate_ingestion_skeleton_pass": s.get("real_observation_candidate_ingestion_skeleton_pass"),
        "final_decision": s.get("final_decision"),
        "recommended_next_phase": s.get("recommended_next_phase"),
        "observation_candidate_count": s.get("observation_candidate_count"),
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
