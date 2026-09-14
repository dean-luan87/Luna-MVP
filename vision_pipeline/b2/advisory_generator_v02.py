"""
Advisory Generator v0.2 - 只做"建议分级"

职责：
- 将 FutureWorld 转为 Advisory
- 不下指令，只给建议
"""

import time
from typing import Optional
from .b2_types_v02 import B2Advisory, FutureWorld

# B2 Advisory TTL（秒）
B2_ADVISORY_TTL_SEC = 10.0


class B2AdvisoryGenerator:
    """
    B2 建议生成器 v0.2
    
    核心职责：
    - 将未来世界投影结果转为 Advisory
    - 不下指令，只给建议
    """
    
    def __init__(self, prewarn_th: float = 0.7):
        """
        初始化建议生成器
        
        Args:
            prewarn_th: PREWARN 阈值
        """
        self.prewarn_th = prewarn_th
    
    def generate(
        self,
        future_world: FutureWorld,
        trigger_reason: str = "TTL_EXPIRE",
    ) -> B2Advisory:
        """
        生成建议
        
        A5.1: B2 → C 的唯一接口：B2Advisory
        
        B2 v0.2: 基于未来预演结果生成建议
        
        Args:
            future_world: 未来世界投影结果
            trigger_reason: 触发原因
        
        Returns:
            B2Advisory: B2 建议
        """
        # 如果没有潜在冲突，生成 DEESCALATE
        if not future_world.impacts:
            return B2Advisory(
                advisory_type="DEESCALATE",
                horizon_sec=future_world.horizon_sec,
                confidence=0.7,
                trigger_reason=trigger_reason,
                impacts=[],
                suggestion={
                    "risk_weight": 0.7,
                    "speech_cooldown_factor": 1.5,
                    "recommended_calm": True,
                },
                meta={
                    "ttl_sec": B2_ADVISORY_TTL_SEC,
                    "timestamp": time.time(),
                }
            )
        
        # 有潜在冲突：根据 TTC 和分数决定建议类型
        min_ttc = min(x.ttc for x in future_world.impacts)
        max_score = max(x.score for x in future_world.impacts)
        
        # PREWARN（提前预警）：如果 TTC <= 5.0 秒
        PREWARN_TTC_SEC = 5.0
        if min_ttc <= PREWARN_TTC_SEC:
            return B2Advisory(
                advisory_type="PREWARN",
                horizon_sec=future_world.horizon_sec,
                confidence=max_score,
                trigger_reason=trigger_reason,
                impacts=future_world.impacts,
                suggestion={
                    "risk_weight": 1.3,
                    "speech_cooldown_factor": 0.8,
                    "attention_raise": True,
                    "earliest_impact_time": min_ttc,
                },
                meta={
                    "ttl_sec": B2_ADVISORY_TTL_SEC,
                    "timestamp": time.time(),
                    "max_score": max_score,
                    "min_ttc": min_ttc,
                }
            )
        
        # WORLD_NOTE（世界变化，不一定影响任务）：TTC >= 5.0 秒
        return B2Advisory(
            advisory_type="WORLD_NOTE",
            horizon_sec=future_world.horizon_sec,
            confidence=max_score * 0.5,  # 降低风险等级
            trigger_reason=trigger_reason,
            impacts=future_world.impacts,
            suggestion={
                "risk_weight": 0.9,
                "speech_cooldown_factor": 1.0,
            },
            meta={
                "ttl_sec": B2_ADVISORY_TTL_SEC,
                "timestamp": time.time(),
                "max_score": max_score,
                "min_ttc": min_ttc,
            }
        )

