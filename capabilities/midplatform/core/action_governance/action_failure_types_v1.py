"""Failure result reference types for Action Governance controlled implementation v1."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class FailureResultReferenceV1:
    failure_class: Optional[str]
    execution_result_reference: Optional[str]
    failure_trace_reference: Optional[str]
    retry_authority_granted: bool = False
