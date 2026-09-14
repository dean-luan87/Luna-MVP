# vision_pipeline/b2/v03/trace/trace_writer.py
"""
B2 Runtime Trace Writer v0.4
最小实现：只负责写入 JSONL
"""

import json
import os
from typing import Dict, Any


class TraceWriter:
    """Trace 写入器（最小实现）"""
    
    def __init__(self, path: str):
        """
        :param path: trace 文件路径
        """
        self.path = path
        # 确保目录存在
        os.makedirs(os.path.dirname(path), exist_ok=True)
    
    def write(self, record: Dict[str, Any]):
        """
        写入一条 trace 记录
        :param record: trace 字典
        """
        with open(self.path, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
            f.flush()
