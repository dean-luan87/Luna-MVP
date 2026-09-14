from __future__ import annotations

from typing import Any, Dict, Tuple

from .types_v1 import (
    ADAPTER_REF,
    PROVIDER_CONTRACT_REF,
    PROVIDER_REF,
    WORKFLOW_REF,
    MODEL_ASSET_REF,
)


def structural_cases_v1() -> Tuple[Dict[str, Any], ...]:
    common = {
        "observation_request_ref": "observation-request:exit-poc",
        "capability_requirement_ref": "capability-requirement:object-detection-ocr",
        "provider_admission_ref": "provider-admission:roboflow:poc",
        "runtime_admission_ref": "runtime-admission:roboflow:poc",
        "capability_model_binding_ref": "capability-model-binding:exit-poc",
        "model_provider_binding_ref": "model-provider-binding:roboflow:poc",
        "provider_ref": PROVIDER_REF,
        "provider_contract_ref": PROVIDER_CONTRACT_REF,
        "workflow_ref": WORKFLOW_REF,
        "workflow_output_mapping": {
            "detections": "$predictions",
        },
        "model_refs": (MODEL_ASSET_REF,),
        "image_ref": "capabilities/test_assets/p1/mobile_sam/mobile_sam_real_local_image_street_scene_v1.png",
        "frame_ref": "frame:exit-poc:observation-1",
        "roi_ref": "roi:room-front",
        "requested_capabilities": ("object_detection",),
        "trace_ref": "trace:roboflow:poc:concern-exit",
        "provenance_refs": ("provenance:roboflow:poc", ADAPTER_REF),
        "source_version_refs": ("concern:v1", "grant:v1", "observation:v1", "provider-declaration:v1"),
        "grant_refs": ("grant:exit-poc:v1",),
        "constraint_refs": ("safety:bounded:v1", "permission:vision:v1", "resource:vision:poc:v1"),
    }
    return (
        {
            "case_id": "observation_1_insufficient",
            "request": {
                **common,
                "request_id": "roboflow-request:exit-poc:observation-1",
            },
            "native_payload": {
                "predictions": [
                    {"id": "door-a", "class": "door", "confidence": 0.62, "bbox": [40, 30, 220, 420]},
                    {"id": "door-b", "class": "door", "confidence": 0.58, "bbox": [300, 40, 480, 420]},
                ],
                "ocr": [],
            },
            "semantic_assessment": {
                "source_owner": "A",
                "hypothesis_id": "hypothesis:exit:cycle-1",
                "hypothesis_statement_candidate": "multiple exit candidates remain unresolved pending signage evidence",
                "unknown_refs": ("unknown:exit-sign-text",),
                "confidence_candidate": "uncertain",
                "state": "ACTIVE_CANDIDATE",
                "sufficiency_status": "INSUFFICIENT",
                "sufficiency_reason": "door geometry exists but signage is unresolved",
                "information_gap": ("targeted OCR for exit signage",),
                "expected_evidence": ("VISION_DETECTION", "OCR_TEXT_EVIDENCE"),
                "target_coverage": True,
                "semantic_coverage": False,
                "spatial_coverage": True,
                "observation_demand_ref": "observation-demand:exit-poc",
                "next_observation_request_ref": "observation-request:exit-poc:ocr-followup",
                "next_step_decision_ref": "a-next-step:exit-poc:cycle-1",
            },
        },
        {
            "case_id": "observation_2_sufficiency_candidate",
            "request": {
                **common,
                "request_id": "roboflow-request:exit-poc:observation-2",
                "frame_ref": "frame:exit-poc:observation-2",
                "roi_ref": "roi:signage-followup",
                "image_ref": "capabilities/test_assets/p1/ocr/ocr_real_image_shop_sign_nostalgic_flavor_v1_001.png",
            },
            "native_payload": {
                "predictions": [
                    {"id": "door-followup", "class": "door", "confidence": 0.91, "bbox": [50, 30, 240, 430]},
                ],
                "ocr": [
                    {"id": "sign-followup", "text": "signage-candidate-text", "confidence": 0.89, "bbox": [70, 20, 180, 70], "region_ref": "roi:signage-followup"},
                ],
            },
            "semantic_assessment": {
                "source_owner": "A",
                "hypothesis_id": "hypothesis:exit:cycle-2",
                "hypothesis_statement_candidate": "A-owned revised exit hypothesis candidate after corroborating signage evidence",
                "revision_parent_ref": "hypothesis:exit:cycle-1",
                "unknown_refs": (),
                "confidence_candidate": "candidate-supported",
                "state": "REVISED_CANDIDATE",
                "sufficiency_status": "SUFFICIENT",
                "sufficiency_reason": "detection and targeted OCR cover the current information need",
                "expected_evidence": ("VISION_DETECTION", "OCR_TEXT_EVIDENCE"),
                "target_coverage": True,
                "semantic_coverage": True,
                "spatial_coverage": True,
                "source_diversity": 1,
            },
        },
    )


