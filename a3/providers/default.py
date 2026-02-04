from __future__ import annotations

from typing import Any, Optional
import os

from a3.types import A3Signals, PerceptionState
from a3.provider_interface import A3SignalProvider


class DefaultA3SignalProvider(A3SignalProvider):
    """
    Read-only adapter.
    Map existing system states -> A3Signals.
    """

    def __init__(
        self,
        risk_mgr: Any,
        nav_mgr: Any,
        vision_mgr: Any,
        advice_mgr: Any,
        task_mgr: Any,
    ):
        self.risk = risk_mgr
        self.nav = nav_mgr
        self.vision = vision_mgr
        self.advice = advice_mgr
        self.task = task_mgr

    @staticmethod
    def _env_float(name: str) -> Optional[float]:
        val = os.environ.get(name)
        if val is None or val == "":
            return None
        try:
            return float(val)
        except ValueError:
            return None

    @staticmethod
    def _env_int(name: str) -> Optional[int]:
        val = os.environ.get(name)
        if val is None or val == "":
            return None
        try:
            return int(val)
        except ValueError:
            return None

    @staticmethod
    def _env_bool(name: str) -> Optional[bool]:
        val = os.environ.get(name)
        if val is None or val == "":
            return None
        return val.lower() in ("1", "true", "yes", "y")

    def collect(self) -> A3Signals:
        risk_density = float(getattr(self.risk, "risk_density", 0.0))
        redline_hit = bool(getattr(self.risk, "redline_hit", False))
        risk_density = self._env_float("A3_RISK_DENSITY") if self._env_float("A3_RISK_DENSITY") is not None else risk_density
        redline_hit = self._env_bool("A3_REDLINE_HIT") if self._env_bool("A3_REDLINE_HIT") is not None else redline_hit

        path_stability = float(getattr(self.nav, "path_stability", 1.0))
        branch_count = int(getattr(self.nav, "branch_count", 0))
        path_stability = self._env_float("A3_PATH_STABILITY") if self._env_float("A3_PATH_STABILITY") is not None else path_stability
        branch_count = self._env_int("A3_BRANCH_COUNT") if self._env_int("A3_BRANCH_COUNT") is not None else branch_count

        roi_count = int(getattr(self.vision, "roi_count", 0))
        roi_type_entropy = float(getattr(self.vision, "roi_type_entropy", 0.0))
        occlusion_ratio = float(getattr(self.vision, "occlusion_ratio", 0.0))
        roi_count = self._env_int("A3_ROI_COUNT") if self._env_int("A3_ROI_COUNT") is not None else roi_count
        roi_type_entropy = self._env_float("A3_ROI_ENTROPY") if self._env_float("A3_ROI_ENTROPY") is not None else roi_type_entropy
        occlusion_ratio = self._env_float("A3_OCCLUSION_RATIO") if self._env_float("A3_OCCLUSION_RATIO") is not None else occlusion_ratio

        recent_speak_rate = float(getattr(self.advice, "recent_speak_rate", 0.0))
        rejected_rate = float(getattr(self.advice, "rejected_rate", 0.0))
        recent_speak_rate = self._env_float("A3_SPEAK_RATE") if self._env_float("A3_SPEAK_RATE") is not None else recent_speak_rate
        rejected_rate = self._env_float("A3_REJECT_RATE") if self._env_float("A3_REJECT_RATE") is not None else rejected_rate

        has_goal = bool(getattr(self.task, "has_goal", False))
        explore_mode = bool(getattr(self.task, "explore_mode", False))
        has_goal = self._env_bool("A3_HAS_GOAL") if self._env_bool("A3_HAS_GOAL") is not None else has_goal
        explore_mode = self._env_bool("A3_EXPLORE_MODE") if self._env_bool("A3_EXPLORE_MODE") is not None else explore_mode

        perception_state_raw = getattr(self.vision, "perception_state", PerceptionState.NORMAL)
        if isinstance(perception_state_raw, str):
            perception_state = PerceptionState.DEGRADED if perception_state_raw == "DEGRADED" else PerceptionState.NORMAL
        elif isinstance(perception_state_raw, PerceptionState):
            perception_state = perception_state_raw
        else:
            perception_state = PerceptionState.NORMAL

        view_confidence = float(getattr(self.vision, "view_confidence", 1.0))
        frame_quality = str(getattr(self.vision, "frame_quality", "GOOD"))
        motion_instability = float(getattr(self.vision, "motion_instability", 0.0))
        path_instability = self._env_float("A3_PATH_INSTABILITY")
        if path_instability is None:
            path_instability = getattr(self.vision, "path_instability", None)
        branch_load = self._env_float("A3_BRANCH_LOAD")
        if branch_load is None and self.vision:
            branch_load = getattr(self.vision, "branch_load", None)
        view_confidence = self._env_float("A3_VIEW_CONFIDENCE") if self._env_float("A3_VIEW_CONFIDENCE") is not None else view_confidence
        frame_quality = os.environ.get("A3_FRAME_QUALITY") or frame_quality

        return A3Signals(
            risk_density=risk_density,
            redline_hit=redline_hit,
            path_stability=path_stability,
            branch_count=branch_count,
            roi_count=roi_count,
            roi_type_entropy=roi_type_entropy,
            occlusion_ratio=occlusion_ratio,
            recent_speak_rate=recent_speak_rate,
            rejected_rate=rejected_rate,
            has_goal=has_goal,
            explore_mode=explore_mode,
            perception_state=perception_state,
            view_confidence=view_confidence,
            frame_quality=frame_quality,
            motion_instability=motion_instability,
            path_instability=path_instability,
            branch_load=branch_load,
        )
