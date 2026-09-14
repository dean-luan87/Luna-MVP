from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

ERROR_NAMESPACE = "A_ROUTE_ORCHESTRATION"


@dataclass(frozen=True)
class ARouteOrchestrationErrorV1:
    code: str
    stage_id: str
    message: str
    fatal: bool
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
) -> ARouteOrchestrationErrorV1:
    return ARouteOrchestrationErrorV1(
        code=code,
        stage_id=stage_id,
        message=message,
        fatal=fatal,
        related_refs=related_refs,
        trace_ref=trace_ref,
        provenance_refs=tuple(f"prov:{ref}" for ref in related_refs),
    )
