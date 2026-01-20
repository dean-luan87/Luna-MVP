# C-Lang：C 模块内部语言与执行边界
## 冻结版 · v1.0

---

## 0. 文件地位

C-Lang 定义了 **C 模块内部允许存在的语言、状态与执行权边界**。

- C 是系统的 **实时执行与导航核心**
- C **不理解世界**，只理解：
  - 当前行为
  - 即时感知
  - DTL 提供的行为影响建议
- C **不需要理解 B 的内部逻辑或感知细节**

---

## 1. C 的核心定位（再次确认）

> **C 负责"当下怎么动"，  
不负责"世界是什么样"。**

C 的目标只有三个（按优先级）：

1. 实时安全（避障、停走、危险规避）
2. 当前任务执行（导航 / 到达 / 探索）
3. 近场环境理解（≤3m）

---

## 2. C 内部允许存在的语言（Internal-Only）

以下语言 **仅存在于 C 内部**，  
禁止直接跨模块输出。

---

### 2.1 行为语言（Action Language）

```text
MOVE_FORWARD
TURN_LEFT
TURN_RIGHT
STOP
WAIT
SLOW_DOWN
EXPLORE
```

**说明：**
- C 的所有执行动作必须来自此集合
- B 不得指定具体动作
- B 只能提供影响建议

---

### 2.2 运动状态语言（Motion State）

```text
speed
heading
stability
acceleration
```

**说明：**
- 用于评估是否可执行动作
- 例如：稳定性不足时拒绝某些建议

---

### 2.3 近场感知语言（Near-Field Perception）

```text
- obstacle_distance
- step_detected
- surface_condition
- door_open_state
- indoor_layout_hint
```

**说明：**
- 感知范围 ≤ 3m
- 室内场景由 C 主导
- 可写入环境记忆（室内）

---

## 3. C 的任务与状态语言（Task Context）

### 3.1 当前任务类型

```text
NAVIGATION
IDLE
EXPLORATION
STOPPED
```

**说明：**
- 决定是否需要 B 的支持
- NAVIGATION 时才请求 B 的前视评估

---

### 3.2 当前行为上下文（Context）

```python
{
  "current_action": "MOVE_FORWARD",
  "speed": 0.6,
  "heading": 90,
  "stability": 0.8,
  "task_type": "NAVIGATION"
}
```

---

## 4. C 与 DTL 的交互语言（唯一合法接口）

### 4.1 C → DTL 的请求结构

```python
{
  "t_horizon": 6.0,
  "current_action": "MOVE_FORWARD",
  "motion_state": {
    "speed": 0.6,
    "heading": 90,
    "stability": 0.8
  },
  "scene_gate": {
    "is_indoor": false,
    "distance_limit_m": 3.0
  }
}
```

**规则：**
- `t_horizon` 由 C 决定
- `scene_gate` 用于裁剪 B 的发言资格

---

### 4.2 C 可理解的 DTL 输入

C 只理解以下内容：

- **DTL.ActionImpact**

或

- **NO_OP**

C 不理解：
- B 的感知信号
- 世界描述
- 原因的原始细节（仅用于日志）

---

## 5. C 的执行与决策规则（冻结）

### 5.1 行为裁决原则

当收到 DTL.ActionImpact 时：
1. 校验是否在当前 t_horizon 内
2. 校验 effective_zone 是否合法
3. 结合自身稳定性 / 任务状态判断是否采纳
4. 决定执行或忽略

---

### 5.2 C 的自主权（非常重要）

- **C 可以拒绝 B 的建议**
- **拒绝并不代表 B 错误**
- **未来事件是预演，不是必然发生**

---

## 6. C → B 的回执语言

### 6.1 回执结构（通过 DTL）

```python
{
  "advice_id": "uuid",
  "accepted": true,
  "executed": false,
  "outcome": "SAFE_PASS",
  "latency_sec": 1.1
}
```

**说明：**
- `accepted` = 是否采纳为参考
- `executed` = 是否真的执行
- `outcome` = 实际结果

---

## 7. C 的职责边界（冻结）

### C 负责

- 实时导航与执行
- 近场安全判断
- 室内环境记忆
- 行为决策

### C 不负责

- 远距世界建模
- 抽象环境理解
- 未来场景推演
- 长期知识维护

---

## 8. 与 DTL / B 的关系（强约束）

- **C 不直接理解 B**
- **C 只消费 DTL**
- **C 的任何反馈必须走 DTL**

**任何绕过 DTL 的交互：**
- 视为架构违规

---

## 9. 冻结原则

- 本文件为 C-Lang v1.0 冻结版
- 修改必须：
  - 同步升级版本号
  - 审查 DTL 兼容性
  - 禁止私下扩展跨模块语言

---
