#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Field Scene Small Range Construction Core Definition v1."""

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

from capabilities.midplatform.field_first_core_model_io_compatibility_precheck_v1 import (
    DEFAULT_OUTPUT as DEFAULT_IO_PRECHECK_ROOT,
)
from capabilities.midplatform.field_scene_small_range_construction_core_definition_v1 import (
    DEFAULT_OUTPUT,
    run_field_scene_small_range_construction_core_definition_v1,
)

OUTPUT_FILES = (
    ("field_scene_small_range_construction_report", "field_scene_small_range_construction_report_v1.json"),
    ("field_scene_scope_definition", "field_scene_scope_definition_v1.json"),
    ("field_scene_input_candidate_contract", "field_scene_input_candidate_contract_v1.json"),
    ("field_scene_output_candidate_contract", "field_scene_output_candidate_contract_v1.json"),
    ("field_scene_processing_flow", "field_scene_processing_flow_v1.json"),
    ("field_scene_mock_case_registry", "field_scene_mock_case_registry_v1.json"),
    ("field_scene_mock_case_results", "field_scene_mock_case_results_v1.json"),
    ("field_entity_candidate_registry", "field_entity_candidate_registry_v1.json"),
    ("depth_uncertainty_policy", "depth_uncertainty_policy_v1.json"),
    ("field_zone_assignment_policy", "field_zone_assignment_policy_v1.json"),
    ("prohibited_scope", "prohibited_scope_v1.json"),
    ("next_stage_split_plan", "next_stage_split_plan_v1.json"),
    ("do_not_misclassify_rules", "do_not_misclassify_rules_v1.json"),
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
    parser.add_argument("--io-precheck-root", default=DEFAULT_IO_PRECHECK_ROOT)
    parser.add_argument("--output-root", default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    result = run_field_scene_small_range_construction_core_definition_v1(
        io_precheck_root=args.io_precheck_root, output_root=args.output_root,
    )
    out = Path(args.output_root)
    out.mkdir(parents=True, exist_ok=True)
    for key, fname in OUTPUT_FILES:
        (out / fname).write_text(json.dumps(result[key], ensure_ascii=False, indent=2, default=_default) + "\n", encoding="utf-8")
    (out / "field_scene_small_range_construction_report_v1.md").write_text(result["field_scene_small_range_construction_report_md"] + "\n", encoding="utf-8")
    s = result["summary"]
    print(json.dumps({
        "output_root": str(out),
        "field_scene_small_range_construction_pass": s.get("field_scene_small_range_construction_pass"),
        "final_decision": s.get("final_decision"),
        "recommended_next_phase": s.get("recommended_next_phase"),
        "mock_case_count": s.get("mock_case_count"),
        "entity_candidate_count": s.get("entity_candidate_count"),
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
