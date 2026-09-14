# Luna — Mid-Platform Formal Decision Stub v2（Structured Pending/Block Reasons）

**文件**：`docs/architecture/LUNA_MID_PLATFORM_FORMAL_DECISION_STUB_V2.md`  
**性质**：Phase-Next-6：formal decision stub 的“结构化原因”升级（只细化 reason，不放行执行）  

关联：
- 正式裁决层设计冻结：`docs/architecture/LUNA_MID_PLATFORM_FORMAL_DECISION_LAYER_V0.md`
- stub v1（最保守条件化输出）：`docs/architecture/LUNA_MID_PLATFORM_FORMAL_DECISION_STUB_V1.md`
- 门控输入（安全/任务有效性）v0：`docs/architecture/LUNA_MID_PLATFORM_FORMAL_DECISION_GATE_INPUTS_V0.md`
- 承接链完整性门控 v0：`docs/architecture/LUNA_MID_PLATFORM_FORMAL_DECISION_HANDOFF_GATES_V0.md`
- 信息充分性门控 v0：`docs/architecture/LUNA_MID_PLATFORM_FORMAL_DECISION_INFORMATION_GATES_V0.md`
- allow-progress 放行前提 v0（设计冻结）：`docs/architecture/LUNA_MID_PLATFORM_FORMAL_DECISION_ALLOW_PROGRESS_PRECONDITIONS_V0.md`
- stub vNext（窄路径 allow-progress）：`docs/architecture/LUNA_MID_PLATFORM_FORMAL_DECISION_STUB_VNEXT_NARROW_ALLOW_PROGRESS_V0.md`

---

## A. 文档定位（写死）

- 这是 formal decision stub 的“结构化原因”升级文档。
- 当前目标不是新增新能力，而是让 `hold_pending` / `block_execution` 的原因 **可区分、可追踪、可回归**。
- 当前不做真实裁决器。
- 当前不做真实执行放行。

---

## B. 为什么现在要先做“结构化原因”

- 现在 formal decision 已经有多类门控输入位（安全/任务有效性/承接链/信息充分性）。
- 若 stub 的 reason 仍然过于笼统，下游与后续阶段将无法判断系统究竟卡在哪一类缺口上。
- 因此必须先把“阻断原因 / 等待原因”结构化。
- 这一步 **先于** allow_progress（当前仍禁止 allow_progress）。

---

## C. 本轮允许的结果集合（写死）

- `block_execution`
- `hold_pending`

---

## D. 本轮建议的结构化原因集合（收敛，写死）

> 口径：reason 是分类标签（枚举），不输出多原因聚合。

### block 类

- `safety_gate_blocked`
- `task_validity_blocked`

### pending 类

- `missing_handoff_gate_inputs`
- `insufficient_information`
- `missing_required_gate_inputs`

---

## E. 原因判定最小规则（写死）

1. **安全门控阻断**  
   - `formal_decision_gate_inputs_v0.safety_gate_v0_present == true`
   - 且 `formal_decision_gate_inputs_v0.safety_status == "blocked"`
   - → `block_execution / safety_gate_blocked`

2. **任务有效性阻断**  
   - `formal_decision_gate_inputs_v0.task_validity_v0_present == true`
   - 且 `formal_decision_gate_inputs_v0.task_validity_status ∈ {"expired","overridden"}`
   - → `block_execution / task_validity_blocked`

3. **承接链不完整**  
   - `formal_decision_handoff_gates_v0.handoff_gate_present == true`
   - 且 `formal_decision_handoff_gates_v0.handoff_gate_status == "incomplete"`
   - → `hold_pending / missing_handoff_gate_inputs`

4. **信息不足**  
   - `formal_decision_information_gates_v0.info_gate_present == true`
   - 且 `formal_decision_information_gates_v0.info_sufficiency_status == "insufficient"`
   - → `hold_pending / insufficient_information`

5. **其他缺失**  
   - 其余缺少正式门控输入或不足以判断的情况
   - → `hold_pending / missing_required_gate_inputs`

---

## F. 必须写清优先级（写死）

当多个原因同时出现时，按如下最小优先级只取一个（不做聚合）：

1. `safety_gate_blocked`
2. `task_validity_blocked`
3. `missing_handoff_gate_inputs`
4. `insufficient_information`
5. `missing_required_gate_inputs`

---

## G. 当前不允许做什么（写死）

- 不允许输出 `allow_progress`
- 不允许输出 `switch_branch`
- 不允许因为 handoff/info 看起来齐了就放行
- 不允许触发真实导航
- 不允许驱动语音/记忆

