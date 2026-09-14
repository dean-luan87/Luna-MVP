#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Midplatform Task Response Candidate Integration DryRunAndReview v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.midplatform_task_response_candidate_integration_dryrun_and_review_v1 import (
    ACTION_MAPPING_DRYRUN,
    BLOCKED_PATHS,
    BOUNDARY_FALSE,
    BOUNDARY_TRUE,
    FINAL_DECISION_GO,
    NEXT_PHASE_GO,
    NON_CLAIMS,
    PHASE_ID,
    SCOPE,
    UPSTREAM_PLANNING_FINAL,
    UPSTREAM_PLANNING_NEXT,
)
from capabilities.governance.midplatform_task_response_candidate_integration_planning_v1 import (
    DECISION_CANDIDATE_INTAKE_FIELDS,
    FAILURE_ESCALATION_RESPONSES,
    TASK_RESPONSE_OUTPUT_FIELDS,
)

MIN_CHECKS = 206

REQUIRED = (
    "task_response_candidate_integration_dryrun_review_policy_v1.json",
    "task_response_candidate_planning_input_review_v1.json",
    "task_response_integration_model_candidate_v1.json",
    "sample_decision_candidate_intake_v1.json",
    "sample_task_response_candidate_v1.json",
    "response_action_mapping_dryrun_review_v1.json",
    "uncertainty_evidence_preservation_review_v1.json",
    "safety_constitution_output_boundary_review_v1.json",
    "speech_output_boundary_review_v1.json",
    "memory_worldmodel_write_boundary_review_v1.json",
    "task_state_commit_boundary_review_v1.json",
    "failure_escalation_response_dryrun_review_v1.json",
    "task_response_candidate_boundary_audit_v1.json",
    "task_response_candidate_blocked_path_result_v1.json",
    "task_response_candidate_closure_decision_v1.json",
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
            "midplatform_task_response_candidate_integration_dryrun_and_review"
        ),
    )
    p.add_argument(
        "--planning-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "midplatform_task_response_candidate_integration_planning"
        ),
    )
    args = p.parse_args()
    root = Path(args.output_root)
    plan_root = Path(args.planning_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in REQUIRED:
        ok(f"file.{f}", (root / f).is_file())

    plan_vr = _load(plan_root / "verifier_report.json")
    plan_sm = _load(plan_root / "summary.json")

    summary = _load(root / "summary.json")
    policy = _load(root / "task_response_candidate_integration_dryrun_review_policy_v1.json")
    input_review = _load(root / "task_response_candidate_planning_input_review_v1.json")
    model = _load(root / "task_response_integration_model_candidate_v1.json")
    sample_decision = _load(root / "sample_decision_candidate_intake_v1.json")
    sample_task = _load(root / "sample_task_response_candidate_v1.json")
    mapping = _load(root / "response_action_mapping_dryrun_review_v1.json")
    preservation = _load(root / "uncertainty_evidence_preservation_review_v1.json")
    safety = _load(root / "safety_constitution_output_boundary_review_v1.json")
    speech = _load(root / "speech_output_boundary_review_v1.json")
    memory = _load(root / "memory_worldmodel_write_boundary_review_v1.json")
    task_state = _load(root / "task_state_commit_boundary_review_v1.json")
    failure = _load(root / "failure_escalation_response_dryrun_review_v1.json")
    boundary = _load(root / "task_response_candidate_boundary_audit_v1.json")
    blocked = _load(root / "task_response_candidate_blocked_path_result_v1.json")
    closure = _load(root / "task_response_candidate_closure_decision_v1.json")
    next_route = _load(root / "next_route_readiness_decision_v1.json")
    non_claims = _load(root / "non_claims_register_v1.json")

    ok("upstream.planning_go", plan_vr.get("verifier") == "GO")
    ok("upstream.planning_final", plan_sm.get("final_decision") == UPSTREAM_PLANNING_FINAL)
    ok("upstream.planning_next", plan_sm.get("recommended_next_phase") == UPSTREAM_PLANNING_NEXT)

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("scope") == SCOPE)
    ok("summary.dryrun_only", summary.get("task_response_candidate_integration_dryrun_and_review_only") is True)
    ok("summary.simulated", summary.get("simulated") is True)
    ok("summary.pass", summary.get("dryrun_and_review_pass") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)

    for field in BOUNDARY_TRUE:
        ok(f"true.{field}", summary.get(field) is True)
    for field in BOUNDARY_FALSE:
        ok(f"false.{field}", summary.get(field) is False)

    ok("policy.phase", policy.get("phase") == PHASE_ID)
    ok("policy.dryrun_not_runtime", policy.get("dryrun_not_runtime") is True)
    ok("policy.assembly_not_user", policy.get("assembly_not_user_output") is True)

    ok("input.review_pass", input_review.get("review_pass") is True)
    ok("input.decision_not_task", input_review.get("decision_not_task_response") is True)
    ok("input.task_not_user", input_review.get("task_response_not_user_output") is True)
    ok("input.mapping13", input_review.get("action_mapping_count") == 13)

    ok("model.module_id", model.get("module_id") == "midplatform_task_response_candidate_integration_v1")
    ok("model.type", model.get("module_type") == "midplatform_response_assembly_module")
    ok("model.role", model.get("role") == "decision_candidate_to_task_response_candidate_assembly")
    ok("model.layer", model.get("system_layer") == "Assembly")
    ok("model.runtime_off", model.get("runtime_enabled_now") is False)
    ok("model.consumes_dc", model.get("consumes_decision_candidate") is True)
    ok("model.emits_task", model.get("emits_task_response_candidate") is True)
    ok("model.no_user", model.get("emits_user_output_candidate") is False)
    ok("model.no_speech_gate", model.get("speech_gate_invocation_allowed") is False)
    ok("model.no_tts", model.get("tts_invocation_allowed") is False)
    ok("model.no_memory", model.get("memory_write_allowed") is False)
    ok("model.no_wm", model.get("world_model_write_allowed") is False)
    ok("model.no_task_state", model.get("task_state_commit_allowed") is False)
    ok("model.no_provider", model.get("provider_invocation_allowed") is False)
    ok("model.upstream_dc", "midplatform_decision_center_v1" in (model.get("upstream_modules") or []))
    ok("model.upstream_flow", "midplatform_candidate_evidence_flow_integration_v1" in (model.get("upstream_modules") or []))
    ok("model.downstream_output", "output_plane_later" in (model.get("downstream_modules") or []))

    for field in DECISION_CANDIDATE_INTAKE_FIELDS:
        ok(f"decision.{field[:18]}", field in sample_decision)
    ok("decision.candidate_only", sample_decision.get("candidate_only") is True)

    for field in TASK_RESPONSE_OUTPUT_FIELDS:
        ok(f"task.{field[:18]}", field in sample_task)
    ok("task.candidate_only", sample_task.get("candidate_only") is True)
    ok("task.no_user", sample_task.get("user_output_allowed") is False)
    ok("task.no_speech", sample_task.get("speech_output_allowed") is False)
    ok("task.no_memory", sample_task.get("memory_write_allowed") is False)
    ok("task.no_wm", sample_task.get("world_model_write_allowed") is False)
    ok("task.no_commit", sample_task.get("task_state_commit_allowed") is False)
    ok("task.not_fact", sample_task.get("fact_status") == "not_fact")
    ok(
        "task.source_ref",
        sample_task.get("source_decision_candidate_ref") == sample_decision.get("decision_candidate_id"),
    )

    ok("mapping.pass", mapping.get("dryrun_and_review_pass") is True)
    ok("mapping.count13", mapping.get("mapping_count") == 13)
    ok("mapping.all13", mapping.get("all_thirteen_actions_covered") is True)
    ok("mapping.no_exec", mapping.get("mapping_does_not_execute_action") is True)
    for m in ACTION_MAPPING_DRYRUN:
        ok(
            f"map.{m['selected_action'][:18]}",
            any(
                x.get("selected_action") == m["selected_action"]
                and x.get("response_assembly") == m["response_assembly"]
                for x in (mapping.get("mappings") or [])
            ),
        )
    for m in mapping.get("mappings") or []:
        ok(f"map.sim.{m.get('selected_action','')[:12]}", m.get("executes_action") is False)

    ok("preserve.pass", preservation.get("dryrun_and_review_pass") is True)
    ok("preserve.refs", preservation.get("sample_refs_preserved") is True)
    ok(
        "preserve.uncertainty",
        sample_task.get("uncertainty_level") == sample_decision.get("uncertainty_level"),
    )
    ok("preserve.evidence", sample_task.get("evidence_refs") == sample_decision.get("evidence_refs"))
    ok("preserve.validation", sample_task.get("validation_refs") == sample_decision.get("validation_refs"))
    ok("preserve.health", sample_task.get("health_refs") == sample_decision.get("health_refs"))
    ok("preserve.constitution", sample_task.get("constitution_refs") == sample_decision.get("constitution_refs"))
    ok("preserve.whitebox", sample_task.get("whitebox_refs") == sample_decision.get("whitebox_refs"))
    ok("preserve.rationale", sample_task.get("rationale_refs") == sample_decision.get("rationale_refs"))

    ok("safety.pass", safety.get("dryrun_and_review_pass") is True)
    ok("safety.constitution_later", safety.get("task_response_requires_output_constitution_later") is True)
    ok("safety.output_plane_later", safety.get("user_output_requires_output_plane_later") is True)

    ok("speech.pass", speech.get("dryrun_and_review_pass") is True)
    ok("speech.not_speech", speech.get("task_response_candidate_is_not_speech") is True)

    ok("memory.pass", memory.get("dryrun_and_review_pass") is True)
    ok("memory.no_admission", memory.get("no_fact_admission_here") is True)

    ok("task_state.pass", task_state.get("dryrun_and_review_pass") is True)
    ok("task_state.no_commit", task_state.get("task_response_does_not_commit_task_state") is True)

    ok("failure.pass", failure.get("dryrun_and_review_pass") is True)
    for route in FAILURE_ESCALATION_RESPONSES:
        ok(
            f"fail.{route['trigger'][:14]}",
            any(
                r.get("trigger") == route["trigger"] and r.get("response") == route["response"]
                for r in (failure.get("routes") or [])
            ),
        )

    ok("audit.pass", boundary.get("dryrun_and_review_pass") is True)
    ok("audit.forbidden", boundary.get("forbidden_actions_absent") is True)

    ok("blocked.all", blocked.get("all_blocked") is True)
    ok("blocked.count13", blocked.get("blocked_count") == len(BLOCKED_PATHS))
    for bp in BLOCKED_PATHS:
        ok(
            f"blocked.{bp[:22]}",
            any(
                x.get("blocked_path") == bp and x.get("blocked") is True
                for x in (blocked.get("blocked_paths") or [])
            ),
        )

    ok("closure.pass", closure.get("dryrun_and_review_pass") is True)
    ok("closure.final", closure.get("final_decision") == FINAL_DECISION_GO)
    ok("closure.next", closure.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("closure.chain", len(closure.get("main_chain_closed") or []) == 4)

    ok("next.ready", next_route.get("ready_for_output_plane_integration_planning") is True)
    ok("next.no_runtime", next_route.get("task_response_runtime_enabled") is False)
    ok("next.no_user", next_route.get("user_output_still_forbidden") is True)
    ok("next.phase", next_route.get("recommended_next_phase") == NEXT_PHASE_GO)

    ok("non_claims.count", len(non_claims.get("non_claims") or []) >= len(NON_CLAIMS))
    for claim in NON_CLAIMS:
        ok(f"claim.{claim[:20]}", claim in (non_claims.get("non_claims") or []))

    passed = sum(1 for c in checks if c["passed"])
    total = len(checks)
    pass_all = summary.get("dryrun_and_review_pass") is True
    go = passed >= MIN_CHECKS and pass_all and passed == total

    report = {
        "phase": PHASE_ID,
        "verifier": "GO" if go else "NO_GO",
        "checks_passed": passed,
        "checks_total": total,
        "min_checks_required": MIN_CHECKS,
        "dryrun_and_review_pass": pass_all,
        "final_decision": summary.get("final_decision"),
        "recommended_next_phase": summary.get("recommended_next_phase"),
        "checks": checks,
    }
    (root / "verifier_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {"verifier": report["verifier"], "checks_passed": passed, "checks_total": total},
            ensure_ascii=False,
        )
    )
    return 0 if go else 1


if __name__ == "__main__":
    raise SystemExit(main())
