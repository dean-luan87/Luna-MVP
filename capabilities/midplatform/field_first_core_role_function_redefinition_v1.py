# -*- coding: utf-8 -*-
"""Field-First Core Role Function Redefinition v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.midplatform.field_first_core_recalibration_and_next_work_definition_v1 import (
    DEFAULT_OUTPUT as DEFAULT_FIELD_FIRST_RECAL_ROOT,
    FINAL_DECISION_GO as FIELD_FIRST_RECAL_FINAL_GO,
)
from capabilities.midplatform.field_first_core_role_function_redefinition_items_v1 import (
    CLOSED_LOOP_CHAIN,
    CORE_ROLES,
    DO_NOT_MISCLASSIFY,
    DRIVE_LAYER_ROLES,
    NEXT_PHASE_FINAL_DECISION_TARGET,
    PRIOR_WORK_REPOSITIONING,
    ROLE_MAIN_CHAIN,
    ROLE_PRINCIPLES,
    ROLE_PRIORITY,
    ROLE_SEPARATION_RULES,
    SELECTED_NEXT_PHASE,
    SELECTED_NEXT_ROUTE,
    SUPPORT_ROLES,
    WORK_MANUAL_OUTPUTS,
)
from capabilities.midplatform.field_first_core_role_function_redefinition_lineage_v1 import (
    FIELD_FIRST_ROLE_REDEF_STAGE_ADDITIONS,
    FIELD_FIRST_ROLE_REDEF_STAGE_TERM_OVERRIDES,
    FIELD_FIRST_ROLE_REDEF_WHITELIST_FILES,
)
from capabilities.midplatform.file_size_governance_v1 import build_file_size_governance_review
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

PHASE_ID = "Phase-Midplatform-Field-First-Core-Role-Function-Redefinition-v1-001"
SCOPE = "field_first_core_role_function_redefinition_only"
SOURCE_CHAIN = "field_first_core_role_function_redefinition_v1"
FINAL_DECISION_GO = "MIDPLATFORM_FIELD_FIRST_CORE_ROLE_FUNCTION_REDEFINITION_READY_FOR_FIELD_FIRST_CORE_WORK_MANUAL_AND_ARCHITECTURE_DEFINITION"
FINAL_DECISION_UPSTREAM = "MIDPLATFORM_FIELD_FIRST_CORE_ROLE_FUNCTION_REDEFINITION_BLOCKED_BY_PRIOR_GAP"
FINAL_DECISION_RECAL = "MIDPLATFORM_FIELD_FIRST_CORE_ROLE_FUNCTION_REDEFINITION_BLOCKED_BY_REDEFINITION_GAP"
NEXT_PHASE_HOLD = "Phase-Midplatform-Field-First-Core-Role-Function-Redefinition-Issue-Review-v1-001"
DEFAULT_OUTPUT = "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/field_first_core_role_function_redefinition_v1_smoke_v0"
GO_NO_GO_PACK = "docs/architecture/evaluation/LUNA_EVALUATION_FIELD_FIRST_CORE_ROLE_FUNCTION_REDEFINITION_V1_GO_NO_GO_PACK_V0.md"
TEMPLATE_LINEAGE_MODULE_PATH = "capabilities/midplatform/field_first_core_role_function_redefinition_lineage_v1.py"
MIDPLATFORM_OVERALL_STATUS = "construction_consolidation"

PHASE_PYTHON_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/field_first_core_role_function_redefinition_v1.py",
    "capabilities/midplatform/field_first_core_role_function_redefinition_items_v1.py",
    "capabilities/midplatform/field_first_core_role_function_redefinition_lineage_v1.py",
    "tools/evaluation/midplatform/run_field_first_core_role_function_redefinition_v1.py",
    "tools/evaluation/midplatform/verify_field_first_core_role_function_redefinition_v1.py",
)

GO_CONDITIONS_KEYS: Tuple[str, ...] = (
    "prior_field_first_recal_go",
    "role_principles_defined",
    "core_roles_defined",
    "drive_roles_defined",
    "support_roles_defined",
    "role_main_chain_defined",
    "role_priority_defined",
    "role_separation_complete",
    "prior_work_repositioning_complete",
    "peripheral_roles_deferred",
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
        "field_first_core_role_function_redefinition_only": True,
        "midplatform_overall_status": MIDPLATFORM_OVERALL_STATUS,
        "foundation_consolidation_not_final_midplatform_completion": True,
        "no_fragmentary_phase_expansion": True,
        "integration_test_executed": False,
        "output_root": str(out), "field_first_recal_root": str(upstream),
    }


def run_field_first_core_role_function_redefinition_v1(
    *,
    field_first_recal_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    out = Path(output_root or DEFAULT_OUTPUT).expanduser().resolve()
    upstream = Path(field_first_recal_root).expanduser().resolve()
    repo_root = Path(__file__).resolve().parents[2]
    meta = _meta(out, upstream)
    issues: List[str] = []

    recal_s = _read_json(upstream / "summary.json")
    recal_v = _read_json(upstream / "verifier_report.json")
    recal_fs = _read_json(upstream / "file_size_governance_review_v1.json")

    prior_field_first_recal_go = (
        recal_s.get("final_decision") == FIELD_FIRST_RECAL_FINAL_GO
        and recal_v.get("verifier") == "GO"
        and int(recal_v.get("passed_checks", 0)) >= 340
        and recal_s.get("field_first_core_recalibration_pass") is True
    )
    if not prior_field_first_recal_go:
        issues.append("field_first_recal_not_go")

    absence = {k: recal_s.get(k) is True for k in ABSENCE_KEYS}
    non_execution_boundary_ok = prior_field_first_recal_go and recal_s.get("non_execution_boundary_ok") is True and all(absence.values())
    if not non_execution_boundary_ok:
        issues.append("non_execution_boundary_gap")

    role_principles_defined = bool(ROLE_PRINCIPLES.get("rules"))
    core_roles_defined = len(CORE_ROLES) >= 7
    drive_roles_defined = len(DRIVE_LAYER_ROLES) >= 3
    support_roles_defined = len(SUPPORT_ROLES) >= 5
    role_main_chain_defined = len(ROLE_MAIN_CHAIN) >= 10
    role_priority_defined = len(ROLE_PRIORITY.get("P0_must_define") or []) >= 6
    role_separation_complete = len(ROLE_SEPARATION_RULES) >= 8
    prior_work_repositioning_complete = len(PRIOR_WORK_REPOSITIONING) >= 5
    p3_roles = [r for r in SUPPORT_ROLES if r.get("priority", "").startswith("P3")]
    peripheral_roles_deferred = all(r.get("status", "").startswith("defer") for r in p3_roles)

    principles = {**ROLE_PRINCIPLES, "role_principles_defined": role_principles_defined, **meta}
    separation = {"rules_id": "role_separation_rules_v1", "role_separation_complete": role_separation_complete, "rules": list(ROLE_SEPARATION_RULES), **meta}
    core = {"register_id": "core_roles_register_v1", "core_roles_defined": core_roles_defined, "count": len(CORE_ROLES), "roles": list(CORE_ROLES), **meta}
    drive = {"register_id": "drive_layer_roles_register_v1", "drive_roles_defined": drive_roles_defined, "count": len(DRIVE_LAYER_ROLES), "roles": list(DRIVE_LAYER_ROLES), **meta}
    support = {"register_id": "support_roles_register_v1", "support_roles_defined": support_roles_defined, "count": len(SUPPORT_ROLES), "roles": list(SUPPORT_ROLES), **meta}
    main_chain = {"chain_id": "role_main_chain_v1", "role_main_chain_defined": role_main_chain_defined, "main_chain": list(ROLE_MAIN_CHAIN), "closed_loop": list(CLOSED_LOOP_CHAIN), **meta}
    priority = {"register_id": "role_priority_register_v1", "role_priority_defined": role_priority_defined, "priorities": {k: list(v) for k, v in ROLE_PRIORITY.items()}, **meta}
    reposition = {"register_id": "prior_work_repositioning_v1", "prior_work_repositioning_complete": prior_work_repositioning_complete, "assets": list(PRIOR_WORK_REPOSITIONING), **meta}
    work_manual = {"definition_id": "work_manual_outputs_v1", "items": list(WORK_MANUAL_OUTPUTS), "next_phase_final_decision_target": NEXT_PHASE_FINAL_DECISION_TARGET, **meta}
    next_route = {
        "decision_id": "next_route_decision_v1",
        "selected_next_route": SELECTED_NEXT_ROUTE,
        "recommended_next_phase": SELECTED_NEXT_PHASE,
        "next_phase_final_decision_target": NEXT_PHASE_FINAL_DECISION_TARGET,
        "rationale": "Roles defined; next define work manuals and architecture per role",
        **meta,
    }
    misclassify = {"rules_id": "do_not_misclassify_rules_v1", "rules": list(DO_NOT_MISCLASSIFY), **meta}

    redef_pass = (
        prior_field_first_recal_go and role_principles_defined and core_roles_defined
        and drive_roles_defined and support_roles_defined and role_main_chain_defined
        and role_priority_defined and role_separation_complete and prior_work_repositioning_complete
        and peripheral_roles_deferred and non_execution_boundary_ok and len(issues) == 0
    )

    template_lineage = build_template_lineage(
        base_phase="Midplatform-Field-First-Core-Recalibration-and-Next-Work-Definition-v1-001",
        base_capability=FIELD_FIRST_ROLE_REDEF_WHITELIST_FILES[0],
        base_runner=FIELD_FIRST_ROLE_REDEF_WHITELIST_FILES[1],
        base_verifier=FIELD_FIRST_ROLE_REDEF_WHITELIST_FILES[2],
        base_go_no_go_pack=GO_NO_GO_PACK,
        stage_phase="Midplatform-Field-First-Core-Role-Function-Redefinition-v1-001",
        stage_term_overrides=FIELD_FIRST_ROLE_REDEF_STAGE_TERM_OVERRIDES,
        stage_additions=FIELD_FIRST_ROLE_REDEF_STAGE_ADDITIONS,
        template_files=FIELD_FIRST_ROLE_REDEF_WHITELIST_FILES,
        repo_root=repo_root,
        upstream_review_phase="Midplatform-Field-First-Core-Recalibration-and-Next-Work-Definition-v1-001",
    )
    if not template_lineage.get("template_lineage_ok"):
        issues.append("template_lineage_gap")

    file_size = build_file_size_governance_review(
        phase_id=PHASE_ID, scope_paths=list(PHASE_PYTHON_FILES), repo_root=repo_root,
        phase_python_paths=PHASE_PYTHON_FILES, template_lineage_path=TEMPLATE_LINEAGE_MODULE_PATH,
        read_strategy="summary_index_first", full_repo_scan=False,
        previous_interruption_type=recal_fs.get("previous_interruption_type"),
    )
    fs_ok = file_size.get("file_size_governance_review_ok") is True
    redef_pass = redef_pass and template_lineage.get("template_lineage_ok") and fs_ok and len(issues) == 0
    next_phase = SELECTED_NEXT_PHASE if redef_pass else NEXT_PHASE_HOLD
    final_decision = FINAL_DECISION_GO if redef_pass else (FINAL_DECISION_UPSTREAM if not prior_field_first_recal_go else FINAL_DECISION_RECAL)

    go_values = {
        "prior_field_first_recal_go": prior_field_first_recal_go,
        "role_principles_defined": role_principles_defined,
        "core_roles_defined": core_roles_defined,
        "drive_roles_defined": drive_roles_defined,
        "support_roles_defined": support_roles_defined,
        "role_main_chain_defined": role_main_chain_defined,
        "role_priority_defined": role_priority_defined,
        "role_separation_complete": role_separation_complete,
        "prior_work_repositioning_complete": prior_work_repositioning_complete,
        "peripheral_roles_deferred": peripheral_roles_deferred,
        "field_first_midplatform_core": True,
        "ipc_repositioned_to_source_intake": True,
        "handoff_contract_p3_defer_remains_defer": True,
        "no_runtime_execution": True,
        "no_integration_test": True,
        "no_record_creation": True,
        "no_grant_creation": True,
        "no_authorization_request_creation": True,
        "midplatform_still_has_remaining_work": True,
        "non_execution_boundary_ok": non_execution_boundary_ok,
        "file_size_governance_review_ok": fs_ok,
        "next_phase_readiness_ok": redef_pass,
        "field_first_core_role_function_redefinition_pass": redef_pass,
        "selected_next_route": SELECTED_NEXT_ROUTE,
        "core_role_count": len(CORE_ROLES),
        "drive_role_count": len(DRIVE_LAYER_ROLES),
        "support_role_count": len(SUPPORT_ROLES),
        "full_repo_scan_absent": file_size.get("full_repo_scan_absent") is True,
        "tmp_eval_out_scan_absent": file_size.get("tmp_eval_out_scan_absent") is True,
        "summary_index_first_reading_ok": file_size.get("summary_index_first_reading_ok") is True,
        **absence,
    }
    core_fields = build_core_go_no_go_summary_fields(
        go_conditions={k: go_values[k] for k in GO_CONDITIONS_KEYS},
        forbidden_runtime_flags=RUNTIME_FORBIDDEN_FLAGS,
        chain_trace_nodes=tuple(list(recal_s.get("chain_trace_nodes") or []) + ["field_first_core_role_function_redefinition"]),
        go_no_go_decision=final_decision, final_decision=final_decision, next_phase=next_phase,
        template_lineage=template_lineage,
    )
    summary = {
        "phase": PHASE_ID, "scope": SCOPE, "blocker_count": len(issues), "issues": issues,
        **go_values, **core_fields, "final_decision": final_decision, "recommended_next_phase": next_phase, **meta,
    }
    md = "\n".join([
        "# Field-First Core Role Function Redefinition v1",
        f"Core roles: `{len(CORE_ROLES)}` | Drive: `{len(DRIVE_LAYER_ROLES)}` | Support: `{len(SUPPORT_ROLES)}`",
        f"P0 core: `{len(ROLE_PRIORITY['P0_must_define'])}` | P3 defer: `{len(ROLE_PRIORITY['P3_defer'])}`",
        f"IPC → Source Intake & Normalization Operator",
        f"Final decision: `{final_decision}`",
        f"Next: `{next_phase}`",
    ])
    return {
        "field_first_core_role_function_redefinition_report": {**go_values, "final_decision": final_decision, **meta},
        "field_first_core_role_function_redefinition_report_md": md,
        "role_principles": principles,
        "role_separation_rules": separation,
        "core_roles_register": core,
        "drive_layer_roles_register": drive,
        "support_roles_register": support,
        "role_main_chain": main_chain,
        "role_priority_register": priority,
        "prior_work_repositioning": reposition,
        "work_manual_outputs_definition": work_manual,
        "next_route_decision": next_route,
        "do_not_misclassify_rules": misclassify,
        "file_size_governance_review": {**file_size, **meta},
        "summary": summary,
    }
