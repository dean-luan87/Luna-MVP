"""Separated stability/mutability partitions."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from .self_governance_registry_v1 import STABILITY_PARTITIONS


@dataclass(frozen=True)
class SelfStabilityPartitionV1:
    partition: str
    examples: Tuple[str, ...]
    change_mode: str
    deferred: bool = False


STABILITY_MODEL_V1: Tuple[SelfStabilityPartitionV1, ...] = (
    SelfStabilityPartitionV1("STRUCTURAL_SELF", ("agent identity reference", "ownership boundary"), "rare_reviewed_candidate_only"),
    SelfStabilityPartitionV1("SEMI_STABLE_SELF", ("role", "relationship position", "preference", "interaction tendency"), "reviewable_revisionable_candidate_only"),
    SelfStabilityPartitionV1("TRANSIENT_SELF", ("current intent", "resource condition", "uncertainty"), "cycle_scoped_candidate_only"),
    SelfStabilityPartitionV1("FUTURE_PERSONALITY_DERIVED_SELF", ("trait candidate", "trait stability", "trait expression"), "DEFERRED", True),
)


def is_valid_partition(partition: str) -> bool:
    return partition in STABILITY_PARTITIONS
