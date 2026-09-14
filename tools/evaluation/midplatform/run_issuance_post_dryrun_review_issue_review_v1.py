#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run issuance post-dryrun review issue review v1."""

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

from capabilities.midplatform.issuance_post_dryrun_review_issue_review_items_v1 import (
    DEFAULT_OUTPUT,
    PASS_FLAG,
)
from capabilities.midplatform.issuance_post_dryrun_review_issue_review_v1 import (
    run_issuance_post_dryrun_review_issue_review_v1,
)

OUTPUT_FILES = (
    ("issuance_post_dryrun_review_issue_review_report", "issuance_post_dryrun_review_issue_review_report_v1.json"),
    ("issuance_post_dryrun_review_gap_review", "issuance_post_dryrun_review_gap_review_v1.json"),
    ("issuance_post_dryrun_review_artifact_visibility_review", "issuance_post_dryrun_review_artifact_visibility_review_v1.json"),
    ("issuance_post_dryrun_review_direct_upstream_registry", "issuance_post_dryrun_review_direct_upstream_registry_v1.json"),
    ("issuance_post_dryrun_review_first_non_go_upstream_review", "issuance_post_dryrun_review_first_non_go_upstream_review_v1.json"),
    ("issuance_post_dryrun_review_dryrun_acceptance_review", "issuance_post_dryrun_review_dryrun_acceptance_review_v1.json"),
    ("issuance_post_dryrun_review_validate_once_reference_review", "issuance_post_dryrun_review_validate_once_reference_review_v1.json"),
    ("issuance_post_dryrun_review_precondition_leakage_review", "issuance_post_dryrun_review_precondition_leakage_review_v1.json"),
    ("issuance_post_dryrun_review_evidence_chain_review", "issuance_post_dryrun_review_evidence_chain_review_v1.json"),
    ("issuance_post_dryrun_review_rerun_review", "issuance_post_dryrun_review_rerun_review_v1.json"),
    ("record_approval_closure_planning_rerun_readiness_review", "record_approval_closure_planning_rerun_readiness_review_v1.json"),
    ("first_unresolved_gap_review", "first_unresolved_gap_review_v1.json"),
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
    result = run_issuance_post_dryrun_review_issue_review_v1(
        output_root=args.output_root,
    )
    out = Path(args.output_root)
    out.mkdir(parents=True, exist_ok=True)
    for key, fname in OUTPUT_FILES:
        (out / fname).write_text(
            json.dumps(result[key], ensure_ascii=False, indent=2, default=_default) + "\n",
            encoding="utf-8",
        )
    (out / "issuance_post_dryrun_review_issue_review_report_v1.md").write_text(
        result["issuance_post_dryrun_review_issue_review_report_md"] + "\n",
        encoding="utf-8",
    )
    s = result["summary"]
    print(json.dumps({
        "output_root": str(out),
        PASS_FLAG: s.get(PASS_FLAG),
        "issuance_post_dryrun_review_go": s.get("issuance_post_dryrun_review_go"),
        "first_non_go_issuance_upstream": s.get("first_non_go_issuance_upstream"),
        "final_decision": s.get("final_decision"),
        "recommended_next_phase": s.get("recommended_next_phase"),
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
