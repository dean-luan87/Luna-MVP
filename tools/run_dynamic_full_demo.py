"""
三合一 Demo：Dynamic View + Task Adapter（任务链）+ C Adapter（即时安全 veto）

信息流：Descriptor → ObservationEngine → entity_state
     → TaskEngine（snapshot 从 entities 构建）
     → CAdapter（只读 stable_world）
     → PRINT / TRACE

不改变现有模块，只做胶水层。

运行：python3 tools/run_dynamic_full_demo.py
（从仓库根或 tools/ 执行均可；脚本自举 PYTHONPATH）

重点确认的 5 件事：
  ✅ 1. Dynamic View 是唯一的世界事实源（Task / C 都不“自己看世界”）
  ✅ 2. Task 只做：看到稳定实体 → 判断是否关心它
  ✅ 3. C 是只读：根据当前世界 + 当前任务 → veto / allow / hold
  ✅ 4. 遮挡是真实的：INVISIBLE 后 Task 仍存在；C 可根据策略升级风险
  ✅ 5. 模块可拆：去掉 Task → Dynamic + C 可跑；去掉 C → Dynamic + Task 可跑
"""
import sys
from pathlib import Path

# 确保仓库根在 path，便于直接 python3 tools/run_dynamic_full_demo.py
_root = Path(__file__).resolve().parents[1]
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))

import time
from pprint import pprint
import argparse
from dataclasses import dataclass
from typing import Optional

# --- Dynamic View ---
from dynamic_view.engine import ObservationEngine
from dynamic_view.descriptors import EntityDescriptor
from dynamic_view.binder.simple import SimpleBinder
from dynamic_view.scheduler import ObservationScheduler
from dynamic_view.scheduler import (
    ObservationContract,
    ObservationPolicy,
    ContractMode,
)
from dynamic_view.types import ObservationState

# --- Task（任务链）---
from tasks.engine import TaskEngine
from tasks.tasks.traffic_light_task import TrafficLightTask

# --- C（即时安全 veto）---
from c_adapter.adapter import CAdapter

# --- Timeline（旁路观测）---
from observe.timeline import TimelineFrame, TimelineRecorder
from dynamic_view.attention_evolution import evolve_attention_from_profiles
from observe.semantic_stability.loader import load_profiles
from vision_interpretation.interpreter import interpret_ocr
from vision_interpretation.schema import RawTextCandidate


# -------------------------------
# Utility
# -------------------------------
def banner(title):
    print("\n" + "=" * 20 + f" {title} " + "=" * 20)


def print_entities(eng):
    for eid, ent in eng.entities.items():
        print(
            f"{eid:20s} | state={ent.state.name:10s} | last_seen={ent.last_seen_ts:.2f}"
        )


def active_tasks(engine):
    """胶水：TaskEngine 仅 single active_task，适配 demo 的 active_tasks() 语义。"""
    if engine.active_task is None:
        return []
    return [engine.active_task]


def build_snapshot_from_entities(entities, attr_map, now):
    """
    胶水：从 Dynamic View 的 entities + 我们维护的 attr_map 构建 TaskEngine 所需 snapshot。
    TrafficLightTask 需要 perception_facts["traffic_light"] = red|green|unknown。
    """
    stable = {
        eid: ent
        for eid, ent in entities.items()
        if ent.state == ObservationState.STABLE
    }
    light_val = "unknown"
    for eid, ent in stable.items():
        if "traffic_light" in eid:
            attrs = attr_map.get(eid) or {}
            light_val = attrs.get("color", "unknown") or "unknown"
            break
    return {
        "perception_facts": {"traffic_light": light_val},
        "navigation_state": {"floor_state": "unknown"},
        "now": now,
    }


