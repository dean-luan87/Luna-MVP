from __future__ import annotations

from typing import Any, Optional

from a3.engine import A3Engine
from a3.config import A3Config
from a3.providers.default import DefaultA3SignalProvider

from runtime.observation_frame import ObservationFrame
from runtime.gates import should_advance_state
from intervention.eligibility import infer_task_state, compute_intervention_eligibility
from intervention.engagement_v0 import get_engagement_v0
from intervention.rhythm_v0 import get_rhythm_v0


class A3Runtime:
    """
    Runtime wiring for A3.
    - Read-only: collects signals and updates runtime context.
    - Safe default: A3Config(enabled=False)
    - 补丁 v1：决策入口为 on_observation(obs)，基于 obs 推进 rhythm/engagement。
    """

    def __init__(self, config: A3Config, managers: Any):
        self.engine = A3Engine(config)
        self.provider = DefaultA3SignalProvider(
            risk_mgr=managers.risk,
            nav_mgr=managers.nav,
            vision_mgr=managers.vision,
            advice_mgr=managers.advice,
            task_mgr=managers.task,
        )
        self.last_mode = None
        self.last_signals = None

    def tick(self, runtime_ctx: Any, now_ms: Optional[int] = None):
        """Legacy：仍用于在 build_real_obs 内拉取 mode/signals 填 ObservationFrame。"""
        signals = self.provider.collect()
        mode = self.engine.tick(signals, now_ms)
        setattr(runtime_ctx, "env_mode", mode)
        self.last_signals = signals
        self.last_mode = mode
        return mode

    def on_observation(self, runtime_ctx: Any, obs: ObservationFrame) -> Any:
        """
        补丁 v1 唯一决策入口：基于 obs 推进 rhythm/engagement，只记录不采样。
        仅当 should_advance_state(obs) 为 True 时才推进 L2/TTL/冷却等状态。
        """
        if not should_advance_state(obs):
            return self.last_mode

        signals = self.last_signals
        mode = self.last_mode
        if signals is None or mode is None:
            return self.last_mode

        # 主线 A：介入资格
        complexity_effective = float(mode.debug.get("raw_effective", 0.0)) if mode.debug else 0.0
        has_goal = bool(getattr(signals, "has_goal", False))
        explore_mode = bool(getattr(signals, "explore_mode", False))
        task_state = infer_task_state(has_goal, explore_mode)
        eligibility = compute_intervention_eligibility(task_state, complexity_effective)

        # 节律与介入强度：用 obs 的 ts/dt/pal/complexity/vc，且本路径仅在 should_advance_state 为 True 时进入
        rhythm_state = get_rhythm_v0().tick(
            now=obs.ts,
            pal=obs.pal,
            eligible=eligibility["allowed"],
            vc=obs.vc,
            task_state=task_state.value,
        )
        eng = get_engagement_v0().on_observation(obs, rhythm_state=rhythm_state)

        runtime_ctx.rhythm_state = rhythm_state
        runtime_ctx.engagement = {
            "level": eng.level,
            "advice_scale": eng.advice_scale,
            "pal_lookahead_m": eng.pal_lookahead_m,
            "speak_cooldown_s": eng.speak_cooldown_s,
        }
        runtime_ctx.eligibility = eligibility
        runtime_ctx.view_confidence = obs.vc
        runtime_ctx.frame_quality = obs.frame_quality

        return self.last_mode
