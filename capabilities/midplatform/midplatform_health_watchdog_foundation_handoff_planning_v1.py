# -*- coding: utf-8 -*-
"""Luna Midplatform Health Watchdog Foundation Handoff Planning v1."""

from __future__ import annotations

import dataclasses
import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.midplatform.core.health_watchdog_types_v1 import (
    DegradationCandidate,
    HealthSeverity,
    HealthSignalCandidate,
    HealthWatchdogState,
    ModuleHealthReviewCandidate,
    RecoveryRecommendationCandidate,
    RequiredObservationCandidate,
    WatchdogHandoffCandidate,
)
from capabilities.midplatform.midplatform_health_watchdog_controlled_skeleton_implementation_dryrun_v1 import (
    PURE_FUNCTION_NAMES,
    RUNTIME_FALSE_FLAGS,
    SKELETON_FILES,
    STATIC_VALIDATOR_NAMES,
)
from capabilities.midplatform.midplatform_health_watchdog_controlled_skeleton_implementation_post_dryrun_review_v1 import (
    FINAL_DECISION_GO as POST_DRYRUN_FINAL_GO,
    NEXT_PHASE_GO as POST_DRYRUN_NEXT,
)

PHASE_ID = "Phase-Midplatform-Health-Watchdog-Foundation-Handoff-Planning-v1-001"
SCOPE = "midplatform_health_watchdog_foundation_handoff_planning_only"
SOURCE_CHAIN = "midplatform_health_watchdog_foundation_handoff_planning_v1"

UPSTREAM_POST_DRYRUN_FINAL = POST_DRYRUN_FINAL_GO
UPSTREAM_POST_DRYRUN_NEXT = POST_DRYRUN_NEXT

FINAL_DECISION_GO = "MIDPLATFORM_HEALTH_WATCHDOG_FOUNDATION_HANDOFF_PLANNING_READY_FOR_DRYRUN_AND_REVIEW"
FINAL_DECISION_HOLD = "MIDPLATFORM_HEALTH_WATCHDOG_FOUNDATION_HANDOFF_PLANNING_HOLD_FOR_ISSUE_REVIEW"
NEXT_PHASE_GO = "Phase-Midplatform-Health-Watchdog-Foundation-Handoff-DryRunAndReview-v1-001"
NEXT_PHASE_HOLD = "Phase-Midplatform-Health-Watchdog-Foundation-Handoff-Issue-Review-v1-001"

FOUNDATION_ID = "midplatform_health_watchdog_foundation_v1"
DEPENDS_ON = "midplatform_decision_center_foundation_v1"
ALSO_DEPENDS_ON = "midplatform_information_integration_foundation_v1"
ALSO_DEPENDS_ON_MICRO_OS = "midplatform_micro_os_foundation_v1"
FOUNDATION_VERSION = "1.0.0-skeleton"
FOUNDATION_STATUS = "frozen_for_downstream_mount_planning"
COMPATIBILITY_SCOPE = "planning_and_static_dryrun_only"

UPSTREAM_POST_DRYRUN_ARTIFACTS: Tuple[str, ...] = (
    "skeleton_file_integrity_review_v1.json",
    "forbidden_runtime_import_review_v1.json",
    "pure_function_boundary_review_v1.json",
    "type_contract_review_v1.json",
    "function_contract_review_v1.json",
    "static_validator_review_v1.json",
    "sample_dryrun_output_review_v1.json",
    "processing_chain_review_v1.json",
    "governance_guard_review_v1.json",
    "recovery_guard_review_v1.json",
    "decision_center_dependency_review_v1.json",
    "downstream_readiness_review_v1.json",
    "boundary_matrix_post_review_v1.json",
    "post_dryrun_issue_register_v1.json",
    "post_dryrun_readiness_decision_v1.json",
    "summary.json",
    "verifier_report.json",
)

FROZEN_ENUM_TYPES: Tuple[str, ...] = ("HealthWatchdogState", "HealthSeverity")
FROZEN_CANDIDATE_TYPES: Tuple[str, ...] = (
    "HealthSignalCandidate",
    "DegradationCandidate",
    "RecoveryRecommendationCandidate",
    "RequiredObservationCandidate",
    "ModuleHealthReviewCandidate",
    "WatchdogHandoffCandidate",
)
REQUIRED_TYPE_BASE_FIELDS: Tuple[str, ...] = ("candidate_id", "trace_ref", "fact_status")

