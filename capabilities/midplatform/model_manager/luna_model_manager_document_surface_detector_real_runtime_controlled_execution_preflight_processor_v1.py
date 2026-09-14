# -*- coding: utf-8 -*-
"""Luna Document Surface Detector — controlled execution preflight processor v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

from capabilities.midplatform.model_manager.runtime.document_surface.controlled_execution_planning.document_surface_controlled_input_registry_v1 import (
    CONTROLLED_IMAGE_REGISTRY,
)
from capabilities.midplatform.model_manager.runtime.document_surface.controlled_execution_preflight.document_surface_abort_policy_preflight_v1 import (
    REQUIRED_ABORT_IDS,
    run_abort_policy_preflight,
)
from capabilities.midplatform.model_manager.runtime.document_surface.controlled_execution_preflight.document_surface_cv2_preflight_check_v1 import (
    CV2_PROCESSING_EXECUTED,
    run_cv2_preflight_check,
)
from capabilities.midplatform.model_manager.runtime.document_surface.controlled_execution_preflight.document_surface_input_registry_preflight_v1 import (
    run_input_registry_preflight,
)
from capabilities.midplatform.model_manager.runtime.document_surface.controlled_execution_preflight.document_surface_output_boundary_preflight_v1 import (
    run_output_boundary_preflight,
)
from capabilities.midplatform.model_manager.runtime.document_surface.controlled_execution_preflight.document_surface_preflight_adapter_v1 import (
    NEXT_PHASE_CV2_REVIEW,
    NEXT_PHASE_DRYRUN,
    run_controlled_execution_preflight,
    run_protocol_compliance_preflight,
)
from capabilities.midplatform.model_manager.runtime.document_surface.controlled_execution_preflight.document_surface_trace_schema_preflight_v1 import (
    run_trace_schema_preflight,
)


def _repo() -> Path:
    return Path.cwd()


def run_cv2_dependency_preflight_case() -> Dict[str, Any]:
    r = run_cv2_preflight_check()
    return {
        "scenario": "case_a_cv2_dependency_preflight",
        "import_attempted": r.get("cv2_import_attempted") is True,
        "no_processing": r.get("no_cv2_processing_executed") is True and CV2_PROCESSING_EXECUTED is False,
        "no_silent_install": r.get("no_silent_install") is True,
        "blocked_if_missing": r.get("next_action") == "dependency_admission_review" if not r.get("cv2_available_candidate") else True,
    }


def run_controlled_input_registry_case() -> Dict[str, Any]:
    r = run_input_registry_preflight(repo_root=_repo())
    return {
        "scenario": "case_b_controlled_input_registry",
        "dir_exists": r.get("controlled_input_directory_exists") is True,
        "schema_valid": r.get("registry_schema_valid") is True,
        "paths_ok": r.get("all_paths_in_controlled_scope") is True,
        "no_content_read": r.get("no_image_content_read") is True,
    }


def run_blocked_invalid_input_path_case() -> Dict[str, Any]:
    path = _repo() / "capabilities/midplatform/model_manager/runtime/document_surface/controlled_execution_planning/document_surface_abort_condition_policy_v1.json"
    pol = json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}
    by_id = {c.get("abort_id"): c for c in (pol.get("abort_conditions") or [])}
    input_abort = by_id.get("input_not_in_registry")
    bad_ref = "/Users/evil/outside.png"
    in_registry = any(img.get("image_ref") == bad_ref for img in CONTROLLED_IMAGE_REGISTRY)
    return {
        "scenario": "case_c_blocked_invalid_input_path",
        "input_not_in_registry_abort_defined": input_abort is not None,
        "bad_path_not_in_registry": not in_registry,
        "abort_has_next_action": bool(input_abort and input_abort.get("next_action")),
        "no_read": True,
    }


def run_output_boundary_case() -> Dict[str, Any]:
    r = run_output_boundary_preflight(repo_root=_repo())
    return {
        "scenario": "case_d_output_boundary",
        "tmp_root": r.get("output_root_in_tmp_eval_out") is True,
        "no_prod": r.get("no_production_write") is True,
        "no_training": r.get("no_training_data_write") is True,
        "no_fact": r.get("no_fact_write") is True,
    }


def run_trace_schema_case() -> Dict[str, Any]:
    r = run_trace_schema_preflight(repo_root=_repo())
    return {
        "scenario": "case_e_trace_schema",
        "fields": r.get("template_fields_present") is True,
        "ocr_off": r.get("ocr_called_false") is True,
        "vlm_off": r.get("vlm_called_false") is True,
        "layout_off": r.get("layout_called_false") is True,
        "fallback_off": r.get("fallback_attempted_false") is True,
    }


def run_abort_policy_case() -> Dict[str, Any]:
    r = run_abort_policy_preflight(repo_root=_repo())
    return {
        "scenario": "case_f_abort_policy",
        "count_13": r.get("required_abort_count") == 13 and r.get("found_abort_count") >= 13,
        "complete": r.get("all_complete") is True,
        "ids": REQUIRED_ABORT_IDS,
    }


def run_protocol_compliance_retained_case() -> Dict[str, Any]:
    r = run_protocol_compliance_preflight(repo_root=_repo())
    pre = run_controlled_execution_preflight(repo_root=_repo(), write_outputs=False)
    return {
        "scenario": "case_g_protocol_compliance_retained",
        "passed": r.get("protocol_compliance_passed") is True,
        "chain_ext": pre.get("existing_midplatform_protocol_chain_extension") is True,
        "not_new_branch": pre.get("protocol_patch_not_new_branch") is True,
    }


def run_real_execution_remains_disabled_case() -> Dict[str, Any]:
    pre = run_controlled_execution_preflight(repo_root=_repo(), write_outputs=False)
    next_phase = pre.get("recommended_next_phase") or ""
    return {
        "scenario": "case_h_real_execution_remains_disabled",
        "detector_off": pre.get("detector_execution_enabled") is False,
        "real_off": pre.get("real_execution_enabled") is False,
        "controlled_next": next_phase in (NEXT_PHASE_DRYRUN, NEXT_PHASE_CV2_REVIEW, None) or "DryRun" in next_phase or "Admission" in next_phase,
        "not_uncontrolled": "uncontrolled" not in next_phase.lower(),
    }
