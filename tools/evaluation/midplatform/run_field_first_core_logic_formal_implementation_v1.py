#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Field-First Core Logic Formal Implementation v1."""

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
    DEFAULT_OUTPUT,
    run_field_first_core_logic_formal_implementation_v1,
)

OUTPUT_FILES = (
    ("field_first_core_logic_formal_implementation_report", "field_first_core_logic_formal_implementation_report_v1.json"),
    ("field_first_core_input_package_contract", "field_first_core_input_package_contract_v1.json"),
    ("field_first_core_pipeline_registry", "field_first_core_pipeline_registry_v1.json"),
    ("field_first_core_result_candidate_registry", "field_first_core_result_candidate_registry_v1.json"),
    ("field_first_core_consistency_validation_results", "field_first_core_consistency_validation_results_v1.json"),
    ("field_first_core_mock_case_results", "field_first_core_mock_case_results_v1.json"),
    ("decision_readiness_summary_registry", "decision_readiness_summary_registry_v1.json"),
    ("warning_missing_information_propagation_review", "warning_missing_information_propagation_review_v1.json"),
    ("non_execution_boundary_review", "non_execution_boundary_review_v1.json"),
    ("next_stage_split_plan", "next_stage_split_plan_v1.json"),
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
    parser.add_argument("--repo-root", default=str(REPO_ROOT))
    args = parser.parse_args()
    result = run_field_first_core_logic_formal_implementation_v1(
        output_root=args.output_root,
        repo_root=args.repo_root,
    )
    out = Path(args.output_root)
    out.mkdir(parents=True, exist_ok=True)
    for key, fname in OUTPUT_FILES:
        (out / fname).write_text(json.dumps(result[key], ensure_ascii=False, indent=2, default=_default) + "\n", encoding="utf-8")
    (out / "field_first_core_logic_formal_implementation_report_v1.md").write_text(
        result["field_first_core_logic_formal_implementation_report_md"] + "\n", encoding="utf-8",
    )
    s = result["summary"]
    print(json.dumps({
        "output_root": str(out),
        "field_first_core_logic_formal_implementation_pass": s.get("field_first_core_logic_formal_implementation_pass"),
        "all_four_upstream_skeletons_go": s.get("all_four_upstream_skeletons_go"),
        "final_decision": s.get("final_decision"),
        "recommended_next_phase": s.get("recommended_next_phase"),
        "mock_case_count": s.get("mock_case_count"),
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
