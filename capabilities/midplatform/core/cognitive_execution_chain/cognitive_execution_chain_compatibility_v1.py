from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

from capabilities.midplatform.core.cognitive_execution_chain.cognitive_execution_chain_types_v1 import (
    CompatibilityDecisionV1,
)


@dataclass(frozen=True)
class HopVersionV1:
    schema_version: str
    contract_version: str


_DEFAULT_HOP_VERSIONS: Dict[str, HopVersionV1] = {
    "H1": HopVersionV1(schema_version="1.0.0", contract_version="1.0.0"),
    "H2": HopVersionV1(schema_version="1.0.0", contract_version="1.0.0"),
    "H3": HopVersionV1(schema_version="1.0.0", contract_version="1.0.0"),
    "H4": HopVersionV1(schema_version="1.0.0", contract_version="1.0.0"),
}


def get_default_hop_version(hop_id: str) -> HopVersionV1:
    return _DEFAULT_HOP_VERSIONS[hop_id]


def decide_compatibility(
    hop_id: str,
    directive_force_incompatible_hop: str,
    directive_force_migration_required_hop: str,
) -> CompatibilityDecisionV1:
    if hop_id == directive_force_incompatible_hop:
        return CompatibilityDecisionV1(
            hop_id=hop_id,
            compatibility_status="incompatible",
            allow_handoff=False,
            hard_block=True,
            reason="forced_incompatible_by_scenario",
        )

    if hop_id == directive_force_migration_required_hop:
        return CompatibilityDecisionV1(
            hop_id=hop_id,
            compatibility_status="migration_required",
            allow_handoff=False,
            hard_block=False,
            reason="migration_required_blocked_in_controlled_integration",
        )

    return CompatibilityDecisionV1(
        hop_id=hop_id,
        compatibility_status="compatible",
        allow_handoff=True,
        hard_block=False,
        reason="compatible",
    )
