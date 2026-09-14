#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run upstream GO artifact chain bootstrap for SLAM P0 v1."""

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

from capabilities.midplatform.upstream_go_artifact_chain_bootstrap_for_slam_p0_lineage_v1 import ARTIFACTS
from capabilities.midplatform.upstream_go_artifact_chain_bootstrap_for_slam_p0_items_v1 import DEFAULT_OUTPUT
from capabilities.midplatform.upstream_go_artifact_chain_bootstrap_for_slam_p0_v1 import (
    run_upstream_go_artifact_chain_bootstrap_for_slam_p0_v1,
)

OUTPUT_FILES = (
    ("upstream_go_artifact_chain_bootstrap_for_slam_p0_report", "upstream_go_artifact_chain_bootstrap_for_slam_p0_report_v1.json"),
    ("upstream_blocked_chain_review", "upstream_blocked_chain_review_v1.json"),
    ("bootstrap_stage_run_registry", "bootstrap_stage_run_registry_v1.json"),
    ("bootstrap_stage_verifier_registry", "bootstrap_stage_verifier_registry_v1.json"),
    ("first_non_go_stage_review", "first_non_go_stage_review_v1.json"),
    ("slam_p0_upstream_readiness_review", "slam_p0_upstream_readiness_review_v1.json"),
    ("slam_p0_revalidation_visibility_review", "slam_p0_revalidation_visibility_review_v1.json"),
    ("no_protocol_change_review", "no_protocol_change_review_v1.json"),
    ("no_world_model_boundary_review", "no_world_model_boundary_review_v1.json"),
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
    result = run_upstream_go_artifact_chain_bootstrap_for_slam_p0_v1(output_root=args.output_root)
    out = Path(args.output_root)
    out.mkdir(parents=True, exist_ok=True)
    for key, fname in OUTPUT_FILES:
        (out / fname).write_text(
            json.dumps(result[key], ensure_ascii=False, indent=2, default=_default) + "\n",
            encoding="utf-8",
        )
    (out / "upstream_go_artifact_chain_bootstrap_for_slam_p0_report_v1.md").write_text(
        result["upstream_go_artifact_chain_bootstrap_for_slam_p0_report_md"] + "\n",
        encoding="utf-8",
    )
    s = result["summary"]
    print(json.dumps({
        "output_root": str(out),
        "upstream_go_artifact_chain_bootstrap_for_slam_p0_pass": s.get("upstream_go_artifact_chain_bootstrap_for_slam_p0_pass"),
        "upstream_bootstrap_complete": s.get("upstream_bootstrap_complete"),
        "first_non_go_stage": s.get("first_non_go_stage"),
        "bootstrap_stop_reason": s.get("bootstrap_stop_reason"),
        "p0_visible_to_scene_graph_review": s.get("p0_visible_to_scene_graph_review"),
        "final_decision": s.get("final_decision"),
        "recommended_next_phase": s.get("recommended_next_phase"),
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
