#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Luna Midplatform Task Manager Foundation Handoff Planning v1."""

from __future__ import annotations

import json
import sys
from argparse import ArgumentParser
from pathlib import Path
from typing import Any, Dict, List, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.midplatform.midplatform_task_manager_controlled_skeleton_implementation_dryrun_v1 import (
    FINAL_DECISION_GO as DRYRUN_FINAL_GO,
    SKELETON_FILES,
)
from capabilities.midplatform.midplatform_task_manager_controlled_skeleton_implementation_post_dryrun_review_v1 import (
    FINAL_DECISION_GO as POST_DRYRUN_FINAL_GO,
)
from capabilities.midplatform.task_manager_foundation_handoff_planning_v1 import (
    BOUNDARY_STATEMENT_EN,
    BOUNDARY_STATEMENT_ZH,
    CANDIDATE_SEMANTICS,
    DEFAULT_DRYRUN_ROOT,
    DEFAULT_OUTPUT,
    DEFAULT_POST_DRYRUN_ROOT,
    DOWNSTREAM_READINESS,
    FINAL_DECISION_GO,
    FOUNDATION_ID,
    NEXT_PHASE_GO,
    NON_EXECUTION_CONSTRAINTS,
    PHASE_ID,
    SCOPE,
)

MIN_CHECKS = 420
REQUIRED_ARTIFACTS: Tuple[str, ...] = (
    "task_manager_foundation_handoff_plan_v1.json",
    "task_manager_foundation_handoff_plan_v1.md",
    "task_manager_foundation_boundary_matrix_v1.json",
    "task_manager_candidate_lifecycle_matrix_v1.json",
    "task_manager_downstream_readiness_matrix_v1.json",
    "task_manager_non_execution_constraints_v1.json",
    "summary.json",
)
FORBIDDEN_CLAIMS: Tuple[str, ...] = (
    "runtime_executor_created_now",
    "scheduler_binding_created_now",
    "task_execution_authority_granted_now",
    "output_authorization_granted_now",
    "module_adapter_integration_created_now",
    "information_channel_governance_implemented_now",
    "protocol_governance_implemented_now",
)
BOUNDARY_FALSE_FLAGS: Tuple[str, ...] = (
    "task_manager_runtime_enabled_now",
    "task_manager_mounted_now",
    "task_execution_now",
    "tool_call_now",
    "model_invoked_now",
    "provider_invoked_now",
    "runtime_enabled_now",
    "memory_write_allowed_now",
    "worldmodel_write_allowed_now",
    "user_output_allowed_now",
    "output_gate_mounted_now",
    "module_adapter_mounted_now",
    "health_watchdog_runtime_enabled_now",
    "decision_center_runtime_enabled_now",
    "real_event_bus_enabled_now",
    "real_working_memory_enabled_now",
    "real_scheduler_enabled_now",
)


def _read(path: Path) -> Dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return {}
    return payload if isinstance(payload, dict) else {}


def _add(checks: List[Dict[str, Any]], check_id: str, passed: bool, detail: str = "") -> None:
    checks.append({"check_id": check_id, "passed": bool(passed), "detail": detail})


