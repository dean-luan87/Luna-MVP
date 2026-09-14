# -*- coding: utf-8 -*-
"""Luna Midplatform Task Manager Foundation Handoff Planning v1."""

from __future__ import annotations

import dataclasses
import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.midplatform.core.task_manager_types_v1 import (
    TaskBlockCandidate,
    TaskCandidate,
    TaskHandoffCandidate,
    TaskPlanCandidate,
    TaskReadinessCandidate,
    TaskStepCandidate,
)
from capabilities.midplatform.midplatform_task_manager_controlled_skeleton_implementation_dryrun_v1 import (
    SKELETON_FILES,
)
from capabilities.midplatform.midplatform_task_manager_controlled_skeleton_implementation_planning_v1 import (
    BOUNDARY_FALSE,
    PURE_FUNCTIONS,
    STATIC_VALIDATORS,
)
from capabilities.midplatform.midplatform_task_manager_controlled_skeleton_implementation_post_dryrun_review_v1 import (
    FINAL_DECISION_GO as POST_DRYRUN_FINAL_GO,
)

PHASE_ID = "Phase-Midplatform-Task-Manager-Foundation-Handoff-Planning-v1-001"
SCOPE = "midplatform_task_manager_foundation_handoff_planning_only"
SOURCE_CHAIN = "midplatform_task_manager_foundation_handoff_planning_v1"
FOUNDATION_ID = "midplatform_task_manager_foundation_v1"
FOUNDATION_VERSION = "1.0.0-skeleton-planning"
FINAL_DECISION_GO = "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_PLANNING_READY_FOR_DRYRUN"
FINAL_DECISION_BOUNDARY = "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_PLANNING_BLOCKED_BY_BOUNDARY_VIOLATION"
FINAL_DECISION_EVIDENCE = "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_PLANNING_BLOCKED_BY_MISSING_EVIDENCE"
FINAL_DECISION_SEMANTICS = "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_PLANNING_BLOCKED_BY_CANDIDATE_SEMANTICS_DRIFT"
FINAL_DECISION_RUNTIME = "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_PLANNING_BLOCKED_BY_RUNTIME_SCOPE_LEAKAGE"
NEXT_PHASE_GO = "Phase-Midplatform-Task-Manager-Foundation-Handoff-DryRun-v1-001"

BOUNDARY_STATEMENT_EN = (
    "This phase performs Task Manager foundation handoff planning only. It does not create runtime execution "
    "capability, scheduler binding, task execution authority, output authorization, memory write authority, "
    "world model write authority, or module adapter integration."
)
BOUNDARY_STATEMENT_ZH = (
    "本阶段仅执行 Task Manager foundation handoff planning，不创建运行时执行能力、调度器绑定、任务执行授权、"
    "输出授权、记忆写入授权、世界模型写入授权或模块适配器集成。"
)

DEFAULT_DRYRUN_ROOT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
    "midplatform_task_manager_controlled_skeleton_implementation_dryrun"
)
DEFAULT_POST_DRYRUN_ROOT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
    "midplatform_task_manager_controlled_skeleton_implementation_post_dryrun_review"
)
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
    "midplatform_task_manager_foundation_handoff_planning_v1_smoke_v0"
)

CANDIDATE_TYPES: Tuple[Any, ...] = (
    TaskCandidate,
    TaskReadinessCandidate,
    TaskBlockCandidate,
    TaskPlanCandidate,
    TaskStepCandidate,
    TaskHandoffCandidate,
)

CANDIDATE_SEMANTICS: Tuple[Dict[str, Any], ...] = (
    {
        "payload_type": "task_candidate",
        "boundary": "task_candidate != task execution",
        "fact_status": "not_fact",
        "task_execution": False,
        "user_output": False,
        "action_allowed": False,
        "output_allowed": False,
    },
    {
        "payload_type": "task_plan_candidate",
        "boundary": "task_plan_candidate != task execution",
        "fact_status": "not_fact",
        "task_execution": False,
        "action_allowed": False,
    },
    {
        "payload_type": "task_step_candidate",
        "boundary": "task_step_candidate != executed step",
        "fact_status": "not_fact",
        "executed_step": False,
        "action_allowed": False,
    },
    {
        "payload_type": "task_handoff_candidate",
        "boundary": "task_handoff_candidate != direct mount",
        "fact_status": "not_fact",
        "direct_mount": False,
        "action_allowed": False,
        "direct_mount_allowed": False,
    },
)

