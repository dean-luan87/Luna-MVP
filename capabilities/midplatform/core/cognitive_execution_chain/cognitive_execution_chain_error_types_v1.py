from __future__ import annotations

from dataclasses import dataclass

ERROR_NAMESPACE = "cognitive_execution_chain.controlled_integration.v1"


@dataclass(frozen=True)
class CognitiveExecutionChainErrorV1:
    code: str
    message: str
    category: str
    recoverable: bool
    namespace: str = ERROR_NAMESPACE


def make_error(
    code: str, message: str, category: str, recoverable: bool
) -> CognitiveExecutionChainErrorV1:
    return CognitiveExecutionChainErrorV1(
        code=code,
        message=message,
        category=category,
        recoverable=recoverable,
    )
