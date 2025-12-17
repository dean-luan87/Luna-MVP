"""Replay input models (v1.4.9 P0-2-A).

原则（P0-2 第一性原则）：
- Replay = 复演一次“已经发生过的、对用户可感知的行为序列”
- 输入只包含：
  1) 当时系统看到的（Perception snapshots）
  2) 当时系统知道的（Map snapshots / initial_state）
  3) 当时系统被允许做的（Intent & Control）

强约束：
- Replay 输入必须完全文件化/内存化
- 不允许隐式依赖系统时间或设备输入

注意：本文件只定义输入结构与校验，不改任何业务逻辑。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass(frozen=True)
class ReplayTimeSpec:
    """逻辑时间轴（禁止 wall clock）。"""

    t0: int = 0
    delta_ms: int = 100
    steps: int = 0

    def validate(self) -> List[str]:
        errors: List[str] = []
        if self.t0 != 0:
            errors.append("time.t0 must be 0 in replay mode")
        if self.delta_ms <= 0:
            errors.append("time.delta_ms must be > 0")
        if self.steps <= 0:
            errors.append("time.steps must be > 0")
        return errors


@dataclass(frozen=True)
class ReplayInitialState:
    """回放开始时的最小初始事实。"""

    has_active_task: bool = False


@dataclass(frozen=True)
class VisionFrameSnapshot:
    """视觉快照（结构化结果，不是原始图像）。"""

    step: int
    vision_state: str
    objects: List[Dict[str, Any]] = field(default_factory=list)
    confidence: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class MapSnapshot:
    """地图快照（固定 MapAdapter 输出，不做在线请求）。"""

    step: int
    route_state: str
    distance_to_turn: Optional[float] = None
    extra: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class IntentEvent:
    """意图/控制输入（必须显式化）。"""

    step: int
    intent: str
    payload: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ReplayInput:
    """P0-2 SSOT 输入结构。"""

    replay_id: str
    seed: int
    time: ReplayTimeSpec
    initial_state: ReplayInitialState
    vision_frames: List[VisionFrameSnapshot]
    map_snapshots: List[MapSnapshot] = field(default_factory=list)
    intents: List[IntentEvent] = field(default_factory=list)

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "ReplayInput":
        time_spec = ReplayTimeSpec(**(data.get("time") or {}))
        initial_state = ReplayInitialState(**(data.get("initial_state") or {}))

        vframes = [VisionFrameSnapshot(**x) for x in (data.get("vision_frames") or [])]
        msnaps = [MapSnapshot(**x) for x in (data.get("map_snapshots") or [])]
        intents = [IntentEvent(**x) for x in (data.get("intents") or [])]

        return ReplayInput(
            replay_id=str(data.get("replay_id") or ""),
            seed=int(data.get("seed") or 0),
            time=time_spec,
            initial_state=initial_state,
            vision_frames=vframes,
            map_snapshots=msnaps,
            intents=intents,
        )

    def validate(self) -> List[str]:
        errors: List[str] = []
        if not self.replay_id:
            errors.append("replay_id is required")
        if self.seed is None:
            errors.append("seed is required")

        errors.extend(self.time.validate())

        # vision frames are required
        if not self.vision_frames:
            errors.append("vision_frames must not be empty")

        # step bounds & monotonicity
        max_step = self.time.steps - 1
        for vf in self.vision_frames:
            if vf.step < 0 or vf.step > max_step:
                errors.append(f"vision_frames.step out of range: {vf.step}")
            if not vf.vision_state:
                errors.append(f"vision_frames[{vf.step}].vision_state is required")

        for ms in self.map_snapshots:
            if ms.step < 0 or ms.step > max_step:
                errors.append(f"map_snapshots.step out of range: {ms.step}")
            if not ms.route_state:
                errors.append(f"map_snapshots[{ms.step}].route_state is required")

        for it in self.intents:
            if it.step < 0 or it.step > max_step:
                errors.append(f"intents.step out of range: {it.step}")
            if not it.intent:
                errors.append(f"intents[{it.step}].intent is required")

        # explicit cancel->confirm support (not forced, but lint)
        cancel_steps = [i.step for i in self.intents if i.intent == "cancel_task"]
        confirm_steps = [i.step for i in self.intents if i.intent == "confirm_cancel"]
        if cancel_steps and not confirm_steps:
            errors.append(
                "intents contains cancel_task but no confirm_cancel; "
                "v1.4.x contract defines a confirm-cancel two-step"
            )

        return errors

    def time_ms_at_step(self, step: int) -> int:
        return self.time.t0 + step * self.time.delta_ms

    def _latest_by_step(self, items: List[Any], step: int) -> Optional[Any]:
        latest = None
        latest_step = -1
        for it in items:
            if it.step <= step and it.step >= latest_step:
                latest = it
                latest_step = it.step
        return latest

    def vision_at_step(self, step: int) -> VisionFrameSnapshot:
        vf = self._latest_by_step(self.vision_frames, step)
        if vf is None:
            # should not happen if validate() passed
            raise ValueError("No vision frame available")
        return vf

    def map_at_step(self, step: int) -> Optional[MapSnapshot]:
        return self._latest_by_step(self.map_snapshots, step)

    def intents_at_step(self, step: int) -> List[IntentEvent]:
        return [i for i in self.intents if i.step == step]
