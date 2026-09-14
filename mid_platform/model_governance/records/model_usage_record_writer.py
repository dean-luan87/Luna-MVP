# -*- coding: utf-8 -*-
from __future__ import annotations

from pathlib import Path

from mid_platform.model_governance.records.jsonl_writer import append_jsonl
from mid_platform.model_governance.schemas.model_usage_record import ModelUsageRecord


class ModelUsageRecordWriter:
    """使用记录 JSONL 落盘。"""

    def __init__(self, base_dir: Path) -> None:
        self._base = base_dir

    def write(self, record: ModelUsageRecord) -> Path:
        return append_jsonl(self._base, "usage_records.jsonl", record)
