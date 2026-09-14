# -*- coding: utf-8 -*-
"""Field-First Core Model I/O Compatibility Precheck v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.midplatform.field_first_core_model_document_capability_review_v1 import (
    DEFAULT_OUTPUT as DEFAULT_DOC_REVIEW_ROOT,
    FINAL_DECISION_GO as DOC_REVIEW_FINAL_GO,
)
from capabilities.midplatform.field_first_core_model_io_compatibility_precheck_items_v1 import (
    CANDIDATE_COMMON_PAYLOAD_REQUIREMENTS,
    COMMON_CONFIDENCE_PAYLOAD,
    COMMON_GRAPH_PAYLOAD,
    COMMON_IDENTITY_PAYLOAD,
    COMMON_SPATIAL_PAYLOAD,
    COMMON_TEMPORAL_PAYLOAD,
    COMMON_TEXT_AUDIO_PAYLOAD,
    DO_NOT_MISCLASSIFY,
    IO_REVIEW_FIELDS,
    MODEL_IO_REVIEW_ITEMS,
    PRECHECK_PRINCIPLES,
    SELECTED_NEXT_PHASE,
    SELECTED_NEXT_ROUTE,
    SKELETON_IO_REQUIREMENTS,
    SKELETON_SCHEMA_ADJUSTMENT_PLAN,
)
from capabilities.midplatform.field_first_core_model_io_compatibility_precheck_lineage_v1 import (
    FIELD_FIRST_IO_PRECHECK_STAGE_ADDITIONS,
    FIELD_FIRST_IO_PRECHECK_STAGE_TERM_OVERRIDES,
    FIELD_FIRST_IO_PRECHECK_WHITELIST_FILES,
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

PHASE_ID = "Phase-Midplatform-Field-First-Core-Model-IO-Compatibility-Precheck-v1-001"
SCOPE = "field_first_core_model_io_precheck_only"
SOURCE_CHAIN = "field_first_core_model_io_compatibility_precheck_v1"
FINAL_DECISION_GO = "MIDPLATFORM_FIELD_FIRST_CORE_MODEL_IO_COMPATIBILITY_PRECHECK_READY_FOR_SELF_DEVELOPED_FIELD_FIRST_SKELETON_IMPLEMENTATION"
FINAL_DECISION_UPSTREAM = "MIDPLATFORM_FIELD_FIRST_CORE_MODEL_IO_PRECHECK_BLOCKED_BY_PRIOR_GAP"
FINAL_DECISION_RECAL = "MIDPLATFORM_FIELD_FIRST_CORE_MODEL_IO_PRECHECK_BLOCKED_BY_PRECHECK_GAP"
NEXT_PHASE_HOLD = "Phase-Midplatform-Field-First-Core-Model-IO-Precheck-Issue-Review-v1-001"
DEFAULT_OUTPUT = "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/field_first_core_model_io_compatibility_precheck_v1_smoke_v0"
GO_NO_GO_PACK = "docs/architecture/evaluation/LUNA_EVALUATION_FIELD_FIRST_CORE_MODEL_IO_COMPATIBILITY_PRECHECK_V1_GO_NO_GO_PACK_V0.md"
TEMPLATE_LINEAGE_MODULE_PATH = "capabilities/midplatform/field_first_core_model_io_compatibility_precheck_lineage_v1.py"
MIDPLATFORM_OVERALL_STATUS = "construction_consolidation"

PHASE_PYTHON_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/field_first_core_model_io_compatibility_precheck_v1.py",
    "capabilities/midplatform/field_first_core_model_io_compatibility_precheck_items_v1.py",
    "capabilities/midplatform/field_first_core_model_io_compatibility_precheck_lineage_v1.py",
    "tools/evaluation/midplatform/run_field_first_core_model_io_compatibility_precheck_v1.py",
    "tools/evaluation/midplatform/verify_field_first_core_model_io_compatibility_precheck_v1.py",
)

GO_CONDITIONS_KEYS: Tuple[str, ...] = (
    "prior_model_document_review_go",
    "model_io_compatibility_precheck_complete",
    "model_io_to_candidate_mapping_complete",
    "candidate_schema_compatibility_matrix_complete",
    "skeleton_schema_adjustment_plan_complete",
    "field_first_skeleton_io_requirements_complete",
    "skeleton_schema_adjustment_needed_evaluated",
    "no_download_execution",
    "non_execution_boundary_ok",
    "file_size_governance_review_ok",
    "next_phase_readiness_ok",
)


def _read_json(path: Path) -> Dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}
    except (json.JSONDecodeError, OSError):
        return {}


def _meta(out: Path, doc_root: Path) -> Dict[str, Any]:
    return {
        "phase": PHASE_ID, "scope": SCOPE, "source_chain": SOURCE_CHAIN,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "foundation_id": "midplatform_task_manager_foundation_v1",
        "runtime_status": "not_enabled",
        "field_first_core_model_io_precheck_only": True,
        "midplatform_overall_status": MIDPLATFORM_OVERALL_STATUS,
        "foundation_consolidation_not_final_midplatform_completion": True,
        "no_fragmentary_phase_expansion": True,
        "integration_test_executed": False,
        "output_root": str(out), "doc_review_root": str(doc_root),
    }


def run_field_first_core_model_io_compatibility_precheck_v1(
    *,
    doc_review_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    out = Path(output_root or DEFAULT_OUTPUT).expanduser().resolve()
    doc_upstream = Path(doc_review_root or DEFAULT_DOC_REVIEW_ROOT).expanduser().resolve()
    repo_root = Path(__file__).resolve().parents[2]
    meta = _meta(out, doc_upstream)
    issues: List[str] = []

    doc_s = _read_json(doc_upstream / "summary.json")
    doc_v = _read_json(doc_upstream / "verifier_report.json")
    prior_model_document_review_go = (
        doc_s.get("final_decision") == DOC_REVIEW_FINAL_GO
        and doc_v.get("verifier") == "GO"
        and int(doc_v.get("passed_checks", 0)) >= 460
        and doc_s.get("field_first_core_model_document_capability_review_pass") is True
    )
    if not prior_model_document_review_go:
        issues.append("doc_review_not_go")

    absence = {k: doc_s.get(k) is True for k in ABSENCE_KEYS}
    non_execution_boundary_ok = prior_model_document_review_go and doc_s.get("non_execution_boundary_ok") is True and all(absence.values())
    if not non_execution_boundary_ok:
        issues.append("non_execution_boundary_gap")

    items = [dict(i) for i in MODEL_IO_REVIEW_ITEMS]
    model_io_compatibility_precheck_complete = len(items) >= 18
    mapping_rows = [{"model_project_id": i["model_project_id"], "maps_to_candidate_type": i["maps_to_candidate_type"], "adapter_transform": i["required_adapter_transform"]} for i in items]
    model_io_to_candidate_mapping_complete = len(mapping_rows) >= 18
    compat_rows = [{"model_project_id": i["model_project_id"], "compatibility_status": i["compatibility_status"], "adjustment_needed": i["skeleton_schema_adjustment_needed"]} for i in items]
    candidate_schema_compatibility_matrix_complete = len(compat_rows) >= 18
    gaps = [{"model_project_id": i["model_project_id"], "missing": i["candidate_fields_missing_or_unclear"]} for i in items if i.get("candidate_fields_missing_or_unclear")]
    skeleton_schema_adjustment_plan_complete = SKELETON_SCHEMA_ADJUSTMENT_PLAN.get("add_common_spatial_payload") is True
    field_first_skeleton_io_requirements_complete = len(SKELETON_IO_REQUIREMENTS) >= 10
    skeleton_schema_adjustment_needed_evaluated = any(i.get("skeleton_schema_adjustment_needed") for i in items)

    registry = {"registry_id": "model_io_review_item_registry_v1", "count": len(items), "fields": list(IO_REVIEW_FIELDS), "items": items, **meta}
    mapping = {"mapping_id": "model_io_to_candidate_mapping_v1", "model_io_to_candidate_mapping_complete": model_io_to_candidate_mapping_complete, "rows": mapping_rows, **meta}
    compat = {"matrix_id": "candidate_schema_compatibility_matrix_v1", "candidate_schema_compatibility_matrix_complete": candidate_schema_compatibility_matrix_complete, "rows": compat_rows, **meta}
    adjust = {**SKELETON_SCHEMA_ADJUSTMENT_PLAN, "skeleton_schema_adjustment_plan_complete": skeleton_schema_adjustment_plan_complete, **meta}
    gap_reg = {"register_id": "model_io_gap_register_v1", "gaps": gaps, **meta}
    skel_io = {"requirements_id": "field_first_skeleton_io_requirements_v1", "field_first_skeleton_io_requirements_complete": field_first_skeleton_io_requirements_complete, "requirements": list(SKELETON_IO_REQUIREMENTS), **meta}
    common_payload = {
        "requirements_id": "candidate_common_payload_requirements_v1",
        "spatial": list(COMMON_SPATIAL_PAYLOAD),
        "temporal": list(COMMON_TEMPORAL_PAYLOAD),
        "identity": list(COMMON_IDENTITY_PAYLOAD),
        "confidence": list(COMMON_CONFIDENCE_PAYLOAD),
        "graph": list(COMMON_GRAPH_PAYLOAD),
        "text_audio": list(COMMON_TEXT_AUDIO_PAYLOAD),
        "common": list(CANDIDATE_COMMON_PAYLOAD_REQUIREMENTS),
        **meta,
    }
    next_route = {"decision_id": "next_route_decision_v1", "selected_next_route": SELECTED_NEXT_ROUTE, "recommended_next_phase": SELECTED_NEXT_PHASE, "rationale": "IO precheck calibrates skeleton before implementation", **meta}
    misclassify = {"rules_id": "do_not_misclassify_rules_v1", "rules": list(DO_NOT_MISCLASSIFY), **meta}

    precheck_pass = (
        prior_model_document_review_go and model_io_compatibility_precheck_complete
        and model_io_to_candidate_mapping_complete and candidate_schema_compatibility_matrix_complete
        and skeleton_schema_adjustment_plan_complete and field_first_skeleton_io_requirements_complete
        and skeleton_schema_adjustment_needed_evaluated and non_execution_boundary_ok and len(issues) == 0
    )

    template_lineage = build_template_lineage(
        base_phase="Midplatform-Field-First-Core-Model-Document-Capability-Review-v1-001",
        base_capability=FIELD_FIRST_IO_PRECHECK_WHITELIST_FILES[0],
        base_runner=FIELD_FIRST_IO_PRECHECK_WHITELIST_FILES[1],
        base_verifier=FIELD_FIRST_IO_PRECHECK_WHITELIST_FILES[2],
        base_go_no_go_pack=GO_NO_GO_PACK,
        stage_phase="Midplatform-Field-First-Core-Model-IO-Compatibility-Precheck-v1-001",
        stage_term_overrides=FIELD_FIRST_IO_PRECHECK_STAGE_TERM_OVERRIDES,
        stage_additions=FIELD_FIRST_IO_PRECHECK_STAGE_ADDITIONS,
        template_files=FIELD_FIRST_IO_PRECHECK_WHITELIST_FILES,
        repo_root=repo_root,
        upstream_review_phase="Midplatform-Field-First-Core-Model-Document-Capability-Review-v1-001",
    )
    if not template_lineage.get("template_lineage_ok"):
        issues.append("template_lineage_gap")

    doc_fs = _read_json(doc_upstream / "file_size_governance_review_v1.json")
    file_size = build_file_size_governance_review(
        phase_id=PHASE_ID, scope_paths=list(PHASE_PYTHON_FILES), repo_root=repo_root,
        phase_python_paths=PHASE_PYTHON_FILES, template_lineage_path=TEMPLATE_LINEAGE_MODULE_PATH,
        read_strategy="summary_index_first", full_repo_scan=False,
        previous_interruption_type=doc_fs.get("previous_interruption_type"),
    )
    fs_ok = file_size.get("file_size_governance_review_ok") is True
    precheck_pass = precheck_pass and template_lineage.get("template_lineage_ok") and fs_ok and len(issues) == 0
    next_phase = SELECTED_NEXT_PHASE if precheck_pass else NEXT_PHASE_HOLD
    final_decision = FINAL_DECISION_GO if precheck_pass else (FINAL_DECISION_UPSTREAM if not prior_model_document_review_go else FINAL_DECISION_RECAL)

    go_values = {
        "prior_model_document_review_go": prior_model_document_review_go,
        "model_io_compatibility_precheck_complete": model_io_compatibility_precheck_complete,
        "model_io_to_candidate_mapping_complete": model_io_to_candidate_mapping_complete,
        "candidate_schema_compatibility_matrix_complete": candidate_schema_compatibility_matrix_complete,
        "skeleton_schema_adjustment_plan_complete": skeleton_schema_adjustment_plan_complete,
        "field_first_skeleton_io_requirements_complete": field_first_skeleton_io_requirements_complete,
        "skeleton_schema_adjustment_needed_evaluated": skeleton_schema_adjustment_needed_evaluated,
        "no_download_execution": True,
        "self_developed_skeleton_still_next": True,
        "download_authorized_all_remain_false": True,
        "field_first_route_preserved": True,
        "no_model_download": True,
        "no_weight_download": True,
        "no_repo_clone": True,
        "no_large_dependency_install": True,
        "no_inference_execution": True,
        "no_runtime_execution": True,
        "no_integration_test": True,
        "no_model_selected_as_production": True,
        "no_record_creation": True,
        "no_grant_creation": True,
        "no_authorization_request_creation": True,
        "midplatform_still_has_remaining_work": True,
        "non_execution_boundary_ok": non_execution_boundary_ok,
        "file_size_governance_review_ok": fs_ok,
        "next_phase_readiness_ok": precheck_pass,
        "field_first_core_model_io_compatibility_precheck_pass": precheck_pass,
        "selected_next_route": SELECTED_NEXT_ROUTE,
        "io_review_item_count": len(items),
        "io_gap_count": len(gaps),
        "full_repo_scan_absent": file_size.get("full_repo_scan_absent") is True,
        "tmp_eval_out_scan_absent": file_size.get("tmp_eval_out_scan_absent") is True,
        "summary_index_first_reading_ok": file_size.get("summary_index_first_reading_ok") is True,
        **absence,
    }
    core_fields = build_core_go_no_go_summary_fields(
        go_conditions={k: go_values[k] for k in GO_CONDITIONS_KEYS},
        forbidden_runtime_flags=RUNTIME_FORBIDDEN_FLAGS,
        chain_trace_nodes=tuple(list(doc_s.get("chain_trace_nodes") or []) + ["field_first_model_io_precheck"]),
        go_no_go_decision=final_decision, final_decision=final_decision, next_phase=next_phase,
        template_lineage=template_lineage,
    )
    summary = {
        "phase": PHASE_ID, "scope": SCOPE, "blocker_count": len(issues), "issues": issues,
        **go_values, **core_fields, "final_decision": final_decision, "recommended_next_phase": next_phase, **meta,
    }
    md = "\n".join([
        "# Model I/O Compatibility Precheck v1",
        f"Reviewed: `{len(items)}` models | Gaps: `{len(gaps)}`",
        "Required skeleton fields: bbox, mask, track_id, text_region, transcript, timestamps, confidence, source_ref",
        f"Final decision: `{final_decision}`", f"Next: `{next_phase}`",
    ])
    report = {**go_values, "principles": PRECHECK_PRINCIPLES, "final_decision": final_decision, **meta}
    return {
        "model_io_compatibility_precheck_report": report,
        "model_io_compatibility_precheck_report_md": md,
        "model_io_review_item_registry": registry,
        "model_io_to_candidate_mapping": mapping,
        "candidate_schema_compatibility_matrix": compat,
        "skeleton_schema_adjustment_plan": adjust,
        "model_io_gap_register": gap_reg,
        "field_first_skeleton_io_requirements": skel_io,
        "candidate_common_payload_requirements": common_payload,
        "next_route_decision": next_route,
        "do_not_misclassify_rules": misclassify,
        "file_size_governance_review": {**file_size, **meta},
        "summary": summary,
    }
