# vision_pipeline/b2/v03/world.py

from typing import Dict
from .types import WorldChange, WorldChangeLevel
from .factors import FactorEvidence, FactorType


class WorldChangeAggregator:
    """
    多因子 → 世界变化等级 的聚合判断器
    
    ⚠️ v0.4 重构说明：
    - ENV 因子不再直接升级为 WORLD 等级（违反 DTL 设计）
    - ENV 信息只进入 factors/reasons，不进入 level
    - 所有 decision 必须基于"是否影响 C 的行为"
    """

    def aggregate(self, factors: Dict[FactorType, FactorEvidence]) -> WorldChange:
        """
        B2 v0.4+
        只负责因子聚合，不再产出 WORLD 级别语义
        """
        if not factors:
            return WorldChange(
                level=WorldChangeLevel.NONE,
                confidence=1.0,
                factors={}
            )

        score_event = factors[FactorType.EVENT].score if FactorType.EVENT in factors else 0.0
        score_path = factors[FactorType.PATH].score if FactorType.PATH in factors else 0.0
        score_local = max(score_event, score_path)

        reasons = {
            k.value: v.reason
            for k, v in factors.items()
        }

        # --- 突发事件 ---
        if score_event >= 0.6:
            return WorldChange(
                level=WorldChangeLevel.EVENT,
                confidence=min(score_event, 1.0),
                factors=reasons,
                interrupt=True
            )

        # --- 局部变化（路况 / 人群等） ---
        if score_path >= 0.6:
            return WorldChange(
                level=WorldChangeLevel.LOCAL,
                confidence=min(score_path, 1.0),
                factors=reasons,
                interrupt=False
            )

        # --- 默认：无变化 ---
        return WorldChange(
            level=WorldChangeLevel.NONE,
            confidence=0.0,
            factors=reasons,
            interrupt=False
        )

