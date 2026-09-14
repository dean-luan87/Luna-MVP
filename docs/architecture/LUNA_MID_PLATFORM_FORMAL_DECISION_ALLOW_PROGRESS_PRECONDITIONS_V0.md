# Luna — Formal Decision Allow-Progress Preconditions v0（首次放行前提：设计冻结）

**文件**：`docs/architecture/LUNA_MID_PLATFORM_FORMAL_DECISION_ALLOW_PROGRESS_PRECONDITIONS_V0.md`  
**性质**：Phase-Next-7：首次允许 `allow_progress` 的最小放行前提定义（只冻结前提，不做实现）  

关联：
- 正式裁决层设计冻结：`docs/architecture/LUNA_MID_PLATFORM_FORMAL_DECISION_LAYER_V0.md`
- formal decision stub v2（结构化 pending/block reasons）：`docs/architecture/LUNA_MID_PLATFORM_FORMAL_DECISION_STUB_V2.md`
- 门控输入（安全/任务有效性）v0：`docs/architecture/LUNA_MID_PLATFORM_FORMAL_DECISION_GATE_INPUTS_V0.md`
- 承接链完整性门控 v0：`docs/architecture/LUNA_MID_PLATFORM_FORMAL_DECISION_HANDOFF_GATES_V0.md`
- 信息充分性门控 v0：`docs/architecture/LUNA_MID_PLATFORM_FORMAL_DECISION_INFORMATION_GATES_V0.md`

---

## A. 文档定位（写死）

- 这是 formal decision **首次允许输出 `allow_progress`** 的前提定义文档。
- 当前目标：冻结“最小放行前提”（可回归、可后续最小接线）。
- 当前不做放行实现。
- 当前不改变 formal decision stub v2 行为。
- 当前不进入真实导航执行。

---

## B. 为什么现在要先定义放行前提

- 目前系统已经具备结构化阻断/等待原因（stub v2），能回答“为什么被拦住、为什么在等待”。
- 但仍缺少“什么时候才允许推进”的正式定义。
- 如果不先定义前提，后续直接放行会越权且不可控（无法解释放行依据、无法回归验证）。
- 因此必须先定义 `allow_progress` 的最小前提，再谈极窄范围首次放行。

---

## C. `allow_progress` 的最小语义（写死）

`allow_progress` 表示：
- 正式裁决层认为：**当前已满足进入下一阶段正式链路的最低前提**。
- 它 **不等于** 真实执行已经发生。
- 它只是“允许继续往下一个正式链路推进”的裁决结果。

并写死：
- `allow_progress` 不是导航启动令
- `allow_progress` 不是语音播报令
- `allow_progress` 不是记忆写入令

---

## D. 最小放行前提集合（只定义类别与最低条件，不做算法）

> 口径：任何关键前提缺失 → 不允许输出 `allow_progress`。

### D1. 安全前提（最低）

- `safety_gate_present == true`
- `safety_status != "blocked"`
- 当前不存在更高优先级安全抢占（若该信号存在）

### D2. 任务有效性前提（最低）

- `task_validity_present == true`
- `task_validity_status == "active"`

### D3. 承接链完整性前提（最低）

- `handoff_gate_present == true`
- `handoff_gate_status == "ready_candidate"`

### D4. 信息充分性前提（最低）

- `info_gate_present == true`
- `info_sufficiency_status == "ready_candidate"`

### D5. 分支一致性前提（最低，占位语义）

- 当前 formal decision 所在链路与建议进入的链路 **不冲突**
- 不存在明显分支不一致状态

写死：
- 当前只定义前提类别与最低条件
- 不做算法实现
- 不做复杂冲突求解

---

## E. 明确写清哪些情况仍然不能放行（写死）

只要命中任一条，就不能输出 `allow_progress`（只能 `hold_pending` 或 `block_execution`）：

- 安全状态缺失或被阻断
- 任务已挂起 / 过期 / 被覆盖
- 承接链不完整
- 信息仍不足
- 当前只是建议层结果存在
- 当前只是 stub 结果存在
- 当前链路分支不一致

---

## F. 与现有 formal decision v2 的关系（写死）

- 当前 v2 仍只支持：
  - `block_execution`
  - `hold_pending`
- 本文档只是定义未来 `allow_progress` 的最小前提。
- 下一步才考虑 formal decision stub/vNext 如何在极窄条件下第一次输出 `allow_progress`。

---

## G. 当前不做（写死）

- 不做 `allow_progress` 代码实现
- 不做真实导航执行
- 不做 `switch_branch`
- 不做地图接入
- 不做语音联动
- 不做记忆联动
- 不做自动补全缺失前提

---

## H. 下一步边界（写死）

- 本轮之后，下一步才考虑：
  - formal decision stub vNext 是否支持极窄范围 `allow_progress`
- 再之后才考虑：
  - 把 allow-progress 结果接到真实导航执行前链路
- 当前不跨这两步

---

## I. 未来最小输出样例（仅说明，不实现）

```json
{
  "decision_attempted": true,
  "decision_scope": "mid_platform_formal_decision_stub_vNext",
  "decision_result": "allow_progress",
  "reason": "all_minimum_preconditions_satisfied"
}
```

