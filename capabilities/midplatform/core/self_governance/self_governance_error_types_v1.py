"""Errors for deterministic candidate validation."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class SelfGovernanceIssueV1:
    code: str
    message: str
    blocker: bool = True


class SelfGovernanceErrorV1(Exception):
    """Base error; no error path performs a side effect."""


class DuplicateCandidateErrorV1(SelfGovernanceErrorV1):
    pass


class OwnershipBoundaryErrorV1(SelfGovernanceErrorV1):
    pass


@dataclass(frozen=True)
class SelfGovernanceValidationResultV1:
    valid: bool
    issues: Tuple[SelfGovernanceIssueV1, ...] = ()
