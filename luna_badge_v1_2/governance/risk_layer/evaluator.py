from collections import deque
from typing import Deque, Optional

from .dynamic.vo_lite import evaluate_vo_lite
from .dynamic_risk import evaluate_dynamic_collision
from .dynamic.cpa import is_cpa_invalidated
from .dynamic.trajectory_shape import estimate_curvature
from .interfaces import RiskSignal, WorldSnapshot
from .static_risk import evaluate_static_collision
from .zone_risk import evaluate_zone_violation


_LEVEL_ORDER = ["UNKNOWN", "LOW", "MEDIUM", "HIGH"]
_CURVATURE_THRESHOLD = 0.7


def _level_rank(level: str) -> int:
    return _LEVEL_ORDER.index(level)


def apply_risk_decay(previous_risk: Optional[RiskSignal], current: RiskSignal) -> RiskSignal:
    if previous_risk is None:
        return current
    if _level_rank(current.risk_level) >= _level_rank(previous_risk.risk_level):
        return current
    # decay by one level per tick
    prev_rank = _level_rank(previous_risk.risk_level)
    new_rank = max(prev_rank - 1, 0)
    return RiskSignal(
        risk_present=new_rank > 0,
        risk_level=_LEVEL_ORDER[new_rank],
        risk_type=previous_risk.risk_type if new_rank > 0 else "UNKNOWN",
        time_to_risk=previous_risk.time_to_risk,
        confidence=None,
        reason_codes=(previous_risk.reason_codes or []) + ["RISK_DECAY"],
    )


def smooth_risk_over_window(signals: Deque[RiskSignal], window: int = 3) -> RiskSignal:
    if not signals:
        return RiskSignal(False, "UNKNOWN", "UNKNOWN", None, None, [])
    recent = list(signals)[-window:]
    worst = max(recent, key=lambda s: _level_rank(s.risk_level))
    return worst


class RiskEvaluator:
    def __init__(self) -> None:
        self._history: Deque[RiskSignal] = deque(maxlen=3)
        self._last_heading: Optional[float] = None
        self._last_ts: Optional[float] = None
        self._last_rel: Optional[dict] = None

    def evaluate(self, snapshot: WorldSnapshot, horizon_sec: float = 3.0) -> RiskSignal:
        try:
            if horizon_sec <= 0:
                return RiskSignal(False, "UNKNOWN", "UNKNOWN", None, None, [])

            signal = evaluate_static_collision(snapshot, horizon_sec)
            if signal is not None:
                signal = RiskSignal(
                    risk_present=True,
                    risk_level=signal.risk_level,
                    risk_type=signal.risk_type,
                    time_to_risk=signal.time_to_risk,
                    confidence=None,
                    reason_codes=[],
                )
                signal = apply_risk_decay(self._history[-1] if self._history else None, signal)
                self._history.append(signal)
                self._last_heading = snapshot.self_heading
                self._last_ts = snapshot.ts
                return smooth_risk_over_window(self._history)

            signal = evaluate_zone_violation(snapshot, horizon_sec)
            if signal is not None:
                signal = RiskSignal(
                    risk_present=True,
                    risk_level=signal.risk_level,
                    risk_type=signal.risk_type,
                    time_to_risk=signal.time_to_risk,
                    confidence=None,
                    reason_codes=[],
                )
                signal = apply_risk_decay(self._history[-1] if self._history else None, signal)
                self._history.append(signal)
                self._last_heading = snapshot.self_heading
                self._last_ts = snapshot.ts
                return smooth_risk_over_window(self._history)

            for obj in snapshot.objects:
                if obj.velocity is None:
                    continue
                prev = self._last_rel.get(obj.object_id) if self._last_rel else None
                event = evaluate_vo_lite(
                    snapshot.self_position,
                    snapshot.self_velocity,
                    obj.position,
                    obj.velocity,
                    horizon_sec=horizon_sec,
                    danger_radius=obj.radius,
                    self_acc=None,
                    other_acc=obj.acceleration,
                )
                if event is not None:
                    if prev and is_cpa_invalidated(
                        prev.get("closing_speed", event.closing_speed),
                        event.closing_speed,
                        prev.get("ttc", event.time_to_risk),
                        event.time_to_risk,
                    ):
                        continue
                    curvature = 0.0
                    if self._last_heading is not None and self._last_ts is not None:
                        curvature = estimate_curvature(
                            self._last_heading,
                            snapshot.self_heading,
                            max(snapshot.ts - self._last_ts, 0.001),
                        )
                    level = event.level
                    reasons = []
                    if curvature > _CURVATURE_THRESHOLD and level == "HIGH":
                        level = "MEDIUM"
                        reasons.append("CURVATURE_BREAKS_CPA")
                    signal = RiskSignal(
                        risk_present=True,
                        risk_level=level,
                        risk_type="RELATIVE_MOTION",
                        time_to_risk=event.time_to_risk,
                        confidence=None,
                        reason_codes=reasons,
                    )
                    self._last_rel = {
                        obj.object_id: {
                            "closing_speed": event.closing_speed,
                            "ttc": event.time_to_risk,
                        }
                    }
                    if "CURVATURE_BREAKS_CPA" in reasons:
                        self._history.clear()
                    signal = apply_risk_decay(self._history[-1] if self._history else None, signal)
                    self._history.append(signal)
                    self._last_heading = snapshot.self_heading
                    self._last_ts = snapshot.ts
                    return smooth_risk_over_window(self._history)

            signal = evaluate_dynamic_collision(snapshot, horizon_sec)
            if signal is not None:
                signal = RiskSignal(
                    risk_present=True,
                    risk_level=signal.risk_level,
                    risk_type=signal.risk_type,
                    time_to_risk=signal.time_to_risk,
                    confidence=None,
                    reason_codes=[],
                )
                signal = apply_risk_decay(self._history[-1] if self._history else None, signal)
                self._history.append(signal)
                self._last_heading = snapshot.self_heading
                self._last_ts = snapshot.ts
                return smooth_risk_over_window(self._history)

            signal = RiskSignal(False, "LOW", "UNKNOWN", None, None, [])
            signal = apply_risk_decay(self._history[-1] if self._history else None, signal)
            self._history.append(signal)
            self._last_heading = snapshot.self_heading
            self._last_ts = snapshot.ts
            return smooth_risk_over_window(self._history)
        except Exception:
            return RiskSignal(False, "UNKNOWN", "UNKNOWN", None, None, [])