HANDOFF_RULES: Tuple[str, ...] = (
    "downstream may only import health/watchdog candidate types",
    "downstream may only import pure functions",
    "downstream may only import validators",
    "downstream may only consume candidate outputs",
    "downstream must not require Health Watchdog runtime",
    "downstream must not treat recovery_recommendation_candidate as recovery execution",
    "downstream must not treat degradation_candidate as real degradation",
    "downstream must not treat watchdog_handoff_candidate as direct mount",
    "downstream must not bypass Governance Gate",
    "downstream must not write Memory or WorldModel directly",
    "downstream must not mount Output Gate runtime directly",
    "downstream must not trigger module restart or process control",
)

DOWNSTREAM_OUTPUT_CONTRACT: Tuple[Dict[str, Any], ...] = (
    {
        "consumer": "task_manager",
        "timing": "later",
        "consumes": [
            "hold_candidate",
            "safety_block_candidate",
            "module_health_review_candidate",
            "watchdog_handoff_candidate",
        ],
    },
    {
        "consumer": "module_adapter",
        "timing": "later",
        "consumes": ["required_observation_candidate"],
    },
    {
        "consumer": "decision_center_loopback",
        "timing": "later",
        "consumes": ["health_review_result_candidate"],
    },
    {
        "consumer": "output_gate",
        "timing": "after_output_gate_mount_and_output_readiness",
        "consumes": ["no_direct_output"],
    },
    {
        "consumer": "worldmodel_memory_bridge",
        "timing": "after_admission_policy_later",
        "consumes": ["health_observation_candidate"],
    },
    {
        "consumer": "governance_gate",
        "timing": "boundary_consumer",
        "consumes": ["high_risk_recovery_candidate", "safety_block_candidate", "governance_review_candidate"],
    },
)

FORBIDDEN_MUTATIONS: Tuple[str, ...] = (
    "modify_recovery_recommendation_recovery_execution_false_semantics",
    "modify_recovery_recommendation_restart_allowed_false_semantics",
    "modify_recovery_recommendation_process_control_allowed_false_semantics",
    "modify_degradation_candidate_real_degradation_false_semantics",
    "modify_watchdog_handoff_direct_mount_false_semantics",
    "remove_candidate_id_or_trace_ref_or_fact_status",
    "turn_pure_function_into_runtime_function",
    "introduce_model_invocation_in_skeleton",
    "introduce_provider_invocation_in_skeleton",
    "execute_recovery_in_skeleton",
    "restart_module_in_skeleton",
    "perform_process_control_in_skeleton",
    "execute_task_chain_in_skeleton",
    "write_memory_or_worldmodel_in_skeleton",
    "generate_user_output_in_skeleton",
    "let_task_manager_treat_hold_or_block_candidate_as_executed_task",
    "let_output_gate_consume_watchdog_handoff_before_mount",
    "let_health_watchdog_redefine_decision_center",
)

CHANGE_CONTROL_STEPS: Tuple[str, ...] = (
    "change_request_candidate",
    "compatibility_impact_review",
    "affected_downstream_consumer_matrix",
    "health_watchdog_candidate_contract_update_review",
    "recovery_boundary_review_required",
    "verifier_update_required",
    "foundation_version_bump_required",
    "no_direct_mutation_allowed",
)

DOWNSTREAM_READINESS: Tuple[Dict[str, str], ...] = (
    {"module": "task_manager_mount_planning", "readiness": "primary_next_ready"},
    {
        "module": "module_adapter_feedback_mount_planning",
        "readiness": "secondary_after_task_manager_or_parallel_later",
    },
    {
        "module": "output_gate_mount_planning",
        "readiness": "not_ready_until_task_manager_and_output_handoff_contract_review",
    },
    {
        "module": "worldmodel_memory_bridge_mount_planning",
        "readiness": "ready_after_health_observation_admission_policy",
    },
    {"module": "decision_center_loopback_review", "readiness": "ready_as_candidate_feedback_consumer"},
    {"module": "governance_gate_review", "readiness": "ready_as_boundary_consumer"},
)

