# execution/p_executor_v0.py
# P 层 v0：仅执行 SAY，服从 M 的 apply_now，结果回写 N

from enum import Enum
from typing import Optional


class PExecutionResult(Enum):
    EXECUTED = "EXECUTED"
    BLOCKED = "BLOCKED"
    FAILED = "FAILED"


class PExecutorV0:
    def __init__(self, tts_engine):
        """
        tts_engine: 任意实现 .say(text: str) 的对象（如 TTS 适配器）
        """
        self.tts = tts_engine

    def try_execute(self, m_action: dict, text: Optional[str] = None) -> dict:
        """
        m_action: M 层输出的 dict（含 action_type / apply_now / modality / urgency）
        text: 要说的内容（由上游准备）

        Returns:
            dict: executed (bool), result (PExecutionResult), reason (str)
        """
        # v0 护栏
        if not m_action.get("apply_now", False):
            return {
                "executed": False,
                "result": PExecutionResult.BLOCKED,
                "reason": "APPLY_NOW_FALSE",
            }

        if m_action.get("action_type") != "SAY":
            return {
                "executed": False,
                "result": PExecutionResult.BLOCKED,
                "reason": "ACTION_NOT_ALLOWED_IN_V0",
            }

        if not text:
            return {
                "executed": False,
                "result": PExecutionResult.FAILED,
                "reason": "EMPTY_TEXT",
            }

        # --- 真实执行 ---
        try:
            self.tts.say(text)
            return {
                "executed": True,
                "result": PExecutionResult.EXECUTED,
                "reason": "SAY_OK",
            }
        except Exception as e:
            return {
                "executed": False,
                "result": PExecutionResult.FAILED,
                "reason": f"TTS_ERROR:{str(e)}",
            }
