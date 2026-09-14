# -*- coding: utf-8 -*-
"""Document Surface — Option B admission dryrun v1."""

from __future__ import annotations

from typing import Any, Dict
from uuid import uuid4

from capabilities.midplatform.model_manager.runtime.document_surface.option_b_candidate_route_dryrun.document_surface_option_b_types_v1 import (
    OPTION_B_STATUS,
)


def run_option_b_admission_dryrun(
    *,
    route_request_id: str | None = None,
    case_profile: str,
    field_context_candidate: Dict[str, Any] | None = None,
    attention_gate_status: str = "allowed",
    ownership_problem_type: str = "document_surface_investigation",
    option_a_result_profile: Dict[str, Any] | None = None,
) -> Dict[str, Any]:
    if attention_gate_status != "allowed":
        return {
            "option_b_admission_candidate": False,
            "admission_status_candidate": "blocked_attention_gate",
            "execution_allowed": False,
            "candidate_only": True,
            "not_fact": True,
        }
    return {
        "route_request_id": route_request_id or f"rr_{uuid4().hex[:10]}",
        "case_profile": case_profile,
        "field_context_candidate": field_context_candidate or {},
        "attention_gate_status": attention_gate_status,
        "ownership_problem_type": ownership_problem_type,
        "option_a_result_profile": option_a_result_profile or {},
        "option_b_status": OPTION_B_STATUS,
        "option_b_admission_candidate": True,
        "admission_status_candidate": "candidate_route_admitted_planning_only",
        "dependency_admission_required": True,
        "execution_allowed": False,
        "model_download_allowed": False,
        "training_allowed": False,
        "active_registry_update_allowed": False,
        "controlled_execution_planning_required_before_any_execution": True,
        "active_model_id": None,
        "model_execution_result": None,
        "segmentation_mask_result": None,
        "candidate_only": True,
        "not_fact": True,
    }
