# vision_pipeline/b2/v03/b2_audit/context.py
"""
Audit Context（只读数据）
"""

import json
from pathlib import Path
from typing import List, Dict, Any, Optional


class AuditContext:
    """验收上下文（只读数据）"""
    
    def __init__(self, trace_path: str, timeline_path: Optional[str] = None):
        """
        初始化验收上下文
        
        :param trace_path: Trace 文件路径（jsonl）
        :param timeline_path: Timeline 文件路径（可选）
        """
        self.traces: List[Dict[str, Any]] = self._load_jsonl(trace_path)
        self.timeline: List[Dict[str, Any]] = self._load_jsonl(timeline_path) if timeline_path else []
        self.trace_path = trace_path
        self.timeline_path = timeline_path
    
    def _load_jsonl(self, path: Optional[str]) -> List[Dict[str, Any]]:
        """加载 JSONL 文件"""
        if not path:
            return []
        
        path_obj = Path(path)
        if not path_obj.exists():
            return []
        
        try:
            with open(path, "r", encoding="utf-8") as f:
                return [json.loads(line) for line in f if line.strip()]
        except Exception as e:
            print(f"⚠️  加载文件失败 {path}: {e}")
            return []
    
    def get_trace_count(self) -> int:
        """获取 trace 数量"""
        return len(self.traces)
    
    def get_timeline_count(self) -> int:
        """获取 timeline 数量"""
        return len(self.timeline)
