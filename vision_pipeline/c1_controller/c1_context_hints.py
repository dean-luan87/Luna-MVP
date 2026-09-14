"""
C1 Context Hints - C 内部态（用于理解 B2，不是执行）

A5.3: C 如何"理解"B2（不是执行）

这是一个极其克制的中间层，用于：
- 让 C"看见"B2
- 但不被 B2 控制
- C 仍然是当下视角的唯一执行者
- B2 只是一个有价值的"未来情报源"
"""

from typing import List, Optional
from vision_pipeline.b2.b2_types_v02 import B2Advisory


class CContextHints:
    """
    C 上下文提示（用于理解 B2）
    
    核心职责：
    - 存储 B2 提供的未来情报
    - 不直接控制 C 的行为
    - 只影响 C 的内部参数和阈值
    """
    
    def __init__(self):
        """初始化 C 上下文提示"""
        # 未来风险等级（0~1）
        self.future_risk_level: float = 0.0
        
        # 是否建议降级警惕
        self.recommended_calm: bool = False
        
        # 世界变化记录
        self.world_notes: List[B2Advisory] = []
        
        # 最后更新的时间戳
        self.last_update_ts: Optional[float] = None
    
    def ingest_b2_advisory(self, advisory: B2Advisory, current_ts: float):
        """
        B2 → C 的映射逻辑（示例）
        
        A5.3: C 如何"理解"B2（不是执行）
        
        ⚠️ 关键点：
        - C 只是"记住"
        - 不立刻反应
        - 不打断当前状态
        
        Args:
            advisory: B2 建议
            current_ts: 当前时间戳
        """
        self.last_update_ts = current_ts
        
        if advisory.advisory_type == "PREWARN":
            # 未来可能有风险：提高风险等级
            self.future_risk_level = max(
                self.future_risk_level,
                advisory.confidence
            )
        
        elif advisory.advisory_type == "DEESCALATE":
            # 明显安全：如果置信度高，建议降级警惕
            if advisory.confidence > 0.7:
                self.recommended_calm = True
        
        elif advisory.advisory_type == "WORLD_NOTE":
            # 世界变化（不一定影响任务）：记录
            self.world_notes.append(advisory)
            # 只保留最近的 5 条
            if len(self.world_notes) > 5:
                self.world_notes = self.world_notes[-5:]
    
    def decay(self, current_ts: float, decay_rate: float = 0.1):
        """
        衰减（随时间降低影响）
        
        Args:
            current_ts: 当前时间戳
            decay_rate: 衰减率（每秒）
        """
        if self.last_update_ts is None:
            return
        
        elapsed = current_ts - self.last_update_ts
        if elapsed > 0:
            # 风险等级衰减
            self.future_risk_level *= (1.0 - decay_rate * elapsed)
            if self.future_risk_level < 0.0:
                self.future_risk_level = 0.0
            
            # 如果超过 10 秒没有更新，重置 recommended_calm
            if elapsed > 10.0:
                self.recommended_calm = False

