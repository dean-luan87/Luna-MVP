#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Luna Midplatform Task Manager Foundation Handoff Freeze Authorization Post-DryRun Review v1."""

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

from capabilities.midplatform.task_manager_foundation_handoff_freeze_authorization_post_dryrun_review_v1 import (
    DEFAULT_FREEZE_AUTH_DRYRUN_ROOT,
    DEFAULT_OUTPUT,
    run_task_manager_foundation_handoff_freeze_authorization_post_dryrun_review_v1,
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("task_manager_foundation_handoff_freeze_authorization_post_dryrun_review", "task_manager_foundation_handoff_freeze_authorization_post_dryrun_review_v1.json"),
    ("task_manager_freeze_authorization_dryrun_review_matrix", "task_manager_freeze_authorization_dryrun_review_matrix_v1.json"),
    ("task_manager_freeze_authorization_boundary_drift_review", "task_manager_freeze_authorization_boundary_drift_review_v1.json"),
    ("task_manager_freeze_authorization_chain_evidence_review", "task_manager_freeze_authorization_chain_evidence_review_v1.json"),
    ("task_manager_freeze_authorization_request_absence_review", "task_manager_freeze_authorization_request_absence_review_v1.json"),
    ("task_manager_freeze_authorization_grant_absence_review", "task_manager_freeze_authorization_grant_absence_review_v1.json"),
    ("task_manager_freeze_state_absence_review", "task_manager_freeze_state_absence_review_v1.json"),
    ("task_manager_freeze_authorization_governance_debt_review", "task_manager_freeze_authorization_governance_debt_review_v1.json"),
    ("task_manager_freeze_authorization_grant_planning_readiness", "task_manager_freeze_authorization_grant_planning_readiness_v1.json"),
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
    parser.add_argument("--freeze-authorization-dryrun-root", default=DEFAULT_FREEZE_AUTH_DRYRUN_ROOT)
    parser.add_argument("--output-root", default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    result = run_task_manager_foundation_handoff_freeze_authorization_post_dryrun_review_v1(
        freeze_authorization_dryrun_root=args.freeze_authorization_dryrun_root,
        output_root=args.output_root,
    )
    out = Path(args.output_root)
    for key, fname in OUTPUT_FILES:
        _write_json(out / fname, result[key])
    (out / "task_manager_foundation_handoff_freeze_authorization_post_dryrun_review_v1.md").write_text(
        result["task_manager_foundation_handoff_freeze_authorization_post_dryrun_review_md"] + "\n",
        encoding="utf-8",
    )
    summary = result["summary"]
    print(
        json.dumps(
            {
                "output_root": str(out),
                "post_dryrun_review_pass": summary.get("post_dryrun_review_pass"),
                "blocker_count": summary.get("blocker_count"),
                "final_decision": summary.get("final_decision"),
                "recommended_next_phase": summary.get("recommended_next_phase"),
            },
            ensure_ascii=False,
        )
    )
    return 0 if summary.get("post_dryrun_review_pass") else 1


if __name__ == "__main__":
    raise SystemExit(main())
