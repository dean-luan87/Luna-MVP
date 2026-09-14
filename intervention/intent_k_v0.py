# intervention/intent_k_v0.py
# K 层 v0：介入意图抽象层（只读、确定性、可冻结）

from enum import Enum
from typing import Optional


class Intent(Enum):
    NAV_GUIDE = "NAV_GUIDE"          # 导航 / 路线 / 转向 / 避让
    ENV_NOTICE = "ENV_NOTICE"        # 环境变化 / 人群 / 障碍
    TASK_ASSIST = "TASK_ASSIST"      # 当前任务相关协助
    SAFETY_WARN = "SAFETY_WARN"      # 安全警示（必胜）
    STATUS_UPDATE = "STATUS_UPDATE"  # 状态同步（当前阶段/完成情况）
    NONE = "NONE"                    # 明确「不介入」


class IntentK_v0:
    """
    K 层 v0：介入意图抽象层（只读）

    输入：G 层 winner
    输出：单一、确定性的 Intent
    """

    def decide(self, winner: Optional[str]) -> Intent:
        """
        根据 G 层 winner 决定介入意图

        参数：
        - winner: G 层输出的 winner 类型字符串
                  e.g. "NAVIGATION", "ENV_AWARENESS", "TASK_STATE", "SAFETY"

        返回：
        - Intent 枚举
        """
        if winner is None:
            return Intent.NONE

        # SAFETY 必胜，直接映射
        if winner == "SAFETY":
            return Intent.SAFETY_WARN

        # 导航相关
        if winner == "NAVIGATION":
            return Intent.NAV_GUIDE

        # 环境感知
        if winner == "ENV_AWARENESS":
            return Intent.ENV_NOTICE

        # 任务态
        if winner == "TASK_STATE":
            return Intent.TASK_ASSIST

        # 兜底：明确 NONE，而不是隐式丢失
        return Intent.NONE


# 单例，供 main 等调用方统一使用（接入点：G 层 winner 确定后）
_intent_k: Optional[IntentK_v0] = None


def get_intent_k_v0() -> IntentK_v0:
    global _intent_k
    if _intent_k is None:
        _intent_k = IntentK_v0()
    return _intent_k