DOWNSTREAM_READINESS: Tuple[Dict[str, str], ...] = (
    {"consumer": "module_adapter", "readiness": "planning-ready", "implementation_ready": "false"},
    {"consumer": "output_gate", "readiness": "planning-ready", "implementation_ready": "false"},
    {"consumer": "information_channel_governance", "readiness": "future_l1_protocol_input", "implementation_ready": "false"},
    {"consumer": "protocol_governance", "readiness": "future_l1_protocol_dependency", "implementation_ready": "false"},
    {"consumer": "system_diagnostics", "readiness": "planning-ready", "implementation_ready": "false"},
    {"consumer": "worldmodel_memory_bridge", "readiness": "planning-ready-after-admission", "implementation_ready": "false"},
)

NON_EXECUTION_CONSTRAINTS: Tuple[str, ...] = (
    "no_runtime_executor",
    "no_scheduler_binding",
    "no_task_execution_authority",
    "no_output_authorization",
    "no_memory_write_authority",
    "no_worldmodel_write_authority",
    "no_module_adapter_integration",
    "no_information_channel_governance_implementation",
    "no_protocol_governance_implementation",
    "no_authorization_grant",
    "no_success_claim_beyond_planning",
)


def _read_json(path: Path) -> Dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return {}
    return payload if isinstance(payload, dict) else {}


def _field_default(cls: Any, field_name: str) -> Any:
    field = cls.__dataclass_fields__[field_name]
    if field.default is not dataclasses.MISSING:
        return field.default
    return None


def _candidate_type_docs() -> List[Dict[str, Any]]:
    docs = []
    for cls in CANDIDATE_TYPES:
        fields = tuple(cls.__dataclass_fields__.keys())
        docs.append(
            {
                "type_name": cls.__name__,
                "fields": list(fields),
                "has_candidate_id": "candidate_id" in fields,
                "has_trace_ref": "trace_ref" in fields,
                "fact_status_default": _field_default(cls, "fact_status"),
                "candidate_not_fact_default": _field_default(cls, "candidate_not_fact"),
                "handoff_stable": True,
            }
        )
    return docs


def _meta(out: Path, dryrun: Path, post: Path) -> Dict[str, Any]:
    meta: Dict[str, Any] = {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "source_chain": SOURCE_CHAIN,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "foundation_id": FOUNDATION_ID,
        "foundation_version": FOUNDATION_VERSION,
        "runtime_status": "not_enabled",
        "foundation_handoff_planning_only": True,
        "task_manager_files_created_now": True,
        "output_root": str(out),
        "upstream_dryrun_root": str(dryrun),
        "upstream_post_dryrun_root": str(post),
        "boundary_statement_en": BOUNDARY_STATEMENT_EN,
        "boundary_statement_zh": BOUNDARY_STATEMENT_ZH,
    }
    for flag in BOUNDARY_FALSE:
        if flag != "task_manager_files_created_now":
            meta[flag] = False
    return meta


