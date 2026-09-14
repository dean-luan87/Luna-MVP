"""Protocol for Runtime Executor controlled engine."""

from __future__ import annotations

from typing import Protocol

from capabilities.midplatform.core.runtime_executor.runtime_executor_io_types_v1 import (
    RuntimeExecutorInputV1,
    RuntimeExecutorOutputV1,
)


class RuntimeExecutorProtocolV1(Protocol):
    def run_case(self, request: RuntimeExecutorInputV1) -> RuntimeExecutorOutputV1: ...
