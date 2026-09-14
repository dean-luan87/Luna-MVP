# -*- coding: utf-8 -*-
from __future__ import annotations

from pathlib import Path

from mid_platform.model_governance.records.jsonl_writer import append_jsonl
from mid_platform.model_governance.schemas.model_governance_record import ModelGovernanceRecord


class ModelGovernanceRecordWriter:
    """治理记录 JSONL 落盘。"""

    def __init__(self, base_dir: Path) -> None:
        self._base = base_dir

    def write(self, record: ModelGovernanceRecord) -> Path:
        return append_jsonl(self._base, "governance_records.jsonl", record)
