# Luna — Navigation Real Execution Readiness Gate Stub v0（最后门控统一出口：只读占位）

**文件**：`docs/architecture/LUNA_NAVIGATION_REAL_EXECUTION_READINESS_GATE_STUB_V0.md`  
**性质**：Phase-Next-12：真实执行前最后门控层的只读 stub（统一输出位；不接执行器）  

关联：
- 最后门控类别冻结：`docs/architecture/LUNA_NAVIGATION_REAL_EXECUTION_READINESS_GATE_V0.md`
- 最后门控输入面（只读承接）：`docs/architecture/LUNA_NAVIGATION_REAL_EXECUTION_READINESS_GATE_INPUTS_V0.md`
- 下游占位消费契约：`docs/architecture/LUNA_NAVIGATION_HANDOFF_POST_BOUND_EXECUTION_STUB_CONSUMPTION_PLAN_V0.md`
- formal decision 窄路径 allow-progress：`docs/architecture/LUNA_MID_PLATFORM_FORMAL_DECISION_STUB_VNEXT_NARROW_ALLOW_PROGRESS_V0.md`
- 执行器接管层方案（冻结）：`docs/architecture/LUNA_NAVIGATION_EXECUTOR_TAKEOVER_PLAN_V0.md`
- 执行器接管层统一只读出口（stub v0）：`docs/architecture/LUNA_NAVIGATION_EXECUTOR_TAKEOVER_STUB_V0.md`
- 真实执行器输入层（输入边界冻结）：`docs/architecture/LUNA_NAVIGATION_REAL_EXECUTOR_INPUT_LAYER_V0.md`
- 输入对象只读占位输出（placeholder v0）：`docs/architecture/LUNA_NAVIGATION_REAL_EXECUTOR_INPUT_OBJECT_PLACEHOLDER_V0.md`

---

## A. 文档定位（写死）

- 这是“真实执行前最后门控层”的**只读 stub** 设计。
- 当前目标：给最后门控层一个**统一输出位**。
- 当前不接真实导航执行器。
- 当前不接地图。
- 当前不驱动语音/记忆。
- 当前不改变现有执行行为。

---

## B. 为什么现在要做 readiness gate stub

- 最后门控类别已经定义（v0）。
- 最后门控输入位已经定义并可只读承接（inputs v0）。
- 但还没有统一输出结果。
- 若没有统一结果，后续接真实执行器时仍会直接读散乱输入、越层取数、难回归。
- 因此需要先把 5 类最后门控输入收束为统一 readiness 结果。

---

## C. readiness gate stub 的最小定义（写死）

- 它不是执行器
- 不是地图规划器
- 不是语音启动器
- 只是“真实执行前最后门控层”的统一只读判断出口
- 作用：读取 5 类门控输入，保守输出 readiness 状态

---

## D. 当前最小输入（写死）

- 只读取：`result.metadata["navigation_real_execution_readiness_gate_inputs_v0"]`
- 不直接去读更下层零散 gate 对象
- 不新增别的复杂输入源

---

## E. 当前最小输出位（写死）

固定写入：
- `result.metadata["navigation_real_execution_readiness_gate_stub_v0"]`

最小结构（建议）：

```json
{
  "readiness_attempted": true,
  "readiness_scope": "navigation_real_execution_readiness_gate_stub_v0",
  "readiness_status": "not_ready|ready_candidate|blocked",
  "reason": "..."
}
```

约束（写死）：
- 不加时间/空间字段
- 不膨胀成复杂对象
- 只做 readiness 统一结果输出

---

## F. 当前最小 readiness 结果集合（只允许 3 类，写死）

1) **blocked**
- 存在明确阻断条件
- 当前不应继续推进到真实执行器

2) **not_ready**
- 没有明确阻断，但最后门控输入不完整或仍不足
- 当前只能停留在占位层

3) **ready_candidate**
- 5 类最后门控输入满足最小“候选就绪”
- 仅表示“未来可考虑交给真实执行器前的下一层”
- 不等于真实执行器可以立即接管

---

## G. 最小判断规则（非常克制，写死）

规则 1：任一 gate 明确 blocked / unavailable 且属于硬阻断 → `blocked`

最小示例：
- `executor_status ∈ {"blocked","unavailable"}`
- 或任一 gate 的状态字段为 `"unavailable"`（按本期最小语义视作硬阻断）

规则 2：5 类 gate 全部 present，且状态达到最小 ready_candidate 条件 → `ready_candidate`

最小条件示例：
- `executor_gate_present == true` 且 `executor_status == "available"` 且 `executor_takeover_allowed == true`
- `path_support_gate_present == true` 且 `path_support_status != "unavailable"`
- `execution_monitor_gate_present == true` 且 `execution_monitor_status == "ready_candidate"`
- `start_policy_gate_present == true` 且 `start_policy_status == "ready_candidate"`
- `fallback_gate_present == true` 且 `fallback_status == "ready_candidate"`

规则 3：其他情况 → `not_ready`

---

## H. 当前不允许做什么（写死）

- 不允许直接接真实导航执行器
- 不允许把 `ready_candidate` 当执行完成或执行许可
- 不允许驱动语音播报“开始导航”
- 不允许触发地图规划
- 不允许切执行链
- 不允许跳过后续真实执行前接管层

---

## I. 与现有链路的关系（写死）

### 与 formal decision

- formal decision 只负责极窄放行到下游占位层
- readiness gate stub 不替代 formal decision

### 与 post-bound execution stub consumption

- readiness gate stub 位于“下游 stub 消费 allow-progress”之后、“真实执行器”之前
- 它只收束 readiness 输入为统一结果，不推进执行

### 与真实执行器

- 真实执行器未来应只读取统一 readiness 结果或其下游正式接管层
- 当前不接入执行器本体