def rf_detr_normalization_cases_v1() -> Tuple[Dict[str, Any], ...]:
    """Synthetic RF-DETR payloads shaped like the observed SDK envelope."""

    base_request = dict(structural_cases_v1()[0]["request"])
    base_request.update(
        {
            "requested_capabilities": ("object_detection",),
            "model_refs": (MODEL_ASSET_REF,),
            "workflow_output_mapping": {"detections": "$[0].model_output_3.predictions"},
        }
    )

    def envelope(predictions: Any) -> list[Dict[str, Any]]:
        return [
            {
                "model_output": "synthetic-bounded-output-1",
                "model_output_2": "synthetic-bounded-output-2",
                "model_output_3": {
                    "image": {"path_ref": "synthetic-image-ref", "metadata": "bounded"},
                    "predictions": predictions,
                },
            }
        ]

    def case(case_id: str, predictions: Any, *, expected_accepted: bool, expected_detection_count: int) -> Dict[str, Any]:
        request = dict(base_request)
        request["request_id"] = f"roboflow-request:rf-detr-normalization:{case_id}"
        request["trace_ref"] = f"trace:roboflow:rf-detr-normalization:{case_id}"
        return {
            "case_id": case_id,
            "request": request,
            "native_payload": envelope(predictions),
            "expected_accepted": expected_accepted,
            "expected_detection_count": expected_detection_count,
        }

    def raw_case(case_id: str, payload: Any, *, expected_accepted: bool) -> Dict[str, Any]:
        request = dict(base_request)
        request["request_id"] = f"roboflow-request:rf-detr-normalization:{case_id}"
        request["trace_ref"] = f"trace:roboflow:rf-detr-normalization:{case_id}"
        return {
            "case_id": case_id,
            "request": request,
            "native_payload": payload,
            "expected_accepted": expected_accepted,
            "expected_detection_count": 0,
        }

    return (
        case(
            "rf_detr_normal_detection",
            [{"detection_id": "det-1", "class": "door", "class_id": 1, "confidence": 0.81, "x": 10, "y": 20, "width": 100, "height": 200, "parent_id": "root"}],
            expected_accepted=True,
            expected_detection_count=1,
        ),
        case(
            "rf_detr_multiple_detections",
            [
                {"detection_id": "det-1", "class": "door", "class_id": 1, "confidence": 0.81, "x": 10, "y": 20, "width": 100, "height": 200, "parent_id": "root"},
                {"detection_id": "det-2", "class": "person", "class_id": 2, "confidence": 0.73, "x": 140, "y": 30, "width": 70, "height": 200, "parent_id": "root"},
            ],
            expected_accepted=True,
            expected_detection_count=2,
        ),
        case("rf_detr_empty_predictions", [], expected_accepted=True, expected_detection_count=0),
        case(
            "rf_detr_malformed_prediction",
            [{"detection_id": "det-malformed", "class": "door", "class_id": 1, "confidence": 0.4}],
            expected_accepted=False,
            expected_detection_count=0,
        ),
        case(
            "rf_detr_low_confidence_candidate",
            [{"detection_id": "det-low", "class": "door", "class_id": 1, "confidence": 0.05, "x": 1, "y": 2, "width": 3, "height": 4, "parent_id": "root"}],
            expected_accepted=True,
            expected_detection_count=1,
        ),
        case(
            "rf_detr_unknown_extra_field",
            [{"detection_id": "det-extra", "class": "door", "class_id": 1, "confidence": 0.66, "x": 1, "y": 2, "width": 3, "height": 4, "parent_id": "root", "unmodeled_field": "provider-only"}],
            expected_accepted=True,
            expected_detection_count=1,
        ),
        raw_case(
            "rf_detr_missing_model_output_3",
            [{"model_output": "synthetic-bounded-output-1", "model_output_2": "synthetic-bounded-output-2"}],
            expected_accepted=False,
        ),
        raw_case(
            "rf_detr_missing_predictions",
            [{"model_output_3": {"image": {"path_ref": "synthetic-image-ref"}}}],
            expected_accepted=False,
        ),
        raw_case(
            "rf_detr_predictions_wrong_type",
            [{"model_output_3": {"image": {"path_ref": "synthetic-image-ref"}, "predictions": {"not": "a-sequence"}}}],
            expected_accepted=False,
        ),
    )


__all__ = ["rf_detr_normalization_cases_v1", "structural_cases_v1"]