NON_CLAIMS: Tuple[str, ...] = (
    "Health Watchdog Foundation Handoff ≠ runtime enabled",
    "Health Watchdog Foundation Handoff ≠ Health Watchdog mounted",
    "Health Watchdog Foundation Handoff ≠ recovery execution",
    "Health Watchdog Foundation Handoff ≠ module restart",
    "Health Watchdog Foundation Handoff ≠ process control",
    "Health Watchdog Foundation Handoff ≠ task execution",
    "Health Watchdog Foundation Handoff ≠ user output",
    "Health Watchdog Foundation Handoff ≠ Output Gate ready",
    "Health Watchdog Foundation Handoff ≠ Task Manager mounted",
    "Health Watchdog Foundation Handoff ≠ model/provider invocation",
    "Health Watchdog Foundation Handoff ≠ Memory / WorldModel write",
    "Health Watchdog Foundation Handoff ≠ full safety system",
)

ROUTE_RATIONALE: Tuple[str, ...] = (
    "Health Watchdog can generate hold / blocked / safety block / required observation / module health review candidates",
    "Task Manager is the natural downstream consumer of health-gated task progression candidates",
    "Output Gate must wait for Task Manager and output handoff contract stability",
    "WorldModel-Memory Bridge must wait for admission policy",
)

DEFAULT_POST_DRYRUN_ROOT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
    "midplatform_health_watchdog_controlled_skeleton_implementation_post_dryrun_review"
)
DEFAULT_SKELETON_DRYRUN_ROOT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
    "midplatform_health_watchdog_controlled_skeleton_implementation_dryrun"
)
DEFAULT_MOUNT_DRYRUN_ROOT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/midplatform_health_watchdog_mount_dryrun_and_review"
)
DEFAULT_DECISION_CENTER_HANDOFF_DRYRUN_ROOT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/midplatform_decision_center_foundation_handoff_dryrun_and_review"
)
DEFAULT_OUTPUT = "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/midplatform_health_watchdog_foundation_handoff_planning"


def _field_default(cls: Any, field_name: str) -> Any:
    field = cls.__dataclass_fields__[field_name]
    if field.default is not dataclasses.MISSING:
        return field.default
    return None


def _candidate_type_docs() -> List[Dict[str, Any]]:
    docs = []
    for cls in (
        HealthSignalCandidate,
        DegradationCandidate,
        RecoveryRecommendationCandidate,
        RequiredObservationCandidate,
        ModuleHealthReviewCandidate,
        WatchdogHandoffCandidate,
    ):
        fields = tuple(cls.__dataclass_fields__.keys())
        docs.append(
            {
                "type_name": cls.__name__,
                "fields": list(fields),
                "required_base_fields": list(REQUIRED_TYPE_BASE_FIELDS),
                "fact_status_default": _field_default(cls, "fact_status"),
                "candidate_not_fact_default": _field_default(cls, "candidate_not_fact"),
                "frozen": True,
            }
        )
    return docs


def _meta(output_root: Path, post_root: Path, dryrun_root: Path, mount_root: Path, dc_root: Path) -> Dict[str, Any]:
    meta: Dict[str, Any] = {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "source_chain": SOURCE_CHAIN,
        "foundation_id": FOUNDATION_ID,
        "depends_on": DEPENDS_ON,
        "also_depends_on": ALSO_DEPENDS_ON,
        "also_depends_on_micro_os": ALSO_DEPENDS_ON_MICRO_OS,
        "runtime_status": "not_enabled",
        "health_watchdog_foundation_handoff_planning_only": True,
        "health_watchdog_foundation_frozen_for_handoff_planning": True,
        "health_watchdog_files_created_now": True,
        "output_root": str(output_root),
        "upstream_post_dryrun_root": str(post_root),
        "upstream_skeleton_dryrun_root": str(dryrun_root),
        "upstream_mount_dryrun_root": str(mount_root),
        "upstream_decision_center_handoff_dryrun_root": str(dc_root),
    }
    for flag in RUNTIME_FALSE_FLAGS:
        meta[flag] = False
    return meta


def _read_json(path: Path) -> Dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return {}
    return payload if isinstance(payload, dict) else {}


