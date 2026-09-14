#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run governance gate integrated implementation repair v1."""

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

from capabilities.midplatform.governance_gate_integrated_implementation_repair_items_v1 import (
    DEFAULT_OUTPUT,
    PASS_FLAG,
)
from capabilities.midplatform.governance_gate_integrated_implementation_repair_v1 import (
    run_governance_gate_integrated_implementation_repair_v1,
)

OUTPUT_FILES = (
    ("governance_gate_integrated_implementation_repair_report", "governance_gate_integrated_implementation_repair_report_v1.json"),
    ("canonical_rebuild_input_review", "canonical_rebuild_input_review_v1.json"),
    ("governance_gate_integrated_implementation_original_stage_locator", "governance_gate_integrated_implementation_original_stage_locator_v1.json"),
    ("governance_gate_integrated_implementation_original_rerun_review", "governance_gate_integrated_implementation_original_rerun_review_v1.json"),
    ("governance_gate_integrated_implementation_failure_classification", "governance_gate_integrated_implementation_failure_classification_v1.json"),
    ("governance_gate_integrated_implementation_decision_drift_repair_review", "governance_gate_integrated_implementation_decision_drift_repair_review_v1.json"),
    ("governance_gate_integrated_implementation_schema_output_repair_review", "governance_gate_integrated_implementation_schema_output_repair_review_v1.json"),
    ("governance_gate_integrated_implementation_downstream_expectation_repair_review", "governance_gate_integrated_implementation_downstream_expectation_repair_review_v1.json"),
    ("governance_gate_integrated_implementation_traceability_repair_review", "governance_gate_integrated_implementation_traceability_repair_review_v1.json"),
    ("governance_gate_integrated_implementation_final_decision_review", "governance_gate_integrated_implementation_final_decision_review_v1.json"),
    ("governance_gate_integrated_implementation_post_repair_rerun_review", "governance_gate_integrated_implementation_post_repair_rerun_review_v1.json"),
    ("canonical_checkpoint_scan_only_after_repair_review", "canonical_checkpoint_scan_only_after_repair_review_v1.json"),
    ("canonical_checkpoint_topdown_after_repair_review", "canonical_checkpoint_topdown_after_repair_review_v1.json"),
    ("group_g_scope_review", "group_g_scope_review_v1.json"),
    ("group_m_untouched_review", "group_m_untouched_review_v1.json"),
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
    result = run_governance_gate_integrated_implementation_repair_v1(output_root=args.output_root)
    out = Path(args.output_root)
    out.mkdir(parents=True, exist_ok=True)
    for key, fname in OUTPUT_FILES:
        (out / fname).write_text(
            json.dumps(result[key], ensure_ascii=False, indent=2, default=_default) + "\n",
            encoding="utf-8",
        )
    (out / "governance_gate_integrated_implementation_repair_report_v1.md").write_text(
        result["governance_gate_integrated_implementation_repair_report_md"] + "\n",
        encoding="utf-8",
    )
    s = result["summary"]
    print(
        json.dumps(
            {
                "output_root": str(out),
                PASS_FLAG: s.get(PASS_FLAG),
                "original_governance_gate_integrated_implementation_verifier_go": s.get(
                    "original_governance_gate_integrated_implementation_verifier_go"
                ),
                "governance_gate_integrated_implementation_checkpoint_go_readable": s.get(
                    "governance_gate_integrated_implementation_checkpoint_go_readable"
                ),
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
