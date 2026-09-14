#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Field-First Minimal Real Model Adapter Integration Planning v1."""

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

from capabilities.midplatform.field_first_core_logic_formal_implementation_v1 import (
    DEFAULT_OUTPUT as DEFAULT_CORE_LOGIC_ROOT,
)
from capabilities.midplatform.field_first_minimal_real_model_adapter_integration_planning_v1 import (
    DEFAULT_OUTPUT,
    run_field_first_minimal_real_model_adapter_integration_planning_v1,
)

OUTPUT_FILES = (
    ("minimal_real_model_adapter_integration_planning_report", "minimal_real_model_adapter_integration_planning_report_v1.json"),
    ("minimal_detector_adapter_plan", "minimal_detector_adapter_plan_v1.json"),
    ("supervision_normalization_plan", "supervision_normalization_plan_v1.json"),
    ("real_observation_candidate_ingestion_plan", "real_observation_candidate_ingestion_plan_v1.json"),
    ("detector_output_to_observation_candidate_mapping", "detector_output_to_observation_candidate_mapping_v1.json"),
    ("depth_missing_fallback_policy", "depth_missing_fallback_policy_v1.json"),
    ("real_model_success_path_readiness_plan", "real_model_success_path_readiness_plan_v1.json"),
    ("model_download_authorization_status", "model_download_authorization_status_v1.json"),
    ("minimal_real_model_planning_case_registry", "minimal_real_model_planning_case_registry_v1.json"),
    ("minimal_real_model_planning_rules", "minimal_real_model_planning_rules_v1.json"),
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
    parser.add_argument("--core-logic-root", default=DEFAULT_CORE_LOGIC_ROOT)
    parser.add_argument("--output-root", default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    result = run_field_first_minimal_real_model_adapter_integration_planning_v1(
        core_logic_root=args.core_logic_root,
        output_root=args.output_root,
    )
    out = Path(args.output_root)
    out.mkdir(parents=True, exist_ok=True)
    for key, fname in OUTPUT_FILES:
        (out / fname).write_text(json.dumps(result[key], ensure_ascii=False, indent=2, default=_default) + "\n", encoding="utf-8")
    (out / "minimal_real_model_adapter_integration_planning_report_v1.md").write_text(
        result["minimal_real_model_adapter_integration_planning_report_md"] + "\n", encoding="utf-8",
    )
    s = result["summary"]
    print(json.dumps({
        "output_root": str(out),
        "minimal_real_model_adapter_integration_planning_pass": s.get("minimal_real_model_adapter_integration_planning_pass"),
        "final_decision": s.get("final_decision"),
        "recommended_next_phase": s.get("recommended_next_phase"),
        "mock_case_count": s.get("mock_case_count"),
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
