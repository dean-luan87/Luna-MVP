# -*- coding: utf-8 -*-
"""Luna Project Organization Work Manual item definitions v1."""

from __future__ import annotations

from typing import Any, Dict, Tuple

PROJECT_WORK_MODE_PRINCIPLES: Tuple[Dict[str, Any], ...] = (
    {"principle_id": "organization_work_manual_first", "name": "Organization / Work Manual First", "summary": "Define organization and work manual before engineering implementation"},
    {"principle_id": "core_work_first", "name": "Core Work First", "summary": "Core capability drives route; peripheral rules serve core"},
    {"principle_id": "role_job_definition_first", "name": "Role / Job Definition First", "summary": "Define who, what work, intake, judgment, delivery, refuse, handoff, escalate, proof"},
    {"principle_id": "workflow_before_protocol", "name": "Workflow Before Protocol", "summary": "Workflow first; protocol is handoff transparency tool not premature wall"},
    {"principle_id": "judge_referee_definition", "name": "Judge / Referee Definition", "summary": "Define who judges correctness, ownership, overreach, overload, omission"},
    {"principle_id": "peripheral_rules_serve_core", "name": "Peripheral Rules Serve Core", "summary": "Modify ordinary rules before weakening core; only safety/auth/privacy hard-constrain"},
    {"principle_id": "strongly_coupled_single_package", "name": "Strongly-Coupled Work Single-Package", "summary": "Coupled small modules complete in one package; files split by responsibility"},
    {"principle_id": "workload_control", "name": "Workload Control", "summary": "Input scope, caps, queue, refuse, defer, handoff, degrade, close rules"},
    {"principle_id": "qualification_evaluation", "name": "Qualification / Evaluation", "summary": "Role, module, org qualification; core work, safety, transparency, traceability"},
    {"principle_id": "future_expansion_reservation", "name": "Future Expansion Reservation", "summary": "Reserve future roles, capabilities, upstream/downstream, runtime, distributed, brain hooks"},
)

STANDARD_WORK_MANUAL_SECTIONS: Tuple[str, ...] = (
    "organization_context",
    "core_work_definition",
    "role_job_definition",
    "work_detail",
    "internal_workflow",
    "external_workflow",
    "judge_referee_rules",
    "governance_protocol_boundary_service_rules",
    "workload_control",
    "qualification_standard",
    "future_expansion",
)

MIDPLATFORM_ORGANIZATION_MANUAL: Dict[str, Any] = {
    "manual_id": "midplatform_organization_manual_v1",
    "organization": "Luna Midplatform",
    "mission": "Process information into governed candidates, coordinate module collaboration, maintain traceability without runtime execution",
    "current_stage": "construction_consolidation_work_manual_alignment",
    "primary_core_work": "Information Processing Core",
    "secondary_core_work": ("Candidate Processing Core", "Orchestration Decision Core"),
    "roles_defined": ("information_processing_core", "candidate_lifecycle_manager", "core_orchestration", "boundary_registry_support", "alignment_support", "governance_referee"),
    "judge_roles": ("module_dryrun_verifier", "static_validator", "non_execution_guard", "governance_constraints"),
    "workload_policy": "candidate_only_non_execution_bounded",
    "qualification_policy": "module_level_controlled_dryrun_before_integration",
}

def _artifact(
    artifact_id: str,
    status: str,
    section: str,
    *,
    core: bool = False,
    support: bool = False,
    peripheral: bool = False,
    governance: bool = False,
    protocol: bool = False,
    boundary: bool = False,
    judge: bool = False,
    workflow: bool = False,
    future: bool = False,
    missing_manual: bool = False,
    overbuild: str = "low",
    keep: bool = True,
    reframe: bool = False,
    defer: bool = False,
    next_action: str = "map_to_work_manual",
) -> Dict[str, Any]:
    return {
        "artifact_id": artifact_id,
        "current_status": status,
        "belongs_to_work_manual_section": section,
        "is_core_work": core,
        "is_core_support": support,
        "is_peripheral_rule": peripheral,
        "is_governance": governance,
        "is_protocol": protocol,
        "is_boundary": boundary,
        "is_judge_rule": judge,
        "is_workflow": workflow,
        "is_future_expansion": future,
        "missing_manual_definition": missing_manual,
        "overbuild_risk": overbuild,
        "should_keep": keep,
        "should_reframe": reframe,
        "should_defer": defer,
        "next_action": next_action,
    }


