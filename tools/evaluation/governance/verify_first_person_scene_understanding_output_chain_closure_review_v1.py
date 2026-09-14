#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify First Person Scene Understanding Output Chain Closure Review v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.first_person_scene_understanding_output_chain_closure_review_v1 import (
    ARTIFACT_INVENTORY_ENTRIES,
    BLOCKED_PATHS,
    BOUNDARY_FALSE,
    BOUNDARY_TRUE,
    CAPABILITY_STACK_CLOSURE_ITEMS,
    CHAIN_HOPS,
    DECISION_TO_TASK_RESP_CLOSURE_ITEMS,
    FINAL_DECISION_GO,
    GATE_COVERAGE_CLOSURE_ITEMS,
    GOVERNANCE_MAPPING_CLOSURE_ITEMS,
    HEALTH_OVERSIGHT_CLOSURE_ITEMS,
    II_TO_DECISION_CLOSURE_ITEMS,
    MEMORY_WM_TASK_NAV_BLOCK_ITEMS,
    NEXT_PHASE_GO,
    NON_CLAIMS,
    OUTPUT_TO_GATE_CLOSURE_ITEMS,
    PHASE_ID,
    SCOPE,
    TASK_RESP_TO_OUTPUT_CLOSURE_ITEMS,
    TRACEABILITY_CLOSURE_ITEMS,
)
from capabilities.governance.first_person_scene_understanding_user_output_gate_chain_dryrun_v1 import (
    FINAL_DECISION_GO as GATE_CHAIN_DR_FINAL_GO,
    NEXT_PHASE_GO as GATE_CHAIN_DR_NEXT_PHASE,
)
from capabilities.governance.layered_governance_mapping_v1 import ADDENDUM_ID

MIN_CHECKS = 213

