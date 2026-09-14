#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Midplatform Minimal Backbone Post-DryRun Review v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.midplatform_minimal_backbone_post_dryrun_review_v1 import (
    run_midplatform_minimal_backbone_post_dryrun_review_v1,
)

DEFAULT_DRYRUN_ROOT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/midplatform_minimal_backbone_dryrun"
)
DEFAULT_OUTPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_minimal_backbone_post_dryrun_review"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    ("minimal_backbone_dryrun_input_review", "minimal_backbone_dryrun_input_review_v1.json"),
    ("flow_abc_review", "flow_abc_review_v1.json"),
    ("candidate_intake_review", "candidate_intake_review_v1.json"),
    ("evidence_governance_review", "evidence_governance_review_v1.json"),
    ("constitution_gate_review_result", "constitution_gate_review_result_v1.json"),
    ("task_routing_and_guidance_queue_review", "task_routing_and_guidance_queue_review_v1.json"),
    ("output_arbitration_review", "output_arbitration_review_v1.json"),
    ("runtime_boundary_review", "runtime_boundary_review_v1.json"),
    ("blocked_path_review", "blocked_path_review_v1.json"),
    ("p0_gap_contract_consumption_review", "p0_gap_contract_consumption_review_v1.json"),
    ("next_route_readiness_decision", "next_route_readiness_decision_v1.json"),
    ("non_claims_register", "non_claims_register_v1.json"),
)


def _write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=DEFAULT_OUTPUT_ROOT)
    p.add_argument("--midplatform-minimal-backbone-dryrun-root", default=DEFAULT_DRYRUN_ROOT)
    args = p.parse_args()

    result = run_midplatform_minimal_backbone_post_dryrun_review_v1(
        midplatform_minimal_backbone_dryrun_root=args.midplatform_minimal_backbone_dryrun_root,
        review_output_root=args.output_root,
    )

    out_root = Path(args.output_root)
    for key, filename in OUTPUT_FILES:
        _write_json(out_root / filename, result[key])

    summary = result["summary"]
    print(
        json.dumps(
            {
                "output_root": str(out_root),
                "boundary_ok": summary.get("boundary_ok"),
                "final_decision": summary.get("final_decision"),
                "recommended_next_phase": summary.get("recommended_next_phase"),
                "three_flows_trusted": summary.get("three_candidate_flows_trusted"),
                "ten_blocks_blocked": summary.get("ten_blocks_all_blocked"),
            },
            ensure_ascii=False,
        )
    )
    return 0 if summary.get("boundary_ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
