# -*- coding: utf-8 -*-
"""Vision / OCR compatibility mapping for shared Provider Runtime Governance."""

from __future__ import annotations

from typing import Any, Dict, List, Tuple

from capabilities.governance.provider_abstraction_standard_alignment_planning_v1 import (
    CONSISTENCY_FIELDS,
    DOMAIN_LIST,
    STANDARD_ID,
)
from capabilities.midplatform.provider_runtime_governance.provider_runtime_governance_types_v1 import (
    DOMAIN_OCR,
    DOMAIN_VISION,
)

VISION_OCR_COMPATIBILITY_REF = "vision_ocr_provider_governance_compatibility_v1"

VISION_OCR_SHARED_FIELD_MAPPING: Dict[str, str] = {
    "provider_domain": "domain_id",
    "provider_candidate_id": "provider_ref",
    "provider_readiness_status": "registration_status",
    "provider_selection_status": "runtime_status",
    "provider_invocation_status": "runtime_status",
    "provider_output_contract": "supported_output_candidate_types",
    "adapter_ref": "adapter_ref",
    "failure_route": "fallback_mode",
    "fallback_candidate": "fallback_provider_refs",
    "boundary_status": "runtime_enable_allowed",
}

OCR_ADMISSION_GATE_EXPECTATIONS: Tuple[str, ...] = (
    "provider_status=planned_candidate",
    "invocation_allowed=false",
    "controlled_trial_required=true",
    "health_binding_required=true",
    "constitution_gate_required=true",
    "evidence_pack_required=true",
)

VISION_RUNTIME_BOUNDARY_EXPECTATIONS: Tuple[str, ...] = (
    "provider_abstraction_required=true",
    "provider_runtime_enabled=false",
    "provider_invocation_allowed=false",
    "candidate_only_output=true",
)

SHARED_GOVERNANCE_INVARIANTS: Tuple[str, ...] = (
    "provider_candidate_not_equal_selected",
    "provider_selected_not_equal_invoked",
    "admission_pass_not_equal_runtime_enable",
    "planning_go_not_equal_runtime_enabled",
    "no_provider_auto_switch",
    "no_direct_action",
    "no_direct_speech",
    "no_direct_fact_write",
)


def build_vision_ocr_combined_governance_profile_v1() -> Dict[str, Any]:
    return {
        "profile_ref": "vision_ocr_provider_governance_profile_v1",
        "domain_id": "vision_ocr",
        "domain_name": "Vision / OCR Compatibility",
        "admission_layer_ref": "provider_abstraction_standard_v1",
        "synthesis_entrypoint": "midplatform_synthesis_v1",
        "provider_refs": (
            "vision_provider_mock_fixture",
            "ocr_provider_mock_fixture",
        ),
        "supported_output_candidate_types": (
            "DetectionCandidate",
            "TrackingCandidate",
            "SceneUnderstandingCandidate",
            "ocr_result_candidate",
            "ocr_evidence_pack_candidate",
            "roi_candidate",
        ),
        "domain_risk_tags": (
            "provider_abstraction_required",
            "candidate_output_only",
            "no_spatial_evidence_candidate_pollution",
        ),
        "uses_shared_manager_skeleton": True,
        "candidate_only": True,
    }


def build_vision_provider_governance_profile_stub_v1() -> Dict[str, Any]:
    return {
        "profile_ref": "vision_provider_governance_profile_v1",
        "domain_id": DOMAIN_VISION,
        "domain_name": "Vision",
        "admission_layer_ref": "vision_module_model_profile_governance_binding_planning_v1",
        "synthesis_entrypoint": "midplatform_synthesis_v1",
        "provider_refs": (
            "vision_provider_mock_fixture",
            "yolo_family_object_detection_candidate",
            "grounded_sam_style_grounding_segmentation_candidate",
        ),
        "supported_output_candidate_types": (
            "DetectionCandidate",
            "TrackingCandidate",
            "SceneUnderstandingCandidate",
        ),
        "domain_risk_tags": (
            "controlled_frame_required",
            "no_fact_admission",
            "provider_abstraction_required",
        ),
        "uses_shared_manager_skeleton": True,
        "candidate_only": True,
    }


