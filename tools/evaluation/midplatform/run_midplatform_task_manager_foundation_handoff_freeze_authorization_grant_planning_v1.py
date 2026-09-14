#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Luna Midplatform Task Manager Foundation Handoff Freeze Authorization Grant Planning v1."""

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

from capabilities.midplatform.task_manager_foundation_handoff_freeze_authorization_grant_planning_v1 import (
    DEFAULT_FREEZE_AUTH_PLANNING_ROOT,
    DEFAULT_FREEZE_AUTH_POST_REVIEW_ROOT,
    DEFAULT_OUTPUT,
    run_task_manager_foundation_handoff_freeze_authorization_grant_planning_v1,
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("task_manager_foundation_handoff_freeze_authorization_grant_plan", "task_manager_foundation_handoff_freeze_authorization_grant_plan_v1.json"),
    ("task_manager_freeze_authorization_grant_scope_matrix", "task_manager_freeze_authorization_grant_scope_matrix_v1.json"),
    ("task_manager_freeze_authorization_grant_candidate_asset_map", "task_manager_freeze_authorization_grant_candidate_asset_map_v1.json"),
    ("task_manager_freeze_authorization_grant_prerequisite_matrix", "task_manager_freeze_authorization_grant_prerequisite_matrix_v1.json"),
    ("task_manager_freeze_authorization_grant_evidence_chain", "task_manager_freeze_authorization_grant_evidence_chain_v1.json"),
    ("task_manager_freeze_authorization_grant_boundary_contract", "task_manager_freeze_authorization_grant_boundary_contract_v1.json"),
    ("task_manager_freeze_authorization_grant_non_execution_constraints", "task_manager_freeze_authorization_grant_non_execution_constraints_v1.json"),
    ("task_manager_freeze_authorization_grant_governance_debt_carryover", "task_manager_freeze_authorization_grant_governance_debt_carryover_v1.json"),
    ("task_manager_freeze_authorization_grant_next_phase_readiness", "task_manager_freeze_authorization_grant_next_phase_readiness_v1.json"),
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
    parser.add_argument("--freeze-authorization-post-review-root", default=DEFAULT_FREEZE_AUTH_POST_REVIEW_ROOT)
    parser.add_argument("--freeze-authorization-planning-root", default=DEFAULT_FREEZE_AUTH_PLANNING_ROOT)
    parser.add_argument("--output-root", default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    result = run_task_manager_foundation_handoff_freeze_authorization_grant_planning_v1(
        freeze_authorization_post_review_root=args.freeze_authorization_post_review_root,
        freeze_authorization_planning_root=args.freeze_authorization_planning_root,
        output_root=args.output_root,
    )
    out = Path(args.output_root)
    for key, fname in OUTPUT_FILES:
        _write_json(out / fname, result[key])
    (out / "task_manager_foundation_handoff_freeze_authorization_grant_plan_v1.md").write_text(
        result["task_manager_foundation_handoff_freeze_authorization_grant_plan_md"] + "\n",
        encoding="utf-8",
    )
    summary = result["summary"]
    print(
        json.dumps(
            {
                "output_root": str(out),
                "planning_pass": summary.get("planning_pass"),
                "blocker_count": summary.get("blocker_count"),
                "final_decision": summary.get("final_decision"),
                "recommended_next_phase": summary.get("recommended_next_phase"),
            },
            ensure_ascii=False,
        )
    )
    return 0 if summary.get("planning_pass") else 1


if __name__ == "__main__":
    raise SystemExit(main())