def run_task_manager_foundation_handoff_planning_v1(
    *,
    dryrun_root: str,
    post_dryrun_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    out = Path(output_root or DEFAULT_OUTPUT).expanduser().resolve()
    dryrun = Path(dryrun_root).expanduser().resolve()
    post = Path(post_dryrun_root).expanduser().resolve()
    repo_root = Path(__file__).resolve().parents[2]
    meta = _meta(out, dryrun, post)
    issues: List[str] = []

    dryrun_summary = _read_json(dryrun / "summary.json")
    dryrun_verifier = _read_json(dryrun / "verifier_report.json")
    post_summary = _read_json(post / "summary.json")
    post_verifier = _read_json(post / "verifier_report.json")

    dryrun_verifier_go = dryrun_verifier.get("verifier") == "GO"
    post_dryrun_final_go = post_summary.get("final_decision") == POST_DRYRUN_FINAL_GO
    post_dryrun_verifier_go = post_verifier.get("verifier") == "GO"

    downstream_readiness_gaps: List[str] = []
    if not dryrun_verifier_go:
        downstream_readiness_gaps.append("controlled_skeleton_implementation_dryrun_verifier_not_go")
    if not post_dryrun_final_go:
        downstream_readiness_gaps.append("controlled_skeleton_implementation_post_dryrun_final_not_go")
    if not post_dryrun_verifier_go:
        downstream_readiness_gaps.append("controlled_skeleton_implementation_post_dryrun_verifier_not_go")

    evidence_files = []
    for rel in SKELETON_FILES:
        path = repo_root / rel
        evidence_files.append({"path": rel, "exists": path.is_file(), "role": "core_skeleton_evidence"})
        if not path.is_file():
            issues.append(f"missing_core_skeleton:{rel}")

    evidence_map = {
        "core_skeleton_files": evidence_files,
        "dryrun_summary": {"path": str(dryrun / "summary.json"), "referenced": (dryrun / "summary.json").is_file()},
        "dryrun_verifier": {"path": str(dryrun / "verifier_report.json"), "referenced": (dryrun / "verifier_report.json").is_file()},
        "post_dryrun_summary": {"path": str(post / "summary.json"), "referenced": (post / "summary.json").is_file()},
        "post_dryrun_verifier": {"path": str(post / "verifier_report.json"), "referenced": (post / "verifier_report.json").is_file()},
    }

    candidate_semantics_preserved = (
        _field_default(TaskCandidate, "task_execution") is False
        and _field_default(TaskCandidate, "user_output") is False
        and _field_default(TaskPlanCandidate, "task_execution") is False
        and _field_default(TaskStepCandidate, "executed_step") is False
        and _field_default(TaskHandoffCandidate, "direct_mount") is False
    )
    if not candidate_semantics_preserved:
        issues.append("candidate_semantics_drift")

    global_boundaries = {
        "task_manager_files_created_now": True,
        **{flag: False for flag in BOUNDARY_FALSE if flag != "task_manager_files_created_now"},
        "runtime_executor_created_now": False,
        "scheduler_binding_created_now": False,
        "task_execution_authority_granted_now": False,
        "output_authorization_granted_now": False,
        "module_adapter_integration_created_now": False,
        "information_channel_governance_implemented_now": False,
        "protocol_governance_implemented_now": False,
    }

    non_execution_boundary_ok = all(value is False for key, value in global_boundaries.items() if key != "task_manager_files_created_now")
    downstream_readiness_scope_ok = all(item["implementation_ready"] == "false" for item in DOWNSTREAM_READINESS)
    planning_pass = len(issues) == 0 and non_execution_boundary_ok and candidate_semantics_preserved and downstream_readiness_scope_ok
    final_decision = FINAL_DECISION_GO
    if not planning_pass:
        final_decision = FINAL_DECISION_EVIDENCE if issues else FINAL_DECISION_BOUNDARY
        if "candidate_semantics_drift" in issues:
            final_decision = FINAL_DECISION_SEMANTICS

    handoff_plan = {
        "plan_id": "task_manager_foundation_handoff_plan_v1",
        "stable_objects": {
            "types_boundary": [doc["type_name"] for doc in _candidate_type_docs()],
            "manager_skeleton_boundary": [item["function_name"] for item in PURE_FUNCTIONS],
            "static_validator_boundary": list(STATIC_VALIDATORS),
            "candidate_lifecycle_boundary": [item["payload_type"] for item in CANDIDATE_SEMANTICS],
        },
        "candidate_only_objects": list(CANDIDATE_SEMANTICS),
        "l1_information_channel_inputs": [
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
        ],
        "module_adapter_constraints": [
            "module_adapter may consume task_handoff_candidate only as planning-ready input",
            "module_adapter must not treat task_handoff_candidate as direct mount",
            "module_adapter must not execute task_step_candidate",
        ],
        "handoff_evidence_map": evidence_map,
        "unauthorized_capabilities": list(NON_EXECUTION_CONSTRAINTS),
        "next_handoff_dryrun_must_verify": [
            "evidence_map_complete",
            "candidate_semantics_preserved",
            "boundary_matrix_frozen",
            "downstream_readiness_planning_only",
            "no_runtime_scope_leakage",
            "no_information_channel_governance_implementation",
            "no_protocol_governance_implementation",
        ],
        **meta,
    }
    boundary_matrix = {
        "matrix_id": "task_manager_foundation_boundary_matrix_v1",
        "global_boundaries": global_boundaries,
        "non_execution_boundary_ok": non_execution_boundary_ok,
        **meta,
    }
    lifecycle_matrix = {
        "matrix_id": "task_manager_candidate_lifecycle_matrix_v1",
        "candidate_semantics": list(CANDIDATE_SEMANTICS),
        "candidate_semantics_preserved": candidate_semantics_preserved,
        **meta,
    }
    downstream_matrix = {
        "matrix_id": "task_manager_downstream_readiness_matrix_v1",
        "downstream": list(DOWNSTREAM_READINESS),
        "downstream_readiness_scope_ok": downstream_readiness_scope_ok,
        **meta,
    }
    non_execution_constraints = {
        "constraints_id": "task_manager_non_execution_constraints_v1",
        "constraints": list(NON_EXECUTION_CONSTRAINTS),
        "no_runtime_executor": True,
        "no_scheduler_binding": True,
        "no_output_authorization": True,
        "no_memory_worldmodel_write_path": True,
        "no_module_adapter_integration": True,
        "no_authorization_claim": True,
        "no_success_claim_beyond_planning": True,
        **meta,
    }
    summary = {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "candidate_only": True,
        "planning_pass": planning_pass,
        "task_manager_foundation_handoff_planning_complete": planning_pass,
        "blocker_count": len(issues),
        "issues": issues,
        "downstream_readiness_gaps": downstream_readiness_gaps,
        "downstream_readiness_refs": {
            "upstream_dryrun_root": str(dryrun),
            "upstream_post_dryrun_root": str(post),
            "controlled_skeleton_dryrun_verifier_go": dryrun_verifier_go,
            "controlled_skeleton_post_dryrun_final_go": post_dryrun_final_go,
            "controlled_skeleton_post_dryrun_verifier_go": post_dryrun_verifier_go,
        },
        "expected_next_phase_refs": {
            "next_phase_on_go": NEXT_PHASE_GO,
            "next_handoff_dryrun_must_verify": handoff_plan.get("next_handoff_dryrun_must_verify"),
        },
        "no_execution_performed": True,
        "no_protocol_change": True,
        "non_execution_boundary_ok": non_execution_boundary_ok,
        "candidate_semantics_preserved": candidate_semantics_preserved,
        "foundation_handoff_planning_only": True,
        "downstream_readiness_scope_ok": downstream_readiness_scope_ok,
        "final_decision": final_decision,
        "recommended_next_phase": NEXT_PHASE_GO if planning_pass else PHASE_ID,
        **meta,
    }
    markdown = "\n".join(
        [
            "# Task Manager Foundation Handoff Plan v1",
            "",
            BOUNDARY_STATEMENT_EN,
            "",
            BOUNDARY_STATEMENT_ZH,
            "",
            f"Final decision: `{summary['final_decision']}`",
            f"Recommended next phase: `{summary['recommended_next_phase']}`",
            "",
            "## Stable Objects",
            "- Task Manager candidate dataclasses",
            "- Task Manager pure candidate generators",
            "- Task Manager static validators",
            "",
            "## Preserved Boundaries",
            "- task_candidate != task execution",
            "- task_step_candidate != executed step",
            "- task_handoff_candidate != direct mount",
            "- Information Channel Governance is future L1 protocol input only",
            "- Protocol Governance is future L1 protocol dependency only",
        ]
    )
    return {
        "task_manager_foundation_handoff_plan": handoff_plan,
        "task_manager_foundation_handoff_plan_md": markdown,
        "task_manager_foundation_boundary_matrix": boundary_matrix,
        "task_manager_candidate_lifecycle_matrix": lifecycle_matrix,
        "task_manager_downstream_readiness_matrix": downstream_matrix,
        "task_manager_non_execution_constraints": non_execution_constraints,
        "summary": summary,
    }
