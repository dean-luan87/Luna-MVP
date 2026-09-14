#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run record approval closure post-dryrun review issue review v1."""

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

from capabilities.midplatform.record_approval_closure_post_dryrun_review_issue_review_items_v1 import (
    DEFAULT_OUTPUT,
    PASS_FLAG,
)
from capabilities.midplatform.record_approval_closure_post_dryrun_review_issue_review_v1 import (
    run_record_approval_closure_post_dryrun_review_issue_review_v1,
)

OUTPUT_FILES = (
    (
        "record_approval_closure_post_dryrun_review_issue_review_report",
        "record_approval_closure_post_dryrun_review_issue_review_report_v1.json",
    ),
    ("post_dryrun_review_gap_review", "post_dryrun_review_gap_review_v1.json"),
    ("post_dryrun_review_artifact_visibility_review", "post_dryrun_review_artifact_visibility_review_v1.json"),
    ("post_dryrun_review_direct_dryrun_upstream_review", "post_dryrun_review_direct_dryrun_upstream_review_v1.json"),
    ("post_dryrun_review_dryrun_result_acceptance_review", "post_dryrun_review_dryrun_result_acceptance_review_v1.json"),
    ("post_dryrun_review_candidate_escalation_review", "post_dryrun_review_candidate_escalation_review_v1.json"),
    ("post_dryrun_review_absence_drift_review", "post_dryrun_review_absence_drift_review_v1.json"),
    ("post_dryrun_review_boundary_drift_review", "post_dryrun_review_boundary_drift_review_v1.json"),
    ("post_dryrun_review_traceability_drift_review", "post_dryrun_review_traceability_drift_review_v1.json"),
    ("post_dryrun_review_rerun_review", "post_dryrun_review_rerun_review_v1.json"),
    ("integrated_implementation_rerun_readiness_review", "integrated_implementation_rerun_readiness_review_v1.json"),
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
    result = run_record_approval_closure_post_dryrun_review_issue_review_v1(
        output_root=args.output_root,
    )
    out = Path(args.output_root)
    out.mkdir(parents=True, exist_ok=True)
    for key, fname in OUTPUT_FILES:
        (out / fname).write_text(
            json.dumps(result[key], ensure_ascii=False, indent=2, default=_default) + "\n",
            encoding="utf-8",
        )
    (out / "record_approval_closure_post_dryrun_review_issue_review_report_v1.md").write_text(
        result["record_approval_closure_post_dryrun_review_issue_review_report_md"] + "\n",
        encoding="utf-8",
    )
    s = result["summary"]
    print(json.dumps({
        "output_root": str(out),
        PASS_FLAG: s.get(PASS_FLAG),
        "post_dryrun_review_go": s.get("post_dryrun_review_go"),
        "direct_dryrun_upstream_go": s.get("direct_dryrun_upstream_go"),
        "first_non_go_dryrun_upstream": s.get("first_non_go_dryrun_upstream"),
        "final_decision": s.get("final_decision"),
        "recommended_next_phase": s.get("recommended_next_phase"),
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
