from __future__ import annotations

from .a_route_orchestration_core_types_v1 import ARouteNegativeGuardsV1

CANONICAL_OWNER = "A Route Orchestration Governance"
FORBIDDEN_SEMANTIC_OWNERS = (
    "Context Orchestrator",
    "Intent Orchestrator",
    "Cognitive Orchestrator",
    "Runtime Orchestrator",
)


def build_negative_guards(
    *, execution_mode: str = "SYNTHETIC_CONTROLLED", synthetic_only: bool = True
) -> ARouteNegativeGuardsV1:
    return ARouteNegativeGuardsV1(
        execution_mode=execution_mode,
        synthetic_only=synthetic_only,
    )


def validate_owner_boundary(owner: str) -> bool:
    return owner == CANONICAL_OWNER and owner not in FORBIDDEN_SEMANTIC_OWNERS


def orchestration_has_no_semantic_authority() -> bool:
    return True