def build_ocr_provider_governance_profile_stub_v1() -> Dict[str, Any]:
    return {
        "profile_ref": "ocr_provider_governance_profile_v1",
        "domain_id": DOMAIN_OCR,
        "domain_name": "OCR",
        "admission_layer_ref": "ocr_controlled_provider_planning_v1",
        "synthesis_entrypoint": "midplatform_synthesis_v1",
        "provider_refs": (
            "ocr_provider_mock_fixture",
            "ocr_provider_paddleocr_later",
            "ocr_provider_rapidocr_later",
        ),
        "supported_output_candidate_types": (
            "ocr_result_candidate",
            "ocr_evidence_pack_candidate",
            "roi_candidate",
        ),
        "domain_risk_tags": (
            "controlled_trial_required",
            "evidence_pack_required",
            "no_paddleocr_or_rapidocr_in_planning",
        ),
        "uses_shared_manager_skeleton": True,
        "candidate_only": True,
    }


def verify_vision_ocr_compatibility_v1() -> Tuple[bool, List[str], Dict[str, Any]]:
    failed: List[str] = []
    passed: List[str] = []

    if "OCR" not in DOMAIN_LIST or "Vision" not in DOMAIN_LIST:
        failed.append("provider_abstraction_domain_list_missing_ocr_or_vision")
    else:
        passed.append("provider_abstraction_domain_list_includes_ocr_and_vision")

    if STANDARD_ID != "provider_abstraction_standard_v1":
        failed.append("provider_abstraction_standard_id_mismatch")
    else:
        passed.append("provider_abstraction_standard_id_ok")

    required_shared_targets = set(VISION_OCR_SHARED_FIELD_MAPPING.values())
    for field in ("domain_id", "provider_ref", "registration_status", "runtime_status"):
        if field not in required_shared_targets:
            failed.append(f"shared_field_mapping_missing_target:{field}")

    for invariant in SHARED_GOVERNANCE_INVARIANTS:
        passed.append(f"invariant_declared:{invariant}")

    vision_profile = build_vision_provider_governance_profile_stub_v1()
    ocr_profile = build_ocr_provider_governance_profile_stub_v1()

    for profile_name, profile in (("vision", vision_profile), ("ocr", ocr_profile)):
        if profile.get("uses_shared_manager_skeleton") is not True:
            failed.append(f"{profile_name}.uses_shared_manager_skeleton=false")
        if not profile.get("provider_refs"):
            failed.append(f"{profile_name}.provider_refs_empty")
        if profile.get("candidate_only") is not True:
            failed.append(f"{profile_name}.candidate_only_not_true")

    ocr_gate_ok = len(OCR_ADMISSION_GATE_EXPECTATIONS) >= 6
    vision_boundary_ok = len(VISION_RUNTIME_BOUNDARY_EXPECTATIONS) >= 4
    if not ocr_gate_ok:
        failed.append("ocr_admission_gate_expectations_incomplete")
    if not vision_boundary_ok:
        failed.append("vision_runtime_boundary_expectations_incomplete")

    compatibility_doc = {
        "compatibility_ref": VISION_OCR_COMPATIBILITY_REF,
        "provider_abstraction_standard_id": STANDARD_ID,
        "consistency_fields": list(CONSISTENCY_FIELDS),
        "shared_field_mapping": dict(VISION_OCR_SHARED_FIELD_MAPPING),
        "ocr_admission_gate_expectations": list(OCR_ADMISSION_GATE_EXPECTATIONS),
        "vision_runtime_boundary_expectations": list(VISION_RUNTIME_BOUNDARY_EXPECTATIONS),
        "shared_governance_invariants": list(SHARED_GOVERNANCE_INVARIANTS),
        "vision_profile_stub": vision_profile,
        "ocr_profile_stub": ocr_profile,
    }

    return len(failed) == 0, failed, compatibility_doc
