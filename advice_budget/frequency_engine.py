from __future__ import annotations

from typing import Dict, Tuple

from .levels import AdviceLevel
from .frequency import FrequencyPolicy, FrequencyState


class FrequencyEngine:
    def __init__(self, policies: Dict[AdviceLevel, FrequencyPolicy]):
        self.policies = policies
        self.state: Dict[Tuple[str, str], FrequencyState] = {}

    def _reset_window_if_needed(self, st: FrequencyState, now: float):
        if now - st.window_start_ts >= 60:
            st.window_start_ts = now
            st.used_in_window = 0

    def can_emit(self, advice_kind: str, source: str, level: AdviceLevel, now: float) -> bool:
        if level == AdviceLevel.EMERGENCY:
            return True

        pol = self.policies[level]
        key = (advice_kind, source)
        st = self.state.setdefault(key, FrequencyState())

        if now - st.last_emit_ts < pol.cooldown_s:
            return False

        self._reset_window_if_needed(st, now)
        if st.used_in_window >= pol.quota_per_min:
            return False

        return True

    def mark_emitted(self, advice_kind: str, source: str, level: AdviceLevel, now: float):
        if level == AdviceLevel.EMERGENCY:
            return
        key = (advice_kind, source)
        st = self.state.setdefault(key, FrequencyState())
        self._reset_window_if_needed(st, now)
        st.last_emit_ts = now
        st.used_in_window += 1
