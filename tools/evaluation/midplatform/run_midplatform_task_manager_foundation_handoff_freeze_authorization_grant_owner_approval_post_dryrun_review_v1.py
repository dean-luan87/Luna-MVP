#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Luna Midplatform Task Manager Foundation Handoff Freeze Authorization Grant Owner Approval Post-DryRun Review v1."""

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

from capabilities.midplatform.task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_dryrun_v1 import (
    DEFAULT_OUTPUT as DEFAULT_OWNER_APPROVAL_DRYRUN_ROOT,
)
from capabilities.midplatform.task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_post_dryrun_review_v1 import (
    DEFAULT_OUTPUT,
    run_task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_post_dryrun_review_v1,
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    (
        "task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_post_dryrun_review_report",
        "task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_post_dryrun_review_report_v1.json",
    ),
    (
        "task_manager_freeze_authorization_grant_owner_approval_dryrun_result_review",
        "task_manager_freeze_authorization_grant_owner_approval_dryrun_result_review_v1.json",
    ),
    (
        "task_manager_freeze_authorization_grant_owner_approval_protocol_reference_review",
        "task_manager_freeze_authorization_grant_owner_approval_protocol_reference_review_v1.json",
    ),
    (
        "task_manager_freeze_authorization_grant_owner_approval_separation_rule_review",
        "task_manager_freeze_authorization_grant_owner_approval_separation_rule_review_v1.json",
    ),
    (
        "task_manager_freeze_authorization_grant_owner_approval_candidate_state_review",
        "task_manager_freeze_authorization_grant_owner_approval_candidate_state_review_v1.json",
    ),
    (
        "task_manager_freeze_authorization_grant_owner_operator_ack_candidate_state_review",
        "task_manager_freeze_authorization_grant_owner_operator_ack_candidate_state_review_v1.json",
    ),
    (
        "task_manager_freeze_authorization_grant_owner_approval_evidence_binding_review",
        "task_manager_freeze_authorization_grant_owner_approval_evidence_binding_review_v1.json",
    ),
    (
        "task_manager_freeze_authorization_grant_owner_approval_request_record_binding_review",
        "task_manager_freeze_authorization_grant_owner_approval_request_record_binding_review_v1.json",
    ),
    (
        "task_manager_freeze_authorization_grant_owner_approval_lifecycle_review",
        "task_manager_freeze_authorization_grant_owner_approval_lifecycle_review_v1.json",
    ),
    (
        "task_manager_freeze_authorization_grant_owner_approval_expiry_revocation_review",
        "task_manager_freeze_authorization_grant_owner_approval_expiry_revocation_review_v1.json",
    ),
    (
        "task_manager_freeze_authorization_grant_owner_approval_absence_review",
        "task_manager_freeze_authorization_grant_owner_approval_absence_review_v1.json",
    ),
    (
        "task_manager_freeze_authorization_grant_owner_approval_boundary_drift_review",
        "task_manager_freeze_authorization_grant_owner_approval_boundary_drift_review_v1.json",
    ),
    (
        "task_manager_freeze_authorization_grant_owner_approval_evidence_chain_review",
        "task_manager_freeze_authorization_grant_owner_approval_evidence_chain_review_v1.json",
    ),
    (
        "task_manager_freeze_authorization_grant_owner_approval_governance_debt_review",
        "task_manager_freeze_authorization_grant_owner_approval_governance_debt_review_v1.json",
    ),
    (
        "task_manager_freeze_authorization_grant_owner_approval_template_lineage",
        "task_manager_freeze_authorization_grant_owner_approval_template_lineage_v1.json",
    ),
    (
        "task_manager_freeze_authorization_grant_owner_approval_next_phase_readiness",
        "task_manager_freeze_authorization_grant_owner_approval_next_phase_readiness_v1.json",
    ),
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
    parser.add_argument("--grant-owner-approval-dryrun-root", default=DEFAULT_OWNER_APPROVAL_DRYRUN_ROOT)
    parser.add_argument("--output-root", default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    result = run_task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_post_dryrun_review_v1(
        grant_owner_approval_dryrun_root=args.grant_owner_approval_dryrun_root,
        output_root=args.output_root,
    )
    out = Path(args.output_root)
    for key, fname in OUTPUT_FILES:
        _write_json(out / fname, result[key])
    (out / "task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_post_dryrun_review_report_v1.md").write_text(
        result["task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_post_dryrun_review_md"] + "\n",
        encoding="utf-8",
    )
    summary = result["summary"]
    print(
        json.dumps(
            {
                "output_root": str(out),
                "post_dryrun_review_pass": summary.get("post_dryrun_review_pass"),
                "blocker_count": summary.get("blocker_count"),
                "protocol_reference_review_ok": summary.get("protocol_reference_review_ok"),
                "absence_review_ok": summary.get("absence_review_ok"),
                "final_decision": summary.get("final_decision"),
                "recommended_next_phase": summary.get("recommended_next_phase"),
            },
            ensure_ascii=False,
        )
    )
    return 0 if summary.get("post_dryrun_review_pass") else 1


if __name__ == "__main__":
    raise SystemExit(main())
