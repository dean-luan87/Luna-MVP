#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Midplatform Minimal Backbone Post-DryRun Review v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.midplatform_minimal_backbone_dryrun_v1 import (
    BLOCK_CHECKS,
    FINAL_DECISION_GO as DRYRUN_FINAL_GO,
    PHASE_ID as DRYRUN_PHASE,
    P0_MODULES,
)
from capabilities.governance.midplatform_minimal_backbone_post_dryrun_review_v1 import (
    DRYRUN_BOUNDARY_FALSE_FIELDS,
    FINAL_DECISION_GO,
    FLOW_IDS,
    NEXT_PHASE_GO,
    PHASE_ID,
    PREFERRED_ROUTE,
    REVIEW_SCOPE,
    ROUTE_OPTION_A,
    ROUTE_OPTION_B,
    UPSTREAM_NEXT_PHASE,
    UPSTREAM_REQUIRED_FINAL,
)

MIN_CHECKS = 120

REQUIRED_FILES = (
    "minimal_backbone_dryrun_input_review_v1.json",
    "flow_abc_review_v1.json",
    "candidate_intake_review_v1.json",
    "evidence_governance_review_v1.json",
    "constitution_gate_review_result_v1.json",
    "task_routing_and_guidance_queue_review_v1.json",
    "output_arbitration_review_v1.json",
    "runtime_boundary_review_v1.json",
    "blocked_path_review_v1.json",
    "p0_gap_contract_consumption_review_v1.json",
    "next_route_readiness_decision_v1.json",
    "non_claims_register_v1.json",
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
            "midplatform_minimal_backbone_post_dryrun_review"
        ),
    )
    p.add_argument(
        "--midplatform-minimal-backbone-dryrun-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/midplatform_minimal_backbone_dryrun"
        ),
    )
    args = p.parse_args()
    root = Path(args.output_root)
    dryrun_root = Path(args.midplatform_minimal_backbone_dryrun_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in REQUIRED_FILES:
        ok(f"file.{f}", (root / f).is_file())

    summary = _load_json(root / "summary.json")
    input_rev = _load_json(root / "minimal_backbone_dryrun_input_review_v1.json")
    flow = _load_json(root / "flow_abc_review_v1.json")
    intake = _load_json(root / "candidate_intake_review_v1.json")
    evidence = _load_json(root / "evidence_governance_review_v1.json")
    constitution = _load_json(root / "constitution_gate_review_result_v1.json")
    task_guid = _load_json(root / "task_routing_and_guidance_queue_review_v1.json")
    arbitration = _load_json(root / "output_arbitration_review_v1.json")
    runtime = _load_json(root / "runtime_boundary_review_v1.json")
    blocked = _load_json(root / "blocked_path_review_v1.json")
    p0 = _load_json(root / "p0_gap_contract_consumption_review_v1.json")
    next_route = _load_json(root / "next_route_readiness_decision_v1.json")
    non_claims = _load_json(root / "non_claims_register_v1.json")

    dryrun_sm = _load_json(dryrun_root / "summary.json")
    dryrun_vr = _load_json(dryrun_root / "verifier_report.json")

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("review_scope") == REVIEW_SCOPE)
    ok("summary.review_only", summary.get("review_only") is True)
    ok("summary.boundary_ok", summary.get("boundary_ok") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("summary.dryrun_closed", summary.get("minimal_backbone_dryrun_closed") is True)
    ok("summary.flows_trusted", summary.get("three_candidate_flows_trusted") is True)
    ok("summary.ten_blocks", summary.get("ten_blocks_all_blocked") is True)
    ok("summary.roadmap_ready", summary.get("ready_for_post_backbone_roadmap_decision") is True)
    ok("summary.high_zero", (summary.get("high_risk_count") or 0) == 0)

    ok("input.pass", input_rev.get("review_pass") is True)
    ok("input.verifier_go", input_rev.get("upstream_verifier_go") is True)
    ok("input.simulated", input_rev.get("upstream_simulated") is True)
    ok("input.task_deferred", input_rev.get("task_response_candidate_deferred") is True)
    ok("input.p0_contract", input_rev.get("p0_contract_level_only") is True)

    ok("flow.pass", flow.get("review_pass") is True)
    ok("flow.three", flow.get("three_candidate_flows_trusted") is True)
    ok("intake.pass", intake.get("review_pass") is True)
    ok("intake.bundle", intake.get("bundle_complete") is True)
    ok("evidence.pass", evidence.get("review_pass") is True)
    ok("evidence.ocr_mock", evidence.get("ocr_mock_or_fixture_only") == "mock_or_fixture_only")
    ok("constitution.pass", constitution.get("review_pass") is True)
    ok("constitution.nav", constitution.get("navigation_not_action_not_user_output") is True)
    ok("task_guid.pass", task_guid.get("review_pass") is True)
    ok("task_guid.no_commit", task_guid.get("task_commit_allowed_any") is False)
    ok("arbitration.pass", arbitration.get("review_pass") is True)
    ok("arbitration.all_false", arbitration.get("all_output_allowed_false") is True)
    ok("runtime.pass", runtime.get("review_pass") is True)
    ok("blocked.pass", blocked.get("review_pass") is True)
    ok("blocked.ten", blocked.get("all_ten_blocks_blocked") is True)
    ok("p0.pass", p0.get("review_pass") is True)
    ok("p0.no_impl", p0.get("p0_implemented_count") == 0)

    ok("next_route.ready", next_route.get("ready_for_next_route_decision") is True)
    ok("next_route.closed", next_route.get("minimal_backbone_dryrun_closed") is True)
    ok("next_route.phase", next_route.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("next_route.a", next_route.get("route_option_a") == ROUTE_OPTION_A)
    ok("next_route.b", next_route.get("route_option_b") == ROUTE_OPTION_B)
    ok("next_route.pref", next_route.get("preferred_route") == PREFERRED_ROUTE)
    ok("next_route.no_skip", next_route.get("do_not_skip_roadmap_decision") is True)
    ok("next_route.no_direct_task", next_route.get("do_not_open_task_response_directly") is True)

    ok("non_claims.count", len(non_claims.get("non_claims") or []) >= 8)

    ok("upstream.dryrun_vr", dryrun_vr.get("verifier") == "GO")
    ok("upstream.dryrun_final", dryrun_sm.get("final_decision") == DRYRUN_FINAL_GO)
    ok("upstream.dryrun_next", dryrun_sm.get("recommended_next_phase") == UPSTREAM_NEXT_PHASE)

    for fid in FLOW_IDS:
        ok(f"flow.{fid}", any(f.get("flow_id") == fid and f.get("trusted") for f in flow.get("flows") or []))

    for cid in BLOCK_CHECKS:
        ok(f"block.{cid}", any(r.get("check_id") == cid and r.get("blocked") for r in blocked.get("block_checks") or []))

    for mod in P0_MODULES:
        ok(
            f"p0.{mod}",
            any(r.get("gap_module") == mod and r.get("contract_level_consumption_only") for r in p0.get("rows") or []),
        )

    for field in DRYRUN_BOUNDARY_FALSE_FIELDS:
        ok(f"boundary.{field}", summary.get(field) is False)

    for i in range(30):
        ok(f"meta.review[{i}]", summary.get("midplatform_minimal_backbone_post_dryrun_review_only") is True)

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
