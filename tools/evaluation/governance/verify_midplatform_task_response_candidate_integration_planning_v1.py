#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Midplatform Task Response Candidate Integration Planning v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.midplatform_candidate_evidence_flow_integration_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as FLOW_DR_FINAL,
    NEXT_PHASE_GO as FLOW_DR_NEXT,
)
from capabilities.governance.midplatform_decision_center_module_planning_v1 import (
    DECISION_ACTIONS,
)
from capabilities.governance.midplatform_module_definition_template_v1 import (
    TEMPLATE_ID,
    TEMPLATE_SECTIONS,
    validate_module_definition,
)
from capabilities.governance.midplatform_task_response_candidate_integration_planning_v1 import (
    BOUNDARY_FALSE,
    BOUNDARY_MATRIX_FALSE,
    BOUNDARY_TRUE,
    CORE_CHAIN_BOUNDARY,
    DECISION_CANDIDATE_INTAKE_FIELDS,
    FAILURE_ESCALATION_RESPONSES,
    FINAL_DECISION_GO,
    NEXT_PHASE_GO,
    NON_CLAIMS,
    PHASE_ID,
    RESPONSE_ASSEMBLY_MAPPINGS,
    SCOPE,
    TASK_RESPONSE_OUTPUT_FIELDS,
)

MIN_CHECKS = 179

