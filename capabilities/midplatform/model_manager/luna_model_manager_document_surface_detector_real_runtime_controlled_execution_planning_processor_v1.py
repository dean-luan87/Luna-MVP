# -*- coding: utf-8 -*-
"""Luna Document Surface Detector — controlled execution planning processor v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

from capabilities.midplatform.model_manager.runtime.document_surface.controlled_execution_planning.document_surface_controlled_execution_planning_adapter_v1 import (
    RECOMMENDED_NEXT_PHASE,
    run_controlled_execution_planning,
)
from capabilities.midplatform.model_manager.runtime.document_surface.controlled_execution_planning.document_surface_controlled_execution_smoke_plan_v1 import (
    build_controlled_smoke_plan,
)
from capabilities.midplatform.model_manager.runtime.document_surface.controlled_execution_planning.document_surface_controlled_input_registry_v1 import (
    build_controlled_input_registry_plan,
)
from capabilities.midplatform.model_manager.runtime.document_surface.controlled_execution_planning.document_surface_controlled_output_policy_v1 import (
    build_controlled_output_policy,
)
from capabilities.midplatform.model_manager.runtime.document_surface.controlled_execution_planning.document_surface_controlled_execution_contract_v1 import (
    build_controlled_execution_trace_template,
)
from capabilities.midplatform.model_manager.runtime.document_surface.controlled_execution_planning.document_surface_cv2_dependency_admission_v1 import (
    CV2_IMPORTED_IN_PLANNING,
    build_cv2_dependency_admission_plan,
)


def _repo() -> Path:
    return Path.cwd()


def run_cv2_dependency_admission_planning() -> Dict[str, Any]:
    adm = build_cv2_dependency_admission_plan()
    return {
        **adm,
        "scenario": "case_a_cv2_dependency_admission_planning",
        "not_admitted": adm.get("cv2_dependency_not_admitted") is True,
        "phase_only": adm.get("allowed_import_phase") == "controlled_execution_only",
        "no_import": CV2_IMPORTED_IN_PLANNING is False,
        "no_silent": adm.get("no_silent_install") is True,
    }


def run_input_output_boundary_planning() -> Dict[str, Any]:
    inp = build_controlled_input_registry_plan()
    out = build_controlled_output_policy()
    return {
        "scenario": "case_b_input_output_boundary_planning",
        "input_defined": inp.get("image_count", 0) >= 6,
        "output_restricted": out.get("no_production_write") is True,
        "no_arbitrary": inp.get("no_arbitrary_input_directory") is True,
        "no_prod_write": out.get("no_runtime_registry_activation") is True,
    }


def run_abort_condition_planning() -> Dict[str, Any]:
    path = _repo() / "capabilities/midplatform/model_manager/runtime/document_surface/controlled_execution_planning/document_surface_abort_condition_policy_v1.json"
    pol = json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}
    conditions = pol.get("abort_conditions") or []
    complete = all(
        c.get("abort_reason") and c.get("next_action") and c.get("forbidden_fallback")
        for c in conditions
    )
    return {
        "scenario": "case_c_abort_condition_planning",
        "count": len(conditions),
        "at_least_12": len(conditions) >= 12,
        "complete": complete,
    }


def run_trace_schema_planning() -> Dict[str, Any]:
    trace = build_controlled_execution_trace_template()
    path = _repo() / "capabilities/midplatform/model_manager/runtime/document_surface/controlled_execution_planning/document_surface_runtime_trace_schema_v1.json"
    schema = json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}
    required = schema.get("required") or []
    return {
        "scenario": "case_d_trace_schema_planning",
        "fields_complete": all(f in trace for f in required),
        "ocr_false": trace.get("ocr_called") is False,
        "vlm_false": trace.get("vlm_called") is False,
        "layout_false": trace.get("layout_called") is False,
        "no_fallback": trace.get("fallback_attempted") is False,
    }


def run_controlled_smoke_plan_case() -> Dict[str, Any]:
    plan = build_controlled_smoke_plan()
    return {
        "scenario": "case_e_controlled_smoke_plan",
        "cases": plan.get("case_count"),
        "at_least_6": plan.get("at_least_six_cases") is True,
        "no_exec": plan.get("no_real_execution_in_planning") is True,
    }


def run_protocol_compliance_retained() -> Dict[str, Any]:
    result = run_controlled_execution_planning(repo_root=_repo(), write_outputs=False)
    return {
        "scenario": "case_f_protocol_compliance_retained",
        "chain_ext": result.get("existing_midplatform_protocol_chain_extension") is True,
        "not_new_branch": result.get("protocol_patch_not_new_branch") is True,
        "required": result.get("protocol_compliance_check") == "required",
    }


def run_next_phase_gate() -> Dict[str, Any]:
    result = run_controlled_execution_planning(repo_root=_repo(), write_outputs=False)
    return {
        "scenario": "case_g_next_phase_gate",
        "real_off": result.get("real_execution_enabled") is False,
        "preflight": result.get("recommended_next_phase") == RECOMMENDED_NEXT_PHASE,
        "not_direct": "Preflight" in (result.get("recommended_next_phase") or ""),
    }
