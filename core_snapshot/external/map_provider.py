# -*- coding: utf-8 -*-
"""
Phase 2.2: MapProvider — 慢信号，只产 map_hint 字符串与 produced_ts。
不解析地图结构，只压扁成 token 字符串；不参与任何判断。
"""
from typing import Any, Tuple

from .base_provider import ExternalProvider

MAP_HINT_TOKENS = frozenset({
    "SIDEWALK", "ROADWAY", "CROSSWALK_AHEAD", "NARROW_PATH",
    "UNKNOWN",
})


class MapProvider(ExternalProvider):
    """
    内部缓存 _last_hint, _last_produced_ts。
    main 在 pipeline/context 后调用 feed_context(context, now)；有 hint 时更新缓存。
    poll(now) 仅返回缓存。允许低频/事件驱动更新。
    """

    def __init__(self, interval_sec: float = 1.0):
        self._interval_sec = max(0.0, interval_sec)
        self._last_hint: str = ""
        self._last_produced_ts: float = 0.0
        self._last_update_ts: float = 0.0

    def feed_context(self, context: Any, now: float) -> None:
        """从 context 取 map_hint 相关字段；有则更新缓存，produced_ts 用 now。"""
        if context is None or not isinstance(context, dict):
            return
        if self._interval_sec > 0 and self._last_update_ts > 0 and (now - self._last_update_ts) < self._interval_sec:
            return
        hint_raw = context.get("map_hint") or context.get("map_hint_token") or ""
        hint = hint_raw.strip().upper() if isinstance(hint_raw, str) else ""
        if hint:
            if hint not in MAP_HINT_TOKENS:
                hint = "UNKNOWN"
            self._last_hint = hint
            self._last_produced_ts = now
            self._last_update_ts = now

    def poll(self, now: float) -> Tuple[str, float]:
        """返回当前缓存 (hint, produced_ts)。"""
        return (self._last_hint, self._last_produced_ts)
