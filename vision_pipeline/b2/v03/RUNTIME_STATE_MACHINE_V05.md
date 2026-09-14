# B2 Runtime State Machine v0.5

## 设计边界

- 本状态机 **不关心识别"对不对"**
- 只关心 **"现在是否适合做判断"**
- 不引入 OCR
- 不引入多镜头融合
- 不引入 C 的策略决策

B2 v0.5 的职责止于：

**"此刻，我是否有条件告诉 C：如果你不作为，可能会发生什么。"**

---

## 状态总览

```
┌─────────┐
│  INIT   │
└────┬────┘
     ↓
┌────────────┐
│ WARMING_UP │  ← 时间窗/统计量未稳定
└────┬───────┘
     ↓
┌────────────┐
│  SUSPENDED │  ← 姿态/环境不满足
└────┬───────┘
     ↓
┌────────────┐
│   ACTIVE   │  ← 唯一允许触发判断的状态
└────┬───────┘
     ↓
┌────────────┐
│ READ_ONLY  │  ← 被动观测，不产出
└────┬───────┘
     ↓
┌─────────┐
│  ERROR  │
└─────────┘
```

---

## 各状态精确定义

### INIT（启动态）

**进入条件**
- 系统启动
- 视频流 / 相机刚接入

**行为**
- 不做任何判断
- 不产生 factors
- 不写 timeline
- 允许写 trace

**退出条件**
- 成功接收连续帧
- FPS、时间戳稳定

**Trace 原因**: `system_start`

---

### WARMING_UP（预热态）

**目的**: 防止"刚启动就判断"

**硬性条件**
- 累计帧数 ≥ N_frames_min（如 90 帧 ≈ 3s）
- 滑动时间窗完整（如 5–7s）

**行为**
- 可计算 perception
- 禁止进入规则判断
- 禁止产生 impact

**Trace 原因**: `insufficient_frames` / `window_not_ready`

---

### SUSPENDED（挂起态）

**进入任一即挂起**
- IMU 抖动超阈值
- 镜头剧烈晃动
- 距离异常（过近 / 过远）
- 场景不可判（强逆光、遮挡）
- 系统负载异常

**行为**
- perception 可以跑（用于恢复判断）
- 禁止 trigger
- 禁止 impact
- 不写 timeline

**Trace 原因**: 
- `imu_unstable`
- `camera_shake`
- `distance_invalid`
- `scene_invalid`
- `system_load_high`

---

### ACTIVE（唯一允许判断的状态）

**只有这个状态，B 才"被允许开口"**

**进入前必须全部满足**
- 来自 WARMING_UP 或 SUSPENDED
- 连续稳定时间 ≥ T_stable（如 1.5s）
- IMU variance < 阈值
- 镜头位姿稳定
- 距离区间合理

**行为**
- 允许 trigger gate
- 允许 rule evaluation
- 允许 impact calculation
- 允许向 C 发送 message
- 允许写 timeline

**Trace 原因**: `stable_camera_and_pose`

---

### READ_ONLY（只读态）

**用途**
- 复杂场景下的"保守模式"
- 被 C 或上层显式要求降级

**行为**
- perception 运行
- rule 可以算（用于 debug / trace）
- impact 一律 NO_OP
- 不向 C 发消息

**Trace 原因**: `explicit_readonly`

---

### ERROR（异常态）

**进入条件**
- 相机中断
- 时间戳异常
- 内部异常

**行为**
- 停止一切判断
- 写 error trace
- 等待外部恢复

**Trace 原因**: `system_error`

---

## 状态转移规则

| From | To | 条件 |
|------|-----|------|
| INIT | WARMING_UP | 帧流稳定 |
| WARMING_UP | ACTIVE | 窗口完成 + 稳定 |
| WARMING_UP | SUSPENDED | 姿态异常 |
| SUSPENDED | ACTIVE | 连续稳定 ≥ T |
| ACTIVE | SUSPENDED | 任一稳定条件破坏 |
| ACTIVE | READ_ONLY | 上层强制 |
| ANY | ERROR | 系统异常 |

---

## Trace 强制字段（v0.5）

每一帧必须写入：

```json
{
  "runtime_state": {
    "state": "ACTIVE",
    "since": "00:02.3",
    "reason": "stable_camera_and_pose"
  },
  "state_gate": {
    "can_trigger": true,
    "blocked_by": null
  }
}
```

**铁律**：如果 `can_trigger=false`，必须写清楚 `blocked_by`。

---

## 与 B → C 的关系

- 状态机 ≠ 判断
- 状态机先于判断
- C 永远不应该看到：
  - WARMING_UP
  - SUSPENDED
  - READ_ONLY
- C 只接收来自 ACTIVE 的结果

---

## v0.5 明确不做的事

- 不区分室内 / 室外
- 不做多镜头合并
- 不主动控制镜头
- 不基于 OCR 决策

---

## 实现状态

✅ 状态机已实现 (`runtime_state_machine.py`)
✅ 已集成到 `b2_v03.py`
✅ Trace schema 已定义 (`b2_runtime_trace_schema_v0.5.json`)
✅ 每帧都写入 `runtime_state` 和 `state_gate`

---

## 下一步

1. Web Trace Viewer（按 state 着色）
2. 集成真实的视觉检测模块
3. 多镜头 / Viewpoint 调度设计
