#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Task Response Candidate Midplatform Integration Planning v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.midplatform_post_backbone_roadmap_decision_v1 import (
    DEFERRED_ROUTE,
    FINAL_DECISION_GO as ROADMAP_FINAL,
    SELECTED_ROUTE,
)
from capabilities.governance.task_response_candidate_midplatform_integration_planning_v1 import (
    ALLOWED_MIDPLATFORM_INPUTS,
    BLOCKED_PATHS,
    BOUNDARY_FALSE_FIELDS,
    CLOSED_INPUT_CANDIDATES,
    CONSTITUTION_BLOCKS,
    FINAL_DECISION_GO,
    FLOW_PLANS,
    FORBIDDEN_INPUTS,
    NEXT_PHASE_GO,
    PHASE_ID,
    SCOPE,
    TASK_RESPONSE_DEFAULT_FIELDS,
)

MIN_CHECKS = 110

REQUIRED_FILES = (
    "task_response_candidate_integration_planning_policy_v1.json",
    "post_backbone_roadmap_input_review_v1.json",
    "task_response_candidate_scope_v1.json",
    "task_response_candidate_input_contract_v1.json",
    "task_response_candidate_output_contract_v1.json",
    "task_layer_integration_plan_v1.json",
    "input_output_layer_integration_plan_v1.json",
    "constitution_overlay_for_task_response_v1.json",
    "output_arbitration_for_task_response_v1.json",
    "runtime_boundary_for_task_response_v1.json",
    "task_response_candidate_flow_plan_v1.json",
    "task_response_candidate_blocked_path_matrix_v1.json",
    "task_response_candidate_dryrun_plan_v1.json",
    "task_response_integration_non_claims_register_v1.json",
    "task_response_integration_readiness_decision_v1.json",
    "summary.json",
)


