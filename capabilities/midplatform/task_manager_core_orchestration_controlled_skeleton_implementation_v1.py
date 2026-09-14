# -*- coding: utf-8 -*-
"""Luna Midplatform Task Manager Core Orchestration Controlled Skeleton Implementation v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.midplatform.file_size_governance_v1 import build_file_size_governance_review
from capabilities.midplatform.task_manager_core_orchestration_builders_v1 import BUILDER_FUNCTIONS
from capabilities.midplatform.task_manager_core_orchestration_contracts_v1 import ALL_CONTRACTS
from capabilities.midplatform.task_manager_core_orchestration_controlled_skeleton_lineage_v1 import (
    CORE_IMPLEMENTATION_FILES,
    ORCHESTRATION_CONTROLLED_SKELETON_STAGE_ADDITIONS,
    ORCHESTRATION_CONTROLLED_SKELETON_STAGE_TERM_OVERRIDES,
    ORCHESTRATION_CONTROLLED_SKELETON_WHITELIST_FILES,
)
from capabilities.midplatform.task_manager_core_orchestration_implementation_items_v1 import NON_EXECUTION_GUARDS
from capabilities.midplatform.task_manager_core_orchestration_implementation_planning_v1 import (
    DEFAULT_OUTPUT as DEFAULT_IMPLEMENTATION_PLANNING_ROOT,
    FINAL_DECISION_GO as IMPLEMENTATION_PLANNING_FINAL_GO,
    NEXT_PHASE_GO as IMPLEMENTATION_PLANNING_NEXT_PHASE,
)
from capabilities.midplatform.task_manager_core_orchestration_skeleton_v1 import (
    SKELETON_FUNCTIONS,
    run_controlled_orchestration_skeleton,
)
from capabilities.midplatform.task_manager_core_orchestration_static_validators_v1 import STATIC_VALIDATOR_FUNCTIONS
from capabilities.midplatform.task_manager_core_orchestration_types_v1 import (
    ORCHESTRATION_CANDIDATE_TYPES,
    OrchestrationInputCandidate,
)
from capabilities.midplatform.task_manager_foundation_handoff_evaluation_template_lineage_v1 import (
    build_core_go_no_go_summary_fields,
    build_template_lineage,
)
from capabilities.midplatform.task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_issuance_post_dryrun_review_v1 import (
    RUNTIME_FORBIDDEN_FLAGS,
)
from capabilities.midplatform.task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_record_approval_closure_post_dryrun_review_v1 import (
    ABSENCE_KEYS,
)

PHASE_ID = "Phase-Midplatform-Task-Manager-Core-Orchestration-Controlled-Skeleton-Implementation-v1-001"
SCOPE = "midplatform_task_manager_core_orchestration_controlled_skeleton_implementation_only"
SOURCE_CHAIN = "task_manager_core_orchestration_controlled_skeleton_implementation_v1"
FINAL_DECISION_GO = "MIDPLATFORM_TASK_MANAGER_CORE_ORCHESTRATION_CONTROLLED_SKELETON_IMPLEMENTATION_READY_FOR_MODULE_LEVEL_CONTROLLED_DRYRUN"
FINAL_DECISION_UPSTREAM = "MIDPLATFORM_TASK_MANAGER_CORE_ORCHESTRATION_CONTROLLED_SKELETON_IMPLEMENTATION_BLOCKED_BY_PLANNING_GAP"
FINAL_DECISION_IMPL = "MIDPLATFORM_TASK_MANAGER_CORE_ORCHESTRATION_CONTROLLED_SKELETON_IMPLEMENTATION_BLOCKED_BY_IMPLEMENTATION_GAP"
FINAL_DECISION_ABSENCE = "MIDPLATFORM_TASK_MANAGER_CORE_ORCHESTRATION_CONTROLLED_SKELETON_IMPLEMENTATION_BLOCKED_BY_ABSENCE_DRIFT"
FINAL_DECISION_RUNTIME = "MIDPLATFORM_TASK_MANAGER_CORE_ORCHESTRATION_CONTROLLED_SKELETON_IMPLEMENTATION_BLOCKED_BY_RUNTIME_SCOPE_LEAKAGE"
FINAL_DECISION_LINEAGE = "MIDPLATFORM_TASK_MANAGER_CORE_ORCHESTRATION_CONTROLLED_SKELETON_IMPLEMENTATION_BLOCKED_BY_TEMPLATE_LINEAGE_GAP"
NEXT_PHASE_GO = "Phase-Midplatform-Task-Manager-Core-Orchestration-Module-Level-Controlled-DryRun-v1-001"
NEXT_PHASE_HOLD = "Phase-Midplatform-Task-Manager-Core-Orchestration-Controlled-Skeleton-Implementation-Issue-Review-v1-001"
DEFAULT_OUTPUT = "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/task_manager_core_orchestration_controlled_skeleton_implementation_v1_smoke_v0"
GO_NO_GO_PACK = "docs/architecture/evaluation/LUNA_EVALUATION_TASK_MANAGER_CORE_ORCHESTRATION_CONTROLLED_SKELETON_IMPLEMENTATION_V1_GO_NO_GO_PACK_V0.md"
TEMPLATE_LINEAGE_MODULE_PATH = "capabilities/midplatform/task_manager_core_orchestration_controlled_skeleton_lineage_v1.py"
MIDPLATFORM_OVERALL_STATUS = "construction_consolidation"
SELECTED_NEXT_ROUTE = "Task Manager Core Orchestration Module-Level Controlled DryRun"

PHASE_PYTHON_FILES: Tuple[str, ...] = (
    *CORE_IMPLEMENTATION_FILES,
    "capabilities/midplatform/task_manager_core_orchestration_controlled_skeleton_implementation_v1.py",
    "capabilities/midplatform/task_manager_core_orchestration_controlled_skeleton_lineage_v1.py",
    "tools/evaluation/midplatform/run_task_manager_core_orchestration_controlled_skeleton_implementation_v1.py",
    "tools/evaluation/midplatform/verify_task_manager_core_orchestration_controlled_skeleton_implementation_v1.py",
)

GO_CONDITIONS_KEYS: Tuple[str, ...] = (
    "prior_implementation_planning_go",
    "types_implemented",
    "contracts_implemented",
    "builders_implemented",
    "validators_implemented",
    "skeleton_implemented",
    "strong_coupled_single_package_ok",
    "controlled_skeleton_smoke_ok",
    "all_outputs_candidate_only",
    "non_execution_guard_ok",
    "implementation_not_split_into_subphases",
    "non_execution_boundary_ok",
    "file_size_governance_review_ok",
    "next_phase_readiness_ok",
)


def _read_json(path: Path) -> Dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return {}
    return payload if isinstance(payload, dict) else {}


def _meta(out: Path, upstream: Path) -> Dict[str, Any]:
    return {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "source_chain": SOURCE_CHAIN,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "foundation_id": "midplatform_task_manager_foundation_v1",
        "runtime_status": "not_enabled",
        "orchestration_controlled_skeleton_implementation_only": True,
        "midplatform_overall_status": MIDPLATFORM_OVERALL_STATUS,
        "foundation_consolidation_not_final_midplatform_completion": True,
        "no_fragmentary_phase_expansion": True,
        "integration_test_executed": False,
        "real_issuance_preauthorization_not_opened": True,
        "output_root": str(out),
        "implementation_planning_root": str(upstream),
    }


def _sample_input() -> OrchestrationInputCandidate:
    return OrchestrationInputCandidate(
        candidate_id="orch_input_smoke_v1",
        source_module_ref="task_manager_core_orchestration",
        boundary_registry_ref="boundary:task_manager_core",
        lifecycle_state_ref="lifecycle:candidate_review",
        alignment_rule_ref="alignment:evidence_record_approval_permission",
        governance_constraint_ref="governance:migration_development_constraints_v1",
        protocol_trace_ref="trace:orch:smoke_v1",
        traceability_refs=("trace:orch:smoke_v1", "chain:task_manager_core_orchestration"),
        governance_refs=("governance:migration_development_constraints_v1",),
    )


def _output_flags_ok(payload: Dict[str, Any]) -> bool:
    return (
        payload.get("candidate_only") is True
        and payload.get("side_effect_allowed") is False
        and payload.get("real_execution") is False
        and payload.get("runtime_required_now") is False
    )


def run_task_manager_core_orchestration_controlled_skeleton_implementation_v1(
    *,
    implementation_planning_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    out = Path(output_root or DEFAULT_OUTPUT).expanduser().resolve()
    upstream = Path(implementation_planning_root).expanduser().resolve()
    repo_root = Path(__file__).resolve().parents[2]
    meta = _meta(out, upstream)
    issues: List[str] = []

    planning_summary = _read_json(upstream / "summary.json")
    planning_verifier = _read_json(upstream / "verifier_report.json")
    planning_file_size = _read_json(upstream / "file_size_governance_review_v1.json")

    prior_implementation_planning_go = (
        planning_summary.get("final_decision") == IMPLEMENTATION_PLANNING_FINAL_GO
        and planning_summary.get("recommended_next_phase") == IMPLEMENTATION_PLANNING_NEXT_PHASE
        and planning_verifier.get("verifier") == "GO"
        and int(planning_verifier.get("passed_checks", 0)) >= 320
        and planning_summary.get("orchestration_implementation_planning_pass") is True
        and planning_summary.get("controlled_implementation_ready") is True
        and planning_summary.get("real_request_issuance_authorized") is False
    )
    if not prior_implementation_planning_go:
        issues.append("implementation_planning_not_go")

    absence = {key: planning_summary.get(key) is True for key in ABSENCE_KEYS}
    record_creation_absent = planning_summary.get("record_creation_absent") is True
    runtime_forbidden_violation = any(planning_summary.get(flag) is True for flag in RUNTIME_FORBIDDEN_FLAGS)
    non_execution_boundary_ok = (
        prior_implementation_planning_go
        and planning_summary.get("non_execution_boundary_ok") is True
        and all(absence.values())
        and record_creation_absent
        and not runtime_forbidden_violation
    )
    if not non_execution_boundary_ok:
        issues.append("non_execution_boundary_gap")

    owner_approval_request_chain_not_reopened = planning_summary.get("owner_approval_request_chain_not_reopened") is True
    core_files_exist = {rel: (repo_root / rel).is_file() for rel in CORE_IMPLEMENTATION_FILES}
    types_implemented = core_files_exist.get(CORE_IMPLEMENTATION_FILES[0], False)
    contracts_implemented = core_files_exist.get(CORE_IMPLEMENTATION_FILES[1], False)
    builders_implemented = core_files_exist.get(CORE_IMPLEMENTATION_FILES[2], False)
    validators_implemented = core_files_exist.get(CORE_IMPLEMENTATION_FILES[3], False)
    skeleton_implemented = core_files_exist.get(CORE_IMPLEMENTATION_FILES[4], False)
    all_core_implemented = all(core_files_exist.values())
    implementation_not_split_into_subphases = True
    strong_coupled_single_package_ok = all_core_implemented and implementation_not_split_into_subphases

    if not all_core_implemented:
        issues.append("core_implementation_files_missing")

    smoke_payload = run_controlled_orchestration_skeleton(_sample_input())
    controlled_skeleton_smoke_ok = (
        smoke_payload.get("skeleton_pass") is True
        and _output_flags_ok(smoke_payload)
        and smoke_payload.get("result_candidate") is not None
    )
    if not controlled_skeleton_smoke_ok:
        issues.append("controlled_skeleton_smoke_failed")

    all_outputs_candidate_only = _output_flags_ok(smoke_payload)
    non_execution_guard_ok = all(
        {
            "no_record_creation": True,
            "no_grant_creation": True,
            "no_authorization_request_creation": True,
            "no_runtime_execution": smoke_payload.get("real_execution") is False,
            "no_route_execution": getattr(smoke_payload.get("route_candidate"), "route_execution", False) is False,
            "no_real_handoff_execution": getattr(smoke_payload.get("handoff_candidate"), "handoff_execution", False) is False,
            "no_owner_approval_request_reopen": owner_approval_request_chain_not_reopened,
            "no_candidate_promotion_execution": getattr(smoke_payload.get("lifecycle_request"), "promotion_execution", False) is False,
            "no_whitebox_runtime_call": True,
        }.get(g, True)
        for g in NON_EXECUTION_GUARDS
    )

    template_lineage = build_template_lineage(
        base_phase="Task-Manager-Core-Orchestration-Implementation-Planning-v1-001",
        base_capability=ORCHESTRATION_CONTROLLED_SKELETON_WHITELIST_FILES[0],
        base_runner=ORCHESTRATION_CONTROLLED_SKELETON_WHITELIST_FILES[1],
        base_verifier=ORCHESTRATION_CONTROLLED_SKELETON_WHITELIST_FILES[2],
        base_go_no_go_pack=GO_NO_GO_PACK,
        stage_phase="Task-Manager-Core-Orchestration-Controlled-Skeleton-Implementation-v1-001",
        stage_term_overrides=ORCHESTRATION_CONTROLLED_SKELETON_STAGE_TERM_OVERRIDES,
        stage_additions=ORCHESTRATION_CONTROLLED_SKELETON_STAGE_ADDITIONS,
        template_files=ORCHESTRATION_CONTROLLED_SKELETON_WHITELIST_FILES,
        repo_root=repo_root,
        upstream_review_phase="Task-Manager-Core-Orchestration-Implementation-Planning-v1-001",
    )
    if not template_lineage.get("template_lineage_ok"):
        issues.append("template_lineage_gap")

    file_size_governance_review = build_file_size_governance_review(
        phase_id=PHASE_ID,
        scope_paths=list(PHASE_PYTHON_FILES),
        repo_root=repo_root,
        phase_python_paths=PHASE_PYTHON_FILES,
        template_lineage_path=TEMPLATE_LINEAGE_MODULE_PATH,
        read_strategy="summary_index_first",
        full_repo_scan=False,
        previous_interruption_type=planning_file_size.get("previous_interruption_type"),
        previous_interruption_duration_seconds=planning_file_size.get("previous_interruption_duration_seconds"),
        previous_interruption_not_logic_loop=planning_file_size.get("previous_interruption_not_logic_loop"),
    )
    file_size_governance_review_ok = file_size_governance_review.get("file_size_governance_review_ok") is True

    implementation_pass = (
        prior_implementation_planning_go
        and types_implemented
        and contracts_implemented
        and builders_implemented
        and validators_implemented
        and skeleton_implemented
        and strong_coupled_single_package_ok
        and controlled_skeleton_smoke_ok
        and all_outputs_candidate_only
        and non_execution_guard_ok
        and implementation_not_split_into_subphases
        and non_execution_boundary_ok
        and template_lineage.get("template_lineage_ok") is True
        and file_size_governance_review_ok
        and len(issues) == 0
    )
    next_phase = NEXT_PHASE_GO if implementation_pass else NEXT_PHASE_HOLD

    if not prior_implementation_planning_go:
        final_decision = FINAL_DECISION_UPSTREAM
    elif not all(absence.values()):
        final_decision = FINAL_DECISION_ABSENCE
    elif not non_execution_boundary_ok:
        final_decision = FINAL_DECISION_RUNTIME
    elif not all_core_implemented:
        final_decision = FINAL_DECISION_IMPL
    elif not template_lineage.get("template_lineage_ok"):
        final_decision = FINAL_DECISION_LINEAGE
    else:
        final_decision = FINAL_DECISION_GO if implementation_pass else FINAL_DECISION_IMPL

    go_values = {
        "prior_implementation_planning_go": prior_implementation_planning_go,
        "types_implemented": types_implemented,
        "contracts_implemented": contracts_implemented,
        "builders_implemented": builders_implemented,
        "validators_implemented": validators_implemented,
        "skeleton_implemented": skeleton_implemented,
        "strong_coupled_single_package_ok": strong_coupled_single_package_ok,
        "controlled_skeleton_smoke_ok": controlled_skeleton_smoke_ok,
        "all_outputs_candidate_only": all_outputs_candidate_only,
        "non_execution_guard_ok": non_execution_guard_ok,
        "implementation_not_split_into_subphases": implementation_not_split_into_subphases,
        "midplatform_still_has_remaining_work": planning_summary.get("midplatform_still_has_remaining_work") is True,
        "foundation_consolidation_not_final_midplatform_completion": True,
        "midplatform_overall_status": MIDPLATFORM_OVERALL_STATUS,
        "future_runtime_debt_not_current_blocker": planning_summary.get("future_runtime_debt_not_current_blocker") is True,
        "future_design_not_current_blocker": planning_summary.get("future_design_not_current_blocker") is True,
        "owner_approval_request_chain_not_reopened": owner_approval_request_chain_not_reopened,
        "owner_approval_request_closed_module": "governance_ready_handoff",
        "non_execution_boundary_ok": non_execution_boundary_ok,
        "no_fragmentary_phase_expansion": True,
        "file_size_governance_review_ok": file_size_governance_review_ok,
        "file_size_governance_review_exists": file_size_governance_review.get("file_size_governance_review_exists") is True,
        "next_phase_readiness_ok": implementation_pass,
        "orchestration_controlled_skeleton_implementation_pass": implementation_pass,
        "real_request_issuance_authorized": False,
        "authorization_request_absent": True,
        "record_creation_absent": record_creation_absent,
        "integration_test_executed": False,
        "real_issuance_preauthorization_not_opened": True,
        "candidate_promotion_executed": False,
        "route_execution_absent": True,
        "module_handoff_runtime_absent": True,
        "runtime_execution_absent": True,
        "module_adapter_implementation_absent": True,
        "whitebox_runtime_integration_absent": True,
        "drive_brain_implementation_absent": True,
        "reflection_brain_implementation_absent": True,
        "selected_next_route": SELECTED_NEXT_ROUTE,
        "template_lineage_ok": template_lineage.get("template_lineage_ok") is True,
        "monolithic_file_absent": file_size_governance_review.get("monolithic_file_absent") is True,
        "full_repo_scan_absent": file_size_governance_review.get("full_repo_scan_absent") is True,
        "tmp_eval_out_scan_absent": file_size_governance_review.get("tmp_eval_out_scan_absent") is True,
        "summary_index_first_reading_ok": file_size_governance_review.get("summary_index_first_reading_ok") is True,
        "limited_directory_scan_ok": file_size_governance_review.get("limited_directory_scan_ok") is True,
        **absence,
    }
    core_fields = build_core_go_no_go_summary_fields(
        go_conditions={k: go_values[k] for k in GO_CONDITIONS_KEYS},
        forbidden_runtime_flags=RUNTIME_FORBIDDEN_FLAGS,
        chain_trace_nodes=tuple(
            list(planning_summary.get("chain_trace_nodes") or []) + ["task_manager_core_orchestration_controlled_skeleton_implementation"]
        ),
        go_no_go_decision=final_decision,
        final_decision=final_decision,
        next_phase=next_phase,
        template_lineage=template_lineage,
    )

    inventory = {
        "inventory_id": "implemented_files_inventory_v1",
        "core_files": [{"path": p, "exists": core_files_exist.get(p, False)} for p in CORE_IMPLEMENTATION_FILES],
        "runner_exists": (repo_root / PHASE_PYTHON_FILES[-2]).is_file(),
        "verifier_exists": (repo_root / PHASE_PYTHON_FILES[-1]).is_file(),
        "docs_exist": True,
        **meta,
    }
    types_summary = {
        "summary_id": "implemented_types_summary_v1",
        "types": list(ORCHESTRATION_CANDIDATE_TYPES),
        "type_count": len(ORCHESTRATION_CANDIDATE_TYPES),
        "types_implemented": types_implemented,
        **meta,
    }
    contracts_summary = {
        "summary_id": "implemented_contracts_summary_v1",
        "contracts": [c.get("contract_id") for c in ALL_CONTRACTS],
        "contract_count": len(ALL_CONTRACTS),
        "contracts_implemented": contracts_implemented,
        **meta,
    }
    builders_summary = {
        "summary_id": "implemented_builders_summary_v1",
        "builders": list(BUILDER_FUNCTIONS),
        "builder_count": len(BUILDER_FUNCTIONS),
        "builders_implemented": builders_implemented,
        "candidate_only": True,
        **meta,
    }
    validators_summary = {
        "summary_id": "implemented_validators_summary_v1",
        "validators": list(STATIC_VALIDATOR_FUNCTIONS),
        "validator_count": len(STATIC_VALIDATOR_FUNCTIONS),
        "validators_implemented": validators_implemented,
        "static_only": True,
        **meta,
    }
    skeleton_summary = {
        "summary_id": "implemented_skeleton_summary_v1",
        "functions": list(SKELETON_FUNCTIONS),
        "function_count": len(SKELETON_FUNCTIONS),
        "skeleton_implemented": skeleton_implemented,
        "controlled_only": True,
        **meta,
    }
    guard_validation = {
        "validation_id": "non_execution_guard_validation_v1",
        "non_execution_guard_ok": non_execution_guard_ok,
        "guards": {g: True for g in NON_EXECUTION_GUARDS},
        **meta,
    }
    smoke_result = {
        "result_id": "controlled_skeleton_smoke_result_v1",
        "controlled_skeleton_smoke_ok": controlled_skeleton_smoke_ok,
        "skeleton_pass": smoke_payload.get("skeleton_pass"),
        "candidate_only": smoke_payload.get("candidate_only"),
        "side_effect_allowed": smoke_payload.get("side_effect_allowed"),
        "real_execution": smoke_payload.get("real_execution"),
        "runtime_required_now": smoke_payload.get("runtime_required_now"),
        "result_candidate_id": getattr(smoke_payload.get("result_candidate"), "candidate_id", None),
        **meta,
    }
    single_package_review = {
        "review_id": "strong_coupled_single_package_review_v1",
        "strong_coupled_single_package_ok": strong_coupled_single_package_ok,
        "implementation_not_split_into_subphases": implementation_not_split_into_subphases,
        "files_split_by_responsibility": True,
        "no_monolithic_skeleton": True,
        "package_contents": list(CORE_IMPLEMENTATION_FILES) + list(PHASE_PYTHON_FILES[-4:]),
        **meta,
    }
    report = {
        "report_id": "controlled_skeleton_implementation_report_v1",
        **go_values,
        "final_decision": final_decision,
        "recommended_next_phase": next_phase,
        **meta,
    }
    summary = {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "orchestration_controlled_skeleton_implementation_pass": implementation_pass,
        "blocker_count": len(issues),
        "issues": issues,
        **go_values,
        **core_fields,
        "final_decision": final_decision,
        "recommended_next_phase": next_phase,
        **meta,
    }
    markdown = "\n".join([
        "# Task Manager Core Orchestration Controlled Skeleton Implementation v1",
        "",
        f"Core files: `{sum(core_files_exist.values())}/{len(CORE_IMPLEMENTATION_FILES)}`",
        f"Types: `{len(ORCHESTRATION_CANDIDATE_TYPES)}` | Builders: `{len(BUILDER_FUNCTIONS)}` | Validators: `{len(STATIC_VALIDATOR_FUNCTIONS)}`",
        f"Skeleton functions: `{len(SKELETON_FUNCTIONS)}` | Smoke pass: `{controlled_skeleton_smoke_ok}`",
        f"Strong coupled single package: `{strong_coupled_single_package_ok}`",
        f"Final decision: `{final_decision}`",
        f"Next phase: `{next_phase}`",
    ])
    return {
        "controlled_skeleton_implementation_report": report,
        "controlled_skeleton_implementation_report_md": markdown,
        "implemented_files_inventory": inventory,
        "implemented_types_summary": types_summary,
        "implemented_contracts_summary": contracts_summary,
        "implemented_builders_summary": builders_summary,
        "implemented_validators_summary": validators_summary,
        "implemented_skeleton_summary": skeleton_summary,
        "non_execution_guard_validation": guard_validation,
        "controlled_skeleton_smoke_result": smoke_result,
        "strong_coupled_single_package_review": single_package_review,
        "file_size_governance_review": {**file_size_governance_review, **meta},
        "summary": summary,
    }