REQUIRED = (
    "first_person_scene_understanding_output_chain_closure_review_policy_v1.json",
    "upstream_gate_chain_input_review_v1.json",
    "full_chain_artifact_inventory_v1.json",
    "scene_understanding_chain_closure_matrix_v1.json",
    "capability_stack_preservation_closure_review_v1.json",
    "layered_governance_mapping_closure_review_v1.json",
    "information_integration_to_decision_closure_review_v1.json",
    "decision_to_task_response_closure_review_v1.json",
    "task_response_to_output_candidate_closure_review_v1.json",
    "output_candidate_to_gate_chain_closure_review_v1.json",
    "gate_coverage_closure_review_v1.json",
    "health_oversight_externality_closure_review_v1.json",
    "memory_worldmodel_task_navigation_runtime_block_closure_review_v1.json",
    "traceability_chain_closure_review_v1.json",
    "closure_boundary_audit_v1.json",
    "closure_blocked_path_result_v1.json",
    "next_workstream_readiness_decision_v1.json",
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
            "first_person_scene_understanding_output_chain_closure_review"
        ),
    )
    p.add_argument(
        "--gate-chain-dryrun-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "first_person_scene_understanding_user_output_gate_chain_dryrun"
        ),
    )
    p.add_argument(
        "--output-candidate-dryrun-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "first_person_scene_understanding_output_candidate_dryrun"
        ),
    )
    p.add_argument(
        "--task-response-dryrun-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "first_person_scene_understanding_task_response_candidate_dryrun"
        ),
    )
    p.add_argument(
        "--decision-chain-dryrun-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "first_person_scene_understanding_decision_chain_candidate_dryrun"
        ),
    )
    p.add_argument(
        "--ii-chain-dryrun-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "first_person_scene_understanding_information_integration_chain_dryrun"
        ),
    )
    args = p.parse_args()
    root = Path(args.output_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in REQUIRED:
        ok(f"file.{f}", (root / f).is_file())

    gate_vr = _load(Path(args.gate_chain_dryrun_root) / "verifier_report.json")
    gate_sm = _load(Path(args.gate_chain_dryrun_root) / "summary.json")
    output_vr = _load(Path(args.output_candidate_dryrun_root) / "verifier_report.json")
    task_vr = _load(Path(args.task_response_dryrun_root) / "verifier_report.json")
    decision_vr = _load(Path(args.decision_chain_dryrun_root) / "verifier_report.json")
    ii_vr = _load(Path(args.ii_chain_dryrun_root) / "verifier_report.json")

    ok("upstream.gate_go", gate_vr.get("verifier") == "GO")
    ok("upstream.gate_final", gate_sm.get("final_decision") == GATE_CHAIN_DR_FINAL_GO)
    ok("upstream.gate_next", gate_sm.get("recommended_next_phase") == GATE_CHAIN_DR_NEXT_PHASE)
    ok("upstream.output_go", output_vr.get("verifier") == "GO")
    ok("upstream.task_go", task_vr.get("verifier") == "GO")
    ok("upstream.decision_go", decision_vr.get("verifier") == "GO")
    ok("upstream.ii_go", ii_vr.get("verifier") == "GO")

    summary = _load(root / "summary.json")
    policy = _load(root / "first_person_scene_understanding_output_chain_closure_review_policy_v1.json")
    gate_input = _load(root / "upstream_gate_chain_input_review_v1.json")
    inventory = _load(root / "full_chain_artifact_inventory_v1.json")
    matrix = _load(root / "scene_understanding_chain_closure_matrix_v1.json")
    stack_review = _load(root / "capability_stack_preservation_closure_review_v1.json")
    gov_review = _load(root / "layered_governance_mapping_closure_review_v1.json")
    ii_decision = _load(root / "information_integration_to_decision_closure_review_v1.json")
    decision_task = _load(root / "decision_to_task_response_closure_review_v1.json")
    task_output = _load(root / "task_response_to_output_candidate_closure_review_v1.json")
    output_gate = _load(root / "output_candidate_to_gate_chain_closure_review_v1.json")
    gate_cov = _load(root / "gate_coverage_closure_review_v1.json")
    health = _load(root / "health_oversight_externality_closure_review_v1.json")
    memory_block = _load(root / "memory_worldmodel_task_navigation_runtime_block_closure_review_v1.json")
    trace = _load(root / "traceability_chain_closure_review_v1.json")
    boundary = _load(root / "closure_boundary_audit_v1.json")
    blocked = _load(root / "closure_blocked_path_result_v1.json")
    next_ws = _load(root / "next_workstream_readiness_decision_v1.json")
    non_claims = _load(root / "non_claims_register_v1.json")

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("scope") == SCOPE)
    ok("summary.pass", summary.get("closure_review_pass") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)

    for field in BOUNDARY_TRUE:
        ok(f"true.{field}", summary.get(field) is True)
    for field in BOUNDARY_FALSE:
        ok(f"false.{field}", summary.get(field) is False)

    ok("policy.closure_only", policy.get("closure_review_only_not_runtime_not_output") is True)

    ok("gate_input.pass", gate_input.get("review_pass") is True)

    ok("inventory.all_present", inventory.get("all_upstream_present") is True)
    ok("inventory.count9", inventory.get("inventory_count") == len(ARTIFACT_INVENTORY_ENTRIES))
    for item in inventory.get("items") or []:
        ok(f"inventory.{item.get('artifact_id', '')[:12]}", item.get("present") is True)

    ok("matrix.pass", matrix.get("dryrun_and_review_pass") is True)
    ok("matrix.hops10", len(matrix.get("chain_hops") or []) == len(CHAIN_HOPS))
    ok("matrix.candidate_only", matrix.get("candidate_only_throughout") is True)
    ok("matrix.no_facing", matrix.get("no_user_facing_output") is True)
    ok("matrix.no_exec", matrix.get("no_execution_layer") is True)
    ok(
        "matrix.integrated",
        matrix.get("artifact_ids", {}).get("integrated_context_candidate")
        == "integrated_context_scene_understanding_chain_001",
    )
    ok(
        "matrix.enforcement",
        matrix.get("artifact_ids", {}).get("enforcement_result")
        == "enforcement_result_scene_understanding_chain_001",
    )

    for item in CAPABILITY_STACK_CLOSURE_ITEMS:
        ok(f"stack_review.{item[:18]}", stack_review.get("dryrun_and_review_pass") is True)
    ok("stack_review.l1", stack_review.get("layer_1_primary") is True)

    for item in GOVERNANCE_MAPPING_CLOSURE_ITEMS:
        ok(f"gov_review.{item[:18]}", gov_review.get("dryrun_and_review_pass") is True)
    ok("gov_review.ref", gov_review.get("layered_governance_mapping_ref") == ADDENDUM_ID)

    for item in II_TO_DECISION_CLOSURE_ITEMS:
        ok(f"ii_decision.{item[:18]}", ii_decision.get("dryrun_and_review_pass") is True)
    for item in DECISION_TO_TASK_RESP_CLOSURE_ITEMS:
        ok(f"decision_task.{item[:18]}", decision_task.get("dryrun_and_review_pass") is True)
    ok("decision_task.observe", decision_task.get("response_status") == "observe_more_candidate")

    for item in TASK_RESP_TO_OUTPUT_CLOSURE_ITEMS:
        ok(f"task_output.{item[:18]}", task_output.get("dryrun_and_review_pass") is True)
    for item in OUTPUT_TO_GATE_CLOSURE_ITEMS:
        ok(f"output_gate.{item[:18]}", output_gate.get("dryrun_and_review_pass") is True)

    for item in GATE_COVERAGE_CLOSURE_ITEMS:
        ok(f"gate_cov.{item[:18]}", gate_cov.get("dryrun_and_review_pass") is True)
    ok("gate_cov.count16", gate_cov.get("gate_count") == 16)

    for item in HEALTH_OVERSIGHT_CLOSURE_ITEMS:
        ok(f"health.{item[:18]}", health.get("dryrun_and_review_pass") is True)
    ok("health.external", health.get("health_oversight_external") is True)

    for item in MEMORY_WM_TASK_NAV_BLOCK_ITEMS:
        ok(f"memory_block.{item[:18]}", memory_block.get("dryrun_and_review_pass") is True)

    for item in TRACEABILITY_CLOSURE_ITEMS:
        ok(f"trace.{item[:18]}", trace.get("dryrun_and_review_pass") is True)
    ok("trace.uoc", trace.get("user_output_ref") == "user_output_scene_understanding_chain_001")

    ok("boundary.audit_pass", boundary.get("audit_pass") is True)
    for field in BOUNDARY_FALSE:
        ok(f"boundary.{field}", boundary.get("boundary_fields", {}).get(field) is False)

    ok("blocked.all", blocked.get("all_blocked") is True)
    ok("blocked.count24", blocked.get("blocked_count") == 24)
    for path in BLOCKED_PATHS:
        ok(
            f"blocked.{path[:18]}",
            any(
                b.get("path_id") == path and b.get("status") == "blocked"
                for b in (blocked.get("blocked_paths") or [])
            ),
        )

    ok("next_ws.ready", next_ws.get("ready_for_scenario_model_governance_planning") is True)
    ok("next_ws.final", next_ws.get("final_decision") == FINAL_DECISION_GO)
    ok("next_ws.phase", next_ws.get("recommended_next_phase") == NEXT_PHASE_GO)

    for claim in NON_CLAIMS:
        ok(f"non_claim.{claim[:18]}", claim in (non_claims.get("non_claims") or []))

    total = len(checks)
    passed = sum(1 for c in checks if c["passed"])
    min_checks = MIN_CHECKS if MIN_CHECKS else total
    verifier = "GO" if passed == total and passed >= min_checks else "NO_GO"
    report = {
        "phase": PHASE_ID,
        "verifier": verifier,
        "checks_passed": passed,
        "checks_total": total,
        "min_checks": min_checks,
        "closure_review_pass": summary.get("closure_review_pass"),
        "final_decision": summary.get("final_decision"),
        "recommended_next_phase": summary.get("recommended_next_phase"),
        "checks": checks,
    }
    (root / "verifier_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps({"verifier": verifier, "checks_passed": passed, "checks_total": total}))
    return 0 if verifier == "GO" else 1


if __name__ == "__main__":
    raise SystemExit(main())