def main() -> int:
    parser = ArgumentParser()
    parser.add_argument("--output-root", default=DEFAULT_OUTPUT)
    parser.add_argument("--dryrun-root", default=DEFAULT_DRYRUN_ROOT)
    parser.add_argument("--post-dryrun-root", default=DEFAULT_POST_DRYRUN_ROOT)
    args = parser.parse_args()
    root = Path(args.output_root)
    dryrun = Path(args.dryrun_root)
    post = Path(args.post_dryrun_root)
    checks: List[Dict[str, Any]] = []

    docs = {fname: _read(root / fname) for fname in REQUIRED_ARTIFACTS if fname.endswith(".json")}
    md_path = root / "task_manager_foundation_handoff_plan_v1.md"
    md = md_path.read_text(encoding="utf-8") if md_path.is_file() else ""
    for fname in REQUIRED_ARTIFACTS:
        _add(checks, f"artifact.exists.{fname}", (root / fname).is_file())

    dryrun_summary = _read(dryrun / "summary.json")
    dryrun_verifier = _read(dryrun / "verifier_report.json")
    post_summary = _read(post / "summary.json")
    post_verifier = _read(post / "verifier_report.json")

    summary = docs["summary.json"]
    _add(checks, "downstream.readiness.dryrun_root_recorded", bool(summary.get("downstream_readiness_refs", {}).get("upstream_dryrun_root")))
    _add(checks, "downstream.readiness.post_root_recorded", bool(summary.get("downstream_readiness_refs", {}).get("upstream_post_dryrun_root")))
    _add(checks, "downstream.readiness.gaps_declared", isinstance(summary.get("downstream_readiness_gaps"), list))
    _add(checks, "downstream.readiness.dryrun_status_readable", bool(dryrun_summary.get("final_decision")))
    _add(checks, "downstream.readiness.post_status_readable", bool(post_summary.get("final_decision")))

    plan = docs["task_manager_foundation_handoff_plan_v1.json"]
    boundary = docs["task_manager_foundation_boundary_matrix_v1.json"]
    lifecycle = docs["task_manager_candidate_lifecycle_matrix_v1.json"]
    downstream = docs["task_manager_downstream_readiness_matrix_v1.json"]
    constraints = docs["task_manager_non_execution_constraints_v1.json"]

    _add(checks, "summary.candidate_only", summary.get("candidate_only") is True)
    _add(checks, "summary.planning_complete", summary.get("task_manager_foundation_handoff_planning_complete") is True)

    for doc_name, doc in docs.items():
        _add(checks, f"meta.phase.{doc_name}", doc.get("phase") == PHASE_ID)
        _add(checks, f"meta.scope.{doc_name}", doc.get("scope") == SCOPE)
        _add(checks, f"meta.foundation.{doc_name}", doc.get("foundation_id") == FOUNDATION_ID)
        _add(checks, f"meta.runtime.{doc_name}", doc.get("runtime_status") == "not_enabled")
        _add(checks, f"meta.planning_only.{doc_name}", doc.get("foundation_handoff_planning_only") is True)
        _add(checks, f"meta.statement_en.{doc_name}", doc.get("boundary_statement_en") == BOUNDARY_STATEMENT_EN)
        _add(checks, f"meta.statement_zh.{doc_name}", doc.get("boundary_statement_zh") == BOUNDARY_STATEMENT_ZH)

    _add(checks, "summary.pass", summary.get("planning_pass") is True)
    _add(checks, "summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    _add(checks, "summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    _add(checks, "summary.blocker0", summary.get("blocker_count") == 0)
    _add(checks, "summary.non_execution_ok", summary.get("non_execution_boundary_ok") is True)
    _add(checks, "summary.candidate_semantics", summary.get("candidate_semantics_preserved") is True)
    _add(checks, "summary.planning_only", summary.get("foundation_handoff_planning_only") is True)
    _add(checks, "summary.downstream_scope", summary.get("downstream_readiness_scope_ok") is True)
    _add(checks, "md.statement_en", BOUNDARY_STATEMENT_EN in md)
    _add(checks, "md.statement_zh", BOUNDARY_STATEMENT_ZH in md)
    _add(checks, "md.not_empty", len(md.strip()) > 200)

    evidence = plan.get("handoff_evidence_map") or {}
    files = evidence.get("core_skeleton_files") or []
    for rel in SKELETON_FILES:
        _add(checks, f"core.file.exists.{rel}", (REPO_ROOT / rel).is_file())
        entry = next((item for item in files if item.get("path") == rel), {})
        _add(checks, f"evidence.core.{rel}", entry.get("exists") is True and entry.get("role") == "core_skeleton_evidence")
    for key in ("dryrun_summary", "dryrun_verifier", "post_dryrun_summary", "post_dryrun_verifier"):
        entry = evidence.get(key) or {}
        _add(checks, f"evidence.{key}.path_recorded", bool(entry.get("path")))
        _add(checks, f"evidence.{key}.declared", "referenced" in entry)

    stable = plan.get("stable_objects") or {}
    for type_name in ("TaskCandidate", "TaskReadinessCandidate", "TaskBlockCandidate", "TaskPlanCandidate", "TaskStepCandidate", "TaskHandoffCandidate"):
        _add(checks, f"stable.type.{type_name}", type_name in (stable.get("types_boundary") or []))
    for function_name in ("validate_task_manager_input", "classify_task_readiness", "build_task_candidate", "build_task_plan_candidate", "build_task_step_candidate", "build_task_handoff_candidate"):
        _add(checks, f"stable.function.{function_name}", function_name in (stable.get("manager_skeleton_boundary") or []))
    for validator_name in ("validate_tm_task_not_execution", "validate_tm_step_not_executed", "validate_tm_handoff_not_direct_mount"):
        _add(checks, f"stable.validator.{validator_name}", validator_name in (stable.get("static_validator_boundary") or []))
    for function_name in (
        "validate_task_manager_input",
        "classify_task_readiness",
        "evaluate_health_gate_block_candidate",
        "evaluate_required_observation_candidate",
        "evaluate_governance_task_candidate",
        "build_task_candidate",
        "build_task_plan_candidate",
        "build_task_step_candidate",
        "build_task_handoff_candidate",
        "validate_task_manager_candidate",
    ):
        _add(checks, f"stable.all_functions.{function_name}", function_name in (stable.get("manager_skeleton_boundary") or []))
    for validator_name in (
        "validate_tm_input_contract",
        "validate_tm_output_candidate_only",
        "validate_tm_task_not_execution",
        "validate_tm_step_not_executed",
        "validate_tm_handoff_not_direct_mount",
        "validate_tm_no_tool_call",
        "validate_tm_no_user_output",
        "validate_tm_no_memory_worldmodel_write",
        "validate_tm_governance_required_for_high_risk_task",
        "validate_tm_no_health_watchdog_redefinition",
        "validate_tm_no_decision_center_redefinition",
        "validate_tm_boundary_matrix",
    ):
        _add(checks, f"stable.all_validators.{validator_name}", validator_name in (stable.get("static_validator_boundary") or []))
    for field in (
        "candidate_id",
        "trace_ref",
        "source_chain",
        "fact_status",
        "governance_ref",
        "health_gate_refs",
        "blocker_refs",
        "direct_mount",
        "task_execution",
        "executed_step",
        "user_output",
    ):
        _add(checks, f"plan.l1_channel_input.{field}", field in (plan.get("l1_information_channel_inputs") or []))
    for phrase in (
        "module_adapter may consume task_handoff_candidate only as planning-ready input",
        "module_adapter must not treat task_handoff_candidate as direct mount",
        "module_adapter must not execute task_step_candidate",
    ):
        _add(checks, f"plan.module_adapter_constraint.{phrase[:40]}", phrase in (plan.get("module_adapter_constraints") or []))
    for expected in (
        "evidence_map_complete",
        "candidate_semantics_preserved",
        "boundary_matrix_frozen",
        "downstream_readiness_planning_only",
        "no_runtime_scope_leakage",
        "no_information_channel_governance_implementation",
        "no_protocol_governance_implementation",
    ):
        _add(checks, f"plan.next_handoff_dryrun.{expected}", expected in (plan.get("next_handoff_dryrun_must_verify") or []))
    for constraint in NON_EXECUTION_CONSTRAINTS:
        _add(checks, f"plan.unauthorized.{constraint}", constraint in (plan.get("unauthorized_capabilities") or []))

    lifecycle_items = lifecycle.get("candidate_semantics") or []
    for semantic in CANDIDATE_SEMANTICS:
        item = next((row for row in lifecycle_items if row.get("payload_type") == semantic["payload_type"]), {})
        _add(checks, f"candidate.semantic.exists.{semantic['payload_type']}", bool(item))
        _add(checks, f"candidate.semantic.boundary.{semantic['payload_type']}", item.get("boundary") == semantic["boundary"])
        _add(checks, f"candidate.semantic.not_fact.{semantic['payload_type']}", item.get("fact_status") == "not_fact")
        _add(checks, f"candidate.semantic.action_false.{semantic['payload_type']}", item.get("action_allowed") is False)
    _add(checks, "candidate.task_execution_false", any(row.get("payload_type") == "task_candidate" and row.get("task_execution") is False for row in lifecycle_items))
    _add(checks, "candidate.step_executed_false", any(row.get("payload_type") == "task_step_candidate" and row.get("executed_step") is False for row in lifecycle_items))
    _add(checks, "candidate.handoff_direct_mount_false", any(row.get("payload_type") == "task_handoff_candidate" and row.get("direct_mount") is False for row in lifecycle_items))
    _add(checks, "candidate.lifecycle_preserved", lifecycle.get("candidate_semantics_preserved") is True)

    global_b = boundary.get("global_boundaries") or {}
    _add(checks, "boundary.files_created", global_b.get("task_manager_files_created_now") is True)
    for flag in BOUNDARY_FALSE_FLAGS:
        _add(checks, f"boundary.false.{flag}", global_b.get(flag) is False)
    for flag in FORBIDDEN_CLAIMS:
        _add(checks, f"boundary.no_claim.{flag}", global_b.get(flag) is False)
    _add(checks, "boundary.non_execution_ok", boundary.get("non_execution_boundary_ok") is True)

    downstream_rows = downstream.get("downstream") or []
    for expected in DOWNSTREAM_READINESS:
        row = next((item for item in downstream_rows if item.get("consumer") == expected["consumer"]), {})
        _add(checks, f"downstream.exists.{expected['consumer']}", bool(row))
        _add(checks, f"downstream.readiness.{expected['consumer']}", row.get("readiness") == expected["readiness"])
        _add(checks, f"downstream.impl_false.{expected['consumer']}", row.get("implementation_ready") == "false")
    _add(checks, "downstream.scope_ok", downstream.get("downstream_readiness_scope_ok") is True)
    _add(checks, "future.icg.only", any(row.get("consumer") == "information_channel_governance" and row.get("readiness") == "future_l1_protocol_input" for row in downstream_rows))
    _add(checks, "future.protocol.only", any(row.get("consumer") == "protocol_governance" and row.get("readiness") == "future_l1_protocol_dependency" for row in downstream_rows))

    for constraint in NON_EXECUTION_CONSTRAINTS:
        _add(checks, f"constraint.exists.{constraint}", constraint in (constraints.get("constraints") or []))
    for key in ("no_runtime_executor", "no_scheduler_binding", "no_output_authorization", "no_memory_worldmodel_write_path", "no_module_adapter_integration", "no_authorization_claim", "no_success_claim_beyond_planning"):
        _add(checks, f"constraint.{key}", constraints.get(key) is True)

    # Cross-document sweeps ensure every planning artifact carries the same non-runtime posture.
    for doc_name, doc in docs.items():
        _add(checks, f"sweep.task_execution_false.{doc_name}", doc.get("task_execution_now") is False)
        _add(checks, f"sweep.tool_false.{doc_name}", doc.get("tool_call_now") is False)
        _add(checks, f"sweep.output_false.{doc_name}", doc.get("user_output_allowed_now") is False)
        _add(checks, f"sweep.memory_false.{doc_name}", doc.get("memory_write_allowed_now") is False)
        _add(checks, f"sweep.worldmodel_false.{doc_name}", doc.get("worldmodel_write_allowed_now") is False)
        _add(checks, f"sweep.output_gate_false.{doc_name}", doc.get("output_gate_mounted_now") is False)
        _add(checks, f"sweep.module_adapter_false.{doc_name}", doc.get("module_adapter_mounted_now") is False)
        _add(checks, f"sweep.runtime_false.{doc_name}", doc.get("runtime_enabled_now") is False)
        _add(checks, f"sweep.model_false.{doc_name}", doc.get("model_invoked_now") is False)
        _add(checks, f"sweep.provider_false.{doc_name}", doc.get("provider_invoked_now") is False)
        _add(checks, f"sweep.planning_only.{doc_name}", doc.get("foundation_handoff_planning_only") is True)
        _add(checks, f"sweep.no_authorization_word_claim.{doc_name}", doc.get("output_authorization_granted_now") is not True)
        for flag in BOUNDARY_FALSE_FLAGS:
            _add(checks, f"sweep.full_boundary_false.{doc_name}.{flag}", doc.get(flag) is False)
        for flag in FORBIDDEN_CLAIMS:
            _add(checks, f"sweep.forbidden_claim_false.{doc_name}.{flag}", doc.get(flag) is not True)

    passed = sum(1 for check in checks if check["passed"])
    failed = [check for check in checks if not check["passed"]]
    verifier = "GO" if not failed and passed >= MIN_CHECKS else "HOLD"
    report = {
        "verifier": verifier,
        "phase": PHASE_ID,
        "passed_checks": passed,
        "failed_checks": len(failed),
        "min_checks": MIN_CHECKS,
        "blocker_count": len(failed),
        "non_execution_boundary_ok": summary.get("non_execution_boundary_ok") is True,
        "candidate_semantics_preserved": summary.get("candidate_semantics_preserved") is True,
        "foundation_handoff_planning_only": summary.get("foundation_handoff_planning_only") is True,
        "downstream_readiness_scope_ok": summary.get("downstream_readiness_scope_ok") is True,
        "final_decision": summary.get("final_decision") if verifier == "GO" else "HOLD",
        "recommended_next_phase": summary.get("recommended_next_phase") if verifier == "GO" else PHASE_ID,
        "failed": failed[:60],
        "checks": checks,
    }
    (root / "verifier_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "verifier": report["verifier"],
                "passed_checks": report["passed_checks"],
                "failed_checks": report["failed_checks"],
                "blocker_count": report["blocker_count"],
                "non_execution_boundary_ok": report["non_execution_boundary_ok"],
                "candidate_semantics_preserved": report["candidate_semantics_preserved"],
                "foundation_handoff_planning_only": report["foundation_handoff_planning_only"],
                "downstream_readiness_scope_ok": report["downstream_readiness_scope_ok"],
                "final_decision": report["final_decision"],
                "recommended_next_phase": report["recommended_next_phase"],
            },
            ensure_ascii=False,
        )
    )
    return 0 if verifier == "GO" else 1


if __name__ == "__main__":
    raise SystemExit(main())
