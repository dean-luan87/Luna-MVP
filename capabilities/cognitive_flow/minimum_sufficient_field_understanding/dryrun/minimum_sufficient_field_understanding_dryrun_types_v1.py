"""Fixture-only types for Minimum Sufficient Field Understanding Controlled DryRun v1."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Tuple


MINIMUM_SUFFICIENT_FIELD_UNDERSTANDING_DRYRUN_SCHEMA_VERSION_V1 = (
    "luna.minimum_sufficient_field_understanding.controlled_dryrun.v1"
)


@dataclass(frozen=True)
class MinimumSufficientFieldUnderstandingDryRunCaseV1:
    """A fixed declaration fixture; it contains no real environment data or inference."""

    case_id: str
    title: str
    request: Mapping[str, object]
    expected_identity_status: str
    required_guard_ids: Tuple[str, ...]
