# -*- coding: utf-8 -*-
"""Model Manager — document_surface_detector_v1 registry entry v1."""

from __future__ import annotations

from typing import Any, Dict

DOCUMENT_SURFACE_RUNTIME_REGISTRY: Dict[str, Dict[str, Any]] = {
    "document_surface_detector_v1": {
        "runtime_id": "document_surface_detector_v1",
        "capability": "detect_document_surface",
        "output_type": "document_surface_candidate",
        "runtime_module": "runtime/document_surface/",
        "request_builder": "document_surface_detector_request_builder_v1.py",
        "response_parser": "document_surface_detector_response_parser_v1.py",
        "evidence_normalizer": "document_surface_detector_evidence_normalizer_v1.py",
        "dryrun_adapter": "dryrun/document_surface_detector_dryrun_adapter_v1.py",
        "dryrun_fixture_runtime": "dryrun/document_surface_detector_fixture_runtime_v1.py",
        "planning_only": True,
        "dryrun_validated": True,
        "implementation_planning_ready": True,
        "implementation_dryrun_validated": True,
        "implementation_post_review_ready": True,
        "controlled_execution_planning_ready": True,
        "controlled_execution_preflight_ready": True,
        "controlled_execution_dryrun_ready": True,
        "controlled_execution_post_review_ready": True,
        "controlled_execution_iteration_planning_ready": True,
        "controlled_execution_iteration_dryrun_ready": True,
        "controlled_execution_iteration_post_review_ready": True,
        "controlled_execution_iteration_v2_planning_ready": True,
        "option_b_candidate_route_dryrun_ready": True,
        "option_b_candidate_route_post_review_ready": True,
        "option_b_dependency_and_model_candidate_admission_planning_ready": True,
        "option_b_dependency_and_model_candidate_admission_dryrun_ready": True,
        "option_b_dependency_and_model_candidate_admission_post_review_ready": True,
        "option_b_model_skill_admission_protocol_alignment_planning_ready": True,
        "option_b_model_skill_admission_protocol_alignment_dryrun_ready": True,
        "option_b_model_skill_admission_protocol_alignment_post_review_ready": True,
        "option_b_preflight_planning_ready": True,
        "option_b_preflight_closure_ready": True,
        "implementation_mode_candidate": "classical_cv_boundary_v1",
        "first_real_implementation_candidate": "option_a_classical_cv_boundary",
        "first_real_lightweight_runtime": True,
        "triggers_ocr": False,
        "candidate_only": True,
    },
}


def match_capability_for_document_surface(
    *,
    attention_gate_status: str,
    required_capability: str = "detect_document_surface",
) -> Dict[str, Any]:
    """Model Manager capability match — attention gate required."""
    if attention_gate_status != "allowed":
        return {
            "match_status": "blocked_attention_gate",
            "runtime_id": None,
            "runtime_call_count": 0,
        }
    if required_capability != "detect_document_surface":
        return {"match_status": "capability_mismatch", "runtime_id": None}
    return {
        "match_status": "matched",
        "runtime_id": "document_surface_detector_v1",
        "capability": "detect_document_surface",
        "registry_ref": DOCUMENT_SURFACE_RUNTIME_REGISTRY["document_surface_detector_v1"],
    }
