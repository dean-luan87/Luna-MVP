from __future__ import annotations

from dataclasses import asdict
from typing import Any, Iterable, Mapping, Sequence, Tuple

from capabilities.midplatform.field_perception_orchestrator.integration.field_perception_real_vision_evidence_types_v1 import (
    ObservationGatewayEvidenceHandoffCandidateV1,
    VisualDetectionEvidenceCandidateV1,
)
from capabilities.midplatform.ocr_manager.module.ocr_manager_module_types_v1 import (
    OCRRawEvidenceV1,
    OCRStructuredEvidenceEnvelopeV1,
)

from .types_v1 import RoboflowNativeResultV1, RoboflowNormalizedProviderResultV1


def _tuple_unique(values: Iterable[str]) -> Tuple[str, ...]:
    return tuple(dict.fromkeys(str(value) for value in values if str(value).strip()))


def _workflow_value_at(payload: Any, path: str) -> Any:
    """Read one explicitly governed workflow output path; no key guessing."""
    normalized = str(path or "").strip()
    if normalized.startswith("$."):
        normalized = normalized[2:]
    elif normalized.startswith("$"):
        normalized = normalized[1:]
    if not normalized:
        return None
    value: Any = payload
    for segment in normalized.split("."):
        if segment.startswith("[") and segment.endswith("]"):
            segment = segment[1:-1]
        if (
            isinstance(value, Sequence)
            and not isinstance(value, (str, bytes))
            and len(value) == 1
            and isinstance(value[0], Mapping)
            and not segment.isdigit()
        ):
            # Inference SDK workflow results may wrap one image's output in a
            # single-item sequence.  Unwrap only that explicit envelope; do
            # not guess provider output keys or merge multiple image results.
            value = value[0]
        if isinstance(value, Mapping) and segment in value:
            value = value[segment]
            continue
        if isinstance(value, Sequence) and not isinstance(value, (str, bytes)) and segment.isdigit():
            index = int(segment)
            if index < 0 or index >= len(value):
                return None
            value = value[index]
            continue
        return None
    return value


def _sequence_at(payload: Any, path: str) -> Tuple[Mapping[str, Any], ...]:
    value = _workflow_value_at(payload, path)
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes)):
        return tuple(item for item in value if isinstance(item, Mapping))
    return ()


def _bbox(value: Any) -> tuple[float, float, float, float]:
    if isinstance(value, Mapping):
        if all(name in value for name in ("x", "y", "width", "height")):
            x, y = float(value["x"]), float(value["y"])
            return (x, y, x + float(value["width"]), y + float(value["height"]))
        value = value.get("bbox") or value.get("bbox_xyxy")
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes)):
        values = tuple(float(item) for item in value)
        if len(values) >= 4:
            return values[:4]
    return (0.0, 0.0, 0.0, 0.0)


def _has_detection_geometry(item: Mapping[str, Any]) -> bool:
    if all(name in item and item.get(name) not in (None, "") for name in ("x", "y", "width", "height")):
        return True
    for key in ("bbox", "bounding_box", "bbox_xyxy"):
        value = item.get(key)
        if isinstance(value, Mapping) and all(
            name in value and value.get(name) not in (None, "")
            for name in ("x", "y", "width", "height")
        ):
            return True
        if isinstance(value, Sequence) and not isinstance(value, (str, bytes)) and len(value) >= 4:
            return True
    return False


def _detection_candidates(
    native: RoboflowNativeResultV1,
    predictions: Sequence[Mapping[str, Any]],
    *,
    frame_ref: str,
    roi_ref: str,
) -> Tuple[VisualDetectionEvidenceCandidateV1, ...]:
    items = []
    for index, item in enumerate(predictions):
        detection_ref = str(item.get("id") or item.get("detection_id") or f"{native.result_id}:detection:{index}")
        evidence_ref = f"evidence:roboflow:detection:{detection_ref}"
        trace_ref = f"{native.trace_ref}:detection:{index}"
        items.append(
            VisualDetectionEvidenceCandidateV1(
                evidence_id=evidence_ref,
                provider_ref=native.provider_ref,
                model_ref=native.model_refs[0] if native.model_refs else "",
                frame_ref=frame_ref,
                detection_ref=detection_ref,
                class_candidate=str(item.get("class") or item.get("class_name") or item.get("label") or "unknown"),
                bbox=_bbox(item.get("bbox") or item.get("bounding_box") or item.get("bbox_xyxy") or item),
                confidence=float(item.get("confidence") or 0.0),
                region_ref=roi_ref,
                temporal_ref=frame_ref,
                uncertainty_refs=(f"uncertainty:{evidence_ref}",),
                contradiction_refs=tuple(str(ref) for ref in item.get("contradiction_refs") or ()),
                trace_ref=trace_ref,
                provenance_refs=_tuple_unique(
                    (*native.provenance_refs, native.provider_ref, native.workflow_ref, *native.model_refs, trace_ref)
                ),
            )
        )
    return tuple(items)


