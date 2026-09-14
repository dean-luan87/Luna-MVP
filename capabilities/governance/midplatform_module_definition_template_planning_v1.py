# -*- coding: utf-8 -*-
"""Midplatform Module Definition Template Planning v1 — establish default module design schema."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.midplatform_decision_center_module_planning_v1 import (
    FINAL_DECISION_GO as DC_MODULE_PLANNING_FINAL_GO,
)
from capabilities.governance.midplatform_module_definition_template_v1 import (
    FAILURE_TRACE_FIELDS,
    INPUT_CONTRACT_BASE_FIELDS,
    OUTPUT_CONTRACT_BASE_FIELDS,
    RUNTIME_BOUNDARY_FIELDS,
    SYSTEM_LAYERS,
    TEMPLATE_ID,
    TEMPLATE_PRINCIPLE,
    TEMPLATE_SECTIONS,
    decision_center_exemplar,
    template_schema,
    validate_module_definition,
)
from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID

PHASE_ID = "Phase-Midplatform-Module-Definition-Template-Planning-v1-001"
SCOPE = "midplatform_module_definition_template_planning_only"
SOURCE_CHAIN = "midplatform_module_definition_template_planning_v1"

UPSTREAM_DC_MODULE_PLANNING_FINAL = DC_MODULE_PLANNING_FINAL_GO

FINAL_DECISION_GO = (
    "MIDPLATFORM_MODULE_DEFINITION_TEMPLATE_PLANNING_READY_FOR_ADOPTION"
)
FINAL_DECISION_HOLD = (
    "MIDPLATFORM_MODULE_DEFINITION_TEMPLATE_PLANNING_HOLD_FOR_ISSUE_REVIEW"
)
NEXT_PHASE_GO = "Phase-Midplatform-Decision-Center-Module-DryRunAndReview-v1-001"
NEXT_PHASE_HOLD = "Phase-Midplatform-Module-Definition-Template-Issue-Review-v1-001"

NON_CLAIMS: Tuple[str, ...] = (
    "Template Planning GO ≠ all modules already migrated to template",
    "exemplar defined ≠ decision center runtime enabled",
    "template adoption required ≠ immediate module rewrite",
)

BOUNDARY_TRUE: Tuple[str, ...] = (
    "midplatform_module_definition_template_planning_only",
    "template_established_as_default",
)

BOUNDARY_FALSE: Tuple[str, ...] = (
    "runtime_enabled_now",
    "all_modules_rewritten_now",
    "decision_center_runtime_enabled_now",
    "provider_invoked_now",
    "memory_written_now",
    "world_model_written_now",
    "user_facing_output_generated_now",
)

DEFAULT_OUTPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_module_definition_template_planning"
)


def _planning_meta() -> Dict[str, Any]:
    meta = {
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "source_chain": SOURCE_CHAIN,
        "selected_provider_for_execution": None,
        "template_principle": TEMPLATE_PRINCIPLE,
    }
    for field in BOUNDARY_TRUE:
        meta[field] = True
    for field in BOUNDARY_FALSE:
        meta[field] = False
    return meta


def _try_read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def run_midplatform_module_definition_template_planning_v1(
    *,
    midplatform_decision_center_module_planning_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []

    dc_root = Path(midplatform_decision_center_module_planning_root).expanduser().resolve()
    dc_sm = _try_read_json(dc_root / "summary.json") or {}
    dc_vr = _try_read_json(dc_root / "verifier_report.json") or {}

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    meta = {
        **_planning_meta(),
        "upstream_decision_center_module_planning_root": str(dc_root),
        "output_root": str(out_root),
    }

    if dc_vr.get("verifier") != "GO":
        blockers.append("Decision Center Module Planning verifier must be GO")
    if dc_sm.get("final_decision") != UPSTREAM_DC_MODULE_PLANNING_FINAL:
        blockers.append("decision center module planning final_decision mismatch")

    exemplar = decision_center_exemplar()
    exemplar_valid, exemplar_issues = validate_module_definition(exemplar)

    if not exemplar_valid:
        blockers.extend(exemplar_issues)

    input_ok = len(blockers) == 0

    dc_input_review = {
        "review_id": "decision_center_module_planning_input_review_v1",
        "decision_center_module_planning_verifier": dc_vr.get("verifier"),
        "decision_center_module_planning_final": dc_sm.get("final_decision"),
        "exemplar_source_module_id": "midplatform_decision_center_v1",
        "review_pass": input_ok,
        "blockers": blockers,
        **meta,
    }

    policy = {
        "policy_id": "midplatform_module_definition_template_policy_v1",
        "phase": PHASE_ID,
        "scope": SCOPE,
        "template_id": TEMPLATE_ID,
        "template_principle": TEMPLATE_PRINCIPLE,
        "adoption_mandatory_for_future_modules": True,
        "adoption_required_for_module_updates": True,
        "ten_section_structure": list(TEMPLATE_SECTIONS),
        "system_layers": list(SYSTEM_LAYERS),
        "definition_rule": (
            "不得只写'这个模块做什么'，必须写清："
            "关系、输入、加工、输出、准则、约束、边界、追溯"
        ),
        **meta,
    }

    template_doc = {
        **template_schema(),
        "input_contract_base_fields": list(INPUT_CONTRACT_BASE_FIELDS),
        "output_contract_base_fields": list(OUTPUT_CONTRACT_BASE_FIELDS),
        "runtime_boundary_fields": list(RUNTIME_BOUNDARY_FIELDS),
        "failure_trace_fields": list(FAILURE_TRACE_FIELDS),
        **meta,
    }

    adoption_requirement = {
        "requirement_id": "template_adoption_requirement_v1",
        "all_future_midplatform_modules_must_use_template": True,
        "minimum_sections": len(TEMPLATE_SECTIONS),
        "required_layers_reference": list(SYSTEM_LAYERS),
        "first_exemplar_module_id": "midplatform_decision_center_v1",
        "exemplar_valid": exemplar_valid,
        "exemplar_issues": exemplar_issues,
        **meta,
    }

    exemplar_doc = {
        **exemplar,
        "exemplar_valid": exemplar_valid,
        "exemplar_issues": exemplar_issues,
        **meta,
    }

    planning_pass = input_ok and exemplar_valid

    planning_decision = {
        "decision_id": "midplatform_module_definition_template_planning_decision_v1",
        "planning_pass": planning_pass,
        "high_risk": not planning_pass,
        "final_decision": FINAL_DECISION_GO if planning_pass else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if planning_pass else NEXT_PHASE_HOLD,
        "template_established": planning_pass,
        **meta,
    }

    non_claims = {
        "register_id": "non_claims_register_v1",
        "non_claims": list(NON_CLAIMS),
        **meta,
    }

    summary = {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "boundary_ok": planning_pass,
        "violations": list(blockers),
        "planning_pass": planning_pass,
        "final_decision": planning_decision["final_decision"],
        "recommended_next_phase": planning_decision["recommended_next_phase"],
        **meta,
    }

    return {
        "midplatform_module_definition_template_policy": policy,
        "decision_center_module_planning_input_review": dc_input_review,
        "midplatform_module_definition_template": template_doc,
        "decision_center_module_full_definition_exemplar": exemplar_doc,
        "template_adoption_requirement": adoption_requirement,
        "non_claims_register": non_claims,
        "midplatform_module_definition_template_planning_decision": planning_decision,
        "summary": summary,
    }
