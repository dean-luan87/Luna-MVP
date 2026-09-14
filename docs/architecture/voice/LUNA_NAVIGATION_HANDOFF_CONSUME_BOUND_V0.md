# Navigation Handoff Consume Bound v0（handoff 消费 destination_bound_v0 专题）

**文件**：`docs/architecture/voice/LUNA_NAVIGATION_HANDOFF_CONSUME_BOUND_V0.md`  
**性质**：navigation_handoff 消费 bound fact 的最小设计与接线（可冻结、可回归）  

上位约束（必须服从）：
- `docs/architecture/LUNA_WORLD_ENTRY_PRINCIPLE_V0.md`
- `docs/architecture/voice/LUNA_VOICE_MAINLINE_BASELINE.md`
- `docs/architecture/voice/LUNA_CONFLICT_GOVERNANCE_CONSTITUTION_V0.md`
- `docs/architecture/voice/LUNA_NAVIGATION_DESTINATION_BOUND_MATERIALIZATION_IMPL_V0.md`

并写死（继续成立）：
- **No Fabrication Rule**：只能消费已有 `destination_bound_v0`，不得补 id，不得用 candidate/语义/记忆/视觉替代。
- **统一时空锚点原则**：本专题不引入任何模块自造的时间/空间字段。

---

## A. 文档定位

- 这是 **navigation_handoff 消费 `destination_bound_v0`** 的最小设计。
- 当前目标是：让 handoff **正式承认 bound fact** 已存在，并产出结构化 consume 结果。
- 当前不实现：
  - 完整真实导航执行
  - 地图接入
  - 视觉导航增强/解释
  - 复杂任务链与多轮导航对话扩展

---

## B. 当前问题定义

- 现在 `destination_bound_v0` 已经进入主链正式事实层（metadata 写入）。
- 但 `navigation_handoff_v0` 仍主要停留在“松散 proposal.metadata 文本 + placeholder”的阶段。
- 当前断点是：**目标已确认（bound fact 已存在），但执行承接仍未切换到 bound fact 的消费**。

---

## C. consume bound 的最小定义（写死）

handoff consume bound **不等于**真实导航启动。

它只表示：
- handoff 已正式读取 `destination_bound_v0`
- handoff 承认当前导航目标事实已存在（可复核的 binding_key/binding_value）
- 后续执行链（未来）可以基于该事实继续推进

---

## D. consume 的最小输入（写死）

只允许消费：
- `proposal.task_action == "start_navigation"`
- `result.metadata["destination_bound_v0"]`

明确不消费（写死）：
- 不消费 candidate
- 不消费 confirmation fact
- 不消费 bound_upgrade_eval / materialization_eval
- 不消费 visual / memory / semantic 猜测

---

## E. consume 后的最小输出（写死）

建议写入：
- `result.metadata["navigation_handoff_consume_bound_v0"]`

最小结构示例：

```json
{
  "bound_consumed": true,
  "consume_scope": "navigation_handoff_consume_bound_v0",
  "binding_key": "destination_id",
  "binding_value": "dest_123",
  "executor": "voice_navigation_handoff_v0"
}
```

并写死：
- 这不代表导航已经开始
- 只代表 handoff 已接住正式目标事实

---

## F. 当前明确禁止项（写死）

- 不允许 handoff 继续消费裸 candidate 替代 bound
- 不允许 consume bound 后顺手启动真实导航
- 不允许在本轮接地图或 navigation_manager 真执行
- 不允许从视觉/记忆/语义补 binding_value

---

## G. 推荐的最小实现落点（只选一个）

**唯一推荐落点**：在 `voice_navigation_handoff_v0.py` 增加一个只读的 consume-bound 分支函数：
- 输入：`decision` + `destination_bound_v0`
- 输出：`navigation_handoff_consume_bound_v0` dict（只读观测）

主线接线位置（最小）：
- 在 `voice_final_text_dispatcher.py` 内，`destination_bound_v0` 已写入后，调用该 consume 函数，把结果写入 `result.metadata["navigation_handoff_consume_bound_v0"]`。

为什么选这里：
- 最连续：紧贴 bound fact 的写入点。
- 最不易失控：consume 是观测层承认，不触发执行。
- 最小改动：不改 proposal、不给 handoff 引入更多输入面。

---

## H. 下一步边界（写死）

- 本轮之后，下一步才考虑“consume bound 后如何连接真实导航执行”
- 再之后才回头补齐视角链与视觉接线
- 本轮不跨这两步

