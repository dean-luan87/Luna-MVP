# Luna — Navigation Governance Action Release Control First Live Guarded Implementation Minimal Real-Effect Guarded Launch Dry-Run v0（最终发车演练层：设计冻结）

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_GUARDED_LAUNCH_DRY_RUN_V0.md`  
**性质**：Phase-Next-101：冻结 `minimal real-effect` 在 `admission == admitted` 之后、真实最小写入实现之前的 **guarded launch dry-run**（只演练、不放权；可冻结、可回归）

基于（已具备）：
- admission gate v0（最小实现已落地）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_ADMISSION_GATE_V0.md`
- admission gate minimal implementation v0（实现说明）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_ADMISSION_GATE_IMPLEMENTATION_V0.md`
- implementation definition / skeleton / implementation dry-run execution（已具备）
- gates / simulation / wiring（已具备）
- standard objects：`execution_state_v0` / `result_v0`

---

## 1. 文档定位（写死）

这份文档是：

- 第一版 `minimal real-effect implementation` 在 admission 通过之后、真实写入之前的**最终发车演练层（guarded launch dry-run）**设计冻结文档。

当前不做：

- 真实写入
- `rollback` / `interrupt`
- 地图接入
- 语音/记忆联动
- 中台真实迁移

且不改变现有主线行为，并保持 `side_effects_released == false`。

---

## 2. 为什么现在必须先定义 guarded launch dry-run（写死理由）

- admission gate implementation 已存在（可结构化产出 `admitted/not_admitted/blocked`）。
- implementation dry-run execution 已存在（可在零副作用模式下跑通未来实现顺序）。
- 若缺少 guarded launch dry-run，后续路径将从 `admitted` 直接跳到“真实写入”，缺少最后一次发车前演练检查层。

因此必须先冻结并尽量实现发车前最后一次演练检查层，继续保持零真实副作用。

---

## 3. 最小定义（写死）

`minimal real-effect guarded launch dry-run` 是：

- admission 通过之后、真实第一版最小写入实现之前的最终发车演练层
- 只负责检查是否具备最后发车条件，并产出统一结果对象

它不是：

- admission gate 本身
- implementation definition 本身
- 真实写入器本身
- `rollback` / `interrupt` 实现

---

## 4. 最小合法输入（写死；只允许标准化对象）

只允许消费（只读）：

- `navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_admission_gate_v0`
  - 必须 `admission_status == "first_live_minimal_real_effect_admitted"`
- `first_live_enablement_approval_gate_v0`
  - 必须 approved
- `first_live_launch_dry_run_v0`
  - 必须 ready
- `live_release_gate_v0`
  - 必须 ready
- `side_effect_release_gate_v0`
  - 必须 ready
- `first_live_guarded_implementation_dry_effect_simulation_v0`
  - 必须 simulated
- `first_live_guarded_implementation_minimal_real_effect_implementation_dry_run_execution_v0`
  - 必须 executed
- implementation skeleton identity / capability
  - 必须在位且仍为 conservative / dry-run mode
- `execution_state_v0`、`result_v0`
  - 在位
- `side_effects_released`
  - 必须仍为 false

并写死：

- 缺任一主前提，launch dry-run 不成立。
- 禁止直接读取 `request_* / approved_* / raw metadata`。

---

## 5. 最小结果集合（写死；三态）

至少包括：

- `first_live_minimal_real_effect_launch_ready`
- `first_live_minimal_real_effect_launch_not_ready`
- `first_live_minimal_real_effect_launch_blocked`

并写死语义：

- `launch_ready` 只表示 admission 通过后，系统具备最后发车前条件
- 不表示真实写入已经开始
- 不表示副作用已经发生
- 不表示 `side_effects_released == true`

---

## 6. 明确禁止（写死）

guarded launch dry-run 不允许直接：

- 打开 `side_effects_released`
- 执行真实 `release_control`
- 执行真实写入
- 改路线
- 触发语音播报
- 写记忆
- 触发中台真实迁移
- 自动触发 `rollback` / `interrupt`
- 越过标准对象吐散字段

---

## 7. 与现有链路的关系（写清；不能混用）

- 与 admission gate：
  - admission gate 决定“是否准入第一版最小真实写入实现”
  - launch dry-run 决定“准入后，是否具备最后发车条件”
  - `admitted != launch_ready`
- 与 implementation dry-run execution：
  - implementation dry-run 验证未来实现顺序
  - launch dry-run 做发车前最后一次总检查
  - 两者不能混用
- 与 implementation definition / plan：
  - definition 定边界
  - plan 定真实写入策略
  - launch dry-run 只做进入真实写入前的最后检查

---

## 8. 当前仍然不能做什么（写死）

- 不允许把 `side_effects_released` 打开
- 不允许真实写入
- 不允许真实 `release_control`
- 不允许真实 `rollback` / `interrupt`
- 不允许 route / voice / memory / migration
- 不允许把 `launch_ready` 当作真实写入已开始

---

## 9. 当前不做（写死）

- 不做真实 minimal real-effect implementation
- 不做地图接入
- 不做语音/记忆联动
- 不做中台真实迁移

---

## 10. 下一步边界（写死）

- 本轮之后，下一步才考虑：
  - minimal real-effect guarded launch dry-run 的 minimal implementation
- 再之后才考虑：
  - 第一版最小真实写入实现方案
- 当前不直接落真实实现

补充链接（最终放行门：设计冻结）：

- Phase-Next-102：Minimal Real-Effect Guarded Launch Gate v0：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_GUARDED_LAUNCH_GATE_V0.md`

