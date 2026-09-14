# Luna — Navigation Governance Action Release Control First Live Guarded Implementation Minimal Real-Effect Live Implementation Stub v0（真实写入本体 runtime 占位层：冻结）

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_LIVE_IMPLEMENTATION_STUB_V0.md`  
**性质**：Phase-Next-116：把 live implementation 从“代码骨架占位”推进到“运行时 stub 占位”，但仍保持完全非动作（只占位、不执行；可冻结、可回归）

基于（已具备）：
- live implementation definition v0（冻结）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_LIVE_IMPLEMENTATION_DEFINITION_V0.md`
- live implementation skeleton v0（冻结 + 代码骨架）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_LIVE_IMPLEMENTATION_SKELETON_V0.md`

---

## A. 文档定位（写死）

- 这是 `release_control first live guarded implementation minimal real-effect live implementation stub` 的设计文档。
- 当前目标：把 live implementation skeleton 推进到运行时 stub，占住未来真实最小写入实现本体的 runtime 承接位。

并且（本轮写死边界）：

- 当前不做真实 `release_control`
- 当前不做真实 `rollback` / `interrupt`
- 当前不做地图接入、不改路线
- 当前不做语音/记忆联动
- 当前不改变现有主线行为
- 当前 `side_effects_released` 仍强制锁死为 `false`

---

## B. 为什么现在要先做 stub

- live implementation definition 已存在。
- live implementation skeleton 已存在（代码壳子）。
- 若缺少 runtime stub，后续容易直接把 skeleton 改成真实实现，导致层次混用与扩权滑坡。

因此必须先单独占住 live implementation 的 runtime stub 层，但当前仍不能触发任何真实治理动作。

---

## C. stub 的最小定义（写死）

live implementation stub：

- 不是真实 live implementation
- 不是真实写入执行器
- 是“第一版真实最小写入实现本体”的 runtime 占位层

作用（写死）：

- 为未来真实最小写入实现预留运行时承接位
- 调用/承接 skeleton 的占位接口
- 明确区分于 skeleton 与未来 minimal implementation

---

## D. 当前最小输入依据（写死）

- 只允许消费标准化对象语义与 definition / skeleton 边界。
- 当前不允许以 raw metadata 直驱真实写入。
- 当前 stub 只是 runtime 占位，不进入主链副作用执行。

---

## E. 必须提供的最小接口（建议写死）

至少提供：

- `get_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_stub_identity()`
- `accept_first_live_minimal_real_effect_live_implementation_runtime_input(...)`
- `emit_live_execution_state_real_effect_placeholder_from_stub(...)`
- `emit_live_result_object_real_effect_placeholder_from_stub(...)`
- `emit_live_failure_or_exception_real_effect_placeholder_from_stub(...)`
- `raise_first_live_minimal_real_effect_live_implementation_stub_exception(...)`

---

## F. 当前接口的共同约束（必须写死）

- 所有接口当前都必须返回 `inactive / not_implemented / placeholder-safe`
- 所有接口当前都必须保持 `side_effects_released == false`
- 不允许声称真实写入已经发生
- 不允许触发真实 `release_control`
- 不允许触发真实 `rollback` / `interrupt`
- 不允许 `route / voice / memory / migration`

---

## G. 与现有链路的关系（写清）

- 与 live implementation skeleton：skeleton 是代码壳子；stub 是运行时占位层；两者不能混用。
- 与 activation gate / activation dry-run：它们负责判断与演练；live implementation stub 是未来真实本体进入 runtime 前的承接层。
- 与 live implementation definition：definition 定边界；stub 是 runtime 占位；`definition ≠ stub`。

---

## H. 当前仍然不能做什么（写死）

- 不允许打开 `side_effects_released`
- 不允许真实写入
- 不允许真实 `release_control`
- 不允许真实 `rollback` / `interrupt`
- 不允许 `route / voice / memory / migration`
- 不允许把 stub 当作真实实现已存在

---

## I. 当前不做（写死）

- 不做 live implementation minimal implementation
- 不做真实最小写入实现
- 不做地图接入
- 不做语音/记忆联动
- 不做中台真实迁移

---

## J. 下一步边界（写死）

- 本轮之后，下一步才考虑：
  - minimal real-effect live implementation minimal implementation v0
- 补充链接：
  - Phase-Next-117：Minimal Real-Effect Live Implementation Admission & Acceptance v0（准入与验收红线：冻结）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_LIVE_IMPLEMENTATION_ADMISSION_AND_ACCEPTANCE_V0.md`
- 当前不直接落真实实现