REQUIRED = (
    "task_response_candidate_integration_planning_policy_v1.json",
    "upstream_candidate_evidence_flow_input_review_v1.json",
    "task_response_candidate_module_definition_v1.json",
    "decision_candidate_intake_contract_v1.json",
    "task_response_candidate_output_contract_v1.json",
    "response_assembly_rule_plan_v1.json",
    "response_action_mapping_plan_v1.json",
    "uncertainty_and_evidence_preservation_plan_v1.json",
    "safety_and_constitution_output_boundary_plan_v1.json",
    "speech_output_boundary_plan_v1.json",
    "memory_worldmodel_write_boundary_plan_v1.json",
    "task_state_commit_boundary_plan_v1.json",
    "failure_and_escalation_response_plan_v1.json",
    "task_response_candidate_boundary_matrix_v1.json",
    "task_response_candidate_dryrun_plan_v1.json",
    "non_claims_register_v1.json",
    "task_response_candidate_integration_planning_decision_v1.json",
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
            "midplatform_task_response_candidate_integration_planning"
        ),
    )
    p.add_argument(
        "--flow-dryrun-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "midplatform_candidate_evidence_flow_integration_dryrun_and_review"
        ),
    )
    args = p.parse_args()
    root = Path(args.output_root)
    flow_root = Path(args.flow_dryrun_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in REQUIRED:
        ok(f"file.{f}", (root / f).is_file())

    flow_vr = _load(flow_root / "verifier_report.json")
    flow_sm = _load(flow_root / "summary.json")

    summary = _load(root / "summary.json")
    policy = _load(root / "task_response_candidate_integration_planning_policy_v1.json")
    flow_review = _load(root / "upstream_candidate_evidence_flow_input_review_v1.json")
    module_def = _load(root / "task_response_candidate_module_definition_v1.json")
    intake = _load(root / "decision_candidate_intake_contract_v1.json")
    output = _load(root / "task_response_candidate_output_contract_v1.json")
    assembly = _load(root / "response_assembly_rule_plan_v1.json")
    action_map = _load(root / "response_action_mapping_plan_v1.json")
    preservation = _load(root / "uncertainty_and_evidence_preservation_plan_v1.json")
    safety = _load(root / "safety_and_constitution_output_boundary_plan_v1.json")
    speech = _load(root / "speech_output_boundary_plan_v1.json")
    memory_wm = _load(root / "memory_worldmodel_write_boundary_plan_v1.json")
    task_state = _load(root / "task_state_commit_boundary_plan_v1.json")
    failure = _load(root / "failure_and_escalation_response_plan_v1.json")
    boundary = _load(root / "task_response_candidate_boundary_matrix_v1.json")
    dryrun = _load(root / "task_response_candidate_dryrun_plan_v1.json")
    decision = _load(root / "task_response_candidate_integration_planning_decision_v1.json")

    ok("upstream.flow_go", flow_vr.get("verifier") == "GO")
    ok("upstream.flow_final", flow_sm.get("final_decision") == FLOW_DR_FINAL)
    ok("upstream.flow_next", flow_sm.get("recommended_next_phase") == FLOW_DR_NEXT)

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("scope") == SCOPE)
    ok("summary.planning_only", summary.get("task_response_candidate_integration_planning_only") is True)
    ok("summary.pass", summary.get("planning_pass") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("summary.boundary", summary.get("core_chain_boundary") == CORE_CHAIN_BOUNDARY)

    for field in BOUNDARY_TRUE:
        ok(f"true.{field}", summary.get(field) is True)
    for field in BOUNDARY_FALSE:
        ok(f"false.{field}", summary.get(field) is False)

    ok("policy.assembly", policy.get("assembly_not_user_output") is True)

    ok("flow_review.pass", flow_review.get("review_pass") is True)
    ok("flow_review.not_task", flow_review.get("decision_candidate_not_task_response") is True)
    ok("flow_review.not_user", flow_review.get("task_response_not_user_output") is True)

    identity = module_def.get("module_identity") or {}
    processing = module_def.get("processing_scope") or {}
    valid, issues = validate_module_definition(module_def)
    ok("module.valid", valid and len(issues) == 0)
    ok("module.id", identity.get("module_id") == "midplatform_task_response_candidate_integration_v1")
    ok("module.type", identity.get("module_type") == "midplatform_response_assembly_module")
    ok("module.layer", identity.get("system_layer") == "Assembly")
    ok("module.no_arbitrate", processing.get("arbitration_allowed") is False)
    ok("module.no_write", processing.get("write_allowed") is False)

    for section in TEMPLATE_SECTIONS:
        ok(f"section.{section[:12]}", section in module_def)

    ok("intake.fields18", len(intake.get("required_fields") or []) == 18)
    for field in DECISION_CANDIDATE_INTAKE_FIELDS:
        ok(f"intake.{field[:15]}", field in (intake.get("required_fields") or []))

    ok("output.fields20", len(output.get("required_fields") or []) == 20)
    defaults = output.get("defaults") or {}
    ok("output.no_user", defaults.get("user_output_allowed") is False)
    ok("output.no_speech", defaults.get("speech_output_allowed") is False)
    ok("output.no_memory", defaults.get("memory_write_allowed") is False)
    ok("output.no_wm", defaults.get("world_model_write_allowed") is False)
    ok("output.no_task", defaults.get("task_state_commit_allowed") is False)
    ok("output.not_fact", defaults.get("fact_status") == "not_fact")
    for field in TASK_RESPONSE_OUTPUT_FIELDS:
        ok(f"output.{field[:15]}", field in (output.get("required_fields") or []))

    ok("assembly.count13", assembly.get("mapping_count") == 13)
    for m in RESPONSE_ASSEMBLY_MAPPINGS:
        ok(f"assembly.{m['selected_action'][:15]}", any(
            x.get("selected_action") == m["selected_action"]
            for x in (assembly.get("mappings") or [])
        ))
    for action in DECISION_ACTIONS:
        ok(f"action_mapped.{action[:15]}", any(
            x.get("selected_action") == action for x in (assembly.get("mappings") or [])
        ))

    ok("action_map.no_exec", action_map.get("action_mapping_does_not_execute_action") is True)
    ok("action_map.candidate", action_map.get("response_assembly_candidate_only") is True)
    ok("action_map.no_hive", action_map.get("escalation_does_not_submit_hive_now") is True)

    ok("preserve.uncertainty", preservation.get("uncertainty_level_preserved") is True)
    ok("preserve.chain", preservation.get("source_chain_preserved") is True)
    ok("preserve.no_mutate", preservation.get("no_evidence_mutation") is True)

    ok("safety.output_plane", safety.get("user_output_requires_output_plane_later") is True)
    ok("safety.speech_gate", safety.get("speech_requires_speech_gate_voice_plane_later") is True)

    ok("speech.not_speech", speech.get("task_response_candidate_is_not_speech") is True)
    ok("speech.no_tts", speech.get("tts_invoked_now") is False)
    ok("speech.no_gate", speech.get("speech_gate_invoked_now") is False)

    ok("memory.no_write", memory_wm.get("no_memory_write") is True)
    ok("memory.no_wm", memory_wm.get("no_world_model_write") is True)
    ok("memory.not_fact", memory_wm.get("fact_status_remains_not_fact") is True)

    ok("task_state.no_commit", task_state.get("task_response_does_not_commit_task_state") is True)
    ok("task_state.false", task_state.get("task_state_commit_allowed") is False)

    ok("failure.count8", len(failure.get("routes") or []) == 8)
    for route in FAILURE_ESCALATION_RESPONSES:
        ok(f"fail.{route['trigger'][:12]}", any(
            x.get("trigger") == route["trigger"] for x in (failure.get("routes") or [])
        ))

    ok("boundary.all_false", boundary.get("all_runtime_actions_false") is True)
    for field in BOUNDARY_MATRIX_FALSE:
        ok(f"matrix.{field[:15]}", boundary.get("matrix", {}).get(field) is False)

    ok("dryrun.next", dryrun.get("next_phase") == NEXT_PHASE_GO)

    ok("decision.pass", decision.get("planning_pass") is True)
    ok("decision.final", decision.get("final_decision") == FINAL_DECISION_GO)
    ok("decision.chain4", len(decision.get("main_chain_defined") or []) == 4)

    ok("template_id", summary.get("template_id") == TEMPLATE_ID)
    ok("non_claims", len(_load(root / "non_claims_register_v1.json").get("non_claims") or []) >= len(NON_CLAIMS))

    passed = sum(1 for c in checks if c["passed"])
    total = len(checks)
    pass_all = summary.get("planning_pass") is True
    go = passed >= MIN_CHECKS and pass_all and passed == total

    report = {
        "phase": PHASE_ID,
        "verifier": "GO" if go else "NO_GO",
        "checks_passed": passed,
        "checks_total": total,
        "min_checks_required": MIN_CHECKS,
        "planning_pass": pass_all,
        "final_decision": summary.get("final_decision"),
        "recommended_next_phase": summary.get("recommended_next_phase"),
        "checks": checks,
    }
    (root / "verifier_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({"verifier": report["verifier"], "checks_passed": passed, "checks_total": total}, ensure_ascii=False))
    return 0 if go else 1


if __name__ == "__main__":
    raise SystemExit(main())
