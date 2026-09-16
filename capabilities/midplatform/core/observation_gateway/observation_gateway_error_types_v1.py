from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

ERROR_NAMESPACE = "OBSERVATION_GATEWAY"
OBSERVATION_GATEWAY_ERROR_CODES = (
    "INVALID_INPUT_SHAPE",
    "INVALID_INGRESS",
    "UNSUPPORTED_INGRESS_TYPE",
    "MISSING_PROVIDER_REF",
    "INVALID_EVIDENCE_MAPPING",
    "MISSING_PROVENANCE",
    "CONTRACT_MISMATCH",
    "VERSION_MISMATCH",
    "DUPLICATE_INGRESS",
    "DUPLICATE_EVIDENCE",
    "DUPLICATE_OBSERVATION",
    "DUPLICATE_CORRECTION",
    "DUPLICATE_REFRESH",
    "REVOCATION_REPLAY",
    "EXPIRATION_REPLAY",
    "SUPERSESSION_REPLAY",
    "INVALID_ADMISSION_TRANSITION",
    "INVALID_CORRECTION_LINEAGE",
    "INVALID_ROUTING_TARGET",
)


@dataclass(frozen=True)
class ObservationGatewayErrorV1:
    code: str
    stage_id: str
    message: str
    fatal: bool = False
    related_refs: Tuple[str, ...] = ()
    trace_ref: str = ""
    provenance_refs: Tuple[str, ...] = ()
    namespace: str = ERROR_NAMESPACE


def make_error(
    code: str,
    stage_id: str,
    message: str,
    fatal: bool = False,
    related_refs: Tuple[str, ...] = (),
    trace_ref: str = "",
) -> ObservationGatewayErrorV1:
    return ObservationGatewayErrorV1(
        code=code,
        stage_id=stage_id,
        message=message,
        fatal=fatal,
        related_refs=related_refs,
        trace_ref=trace_ref,
        provenance_refs=tuple(f"prov:{ref}" for ref in related_refs),
    )
