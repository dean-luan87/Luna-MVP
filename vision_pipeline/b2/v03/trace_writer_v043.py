"""
B2 Runtime Trace Writer v0.4.3

统一 Trace Schema，每帧一条 JSONL
"""

from __future__ import annotations
import json
import os
from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class TraceWriterV043:
    """B2 Trace Writer v0.4.3（统一 Schema）"""
    
    out_path: str
    enabled: bool = True

    def __post_init__(self) -> None:
        """初始化：确保输出目录存在"""
        if not self.enabled:
            return
        out_dir = os.path.dirname(self.out_path)
        if out_dir:
            os.makedirs(out_dir, exist_ok=True)

    def write(self, rec: Dict[str, Any]) -> None:
        """
        写入一条 trace 记录
        
        :param rec: trace 字典（会自动添加 schema_version）
        """
        if not self.enabled:
            return
        
        # 自动添加 schema_version
        rec.setdefault("schema_version", "b2.trace.v0.4.3")
        
        # 写入 JSONL
        with open(self.out_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
            f.flush()
