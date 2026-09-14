# -*- coding: utf-8 -*-
"""Document Surface Implementation — contract reviewer v1."""

from __future__ import annotations

from typing import Any, Dict

from capabilities.midplatform.model_manager.runtime.document_surface.implementation_planning.document_surface_real_runtime_contract_v1 import (
    build_implementation_input_contract,
    build_implementation_output_contract,
    validate_contract_alignment,
)
from capabilities.midplatform.model_manager.runtime.document_surface.implementation_planning.document_surface_real_runtime_failure_modes_v1 import (
    FAILURE_MODES,
    build_failure_modes_registry,
)


INPUT_REQUIRED = (
    "source_region_id", "attention_gate_status", "goal_context",
    "allowed_capabilities", "forbidden_capabilities", "candidate_only",
)

OUTPUT_REQUIRED = (
    "runtime_id", "implementation_mode_candidate", "document_surface_candidates",
    "relation_hint_candidates", "runtime_status_candidate", "candidate_only", "not_fact",
)

REQUIRED_FAILURE_MODES = (
    "no_document_surface_found", "low_contrast_boundary", "severe_occlusion",
    "curved_or_folded_surface", "multiple_overlapping_surfaces", "reflective_surface_confusion",
    "screen_surface_confusion", "background_texture_false_positive",
    "runtime_dependency_missing", "runtime_timeout", "unsupported_image_format",
)


def review_implementation_contract() -> Dict[str, Any]:
    inp = build_implementation_input_contract(field_context_candidate={})
    out = build_implementation_output_contract()
    alignment = validate_contract_alignment(input_contract=inp, output_contract=out)
    in_ok = all(k in inp for k in INPUT_REQUIRED) and inp.get("candidate_only") is True
    out_ok = all(k in out for k in OUTPUT_REQUIRED) and out.get("candidate_only") is True and out.get("not_fact") is True
    field_ok = "field_context_candidate" in inp and "max_runtime_cost" in inp

    fm_reg = build_failure_modes_registry()
    fm_ids = {fm["failure_mode_id"] for fm in FAILURE_MODES}
    fm_ok = all(fid in fm_ids for fid in REQUIRED_FAILURE_MODES) and fm_reg.get("all_modes_complete")

    return {
        "review_id": "document_surface_implementation_contract_review_v1",
        "input_contract_complete": in_ok and field_ok,
        "output_contract_complete": out_ok,
        "aligned_with_dryrun": alignment.get("aligned_with_dryrun") is True,
        "failure_modes_complete": fm_ok,
        "failure_mode_count": fm_reg.get("failure_mode_count"),
        "passed": in_ok and out_ok and field_ok and alignment.get("aligned_with_dryrun") and fm_ok,
    }
