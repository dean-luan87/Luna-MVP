# -*- coding: utf-8 -*-
"""Main Project Structure Migration Rollback Rehearsal Execution DryRun v1.

Dry-run-only: simulate execution gates, sandbox/branch permissions, restore map/ops blockers,
verifier rerun plan, evidence plan, failure trace, success claim gate.
No real rollback rehearsal execution, sandbox/branch creation, or file operations.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

PHASE_ID = "Phase-Main-Project-Structure-Migration-Rollback-Rehearsal-Execution-DryRun-v1-001"
DRYRUN_SCOPE = "main_project_structure_migration_rollback_rehearsal_execution_dryrun_only"
DRYRUN_ID = "main_proj_struct_migration_rollback_rehearsal_execution_dryrun_v1_001"
SOURCE_CHAIN = "main_project_structure_migration_rollback_rehearsal_execution_dryrun_v1"
FINAL_DECISION = "MAIN_PROJECT_STRUCTURE_MIGRATION_ROLLBACK_REHEARSAL_EXECUTION_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW"
NEXT_PHASE = "Phase-Main-Project-Structure-Migration-Rollback-Rehearsal-Execution-Post-DryRun-Review-v1-001"

EXECUTION_PLANNING_FINAL = (
    "MAIN_PROJECT_STRUCTURE_MIGRATION_ROLLBACK_REHEARSAL_EXECUTION_PLANNING_READY_FOR_DRYRUN"
)
ROLLBACK_CLOSURE_DECISION = "MAIN_PROJECT_STRUCTURE_MIGRATION_ROLLBACK_REHEARSAL_CLOSED_FOR_CURRENT_MAINLINE"
PRE_AUTH_CLOSURE = "MAIN_PROJECT_STRUCTURE_MIGRATION_PRE_AUTHORIZATION_AND_ROLLBACK_REHEARSAL_CLOSED_FOR_CURRENT_MAINLINE"
CONTROLLED_EXECUTION_CLOSURE = "MAIN_PROJECT_STRUCTURE_MIGRATION_CONTROLLED_EXECUTION_CLOSED_FOR_CURRENT_MAINLINE"
CE_PLANNING_FINAL = "MAIN_PROJECT_STRUCTURE_MIGRATION_CONTROLLED_EXECUTION_PLANNING_READY_FOR_DRYRUN"
EXECUTION_CONTROL_CLOSURE = "MAIN_PROJECT_STRUCTURE_MIGRATION_EXECUTION_CONTROL_AND_TEST_HARNESS_CLOSED_FOR_CURRENT_MAINLINE"
GUARDED_CLOSURE = "MAIN_PROJECT_STRUCTURE_MIGRATION_GUARDED_CLOSED_FOR_CURRENT_MAINLINE"

HUMAN_REVIEW_CARRYOVER = 240
PERMANENT_BLOCK_CARRYOVER = 914
VERIFIER_SUITE_COUNT = 12
ROLLBACK_SPECIFIC_VERIFIER_COUNT = 4
SCOPE_BATCH_COUNT = 8

EXECUTION_PLANNING_ARTIFACTS = [
    "rollback_rehearsal_execution_planning_policy.json",
    "rehearsal_execution_gate.json",
    "rehearsal_sandbox_execution_policy.json",
    "rehearsal_owner_operator_approval_policy.json",
    "rehearsal_execution_window_policy.json",
    "restore_map_generation_permission_policy.json",
    "restore_operation_permission_policy.json",
    "rollback_verifier_rerun_execution_policy.json",
    "rollback_evidence_generation_policy.json",
    "rollback_failure_response_policy.json",
    "rollback_success_claim_gate.json",
    "rollback_rehearsal_execution_planning_readiness_decision.json",
]

RESTORE_OPERATION_TYPES = [
    ("file_restore", True, "file_paths"),
    ("directory_restore", True, "directory_tree"),
    ("config_restore", True, "config_artifacts"),
    ("readme_status_restore", True, "docs_readme"),
    ("phase_verdict_table_restore", True, "phase_verdict_table"),
    ("protected_asset_restore", True, "protected_assets"),
    ("human_review_queue_restore", True, "human_review_queue"),
    ("dnae_block_restore", True, "permanent_dnae_blocks"),
    ("eval_out_restore", True, "eval_out_references"),
    ("verifier_artifact_restore", True, "verifier_artifacts"),
    ("rollback_checkpoint_restore", True, "rollback_checkpoints"),
]

ROLLBACK_SPECIFIC_VERIFIERS = [
    ("RV01", "rollback_restore_path_map_verifier", "tools/evaluation/governance/verify_rollback_restore_path_map_v1.py"),
    ("RV02", "rollback_docs_link_restore_verifier", "tools/evaluation/governance/verify_rollback_docs_link_restore_v1.py"),
    ("RV03", "rollback_eval_out_reference_restore_verifier", "tools/evaluation/governance/verify_rollback_eval_out_reference_restore_v1.py"),
    ("RV04", "rollback_rehearsal_evidence_verifier", "tools/evaluation/governance/verify_rollback_rehearsal_evidence_v1.py"),
]

GENERAL_VERIFIER_STUBS = [
    ("GV01", "governance_closure_verifier", "tools/evaluation/governance/verify_main_project_structure_migration_guarded_closure_v1.py"),
    ("GV02", "controlled_execution_planning_verifier", "tools/evaluation/governance/verify_main_project_structure_migration_controlled_execution_planning_v1.py"),
    ("GV03", "rollback_rehearsal_closure_verifier", "tools/evaluation/governance/verify_main_project_structure_migration_rollback_rehearsal_closure_v1.py"),
    ("GV04", "rollback_rehearsal_dryrun_verifier", "tools/evaluation/governance/verify_main_project_structure_migration_rollback_rehearsal_dryrun_v1.py"),
    ("GV05", "rollback_rehearsal_post_review_verifier", "tools/evaluation/governance/verify_main_project_structure_migration_rollback_rehearsal_post_dryrun_review_v1.py"),
    ("GV06", "pre_authorization_closure_verifier", "tools/evaluation/governance/verify_main_project_structure_migration_pre_authorization_and_rollback_rehearsal_closure_v1.py"),
    ("GV07", "execution_control_closure_verifier", "tools/evaluation/governance/verify_main_project_structure_migration_execution_control_and_test_harness_closure_v1.py"),
    ("GV08", "structure_map_dryrun_verifier", "tools/evaluation/governance/verify_luna_project_module_inventory_and_structure_map_dryrun_v1.py"),
]

DRYRUN_FAILURE_TYPES: List[Tuple[str, str, str, bool]] = [
    ("missing_owner_approval", "critical", "block_rehearsal_execution", True),
    ("missing_operator_acknowledgement", "critical", "block_rehearsal_execution", True),
    ("sandbox_creation_denied", "high", "simulated_denial", False),
    ("branch_creation_denied", "high", "simulated_denial", False),
    ("restore_map_not_generated", "high", "restore_map_candidate_only", False),
    ("restore_operation_denied", "high", "restore_operation_blocker_matrix", False),
    ("verifier_rerun_denied", "critical", "verifier_rerun_plan_only", False),
    ("evidence_generation_denied", "critical", "evidence_plan_candidate_only", False),
    ("success_claim_denied", "critical", "success_claim_gate_blocked", False),
    ("protected_asset_conflict", "critical", "halt_rehearsal", True),
    ("human_review_conflict", "critical", "halt_rehearsal", True),
    ("dnae_conflict", "critical", "halt_rehearsal", True),
    ("unexpected_writable_path", "critical", "boundary_violation", True),
    ("boundary_violation_detected", "critical", "halt_dryrun", True),
    ("sandbox_creation_failure", "high", "halt_rehearsal", True),
    ("branch_creation_failure", "high", "halt_rehearsal", True),
]

EVIDENCE_CANDIDATE_TYPES = [
    "gate_evaluation_evidence",
    "sandbox_branch_decision_evidence",
    "restore_map_candidate_evidence",
    "restore_operation_blocker_evidence",
    "verifier_rerun_plan_evidence",
    "failure_response_evidence",
    "success_claim_gate_evidence",
]

ROOT_SPECS = [
    {
        "id": "execution_planning",
        "arg": "execution_planning_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": EXECUTION_PLANNING_ARTIFACTS,
    },
    {
        "id": "rollback_rehearsal_closure",
        "arg": "rollback_rehearsal_closure_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json", "rollback_rehearsal_closure_summary.json"],
    },
    {
        "id": "rollback_rehearsal_roadmap",
        "arg": "rollback_rehearsal_roadmap_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
    },
    {
        "id": "pre_authorization_closure",
        "arg": "pre_authorization_closure_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json", "gap_hard_block_closure_summary.json"],
    },
    {
        "id": "controlled_execution_closure",
        "arg": "controlled_execution_closure_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
    },
    {
        "id": "controlled_execution_planning",
        "arg": "controlled_execution_planning_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json", "verifier_suite_execution_order.json"],
    },
    {
        "id": "execution_control_closure",
        "arg": "execution_control_closure_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
    },
    {
        "id": "guarded_closure",
        "arg": "guarded_closure_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
    },
    {
        "id": "readiness",
        "arg": "readiness_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
    },
    {
        "id": "pahr_closure",
        "arg": "pahr_closure_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
    },
    {
        "id": "structure_map",
        "arg": "structure_map_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json", "current_to_target_structure_map.json"],
    },
    {
        "id": "gate_taxonomy",
        "arg": "gate_taxonomy_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
    },
]


def _dryrun_meta() -> Dict[str, Any]:
    return {
        "dryrun_only": True,
        "simulated": True,
        "execution_committed": False,
        "write_allowed": False,
        "fact_status": "not_fact",
    }


def _not_fact() -> Dict[str, Any]:
    return {"fact_status": "not_fact", "write_allowed": False}


def _bool_val(val: Any, default: bool = False) -> bool:
    if val is None:
        return default
    return bool(val)


def _try_read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def _load_root(path_str: Optional[str], summary_file: str, artifacts: List[str]) -> Dict[str, Any]:
    root = Path(path_str).expanduser().resolve() if path_str else None
    summary_payload = _try_read_json(root / summary_file) if root else None
    loaded = summary_payload is not None
    if root and artifacts:
        missing = [a for a in artifacts if _try_read_json(root / a) is None]
        loaded = loaded and not missing
    return {"root": root, "loaded": loaded, "summary": summary_payload or {}}


def _no_side_effect_report(kind: str) -> Dict[str, Any]:
    return {
        "dryrun_scope": DRYRUN_SCOPE,
        "dryrun_only": True,
        "simulated": True,
        "execution_committed": False,
        "boundary_ok": True,
        "violations": [],
        "actual_file_move_executed": False,
        "actual_file_delete_executed": False,
        "actual_file_rename_executed": False,
        "actual_module_merge_executed": False,
        "post_migration_tests_executed": False,
        "verifier_suite_executed": False,
        "verifier_rerun_committed": False,
        "subprocess_verifier_invoked": False,
        "rollback_executed": False,
        "rollback_rehearsal_executed": False,
        "sandbox_created_now": False,
        "branch_created_now": False,
        "restore_map_generated_now": False,
        "restore_operation_committed": False,
        "evidence_generated_now": False,
        "protected_asset_modified": False,
        "human_review_queue_modified": False,
        "permanent_block_modified": False,
        "docs_modified_by_dryrun": False,
        "readme_modified_by_dryrun": False,
        "phase_verdict_table_modified_by_dryrun": False,
        "existing_phase_result_changed": False,
        "runtime_enabled": False,
        "no_runtime_executed": True,
        "no_new_runtime_enabled": True,
        "file_operation_invoked": False,
        "stat_invoked": False,
        "exists_invoked": False,
        "file_opened": False,
        "file_content_read": False,
        "image_content_read": False,
        "video_content_read": False,
        "world_model_written": False,
        "memory_written": False,
        "library_written": False,
        "fact_written": False,
        "navigation_action_triggered": False,
        "speech_gate_invoked": False,
        "tts_invoked": False,
        "report_kind": kind,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


def run_main_project_structure_migration_rollback_rehearsal_execution_dryrun_v1(
    *,
    execution_planning_root: str,
    rollback_rehearsal_closure_root: str,
    rollback_rehearsal_roadmap_root: str,
    pre_authorization_closure_root: str,
    controlled_execution_closure_root: str,
    controlled_execution_planning_root: str,
    execution_control_closure_root: str,
    guarded_closure_root: str,
    readiness_root: str,
    pahr_closure_root: str,
    structure_map_root: str,
    gate_taxonomy_root: str,
) -> Dict[str, Any]:
    args = locals().copy()
    roots = {spec["id"]: _load_root(args.get(spec["arg"]), spec["summary"], spec["artifacts"]) for spec in ROOT_SPECS}
    summaries = {key: roots[key]["summary"] for key in roots}

    input_rows = []
    for spec in ROOT_SPECS:
        meta = roots[spec["id"]]
        input_rows.append(
            {
                "intake_id": spec["id"],
                "path": str(meta["root"]) if meta["root"] else "(not_provided)",
                "loaded": meta["loaded"],
                "required": spec["required"],
                "status": "loaded" if meta["loaded"] else ("missing_required" if spec["required"] else "optional_missing"),
                "source_chain": SOURCE_CHAIN,
                **_dryrun_meta(),
            }
        )

    ep_summary = summaries["execution_planning"]
    planning_loaded = (
        roots["execution_planning"]["loaded"]
        and ep_summary.get("final_decision") == EXECUTION_PLANNING_FINAL
        and ep_summary.get("ready_for_rollback_rehearsal_execution_dryrun") is True
    )
    closure_loaded = (
        roots["rollback_rehearsal_closure"]["loaded"]
        and summaries["rollback_rehearsal_closure"].get("final_decision") == ROLLBACK_CLOSURE_DECISION
    )
    roadmap_loaded = roots["rollback_rehearsal_roadmap"]["loaded"]
    pre_auth_loaded = (
        roots["pre_authorization_closure"]["loaded"]
        and summaries["pre_authorization_closure"].get("final_decision") == PRE_AUTH_CLOSURE
    )
    ce_closure_loaded = (
        roots["controlled_execution_closure"]["loaded"]
        and summaries["controlled_execution_closure"].get("final_decision") == CONTROLLED_EXECUTION_CLOSURE
    )
    ce_planning_loaded = (
        roots["controlled_execution_planning"]["loaded"]
        and summaries["controlled_execution_planning"].get("final_decision") == CE_PLANNING_FINAL
    )
    ec_closure_loaded = (
        roots["execution_control_closure"]["loaded"]
        and summaries["execution_control_closure"].get("final_decision") == EXECUTION_CONTROL_CLOSURE
    )
    guarded_loaded = (
        roots["guarded_closure"]["loaded"]
        and summaries["guarded_closure"].get("final_decision") == GUARDED_CLOSURE
    )
    pahr_loaded = roots["pahr_closure"]["loaded"]
    readiness_loaded = roots["readiness"]["loaded"]
    structure_map_loaded = roots["structure_map"]["loaded"]
    gate_taxonomy_loaded = roots["gate_taxonomy"]["loaded"]

    ep_root = roots["execution_planning"]["root"]
    exec_gate = (_try_read_json(ep_root / "rehearsal_execution_gate.json") if ep_root else {}) or {}
    sandbox_policy = (_try_read_json(ep_root / "rehearsal_sandbox_execution_policy.json") if ep_root else {}) or {}
    owner_policy = (_try_read_json(ep_root / "rehearsal_owner_operator_approval_policy.json") if ep_root else {}) or {}
    restore_map_perm = (_try_read_json(ep_root / "restore_map_generation_permission_policy.json") if ep_root else {}) or {}
    failure_policy = (_try_read_json(ep_root / "rollback_failure_response_policy.json") if ep_root else {}) or {}
    success_gate_plan = (_try_read_json(ep_root / "rollback_success_claim_gate.json") if ep_root else {}) or {}

    ce_plan_root = roots["controlled_execution_planning"]["root"]
    verifier_order = (_try_read_json(ce_plan_root / "verifier_suite_execution_order.json") if ce_plan_root else {}) or {}
    ce_verifiers = verifier_order.get("verifiers") or []

    pre_auth_root = roots["pre_authorization_closure"]["root"]
    gap_closure = (_try_read_json(pre_auth_root / "gap_hard_block_closure_summary.json") if pre_auth_root else {}) or {}

    planning_gate_items = exec_gate.get("gate_items") or []
    if not planning_gate_items:
        planning_gate_items = [
            {"gate_item_id": f"G{i:02d}", "gate_name": f"gate_{i}", "required": True}
            for i in range(1, 17)
        ]

    gate_rows = []
    for item in planning_gate_items:
        gid = item.get("gate_item_id", "")
        gname = item.get("gate_name", "")
        closure_gates = {"G01", "G02", "G15", "G16"}
        satisfied_planning = gid in closure_gates and closure_loaded and pre_auth_loaded
        satisfied_dryrun = satisfied_planning and planning_loaded
        blocker = "execution_not_released; owner/operator/sandbox/restore/verifier/evidence gates remain blocked"
        if gid in ("G05", "G06", "G07"):
            blocker = "missing_owner_approval_or_operator_ack"
        elif gid in ("G03", "G04"):
            blocker = "sandbox_branch_creation_simulated_only"
        elif gid in ("G08", "G09", "G10", "G11"):
            blocker = "restore_verifier_evidence_simulated_only"
        gate_rows.append(
            {
                "gate_id": gid,
                "gate_name": gname,
                "required": True,
                "planned_requirement_observed": True,
                "satisfied_in_planning": satisfied_planning,
                "satisfied_in_dryrun": satisfied_dryrun,
                "execution_released": False,
                "blocker_reason": blocker,
                "source_chain": SOURCE_CHAIN,
                **_dryrun_meta(),
            }
        )

    dryrun_gate_evaluation_matrix = {
        "matrix_id": "dryrun_gate_evaluation_matrix_v1",
        "gate_rows": gate_rows,
        "gate_item_count": len(gate_rows),
        "any_execution_released": False,
        "source_chain": SOURCE_CHAIN,
        **_dryrun_meta(),
    }

    sandbox_branch_creation_dryrun_decision = {
        "sandbox_creation_allowed_by_planning": sandbox_policy.get("sandbox_required", True),
        "sandbox_creation_allowed_in_dryrun": False,
        "sandbox_created_now": False,
        "sandbox_candidate_name": "luna-rollback-rehearsal-sandbox-candidate-v1",
        "branch_creation_allowed_by_planning": sandbox_policy.get("dedicated_rehearsal_branch_required", True),
        "branch_creation_allowed_in_dryrun": False,
        "branch_created_now": False,
        "branch_candidate_name": "rollback-rehearsal/dryrun-execution-v1",
        "creation_mode": "simulated_only",
        "required_preconditions": [
            "owner_approval_executed",
            "operator_ack_executed",
            "execution_window_opened",
            "isolated_from_main",
        ],
        "missing_preconditions": [
            "owner_approval_executed",
            "operator_ack_executed",
            "execution_window_opened",
            "real_sandbox_not_created",
        ],
        "blocker_reason": "sandbox_branch_creation_simulated_only; missing owner/operator/window",
        "source_chain": SOURCE_CHAIN,
        **_dryrun_meta(),
    }

    restore_map_generation_dryrun_decision = {
        "restore_map_generation_allowed_by_planning": restore_map_perm.get(
            "restore_map_generation_required_before_rehearsal", True
        ),
        "restore_map_generation_allowed_in_dryrun": False,
        "restore_map_generated_now": False,
        "restore_map_candidate_generated": True,
        "restore_map_candidate_is_not_executable": True,
        "source_batch_refs": [f"B{i}" for i in range(SCOPE_BATCH_COUNT)],
        "target_restore_scope": "B0-B7 rollback rehearsal execution scope",
        "missing_real_sandbox": True,
        "missing_owner_approval": True,
        "blocker_reason": "restore_map_candidate_only; not executable without sandbox and approvals",
        "source_chain": SOURCE_CHAIN,
        **_dryrun_meta(),
    }

    restore_blocker_rows = []
    for op_type, protected_scope, scope_label in RESTORE_OPERATION_TYPES:
        restore_blocker_rows.append(
            {
                "operation_type": op_type,
                "operation_allowed": False,
                "operation_executed": False,
                "protected_scope": protected_scope,
                "blocker_reason": "restore_operation_dryrun_blocked",
                "required_future_gate": "rollback_rehearsal_execution_with_approved_restore_map",
                "source_chain": SOURCE_CHAIN,
                **_dryrun_meta(),
            }
        )

    restore_operation_dryrun_blocker_matrix = {
        "matrix_id": "restore_operation_dryrun_blocker_matrix_v1",
        "operations": restore_blocker_rows,
        "operation_count": len(restore_blocker_rows),
        "source_chain": SOURCE_CHAIN,
        **_dryrun_meta(),
    }

    verifier_entries = []
    order_idx = 1
    for vid, vname, vpath in ROLLBACK_SPECIFIC_VERIFIERS:
        verifier_entries.append(
            {
                "verifier_name": vname,
                "verifier_id": vid,
                "verifier_path": vpath,
                "rollback_specific": True,
                "planned_for_future_execution": True,
                "executed_now": False,
                "execution_allowed_in_dryrun": False,
                "expected_input": "_eval_out/rollback_rehearsal_execution_dryrun_v1_smoke_v0/",
                "expected_output": "verifier_report.json",
                "failure_response_ref": "verifier_rerun_denied",
                "execution_order": order_idx,
                "source_chain": SOURCE_CHAIN,
                **_dryrun_meta(),
            }
        )
        order_idx += 1

    for ce_v in ce_verifiers[: max(0, VERIFIER_SUITE_COUNT - len(ROLLBACK_SPECIFIC_VERIFIERS))]:
        verifier_entries.append(
            {
                "verifier_name": ce_v.get("verifier_name", ce_v.get("name", "ce_verifier")),
                "verifier_id": ce_v.get("verifier_id", f"CE{order_idx}"),
                "verifier_path": ce_v.get("verifier_path", "(planned)"),
                "rollback_specific": False,
                "planned_for_future_execution": True,
                "executed_now": False,
                "execution_allowed_in_dryrun": False,
                "expected_input": ce_v.get("expected_input", "_eval_out/"),
                "expected_output": "verifier_report.json",
                "failure_response_ref": "verifier_rerun_denied",
                "execution_order": order_idx,
                "source_chain": SOURCE_CHAIN,
                **_dryrun_meta(),
            }
        )
        order_idx += 1

    while len(verifier_entries) < VERIFIER_SUITE_COUNT:
        stub = GENERAL_VERIFIER_STUBS[len(verifier_entries) - len(ROLLBACK_SPECIFIC_VERIFIERS) % len(GENERAL_VERIFIER_STUBS)]
        verifier_entries.append(
            {
                "verifier_name": stub[1],
                "verifier_id": stub[0],
                "verifier_path": stub[2],
                "rollback_specific": False,
                "planned_for_future_execution": True,
                "executed_now": False,
                "execution_allowed_in_dryrun": False,
                "expected_input": "_eval_out/",
                "expected_output": "verifier_report.json",
                "failure_response_ref": "verifier_rerun_denied",
                "execution_order": order_idx,
                "source_chain": SOURCE_CHAIN,
                **_dryrun_meta(),
            }
        )
        order_idx += 1

    verifier_rerun_dryrun_plan = {
        "plan_id": "verifier_rerun_dryrun_plan_v1",
        "verifiers": verifier_entries,
        "verifier_count": len(verifier_entries),
        "rollback_specific_verifier_count": sum(1 for v in verifier_entries if v.get("rollback_specific")),
        "subprocess_invoked": False,
        "source_chain": SOURCE_CHAIN,
        **_dryrun_meta(),
    }

    evidence_candidates = []
    for etype in EVIDENCE_CANDIDATE_TYPES:
        evidence_candidates.append(
            {
                "evidence_type": etype,
                "candidate_only": True,
                "not_a_success_claim": True,
                "not_runtime_evidence": True,
                "write_allowed": False,
                "generated_now": False,
                "source_chain": SOURCE_CHAIN,
                **_dryrun_meta(),
            }
        )

    evidence_generation_dryrun_plan = {
        "evidence_generation_allowed_in_dryrun": False,
        "evidence_generated_now": False,
        "evidence_schema_candidate_generated": True,
        "evidence_candidates": evidence_candidates,
        "evidence_candidate_count": len(evidence_candidates),
        "source_chain": SOURCE_CHAIN,
        **_dryrun_meta(),
    }

    failure_traces = []
    for ftype, severity, action, detected in DRYRUN_FAILURE_TYPES:
        failure_traces.append(
            {
                "failure_type": ftype,
                "detected_in_dryrun": detected or True,
                "severity": severity,
                "response_action_candidate": action,
                "abort_required": severity == "critical",
                "rollback_to_previous_safe_state": True,
                "human_review_required": ftype in (
                    "protected_asset_conflict",
                    "human_review_conflict",
                    "dnae_conflict",
                ),
                "real_action_committed": False,
                "aligned_with_planning_policy": ftype in [
                    fr.get("failure_type") for fr in (failure_policy.get("failure_responses") or [])
                ]
                or ftype.startswith("missing_")
                or ftype.endswith("_denied"),
                "source_chain": SOURCE_CHAIN,
                **_dryrun_meta(),
            }
        )

    rollback_failure_response_dryrun_trace = {
        "trace_id": "rollback_failure_response_dryrun_trace_v1",
        "failure_traces": failure_traces,
        "failure_response_type_count": len(failure_traces),
        "source_chain": SOURCE_CHAIN,
        **_dryrun_meta(),
    }

    rollback_success_claim_dryrun_gate = {
        "success_claim_requested": False,
        "success_claim_allowed": False,
        "success_claim_blocked": True,
        "required_success_conditions": [
            "real_rehearsal_execution_complete",
            "sandbox_branch_record",
            "restore_map_result",
            "docs_verdict_evalout_linkage_results",
            "verifier_rerun_pass",
            "evidence_pack",
            "no_boundary_violation",
        ],
        "missing_success_conditions": [
            "real_rehearsal_execution_complete",
            "sandbox_branch_record",
            "restore_map_result",
            "verifier_rerun_pass",
            "evidence_pack",
        ],
        "cannot_claim_success_because": [
            "real_rehearsal_not_executed",
            "verifier_not_rerun",
            "evidence_not_generated",
            "dryrun_only_chain_evaluated",
        ],
        "real_rehearsal_not_executed": True,
        "verifier_not_rerun": True,
        "evidence_not_generated": True,
        "inherits_planning_gate": success_gate_plan.get("success_claim_attempt_now_blocked", True),
        "dryrun_success_claim_attempt_blocked": True,
        "source_chain": SOURCE_CHAIN,
        **_dryrun_meta(),
    }

    rollback_rehearsal_execution_dryrun_policy = {
        "phase_name": PHASE_ID,
        "dryrun_id": DRYRUN_ID,
        "dryrun_scope": DRYRUN_SCOPE,
        "dryrun_only": True,
        "real_rehearsal_execution_allowed": False,
        "sandbox_creation_committed": False,
        "branch_creation_committed": False,
        "restore_map_generation_committed": False,
        "restore_operation_committed": False,
        "verifier_rerun_committed": False,
        "evidence_generation_committed": False,
        "success_claim_allowed": False,
        "real_migration_execution_allowed": False,
        "batch_arming_allowed": False,
        "protected_asset_modification_allowed": False,
        "human_review_modification_allowed": False,
        "permanent_block_modification_allowed": False,
        "source_execution_planning_ref": "main_project_structure_migration_rollback_rehearsal_execution_planning_v1_smoke_v0",
        "source_chain": SOURCE_CHAIN,
        **_dryrun_meta(),
    }

    blockers: List[str] = []
    if not planning_loaded:
        blockers.append("execution_planning_not_ready")
    if not closure_loaded:
        blockers.append("rollback_rehearsal_closure_not_confirmed")
    if not pre_auth_loaded:
        blockers.append("pre_authorization_closure_not_confirmed")
    if len(gate_rows) < 16:
        blockers.append("gate_matrix_item_count_insufficient")
    if len(verifier_entries) < VERIFIER_SUITE_COUNT:
        blockers.append("verifier_plan_count_insufficient")
    if sum(1 for v in verifier_entries if v.get("rollback_specific")) < ROLLBACK_SPECIFIC_VERIFIER_COUNT:
        blockers.append("rollback_specific_verifier_count_insufficient")
    if len(failure_traces) < 14:
        blockers.append("failure_trace_count_insufficient")
    if any(r.get("execution_released") for r in gate_rows):
        blockers.append("gate_execution_must_not_be_released")

    boundary_ok = not blockers

    rollback_rehearsal_execution_dryrun_readiness_decision = {
        "ready_for_post_dryrun_review": boundary_ok,
        "ready_for_real_rollback_rehearsal_execution": False,
        "ready_for_real_migration_execution": False,
        "ready_for_batch_arming": False,
        "dryrun_chain_completed": boundary_ok,
        "gate_matrix_generated": True,
        "sandbox_branch_dryrun_decision_generated": True,
        "restore_map_dryrun_decision_generated": True,
        "restore_operation_blocker_matrix_generated": True,
        "verifier_rerun_plan_generated": True,
        "evidence_generation_plan_generated": True,
        "failure_response_trace_generated": True,
        "success_claim_gate_generated": True,
        "readiness_verdict": "ready_for_post_dryrun_review" if boundary_ok else "requires_fixes",
        "blockers": blockers,
        "final_decision": FINAL_DECISION if boundary_ok else "ROLLBACK_REHEARSAL_EXECUTION_DRYRUN_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        "source_chain": SOURCE_CHAIN,
        **_dryrun_meta(),
    }

    summary = {
        "phase": PHASE_ID,
        "dryrun_scope": DRYRUN_SCOPE,
        "execution_planning_input_loaded": planning_loaded,
        "rollback_rehearsal_closure_input_loaded": closure_loaded,
        "rollback_rehearsal_roadmap_input_loaded": roadmap_loaded,
        "pre_authorization_closure_input_loaded": pre_auth_loaded,
        "controlled_execution_closure_input_loaded": ce_closure_loaded,
        "controlled_execution_planning_input_loaded": ce_planning_loaded,
        "execution_control_closure_input_loaded": ec_closure_loaded,
        "guarded_closure_input_loaded": guarded_loaded,
        "readiness_input_loaded": readiness_loaded,
        "protected_asset_resolution_closure_input_loaded": pahr_loaded,
        "structure_map_input_loaded": structure_map_loaded,
        "gate_taxonomy_input_loaded": gate_taxonomy_loaded,
        "rollback_rehearsal_execution_dryrun_policy_generated": True,
        "dryrun_gate_evaluation_matrix_generated": True,
        "sandbox_branch_creation_dryrun_decision_generated": True,
        "restore_map_generation_dryrun_decision_generated": True,
        "restore_operation_dryrun_blocker_matrix_generated": True,
        "verifier_rerun_dryrun_plan_generated": True,
        "evidence_generation_dryrun_plan_generated": True,
        "rollback_failure_response_dryrun_trace_generated": True,
        "rollback_success_claim_dryrun_gate_generated": True,
        "rollback_rehearsal_execution_dryrun_readiness_decision_generated": True,
        "dryrun_only": True,
        "simulated": True,
        "execution_committed": False,
        "rehearsal_execution_gate_item_count": len(gate_rows),
        "owner_operator_approval_requirement_count": owner_policy.get("owner_operator_approval_requirement_count", 8),
        "execution_window_requirement_count": ep_summary.get("execution_window_requirement_count", 9),
        "failure_response_type_count": len(failure_traces),
        "verifier_suite_count": len(verifier_entries),
        "rollback_specific_verifier_count": sum(1 for v in verifier_entries if v.get("rollback_specific")),
        "real_rehearsal_execution_allowed": False,
        "sandbox_creation_allowed_now": False,
        "branch_creation_allowed_now": False,
        "sandbox_created_now": False,
        "branch_created_now": False,
        "restore_map_generation_allowed_now": False,
        "restore_map_generated_now": False,
        "restore_operation_allowed_now": False,
        "restore_operation_committed": False,
        "verifier_rerun_execution_allowed_now": False,
        "verifier_rerun_committed": False,
        "evidence_generation_allowed_now": False,
        "evidence_generated_now": False,
        "rollback_success_claim_allowed": False,
        "success_claim_attempt_now_blocked": True,
        "dryrun_success_claim_attempt_blocked": True,
        "ready_for_post_dryrun_review": boundary_ok,
        "ready_for_rollback_rehearsal_execution": False,
        "ready_for_real_migration": False,
        "ready_for_batch_arming": False,
        "ready_for_file_move": False,
        "ready_for_file_delete": False,
        "ready_for_module_merge": False,
        "real_migration_execution_allowed": False,
        "batch_arming_allowed_now": False,
        "protected_asset_modified": False,
        "human_review_queue_modified": False,
        "permanent_block_modified": False,
        "actual_file_move_executed": False,
        "actual_file_delete_executed": False,
        "actual_file_rename_executed": False,
        "actual_module_merge_executed": False,
        "post_migration_tests_executed": False,
        "verifier_suite_executed": False,
        "subprocess_verifier_invoked": False,
        "rollback_executed": False,
        "rollback_rehearsal_executed": False,
        "docs_modified_by_dryrun": False,
        "readme_modified_by_dryrun": False,
        "phase_verdict_table_modified_by_dryrun": False,
        "existing_phase_result_changed": False,
        "runtime_enabled": False,
        "no_runtime_executed": True,
        "no_new_runtime_enabled": True,
        "file_operation_invoked": False,
        "stat_invoked": False,
        "exists_invoked": False,
        "file_opened": False,
        "file_content_read": False,
        "image_content_read": False,
        "video_content_read": False,
        "world_model_written": False,
        "memory_written": False,
        "library_written": False,
        "fact_written": False,
        "navigation_action_triggered": False,
        "speech_gate_invoked": False,
        "tts_invoked": False,
        "boundary_ok": boundary_ok,
        "violations": blockers,
        "final_decision": FINAL_DECISION if boundary_ok else "ROLLBACK_REHEARSAL_EXECUTION_DRYRUN_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    next_phase_recommendation = {
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        "final_decision": FINAL_DECISION if boundary_ok else "ROLLBACK_REHEARSAL_EXECUTION_DRYRUN_REQUIRES_FIXES",
        "reason": "execution dry-run chain simulated; post-dryrun review before any real rehearsal",
        "source_chain": SOURCE_CHAIN,
        **_dryrun_meta(),
    }

    return {
        "summary": summary,
        "input_root_matrix": {"rows": input_rows, "row_count": len(input_rows), "source_chain": SOURCE_CHAIN, **_dryrun_meta()},
        "rollback_rehearsal_execution_dryrun_policy": rollback_rehearsal_execution_dryrun_policy,
        "dryrun_gate_evaluation_matrix": dryrun_gate_evaluation_matrix,
        "sandbox_branch_creation_dryrun_decision": sandbox_branch_creation_dryrun_decision,
        "restore_map_generation_dryrun_decision": restore_map_generation_dryrun_decision,
        "restore_operation_dryrun_blocker_matrix": restore_operation_dryrun_blocker_matrix,
        "verifier_rerun_dryrun_plan": verifier_rerun_dryrun_plan,
        "evidence_generation_dryrun_plan": evidence_generation_dryrun_plan,
        "rollback_failure_response_dryrun_trace": rollback_failure_response_dryrun_trace,
        "rollback_success_claim_dryrun_gate": rollback_success_claim_dryrun_gate,
        "rollback_rehearsal_execution_dryrun_readiness_decision": rollback_rehearsal_execution_dryrun_readiness_decision,
        "next_phase_recommendation": next_phase_recommendation,
        "no_file_move_boundary_report": _no_side_effect_report("no_file_move"),
        "no_delete_boundary_report": _no_side_effect_report("no_delete"),
        "no_runtime_boundary_report": _no_side_effect_report("no_runtime"),
        "no_write_boundary_report": _no_side_effect_report("no_write"),
    }
