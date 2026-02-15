# -*- coding: utf-8 -*-
"""
Phase 2.2: ExternalProvider 抽象 — 外部慢信号只 pull 已完成结果，不阻塞、不判断。
"""
from abc import ABC, abstractmethod
from typing import Any, Tuple


class ExternalProvider(ABC):
    """
    外部感知 Provider 统一接口。
    只允许 poll(now)；不访问 ObservationFrame / runtime_ctx，不 CLOCK / sleep / 阻塞。
    """

    @abstractmethod
    def poll(self, now: float) -> Tuple[Any, float]:
        """
        Returns:
            value: 当前值（OCR 文本 / map_hint 字符串 / speech_event token）
            produced_ts: 感知产生时间（单调秒，仅记录，不参与 if）
        """
        pass
