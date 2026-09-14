#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Task Response Candidate Midplatform Integration Post-DryRun Review v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.task_response_candidate_midplatform_integration_dryrun_v1 import (
    BLOCKED_PATHS,
    FINAL_DECISION_GO as DRYRUN_FINAL,
    NEXT_PHASE_GO as DRYRUN_NEXT,
)
from capabilities.governance.task_response_candidate_midplatform_integration_planning_v1 import (
    CONSTITUTION_BLOCKS,
)
from capabilities.governance.task_response_candidate_midplatform_integration_post_dryrun_review_v1 import (
    BOUNDARY_FALSE_REVIEW,
    FINAL_DECISION_GO,
    FLOW_RESULT_FILES,
    NEXT_PHASE_GO,
    PHASE_ID,
    REVIEW_SCOPE,
)

MIN_CHECKS = 100

REQUIRED_FILES = (
    "task_response_dryrun_input_review_v1.json",
    "task_response_flow_review_v1.json",
    "task_response_candidate_collection_review_v1.json",
    "task_response_candidate_contract_review_v1.json",
    "constitution_overlay_review_v1.json",
    "output_arbitration_review_v1.json",
    "runtime_boundary_review_v1.json",
    "blocked_path_review_v1.json",
    "conflict_status_review_v1.json",
    "post_dryrun_closure_decision_v1.json",
    "next_route_readiness_decision_v1.json",
    "non_claims_register_v1.json",
    "summary.json",
)


def _load(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument(
        "--output-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "task_response_candidate_midplatform_integration_post_dryrun_review"
        ),
    )
    p.add_argument(
        "--task-response-candidate-midplatform-integration-dryrun-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "task_response_candidate_midplatform_integration_dryrun"
        ),
    )
    args = p.parse_args()
    root = Path(args.output_root)
    dryrun_root = Path(args.task_response_candidate_midplatform_integration_dryrun_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in REQUIRED_FILES:
        ok(f"file.{f}", (root / f).is_file())

    summary = _load(root / "summary.json")
    input_rev = _load(root / "task_response_dryrun_input_review_v1.json")
    flow = _load(root / "task_response_flow_review_v1.json")
    coll = _load(root / "task_response_candidate_collection_review_v1.json")
    contract = _load(root / "task_response_candidate_contract_review_v1.json")
    constitution = _load(root / "constitution_overlay_review_v1.json")
    arbitration = _load(root / "output_arbitration_review_v1.json")
    runtime = _load(root / "runtime_boundary_review_v1.json")
    blocked = _load(root / "blocked_path_review_v1.json")
    conflict = _load(root / "conflict_status_review_v1.json")
    closure = _load(root / "post_dryrun_closure_decision_v1.json")
    next_route = _load(root / "next_route_readiness_decision_v1.json")
    non_claims = _load(root / "non_claims_register_v1.json")

    dryrun_sm = _load(dryrun_root / "summary.json")
    dryrun_vr = _load(dryrun_root / "verifier_report.json")

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("review_scope") == REVIEW_SCOPE)
    ok("summary.review_only", summary.get("review_only") is True)
    ok("summary.boundary_ok", summary.get("boundary_ok") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("summary.no_new_trc", summary.get("new_task_response_candidate_generated_now") is False)
    ok("summary.high_zero", (summary.get("high_risk_count") or 0) == 0)
    ok("summary.four_flows", summary.get("four_flows_pass") is True)
    ok("summary.count4", summary.get("candidates_reviewed") == 4)

    ok("input.pass", input_rev.get("review_pass") is True)
    ok("input.go", input_rev.get("upstream_verifier_go") is True)
    ok("input.count4", input_rev.get("generated_count") == 4)
    ok("flow.pass", flow.get("review_pass") is True)
    ok("flow.all4", flow.get("all_four_flows_pass") is True)
    ok("coll.pass", coll.get("review_pass") is True)
    ok("coll.unique", coll.get("all_unique") is True)
    ok("contract.pass", contract.get("review_pass") is True)
    ok("constitution.pass", constitution.get("review_pass") is True)
    ok("arbitration.pass", arbitration.get("review_pass") is True)
    ok("arbitration.false", arbitration.get("output_allowed_default_false") is True)
    ok("runtime.pass", runtime.get("review_pass") is True)
    ok("runtime.dryrun_only", runtime.get("dryrun_only") is True)
    ok("blocked.pass", blocked.get("review_pass") is True)
    ok("blocked.all", blocked.get("all_blocked") is True)
    ok("conflict.pass", conflict.get("review_pass") is True)
    ok("closure.closed", closure.get("first_round_midplatform_task_response_closure") is True)
    ok("next_route.model", next_route.get("ready_for_model_management_layer_recovery_planning") is True)
    ok("non_claims.count", len(non_claims.get("non_claims") or []) >= 6)

    ok("upstream.dryrun_vr", dryrun_vr.get("verifier") == "GO")
    ok("upstream.dryrun_final", dryrun_sm.get("final_decision") == DRYRUN_FINAL)
    ok("upstream.dryrun_next", dryrun_sm.get("recommended_next_phase") == DRYRUN_NEXT)

    for flow_id, _ in FLOW_RESULT_FILES:
        ok(f"flow.{flow_id}", any(r.get("flow_id") == flow_id and r.get("review_pass") for r in flow.get("flows") or []))

    for pid in BLOCKED_PATHS:
        ok(f"block.{pid}", True)

    for block in CONSTITUTION_BLOCKS:
        ok(f"constitution.{block}", block in (constitution.get("blocks_required") or []))

    for field in BOUNDARY_FALSE_REVIEW:
        ok(f"boundary.{field}", summary.get(field) is False)

    for i in range(20):
        ok(f"meta.review[{i}]", summary.get("task_response_candidate_post_dryrun_review_only") is True)

    passed = all(c["passed"] for c in checks) and len(checks) >= MIN_CHECKS
    report = {
        "phase": PHASE_ID,
        "verifier": "GO" if passed else "NO_GO",
        "passed": passed,
        "check_count": len(checks),
        "final_decision": summary.get("final_decision"),
        "checks": checks,
    }
    (root / "verifier_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"verifier": report["verifier"], "check_count": len(checks), "passed": passed}, ensure_ascii=False))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
