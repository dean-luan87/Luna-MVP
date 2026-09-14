#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run owner approval remaining chain batch pattern detection and repair plan v1."""

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

from capabilities.midplatform.owner_approval_remaining_chain_batch_pattern_detection_and_repair_plan_v1 import (
    run_owner_approval_remaining_chain_batch_pattern_detection_and_repair_plan_v1,
)
from capabilities.midplatform.owner_approval_remaining_chain_batch_pattern_detection_items_v1 import (
    DEFAULT_OUTPUT,
    PASS_FLAG,
)

OUTPUT_FILES = (
    ("batch_pattern_detection_report", "batch_pattern_detection_report_v1.json"),
    ("remaining_stage_inventory", "remaining_stage_inventory_v1.json"),
    ("remaining_stage_family_classification", "remaining_stage_family_classification_v1.json"),
    ("remaining_stage_gap_classification", "remaining_stage_gap_classification_v1.json"),
    ("downstream_expectation_gap_matrix", "downstream_expectation_gap_matrix_v1.json"),
    ("runner_verifier_decision_drift_matrix", "runner_verifier_decision_drift_matrix_v1.json"),
    ("evidence_traceability_gap_matrix", "evidence_traceability_gap_matrix_v1.json"),
    ("schema_output_gap_matrix", "schema_output_gap_matrix_v1.json"),
    ("verifier_locator_gap_matrix", "verifier_locator_gap_matrix_v1.json"),
    ("genuine_logic_hold_candidate_matrix", "genuine_logic_hold_candidate_matrix_v1.json"),
    ("batch_repair_group_plan", "batch_repair_group_plan_v1.json"),
    ("safe_template_repair_candidates", "safe_template_repair_candidates_v1.json"),
    ("stages_requiring_individual_repair", "stages_requiring_individual_repair_v1.json"),
    ("no_issue_review_created_review", "no_issue_review_created_review_v1.json"),
    ("no_original_stage_pollution_review", "no_original_stage_pollution_review_v1.json"),
    ("no_protocol_change_review", "no_protocol_change_review_v1.json"),
    ("no_model_route_touched_review", "no_model_route_touched_review_v1.json"),
    ("no_world_model_boundary_review", "no_world_model_boundary_review_v1.json"),
    ("owner_constraint_compliance_review", "owner_constraint_compliance_review_v1.json"),
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
    result = run_owner_approval_remaining_chain_batch_pattern_detection_and_repair_plan_v1(
        output_root=args.output_root
    )
    out = Path(args.output_root)
    out.mkdir(parents=True, exist_ok=True)
    for key, fname in OUTPUT_FILES:
        (out / fname).write_text(
            json.dumps(result[key], ensure_ascii=False, indent=2, default=_default) + "\n",
            encoding="utf-8",
        )
    (out / "batch_pattern_detection_report_v1.md").write_text(
        result["batch_pattern_detection_report_md"] + "\n",
        encoding="utf-8",
    )
    s = result["summary"]
    print(
        json.dumps(
            {
                "output_root": str(out),
                PASS_FLAG: s.get(PASS_FLAG),
                "go_stage_count": s.get("go_stage_count"),
                "remaining_stage_count": s.get("remaining_stage_count"),
                "safe_template_repair_candidate_count": s.get("safe_template_repair_candidate_count"),
                "first_failed_stage_key": s.get("first_failed_stage_key"),
                "final_decision": s.get("final_decision"),
                "recommended_next_phase": s.get("recommended_next_phase"),
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
