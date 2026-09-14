#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Field-First Model Document Capability Review v1."""

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
    DEFAULT_OUTPUT as DEFAULT_IDEAL_OP_ROOT,
)
from capabilities.midplatform.field_first_core_model_document_capability_review_v1 import (
    DEFAULT_OUTPUT,
    DEFAULT_PREINSTALL_ROOT,
    run_field_first_core_model_document_capability_review_v1,
)

OUTPUT_FILES = (
    ("model_document_capability_review_report", "model_document_capability_review_report_v1.json"),
    ("model_review_item_registry", "model_review_item_registry_v1.json"),
    ("operation_node_model_fit_matrix", "operation_node_model_fit_matrix_v1.json"),
    ("model_requirement_satisfaction_matrix", "model_requirement_satisfaction_matrix_v1.json"),
    ("near_term_adapter_candidate_matrix", "near_term_adapter_candidate_matrix_v1.json"),
    ("future_adapter_candidate_matrix", "future_adapter_candidate_matrix_v1.json"),
    ("reference_only_model_matrix", "reference_only_model_matrix_v1.json"),
    ("unsuitable_or_deferred_model_matrix", "unsuitable_or_deferred_model_matrix_v1.json"),
    ("model_document_gap_register", "model_document_gap_register_v1.json"),
    ("model_risk_register", "model_risk_register_v1.json"),
    ("download_authorization_recommendation", "download_authorization_recommendation_v1.json"),
    ("adapter_priority_recommendation", "adapter_priority_recommendation_v1.json"),
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
    parser.add_argument("--preinstall-root", default=DEFAULT_PREINSTALL_ROOT)
    parser.add_argument("--ideal-operation-root", default=DEFAULT_IDEAL_OP_ROOT)
    parser.add_argument("--output-root", default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    result = run_field_first_core_model_document_capability_review_v1(
        preinstall_root=args.preinstall_root,
        ideal_operation_root=args.ideal_operation_root,
        output_root=args.output_root,
    )
    out = Path(args.output_root)
    out.mkdir(parents=True, exist_ok=True)
    for key, fname in OUTPUT_FILES:
        (out / fname).write_text(json.dumps(result[key], ensure_ascii=False, indent=2, default=_default) + "\n", encoding="utf-8")
    (out / "model_document_capability_review_report_v1.md").write_text(result["model_document_capability_review_report_md"] + "\n", encoding="utf-8")
    s = result["summary"]
    print(json.dumps({
        "output_root": str(out),
        "field_first_core_model_document_capability_review_pass": s.get("field_first_core_model_document_capability_review_pass"),
        "final_decision": s.get("final_decision"),
        "recommended_next_phase": s.get("recommended_next_phase"),
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
