from __future__ import annotations

import json
from typing import Any, Dict, Iterable, List, Optional

from .types import (
    InterpretationKey,
    InterpretationStats,
    StableInterpretationProfile,
)
from .config import StabilityConfig
from .extractors import extract_interpretations, extract_validation_signals, extract_semantic_observations
from .scoring import compute_stability_score


class SemanticStabilityLearner:
    """
    C3.1: Read-only learning over Timeline.
    Produces stability profiles used ONLY for attention/learning, not action.
    """

    def __init__(self, cfg: Optional[StabilityConfig] = None):
        self.cfg = cfg or StabilityConfig()

    def learn_from_frames(
        self,
        frames: Iterable[Dict[str, Any]],
        environment_id: str = "device_default",
        scope: str = "device_local",
        now_ts: Optional[float] = None,
    ) -> List[StableInterpretationProfile]:
        cfg = self.cfg
        stats_map: Dict[InterpretationKey, InterpretationStats] = {}

        latest_ts: float = 0.0

        for frame in frames:
            ts = float(frame.get("ts") or frame.get("timestamp") or 0.0)
            if ts > latest_ts:
                latest_ts = ts

            observations = extract_semantic_observations(frame)
            for obs in observations:
                category = obs.category or "unknown"
                key = InterpretationKey(
                    roi_kind=obs.roi_kind,
                    category=category,
                    meaning=obs.meaning,
                )
                st = stats_map.get(key) or InterpretationStats()
                st.appear_count += 1
                st.last_seen_ts = ts or st.last_seen_ts
                stats_map[key] = st

            _ = extract_validation_signals(frame)

        if now_ts is None:
            now_ts = latest_ts if latest_ts > 0 else 0.0

        profiles: List[StableInterpretationProfile] = []
        for key, st in stats_map.items():
            score = compute_stability_score(st, cfg, now_ts)

            if st.appear_count < cfg.min_appear_for_observe:
                suggestion = "IGNORE"
            else:
                if score.stability >= cfg.promote_threshold and score.confidence >= 0.3:
                    suggestion = "PROMOTE"
                elif score.stability >= cfg.observe_threshold:
                    suggestion = "OBSERVE"
                else:
                    suggestion = "IGNORE"

            profiles.append(
                StableInterpretationProfile(
                    key=key,
                    score=score,
                    suggestion=suggestion,
                    scope=scope,
                    environment_id=environment_id,
                )
            )

        profiles.sort(key=lambda p: (p.key.roi_kind, p.key.category, p.key.meaning))
        return profiles

    def learn_from_timeline_jsonl(
        self,
        path: str,
        environment_id: str = "device_default",
        scope: str = "device_local",
    ) -> List[StableInterpretationProfile]:
        def _frames():
            with open(path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    yield json.loads(line)

        return self.learn_from_frames(
            _frames(),
            environment_id=environment_id,
            scope=scope,
        )
