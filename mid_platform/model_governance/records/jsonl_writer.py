# -*- coding: utf-8 -*-
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Protocol


class _RecordProto(Protocol):
    def to_dict(self) -> Dict[str, Any]:
        ...


def append_jsonl(base_dir: Path, filename: str, record: _RecordProto) -> Path:
    """将一条记录追加写入 JSONL 文件。"""
    base_dir.mkdir(parents=True, exist_ok=True)
    path = base_dir / filename
    line = json.dumps(record.to_dict(), ensure_ascii=False) + "\n"
    path.open("a", encoding="utf-8").write(line)
    return path
