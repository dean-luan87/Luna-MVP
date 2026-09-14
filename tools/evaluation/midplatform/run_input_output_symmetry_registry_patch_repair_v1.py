#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run input/output symmetry registry patch repair v1."""

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

from capabilities.midplatform.input_output_symmetry_registry_patch_repair_items_v1 import (
    DEFAULT_OUTPUT,
    PASS_FLAG,
)
from capabilities.midplatform.input_output_symmetry_registry_patch_repair_v1 import (
    run_input_output_symmetry_registry_patch_repair_v1,
)

OUTPUT_FILES = (
    ("input_output_symmetry_registry_patch_repair_report", "input_output_symmetry_registry_patch_repair_report_v1.json"),
    ("canonical_rebuild_input_review", "canonical_rebuild_input_review_v1.json"),
    ("registry_patch_original_stage_locator", "registry_patch_original_stage_locator_v1.json"),
    ("registry_patch_original_rerun_review", "registry_patch_original_rerun_review_v1.json"),
    ("registry_patch_failure_classification", "registry_patch_failure_classification_v1.json"),
    ("registry_patch_schema_output_repair_review", "registry_patch_schema_output_repair_review_v1.json"),
    ("registry_patch_mapping_repair_review", "registry_patch_mapping_repair_review_v1.json"),
    ("registry_patch_downstream_expectation_review", "registry_patch_downstream_expectation_review_v1.json"),
    ("registry_patch_final_decision_review", "registry_patch_final_decision_review_v1.json"),
    ("registry_patch_post_repair_rerun_review", "registry_patch_post_repair_rerun_review_v1.json"),
    ("canonical_checkpoint_scan_only_after_repair_review", "canonical_checkpoint_scan_only_after_repair_review_v1.json"),
    ("no_issue_review_created_review", "no_issue_review_created_review_v1.json"),
    ("no_original_stage_pollution_review", "no_original_stage_pollution_review_v1.json"),
    ("no_protocol_change_review", "no_protocol_change_review_v1.json"),
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
    result = run_input_output_symmetry_registry_patch_repair_v1(output_root=args.output_root)
    out = Path(args.output_root)
    out.mkdir(parents=True, exist_ok=True)
    for key, fname in OUTPUT_FILES:
        (out / fname).write_text(
            json.dumps(result[key], ensure_ascii=False, indent=2, default=_default) + "\n",
            encoding="utf-8",
        )
    (out / "input_output_symmetry_registry_patch_repair_report_v1.md").write_text(
        result["input_output_symmetry_registry_patch_repair_report_md"] + "\n",
        encoding="utf-8",
    )
    s = result["summary"]
    print(json.dumps({
        "output_root": str(out),
        PASS_FLAG: s.get(PASS_FLAG),
        "original_registry_patch_verifier_go": s.get("original_registry_patch_verifier_go"),
        "registry_patch_checkpoint_go_readable": s.get("registry_patch_checkpoint_go_readable"),
        "first_failed_stage_after_repair": s.get("first_failed_stage_after_repair"),
        "final_decision": s.get("final_decision"),
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