def snapshot_timeline(
    obs,
    task_engine,
    c_decision,
    ts,
    signals=None,
    roi_debug=None,
    map_download_debug=None,
    roi_perception_debug=None,
    roi_learning_debug=None,
    visual_semantic_debug=None,
    attention_debug=None,
    vision_interpretation=None,
    advice_budget_debug=None,
):
    """
    构建 TimelineFrame：记录每个 tick 的"所见、所想、所裁决"。
    不参与决策，只做旁路观测。
    
    支持 Task v1 (TaskBase) 和 Task v2 (BaseTask)。
    """
    tasks_list = []
    for t in active_tasks(task_engine):
        # 判断是 Task v2 (BaseTask) 还是 Task v1 (TaskBase)
        # Task v2 有 state 属性，Task v1 有 status 属性
        if hasattr(t, 'state'):
            # Task v2: BaseTask
            task_info = {
                "task": getattr(t, 'task_name', 'Unknown'),
                "state": t.state.name if hasattr(t.state, 'name') else str(t.state),
                "reason": t.last_reason,
                "since": getattr(t, 'started_at', None),
            }
        else:
            # Task v1: TaskBase
            task_info = {
                "task": t.name,
                "state": t.status.value,
                "reason": t.last_reason,
                "since": None,  # Task v1 没有 started_at
            }
        tasks_list.append(task_info)
    
    signals = signals or []
    roi_debug = roi_debug or {}
    map_download_debug = map_download_debug or {}
    roi_perception_debug = roi_perception_debug or {}
    roi_learning_debug = roi_learning_debug or {}
    attention_debug = attention_debug or {}

    return TimelineFrame(
        ts=ts,
        entities={
            eid: {
                "state": ent.state.name,
                "last_seen": ent.last_seen_ts,
            }
            for eid, ent in obs.entities.items()
        },
        tasks=tasks_list,
        c_decision={k: v.value for k, v in c_decision.items()},
        signals=[
            {
                "signal_type": s.signal_type,
                "provider": s.provider,
                "ts": s.ts,
                "payload": s.payload,
            }
            for s in signals
        ],
        roi_debug=roi_debug,
        map_download_debug=map_download_debug,
        roi_perception_debug=roi_perception_debug,
        roi_learning_debug=roi_learning_debug,
        visual_semantic_debug=visual_semantic_debug,
        attention_debug=attention_debug,
        vision_interpretation=vision_interpretation,
        advice_budget_debug=advice_budget_debug,
    )


# -------------------------------
# Demo Main
# -------------------------------
@dataclass
class RuntimeFlags:
    enable_attention_evolution: bool = False


@dataclass
class RuntimePaths:
    semantic_stability_profiles: Optional[str] = None


@dataclass
class RuntimeContext:
    flags: RuntimeFlags
    paths: RuntimePaths


def _build_attention_config(context: RuntimeContext):
    base_attention = {
        "exit_area": 0.4,
        "traffic_signal": 0.5,
        "elevator": 0.3,
        "platform": 0.2,
        "bus_stop": 0.2,
    }
    if not context.flags.enable_attention_evolution:
        return base_attention, base_attention

    profiles_path = context.paths.semantic_stability_profiles
    if not profiles_path:
        return base_attention, base_attention

    try:
        profiles = load_profiles(profiles_path)
    except Exception:
        return base_attention, base_attention

    evolved = evolve_attention_from_profiles(
        base_attention=base_attention,
        profiles=profiles,
        enabled=True,
        max_boost_ratio=0.5,
    )
    return base_attention, evolved


