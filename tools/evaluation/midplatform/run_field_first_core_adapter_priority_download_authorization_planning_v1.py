#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Field-First Adapter Priority and Download Authorization Planning v1."""

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

from capabilities.midplatform.field_first_core_adapter_priority_download_authorization_planning_v1 import (
    DEFAULT_OUTPUT,
    DEFAULT_PREINSTALL_ROOT,
    run_field_first_core_adapter_priority_download_authorization_planning_v1,
)
from capabilities.midplatform.field_first_core_model_document_capability_review_v1 import (
    DEFAULT_OUTPUT as DEFAULT_DOC_REVIEW_ROOT,
)

OUTPUT_FILES = (
    ("adapter_priority_and_download_authorization_plan_report", "adapter_priority_and_download_authorization_plan_report_v1.json"),
    ("adapter_priority_queue", "adapter_priority_queue_v1.json"),
    ("adapter_batch_plan", "adapter_batch_plan_v1.json"),
    ("download_authorization_plan", "download_authorization_plan_v1.json"),
    ("owner_review_candidate_downloads", "owner_review_candidate_downloads_v1.json"),
    ("no_download_required_self_developed_items", "no_download_required_self_developed_items_v1.json"),
    ("conditional_future_download_review", "conditional_future_download_review_v1.json"),
    ("reference_only_no_download", "reference_only_no_download_v1.json"),
    ("deferred_no_download", "deferred_no_download_v1.json"),
    ("adapter_skeleton_batch_recommendation", "adapter_skeleton_batch_recommendation_v1.json"),
    ("model_status_transition_plan", "model_status_transition_plan_v1.json"),
    ("risk_control_plan", "risk_control_plan_v1.json"),
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
    parser.add_argument("--preinstall-root", default=DEFAULT_PREINSTALL_ROOT)
    parser.add_argument("--output-root", default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    result = run_field_first_core_adapter_priority_download_authorization_planning_v1(
        doc_review_root=args.doc_review_root, preinstall_root=args.preinstall_root, output_root=args.output_root,
    )
    out = Path(args.output_root)
    out.mkdir(parents=True, exist_ok=True)
    for key, fname in OUTPUT_FILES:
        (out / fname).write_text(json.dumps(result[key], ensure_ascii=False, indent=2, default=_default) + "\n", encoding="utf-8")
    (out / "adapter_priority_and_download_authorization_plan_report_v1.md").write_text(result["adapter_priority_and_download_authorization_plan_report_md"] + "\n", encoding="utf-8")
    s = result["summary"]
    print(json.dumps({
        "output_root": str(out),
        "field_first_core_adapter_priority_planning_pass": s.get("field_first_core_adapter_priority_planning_pass"),
        "final_decision": s.get("final_decision"),
        "recommended_next_phase": s.get("recommended_next_phase"),
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
