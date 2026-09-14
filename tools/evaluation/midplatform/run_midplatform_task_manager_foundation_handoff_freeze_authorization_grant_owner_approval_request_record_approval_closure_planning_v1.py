#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Luna Midplatform Task Manager Foundation Handoff Freeze Authorization Grant Owner Approval Request Record Approval Closure Planning v1."""

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

from capabilities.midplatform.task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_record_approval_closure_planning_v1 import (
    DEFAULT_OWNER_APPROVAL_REQUEST_ISSUANCE_POST_REVIEW_ROOT,
    DEFAULT_OUTPUT,
    run_task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_record_approval_closure_planning_v1,
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    (
        "task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_record_approval_closure_plan",
        "task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_record_approval_closure_plan_v1.json",
    ),
    (
        "task_manager_freeze_authorization_grant_owner_approval_request_record_candidate_closure_matrix",
        "task_manager_freeze_authorization_grant_owner_approval_request_record_candidate_closure_matrix_v1.json",
    ),
    (
        "task_manager_freeze_authorization_grant_owner_approval_request_approval_candidate_closure_matrix",
        "task_manager_freeze_authorization_grant_owner_approval_request_approval_candidate_closure_matrix_v1.json",
    ),
    (
        "task_manager_freeze_authorization_grant_owner_approval_request_ack_candidate_closure_matrix",
        "task_manager_freeze_authorization_grant_owner_approval_request_ack_candidate_closure_matrix_v1.json",
    ),
    (
        "task_manager_freeze_authorization_grant_owner_approval_request_evidence_binding_closure_matrix",
        "task_manager_freeze_authorization_grant_owner_approval_request_evidence_binding_closure_matrix_v1.json",
    ),
    (
        "task_manager_freeze_authorization_grant_owner_approval_request_record_approval_traceability_matrix",
        "task_manager_freeze_authorization_grant_owner_approval_request_record_approval_traceability_matrix_v1.json",
    ),
    (
        "task_manager_freeze_authorization_grant_owner_approval_request_record_approval_protocol_reference_matrix",
        "task_manager_freeze_authorization_grant_owner_approval_request_record_approval_protocol_reference_matrix_v1.json",
    ),
    (
        "task_manager_freeze_authorization_grant_owner_approval_request_record_approval_error_namespace_matrix",
        "task_manager_freeze_authorization_grant_owner_approval_request_record_approval_error_namespace_matrix_v1.json",
    ),
    (
        "task_manager_freeze_authorization_grant_owner_approval_request_record_approval_whitebox_candidate_ref_matrix",
        "task_manager_freeze_authorization_grant_owner_approval_request_record_approval_whitebox_candidate_ref_matrix_v1.json",
    ),
    (
        "task_manager_freeze_authorization_grant_owner_approval_request_record_approval_boundary_contract",
        "task_manager_freeze_authorization_grant_owner_approval_request_record_approval_boundary_contract_v1.json",
    ),
    (
        "task_manager_freeze_authorization_grant_owner_approval_request_record_approval_non_execution_constraints",
        "task_manager_freeze_authorization_grant_owner_approval_request_record_approval_non_execution_constraints_v1.json",
    ),
    (
        "task_manager_freeze_authorization_grant_owner_approval_request_record_approval_rejection_reference_matrix",
        "task_manager_freeze_authorization_grant_owner_approval_request_record_approval_rejection_reference_matrix_v1.json",
    ),
    (
        "task_manager_freeze_authorization_grant_owner_approval_request_record_approval_expiry_reference_matrix",
        "task_manager_freeze_authorization_grant_owner_approval_request_record_approval_expiry_reference_matrix_v1.json",
    ),
    (
        "task_manager_freeze_authorization_grant_owner_approval_request_record_approval_revocation_reference_matrix",
        "task_manager_freeze_authorization_grant_owner_approval_request_record_approval_revocation_reference_matrix_v1.json",
    ),
    (
        "task_manager_freeze_authorization_grant_owner_approval_request_record_approval_governance_debt_carryover",
        "task_manager_freeze_authorization_grant_owner_approval_request_record_approval_governance_debt_carryover_v1.json",
    ),
    (
        "task_manager_freeze_authorization_grant_owner_approval_request_record_approval_template_lineage",
        "task_manager_freeze_authorization_grant_owner_approval_request_record_approval_template_lineage_v1.json",
    ),
    (
        "task_manager_freeze_authorization_grant_owner_approval_request_record_approval_next_phase_readiness",
        "task_manager_freeze_authorization_grant_owner_approval_request_record_approval_next_phase_readiness_v1.json",
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
        "--owner-approval-request-issuance-post-dryrun-review-root",
        default=DEFAULT_OWNER_APPROVAL_REQUEST_ISSUANCE_POST_REVIEW_ROOT,
    )
    parser.add_argument("--output-root", default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    result = run_task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_record_approval_closure_planning_v1(
        owner_approval_request_issuance_post_dryrun_review_root=args.owner_approval_request_issuance_post_dryrun_review_root,
        output_root=args.output_root,
    )
    out = Path(args.output_root)
    for key, fname in OUTPUT_FILES:
        _write_json(out / fname, result[key])
    (out / "task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_record_approval_closure_plan_v1.md").write_text(
        result["task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_record_approval_closure_plan_md"] + "\n",
        encoding="utf-8",
    )
    summary = result["summary"]
    print(
        json.dumps(
            {
                "output_root": str(out),
                "planning_pass": summary.get("planning_pass"),
                "blocker_count": summary.get("blocker_count"),
                "template_lineage_ok": summary.get("template_lineage_ok"),
                "record_approval_closure_plan_complete": summary.get("record_approval_closure_plan_complete"),
                "file_size_governance_review_exists": summary.get("file_size_governance_review_exists"),
                "final_decision": summary.get("final_decision"),
                "recommended_next_phase": summary.get("recommended_next_phase"),
            },
            ensure_ascii=False,
        )
    )
    return 0 if summary.get("planning_pass") else 1


if __name__ == "__main__":
    raise SystemExit(main())
