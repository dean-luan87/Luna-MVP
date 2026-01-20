# vision_pipeline/b2/v03/b2_runtime_trace.py
"""
B2 Runtime Trace v0.4
可审计的认知运行记录系统

目标：用"人能理解的时间 + 语言"，完整复盘 B 在某一段时间内的思考过程
"""

from __future__ import annotations
import json
import os
from typing import Dict, Any, Optional, TextIO
from dataclasses import dataclass, field
from enum import Enum


class BRuntimeMode(str, Enum):
    """B 运行模式"""
    ACTIVE = "ACTIVE"           # 正常工作
    READ_ONLY = "READ_ONLY"     # 只读模式（不输出决策）
    GATED = "GATED"             # 被门控（不运行）


@dataclass
class B2RuntimeTrace:
    """
    B2 Runtime Trace v0.4 完整结构
    一行 JSON = B 在这一刻的全部思考过程
    """
    
    # 一、时间与帧的统一
    time: Dict[str, Any]
    
    # 二、B 是否"开始工作"的显式标记
    b_runtime_state: Dict[str, Any]
    
    # 三、触发起点
    trigger: Dict[str, Any]
    
    # 四、计算过程透明化
    perception: Dict[str, Any]
    rule_evaluation: list
    
    # 五、计算结果
    impact_evaluation: Dict[str, Any]
    
    # 六、人类可读转译
    human_interpretation: Dict[str, Any]
    
    # 七、B → C 的通信内容
    to_c_message: Dict[str, Any]
    
    # 八、输出与记录情况
    writeback: Dict[str, Any]
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "time": self.time,
            "b_runtime_state": self.b_runtime_state,
            "trigger": self.trigger,
            "perception": self.perception,
            "rule_evaluation": self.rule_evaluation,
            "impact_evaluation": self.impact_evaluation,
            "human_interpretation": self.human_interpretation,
            "to_c_message": self.to_c_message,
            "writeback": self.writeback,
        }
    
    def to_json(self) -> str:
        """转换为 JSON 字符串"""
        return json.dumps(self.to_dict(), ensure_ascii=False)


class B2RuntimeTraceWriter:
    """
    B2 Runtime Trace 写入器
    负责将 trace 写入 JSONL 文件
    """
    
    def __init__(
        self,
        trace_file: Optional[str] = None,
        enable: bool = True,
        fps: float = 30.0
    ):
        """
        :param trace_file: trace 文件路径（如果为 None，使用默认路径）
        :param enable: 是否启用 trace 记录
        :param fps: 视频帧率（用于计算 frame_id）
        """
        self.enable = enable
        self.fps = fps
        self._fp: Optional[TextIO] = None
        self._trace_count = 0
        
        if enable:
            if trace_file is None:
                # 默认路径：traces/b2_runtime_trace_v04.jsonl
                trace_dir = "traces"
                os.makedirs(trace_dir, exist_ok=True)
                trace_file = os.path.join(trace_dir, "b2_runtime_trace_v04.jsonl")
            
            self.trace_file = trace_file
            self._fp = open(trace_file, "a", encoding="utf-8")
    
    def write(self, trace: B2RuntimeTrace):
        """写入一条 trace"""
        if not self.enable or not self._fp:
            return
        
        line = trace.to_json()
        self._fp.write(line + "\n")
        self._fp.flush()
        self._trace_count += 1
    
    def close(self):
        """关闭文件"""
        if self._fp:
            self._fp.close()
            self._fp = None
    
    def __del__(self):
        """析构时关闭文件"""
        self.close()