def _ocr_candidates(
    native: RoboflowNativeResultV1,
    text_items: Sequence[Mapping[str, Any]],
    *,
    frame_ref: str,
    roi_ref: str,
) -> Tuple[OCRRawEvidenceV1, ...]:
    items = []
    for index, item in enumerate(text_items):
        text = str(item.get("text") or item.get("raw_text") or item.get("value") or "")
        if not text.strip():
            continue
        evidence_id = str(item.get("id") or f"{native.result_id}:ocr:{index}")
        region_ref = str(item.get("region_ref") or roi_ref)
        items.append(
            OCRRawEvidenceV1(
                evidence_id=f"evidence:roboflow:ocr:{evidence_id}",
                raw_text=text,
                normalized_text_candidate=text.strip(),
                region_ref=region_ref,
                line_ref=str(item.get("line_ref") or f"line:{evidence_id}"),
                engine_ref=native.provider_ref,
                confidence=float(item.get("confidence") or 0.0),
                language_candidate=str(item.get("language") or "unknown"),
                bounding_geometry=item.get("bbox") or item.get("bounding_box") or {},
                source_frame_ref=frame_ref,
                captured_at=str(item.get("captured_at") or ""),
                evidence_status="candidate",
            )
        )
    return tuple(items)


def translate_roboflow_result_to_luna_evidence_v1(
    native: RoboflowNativeResultV1,
    *,
    frame_ref: str,
    roi_ref: str,
) -> RoboflowNormalizedProviderResultV1:
    """Map provider-native payload without exporting the raw provider schema."""

    if native.invalidation_refs:
        return RoboflowNormalizedProviderResultV1(
            result_id=native.result_id,
            accepted=False,
            provider_ref=native.provider_ref,
            workflow_ref=native.workflow_ref,
            model_refs=native.model_refs,
            frame_ref=frame_ref,
            roi_ref=roi_ref,
            detection_evidence=(),
            ocr_evidence=(),
            ocr_envelope=None,
            trace_ref=native.trace_ref,
            provenance_refs=native.provenance_refs,
            source_version_refs=native.source_version_refs,
            invalidation_refs=native.invalidation_refs,
            error_class="STALE_PROVIDER_RESULT",
            error_detail="invalidated provider result cannot become Evidence",
            actual_provider_response=native.actual_provider_response,
        )

    if native.error_class:
        return RoboflowNormalizedProviderResultV1(
            result_id=native.result_id,
            accepted=False,
            provider_ref=native.provider_ref,
            workflow_ref=native.workflow_ref,
            model_refs=native.model_refs,
            frame_ref=frame_ref,
            roi_ref=roi_ref,
            detection_evidence=(),
            ocr_evidence=(),
            ocr_envelope=None,
            trace_ref=native.trace_ref,
            provenance_refs=native.provenance_refs,
            source_version_refs=native.source_version_refs,
            invalidation_refs=(),
            error_class=native.error_class,
            error_detail=native.error_detail,
            actual_provider_response=native.actual_provider_response,
        )

    payload = native.payload
    detection_value = _workflow_value_at(payload, native.workflow_output_mapping.get("detections", ""))
    if not isinstance(detection_value, Sequence) or isinstance(detection_value, (str, bytes)):
        return RoboflowNormalizedProviderResultV1(
            result_id=native.result_id,
            accepted=False,
            provider_ref=native.provider_ref,
            workflow_ref=native.workflow_ref,
            model_refs=native.model_refs,
            frame_ref=frame_ref,
            roi_ref=roi_ref,
            detection_evidence=(),
            ocr_evidence=(),
            ocr_envelope=None,
            trace_ref=native.trace_ref,
            provenance_refs=native.provenance_refs,
            source_version_refs=native.source_version_refs,
            invalidation_refs=(),
            error_class="PROVIDER_RESULT_SCHEMA_INVALID",
            error_detail="governed detection output mapping must resolve to a sequence",
            actual_provider_response=native.actual_provider_response,
        )
    if any(
        not isinstance(item, Mapping)
        or not all(key in item and item.get(key) not in (None, "") for key in ("class", "confidence"))
        or not _has_detection_geometry(item)
        for item in detection_value
    ):
        return RoboflowNormalizedProviderResultV1(
            result_id=native.result_id,
            accepted=False,
            provider_ref=native.provider_ref,
            workflow_ref=native.workflow_ref,
            model_refs=native.model_refs,
            frame_ref=frame_ref,
            roi_ref=roi_ref,
            detection_evidence=(),
            ocr_evidence=(),
            ocr_envelope=None,
            trace_ref=native.trace_ref,
            provenance_refs=native.provenance_refs,
            source_version_refs=native.source_version_refs,
            invalidation_refs=(),
            error_class="PROVIDER_RESULT_SCHEMA_INVALID",
            error_detail="RF-DETR predictions require class, confidence and observed geometry",
            actual_provider_response=native.actual_provider_response,
        )
    predictions = _sequence_at(payload, native.workflow_output_mapping.get("detections", ""))
    text_items = _sequence_at(payload, native.workflow_output_mapping.get("ocr", ""))
    detections = _detection_candidates(native, predictions, frame_ref=frame_ref, roi_ref=roi_ref)
    ocr_evidence = _ocr_candidates(native, text_items, frame_ref=frame_ref, roi_ref=roi_ref)
    provenance = _tuple_unique(
        (*native.provenance_refs, native.provider_ref, native.workflow_ref, *native.model_refs, native.trace_ref)
    )
    envelope = None
    if ocr_evidence:
        envelope = OCRStructuredEvidenceEnvelopeV1(
            request_id=native.request_id,
            evidence_envelope_id=f"ocr-envelope:{native.result_id}",
            source_refs=_tuple_unique((native.request_id, native.provider_ref, native.workflow_ref, frame_ref, roi_ref)),
            engine_refs=_tuple_unique((native.provider_ref, *native.model_refs)),
            raw_evidence=tuple(asdict(item) for item in ocr_evidence),
            layout_candidates=(),
            reading_order_candidates=(),
            region_attribution_candidates=(),
            enhancement_candidates=(),
            correction_candidates=(),
            crossmodal_consistency_candidates=(),
            ambiguity_flags=(),
            conflict_flags=(),
            provenance_refs=provenance,
            trace_ref=f"{native.trace_ref}:ocr-envelope",
            replay_key=f"replay:{native.request_id}",
        )
    return RoboflowNormalizedProviderResultV1(
        result_id=native.result_id,
        accepted=True,
        provider_ref=native.provider_ref,
        workflow_ref=native.workflow_ref,
        model_refs=native.model_refs,
        frame_ref=frame_ref,
        roi_ref=roi_ref,
        detection_evidence=detections,
        ocr_evidence=ocr_evidence,
        ocr_envelope=envelope,
        trace_ref=native.trace_ref,
        provenance_refs=provenance,
        source_version_refs=native.source_version_refs,
        invalidation_refs=(),
        actual_provider_response=native.actual_provider_response,
    )


