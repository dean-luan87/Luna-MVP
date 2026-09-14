# -*- coding: utf-8 -*-
"""Document Surface — Option B model candidate admission dryrun v1."""

from __future__ import annotations

from typing import Any, Dict

from capabilities.midplatform.model_manager.runtime.document_surface.option_b_admission_dryrun.document_surface_option_b_abort_rollback_dryrun_v1 import (
    build_abort_rollback_dryrun,
)
from capabilities.midplatform.model_manager.runtime.document_surface.option_b_admission_dryrun.document_surface_option_b_dependency_admission_dryrun_v1 import (
    run_dependency_admission_dryrun,
)
from capabilities.midplatform.model_manager.runtime.document_surface.option_b_admission_dryrun.document_surface_option_b_license_weight_dryrun_v1 import (
    run_license_weight_dryrun,
)
from capabilities.midplatform.model_manager.runtime.document_surface.option_b_admission_dryrun.document_surface_option_b_output_contract_dryrun_v1 import (
    run_output_contract_dryrun,
)
from capabilities.midplatform.model_manager.runtime.document_surface.option_b_admission_dryrun.document_surface_option_b_wrapper_requirement_dryrun_v1 import (
    run_wrapper_requirement_dryrun,
)

EXPECTED_STATUS = {
    "family_a_classical_helper_ok_candidate": "admitted_for_preflight_candidate",
    "family_a_requires_uncontrolled_binary": "blocked_dependency_not_admitted_candidate",
    "family_b_lightweight_sam_like_weight_missing": "blocked_model_weight_missing_candidate",
    "family_b_sam_like_license_unknown": "blocked_license_not_cleared_candidate",
    "family_b_sam_like_caption_or_text_default": "blocked_or_requires_wrapper_candidate",
    "family_c_document_specific_surface_model_ok_for_preflight": "admitted_for_preflight_candidate",
    "family_c_document_model_outputs_document_type_fact": "blocked_output_contract_violation_candidate",
    "family_d_depth_geometric_requires_hardware": "blocked_hardware_requirement_missing_candidate",
}


def run_model_candidate_admission_dryrun(*, candidate: Dict[str, Any]) -> Dict[str, Any]:
    cid = candidate["model_candidate_id"]
    dep = run_dependency_admission_dryrun(candidate=candidate)
    lic = run_license_weight_dryrun(candidate=candidate)
    contract = run_output_contract_dryrun(candidate=candidate)
    wrapper = run_wrapper_requirement_dryrun(candidate=candidate)

    status = "admitted_for_preflight_candidate"
    if dep.get("dependency_admission_result_candidate", "").startswith("blocked"):
        status = dep["dependency_admission_result_candidate"]
    elif lic.get("license_weight_result_candidate", "").startswith("blocked"):
        status = lic["license_weight_result_candidate"]
    elif contract.get("output_contract_result_candidate") == "blocked_or_requires_wrapper_candidate":
        status = "blocked_or_requires_wrapper_candidate"
    elif contract.get("output_contract_result_candidate", "").startswith("blocked"):
        status = contract["output_contract_result_candidate"]
    elif wrapper.get("wrapper_missing_blocked"):
        status = "blocked_or_requires_wrapper_candidate"

    abort = build_abort_rollback_dryrun(
        admission_status=status,
        abort_reason=None if status.startswith("admitted") else status,
    )

    expected = EXPECTED_STATUS.get(cid)
    expectation_met = status == expected

    return {
        "model_candidate_id": cid,
        "admission_status_candidate": status,
        "expected_admission_status": expected,
        "expectation_met": expectation_met,
        "dependency_admission": dep,
        "license_weight": lic,
        "output_contract": contract,
        "wrapper_requirement": wrapper,
        "abort_rollback": abort,
        "execution_allowed": False,
        "active_status": False,
        "active_model_selected": False,
        "candidate_only": True,
        "not_fact": True,
    }
