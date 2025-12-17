# P0-2-A｜Replay 输入标准化（Deterministic Replay · Input Spec）

本文件是 v1.4.9 P0-2-A 的 **Replay Input SSOT** 说明。

目标不是“能回放”，而是：任何一次回放，都是对同一条“事实世界线”的复演。

---

## 第一性原则

Replay = 还原一次“已经发生过的、对用户可感知的行为序列”。

因此 Replay 输入只允许三类来源：
1. 当时系统“看到的”（Vision snapshots）
2. 当时系统“知道的”（Map snapshots / initial_state）
3. 当时系统“被允许做的”（Intents & Control）

其他一律禁止。

---

## 输入来源一：时间（Time）

规则：
- 禁止使用任何系统时间 / wall clock
- 禁止隐式 sleep / now / monotonic

标准做法：
- 使用逻辑时间轴（step index 推进）

示例：

```json
"time": {
  "t0": 0,
  "delta_ms": 100,
  "steps": 120
}
```

说明：Replay 中的“时间”只服务于：
- TimeWindowGate
- 冷却/节流逻辑
-（后续 P0-2-B 才会扩展到更复杂的确定性约束）

不代表真实时间。

---

## 输入来源二：感知输入（Perception）

### Vision（必需）
- 使用已记录的 vision snapshot
- snapshot 为结构化结果，不是原始图像

```json
"vision_frames": [
  {
    "step": 0,
    "vision_state": "STRAIGHT",
    "objects": [],
    "confidence": {}
  }
]
```

注意：vision_state 允许使用 TURNING / STRAIGHT 等“行为态”，不要求是统一系统态。

### Map（可选但推荐）
- 固定 MapAdapter 输出
- 不做任何在线请求

```json
"map_snapshots": [
  {
    "step": 0,
    "route_state": "ON_ROUTE",
    "distance_to_turn": 12.3
  }
]
```

---

## 输入来源三：意图 / 控制输入（Intent & Control）

- 必须显式记录 start / cancel / confirm / noop
- 必须显式记录 cancel_confirm 的确认步骤

```json
"intents": [
  { "step": 10, "intent": "cancel_task" },
  { "step": 12, "intent": "confirm_cancel" }
]
```

重要：Replay 必须尊重“确认式取消”的两步语义（cancel → confirm）。

---

## 统一结构（SSOT）

Replay Runner 只认这一结构：

```json
{
  "replay_id": "case_nav_turn_001",
  "seed": 42,
  "time": { "t0": 0, "delta_ms": 100, "steps": 120 },
  "initial_state": { "has_active_task": false },
  "vision_frames": [],
  "map_snapshots": [],
  "intents": []
}
```

---

## Replay 模式下屏蔽的实时依赖点（记录）

Replay 路径禁止：
- 设备输入：摄像头/传感器/麦克风
- 在线依赖：地图在线请求
- wall clock：time.time / time.sleep / time.monotonic

当前实现：Replay runner 在进程内对 time.time/time.sleep/monotonic 做逻辑时钟 patch（仅影响回放进程，不修改业务逻辑）。
