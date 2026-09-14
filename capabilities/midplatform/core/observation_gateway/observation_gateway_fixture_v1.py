from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Tuple

from .observation_gateway_core_types_v1 import ObservationGatewayResultV1, ObservationIngressRequestV1


@dataclass(frozen=True)
class ObservationGatewayFixtureCaseV1:
    case_id: str
    title: str
    request: ObservationIngressRequestV1
    expected_admission_state: str
    expected_route_status: str
    expected_error_code: str = ""
    expected_route_ready: bool = False
    expected_evidence_count: int = 1
    expected_correction_lineage: bool = False
    expected_contradiction_lineage: bool = False
    expected_deferred_ref: str = ""


def _request(case_id: str, **overrides: object) -> ObservationIngressRequestV1:
    values: Dict[str, object] = {"scenario_id": case_id}
    values.update(overrides)
    return ObservationIngressRequestV1(**values)


def get_observation_gateway_fixtures_v1() -> Tuple[ObservationGatewayFixtureCaseV1, ...]:
    definitions = (
        ("O01", "user command ingress", {"ingress_type": "USER_INPUT"}, "ADMITTED_OBSERVATION", "INGRESS_READY", "", True, 1, False, False, ""),
        ("O02", "user statement ingress", {"ingress_type": "USER_INPUT"}, "ADMITTED_OBSERVATION", "INGRESS_READY", "", True, 1, False, False, ""),
        ("O03", "user correction ingress", {"ingress_type": "USER_INPUT", "user_correction": True, "correction_ref": "correction:O03", "corrected_evidence_ref": "evidence:O03:prior", "corrected_observation_ref": "observation:O03:prior"}, "ADMITTED_OBSERVATION", "INGRESS_READY", "", True, 1, True, False, ""),
        ("O04", "user confirmation ingress", {"ingress_type": "USER_INPUT", "needs_confirmation": False}, "ADMITTED_OBSERVATION", "INGRESS_READY", "", True, 1, False, False, ""),
        ("O05", "vision evidence", {"ingress_type": "VISION", "source_model_ref": "model:vision", "source_region_ref": "region:1"}, "ADMITTED_OBSERVATION", "INGRESS_READY", "", True, 1, False, False, ""),
        ("O06", "OCR evidence", {"ingress_type": "OCR", "source_model_ref": "model:ocr"}, "ADMITTED_OBSERVATION", "INGRESS_READY", "", True, 1, False, False, ""),
        ("O07", "audio evidence", {"ingress_type": "AUDIO", "source_model_ref": "model:audio"}, "ADMITTED_OBSERVATION", "INGRESS_READY", "", True, 1, False, False, ""),
        ("O08", "SLAM spatial evidence", {"ingress_type": "SLAM_SPATIAL", "spatial_refs": ("geometry:O08",)}, "ADMITTED_OBSERVATION", "INGRESS_READY", "", True, 1, False, False, ""),
        ("O09", "Field reference", {"ingress_type": "FIELD_REFERENCE", "route_to_field": True}, "ADMITTED_OBSERVATION", "INGRESS_READY", "", True, 1, False, False, ""),
        ("O10", "system event", {"ingress_type": "SYSTEM_EVENT"}, "ADMITTED_OBSERVATION", "INGRESS_READY", "", True, 1, False, False, ""),
        ("O11", "external provider", {"ingress_type": "EXTERNAL_PROVIDER"}, "ADMITTED_OBSERVATION", "INGRESS_READY", "", True, 1, False, False, ""),
        ("O12", "Vision plus OCR observation", {"ingress_type": "VISION", "multi_evidence_agreement": True, "evidence_refs": ("evidence:vision", "evidence:ocr")}, "ADMITTED_OBSERVATION", "INGRESS_READY", "", True, 2, False, False, ""),
        ("O13", "Vision plus SLAM observation", {"ingress_type": "VISION", "multi_evidence_agreement": True, "spatial_refs": ("geometry:O13",)}, "ADMITTED_OBSERVATION", "INGRESS_READY", "", True, 2, False, False, ""),
        ("O14", "multi-evidence agreement", {"ingress_type": "EXTERNAL_PROVIDER", "multi_evidence_agreement": True}, "ADMITTED_OBSERVATION", "INGRESS_READY", "", True, 2, False, False, ""),
        ("O15", "multi-evidence contradiction", {"ingress_type": "VISION", "multi_evidence_contradiction": True}, "CONTESTED", "ROUTING_CANDIDATE_READY", "", False, 2, False, True, ""),
        ("O16", "uncertain evidence", {"ingress_type": "VISION", "uncertainty": True}, "NEEDS_CONFIRMATION", "ROUTING_CANDIDATE_READY", "", False, 1, False, False, ""),
        ("O17", "missing provider", {"missing_provider": True}, "REJECTED", "BLOCKED", "MISSING_PROVIDER_REF", False, 0, False, False, ""),
        ("O18", "missing provenance", {"missing_provenance": True}, "REJECTED", "BLOCKED", "MISSING_PROVENANCE", False, 0, False, False, ""),
        ("O19", "observation admitted", {}, "ADMITTED_OBSERVATION", "INGRESS_READY", "", True, 1, False, False, ""),
        ("O20", "observation needs confirmation", {"needs_confirmation": True}, "NEEDS_CONFIRMATION", "ROUTING_CANDIDATE_READY", "", False, 1, False, False, ""),
        ("O21", "observation contested", {"contested": True}, "CONTESTED", "ROUTING_CANDIDATE_READY", "", False, 1, False, False, ""),
        ("O22", "observation rejected", {"rejected": True}, "REJECTED", "BLOCKED", "", False, 1, False, False, ""),
        ("O23", "observation revoked", {"revoked": True}, "REVOKED", "ROUTING_CANDIDATE_READY", "", False, 1, False, False, ""),
        ("O24", "observation expired", {"expired": True}, "EXPIRED", "ROUTING_CANDIDATE_READY", "", False, 1, False, False, ""),
        ("O25", "observation superseded", {"superseded": True}, "SUPERSEDED", "ROUTING_CANDIDATE_READY", "", False, 1, False, False, ""),
        ("O26", "duplicate ingress", {"duplicate_ingress": True}, "REJECTED", "BLOCKED", "DUPLICATE_INGRESS", False, 0, False, False, ""),
        ("O27", "duplicate evidence", {"duplicate_evidence": True}, "REJECTED", "BLOCKED", "DUPLICATE_EVIDENCE", False, 0, False, False, ""),
        ("O28", "duplicate observation", {"duplicate_observation": True}, "REJECTED", "BLOCKED", "DUPLICATE_OBSERVATION", False, 0, False, False, ""),
        ("O29", "duplicate correction", {"duplicate_correction": True}, "REJECTED", "BLOCKED", "DUPLICATE_CORRECTION", False, 0, False, False, ""),
        ("O30", "refresh replay", {"duplicate_refresh": True}, "REJECTED", "BLOCKED", "DUPLICATE_REFRESH", False, 0, False, False, ""),
        ("O31", "user correction precedence", {"user_correction": True, "correction_ref": "correction:O31", "uncertainty": True}, "ADMITTED_OBSERVATION", "INGRESS_READY", "", True, 1, True, False, ""),
        ("O32", "OCR evidence not fact", {"ingress_type": "OCR"}, "ADMITTED_OBSERVATION", "INGRESS_READY", "", True, 1, False, False, ""),
        ("O33", "visual detection not fact", {"ingress_type": "VISION"}, "ADMITTED_OBSERVATION", "INGRESS_READY", "", True, 1, False, False, ""),
        ("O34", "SLAM not semantic truth", {"ingress_type": "SLAM_SPATIAL"}, "ADMITTED_OBSERVATION", "INGRESS_READY", "", True, 1, False, False, ""),
        ("O35", "Field routing without Field mutation", {"route_to_field": True}, "ADMITTED_OBSERVATION", "INGRESS_READY", "", True, 1, False, False, ""),
        ("O36", "Context routing without Context mutation", {"route_to_context": True}, "ADMITTED_OBSERVATION", "INGRESS_READY", "", True, 1, False, False, ""),
        ("O37", "Attention routing without Attention mutation", {"route_to_attention": True}, "ADMITTED_OBSERVATION", "INGRESS_READY", "", True, 1, False, False, ""),
        ("O38", "A Route ingress ready", {}, "ADMITTED_OBSERVATION", "INGRESS_READY", "", True, 1, False, False, ""),
        ("O39", "trace reverse lookup", {}, "ADMITTED_OBSERVATION", "INGRESS_READY", "", True, 1, False, False, ""),
        ("O40", "correction lineage", {"user_correction": True, "correction_ref": "correction:O40"}, "ADMITTED_OBSERVATION", "INGRESS_READY", "", True, 1, True, False, ""),
        ("O41", "contradiction lineage", {"multi_evidence_contradiction": True}, "CONTESTED", "ROUTING_CANDIDATE_READY", "", False, 2, False, True, ""),
        ("O42", "temporal validity", {"valid_until_candidate": "2026-08-13T01:00:00Z", "refresh": True}, "EVIDENCE_READY", "ROUTING_CANDIDATE_READY", "", False, 1, False, False, ""),
        ("O43", "Emotion deferred", {"emotion_deferred": True}, "ADMITTED_OBSERVATION", "INGRESS_READY", "", True, 1, False, False, "emotion_engine"),
        ("O44", "B Route deferred", {"b_route_deferred": True}, "ADMITTED_OBSERVATION", "INGRESS_READY", "", True, 1, False, False, "b_route"),
        ("O45", "semantic compression deferred", {"semantic_compression_deferred": True}, "ADMITTED_OBSERVATION", "INGRESS_READY", "", True, 1, False, False, "semantic_compression"),
        ("O46", "no runtime/model/device side effects", {}, "ADMITTED_OBSERVATION", "INGRESS_READY", "", True, 1, False, False, ""),
    )
    return tuple(
        ObservationGatewayFixtureCaseV1(
            case_id=case_id,
            title=title,
            request=_request(case_id, **overrides),
            expected_admission_state=admission,
            expected_route_status=route_status,
            expected_error_code=error,
            expected_route_ready=route_ready,
            expected_evidence_count=evidence_count,
            expected_correction_lineage=correction,
            expected_contradiction_lineage=contradiction,
            expected_deferred_ref=deferred,
        )
        for case_id, title, overrides, admission, route_status, error, route_ready, evidence_count, correction, contradiction, deferred in definitions
    )
