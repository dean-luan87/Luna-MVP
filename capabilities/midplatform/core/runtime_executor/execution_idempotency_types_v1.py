"""Idempotency registry and state types."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional


@dataclass(frozen=True)
class IdempotencyRecordV1:
    idempotency_key: str
    scope_key: str
    execution_id: str
    status: str
    result_ref: str | None


class IdempotencyRegistryV1:
    def __init__(self) -> None:
        self._records: Dict[str, IdempotencyRecordV1] = {}

    def get(self, key: str) -> Optional[IdempotencyRecordV1]:
        return self._records.get(key)

    def put(self, record: IdempotencyRecordV1) -> None:
        self._records[record.idempotency_key] = record

    def size(self) -> int:
        return len(self._records)
