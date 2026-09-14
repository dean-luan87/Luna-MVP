# Luna — Navigation Governance Action Release Control First Live Guarded Implementation Minimal Real-Effect Live Implementation Skeleton v0（真实写入本体专用骨架：冻结）

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_LIVE_IMPLEMENTATION_SKELETON_V0.md`  
**性质**：Phase-Next-115：把 live implementation definition 落成一个独立、专用、不可放权的代码骨架（只占位、不执行；可冻结、可回归）

基于（已具备）：
- live implementation definition v0（冻结）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_LIVE_IMPLEMENTATION_DEFINITION_V0.md`
- activation gate / activation dry-run（已具备实现）
- commit / pre-commit / launch / admission 链路（已具备实现）
- 现有 implementation skeleton v0（早期承载位）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_IMPLEMENTATION_SKELETON_V0.md`

---

## A. 文档定位（写死）

- 这是 `release_control first live guarded implementation minimal real-effect live implementation skeleton` 的设计文档。
- 当前目标：把 live implementation definition 落成专用代码骨架，作为未来第一版真实最小写入实现本体的**唯一代码承载壳子**。

并且（本轮写死边界）：

- 当前不做真实 `release_control`
- 当前不做真实 `rollback` / `interrupt`
- 当前不做地图接入、不改路线
- 当前不做语音/记忆联动
- 当前不改变现有主线行为
- 当前 `side_effects_released` 仍强制锁死为 `false`

---

## B. 为什么现在要先做 skeleton

- live implementation definition 已存在。
- 若没有专用 skeleton，后续最容易把真实实现、旧 skeleton、stub、dry-run、gate 混用，导致真实写入入口与边界失控。

因此必须先单独占住 live implementation 的代码壳子，但当前仍不能触发任何真实治理动作。

---

## C. skeleton 的最小定义（写死）

live implementation skeleton：

- 不是真实 live implementation
- 不是真实写入执行器
- 是“第一版真实最小写入实现本体”的专用代码骨架

作用（写死）：

- 为未来真实最小写入实现预留唯一承载位
- 固定 identity / capability / scope
- 提供专用占位接口（全部 placeholder-safe / inactive）

---

## D. 当前最小输入依据（写死）

- 只允许消费标准化对象语义与 definition 边界（未来由真实实现层消费）。
- 不允许直读 raw metadata 作为真实输入来源。
- skeleton 当前只是代码骨架，不依赖 dispatcher 主链输出才可存在（它可以被导入，但不产生任何副作用）。

---

## E. 必须提供的最小接口（建议写死）

至少提供：

- `get_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_skeleton_identity()`
- `accept_first_live_minimal_real_effect_live_implementation_input(...)`
- `write_live_execution_state_real_effect_from_live_implementation(...)`
- `write_live_result_object_real_effect_from_live_implementation(...)`
- `write_live_failure_or_exception_real_effect_from_live_implementation(...)`

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

- 与 `implementation_skeleton_v0`：旧 skeleton 服务更早阶段的 implementation 承载；live implementation skeleton 是未来真实本体专用骨架；两者不能混用。
- 与 activation gate / activation dry-run：它们负责判断与演练；live implementation skeleton 是未来真实执行本体承载位。
- 与 live implementation definition：definition 定边界；skeleton 是代码壳子；`definition ≠ skeleton`。

---

## H. 当前仍然不能做什么（写死）

- 不允许打开 `side_effects_released`
- 不允许真实写入
- 不允许真实 `release_control`
- 不允许真实 `rollback` / `interrupt`
- 不允许 `route / voice / memory / migration`
- 不允许把 skeleton 当作真实实现已存在

---

## I. 当前不做（写死）

- 不做 live implementation stub
- 不做 live implementation minimal implementation
- 不做真实最小写入实现
- 不做地图接入
- 不做语音/记忆联动
- 不做中台真实迁移

---

## J. 下一步边界（写死）

- 本轮之后，下一步才考虑：
  - minimal real-effect live implementation stub v0
- 再之后才考虑：
  - minimal real-effect live implementation minimal implementation v0
- 当前不直接落真实实现