def run_midplatform_health_watchdog_foundation_handoff_planning_v1(
    *,
    post_dryrun_root: str,
    skeleton_dryrun_root: str,
    mount_dryrun_root: str,
    decision_center_handoff_dryrun_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    out = Path(output_root or DEFAULT_OUTPUT).expanduser().resolve()
    post = Path(post_dryrun_root).expanduser().resolve()
    dryrun = Path(skeleton_dryrun_root).expanduser().resolve()
    mount = Path(mount_dryrun_root).expanduser().resolve()
    dc = Path(decision_center_handoff_dryrun_root).expanduser().resolve()
    repo_root = Path(__file__).resolve().parents[2]
    meta = _meta(out, post, dryrun, mount, dc)
    issues: List[str] = []

    post_summary = _read_json(post / "summary.json")
    post_decision = _read_json(post / "post_dryrun_readiness_decision_v1.json")
    post_verifier = _read_json(post / "verifier_report.json")
    if post_summary.get("final_decision") != UPSTREAM_POST_DRYRUN_FINAL:
        issues.append("post_dryrun_final_decision_not_go")
    if post_decision.get("final_decision") != UPSTREAM_POST_DRYRUN_FINAL:
        issues.append("post_dryrun_readiness_not_go")
    if post_verifier.get("verifier") != "GO":
        issues.append("post_dryrun_verifier_not_go")
    for artifact in UPSTREAM_POST_DRYRUN_ARTIFACTS:
        if not (post / artifact).is_file():
            issues.append(f"missing_post_dryrun_artifact:{artifact}")
    for rel in SKELETON_FILES:
        if not (repo_root / rel).is_file():
            issues.append(f"missing_skeleton_file:{rel}")

    handoff_scope = {
        "scope_id": "health_watchdog_foundation_handoff_scope_v1",
        "frozen_skeleton_files": list(SKELETON_FILES),
        "frozen_enums": list(FROZEN_ENUM_TYPES),
        "frozen_candidate_types": list(FROZEN_CANDIDATE_TYPES),
        "frozen_functions": list(PURE_FUNCTION_NAMES),
        "frozen_validators": list(STATIC_VALIDATOR_NAMES),
        "processing_chain_frozen": True,
        "governance_guard_frozen": True,
        "recovery_guard_frozen": True,
        "decision_center_dependency_guard_frozen": True,
        "downstream_readiness_frozen": True,
        "handoff_not_runtime_enabled": True,
        **meta,
    }
    version_tag = {
        "tag_id": "health_watchdog_foundation_version_tag_v1",
        "foundation_id": FOUNDATION_ID,
        "depends_on": DEPENDS_ON,
        "also_depends_on": ALSO_DEPENDS_ON,
        "also_depends_on_micro_os": ALSO_DEPENDS_ON_MICRO_OS,
        "version": FOUNDATION_VERSION,
        "status": FOUNDATION_STATUS,
        "runtime_status": "not_enabled",
        "compatibility_scope": COMPATIBILITY_SCOPE,
        "allowed_consumers": [
            "task_manager",
            "module_adapter",
            "output_gate",
            "worldmodel_memory_bridge",
            "decision_center_loopback",
            "governance_gate",
        ],
        **meta,
    }
    frozen_type_interface = {
        "interface_id": "health_watchdog_frozen_type_interface_v1",
        "enums": {
            "HealthWatchdogState": [s.value for s in HealthWatchdogState],
            "HealthSeverity": [s.value for s in HealthSeverity],
        },
        "types": _candidate_type_docs(),
        "type_count": len(FROZEN_CANDIDATE_TYPES),
        "enum_count": len(FROZEN_ENUM_TYPES),
        "required_base_fields": list(REQUIRED_TYPE_BASE_FIELDS),
        "fact_status_default": "not_fact",
        "degradation_real_degradation_default": _field_default(DegradationCandidate, "real_degradation"),
        "recovery_execution_default": _field_default(RecoveryRecommendationCandidate, "recovery_execution"),
        "restart_allowed_default": _field_default(RecoveryRecommendationCandidate, "restart_allowed"),
        "process_control_allowed_default": _field_default(RecoveryRecommendationCandidate, "process_control_allowed"),
        "watchdog_handoff_direct_mount_default": _field_default(WatchdogHandoffCandidate, "direct_mount"),
        **meta,
    }
    frozen_function_interface = {
        "interface_id": "health_watchdog_frozen_function_interface_v1",
        "functions": list(PURE_FUNCTION_NAMES),
        "function_count": len(PURE_FUNCTION_NAMES),
        "candidate_only": True,
        "no_runtime": True,
        "no_recovery_execution": True,
        "no_restart": True,
        "no_process_control": True,
        "no_task_execution": True,
        "no_user_output": True,
        **meta,
    }
    frozen_validator_interface = {
        "interface_id": "health_watchdog_frozen_validator_interface_v1",
        "validators": list(STATIC_VALIDATOR_NAMES),
        "validator_count": len(STATIC_VALIDATOR_NAMES),
        "reusable_downstream": True,
        **meta,
    }
    handoff_contract = {
        "contract_id": "health_watchdog_handoff_contract_v1",
        "rules": list(HANDOFF_RULES),
        "rule_count": len(HANDOFF_RULES),
        **meta,
    }
    downstream_output_contract = {
        "contract_id": "health_watchdog_downstream_output_contract_v1",
        "outputs": list(DOWNSTREAM_OUTPUT_CONTRACT),
        "task_manager_ready": False,
        "output_gate_ready": False,
        "module_adapter_ready": False,
        **meta,
    }
    forbidden_mutation_policy = {
        "policy_id": "health_watchdog_forbidden_mutation_policy_v1",
        "forbidden_mutations": list(FORBIDDEN_MUTATIONS),
        "mutation_count": len(FORBIDDEN_MUTATIONS),
        **meta,
    }
    change_control_policy = {
        "policy_id": "health_watchdog_change_control_policy_v1",
        "steps": list(CHANGE_CONTROL_STEPS),
        "step_count": len(CHANGE_CONTROL_STEPS),
        "real_change_executed_now": False,
        **meta,
    }
    boundary_freeze = {
        "freeze_id": "health_watchdog_boundary_freeze_v1",
        "global_boundaries": {"health_watchdog_files_created_now": True, **{flag: False for flag in RUNTIME_FALSE_FLAGS}},
        **meta,
    }
    downstream_readiness_matrix = {
        "matrix_id": "health_watchdog_downstream_readiness_matrix_v1",
        "readiness": list(DOWNSTREAM_READINESS),
        "route_recommendation": "Task Manager Mount Planning = primary_next_ready",
        **meta,
    }
    non_claims = {
        "register_id": "health_watchdog_non_claims_v1",
        "non_claims": list(NON_CLAIMS),
        **meta,
    }
    route_decision = {
        "decision_id": "health_watchdog_route_decision_v1",
        "primary_next_phase": "Phase-Midplatform-Task-Manager-Mount-Planning-v1-001",
        "secondary_next_phase": "Phase-Midplatform-Module-Adapter-Feedback-Mount-Planning-v1-001",
        "deferred": [
            "Output Gate Mount",
            "WorldModel-Memory Bridge Mount",
            "Decision Center Loopback Review",
        ],
        "rationale": list(ROUTE_RATIONALE),
        **meta,
    }
    planning_pass = len(issues) == 0
    readiness_decision = {
        "decision_id": "health_watchdog_foundation_handoff_readiness_decision_v1",
        "planning_pass": planning_pass,
        "foundation_frozen": planning_pass,
        "final_decision": FINAL_DECISION_GO if planning_pass else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if planning_pass else NEXT_PHASE_HOLD,
        "blocker_count": len(issues),
        **meta,
    }
    summary = {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "planning_pass": planning_pass,
        "blocker_count": len(issues),
        "violations": issues,
        "final_decision": readiness_decision["final_decision"],
        "recommended_next_phase": readiness_decision["recommended_next_phase"],
        "recommended_route_primary_next_phase": route_decision["primary_next_phase"],
        "recommended_route_secondary_next_phase": route_decision["secondary_next_phase"],
        **meta,
    }
    return {
        "summary": summary,
        "health_watchdog_foundation_handoff_scope": handoff_scope,
        "health_watchdog_foundation_version_tag": version_tag,
        "health_watchdog_frozen_type_interface": frozen_type_interface,
        "health_watchdog_frozen_function_interface": frozen_function_interface,
        "health_watchdog_frozen_validator_interface": frozen_validator_interface,
        "health_watchdog_handoff_contract": handoff_contract,
        "health_watchdog_downstream_output_contract": downstream_output_contract,
        "health_watchdog_forbidden_mutation_policy": forbidden_mutation_policy,
        "health_watchdog_change_control_policy": change_control_policy,
        "health_watchdog_boundary_freeze": boundary_freeze,
        "health_watchdog_downstream_readiness_matrix": downstream_readiness_matrix,
        "health_watchdog_non_claims": non_claims,
        "health_watchdog_route_decision": route_decision,
        "health_watchdog_foundation_handoff_readiness_decision": readiness_decision,
    }
