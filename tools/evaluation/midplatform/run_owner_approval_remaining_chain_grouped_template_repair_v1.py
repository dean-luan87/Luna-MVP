#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run owner approval remaining chain grouped template repair v1."""

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

from capabilities.midplatform.owner_approval_remaining_chain_grouped_template_repair_items_v1 import (
    DEFAULT_OUTPUT,
    PASS_FLAG,
)
from capabilities.midplatform.owner_approval_remaining_chain_grouped_template_repair_v1 import (
    run_owner_approval_remaining_chain_grouped_template_repair_v1,
)

OUTPUT_FILES = (
    ("grouped_template_repair_report", "grouped_template_repair_report_v1.json"),
    ("batch_detection_input_review", "batch_detection_input_review_v1.json"),
    ("safe_template_candidate_execution_matrix", "safe_template_candidate_execution_matrix_v1.json"),
    ("group_p_planning_template_repair_review", "group_p_planning_template_repair_review_v1.json"),
    ("group_d_dryrun_template_repair_review", "group_d_dryrun_template_repair_review_v1.json"),
    ("group_r_post_review_template_repair_review", "group_r_post_review_template_repair_review_v1.json"),
    ("per_stage_original_rerun_results", "per_stage_original_rerun_results_v1.json"),
    ("per_stage_final_decision_alignment_review", "per_stage_final_decision_alignment_review_v1.json"),
    ("per_stage_evidence_traceability_repair_review", "per_stage_evidence_traceability_repair_review_v1.json"),
    ("per_stage_downstream_readiness_repair_review", "per_stage_downstream_readiness_repair_review_v1.json"),
    ("group_g_untouched_review", "group_g_untouched_review_v1.json"),
    ("group_m_untouched_review", "group_m_untouched_review_v1.json"),
    ("canonical_checkpoint_scan_only_after_grouped_repair", "canonical_checkpoint_scan_only_after_grouped_repair_v1.json"),
    ("canonical_checkpoint_topdown_after_grouped_repair", "canonical_checkpoint_topdown_after_grouped_repair_v1.json"),
    ("no_issue_review_created_review", "no_issue_review_created_review_v1.json"),
    ("no_gap_review_created_review", "no_gap_review_created_review_v1.json"),
    ("no_rerun_review_created_review", "no_rerun_review_created_review_v1.json"),
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
    result = run_owner_approval_remaining_chain_grouped_template_repair_v1(output_root=args.output_root)
    out = Path(args.output_root)
    out.mkdir(parents=True, exist_ok=True)
    for key, fname in OUTPUT_FILES:
        (out / fname).write_text(
            json.dumps(result[key], ensure_ascii=False, indent=2, default=_default) + "\n",
            encoding="utf-8",
        )
    (out / "grouped_template_repair_report_v1.md").write_text(
        result["grouped_template_repair_report_md"] + "\n",
        encoding="utf-8",
    )
    s = result["summary"]
    print(
        json.dumps(
            {
                "output_root": str(out),
                PASS_FLAG: s.get(PASS_FLAG),
                "safe_template_candidate_count": s.get("safe_template_candidate_count"),
                "processed_template_candidate_count": s.get("processed_template_candidate_count"),
                "issuance_closure_template_chain_cleared": s.get("issuance_closure_template_chain_cleared"),
                "go_stage_count_after_repair": s.get("go_stage_count_after_repair"),
                "first_failed_stage_key_after_repair": s.get("first_failed_stage_key_after_repair"),
                "final_decision": s.get("final_decision"),
                "recommended_next_phase": s.get("recommended_next_phase"),
            },
            ensure_ascii=False,
        )
    )
    return 0 if s.get(PASS_FLAG) else 1


if __name__ == "__main__":
    raise SystemExit(main())
