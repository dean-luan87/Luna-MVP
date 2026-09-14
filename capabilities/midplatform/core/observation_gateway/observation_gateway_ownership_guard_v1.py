from __future__ import annotations

from .observation_gateway_core_types_v1 import ObservationGatewayNegativeGuardsV1

CANONICAL_OWNER = "Observation Gateway Governance"
PARALLEL_OWNERS = (
    "Perception Governance",
    "Observation Governance",
    "Vision Governance",
    "OCR Governance",
    "SLAM Governance",
)


def build_negative_guards(
    *, execution_mode: str = "SYNTHETIC_CONTROLLED", synthetic_only: bool = True
) -> ObservationGatewayNegativeGuardsV1:
    return ObservationGatewayNegativeGuardsV1(
        execution_mode=execution_mode,
        synthetic_only=synthetic_only,
    )


def validate_owner(owner: str) -> bool:
    return owner == CANONICAL_OWNER and owner not in PARALLEL_OWNERS
