# -*- coding: utf-8 -*-
"""
Phase 3.1: Episode 触发器 — 只检测、不截流。
仅根据 speech_event 与 decision.safety_level 变化触发，不读取 OCR/map 参与判断。
"""
from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class EpisodeTrigger:
    type: str   # "SPEECH" | "SAFETY_CHANGE"
    ts: float
    seq: int


def _safety_level_value(decision: Any) -> Any:
    """从 decision 取出可比较的 safety_level 值（enum.value 或原值）。"""
    sl = getattr(decision, "safety_level", None)
    if sl is None:
        return None
    return getattr(sl, "value", sl)


class EpisodeTriggerDetector:
    """
    仅保存 last_sampled_seq、last_safety_level，用于相邻 sampled 比较。
    触发条件：obs.sampled 为 True 时，
      - speech_event != "" -> SPEECH
      - 否则 decision.safety_level 与 last_safety_level 不同 -> SAFETY_CHANGE
    last_safety_level 仅在 sampled=True 时更新。
    """

    def __init__(self) -> None:
        self.last_sampled_seq: int = -1
        self.last_safety_level: Any = None

    def on_record(self, obs: Any, decision: Any) -> Optional[EpisodeTrigger]:
        """
        只检测、不截流。不读取 OCR/map 字段做任何判断。
        """
        if not getattr(obs, "sampled", False):
            return None

        ts = getattr(obs, "ts", 0.0)
        seq = getattr(obs, "seq", 0)
        speech_event = getattr(obs, "speech_event", "") or ""

        current_safety = _safety_level_value(decision)

        # 1) speech_event 非空 -> SPEECH
        if speech_event != "":
            self.last_sampled_seq = seq
            self.last_safety_level = current_safety
            return EpisodeTrigger(type="SPEECH", ts=ts, seq=seq)

        # 2) safety_level 变化 -> SAFETY_CHANGE
        if current_safety != self.last_safety_level:
            self.last_sampled_seq = seq
            self.last_safety_level = current_safety
            return EpisodeTrigger(type="SAFETY_CHANGE", ts=ts, seq=seq)

        # 仅 sampled=True 时更新 last_safety_level
        self.last_sampled_seq = seq
        self.last_safety_level = current_safety
        return None
