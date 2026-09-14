# -*- coding: utf-8 -*-
"""Luna Midplatform Module Integration Gap Consolidation v1."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.midplatform.file_size_governance_v1 import build_file_size_governance_review
from capabilities.midplatform.module_integration_gap_consolidation_items_v1 import (
    COMPLETED_MODULES,
    DO_NOT_REOPEN_RULES,
    GAP_CLASSIFICATIONS,
    MODULE_CHAIN_READINESS,
    NEXT_MODULE_CANDIDATES,
    NEXT_ROUTE_B,
    NEXT_ROUTE_C,
    NEXT_ROUTE_D,
    NEXT_ROUTE_E,
    REMAINING_GAPS,
    SELECTED_NEXT_MODULE,
    SELECTED_NEXT_ROUTE,
)
from capabilities.midplatform.module_integration_gap_consolidation_lineage_v1 import (
    MODULE_INTEGRATION_GAP_CONSOLIDATION_STAGE_ADDITIONS,
    MODULE_INTEGRATION_GAP_CONSOLIDATION_STAGE_TERM_OVERRIDES,
    MODULE_INTEGRATION_GAP_CONSOLIDATION_WHITELIST_FILES,
)
from capabilities.midplatform.task_manager_core_orchestration_module_level_controlled_dryrun_v1 import (
    DEFAULT_OUTPUT as DEFAULT_MODULE_DRYRUN_ROOT,
    FINAL_DECISION_GO as MODULE_DRYRUN_FINAL_GO,
    NEXT_PHASE_GO as MODULE_DRYRUN_NEXT_PHASE,
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

PHASE_ID = "Phase-Midplatform-Module-Integration-Gap-Consolidation-v1-001"
SCOPE = "midplatform_module_integration_gap_consolidation_only"
SOURCE_CHAIN = "module_integration_gap_consolidation_v1"
FINAL_DECISION_GO = "MIDPLATFORM_MODULE_INTEGRATION_GAP_CONSOLIDATION_READY_FOR_MODULE_HANDOFF_CONTRACT_CONTROLLED_IMPLEMENTATION"
FINAL_DECISION_UPSTREAM = "MIDPLATFORM_MODULE_INTEGRATION_GAP_CONSOLIDATION_BLOCKED_BY_MODULE_DRYRUN_GAP"
FINAL_DECISION_CONSOLIDATION = "MIDPLATFORM_MODULE_INTEGRATION_GAP_CONSOLIDATION_BLOCKED_BY_CONSOLIDATION_GAP"
FINAL_DECISION_ABSENCE = "MIDPLATFORM_MODULE_INTEGRATION_GAP_CONSOLIDATION_BLOCKED_BY_ABSENCE_DRIFT"
FINAL_DECISION_RUNTIME = "MIDPLATFORM_MODULE_INTEGRATION_GAP_CONSOLIDATION_BLOCKED_BY_RUNTIME_SCOPE_LEAKAGE"
FINAL_DECISION_LINEAGE = "MIDPLATFORM_MODULE_INTEGRATION_GAP_CONSOLIDATION_BLOCKED_BY_TEMPLATE_LINEAGE_GAP"
NEXT_PHASE_GO = SELECTED_NEXT_ROUTE
NEXT_PHASE_HOLD = "Phase-Midplatform-Module-Integration-Gap-Consolidation-Issue-Review-v1-001"
DEFAULT_OUTPUT = "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/module_integration_gap_consolidation_v1_smoke_v0"
GO_NO_GO_PACK = "docs/architecture/evaluation/LUNA_EVALUATION_MODULE_INTEGRATION_GAP_CONSOLIDATION_V1_GO_NO_GO_PACK_V0.md"
TEMPLATE_LINEAGE_MODULE_PATH = "capabilities/midplatform/module_integration_gap_consolidation_lineage_v1.py"
MIDPLATFORM_OVERALL_STATUS = "construction_consolidation"

PHASE_PYTHON_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/module_integration_gap_consolidation_v1.py",
    "capabilities/midplatform/module_integration_gap_consolidation_items_v1.py",
    "capabilities/midplatform/module_integration_gap_consolidation_lineage_v1.py",
    "tools/evaluation/midplatform/run_module_integration_gap_consolidation_v1.py",
    "tools/evaluation/midplatform/verify_module_integration_gap_consolidation_v1.py",
)

GO_CONDITIONS_KEYS: Tuple[str, ...] = (
    "prior_core_orchestration_module_dryrun_go",
    "completed_module_inventory_complete",
    "remaining_gap_inventory_complete",
    "gap_classification_matrix_complete",
    "module_chain_readiness_map_complete",
    "next_module_candidate_selection_complete",
    "do_not_reopen_do_not_overbuild_rules_complete",
    "next_route_decision_complete",
    "core_orchestration_not_extended",
    "module_handoff_contract_gap_identified",
    "future_runtime_debt_not_current_blocker",
    "future_design_not_current_blocker",
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
        "module_integration_gap_consolidation_only": True,
        "midplatform_overall_status": MIDPLATFORM_OVERALL_STATUS,
        "foundation_consolidation_not_final_midplatform_completion": True,
        "no_fragmentary_phase_expansion": True,
        "integration_test_executed": False,
        "real_issuance_preauthorization_not_opened": True,
        "output_root": str(out),
        "module_dryrun_root": str(upstream),
    }


def run_module_integration_gap_consolidation_v1(
    *,
    module_dryrun_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    out = Path(output_root or DEFAULT_OUTPUT).expanduser().resolve()
    upstream = Path(module_dryrun_root).expanduser().resolve()
    repo_root = Path(__file__).resolve().parents[2]
    meta = _meta(out, upstream)
    issues: List[str] = []

    dryrun_summary = _read_json(upstream / "summary.json")
    dryrun_verifier = _read_json(upstream / "verifier_report.json")
    dryrun_file_size = _read_json(upstream / "file_size_governance_review_v1.json")

    prior_core_orchestration_module_dryrun_go = (
        dryrun_summary.get("final_decision") == MODULE_DRYRUN_FINAL_GO
        and dryrun_summary.get("recommended_next_phase") == MODULE_DRYRUN_NEXT_PHASE
        and dryrun_verifier.get("verifier") == "GO"
        and int(dryrun_verifier.get("passed_checks", 0)) >= 360
        and dryrun_summary.get("module_level_controlled_dryrun_ok") is True
        and dryrun_summary.get("all_scenarios_passed") is True
        and dryrun_summary.get("real_request_issuance_authorized") is False
    )
    if not prior_core_orchestration_module_dryrun_go:
        issues.append("module_dryrun_not_go")

    absence = {key: dryrun_summary.get(key) is True for key in ABSENCE_KEYS}
    record_creation_absent = dryrun_summary.get("record_creation_absent") is True
    runtime_forbidden_violation = any(dryrun_summary.get(flag) is True for flag in RUNTIME_FORBIDDEN_FLAGS)
    owner_approval_request_chain_not_reopened = dryrun_summary.get("owner_approval_request_chain_not_reopened") is True
    non_execution_boundary_ok = (
        prior_core_orchestration_module_dryrun_go
        and dryrun_summary.get("non_execution_boundary_ok") is True
        and all(absence.values())
        and record_creation_absent
        and not runtime_forbidden_violation
    )
    if not non_execution_boundary_ok:
        issues.append("non_execution_boundary_gap")

    completed_rows = [dict(m) for m in COMPLETED_MODULES]
    gap_rows = [dict(g) for g in REMAINING_GAPS]
    completed_module_inventory_complete = len(completed_rows) >= 12
    remaining_gap_inventory_complete = len(gap_rows) >= 16

    classification_counts = Counter(g["classification"] for g in gap_rows)
    gap_classification_matrix = {
        "matrix_id": "gap_classification_matrix_v1",
        "gap_classification_matrix_complete": len(classification_counts) >= 6,
        "classifications": list(GAP_CLASSIFICATIONS),
        "counts": dict(classification_counts),
        "future_runtime_debt_not_current_blocker": all(
            not g.get("blocker_now") for g in gap_rows if g.get("classification") == "future_runtime_debt"
        ),
        "future_design_not_current_blocker": all(
            not g.get("blocker_now") for g in gap_rows if g.get("classification") == "future_design"
        ),
        "integration_test_planning_deferred": any(
            g.get("gap_id") == "integration_test_planning_deferred" for g in gap_rows
        ),
        "runtime_not_ready": MODULE_CHAIN_READINESS.get("runtime_not_ready") is True,
        "real_execution_not_ready": MODULE_CHAIN_READINESS.get("real_execution_not_ready") is True,
        **meta,
    }
    future_runtime_debt_not_current_blocker = gap_classification_matrix["future_runtime_debt_not_current_blocker"]
    future_design_not_current_blocker = gap_classification_matrix["future_design_not_current_blocker"]

    module_chain_readiness_map = {
        "map_id": "module_chain_readiness_map_v1",
        "module_chain_readiness_map_complete": True,
        **MODULE_CHAIN_READINESS,
        "boundary_lifecycle_alignment_orchestration_controlled_flow": (
            MODULE_CHAIN_READINESS.get("boundary_to_lifecycle_controlled_flow")
            and MODULE_CHAIN_READINESS.get("lifecycle_to_alignment_controlled_flow")
            and MODULE_CHAIN_READINESS.get("alignment_to_orchestration_controlled_flow")
        ),
        **meta,
    }

    module_handoff_contract_gap_identified = any(
        g.get("gap_id") == "module_handoff_contract_not_implemented" for g in gap_rows
    )
    core_orchestration_not_extended = "core_orchestration_submodule_not_extended_after_module_dryrun_go" in DO_NOT_REOPEN_RULES

    next_module_candidate_selection = {
        "selection_id": "next_module_candidate_selection_v1",
        "next_module_candidate_selection_complete": SELECTED_NEXT_MODULE == "Module Handoff Contract Controlled Implementation",
        "selected_module": SELECTED_NEXT_MODULE,
        "selected_route_id": "A",
        "candidates": list(NEXT_MODULE_CANDIDATES),
        "rationale": "Orchestration produces handoff candidate; unified module handoff contract needed next",
        **meta,
    }

    do_not_reopen = {
        "rules_id": "do_not_reopen_do_not_overbuild_rules_v1",
        "do_not_reopen_do_not_overbuild_rules_complete": len(DO_NOT_REOPEN_RULES) >= 8,
        "rules": list(DO_NOT_REOPEN_RULES),
        **meta,
    }

    next_route_decision = {
        "decision_id": "next_route_decision_v1",
        "next_route_decision_complete": SELECTED_NEXT_ROUTE == NEXT_PHASE_GO,
        "selected_next_route": SELECTED_NEXT_MODULE,
        "selected_route_id": "A",
        "recommended_next_phase": NEXT_PHASE_GO,
        "alternate_routes": [
            {"route_id": "B", "phase_id": NEXT_ROUTE_B},
            {"route_id": "C", "phase_id": NEXT_ROUTE_C},
            {"route_id": "D", "phase_id": NEXT_ROUTE_D},
            {"route_id": "E", "phase_id": NEXT_ROUTE_E},
        ],
        "do_not_declare_midplatform_completed": True,
        **meta,
    }

    consolidation_pass = (
        prior_core_orchestration_module_dryrun_go
        and completed_module_inventory_complete
        and remaining_gap_inventory_complete
        and gap_classification_matrix["gap_classification_matrix_complete"]
        and module_chain_readiness_map["module_chain_readiness_map_complete"]
        and next_module_candidate_selection["next_module_candidate_selection_complete"]
        and do_not_reopen["do_not_reopen_do_not_overbuild_rules_complete"]
        and next_route_decision["next_route_decision_complete"]
        and core_orchestration_not_extended
        and module_handoff_contract_gap_identified
        and future_runtime_debt_not_current_blocker
        and future_design_not_current_blocker
        and non_execution_boundary_ok
        and len(issues) == 0
    )

    template_lineage = build_template_lineage(
        base_phase="Task-Manager-Core-Orchestration-Module-Level-Controlled-DryRun-v1-001",
        base_capability=MODULE_INTEGRATION_GAP_CONSOLIDATION_WHITELIST_FILES[0],
        base_runner=MODULE_INTEGRATION_GAP_CONSOLIDATION_WHITELIST_FILES[1],
        base_verifier=MODULE_INTEGRATION_GAP_CONSOLIDATION_WHITELIST_FILES[2],
        base_go_no_go_pack=GO_NO_GO_PACK,
        stage_phase="Module-Integration-Gap-Consolidation-v1-001",
        stage_term_overrides=MODULE_INTEGRATION_GAP_CONSOLIDATION_STAGE_TERM_OVERRIDES,
        stage_additions=MODULE_INTEGRATION_GAP_CONSOLIDATION_STAGE_ADDITIONS,
        template_files=MODULE_INTEGRATION_GAP_CONSOLIDATION_WHITELIST_FILES,
        repo_root=repo_root,
        upstream_review_phase="Task-Manager-Core-Orchestration-Module-Level-Controlled-DryRun-v1-001",
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
        previous_interruption_type=dryrun_file_size.get("previous_interruption_type"),
        previous_interruption_duration_seconds=dryrun_file_size.get("previous_interruption_duration_seconds"),
        previous_interruption_not_logic_loop=dryrun_file_size.get("previous_interruption_not_logic_loop"),
    )
    file_size_governance_review_ok = file_size_governance_review.get("file_size_governance_review_ok") is True
    if not file_size_governance_review_ok:
        issues.append("file_size_governance_gap")

    consolidation_pass = consolidation_pass and template_lineage.get("template_lineage_ok") and file_size_governance_review_ok and len(issues) == 0
    next_phase = NEXT_PHASE_GO if consolidation_pass else NEXT_PHASE_HOLD

    if not prior_core_orchestration_module_dryrun_go:
        final_decision = FINAL_DECISION_UPSTREAM
    elif not all(absence.values()):
        final_decision = FINAL_DECISION_ABSENCE
    elif not non_execution_boundary_ok:
        final_decision = FINAL_DECISION_RUNTIME
    elif not template_lineage.get("template_lineage_ok"):
        final_decision = FINAL_DECISION_LINEAGE
    elif consolidation_pass:
        final_decision = FINAL_DECISION_GO
    else:
        final_decision = FINAL_DECISION_CONSOLIDATION

    go_values = {
        "prior_core_orchestration_module_dryrun_go": prior_core_orchestration_module_dryrun_go,
        "completed_module_inventory_complete": completed_module_inventory_complete,
        "remaining_gap_inventory_complete": remaining_gap_inventory_complete,
        "gap_classification_matrix_complete": gap_classification_matrix["gap_classification_matrix_complete"],
        "module_chain_readiness_map_complete": module_chain_readiness_map["module_chain_readiness_map_complete"],
        "next_module_candidate_selection_complete": next_module_candidate_selection["next_module_candidate_selection_complete"],
        "do_not_reopen_do_not_overbuild_rules_complete": do_not_reopen["do_not_reopen_do_not_overbuild_rules_complete"],
        "next_route_decision_complete": next_route_decision["next_route_decision_complete"],
        "core_orchestration_not_extended": core_orchestration_not_extended,
        "module_handoff_contract_gap_identified": module_handoff_contract_gap_identified,
        "future_runtime_debt_not_current_blocker": future_runtime_debt_not_current_blocker,
        "future_design_not_current_blocker": future_design_not_current_blocker,
        "midplatform_still_has_remaining_work": True,
        "foundation_consolidation_not_final_midplatform_completion": True,
        "midplatform_overall_status": MIDPLATFORM_OVERALL_STATUS,
        "owner_approval_request_chain_not_reopened": owner_approval_request_chain_not_reopened,
        "owner_approval_request_closed_module": "governance_ready_handoff",
        "non_execution_boundary_ok": non_execution_boundary_ok,
        "no_fragmentary_phase_expansion": True,
        "file_size_governance_review_ok": file_size_governance_review_ok,
        "file_size_governance_review_exists": file_size_governance_review.get("file_size_governance_review_exists") is True,
        "next_phase_readiness_ok": consolidation_pass,
        "module_integration_gap_consolidation_pass": consolidation_pass,
        "real_request_issuance_authorized": False,
        "authorization_request_absent": True,
        "record_creation_absent": record_creation_absent,
        "integration_test_executed": False,
        "integration_test_planning_deferred": True,
        "runtime_not_ready": True,
        "real_execution_not_ready": True,
        "real_issuance_preauthorization_not_opened": True,
        "candidate_promotion_executed": False,
        "route_execution_absent": True,
        "module_handoff_runtime_absent": True,
        "runtime_execution_absent": True,
        "module_adapter_implementation_absent": True,
        "whitebox_runtime_integration_absent": True,
        "drive_brain_implementation_absent": True,
        "survival_brain_implementation_absent": True,
        "reflection_brain_implementation_absent": True,
        "selected_next_module": SELECTED_NEXT_MODULE,
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
            list(dryrun_summary.get("chain_trace_nodes") or []) + ["module_integration_gap_consolidation"]
        ),
        go_no_go_decision=final_decision,
        final_decision=final_decision,
        next_phase=next_phase,
        template_lineage=template_lineage,
    )

    scope_doc = {
        "scope_id": "integration_gap_consolidation_scope_v1",
        "purpose": "Module integration gap merge and route reprioritization only",
        "not_core_orchestration_extension": True,
        "not_integration_test": True,
        "not_runtime": True,
        "not_record_grant_creation": True,
        **meta,
    }
    completed_inventory = {
        "inventory_id": "completed_module_inventory_v1",
        "completed_module_inventory_complete": completed_module_inventory_complete,
        "modules": completed_rows,
        "module_count": len(completed_rows),
        **meta,
    }
    remaining_inventory = {
        "inventory_id": "remaining_gap_inventory_v1",
        "remaining_gap_inventory_complete": remaining_gap_inventory_complete,
        "gaps": gap_rows,
        "gap_count": len(gap_rows),
        **meta,
    }
    report = {
        "report_id": "module_integration_gap_consolidation_report_v1",
        **go_values,
        "final_decision": final_decision,
        "recommended_next_phase": next_phase,
        **meta,
    }
    summary = {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "module_integration_gap_consolidation_pass": consolidation_pass,
        "blocker_count": len(issues),
        "issues": issues,
        **go_values,
        **core_fields,
        "final_decision": final_decision,
        "recommended_next_phase": next_phase,
        **meta,
    }
    markdown = "\n".join([
        "# Module Integration Gap Consolidation v1",
        "",
        f"Completed modules: `{len(completed_rows)}` | Remaining gaps: `{len(gap_rows)}`",
        f"Selected next module: `{SELECTED_NEXT_MODULE}`",
        f"Module handoff contract gap identified: `{module_handoff_contract_gap_identified}`",
        f"Core orchestration not extended: `{core_orchestration_not_extended}`",
        f"Final decision: `{final_decision}`",
        f"Next phase: `{next_phase}`",
    ])
    return {
        "module_integration_gap_consolidation_report": report,
        "module_integration_gap_consolidation_report_md": markdown,
        "integration_gap_consolidation_scope": scope_doc,
        "completed_module_inventory": completed_inventory,
        "remaining_gap_inventory": remaining_inventory,
        "gap_classification_matrix": gap_classification_matrix,
        "module_chain_readiness_map": module_chain_readiness_map,
        "next_module_candidate_selection": next_module_candidate_selection,
        "do_not_reopen_do_not_overbuild_rules": do_not_reopen,
        "next_route_decision": next_route_decision,
        "file_size_governance_review": {**file_size_governance_review, **meta},
        "summary": summary,
    }
