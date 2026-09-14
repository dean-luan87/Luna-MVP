# -*- coding: utf-8 -*-
"""
Phase 2.2: OCRProvider — 只产 OCR 文本与 produced_ts，不读 ObservationFrame，不参与判断。
内部缓存 _last_text / _last_produced_ts；poll(now) 返回缓存；有新结果时由 feed 更新缓存。
"""
from typing import Any, Optional, Tuple

from .base_provider import ExternalProvider


class OCRProvider(ExternalProvider):
    """
    内部仅维护 _last_text, _last_produced_ts。
    main 在 pipeline 后调用 feed_pipeline_result(pipeline_result, now)；有 OCR 结果时更新缓存。
    poll(now) 仅返回上次缓存，不判断 produced_ts 是否过期。
    """

    def __init__(self, interval_sec: float = 1.0):
        self._interval_sec = max(0.0, interval_sec)
        self._last_text: str = ""
        self._last_produced_ts: float = 0.0
        self._last_update_ts: Optional[float] = None
        self._last_pipeline_result: Optional[dict] = None

    def feed_pipeline_result(self, pipeline_result: Optional[dict], now: float) -> None:
        """
        Main 在 pipeline 后调用。若有新 OCR 文本则更新缓存；produced_ts 用传入的 now（感知可用时刻）。
        """
        self._last_pipeline_result = pipeline_result
        if pipeline_result is None:
            return
        if self._interval_sec > 0 and self._last_update_ts is not None:
            if (now - self._last_update_ts) < self._interval_sec:
                return
        modeling = pipeline_result.get("modeling_result") if isinstance(pipeline_result, dict) else None
        if modeling is None:
            return
        candidates = getattr(modeling, "content_candidates", None) or []
        parts = []
        for c in candidates:
            raw = getattr(c, "raw_text", None)
            if raw and isinstance(raw, str):
                parts.append(raw.strip())
        text = " ".join(parts).strip() if parts else ""
        if text:
            self._last_text = text
            self._last_produced_ts = now
            self._last_update_ts = now

    def poll(self, now: float) -> Tuple[str, float]:
        """返回当前缓存 (text, produced_ts)；不判断是否过期。"""
        return (self._last_text, self._last_produced_ts)
