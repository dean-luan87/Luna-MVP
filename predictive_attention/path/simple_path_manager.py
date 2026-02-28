from __future__ import annotations

import math
import time
import uuid
from dataclasses import dataclass
from typing import Optional, Tuple, List

from predictive_attention.context import PalContext
from predictive_attention.schema import PathKind, PathSegment, PathStackState, MotionSample
from predictive_attention.path.interface import PathManager


def _bearing_deg(p0: Tuple[float, float], p1: Tuple[float, float]) -> Optional[float]:
    dx = p1[0] - p0[0]
    dy = p1[1] - p0[1]
    if abs(dx) < 1e-6 and abs(dy) < 1e-6:
        return None
    ang = math.degrees(math.atan2(dy, dx))
    return (ang + 360.0) % 360.0


def _ang_diff_deg(a: float, b: float) -> float:
    d = abs(a - b) % 360.0
    return d if d <= 180.0 else 360.0 - d


@dataclass
class SimplePathConfig:
    branch_angle_deg: float = 30.0
    return_angle_deg: float = 20.0
    branch_timeout_s: float = 10.0
    min_samples: int = 2


class SimplePathManager(PathManager):
    def __init__(self, cfg: Optional[SimplePathConfig] = None):
        self._cfg = cfg or SimplePathConfig()
        now = time.time()
        self._state = PathStackState(
            main=PathSegment(
                segment_id=f"main_{uuid.uuid4().hex[:8]}",
                kind=PathKind.MAIN,
                start_ts=now,
                last_ts=now,
                avg_heading_deg=None,
                avg_speed_mps=None,
            ),
            active_branch=None,
        )

    def _estimate_heading(self, motion: List[MotionSample]) -> Optional[float]:
        if len(motion) < self._cfg.min_samples:
            return None
        p0 = motion[0].position_xy
        p1 = motion[-1].position_xy
        return _bearing_deg(p0, p1)

    def update(self, ctx: PalContext) -> PathStackState:
        now = ctx.now_ts
        heading = self._estimate_heading(ctx.motion_window)

        self._state.main.last_ts = now

        main_heading = self._state.main.avg_heading_deg
        if heading is None:
            return self._state
        if main_heading is None:
            self._state.main.avg_heading_deg = heading
            return self._state
        diff = _ang_diff_deg(heading, main_heading)

        br = self._state.active_branch
        if br is not None:
            br.last_ts = now
            if (now - br.start_ts) > self._cfg.branch_timeout_s:
                self._state.active_branch = None
                self._state.main.avg_heading_deg = heading
                return self._state
            if diff <= self._cfg.return_angle_deg:
                self._state.active_branch = None
                self._state.main.avg_heading_deg = heading
                return self._state
            br.avg_heading_deg = heading
            return self._state

        branch_created = False
        if diff >= self._cfg.branch_angle_deg:
            self._state.active_branch = PathSegment(
                segment_id=f"branch_{uuid.uuid4().hex[:8]}",
                kind=PathKind.BRANCH,
                start_ts=now,
                last_ts=now,
                avg_heading_deg=heading,
                avg_speed_mps=None,
                parent_main_id=self._state.main.segment_id,
                meta={"trigger_diff_deg": diff},
            )
            branch_created = True

        if not branch_created:
            self._state.main.avg_heading_deg = heading
        return self._state
