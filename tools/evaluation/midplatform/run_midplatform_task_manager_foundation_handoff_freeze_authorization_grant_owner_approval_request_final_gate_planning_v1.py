#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Luna Midplatform Final Gate Planning v1."""

from __future__ import annotations

import dataclasses
import json
import sys
from argparse import ArgumentParser
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.midplatform.task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_final_gate_planning_v1 import (
    DEFAULT_OUTPUT,
    DEFAULT_POST_REVIEW_ROOT,
    run_task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_final_gate_planning_v1,
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    (
        "task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_final_gate_plan",
        "task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_final_gate_plan_v1.json",
    ),
    (
        "task_manager_freeze_authorization_grant_owner_approval_request_final_gate_readiness_matrix",
        "task_manager_freeze_authorization_grant_owner_approval_request_final_gate_readiness_matrix_v1.json",
    ),
    (
        "task_manager_freeze_authorization_grant_owner_approval_request_final_gate_missing_conditions",
        "task_manager_freeze_authorization_grant_owner_approval_request_final_gate_missing_conditions_v1.json",
    ),
    (
        "task_manager_freeze_authorization_grant_owner_approval_request_final_gate_blocker_matrix",
        "task_manager_freeze_authorization_grant_owner_approval_request_final_gate_blocker_matrix_v1.json",
    ),
    (
        "task_manager_freeze_authorization_grant_owner_approval_request_final_gate_non_execution_boundary",
        "task_manager_freeze_authorization_grant_owner_approval_request_final_gate_non_execution_boundary_v1.json",
    ),
    (
        "task_manager_freeze_authorization_grant_owner_approval_request_final_gate_governance_rule_reference",
        "task_manager_freeze_authorization_grant_owner_approval_request_final_gate_governance_rule_reference_v1.json",
    ),
    (
        "task_manager_freeze_authorization_grant_owner_approval_request_final_gate_next_phase_readiness",
        "task_manager_freeze_authorization_grant_owner_approval_request_final_gate_next_phase_readiness_v1.json",
    ),
    (
        "module_first_development_verification_cadence_rule_reference",
        "module_first_development_verification_cadence_rule_reference_v1.json",
    ),
    ("file_size_governance_review", "file_size_governance_review_v1.json"),
    ("summary", "summary.json"),
)


def _default(obj: Any) -> Any:
    if dataclasses.is_dataclass(obj):
        return dataclasses.asdict(obj)
    if isinstance(obj, tuple):
        return list(obj)
    return str(obj)


def _write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, default=_default) + "\n", encoding="utf-8")


def main() -> int:
    parser = ArgumentParser()
    parser.add_argument(
        "--record-approval-closure-post-review-root",
        default=DEFAULT_POST_REVIEW_ROOT,
    )
    parser.add_argument("--output-root", default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    result = run_task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_final_gate_planning_v1(
        record_approval_closure_post_review_root=args.record_approval_closure_post_review_root,
        output_root=args.output_root,
    )
    out = Path(args.output_root)
    for key, fname in OUTPUT_FILES:
        _write_json(out / fname, result[key])
    (out / "task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_final_gate_plan_v1.md").write_text(
        result["task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_final_gate_plan_md"] + "\n",
        encoding="utf-8",
    )
    summary = result["summary"]
    print(
        json.dumps(
            {
                "output_root": str(out),
                "final_gate_planning_pass": summary.get("final_gate_planning_pass"),
                "prior_post_review_go": summary.get("prior_record_approval_closure_post_review_go"),
                "module_first_cadence_rule_ref_ok": summary.get("module_first_cadence_rule_ref_ok"),
                "blocker_count": summary.get("blocker_count"),
                "final_decision": summary.get("final_decision"),
                "recommended_next_phase": summary.get("recommended_next_phase"),
            },
            ensure_ascii=False,
        )
    )
    return 0 if summary.get("final_gate_planning_pass") else 1


if __name__ == "__main__":
    raise SystemExit(main())
