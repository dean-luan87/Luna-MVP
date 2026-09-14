# Luna — Mid-Platform Formal Decision Stub v1（最保守条件化输出）

**文件**：`docs/architecture/LUNA_MID_PLATFORM_FORMAL_DECISION_STUB_V1.md`  
**性质**：Phase-Next-3：formal decision stub 最小升级（只允许 block / pending）  

关联：
- 正式裁决层设计冻结：`docs/architecture/LUNA_MID_PLATFORM_FORMAL_DECISION_LAYER_V0.md`
- stub v0：`docs/architecture/LUNA_MID_PLATFORM_FORMAL_DECISION_STUB_V0.md`
- 门控输入 v0：`docs/architecture/LUNA_MID_PLATFORM_FORMAL_DECISION_GATE_INPUTS_V0.md`
- stub v2（结构化原因）：`docs/architecture/LUNA_MID_PLATFORM_FORMAL_DECISION_STUB_V2.md`

---

## A. 文档定位（写死）

- 这是 formal decision stub 的最小升级文档。
- 当前目标：从固定 `hold_pending` 升级到最保守的条件化输出。
- 当前不做完整正式裁决器，也不放行真实执行。

---

## B. 为什么现在只允许最保守升级

- 当前已经有两类门控输入位：
  - 安全门控
  - 任务有效性门控
- 它们天然适合支持“**阻断**”判断。
- 但当前仍缺：
  - 更完整的信息充分性门控
  - 更完整的承接链完整性门控（可执行放行所需）
  - 更完整的正式裁决上下文
- 因此本轮只允许输出：
  - `block_execution`
  - `hold_pending`

---

## C. 本轮最小升级规则（写死）

> 仅基于已占位好的两类门控输入，且缺失时不得脑补。

### 规则 1：安全阻断

- 若 `safety_gate_present == true`
- 且 `safety_status == "blocked"`

→ `decision_result = "block_execution"`  
→ `reason = "safety_gate_blocked"`

### 规则 2：任务无效阻断

- 若 `task_validity_present == true`
- 且 `task_validity_status ∈ {"expired", "overridden"}`

→ `decision_result = "block_execution"`  
→ `reason = "task_validity_blocked"`

### 规则 3：其余情况

→ `decision_result = "hold_pending"`  
→ `reason = "missing_required_gate_inputs"`（或同等保守原因）

---

## D. 明确不支持的输出（写死）

- 当前不输出 `allow_progress`
- 当前不输出 `switch_branch`

---

## E. 当前不允许做什么（写死）

- 不允许真实切导航链
- 不允许真实启动导航
- 不允许直接驱动语音/记忆
- 不允许伪造缺失门控输入
- 不允许把 `guarded/safe` 自动理解为可放行

后续门控输入（承接链完整性，占位）：
- `docs/architecture/LUNA_MID_PLATFORM_FORMAL_DECISION_HANDOFF_GATES_V0.md`

后续门控输入（信息充分性，占位）：
- `docs/architecture/LUNA_MID_PLATFORM_FORMAL_DECISION_INFORMATION_GATES_V0.md`

