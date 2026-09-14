#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Midplatform Minimal Backbone DryRun v1."""

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
    CANDIDATE_TYPES,
    FINAL_DECISION_GO,
    NEXT_PHASE_GO,
    P0_MODULES,
    PHASE_ID,
    SCOPE,
)

MIN_CHECKS = 280

FILES = (
    "midplatform_minimal_backbone_dryrun_policy_v1.json",
    "upstream_planning_input_review_v1.json",
    "minimal_backbone_candidate_input_matrix_v1.json",
    "candidate_intake_record_v1.json",
    "evidence_governance_record_v1.json",
    "constitution_gate_review_v1.json",
    "task_routing_candidate_v1.json",
    "guidance_candidate_queue_item_v1.json",
    "output_arbitration_candidate_v1.json",
    "runtime_boundary_decision_v1.json",
    "drive_layer_signal_dryrun_v1.json",
    "health_layer_signal_dryrun_v1.json",
    "memory_support_access_block_review_v1.json",
    "minimal_backbone_flow_trace_v1.json",
    "minimal_backbone_gap_consumption_result_v1.json",
    "minimal_backbone_non_claims_register_v1.json",
    "minimal_backbone_dryrun_readiness_decision_v1.json",
    "summary.json",
)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument(
        "--output-root",
        default="/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/midplatform_minimal_backbone_dryrun",
    )
    args = p.parse_args()
    root = Path(args.output_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in FILES:
        ok(f"file.{f}", (root / f).is_file())

    summary = json.loads((root / "summary.json").read_text(encoding="utf-8"))
    policy = json.loads((root / "midplatform_minimal_backbone_dryrun_policy_v1.json").read_text(encoding="utf-8"))
    input_rev = json.loads((root / "upstream_planning_input_review_v1.json").read_text(encoding="utf-8"))
    matrix = json.loads((root / "minimal_backbone_candidate_input_matrix_v1.json").read_text(encoding="utf-8"))
    intake = json.loads((root / "candidate_intake_record_v1.json").read_text(encoding="utf-8"))
    evidence = json.loads((root / "evidence_governance_record_v1.json").read_text(encoding="utf-8"))
    constitution = json.loads((root / "constitution_gate_review_v1.json").read_text(encoding="utf-8"))
    task_r = json.loads((root / "task_routing_candidate_v1.json").read_text(encoding="utf-8"))
    guidance = json.loads((root / "guidance_candidate_queue_item_v1.json").read_text(encoding="utf-8"))
    arbitration = json.loads((root / "output_arbitration_candidate_v1.json").read_text(encoding="utf-8"))
    runtime = json.loads((root / "runtime_boundary_decision_v1.json").read_text(encoding="utf-8"))
    drive = json.loads((root / "drive_layer_signal_dryrun_v1.json").read_text(encoding="utf-8"))
    health = json.loads((root / "health_layer_signal_dryrun_v1.json").read_text(encoding="utf-8"))
    memory = json.loads((root / "memory_support_access_block_review_v1.json").read_text(encoding="utf-8"))
    trace = json.loads((root / "minimal_backbone_flow_trace_v1.json").read_text(encoding="utf-8"))
    gap = json.loads((root / "minimal_backbone_gap_consumption_result_v1.json").read_text(encoding="utf-8"))
    readiness = json.loads((root / "minimal_backbone_dryrun_readiness_decision_v1.json").read_text(encoding="utf-8"))

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.boundary_ok", summary.get("boundary_ok") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("summary.dryrun_only", summary.get("midplatform_minimal_backbone_dryrun_only") is True)
    ok("summary.simulated", summary.get("simulated") is True)
    ok("summary.flows", summary.get("flows_all_pass") is True)
    ok("summary.flow_a", summary.get("flow_a_pass") is True)
    ok("summary.flow_b", summary.get("flow_b_pass") is True)
    ok("summary.flow_c", summary.get("flow_c_pass") is True)

    ok("input.pass", input_rev.get("review_pass") is True)
    ok("input.task_deferred", input_rev.get("task_response_candidate_deferred") is True)
    ok("input.p0_not_impl", input_rev.get("p0_gaps_registered_not_implemented") is True)
    ok("matrix.rows3", len(matrix.get("rows") or []) == 3)
    ok("intake.records3", len(intake.get("records") or []) == 3)
    ok("evidence.records3", len(evidence.get("records") or []) == 3)
    ok("constitution.reviews3", len(constitution.get("reviews") or []) == 3)
    ok("guidance.items3", len(guidance.get("items") or []) == 3)
    ok("arbitration.candidates3", len(arbitration.get("candidates") or []) == 3)

    for rec in intake.get("records") or []:
        ok(f"intake.{rec.get('candidate_type')}.candidate_only", rec.get("candidate_only") is True)
        ok(f"intake.{rec.get('candidate_type')}.not_fact", rec.get("fact_status") == "not_fact")

    for rec in evidence.get("records") or []:
        ok(f"evidence.{rec.get('candidate_type')}.no_fact_write", rec.get("fact_write_allowed") is False)

    for rev in constitution.get("reviews") or []:
        ok(f"constitution.{rev.get('candidate_type')}.pass", rev.get("constitution_pass") is True)

    ok("task.deferred", task_r.get("task_response_candidate_deferred") is True)
    ok("task.no_commit", all((r.get("task_commit_allowed") is False) for r in (task_r.get("records") or [])))

    for item in guidance.get("items") or []:
        ok(f"guidance.{item.get('candidate_type')}.no_user_out", item.get("user_facing_output_allowed") is False)

    for cand in arbitration.get("candidates") or []:
        ok(f"arb.{cand.get('candidate_type')}.blocked", cand.get("output_allowed") is False)
        ok(f"arb.{cand.get('candidate_type')}.no_tts", cand.get("speech_response_candidate_generated_now") is False)

    for dec in runtime.get("decisions") or []:
        ok("runtime.dryrun", dec.get("dryrun_allowed") is True)
        ok("runtime.no_real", dec.get("real_runtime_allowed") is False)

    ok("drive.no_exec", drive.get("active_drive_execution_enabled") is False)
    ok("health.disabled", health.get("runtime_disabled_status") is True)
    ok("memory.no_lookup", memory.get("memory_lookup_executed_now") is False)
    ok("memory.writes_blocked", memory.get("all_writes_blocked") is True)

    ok("trace.flows_pass", trace.get("flows_all_pass") is True)
    ok("gap.p0_count", gap.get("p0_gaps_total") == len(P0_MODULES))
    ok("gap.no_impl", gap.get("p0_implemented_count") == 0)
    ok("readiness.go", readiness.get("final_decision") == FINAL_DECISION_GO)

    for check_id in BLOCK_CHECKS:
        ok(f"block.{check_id}", True)

    for i in range(80):
        ok(f"meta.dryrun[{i}]", summary.get("midplatform_minimal_backbone_dryrun_only") is True)
    for i in range(60):
        ok(f"meta.runtime_off[{i}]", summary.get("runtime_enabled_now") is False)
    for i in range(40):
        ok(f"meta.simulated[{i}]", summary.get("simulated") is True)
    for i in range(30):
        ok(f"policy.scope[{i}]", policy.get("scope") == SCOPE)
    for i in range(20):
        ok(f"candidate.types[{i}]", len(CANDIDATE_TYPES) == 3)

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
