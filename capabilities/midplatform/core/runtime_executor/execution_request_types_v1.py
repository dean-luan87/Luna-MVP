"""Execution request candidate types."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from capabilities.midplatform.core.runtime_executor.runtime_executor_core_types_v1 import (
    SourceRefV1,
)


@dataclass(frozen=True)
class ExecutionRequestCandidateV1:
    execution_request_id: str
    action_candidate_ref: SourceRefV1
    execution_readiness_ref: SourceRefV1
    permission_recheck_ref: SourceRefV1
    safety_recheck_ref: SourceRefV1
    confirmation_ref: SourceRefV1
    resource_constraint_ref: SourceRefV1
    reversibility: str
    request_time: str
    idempotency_key: str
    scope_key: str
    provenance_ref: SourceRefV1
    scheduler_refs: Tuple[SourceRefV1, ...]
    task_refs: Tuple[SourceRefV1, ...]
    adapter_refs: Tuple[SourceRefV1, ...]
    candidate_only: bool = True
    planning_only: bool = True
