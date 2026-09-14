# -*- coding: utf-8 -*-
"""Document Surface — Option B validation adapter v1."""

from __future__ import annotations

from typing import Any, Dict

from capabilities.midplatform.model_manager.runtime.document_surface.option_b_candidate_route_dryrun.document_surface_option_b_output_contract_v1 import (
    validate_option_b_output_contract,
)


def validate_option_b_dryrun_outputs(outputs: Dict[str, Any]) -> Dict[str, Any]:
    contract = validate_option_b_output_contract(outputs)
    admission = outputs.get("admission") or {}
    route = outputs.get("route_selection") or {}
    conflict = outputs.get("conflict_policy") or {}

    blockers = []
    if admission.get("execution_allowed") is True:
        blockers.append("execution_allowed_leak")
    if admission.get("active_model_id"):
        blockers.append("active_model_id_leak")
    if admission.get("segmentation_mask_result"):
        blockers.append("segmentation_result_leak")
    if route.get("execution_decision"):
        blockers.append("execution_decision_leak")
    if route.get("fallback_decision"):
        blockers.append("fallback_decision_leak")
    if conflict.get("silent_fallback") is True:
        blockers.append("silent_fallback")
    if conflict.get("confidence_auto_override") is True:
        blockers.append("confidence_auto_override")

    return {
        "validation_status_candidate": "passed" if not blockers and contract.get("contract_compliant") else "aborted",
        "contract": contract,
        "blockers": blockers,
        "no_fact_output": outputs.get("not_fact") is True,
        "no_ocr_leak": "ocr" not in str(outputs).lower() or "no_ocr" in str(outputs).lower(),
        "candidate_only": True,
        "not_fact": True,
    }
