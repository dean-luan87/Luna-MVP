from dataclasses import dataclass
from typing import Callable
from enum import Enum
import time
from infra.logging_manager import get_logger

logger = get_logger("task_transition")


class TaskDecision(Enum):
    KEEP = "keep"
    ASK_END = "ask_end"
    END = "end"


@dataclass
class PositionState:
    at_target: bool
    distance_to_target: float
    stationary_seconds: float


@dataclass
class UserIntentState:
    want_stop: bool
    want_continue: bool


@dataclass
class TaskContext:
    position: PositionState
    intent: UserIntentState


class TaskTransitionManager:
    def __init__(self, ask_end_callback: Callable[[], None]) -> None:
        self._ask_end_callback = ask_end_callback
        # ASK_END 状态防抖
        self._ask_end_pending: bool = False
        self._last_ask_end_ts: float = 0.0
        self._ask_end_cooldown_sec: float = 10.0  # 10 秒不重复问

    def clear_ask_end_pending(self) -> None:
        """清除 ASK_END 待处理状态（用户做出选择后调用）"""
        self._ask_end_pending = False
        self._last_ask_end_ts = time.time()
        logger.debug("[TASK] clear ASK_END pending by user decision")

    def decide(self, ctx: TaskContext) -> TaskDecision:
        if ctx.intent.want_stop:
            logger.info("[TASK] user wants to stop, END")
            return TaskDecision.END

        # 接近目标判断（带状态+时间防抖）
        if ctx.position.at_target or ctx.position.distance_to_target < 1.5:
            now = time.time()
            if (not self._ask_end_pending) or (now - self._last_ask_end_ts > self._ask_end_cooldown_sec):
                self._ask_end_pending = True
                self._last_ask_end_ts = now
                logger.info("[TASK] near target, ASK_END (emit)")
                self._ask_end_callback()
                return TaskDecision.ASK_END
            else:
                logger.debug("[TASK] near target, ASK_END already pending, skip")
                return TaskDecision.ASK_END
        else:
            # 一旦离开"接近区域"，就允许未来再次触发
            if self._ask_end_pending:
                logger.debug("[TASK] leave target area, reset ASK_END pending")
            self._ask_end_pending = False

        if ctx.position.stationary_seconds > 60 and not ctx.intent.want_continue:
            now = time.time()
            if (not self._ask_end_pending) or (now - self._last_ask_end_ts > self._ask_end_cooldown_sec):
                self._ask_end_pending = True
                self._last_ask_end_ts = now
                logger.info("[TASK] stationary too long, ASK_END (emit)")
                self._ask_end_callback()
                return TaskDecision.ASK_END
            else:
                logger.debug("[TASK] stationary too long, ASK_END already pending, skip")
                return TaskDecision.ASK_END

        return TaskDecision.KEEP
