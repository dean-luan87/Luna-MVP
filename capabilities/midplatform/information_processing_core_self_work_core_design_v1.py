# -*- coding: utf-8 -*-
"""Information Processing Core Self-Work Core Design v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.midplatform.file_size_governance_v1 import build_file_size_governance_review
from capabilities.midplatform.information_processing_core_controlled_implementation_v1 import (
    DEFAULT_OUTPUT as DEFAULT_IPC_IMPL_ROOT,
    FINAL_DECISION_GO as IPC_IMPL_FINAL_GO,
)
from capabilities.midplatform.information_processing_core_self_work_core_design_items_v1 import (
    CONCLUSION_REQUIRED_FIELDS,
    CONCLUSION_TYPES,
    CURRENT_NON_GOALS,
    DESIGN_PRINCIPLES,
    DOWNSTREAM_NEED_OBSERVATIONS,
    INTERNAL_PROCESSING_FLOW,
    INFORMATION_TYPES,
    SELECTED_NEXT_PHASE,
    SELECTED_NEXT_ROUTE,
    SELF_CHECK_REFEREE_RULES,
    SELF_WORK_SCOPE,
    THREE_PART_WORK_MODEL,
    TRANSPARENCY_FIELDS,
    UPSTREAM_MINIMUM_ASSUMPTIONS,
    WORKLOAD_CONTROL_RULES,
)
from capabilities.midplatform.information_processing_core_self_work_core_design_lineage_v1 import (
    IPC_SELF_WORK_DESIGN_STAGE_ADDITIONS,
    IPC_SELF_WORK_DESIGN_STAGE_TERM_OVERRIDES,
    IPC_SELF_WORK_DESIGN_WHITELIST_FILES,
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

PHASE_ID = "Phase-Midplatform-Information-Processing-Core-Self-Work-Core-Design-v1-001"
SCOPE = "information_processing_core_self_work_core_design_only"
SOURCE_CHAIN = "information_processing_core_self_work_core_design_v1"
FINAL_DECISION_GO = "MIDPLATFORM_INFORMATION_PROCESSING_CORE_SELF_WORK_CORE_DESIGN_READY_FOR_SELF_WORK_CORE_CAPABILITY_DRYRUN"
FINAL_DECISION_UPSTREAM = "MIDPLATFORM_INFORMATION_PROCESSING_CORE_SELF_WORK_CORE_DESIGN_BLOCKED_BY_IMPLEMENTATION_GAP"
FINAL_DECISION_DESIGN = "MIDPLATFORM_INFORMATION_PROCESSING_CORE_SELF_WORK_CORE_DESIGN_BLOCKED_BY_DESIGN_GAP"
NEXT_PHASE_HOLD = "Phase-Midplatform-Information-Processing-Core-Self-Work-Core-Design-Issue-Review-v1-001"
DEFAULT_OUTPUT = "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/information_processing_core_self_work_core_design_v1_smoke_v0"
GO_NO_GO_PACK = "docs/architecture/evaluation/LUNA_EVALUATION_INFORMATION_PROCESSING_CORE_SELF_WORK_CORE_DESIGN_V1_GO_NO_GO_PACK_V0.md"
TEMPLATE_LINEAGE_MODULE_PATH = "capabilities/midplatform/information_processing_core_self_work_core_design_lineage_v1.py"
MIDPLATFORM_OVERALL_STATUS = "construction_consolidation"

PHASE_PYTHON_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/information_processing_core_self_work_core_design_v1.py",
    "capabilities/midplatform/information_processing_core_self_work_core_design_items_v1.py",
    "capabilities/midplatform/information_processing_core_self_work_core_design_lineage_v1.py",
    "tools/evaluation/midplatform/run_information_processing_core_self_work_core_design_v1.py",
    "tools/evaluation/midplatform/verify_information_processing_core_self_work_core_design_v1.py",
)

GO_CONDITIONS_KEYS: Tuple[str, ...] = (
    "prior_ipc_controlled_implementation_go",
    "ipc_self_work_scope_complete",
    "ipc_internal_processing_flow_complete",
    "ipc_conclusion_model_complete",
    "ipc_transparency_traceability_model_complete",
    "ipc_self_check_referee_model_complete",
    "ipc_workload_control_model_complete",
    "downstream_need_observation_model_complete",
    "upstream_minimum_assumption_register_complete",
    "self_work_first",
    "downstream_contract_not_defined_yet",
    "ipc_internal_processing_defined",
    "non_execution_boundary_ok",
    "file_size_governance_review_ok",
    "next_phase_readiness_ok",
)


def _read_json(path: Path) -> Dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}
    except (json.JSONDecodeError, OSError):
        return {}


def _meta(out: Path, upstream: Path) -> Dict[str, Any]:
    return {
        "phase": PHASE_ID, "scope": SCOPE, "source_chain": SOURCE_CHAIN,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "foundation_id": "midplatform_task_manager_foundation_v1",
        "runtime_status": "not_enabled",
        "information_processing_core_self_work_core_design_only": True,
        "midplatform_overall_status": MIDPLATFORM_OVERALL_STATUS,
        "foundation_consolidation_not_final_midplatform_completion": True,
        "no_fragmentary_phase_expansion": True,
        "integration_test_executed": False,
        "output_root": str(out), "ipc_implementation_root": str(upstream),
    }


def run_information_processing_core_self_work_core_design_v1(
    *,
    ipc_implementation_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    out = Path(output_root or DEFAULT_OUTPUT).expanduser().resolve()
    upstream = Path(ipc_implementation_root).expanduser().resolve()
    repo_root = Path(__file__).resolve().parents[2]
    meta = _meta(out, upstream)
    issues: List[str] = []

    impl_s = _read_json(upstream / "summary.json")
    impl_v = _read_json(upstream / "verifier_report.json")
    impl_fs = _read_json(upstream / "file_size_governance_review_v1.json")

    prior_ipc_controlled_implementation_go = (
        impl_s.get("final_decision") == IPC_IMPL_FINAL_GO
        and impl_v.get("verifier") == "GO"
        and int(impl_v.get("passed_checks", 0)) >= 420
        and impl_s.get("information_processing_core_controlled_implementation_pass") is True
    )
    if not prior_ipc_controlled_implementation_go:
        issues.append("ipc_implementation_not_go")

    absence = {k: impl_s.get(k) is True for k in ABSENCE_KEYS}
    non_execution_boundary_ok = prior_ipc_controlled_implementation_go and impl_s.get("non_execution_boundary_ok") is True and all(absence.values())
    if not non_execution_boundary_ok:
        issues.append("non_execution_boundary_gap")

    ipc_self_work_scope_complete = len(SELF_WORK_SCOPE.get("responsibilities") or ()) >= 10
    ipc_internal_processing_flow_complete = len(INTERNAL_PROCESSING_FLOW) >= 12
    ipc_conclusion_model_complete = len(CONCLUSION_TYPES) >= 11
    ipc_transparency_traceability_model_complete = len(TRANSPARENCY_FIELDS) >= 14
    ipc_self_check_referee_model_complete = len(SELF_CHECK_REFEREE_RULES) >= 10
    ipc_workload_control_model_complete = len(WORKLOAD_CONTROL_RULES) >= 8
    downstream_need_observation_model_complete = len(DOWNSTREAM_NEED_OBSERVATIONS) >= 6
    upstream_minimum_assumption_register_complete = len(UPSTREAM_MINIMUM_ASSUMPTIONS) >= 6
    ipc_internal_processing_defined = ipc_internal_processing_flow_complete and ipc_conclusion_model_complete

    three_part = {**THREE_PART_WORK_MODEL, **meta}
    self_scope = {**SELF_WORK_SCOPE, "ipc_self_work_scope_complete": ipc_self_work_scope_complete, **meta}
    internal_flow = {
        "flow_id": "ipc_internal_processing_flow_v1",
        "ipc_internal_processing_flow_complete": ipc_internal_processing_flow_complete,
        "step_count": len(INTERNAL_PROCESSING_FLOW),
        "steps": list(INTERNAL_PROCESSING_FLOW),
        "information_types": list(INFORMATION_TYPES),
        **meta,
    }
    conclusion_model = {
        "model_id": "ipc_conclusion_model_v1",
        "ipc_conclusion_model_complete": ipc_conclusion_model_complete,
        "conclusion_types": list(CONCLUSION_TYPES),
        "required_fields": list(CONCLUSION_REQUIRED_FIELDS),
        **meta,
    }
    transparency = {
        "model_id": "ipc_transparency_traceability_model_v1",
        "ipc_transparency_traceability_model_complete": ipc_transparency_traceability_model_complete,
        "fields": list(TRANSPARENCY_FIELDS),
        "no_black_box_conclusions": True,
        **meta,
    }
    self_referee = {
        "model_id": "ipc_self_check_referee_model_v1",
        "ipc_self_check_referee_model_complete": ipc_self_check_referee_model_complete,
        "checks": list(SELF_CHECK_REFEREE_RULES),
        **meta,
    }
    workload = {
        "model_id": "ipc_workload_control_model_v1",
        "ipc_workload_control_model_complete": ipc_workload_control_model_complete,
        "rules": list(WORKLOAD_CONTROL_RULES),
        **meta,
    }
    downstream_obs = {
        "model_id": "downstream_need_observation_model_v1",
        "downstream_need_observation_model_complete": downstream_need_observation_model_complete,
        "downstream_needs_observed_not_contracted": True,
        "downstream_contract_not_defined_yet": True,
        "observations": list(DOWNSTREAM_NEED_OBSERVATIONS),
        **meta,
    }
    upstream_reg = {
        "register_id": "upstream_minimum_assumption_register_v1",
        "upstream_minimum_assumption_register_complete": upstream_minimum_assumption_register_complete,
        "upstream_protocol_not_rewritten_yet": True,
        "assumptions": list(UPSTREAM_MINIMUM_ASSUMPTIONS),
        **meta,
    }
    non_goals = {
        "register_id": "current_non_goals_v1",
        "non_goals": list(CURRENT_NON_GOALS),
        "handoff_contract_p3_defer_remains_defer": True,
        **meta,
    }
    next_route = {
        "decision_id": "next_route_decision_v1",
        "selected_next_route": SELECTED_NEXT_ROUTE,
        "recommended_next_phase": SELECTED_NEXT_PHASE,
        "rationale": "Self-work core design complete; validate via lightweight self-work dryrun",
        **meta,
    }

    design_pass = (
        prior_ipc_controlled_implementation_go and ipc_self_work_scope_complete
        and ipc_internal_processing_flow_complete and ipc_conclusion_model_complete
        and ipc_transparency_traceability_model_complete and ipc_self_check_referee_model_complete
        and ipc_workload_control_model_complete and downstream_need_observation_model_complete
        and upstream_minimum_assumption_register_complete and ipc_internal_processing_defined
        and non_execution_boundary_ok and len(issues) == 0
    )

    template_lineage = build_template_lineage(
        base_phase="Midplatform-Information-Processing-Core-Controlled-Implementation-v1-001",
        base_capability=IPC_SELF_WORK_DESIGN_WHITELIST_FILES[0],
        base_runner=IPC_SELF_WORK_DESIGN_WHITELIST_FILES[1],
        base_verifier=IPC_SELF_WORK_DESIGN_WHITELIST_FILES[2],
        base_go_no_go_pack=GO_NO_GO_PACK,
        stage_phase="Midplatform-Information-Processing-Core-Self-Work-Core-Design-v1-001",
        stage_term_overrides=IPC_SELF_WORK_DESIGN_STAGE_TERM_OVERRIDES,
        stage_additions=IPC_SELF_WORK_DESIGN_STAGE_ADDITIONS,
        template_files=IPC_SELF_WORK_DESIGN_WHITELIST_FILES,
        repo_root=repo_root,
        upstream_review_phase="Midplatform-Information-Processing-Core-Controlled-Implementation-v1-001",
    )
    if not template_lineage.get("template_lineage_ok"):
        issues.append("template_lineage_gap")

    file_size = build_file_size_governance_review(
        phase_id=PHASE_ID, scope_paths=list(PHASE_PYTHON_FILES), repo_root=repo_root,
        phase_python_paths=PHASE_PYTHON_FILES, template_lineage_path=TEMPLATE_LINEAGE_MODULE_PATH,
        read_strategy="summary_index_first", full_repo_scan=False,
        previous_interruption_type=impl_fs.get("previous_interruption_type"),
    )
    fs_ok = file_size.get("file_size_governance_review_ok") is True
    design_pass = design_pass and template_lineage.get("template_lineage_ok") and fs_ok and len(issues) == 0
    next_phase = SELECTED_NEXT_PHASE if design_pass else NEXT_PHASE_HOLD
    final_decision = FINAL_DECISION_GO if design_pass else (FINAL_DECISION_UPSTREAM if not prior_ipc_controlled_implementation_go else FINAL_DECISION_DESIGN)

    go_values = {
        "prior_ipc_controlled_implementation_go": prior_ipc_controlled_implementation_go,
        "ipc_self_work_scope_complete": ipc_self_work_scope_complete,
        "ipc_internal_processing_flow_complete": ipc_internal_processing_flow_complete,
        "ipc_conclusion_model_complete": ipc_conclusion_model_complete,
        "ipc_transparency_traceability_model_complete": ipc_transparency_traceability_model_complete,
        "ipc_self_check_referee_model_complete": ipc_self_check_referee_model_complete,
        "ipc_workload_control_model_complete": ipc_workload_control_model_complete,
        "downstream_need_observation_model_complete": downstream_need_observation_model_complete,
        "upstream_minimum_assumption_register_complete": upstream_minimum_assumption_register_complete,
        "self_work_first": True,
        "downstream_contract_not_defined_yet": True,
        "upstream_protocol_not_rewritten_yet": True,
        "ipc_internal_processing_defined": ipc_internal_processing_defined,
        "downstream_needs_observed_not_contracted": True,
        "peripheral_contract_does_not_constrain_core": True,
        "handoff_contract_p3_defer_remains_defer": True,
        "no_runtime_execution": True,
        "no_integration_test": True,
        "no_record_creation": True,
        "no_grant_creation": True,
        "no_authorization_request_creation": True,
        "midplatform_still_has_remaining_work": True,
        "non_execution_boundary_ok": non_execution_boundary_ok,
        "file_size_governance_review_ok": fs_ok,
        "next_phase_readiness_ok": design_pass,
        "information_processing_core_self_work_core_design_pass": design_pass,
        "selected_next_route": SELECTED_NEXT_ROUTE,
        "full_repo_scan_absent": file_size.get("full_repo_scan_absent") is True,
        "tmp_eval_out_scan_absent": file_size.get("tmp_eval_out_scan_absent") is True,
        "summary_index_first_reading_ok": file_size.get("summary_index_first_reading_ok") is True,
        **absence,
    }
    core_fields = build_core_go_no_go_summary_fields(
        go_conditions={k: go_values[k] for k in GO_CONDITIONS_KEYS},
        forbidden_runtime_flags=RUNTIME_FORBIDDEN_FLAGS,
        chain_trace_nodes=tuple(list(impl_s.get("chain_trace_nodes") or []) + ["ipc_self_work_core_design"]),
        go_no_go_decision=final_decision, final_decision=final_decision, next_phase=next_phase,
        template_lineage=template_lineage,
    )
    summary = {
        "phase": PHASE_ID, "scope": SCOPE, "blocker_count": len(issues), "issues": issues,
        **go_values, **core_fields, "final_decision": final_decision, "recommended_next_phase": next_phase, **meta,
    }
    md = "\n".join([
        "# IPC Self-Work Core Design v1",
        f"Principles: `{len(DESIGN_PRINCIPLES)}` | Flow steps: `{len(INTERNAL_PROCESSING_FLOW)}`",
        f"Conclusion types: `{len(CONCLUSION_TYPES)}` | Self-check rules: `{len(SELF_CHECK_REFEREE_RULES)}`",
        f"Self-work first: `True` | Downstream contract: `not defined`",
        f"Final decision: `{final_decision}`",
    ])
    return {
        "ipc_self_work_core_design_report": {**go_values, "design_principles": list(DESIGN_PRINCIPLES), "final_decision": final_decision, **meta},
        "ipc_self_work_core_design_report_md": md,
        "three_part_work_model_positioning": three_part,
        "ipc_self_work_scope": self_scope,
        "ipc_internal_processing_flow": internal_flow,
        "ipc_conclusion_model": conclusion_model,
        "ipc_transparency_traceability_model": transparency,
        "ipc_self_check_referee_model": self_referee,
        "ipc_workload_control_model": workload,
        "downstream_need_observation_model": downstream_obs,
        "upstream_minimum_assumption_register": upstream_reg,
        "current_non_goals": non_goals,
        "next_route_decision": next_route,
        "file_size_governance_review": {**file_size, **meta},
        "summary": summary,
    }
