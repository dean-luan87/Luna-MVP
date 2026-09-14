#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run SLAM spatial mapping task collaboration planning revalidation v1."""

from __future__ import annotations

import json
import subprocess
import sys
from argparse import ArgumentParser
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.midplatform.slam_spatial_mapping_task_collaboration_planning_revalidation_v1 import (
    DEFAULT_OUTPUT,
    run_slam_spatial_mapping_task_collaboration_planning_revalidation_v1,
)
from capabilities.midplatform.slam_spatial_mapping_task_collaboration_planning_v1 import (
    DEFAULT_OUTPUT as DEFAULT_PLANNING_ROOT,
)

OUTPUT_FILES = (
    ("slam_task_collaboration_revalidation_report", "slam_task_collaboration_revalidation_report_v1.json"),
    ("slam_task_collaboration_bootstrap_review", "slam_task_collaboration_bootstrap_review_v1.json"),
    ("slam_task_collaboration_p0_visibility_review", "slam_task_collaboration_p0_visibility_review_v1.json"),
    ("slam_task_collaboration_artifact_alignment_review", "slam_task_collaboration_artifact_alignment_review_v1.json"),
    ("file_size_governance_review", "file_size_governance_review_v1.json"),
    ("summary", "summary.json"),
)


def main() -> int:
    parser = ArgumentParser()
    parser.add_argument("--planning-root", default=DEFAULT_PLANNING_ROOT)
    parser.add_argument("--output-root", default=DEFAULT_OUTPUT)
    parser.add_argument("--bootstrap-passes", type=int, default=0)
    args = parser.parse_args()
    result = run_slam_spatial_mapping_task_collaboration_planning_revalidation_v1(
        planning_root=args.planning_root,
        output_root=args.output_root,
        bootstrap_passes=args.bootstrap_passes,
    )
    out = Path(args.output_root)
    out.mkdir(parents=True, exist_ok=True)
    for key, fname in OUTPUT_FILES:
        (out / fname).write_text(
            json.dumps(result[key], ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
    (out / "slam_task_collaboration_revalidation_report_v1.md").write_text(
        result["slam_task_collaboration_revalidation_report_md"] + "\n",
        encoding="utf-8",
    )
    verify_proc = subprocess.run(
        [sys.executable, str(REPO_ROOT / "tools/evaluation/midplatform/verify_slam_spatial_mapping_task_collaboration_planning_revalidation_v1.py"), "--output-root", str(out)],
        capture_output=True,
        text=True,
    )
    s = result["summary"]
    print(json.dumps({
        "output_root": str(out),
        "planning_root": s.get("planning_root"),
        "slam_task_collaboration_planning_revalidation_pass": s.get("slam_task_collaboration_planning_revalidation_pass"),
        "prior_planning_go": s.get("prior_slam_spatial_mapping_task_collaboration_planning_go"),
        "verifier_exit_code": verify_proc.returncode,
        "final_decision": s.get("final_decision"),
        "recommended_next_phase": s.get("recommended_next_phase"),
        "blocker_count": s.get("blocker_count"),
        "issues": s.get("issues"),
    }, ensure_ascii=False))
    return 0 if s.get("slam_task_collaboration_planning_revalidation_pass") and verify_proc.returncode == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
