from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict


@dataclass(frozen=True)
class ContextPcnIntentIntegrationErrorV1:
    code: str
    stage: str
    message: str
    hard_block: bool
    details: Dict[str, str] = field(default_factory=dict)


def make_error(
    code: str,
    stage: str,
    message: str,
    hard_block: bool,
    **details: str,
) -> ContextPcnIntentIntegrationErrorV1:
    return ContextPcnIntentIntegrationErrorV1(
        code=code,
        stage=stage,
        message=message,
        hard_block=hard_block,
        details=details,
    )