def _maybe_visual_interpretation(step: str):
    if step == "step_1":
        raw = [
            RawTextCandidate(text="EXIT", confidence=0.82),
            RawTextCandidate(text="E X I T", confidence=0.61),
        ]
        return interpret_ocr(roi_kind="exit_area", raw_text_candidates=raw).__dict__
    if step == "step_4":
        raw = [
            RawTextCandidate(text="EXIT", confidence=0.74),
        ]
        return interpret_ocr(roi_kind="exit_area", raw_text_candidates=raw).__dict__
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="runs/dynamic_demo.timeline.jsonl")
    ap.add_argument("--enable-attention-evolution", action="store_true")
    ap.add_argument("--enable-vision-interpretation", action="store_true")
    ap.add_argument("--semantic-profiles", default=None)
    args = ap.parse_args()

    t0 = time.time()
    attr_map = {}  # entity_id -> last descriptor.attributes（胶水维护）

    # ========= Dynamic View =========
    banner("Init Dynamic View")

    binder = SimpleBinder()
    scheduler = ObservationScheduler()

    scheduler.register(
        ObservationContract(
            contract_id="safety_default",
            mode=ContractMode.AUTONOMOUS,
            entity_id=None,
            policy=ObservationPolicy(
                max_invisible_time=0.8,
                recovery_grace_time=0.3,
                priority=10,
            ),
        )
    )

    obs = ObservationEngine(
        scheduler=scheduler,
        binder=binder,
    )

    # ========= Task Engine =========
    banner("Init Task Engine")

    task_engine = TaskEngine()

    # ========= C Controller =========
    banner("Init C Controller")

    c_adapter = CAdapter()

    # ========= Timeline Recorder =========
    timeline_fp = open(args.out, "w", encoding="utf-8")
    recorder = TimelineRecorder(timeline_fp)

    context = RuntimeContext(
        flags=RuntimeFlags(enable_attention_evolution=args.enable_attention_evolution),
        paths=RuntimePaths(semantic_stability_profiles=args.semantic_profiles),
    )
    base_attention, evolved_attention = _build_attention_config(context)
    attention_debug = {
        "enabled": bool(context.flags.enable_attention_evolution),
        "base_attention": base_attention,
        "evolved_attention": evolved_attention,
    }

    # ========= Step 1：红绿灯出现 =========
    banner("Step 1: Traffic Light Appears")

    light_desc = EntityDescriptor(
        kind="traffic_light",
        signature="sig_light_main_cross",
        attributes={"color": "red"},
    )

    light_eid = obs.ingest_descriptor(light_desc, t0)
    if light_eid:
        attr_map[light_eid] = light_desc.attributes or {}
    obs.tick(t0)
    obs.tick(t0 + 0.1)

    print_entities(obs)

    # 记录 Timeline
    stable_world = obs.stable_world_state()
    c_decision = c_adapter.decide(stable_world)
    vision_interpretation = (
        _maybe_visual_interpretation("step_1") if args.enable_vision_interpretation else None
    )
    frame = snapshot_timeline(
        obs,
        task_engine,
        c_decision,
        t0 + 0.1,
        attention_debug=attention_debug,
        vision_interpretation=vision_interpretation,
    )
    recorder.record(frame)

    # ========= Step 2：Task 关注红绿灯 =========
    banner("Step 2: Task Adapter Reacts")

    snapshot = build_snapshot_from_entities(obs.entities, attr_map, t0 + 0.1)
    if not task_engine.active_task and light_eid:
        task_engine.start_task(
            TrafficLightTask(task_id="tl_main", meta={})
        )
    task_engine.tick(snapshot)

    pprint(active_tasks(task_engine))

    # ========= Step 3：C 读取世界状态 =========
    banner("Step 3: C Safety Check")

    stable_world = obs.stable_world_state()
    c_decision = c_adapter.decide(stable_world)

    print("C decision:", c_decision)

    # 记录 Timeline
    vision_interpretation = (
        _maybe_visual_interpretation("step_2") if args.enable_vision_interpretation else None
    )
    frame = snapshot_timeline(
        obs,
        task_engine,
        c_decision,
        t0 + 0.1,
        attention_debug=attention_debug,
        vision_interpretation=vision_interpretation,
    )
    recorder.record(frame)

    # ========= Step 4：红绿灯变绿 =========
    banner("Step 4: Traffic Light Turns Green")

    light_desc_green = EntityDescriptor(
        kind="traffic_light",
        signature="sig_light_main_cross",
        attributes={"color": "green"},
    )

    eid_green = obs.ingest_descriptor(light_desc_green, t0 + 1.0)
    if eid_green:
        attr_map[eid_green] = light_desc_green.attributes or {}
    obs.tick(t0 + 1.0)
    obs.tick(t0 + 1.1)

    print_entities(obs)

    snapshot = build_snapshot_from_entities(obs.entities, attr_map, t0 + 1.1)
    task_engine.tick(snapshot)

    pprint(active_tasks(task_engine))

    stable_world = obs.stable_world_state()
    c_decision = c_adapter.decide(stable_world)
    print("C decision:", c_decision)

    # 记录 Timeline
    vision_interpretation = (
        _maybe_visual_interpretation("step_4") if args.enable_vision_interpretation else None
    )
    frame = snapshot_timeline(
        obs,
        task_engine,
        c_decision,
        t0 + 1.1,
        attention_debug=attention_debug,
        vision_interpretation=vision_interpretation,
    )
    recorder.record(frame)

    # ========= Step 5：红绿灯消失（遮挡） =========
    banner("Step 5: Occlusion")

    obs.tick(t0 + 3.0)
    print_entities(obs)

    snapshot = build_snapshot_from_entities(obs.entities, attr_map, t0 + 3.0)
    task_engine.tick(snapshot)

    pprint(active_tasks(task_engine))

    stable_world = obs.stable_world_state()
    c_decision = c_adapter.decide(stable_world)
    print("C decision:", c_decision)

    # 记录 Timeline
    vision_interpretation = (
        _maybe_visual_interpretation("step_5") if args.enable_vision_interpretation else None
    )
    frame = snapshot_timeline(
        obs,
        task_engine,
        c_decision,
        t0 + 3.0,
        attention_debug=attention_debug,
        vision_interpretation=vision_interpretation,
    )
    recorder.record(frame)

    # ========= Step 6：新增实体类型（公交/地铁/电梯） =========
    banner("Step 6: New Entity Types (Bus/Subway/Elevator)")

    # 公交
    bus_desc = EntityDescriptor(
        kind="bus",
        signature="bus_71_up",
        attributes={
            "route": "71",
            "direction": "up",
        },
    )
    bus_eid = obs.ingest_descriptor(bus_desc, t0 + 4.0)
    if bus_eid:
        attr_map[bus_eid] = bus_desc.attributes or {}

    # 地铁
    subway_desc = EntityDescriptor(
        kind="subway_train",
        signature="line2_east",
        attributes={
            "line": "2",
            "direction": "east",
        },
    )
    subway_eid = obs.ingest_descriptor(subway_desc, t0 + 4.0)
    if subway_eid:
        attr_map[subway_eid] = subway_desc.attributes or {}

    # 电梯
    elevator_desc = EntityDescriptor(
        kind="elevator",
        signature="elev_A",
        attributes={
            "building": "A",
            "floor": 1,
        },
    )
    elevator_eid = obs.ingest_descriptor(elevator_desc, t0 + 4.0)
    if elevator_eid:
        attr_map[elevator_eid] = elevator_desc.attributes or {}

    obs.tick(t0 + 4.0)
    obs.tick(t0 + 4.1)

    print_entities(obs)

    # 记录 Timeline
    stable_world = obs.stable_world_state()
    c_decision = c_adapter.decide(stable_world)
    vision_interpretation = (
        _maybe_visual_interpretation("step_6") if args.enable_vision_interpretation else None
    )
    frame = snapshot_timeline(
        obs,
        task_engine,
        c_decision,
        t0 + 4.1,
        attention_debug=attention_debug,
        vision_interpretation=vision_interpretation,
    )
    recorder.record(frame)

    print("C decision:", c_decision)

    # 关闭 Timeline
    timeline_fp.close()

    banner("Demo Finished")


if __name__ == "__main__":
    main()
