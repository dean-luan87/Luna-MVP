# -*- coding: utf-8 -*-
"""
Phase 3.1: Episode 窗口缓冲器 — 只做窗口截取（pre_n + center + post_n），不判断、不写回。
只处理 sampled 记录；record 为不透明字典，不访问外部字段。
"""
from collections import deque
from dataclasses import dataclass, field
from typing import Any, List, Optional


@dataclass
class EpisodeWindowConfig:
    pre_n: int
    post_n: int


@dataclass
class EpisodeWindow:
    trigger_type: str
    trigger_ts: float
    trigger_seq: int
    records: List[dict] = field(default_factory=list)


class EpisodeWindowBuffer:
    """
    内部 deque 只存最近 pre_n 条 sampled 记录。
    on_sample(record, trigger=None)：无 trigger 则只入队；有 trigger 且未在 capture 则开启 capture，
    center=当前 record，收集 post_n 条后返回 EpisodeWindow 并 reset。capture 期间新 trigger 丢弃。
    """

    def __init__(self, config: EpisodeWindowConfig) -> None:
        self._config = config
        self._deque: deque = deque(maxlen=config.pre_n)
        self._capturing = False
        self._pre_list: List[dict] = []
        self._center: Optional[dict] = None
        self._post_list: List[dict] = []
        self._trigger_type: str = ""
        self._trigger_ts: float = 0.0
        self._trigger_seq: int = 0

    def on_sample(self, record: dict, trigger: Any = None) -> Optional[EpisodeWindow]:
        """
        record: 单条 OBS_V1 风格字典（含 ts/seq/obs/decision 等），不透明存储。
        trigger: EpisodeTrigger 或带 type/ts/seq 的对象；None 表示仅维护 pre 窗口。
        """
        if self._capturing:
            self._post_list.append(record)
            if len(self._post_list) >= self._config.post_n:
                out = EpisodeWindow(
                    trigger_type=self._trigger_type,
                    trigger_ts=self._trigger_ts,
                    trigger_seq=self._trigger_seq,
                    records=self._pre_list + [self._center] + self._post_list,
                )
                self._reset_capture()
                return out
            return None

        if trigger is not None:
            self._capturing = True
            self._pre_list = list(self._deque)
            self._center = record
            self._post_list = []
            self._trigger_type = getattr(trigger, "type", "") or ""
            self._trigger_ts = getattr(trigger, "ts", 0.0) or 0.0
            self._trigger_seq = getattr(trigger, "seq", 0) or 0
            return None

        self._deque.append(record)
        return None

    def _reset_capture(self) -> None:
        self._capturing = False
        self._pre_list = []
        self._center = None
        self._post_list = []
        self._trigger_type = ""
        self._trigger_ts = 0.0
        self._trigger_seq = 0
