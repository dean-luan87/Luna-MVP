#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Field-First Model I/O Compatibility Precheck v1."""

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

from capabilities.midplatform.field_first_core_model_document_capability_review_v1 import (
    DEFAULT_OUTPUT as DEFAULT_DOC_REVIEW_ROOT,
)
from capabilities.midplatform.field_first_core_model_io_compatibility_precheck_v1 import (
    DEFAULT_OUTPUT,
    run_field_first_core_model_io_compatibility_precheck_v1,
)

OUTPUT_FILES = (
    ("model_io_compatibility_precheck_report", "model_io_compatibility_precheck_report_v1.json"),
    ("model_io_review_item_registry", "model_io_review_item_registry_v1.json"),
    ("model_io_to_candidate_mapping", "model_io_to_candidate_mapping_v1.json"),
    ("candidate_schema_compatibility_matrix", "candidate_schema_compatibility_matrix_v1.json"),
    ("skeleton_schema_adjustment_plan", "skeleton_schema_adjustment_plan_v1.json"),
    ("model_io_gap_register", "model_io_gap_register_v1.json"),
    ("field_first_skeleton_io_requirements", "field_first_skeleton_io_requirements_v1.json"),
    ("candidate_common_payload_requirements", "candidate_common_payload_requirements_v1.json"),
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
    parser.add_argument("--doc-review-root", default=DEFAULT_DOC_REVIEW_ROOT)
    parser.add_argument("--output-root", default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    result = run_field_first_core_model_io_compatibility_precheck_v1(
        doc_review_root=args.doc_review_root, output_root=args.output_root,
    )
    out = Path(args.output_root)
    out.mkdir(parents=True, exist_ok=True)
    for key, fname in OUTPUT_FILES:
        (out / fname).write_text(json.dumps(result[key], ensure_ascii=False, indent=2, default=_default) + "\n", encoding="utf-8")
    (out / "model_io_compatibility_precheck_report_v1.md").write_text(result["model_io_compatibility_precheck_report_md"] + "\n", encoding="utf-8")
    s = result["summary"]
    print(json.dumps({
        "output_root": str(out),
        "field_first_core_model_io_compatibility_precheck_pass": s.get("field_first_core_model_io_compatibility_precheck_pass"),
        "final_decision": s.get("final_decision"),
        "recommended_next_phase": s.get("recommended_next_phase"),
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
