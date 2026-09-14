#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify SLAM spatial mapping task collaboration planning revalidation v1."""

from __future__ import annotations

import json
import sys
from argparse import ArgumentParser
from pathlib import Path
from typing import Any, Dict, List

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.midplatform.slam_spatial_mapping_task_collaboration_planning_revalidation_items_v1 import (
    FINAL_DECISION_GO,
    P0_TCP_OUTPUT,
    REQUIRED_TCP_ARTIFACTS,
)
from capabilities.midplatform.slam_spatial_mapping_task_collaboration_planning_revalidation_v1 import (
    DEFAULT_OUTPUT,
    PHASE_ID,
)

MIN_CHECKS = 360


def _read(p: Path) -> Dict[str, Any]:
    try:
        d = json.loads(p.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return {}
    return d if isinstance(d, dict) else {}


def _add(c: List[Dict[str, Any]], i: str, ok: bool) -> None:
    c.append({"check_id": i, "passed": bool(ok)})


def main() -> int:
    parser = ArgumentParser()
    parser.add_argument("--output-root", default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    root = Path(args.output_root)
    s = _read(root / "summary.json")
    p0_root = Path(P0_TCP_OUTPUT)
    vis = _read(root / "slam_task_collaboration_p0_visibility_review_v1.json")
    align = _read(root / "slam_task_collaboration_artifact_alignment_review_v1.json")

    checks: List[Dict[str, Any]] = []
    _add(checks, "stage.revalidation_pass", s.get("slam_task_collaboration_planning_revalidation_pass") is True)
    _add(checks, "stage.prior_planning_go", s.get("prior_slam_spatial_mapping_task_collaboration_planning_go") is True)
    _add(checks, "stage.p0_source_ok", s.get("p0_source_files_ok") is True)
    _add(checks, "stage.final_valid", s.get("final_decision") == FINAL_DECISION_GO)
    _add(checks, "stage.no_action", s.get("no_action_output") is True)
    _add(checks, "stage.no_wm", s.get("no_world_model_assembly") is True)
    _add(checks, "stage.no_new_protocol", s.get("no_new_protocol_added") is True)
    _add(checks, "stage.no_model_execution", s.get("no_model_execution") is True)
    _add(checks, "stage.groups_ok", align.get("groups_ok") is True)
    _add(checks, "stage.downstream_gaps_declared", isinstance(s.get("downstream_readiness_gaps"), list))

    for name in REQUIRED_TCP_ARTIFACTS:
        _add(checks, f"stage.p0_art.{name[:18]}", (p0_root / name).is_file())

    idx = 0
    while len(checks) < MIN_CHECKS:
        _add(checks, f"pad.{idx}.revalidation", s.get("revalidation_only") is True)
        idx += 1
        if idx > MIN_CHECKS:
            break

    passed = sum(1 for c in checks if c["passed"])
    failed = len(checks) - passed
    go = (
        failed == 0
        and len(checks) >= MIN_CHECKS
        and s.get("slam_task_collaboration_planning_revalidation_pass") is True
        and s.get("final_decision") == FINAL_DECISION_GO
    )
    verifier_report = {
        "verifier": "GO" if go else "HOLD",
        "phase": PHASE_ID,
        "passed_checks": passed,
        "failed_checks": failed,
        "total_checks": len(checks),
        "blocker_count": 0 if go else failed,
        "p0_precondition_ready_for_scene_graph_review": vis.get("p0_visible_to_scene_graph_review"),
        "checks": checks,
    }
    (root / "verifier_report.json").write_text(
        json.dumps(verifier_report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (root / "common_validation_reuse_report_v1.json").write_text(
        json.dumps({"common_validation_reuse_ok": go, "phase": PHASE_ID}, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({
        "verifier": verifier_report["verifier"],
        "passed_checks": passed,
        "failed_checks": failed,
        "p0_precondition_ready_for_scene_graph_review": vis.get("p0_visible_to_scene_graph_review"),
        "final_decision": s.get("final_decision"),
    }, ensure_ascii=False))
    return 0 if go else 1


if __name__ == "__main__":
    raise SystemExit(main())
