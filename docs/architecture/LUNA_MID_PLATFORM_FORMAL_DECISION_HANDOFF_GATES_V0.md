# Luna — Formal Decision Handoff Gates v0（承接链完整性门控：设计/占位）

**文件**：`docs/architecture/LUNA_MID_PLATFORM_FORMAL_DECISION_HANDOFF_GATES_V0.md`  
**性质**：Phase-Next-4：正式裁决层的“承接链完整性门控”最小设计（先占位，不改裁决行为）  

关联：
- 正式裁决层设计冻结：`docs/architecture/LUNA_MID_PLATFORM_FORMAL_DECISION_LAYER_V0.md`
- formal decision stub v1：`docs/architecture/LUNA_MID_PLATFORM_FORMAL_DECISION_STUB_V1.md`
- 导航执行前承接设计：`docs/architecture/LUNA_NAVIGATION_HANDOFF_POST_BOUND_EXECUTION_PLAN_V0.md`
- 导航执行前承接 stub：`docs/architecture/LUNA_NAVIGATION_HANDOFF_POST_BOUND_EXECUTION_STUB_V0.md`
- bound 材料化设计：`docs/architecture/voice/LUNA_NAVIGATION_DESTINATION_BOUND_MATERIALIZATION_IMPL_V0.md`

---

## A. 文档定位（写死）

- 这是正式裁决层“**承接链完整性门控**”的最小设计文档。
- 当前目标：定义导航执行前承接链，如何作为正式裁决层的门控输入。
- 当前不做真实门控实现；当前不改变 formal decision stub v1 的最保守输出边界。

---

## B. 为什么现在必须补“承接链完整性门控”

- 当前 formal decision stub v1 已能处理：
  - 安全阻断
  - 任务无效阻断
- 但仍无法区分：
  - “真的可以往前推进”
  - vs “只是承接链还没准备好”
- 因此必须补一类新的门控输入：**承接链完整性门控**，用于解释“为什么 pending”。

---

## C. 最小门控输入集合（只定义最小集合）

建议 `formal_decision_handoff_gates_v0` 最小字段：
- **handoff_gate_present**：bool
- **bound_present**：bool
- **consume_bound_present**：bool
- **post_bound_stub_present**：bool
- **handoff_gate_status**：`incomplete | ready_candidate | blocked`
- **consume_mode**：固定 `read_only`

注意（写死）：
- 当前不做 `ready_candidate -> allow_progress`
- 这里只定义语义与占位输出

---

## D. 这类门控输入未来来自哪里（来源说明，占位）

这类门控输入未来应由以下已存在骨架整理而来：
- `result.metadata["destination_bound_v0"]`
- `result.metadata["navigation_handoff_consume_bound_v0"]`
- `result.metadata["navigation_handoff_post_bound_execution_stub_v0"]`

写死：
- 这些是当前系统里已经存在的承接链骨架
- 未来应先整理成一个正式门控输入对象
- 再供正式裁决层消费

---

## E. 最小门控原则（写死）

1. `destination_bound_v0` 不存在 → `handoff_gate_status = "incomplete"`
2. `navigation_handoff_consume_bound_v0` 不存在 → `handoff_gate_status = "incomplete"`
3. `navigation_handoff_post_bound_execution_stub_v0` 不存在 → `handoff_gate_status = "incomplete"`
4. 即使三者都存在，当前也只能认为是 `ready_candidate`，不是直接放行执行
5. 若未来发现承接链内部有明确阻断原因，可标记为 `blocked`（本期仅占位，不实现）

---

## F. 与 formal decision stub 的关系（写死）

- 本轮先定义并占位这类门控输入。
- 本轮不要求 formal decision stub v1 立刻消费它。
- 下一步才考虑 formal decision stub v2 如何读取它（用于解释 pending 原因）。
- 即使后续读取，也不等于立即放行。

---

## G. 当前不做（写死）

- 不做真实承接链门控实现
- 不做真实放行
- 不做真实导航执行
- 不做地图接入
- 不做跨链自动切换
- 不做承接链缺失自动补全

---

## H. 下一步边界（写死）

- 本轮之后，下一步才考虑：
  - 把这类门控输入接到 formal decision stub v2
- 再之后才考虑：
  - formal decision 是否允许极窄范围 allow_progress
- 当前不跨这两步