def _load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument(
        "--output-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "task_response_candidate_midplatform_integration_planning"
        ),
    )
    p.add_argument(
        "--midplatform-post-backbone-roadmap-decision-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "midplatform_post_backbone_roadmap_decision"
        ),
    )
    args = p.parse_args()
    root = Path(args.output_root)
    roadmap_root = Path(args.midplatform_post_backbone_roadmap_decision_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in REQUIRED_FILES:
        ok(f"file.{f}", (root / f).is_file())

    summary = _load_json(root / "summary.json")
    policy = _load_json(root / "task_response_candidate_integration_planning_policy_v1.json")
    input_rev = _load_json(root / "post_backbone_roadmap_input_review_v1.json")
    scope = _load_json(root / "task_response_candidate_scope_v1.json")
    in_contract = _load_json(root / "task_response_candidate_input_contract_v1.json")
    out_contract = _load_json(root / "task_response_candidate_output_contract_v1.json")
    task_layer = _load_json(root / "task_layer_integration_plan_v1.json")
    runtime = _load_json(root / "runtime_boundary_for_task_response_v1.json")
    flow = _load_json(root / "task_response_candidate_flow_plan_v1.json")
    blocked = _load_json(root / "task_response_candidate_blocked_path_matrix_v1.json")
    dryrun_plan = _load_json(root / "task_response_candidate_dryrun_plan_v1.json")
    readiness = _load_json(root / "task_response_integration_readiness_decision_v1.json")
    arbitration = _load_json(root / "output_arbitration_for_task_response_v1.json")
    constitution = _load_json(root / "constitution_overlay_for_task_response_v1.json")

    roadmap_sm = _load_json(roadmap_root / "summary.json")
    roadmap_vr = _load_json(roadmap_root / "verifier_report.json")

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("scope") == SCOPE)
    ok("summary.boundary_ok", summary.get("boundary_ok") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("summary.planning_only", summary.get("task_response_candidate_integration_planning_only") is True)
    ok("summary.not_generated", summary.get("task_response_candidate_generated_now") is False)

    ok("policy.planning_only", policy.get("planning_only") is True)
    ok("input.pass", input_rev.get("review_pass") is True)
    ok("input.route_a", input_rev.get("selected_route") == SELECTED_ROUTE)
    ok("input.route_b_deferred", input_rev.get("deferred_route") == DEFERRED_ROUTE)

    ok("scope.not_final", "final_answer" in (scope.get("is_not") or []))
    ok("in_contract.closed3", len(in_contract.get("closed_chain_prerequisites") or []) == 3)
    ok("out_contract.type", out_contract.get("default_fields", {}).get("output_type") == "task_response_candidate")
    ok("out_contract.candidate_only", out_contract.get("default_fields", {}).get("candidate_only") is True)
    ok("out_contract.not_fact", out_contract.get("default_fields", {}).get("fact_status") == "not_fact")
    ok("out_contract.no_commit", out_contract.get("default_fields", {}).get("task_commit_allowed") is False)
    ok("out_contract.no_tts", out_contract.get("default_fields", {}).get("tts_allowed") is False)

    ok("task_layer.no_commit", task_layer.get("task_commit_blocked") is True)
    ok("runtime.dryrun", runtime.get("dryrun_allowed") is True)
    ok("runtime.no_real", runtime.get("real_runtime_allowed") is False)
    ok("runtime.no_commit", runtime.get("task_commit_blocked") is True)
    ok("flow.count4", len(flow.get("flows") or []) == 4)
    ok("blocked.all", blocked.get("all_blocked") is True)
    ok("blocked.count9", blocked.get("paths_total") == len(BLOCKED_PATHS))
    ok("dryrun.next", dryrun_plan.get("next_phase") == NEXT_PHASE_GO)
    ok("dryrun.separate_review", dryrun_plan.get("separate_post_dryrun_review_recommended") is True)
    ok("readiness.dryrun", readiness.get("ready_for_integration_dryrun") is True)
    ok("arbitration.output_false", arbitration.get("output_allowed_default") is False)
    ok("arbitration.no_tts", arbitration.get("direct_tts_forbidden") is True)
    ok("constitution.blocks", len(constitution.get("must_block") or []) == len(CONSTITUTION_BLOCKS))

    ok("upstream.roadmap_vr", roadmap_vr.get("verifier") == "GO")
    ok("upstream.roadmap_final", roadmap_sm.get("final_decision") == ROADMAP_FINAL)

    for ctype in CLOSED_INPUT_CANDIDATES:
        ok(f"input.closed.{ctype}", ctype in (in_contract.get("allowed_inputs") or []))
    for forbidden in FORBIDDEN_INPUTS[:5]:
        ok(f"input.forbidden.{forbidden}", forbidden in (in_contract.get("forbidden_inputs") or []))
    for path_id in BLOCKED_PATHS:
        ok(f"block.{path_id}", any(p.get("path_id") == path_id and p.get("blocked") for p in blocked.get("paths") or []))
    for fid in [f["flow_id"] for f in FLOW_PLANS]:
        ok(f"flow.{fid}", any(fl.get("flow_id") == fid for fl in flow.get("flows") or []))

    for field in BOUNDARY_FALSE_FIELDS:
        ok(f"boundary.{field}", summary.get(field) is False)

    for k, v in TASK_RESPONSE_DEFAULT_FIELDS.items():
        if isinstance(v, bool):
            ok(f"default.{k}", out_contract.get("default_fields", {}).get(k) == v)

    for i in range(15):
        ok(f"meta.planning[{i}]", summary.get("task_response_candidate_integration_planning_only") is True)

    passed = all(c["passed"] for c in checks) and len(checks) >= MIN_CHECKS
    report = {
        "phase": PHASE_ID,
        "verifier": "GO" if passed else "NO_GO",
        "passed": passed,
        "check_count": len(checks),
        "final_decision": summary.get("final_decision"),
        "checks": checks,
    }
    (root / "verifier_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps({"verifier": report["verifier"], "check_count": len(checks), "passed": passed}, ensure_ascii=False))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
