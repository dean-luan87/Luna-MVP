# -*- coding: utf-8 -*-
"""Field-First Core Model Room and Interface Logic Definition v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.midplatform.field_first_core_model_room_items_v1 import (
    CANDIDATE_OUTPUT_TYPES,
    DEFERRED_MODEL_INTEGRATION,
    DO_NOT_MISCLASSIFY,
    FIELD_MODEL_INPUT_CONTRACT,
    FIELD_SIMULATION_IO_CONTRACT,
    INTERFACE_LOGIC,
    MIDPLATFORM_REASONING_IO_CONTRACT,
    MODEL_ADAPTER_BUS,
    MODEL_ADAPTER_INTERFACE_FIELDS,
    MODEL_ROOM_PRINCIPLES,
    MODEL_ROOMS,
    MODEL_USAGE_ORDER,
    OPEN_SOURCE_REFERENCE_INVENTORY,
    PRIOR_ASSET_REPOSITIONING,
    PROHIBITED_MODEL_OUTPUTS,
    SELECTED_NEXT_PHASE,
    SELECTED_NEXT_ROUTE,
)
from capabilities.midplatform.field_first_core_model_room_lineage_v1 import (
    FIELD_FIRST_MODEL_ROOM_STAGE_ADDITIONS,
    FIELD_FIRST_MODEL_ROOM_STAGE_TERM_OVERRIDES,
    FIELD_FIRST_MODEL_ROOM_WHITELIST_FILES,
)
from capabilities.midplatform.field_first_core_role_function_redefinition_v1 import (
    DEFAULT_OUTPUT as DEFAULT_ROLE_REDEF_ROOT,
    FINAL_DECISION_GO as ROLE_REDEF_FINAL_GO,
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

PHASE_ID = "Phase-Midplatform-Field-First-Core-Model-Room-and-Interface-Logic-Definition-v1-001"
SCOPE = "field_first_core_model_room_interface_logic_definition_only"
SOURCE_CHAIN = "field_first_core_model_room_interface_logic_definition_v1"
FINAL_DECISION_GO = "MIDPLATFORM_FIELD_FIRST_CORE_MODEL_ROOM_AND_INTERFACE_LOGIC_READY_FOR_FIELD_FIRST_CORE_WORK_MANUAL_AND_ARCHITECTURE_DEFINITION"
FINAL_DECISION_UPSTREAM = "MIDPLATFORM_FIELD_FIRST_CORE_MODEL_ROOM_BLOCKED_BY_PRIOR_GAP"
FINAL_DECISION_RECAL = "MIDPLATFORM_FIELD_FIRST_CORE_MODEL_ROOM_BLOCKED_BY_DEFINITION_GAP"
NEXT_PHASE_HOLD = "Phase-Midplatform-Field-First-Core-Model-Room-Issue-Review-v1-001"
DEFAULT_OUTPUT = "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/field_first_core_model_room_interface_logic_definition_v1_smoke_v0"
GO_NO_GO_PACK = "docs/architecture/evaluation/LUNA_EVALUATION_FIELD_FIRST_CORE_MODEL_ROOM_INTERFACE_LOGIC_DEFINITION_V1_GO_NO_GO_PACK_V0.md"
TEMPLATE_LINEAGE_MODULE_PATH = "capabilities/midplatform/field_first_core_model_room_lineage_v1.py"
MIDPLATFORM_OVERALL_STATUS = "construction_consolidation"

PHASE_PYTHON_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/field_first_core_model_room_interface_logic_definition_v1.py",
    "capabilities/midplatform/field_first_core_model_room_items_v1.py",
    "capabilities/midplatform/field_first_core_model_room_lineage_v1.py",
    "tools/evaluation/midplatform/run_field_first_core_model_room_interface_logic_definition_v1.py",
    "tools/evaluation/midplatform/verify_field_first_core_model_room_interface_logic_definition_v1.py",
)

GO_CONDITIONS_KEYS: Tuple[str, ...] = (
    "prior_field_first_role_redef_go",
    "model_room_definition_complete",
    "open_source_reference_inventory_complete",
    "model_adapter_interface_complete",
    "candidate_output_registry_complete",
    "field_model_model_interface_complete",
    "field_simulation_interface_complete",
    "midplatform_reasoning_interface_complete",
    "model_integration_deferred",
    "model_output_candidate_only",
    "model_does_not_define_core",
    "adapter_required_for_all_models",
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
        "field_first_core_model_room_interface_logic_definition_only": True,
        "midplatform_overall_status": MIDPLATFORM_OVERALL_STATUS,
        "foundation_consolidation_not_final_midplatform_completion": True,
        "no_fragmentary_phase_expansion": True,
        "integration_test_executed": False,
        "output_root": str(out), "role_redef_root": str(upstream),
    }


def run_field_first_core_model_room_interface_logic_definition_v1(
    *,
    role_redef_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    out = Path(output_root or DEFAULT_OUTPUT).expanduser().resolve()
    upstream = Path(role_redef_root).expanduser().resolve()
    repo_root = Path(__file__).resolve().parents[2]
    meta = _meta(out, upstream)
    issues: List[str] = []

    role_s = _read_json(upstream / "summary.json")
    role_v = _read_json(upstream / "verifier_report.json")
    role_fs = _read_json(upstream / "file_size_governance_review_v1.json")

    prior_field_first_role_redef_go = (
        role_s.get("final_decision") == ROLE_REDEF_FINAL_GO
        and role_v.get("verifier") == "GO"
        and int(role_v.get("passed_checks", 0)) >= 380
        and role_s.get("field_first_core_role_function_redefinition_pass") is True
    )
    if not prior_field_first_role_redef_go:
        issues.append("field_first_role_redef_not_go")

    absence = {k: role_s.get(k) is True for k in ABSENCE_KEYS}
    non_execution_boundary_ok = prior_field_first_role_redef_go and role_s.get("non_execution_boundary_ok") is True and all(absence.values())
    if not non_execution_boundary_ok:
        issues.append("non_execution_boundary_gap")

    model_room_definition_complete = len(MODEL_ROOMS) >= 9
    open_source_reference_inventory_complete = len(OPEN_SOURCE_REFERENCE_INVENTORY) >= 12
    model_adapter_interface_complete = len(MODEL_ADAPTER_INTERFACE_FIELDS) >= 12
    candidate_output_registry_complete = len(CANDIDATE_OUTPUT_TYPES) >= 18
    field_model_model_interface_complete = bool(FIELD_MODEL_INPUT_CONTRACT.get("contract_id"))
    field_simulation_interface_complete = bool(FIELD_SIMULATION_IO_CONTRACT.get("contract_id"))
    midplatform_reasoning_interface_complete = bool(MIDPLATFORM_REASONING_IO_CONTRACT.get("contract_id"))
    deferred_items = [d for d in DEFERRED_MODEL_INTEGRATION if d.get("status", "").startswith("defer")]
    model_integration_deferred = len(deferred_items) >= 8
    model_output_candidate_only = len(PROHIBITED_MODEL_OUTPUTS) >= 7
    model_does_not_define_core = MODEL_ROOM_PRINCIPLES.get("rules") and "model_cannot_reverse_define_midplatform" in MODEL_ROOM_PRINCIPLES["rules"]
    adapter_required_for_all_models = MODEL_ADAPTER_BUS.get("adapter_required_for_all_models") is True

    rooms = {"registry_id": "model_room_registry_v1", "model_room_definition_complete": model_room_definition_complete, "count": len(MODEL_ROOMS), "principles": MODEL_ROOM_PRINCIPLES, "rooms": list(MODEL_ROOMS), **meta}
    inventory = {"inventory_id": "open_source_reference_inventory_v1", "open_source_reference_inventory_complete": open_source_reference_inventory_complete, "count": len(OPEN_SOURCE_REFERENCE_INVENTORY), "entries": list(OPEN_SOURCE_REFERENCE_INVENTORY), **meta}
    mapping = {"mapping_id": "model_capability_mapping_v1", "entries": list(OPEN_SOURCE_REFERENCE_INVENTORY), **meta}
    adapter = {
        "interface_id": "model_adapter_interface_v1",
        "model_adapter_interface_complete": model_adapter_interface_complete,
        "required_fields": list(MODEL_ADAPTER_INTERFACE_FIELDS),
        "bus": MODEL_ADAPTER_BUS,
        "usage_order": list(MODEL_USAGE_ORDER),
        **meta,
    }
    candidates = {"registry_id": "model_candidate_output_registry_v1", "candidate_output_registry_complete": candidate_output_registry_complete, "candidate_types": list(CANDIDATE_OUTPUT_TYPES), **meta}
    field_in = {**FIELD_MODEL_INPUT_CONTRACT, "field_model_model_interface_complete": field_model_model_interface_complete, **meta}
    sim_io = {**FIELD_SIMULATION_IO_CONTRACT, "field_simulation_interface_complete": field_simulation_interface_complete, **meta}
    reason_io = {**MIDPLATFORM_REASONING_IO_CONTRACT, "midplatform_reasoning_interface_complete": midplatform_reasoning_interface_complete, **meta}
    prohibited = {"registry_id": "prohibited_model_outputs_v1", "prohibited_outputs": list(PROHIBITED_MODEL_OUTPUTS), **meta}
    deferred = {"register_id": "deferred_model_integration_register_v1", "model_integration_deferred": model_integration_deferred, "entries": list(DEFERRED_MODEL_INTEGRATION), **meta}
    reposition = {"register_id": "prior_asset_repositioning_v1", "assets": list(PRIOR_ASSET_REPOSITIONING), **meta}
    iface_logic = {"logic_id": "interface_logic_v1", "flows": list(INTERFACE_LOGIC), **meta}
    next_route = {
        "decision_id": "next_route_decision_v1",
        "selected_next_route": SELECTED_NEXT_ROUTE,
        "recommended_next_phase": SELECTED_NEXT_PHASE,
        "rationale": "Model rooms and adapter interfaces defined; next define work manuals per room/role",
        **meta,
    }
    misclassify = {"rules_id": "do_not_misclassify_rules_v1", "rules": list(DO_NOT_MISCLASSIFY), **meta}

    def_pass = (
        prior_field_first_role_redef_go and model_room_definition_complete
        and open_source_reference_inventory_complete and model_adapter_interface_complete
        and candidate_output_registry_complete and field_model_model_interface_complete
        and field_simulation_interface_complete and midplatform_reasoning_interface_complete
        and model_integration_deferred and model_output_candidate_only and model_does_not_define_core
        and adapter_required_for_all_models and non_execution_boundary_ok and len(issues) == 0
    )

    template_lineage = build_template_lineage(
        base_phase="Midplatform-Field-First-Core-Role-Function-Redefinition-v1-001",
        base_capability=FIELD_FIRST_MODEL_ROOM_WHITELIST_FILES[0],
        base_runner=FIELD_FIRST_MODEL_ROOM_WHITELIST_FILES[1],
        base_verifier=FIELD_FIRST_MODEL_ROOM_WHITELIST_FILES[2],
        base_go_no_go_pack=GO_NO_GO_PACK,
        stage_phase="Midplatform-Field-First-Core-Model-Room-and-Interface-Logic-Definition-v1-001",
        stage_term_overrides=FIELD_FIRST_MODEL_ROOM_STAGE_TERM_OVERRIDES,
        stage_additions=FIELD_FIRST_MODEL_ROOM_STAGE_ADDITIONS,
        template_files=FIELD_FIRST_MODEL_ROOM_WHITELIST_FILES,
        repo_root=repo_root,
        upstream_review_phase="Midplatform-Field-First-Core-Role-Function-Redefinition-v1-001",
    )
    if not template_lineage.get("template_lineage_ok"):
        issues.append("template_lineage_gap")

    file_size = build_file_size_governance_review(
        phase_id=PHASE_ID, scope_paths=list(PHASE_PYTHON_FILES), repo_root=repo_root,
        phase_python_paths=PHASE_PYTHON_FILES, template_lineage_path=TEMPLATE_LINEAGE_MODULE_PATH,
        read_strategy="summary_index_first", full_repo_scan=False,
        previous_interruption_type=role_fs.get("previous_interruption_type"),
    )
    fs_ok = file_size.get("file_size_governance_review_ok") is True
    def_pass = def_pass and template_lineage.get("template_lineage_ok") and fs_ok and len(issues) == 0
    next_phase = SELECTED_NEXT_PHASE if def_pass else NEXT_PHASE_HOLD
    final_decision = FINAL_DECISION_GO if def_pass else (FINAL_DECISION_UPSTREAM if not prior_field_first_role_redef_go else FINAL_DECISION_RECAL)

    go_values = {
        "prior_field_first_role_redef_go": prior_field_first_role_redef_go,
        "model_room_definition_complete": model_room_definition_complete,
        "open_source_reference_inventory_complete": open_source_reference_inventory_complete,
        "model_adapter_interface_complete": model_adapter_interface_complete,
        "candidate_output_registry_complete": candidate_output_registry_complete,
        "field_model_model_interface_complete": field_model_model_interface_complete,
        "field_simulation_interface_complete": field_simulation_interface_complete,
        "midplatform_reasoning_interface_complete": midplatform_reasoning_interface_complete,
        "model_integration_deferred": model_integration_deferred,
        "model_output_candidate_only": model_output_candidate_only,
        "model_does_not_define_core": model_does_not_define_core,
        "adapter_required_for_all_models": adapter_required_for_all_models,
        "field_first_route_preserved": True,
        "ipc_repositioned_as_source_normalization_asset": True,
        "kimera_hydra_hovsg_reference_only_now": True,
        "sam2_grounded_sam2_reference_or_future_adapter_only_now": True,
        "ecs_reference_does_not_force_runtime": True,
        "kg_reference_does_not_force_full_knowledge_graph": True,
        "handoff_contract_p3_defer_remains_defer": True,
        "no_real_model_download": True,
        "no_weight_download": True,
        "no_inference_execution": True,
        "no_runtime_execution": True,
        "no_integration_test": True,
        "no_world_model_fact_creation": True,
        "no_persistent_memory_write": True,
        "no_record_creation": True,
        "no_grant_creation": True,
        "no_authorization_request_creation": True,
        "midplatform_still_has_remaining_work": True,
        "non_execution_boundary_ok": non_execution_boundary_ok,
        "file_size_governance_review_ok": fs_ok,
        "next_phase_readiness_ok": def_pass,
        "field_first_core_model_room_interface_logic_definition_pass": def_pass,
        "selected_next_route": SELECTED_NEXT_ROUTE,
        "model_room_count": len(MODEL_ROOMS),
        "open_source_reference_count": len(OPEN_SOURCE_REFERENCE_INVENTORY),
        "full_repo_scan_absent": file_size.get("full_repo_scan_absent") is True,
        "tmp_eval_out_scan_absent": file_size.get("tmp_eval_out_scan_absent") is True,
        "summary_index_first_reading_ok": file_size.get("summary_index_first_reading_ok") is True,
        **absence,
    }
    core_fields = build_core_go_no_go_summary_fields(
        go_conditions={k: go_values[k] for k in GO_CONDITIONS_KEYS},
        forbidden_runtime_flags=RUNTIME_FORBIDDEN_FLAGS,
        chain_trace_nodes=tuple(list(role_s.get("chain_trace_nodes") or []) + ["field_first_core_model_room_interface_logic"]),
        go_no_go_decision=final_decision, final_decision=final_decision, next_phase=next_phase,
        template_lineage=template_lineage,
    )
    summary = {
        "phase": PHASE_ID, "scope": SCOPE, "blocker_count": len(issues), "issues": issues,
        **go_values, **core_fields, "final_decision": final_decision, "recommended_next_phase": next_phase, **meta,
    }
    md = "\n".join([
        "# Field-First Core Model Room & Interface Logic v1",
        f"Model rooms: `{len(MODEL_ROOMS)}` | Open source refs: `{len(OPEN_SOURCE_REFERENCE_INVENTORY)}`",
        f"Candidate types: `{len(CANDIDATE_OUTPUT_TYPES)}` | Prohibited: `{len(PROHIBITED_MODEL_OUTPUTS)}`",
        f"Adapter required: `{adapter_required_for_all_models}` | Integration deferred: `{model_integration_deferred}`",
        f"Final decision: `{final_decision}`",
        f"Next: `{next_phase}`",
    ])
    return {
        "model_room_interface_logic_report": {**go_values, "final_decision": final_decision, **meta},
        "model_room_interface_logic_report_md": md,
        "model_room_registry": rooms,
        "open_source_reference_inventory": inventory,
        "model_capability_mapping": mapping,
        "model_adapter_interface": adapter,
        "model_candidate_output_registry": candidates,
        "field_model_input_contract_from_models": field_in,
        "field_simulation_input_output_contract": sim_io,
        "midplatform_reasoning_model_input_output_contract": reason_io,
        "prohibited_model_outputs": prohibited,
        "deferred_model_integration_register": deferred,
        "prior_asset_repositioning": reposition,
        "interface_logic_flows": iface_logic,
        "next_route_decision": next_route,
        "do_not_misclassify_rules": misclassify,
        "file_size_governance_review": {**file_size, **meta},
        "summary": summary,
    }