EXISTING_ARTIFACT_MAPPINGS: Tuple[Dict[str, Any], ...] = (
    _artifact("foundation_handoff", "go", "organization_context", governance=True, workflow=True),
    _artifact("final_closure", "go", "organization_context", governance=True),
    _artifact("freeze_authorization", "go", "governance_protocol_boundary_service_rules", governance=True, protocol=True),
    _artifact("broader_midplatform_remaining_work_roadmap", "go", "organization_context", workflow=True),
    _artifact("foundation_closure_consolidation", "go", "organization_context", governance=True),
    _artifact("owner_approval_request_subchain", "closed_go", "governance_protocol_boundary_service_rules", governance=True, peripheral=True, missing_manual=True, reframe=True, next_action="keep_as_closed_governance_reference"),
    _artifact("module_boundary_registry_planning", "go", "governance_protocol_boundary_service_rules", boundary=True, support=True),
    _artifact("candidate_lifecycle_unification_planning", "go", "internal_workflow", workflow=True, support=True, missing_manual=True, next_action="write_lifecycle_manager_work_manual"),
    _artifact("evidence_record_approval_permission_alignment_planning", "go", "governance_protocol_boundary_service_rules", support=True, governance=True),
    _artifact("task_manager_core_orchestration_skeleton_consolidation", "go", "core_work_definition", core=True, workflow=True),
    _artifact("task_manager_core_orchestration_implementation_planning", "go", "work_detail", core=True, support=True),
    _artifact("task_manager_core_orchestration_controlled_skeleton_implementation", "go", "role_job_definition", core=True, workflow=True),
    _artifact("task_manager_core_orchestration_module_level_controlled_dryrun", "go", "qualification_standard", core=True, judge=True),
    _artifact("module_integration_gap_consolidation", "go", "organization_context", workflow=True, peripheral=True, overbuild="medium", reframe=True, next_action="superseded_by_work_manual_mapping"),
    _artifact("core_capability_peripheral_service_recalibration", "go", "organization_context", core=True, workflow=True, next_action="inform_work_manual_definition"),
    _artifact("module_handoff_contract_gap", "identified_not_implemented", "external_workflow", peripheral=True, missing_manual=True, overbuild="high", defer=True, next_action="defer_until_core_work_manuals_ready"),
    _artifact("information_processing_core", "not_implemented", "core_work_definition", core=True, missing_manual=True, next_action="write_work_manual_before_implementation"),
    _artifact("candidate_lifecycle_manager", "not_implemented", "role_job_definition", core=True, missing_manual=True, next_action="write_work_manual_before_implementation"),
)

MISSING_WORK_MANUAL_GAPS: Tuple[Dict[str, Any], ...] = (
    {"gap_id": "organization_mission_not_formalized_in_manual", "priority": "P1", "blocker_now": True},
    {"gap_id": "midplatform_role_job_manuals_missing", "priority": "P1", "blocker_now": True},
    {"gap_id": "information_processing_core_work_manual_missing", "priority": "P1", "blocker_now": True},
    {"gap_id": "candidate_lifecycle_manager_work_manual_missing", "priority": "P1", "blocker_now": True},
    {"gap_id": "internal_workflow_manual_incomplete", "priority": "P2", "blocker_now": False},
    {"gap_id": "external_workflow_manual_incomplete", "priority": "P2", "blocker_now": False},
    {"gap_id": "judge_referee_manual_incomplete", "priority": "P2", "blocker_now": False},
    {"gap_id": "workload_control_manual_incomplete", "priority": "P2", "blocker_now": False},
    {"gap_id": "qualification_standard_manual_incomplete", "priority": "P2", "blocker_now": False},
    {"gap_id": "peripheral_rules_premature_hardening_risk", "priority": "P2", "blocker_now": False},
    {"gap_id": "protocol_constitution_boundary_misclassified_as_core_risk", "priority": "P2", "blocker_now": False},
    {"gap_id": "module_lego_fragmentation_risk", "priority": "P3", "blocker_now": False},
    {"gap_id": "existing_artifacts_need_reclassification_as_core_serving_peripheral", "priority": "P2", "blocker_now": False},
)

OVERBUILD_RISK_REVIEW: Tuple[Dict[str, Any], ...] = (
    {"risk_id": "handoff_contract_p1_auto_route", "severity": "high", "mitigation": "recalibrated_to_p3_work_manual_first", "status": "mitigated"},
    {"risk_id": "gap_consolidation_peripheral_priority", "severity": "medium", "mitigation": "work_manual_mapping_reframe", "status": "mitigated"},
    {"risk_id": "protocol_before_workflow", "severity": "medium", "mitigation": "workflow_before_protocol_principle", "status": "open_monitor"},
    {"risk_id": "governance_gate_over_core", "severity": "medium", "mitigation": "peripheral_rules_serve_core", "status": "open_monitor"},
    {"risk_id": "fragmentary_subphases", "severity": "low", "mitigation": "single_package_rule", "status": "mitigated"},
)

NEXT_WORK_GOVERNANCE_RULES: Tuple[str, ...] = (
    "new_feature_requires_work_manual_before_implementation",
    "work_manual_must_define_core_work_first",
    "module_must_define_role_upstream_downstream_internal_external_flow",
    "protocol_boundary_governance_must_declare_core_served",
    "peripheral_rule_must_declare_no_reverse_constraint_on_core",
    "strongly_coupled_module_single_package_completion",
    "go_does_not_auto_follow_recommended_phase_without_core_service_check",
    "each_phase_must_declare_core_core_support_peripheral_judge_governance_future",
    "each_phase_must_have_workload_control_and_qualification_standard",
    "each_phase_must_reserve_future_expansion",
)

SELECTED_NEXT_PHASE = "Phase-Midplatform-Information-Processing-Core-Work-Manual-Definition-v1-001"
SELECTED_NEXT_ROUTE = "Information Processing Core Work Manual Definition"
DEFERRED_ROUTE = "Phase-Midplatform-Information-Processing-Core-Controlled-Implementation-v1-001"
DEFER_REASON = "Information Processing Core work manual not yet defined; role/job/workflow/judge not ready"
