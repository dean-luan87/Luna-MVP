#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Field-First Ideal Operation Mechanism and Model Requirement Mapping v1."""

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

from capabilities.midplatform.field_first_core_ideal_operation_mechanism_and_model_requirement_mapping_v1 import (
    DEFAULT_OUTPUT,
    DEFAULT_ROLE_REDEF_ROOT,
    run_field_first_core_ideal_operation_mechanism_and_model_requirement_mapping_v1,
)

OUTPUT_FILES = (
    ("ideal_operation_mechanism_report", "ideal_operation_mechanism_report_v1.json"),
    ("ideal_operation_mechanism", "ideal_operation_mechanism_v1.json"),
    ("operation_node_registry", "operation_node_registry_v1.json"),
    ("operation_node_model_mapping", "operation_node_model_mapping_v1.json"),
    ("model_requirement_matrix", "model_requirement_matrix_v1.json"),
    ("model_document_review_template", "model_document_review_template_v1.json"),
    ("model_room_alignment_update", "model_room_alignment_update_v1.json"),
    ("self_work_vs_model_dependency_boundary", "self_work_vs_model_dependency_boundary_v1.json"),
    ("next_research_targets", "next_research_targets_v1.json"),
    ("next_route_decision", "next_route_decision_v1.json"),
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
    parser.add_argument("--role-redef-root", default=DEFAULT_ROLE_REDEF_ROOT)
    parser.add_argument("--output-root", default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    result = run_field_first_core_ideal_operation_mechanism_and_model_requirement_mapping_v1(
        role_redef_root=args.role_redef_root, output_root=args.output_root,
    )
    out = Path(args.output_root)
    out.mkdir(parents=True, exist_ok=True)
    for key, fname in OUTPUT_FILES:
        (out / fname).write_text(json.dumps(result[key], ensure_ascii=False, indent=2, default=_default) + "\n", encoding="utf-8")
    (out / "ideal_operation_mechanism_report_v1.md").write_text(result["ideal_operation_mechanism_report_md"] + "\n", encoding="utf-8")
    s = result["summary"]
    print(json.dumps({
        "output_root": str(out),
        "field_first_core_ideal_operation_mechanism_pass": s.get("field_first_core_ideal_operation_mechanism_pass"),
        "final_decision": s.get("final_decision"),
        "recommended_next_phase": s.get("recommended_next_phase"),
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
