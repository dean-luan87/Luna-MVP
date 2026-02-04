# vision_pipeline/b2/v03/timeline_writer.py
from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any, Dict, TextIO


@dataclass
class TimelineWriter:
    """
    B2 v0.4+ 时间轴事件写入器
    
    NOTE:
    - timeline = 行为影响时间轴，只记录"有行为意义"的输出
    - NOTICE == NO_OP == SILENT（不进入 timeline）
    - 只记录：NEED_STOP / NEED_DETOUR / PATH_UNCERTAIN / NEED_SLOW_DOWN
    """
    fp: TextIO
    enabled: bool = True

    def write(self, record: Dict[str, Any]) -> None:
        """
        record 必须是「结构化事实」，不是日志文本
        
        注意：
        - 只写入有行为影响的 decision（impact != NO_OP）
        - NOTICE / NO_OP 不应调用此方法

        推荐字段（v0.4+）：
        {
            "t_video": 195.12,
            "t_str": "03:15.12",
            "frame_idx": 5850,

            "window": {"start": 196.1, "end": 203.1},

            "event_type": "DECISION",
            "decision": "INTERRUPT",  # 或 "CONDITION_CHANGE"
            "impact": "NEED_STOP",    # 真实语义：NEED_STOP / NEED_DETOUR / PATH_UNCERTAIN / NEED_SLOW_DOWN
            "main_factor": "event",
            "confidence": 0.72,

            "scores": {...},
            "reasons": {...},

            "evidence_ref": "b2_v03_records/evidence_03_15.json"
        }
        """
        if not self.enabled:
            return

        line = json.dumps(record, ensure_ascii=False)
        self.fp.write(line + "\n")
        self.fp.flush()

