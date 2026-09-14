# intervention/outcome_q_v0.py
# Q v0：执行回执层（Execution Receipt）
# 只做事实记录，不引入学习或策略；P 尝试 SAY 时留下结果回执，供统计、解释与后续演进。

from enum import Enum
from dataclasses import dataclass
from typing import Optional, Dict, Any
import time


# -----------------------------
# Q v0 冻结枚举
# -----------------------------

class QAckState(str, Enum):
    ACCEPTED = "ACCEPTED"     # 用户明显接受（未来用）
    REJECTED = "REJECTED"     # 用户明显拒绝（未来用）
    TIMEOUT = "TIMEOUT"       # 无反馈超时
    UNKNOWN = "UNKNOWN"       # v0 默认态（未观测）


class QSource(str, Enum):
    SYSTEM = "SYSTEM"         # 当前全部来自系统推断
    USER = "USER"             # 预留（语音/按键等）


# -----------------------------
# Q v0 数据结构
# -----------------------------

@dataclass
class OutcomeQv0:
    ts: float
    ack_state: QAckState
    source: QSource
    latency_ms: Optional[int]
    meta: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "ts": self.ts,
            "ack_state": self.ack_state.value,
            "source": self.source.value,
            "latency_ms": self.latency_ms,
            "meta": self.meta,
        }


# -----------------------------
# Q v0 核心接口
# -----------------------------

class OutcomeQRecorderV0:
    """
    Q v0：执行回执记录器
    只做一件事：
      - 在 P 层执行完后，记录一次 outcome 回执
    """

    def record(
        self,
        *,
        action_type: str,
        executed: bool,
        reason: str,
        latency_ms: Optional[int] = None,
        extra_meta: Optional[Dict[str, Any]] = None,
    ) -> OutcomeQv0:
        """
        Parameters
        ----------
        action_type : str
            例如 SAY / NONE
        executed : bool
            是否真正执行（TTS 播放成功）
        reason : str
            EXECUTED / BLOCKED_* / FAILED_*
        latency_ms : Optional[int]
            执行耗时（若有）
        extra_meta : dict
            预留字段（如 voice_id, text_len 等）
        """

        # v0 不做用户态判断，统一 UNKNOWN
        ack_state = QAckState.UNKNOWN

        meta = {
            "action_type": action_type,
            "executed": executed,
            "reason": reason,
        }

        if extra_meta:
            meta.update(extra_meta)

        return OutcomeQv0(
            ts=time.time(),
            ack_state=ack_state,
            source=QSource.SYSTEM,
            latency_ms=latency_ms,
            meta=meta,
        )
