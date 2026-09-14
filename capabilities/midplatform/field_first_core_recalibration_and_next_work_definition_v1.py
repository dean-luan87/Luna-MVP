# -*- coding: utf-8 -*-
"""Field-First Core Recalibration and Next Work Definition v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.midplatform.field_first_core_recalibration_and_next_work_definition_items_v1 import (
    ALTERNATE_NEXT_PHASE,
    ATTRIBUTE_TIERS,
    CORE_ROUTE_ADJUSTMENT,
    DEFERRED_ROUTES,
    DO_NOT_MISCLASSIFY,
    DRIVE_LAYER_FIELD,
    FIELD_BOUNDARY,
    FIELD_CONTINUITY,
    FIELD_FIRST_CONCEPTS,
    FIELD_MODEL_LAYERS,
    FIELD_SIMULATION,
    IPC_REPOSITIONING,
    MIDPLATFORM_REASONING_INPUT,
    NEXT_WORK_ITEMS,
    PERCEPTION_LOOP,
    SELECTED_NEXT_PHASE,
    SELECTED_NEXT_ROUTE,
    SOURCE_MOUNTING,
)
from capabilities.midplatform.field_first_core_recalibration_and_next_work_definition_lineage_v1 import (
    FIELD_FIRST_RECAL_STAGE_ADDITIONS,
    FIELD_FIRST_RECAL_STAGE_TERM_OVERRIDES,
    FIELD_FIRST_RECAL_WHITELIST_FILES,
)
from capabilities.midplatform.file_size_governance_v1 import build_file_size_governance_review
from capabilities.midplatform.information_processing_core_self_work_core_design_v1 import (
    DEFAULT_OUTPUT as DEFAULT_IPC_DESIGN_ROOT,
    FINAL_DECISION_GO as IPC_DESIGN_FINAL_GO,
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

PHASE_ID = "Phase-Midplatform-Field-First-Core-Recalibration-and-Next-Work-Definition-v1-001"
SCOPE = "field_first_core_recalibration_only"
SOURCE_CHAIN = "field_first_core_recalibration_and_next_work_definition_v1"
FINAL_DECISION_GO = "MIDPLATFORM_FIELD_FIRST_CORE_RECALIBRATION_AND_NEXT_WORK_DEFINITION_READY_FOR_FIELD_FIRST_CORE_WORK_MANUAL_AND_ARCHITECTURE_DEFINITION"
FINAL_DECISION_UPSTREAM = "MIDPLATFORM_FIELD_FIRST_CORE_RECALIBRATION_BLOCKED_BY_PRIOR_GAP"
FINAL_DECISION_RECAL = "MIDPLATFORM_FIELD_FIRST_CORE_RECALIBRATION_BLOCKED_BY_RECALIBRATION_GAP"
NEXT_PHASE_HOLD = "Phase-Midplatform-Field-First-Core-Recalibration-Issue-Review-v1-001"
DEFAULT_OUTPUT = "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/field_first_core_recalibration_and_next_work_definition_v1_smoke_v0"
GO_NO_GO_PACK = "docs/architecture/evaluation/LUNA_EVALUATION_FIELD_FIRST_CORE_RECALIBRATION_AND_NEXT_WORK_DEFINITION_V1_GO_NO_GO_PACK_V0.md"
TEMPLATE_LINEAGE_MODULE_PATH = "capabilities/midplatform/field_first_core_recalibration_and_next_work_definition_lineage_v1.py"
MIDPLATFORM_OVERALL_STATUS = "construction_consolidation"

PHASE_PYTHON_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/field_first_core_recalibration_and_next_work_definition_v1.py",
    "capabilities/midplatform/field_first_core_recalibration_and_next_work_definition_items_v1.py",
    "capabilities/midplatform/field_first_core_recalibration_and_next_work_definition_lineage_v1.py",
    "tools/evaluation/midplatform/run_field_first_core_recalibration_and_next_work_definition_v1.py",
    "tools/evaluation/midplatform/verify_field_first_core_recalibration_and_next_work_definition_v1.py",
)

GO_CONDITIONS_KEYS: Tuple[str, ...] = (
    "prior_ipc_self_work_design_go",
    "field_first_core_route_defined",
    "core_route_adjustment_complete",
    "field_first_core_concept_complete",
    "field_model_architecture_sketch_complete",
    "next_work_definition_complete",
    "ipc_repositioned_not_invalidated",
    "peripheral_not_prematurely_fixed",
    "prior_go_results_not_invalidated",
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
        "field_first_core_recalibration_only": True,
        "midplatform_overall_status": MIDPLATFORM_OVERALL_STATUS,
        "foundation_consolidation_not_final_midplatform_completion": True,
        "no_fragmentary_phase_expansion": True,
        "integration_test_executed": False,
        "output_root": str(out), "ipc_design_root": str(upstream),
    }


def run_field_first_core_recalibration_and_next_work_definition_v1(
    *,
    ipc_design_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    out = Path(output_root or DEFAULT_OUTPUT).expanduser().resolve()
    upstream = Path(ipc_design_root).expanduser().resolve()
    repo_root = Path(__file__).resolve().parents[2]
    meta = _meta(out, upstream)
    issues: List[str] = []

    design_s = _read_json(upstream / "summary.json")
    design_v = _read_json(upstream / "verifier_report.json")
    design_fs = _read_json(upstream / "file_size_governance_review_v1.json")

    prior_ipc_self_work_design_go = (
        design_s.get("final_decision") == IPC_DESIGN_FINAL_GO
        and design_v.get("verifier") == "GO"
        and int(design_v.get("passed_checks", 0)) >= 300
        and design_s.get("information_processing_core_self_work_core_design_pass") is True
    )
    if not prior_ipc_self_work_design_go:
        issues.append("ipc_self_work_design_not_go")

    absence = {k: design_s.get(k) is True for k in ABSENCE_KEYS}
    non_execution_boundary_ok = prior_ipc_self_work_design_go and design_s.get("non_execution_boundary_ok") is True and all(absence.values())
    if not non_execution_boundary_ok:
        issues.append("non_execution_boundary_gap")

    field_first_core_route_defined = CORE_ROUTE_ADJUSTMENT.get("field_first_midplatform_core") is True
    core_route_adjustment_complete = len(CORE_ROUTE_ADJUSTMENT.get("new_route") or []) >= 7
    field_first_core_concept_complete = bool(FIELD_FIRST_CONCEPTS.get("field_model"))
    field_model_architecture_sketch_complete = len(FIELD_MODEL_LAYERS) >= 3
    next_work_definition_complete = len(NEXT_WORK_ITEMS) >= 14
    ipc_repositioned_not_invalidated = IPC_REPOSITIONING.get("ipc_not_invalidated") is True
    peripheral_not_prematurely_fixed = all(r.get("status", "").startswith("defer") for r in DEFERRED_ROUTES if "handoff" in r.get("route_id", "") or "lifecycle" in r.get("route_id", ""))
    prior_go_results_not_invalidated = ipc_repositioned_not_invalidated

    route_adj = {**CORE_ROUTE_ADJUSTMENT, "core_route_adjustment_complete": core_route_adjustment_complete, **meta}
    concepts = {**FIELD_FIRST_CONCEPTS, "field_first_core_concept_complete": field_first_core_concept_complete, **meta}
    arch = {"sketch_id": "field_model_architecture_sketch_v1", "field_model_architecture_sketch_complete": field_model_architecture_sketch_complete, "layers": list(FIELD_MODEL_LAYERS), "attribute_tiers": list(ATTRIBUTE_TIERS), **meta}
    source = {**SOURCE_MOUNTING, **meta}
    boundary = {**FIELD_BOUNDARY, **meta}
    continuity = {**FIELD_CONTINUITY, **meta}
    simulation = {**FIELD_SIMULATION, **meta}
    reasoning = {**MIDPLATFORM_REASONING_INPUT, **meta}
    drive = {**DRIVE_LAYER_FIELD, **meta}
    perception = {**PERCEPTION_LOOP, **meta}
    ipc_repo = {**IPC_REPOSITIONING, **meta}
    deferred = {"register_id": "deferred_route_register_v1", "routes": list(DEFERRED_ROUTES), **meta}
    next_work = {"definition_id": "next_work_definition_v1", "next_work_definition_complete": next_work_definition_complete, "items": list(NEXT_WORK_ITEMS), **meta}
    next_route = {
        "decision_id": "next_route_decision_v1",
        "selected_next_route": SELECTED_NEXT_ROUTE,
        "recommended_next_phase": SELECTED_NEXT_PHASE,
        "alternate_next_phase": ALTERNATE_NEXT_PHASE,
        "rationale": "Field-First core must be defined before IPC/CLM/handoff peripheral fixation",
        **meta,
    }
    misclassify = {"rules_id": "do_not_misclassify_rules_v1", "rules": list(DO_NOT_MISCLASSIFY), **meta}

    recal_pass = (
        prior_ipc_self_work_design_go and field_first_core_route_defined and core_route_adjustment_complete
        and field_first_core_concept_complete and field_model_architecture_sketch_complete
        and next_work_definition_complete and ipc_repositioned_not_invalidated and peripheral_not_prematurely_fixed
        and prior_go_results_not_invalidated and non_execution_boundary_ok and len(issues) == 0
    )

    template_lineage = build_template_lineage(
        base_phase="Midplatform-Information-Processing-Core-Self-Work-Core-Design-v1-001",
        base_capability=FIELD_FIRST_RECAL_WHITELIST_FILES[0],
        base_runner=FIELD_FIRST_RECAL_WHITELIST_FILES[1],
        base_verifier=FIELD_FIRST_RECAL_WHITELIST_FILES[2],
        base_go_no_go_pack=GO_NO_GO_PACK,
        stage_phase="Midplatform-Field-First-Core-Recalibration-and-Next-Work-Definition-v1-001",
        stage_term_overrides=FIELD_FIRST_RECAL_STAGE_TERM_OVERRIDES,
        stage_additions=FIELD_FIRST_RECAL_STAGE_ADDITIONS,
        template_files=FIELD_FIRST_RECAL_WHITELIST_FILES,
        repo_root=repo_root,
        upstream_review_phase="Midplatform-Information-Processing-Core-Self-Work-Core-Design-v1-001",
    )
    if not template_lineage.get("template_lineage_ok"):
        issues.append("template_lineage_gap")

    file_size = build_file_size_governance_review(
        phase_id=PHASE_ID, scope_paths=list(PHASE_PYTHON_FILES), repo_root=repo_root,
        phase_python_paths=PHASE_PYTHON_FILES, template_lineage_path=TEMPLATE_LINEAGE_MODULE_PATH,
        read_strategy="summary_index_first", full_repo_scan=False,
        previous_interruption_type=design_fs.get("previous_interruption_type"),
    )
    fs_ok = file_size.get("file_size_governance_review_ok") is True
    recal_pass = recal_pass and template_lineage.get("template_lineage_ok") and fs_ok and len(issues) == 0
    next_phase = SELECTED_NEXT_PHASE if recal_pass else NEXT_PHASE_HOLD
    final_decision = FINAL_DECISION_GO if recal_pass else (FINAL_DECISION_UPSTREAM if not prior_ipc_self_work_design_go else FINAL_DECISION_RECAL)

    go_values = {
        "prior_ipc_self_work_design_go": prior_ipc_self_work_design_go,
        "field_first_core_route_defined": field_first_core_route_defined,
        "core_route_adjustment_complete": core_route_adjustment_complete,
        "field_first_core_concept_complete": field_first_core_concept_complete,
        "field_model_architecture_sketch_complete": field_model_architecture_sketch_complete,
        "next_work_definition_complete": next_work_definition_complete,
        "ipc_repositioned_not_invalidated": ipc_repositioned_not_invalidated,
        "peripheral_not_prematurely_fixed": peripheral_not_prematurely_fixed,
        "prior_go_results_not_invalidated": prior_go_results_not_invalidated,
        "field_first_midplatform_core": True,
        "ipc_no_longer_direct_center": True,
        "handoff_contract_p3_defer_remains_defer": True,
        "no_runtime_execution": True,
        "no_integration_test": True,
        "no_record_creation": True,
        "no_grant_creation": True,
        "no_authorization_request_creation": True,
        "midplatform_still_has_remaining_work": True,
        "non_execution_boundary_ok": non_execution_boundary_ok,
        "file_size_governance_review_ok": fs_ok,
        "next_phase_readiness_ok": recal_pass,
        "field_first_core_recalibration_pass": recal_pass,
        "selected_next_route": SELECTED_NEXT_ROUTE,
        "full_repo_scan_absent": file_size.get("full_repo_scan_absent") is True,
        "tmp_eval_out_scan_absent": file_size.get("tmp_eval_out_scan_absent") is True,
        "summary_index_first_reading_ok": file_size.get("summary_index_first_reading_ok") is True,
        **absence,
    }
    core_fields = build_core_go_no_go_summary_fields(
        go_conditions={k: go_values[k] for k in GO_CONDITIONS_KEYS},
        forbidden_runtime_flags=RUNTIME_FORBIDDEN_FLAGS,
        chain_trace_nodes=tuple(list(design_s.get("chain_trace_nodes") or []) + ["field_first_core_recalibration"]),
        go_no_go_decision=final_decision, final_decision=final_decision, next_phase=next_phase,
        template_lineage=template_lineage,
    )
    summary = {
        "phase": PHASE_ID, "scope": SCOPE, "blocker_count": len(issues), "issues": issues,
        **go_values, **core_fields, "final_decision": final_decision, "recommended_next_phase": next_phase, **meta,
    }
    md = "\n".join([
        "# Field-First Core Recalibration v1",
        f"Old route: IPC-centric → New route: Field-First",
        f"Field layers: `{len(FIELD_MODEL_LAYERS)}` | Next work items: `{len(NEXT_WORK_ITEMS)}`",
        f"IPC repositioned: `{IPC_REPOSITIONING['ipc_status']}`",
        f"Final decision: `{final_decision}`",
        f"Next: `{next_phase}`",
    ])
    return {
        "field_first_core_recalibration_report": {**go_values, "final_decision": final_decision, **meta},
        "field_first_core_recalibration_report_md": md,
        "core_route_adjustment": route_adj,
        "field_first_core_concept_definition": concepts,
        "field_model_architecture_sketch": arch,
        "source_mounting_model": source,
        "field_boundary_model": boundary,
        "field_continuity_model": continuity,
        "field_simulation_model": simulation,
        "midplatform_reasoning_input_model": reasoning,
        "drive_layer_field_relationship": drive,
        "perception_request_loop_model": perception,
        "ipc_repositioning_review": ipc_repo,
        "deferred_route_register": deferred,
        "next_work_definition": next_work,
        "next_route_decision": next_route,
        "do_not_misclassify_rules": misclassify,
        "file_size_governance_review": {**file_size, **meta},
        "summary": summary,
    }
