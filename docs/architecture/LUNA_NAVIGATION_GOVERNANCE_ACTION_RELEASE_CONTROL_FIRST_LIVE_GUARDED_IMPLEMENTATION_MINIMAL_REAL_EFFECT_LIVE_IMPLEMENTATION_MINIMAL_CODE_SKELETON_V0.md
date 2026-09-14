# Luna — Navigation Governance Action Release Control First Live Guarded Implementation Minimal Real-Effect Live Implementation Minimal Code Skeleton v0（真实代码壳子：冻结 + 占位）

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_LIVE_IMPLEMENTATION_MINIMAL_CODE_SKELETON_V0.md`  
**性质**：Phase-Next-124：为第一版真实最小写入实现本体占住“real implementation code shell（最小代码骨架）”的独立承载位（当前完全非动作；不接入 dispatcher；可冻结、可回归）

基于（已具备）：
- real-write go/no-go gate v0（冻结）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_LIVE_IMPLEMENTATION_REAL_WRITE_GO_NO_GO_GATE_V0.md`
- first real write rollout plan v0（冻结）
- live implementation definition / skeleton / stub（冻结 + 在位）
- wiring / dry-run execution / runtime activation stub（在位）
- activation / commit / pre-commit / launch / admission 全链路对象（在位）
- 当前 `side_effects_released` 仍强制锁死为 `false`

---

## 1. 文档定位（写死）

这份文档是：

- 第一版 `live implementation minimal implementation` 的**最小代码骨架（real code shell）**设计冻结文档。
- 当前目标：冻结“从 go/no-go gate 进入未来真实最小写入代码本体”的代码承载边界：代码落点、最小接口、共同约束（全部 placeholder-safe）。

并且（本轮写死边界）：

- 本轮只做 minimal code skeleton（代码壳子占位）。
- 不做真实代码执行。
- 不做真实 rollout 启用。
- 不做真实 `rollback` / `interrupt`。
- 不接地图、不改路线。
- 不驱动语音/记忆。
- 不触发中台真实迁移。
- 不改变现有主线行为。

---

## 2. 为什么现在必须先做 minimal code skeleton（写死理由）

- go/no-go gate 已存在：是否允许开始已冻结。
- rollout plan 已存在：试运行策略已冻结。
- live implementation definition / skeleton / stub 已存在：占位、边界、承载位已建立。
- 但还没有一个专用的“未来真实最小写入代码本体”代码骨架。
- 如果不先做 minimal code skeleton，后续最容易在 stub 或旧 skeleton 上硬改真实逻辑，造成混层（skeleton/stub/body/rollout opening 混在一起），难以回归与熔断。

因此必须先单独占住 real code shell：未来真实最小写入代码只能落在该骨架文件中。

---

## 3. 最小定义（写死）

`release_control first live guarded implementation minimal real-effect live implementation minimal code skeleton` 是：

- future real minimal write code body 的**唯一代码承载骨架**
- 当前只提供接口与固定边界，不执行真实写入

它不是：

- 旧 live implementation skeleton（占位壳子）
- runtime stub（运行时占位）
- dry-run runner（演练器）
- rollout gate / rollout plan（放行与试运行策略）
- 真实实现本身（real write 未发生）

---

## 4. 最小代码落点（写死结论 + 理由）

### 4.1 结论（写死）

最适合的文件路径：

- `capabilities/governance/runtime/navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_code_skeleton_v0.py`

### 4.2 为什么应与 governance/runtime 同域（写死）

- 这是“治理动作本体承载位”家族（与现有 live implementation skeleton/stub 同域），便于保持单一入口与审计边界。

### 4.3 为什么要独立文件（写死）

- 旧 skeleton/stub 必须永远保持“非动作、不可写入、不可激活”的可回归性；真实代码体承载位必须物理隔离，避免未来混写与误接线。

---

## 5. 必须提供的最小接口（写死）

最小接口建议至少包括：

- `get_release_control_first_live_guarded_implementation_minimal_real_effect_live_code_skeleton_identity()`
- `accept_first_live_minimal_real_effect_live_code_input(...)`
- `perform_first_live_execution_state_real_write_placeholder(...)`
- `perform_first_live_result_object_real_write_placeholder(...)`
- `perform_first_live_exception_or_failure_real_write_placeholder(...)`
- `perform_first_live_recover_side_effects_false_placeholder(...)`

---

## 6. 当前接口共同约束（写死）

所有接口当前必须满足：

- `inactive / not_implemented / placeholder-safe`
- `side_effects_released` 必须保持 `false`
- 不允许声称真实写入已发生
- 不允许触发真实 `release_control`
- 不允许 route / voice / memory / migration
- 不允许 `rollback` / `interrupt`

---

## 7. 与现有链路关系（写清；不能混用）

- 与 live implementation skeleton：旧 skeleton 是本体占位层；minimal code skeleton 是未来真实代码体专用骨架；两者不能混用。
- 与 live implementation stub：stub 是 runtime 占位；minimal code skeleton 是未来真实代码骨架。
- 与 go/no-go gate：go/no-go gate 负责“能不能开始”；minimal code skeleton 负责“开始后代码体放哪儿”。
- 与 rollout plan：rollout plan 定试运行策略；minimal code skeleton 只承载代码本体。

---

## 8. 当前仍然不能做什么（写死）

- 不允许打开 `side_effects_released`
- 不允许真实写入
- 不允许真实 `release_control`
- 不允许真实 rollout
- 不允许真实 `rollback` / `interrupt`
- 不允许 route / voice / memory / migration
- 不允许把 code skeleton 当作真实实现已存在

---

## 9. 当前不做（写死）

- 不做真实最小写入实现
- 不做真实 rollout 开启
- 不做地图接入
- 不做语音/记忆联动
- 不做中台真实迁移

---

## 10. 下一步边界（写死）

- 本轮之后，下一步才考虑：
  - minimal code path dry-run v0
- 再之后才考虑：
  - 第一版真实最小写入代码
- 当前不直接落真实实现

