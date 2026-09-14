from __future__ import annotations

import uuid
from dataclasses import dataclass
from typing import Optional, List

from predictive_attention.context import PalContext
from predictive_attention.schema import AttentionHint, PathStackState, RoiKind, RoiPriority
from predictive_attention.roi.interface import RoiPredictor


@dataclass
class SimpleRoiConfig:
    ttl_s: float = 3.0
    enable_safety: bool = True
    enable_route: bool = True


class SimpleRoiPredictor(RoiPredictor):
    def __init__(self, cfg: Optional[SimpleRoiConfig] = None):
        self._cfg = cfg or SimpleRoiConfig()

    def propose(self, ctx: PalContext, paths: PathStackState) -> List[AttentionHint]:
        out: List[AttentionHint] = []
        now = ctx.now_ts

        in_branch = paths.active_branch is not None

        if self._cfg.enable_safety and not in_branch:
            out.append(
                AttentionHint(
                    hint_id=f"pal_{uuid.uuid4().hex[:8]}",
                    roi_kind=RoiKind.TRAFFIC_SIGNAL,
                    priority=RoiPriority.SAFETY,
                    area_circle=None,
                    area_rect_img=None,
                    reason_codes=["PREDICT_SAFETY_AHEAD"],
                    confidence=0.55,
                    ttl_s=self._cfg.ttl_s,
                    created_ts=now,
                    meta={"from": "simple_roi_predictor"},
                )
            )

        if self._cfg.enable_route and (ctx.goal is not None or in_branch):
            out.append(
                AttentionHint(
                    hint_id=f"pal_{uuid.uuid4().hex[:8]}",
                    roi_kind=RoiKind.EXIT_AREA,
                    priority=RoiPriority.ROUTE,
                    area_circle=None,
                    area_rect_img=None,
                    reason_codes=["PREDICT_ROUTE_DECISION_POINT"],
                    confidence=0.5 if ctx.goal else 0.45,
                    ttl_s=self._cfg.ttl_s,
                    created_ts=now,
                    meta={"branch": bool(in_branch)},
                )
            )

        return out
