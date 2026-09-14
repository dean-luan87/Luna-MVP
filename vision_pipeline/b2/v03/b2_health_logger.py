# vision_pipeline/b2/v03/b2_health_logger.py

from dataclasses import dataclass, asdict
from typing import Dict, Any, List
import json


@dataclass
class B2HealthEvent:
    ts: float
    decision: str              # INTERRUPT / CONDITION_CHANGE / NOTICE
                               # - INTERRUPT: 需要立即改变行为（NEED_STOP / NEED_DETOUR）
                               # - CONDITION_CHANGE: 需要调整行为（NEED_SLOW_DOWN / PATH_UNCERTAIN）
                               # - NOTICE: 不影响行为（NO_OP / SILENT，不写入 timeline）
    impact: str = None         # 真实语义（可选）：NEED_STOP / NEED_DETOUR / PATH_UNCERTAIN / NEED_SLOW_DOWN / NO_OP
    scores: Dict[str, float] = None  # factor scores
    reasons: Dict[str, str] = None   # factor reasons
    confidence: float = 0.0
    main_factor: str = None    # main factor name
    # v0.4.2: Gate 信息（可追溯）
    gate_mode: str = None          # "ACTIVE" | "READ_ONLY" | "SUSPENDED"
    gate_blocked_by: str = None   # 如果被 Gate 阻断，记录原因


class B2HealthLogger:
    """
    B2 v0.3 运行态健康日志记录器
    - 只记录有决策输出的情况（NONE 不记录）
    - 用于未来 Debug / 回放 / 人工对齐
    """
    
    def __init__(self, enable: bool = True):
        self.enable = enable
        self.events: List[B2HealthEvent] = []

    def log(self, event: B2HealthEvent):
        """记录一个健康事件"""
        if not self.enable:
            return
        self.events.append(event)

    def dump(self, path: str):
        """将事件列表 dump 为 JSON 文件"""
        if not self.enable:
            return
        
        # 转换为字典列表
        events_dict = [asdict(e) for e in self.events]
        
        with open(path, "w", encoding="utf-8") as f:
            json.dump(
                events_dict,
                f,
                indent=2,
                ensure_ascii=False
            )
        
        print(f"[B2-Health] 已保存 {len(self.events)} 条事件到 {path}")

    def clear(self):
        """清空事件列表"""
        self.events.clear()