def build_roboflow_observation_gateway_handoff_candidate_v1(
    normalized: RoboflowNormalizedProviderResultV1,
) -> ObservationGatewayEvidenceHandoffCandidateV1 | None:
    """Build the existing candidate-only Gateway handoff from normalized evidence.

    This is a translation seam only.  It never admits evidence, writes Field or
    Current World, or exports the provider-native payload.  An accepted empty
    result has no Evidence refs and therefore produces no handoff candidate.
    """

    if not normalized.accepted:
        return None
    evidence_refs = tuple(
        item.evidence_id
        for item in (*normalized.detection_evidence, *normalized.ocr_evidence)
        if str(item.evidence_id).strip()
    )
    if not evidence_refs:
        return None
    handoff_trace = f"{normalized.trace_ref}:observation-gateway-handoff"
    return ObservationGatewayEvidenceHandoffCandidateV1(
        handoff_id=f"gateway-handoff:roboflow:{normalized.result_id}",
        ingress_type="VISION",
        evidence_refs=evidence_refs,
        provider_ref=normalized.provider_ref,
        source_frame_ref=normalized.frame_ref,
        raw_output_refs=(normalized.result_id,),
        trace_ref=handoff_trace,
        provenance_refs=tuple(
            dict.fromkeys((*normalized.provenance_refs, normalized.workflow_ref, handoff_trace))
        ),
        candidate_only=True,
        gateway_admission=False,
        semantic_authority=False,
    )


__all__ = [
    "build_roboflow_observation_gateway_handoff_candidate_v1",
    "translate_roboflow_result_to_luna_evidence_v1",
]
