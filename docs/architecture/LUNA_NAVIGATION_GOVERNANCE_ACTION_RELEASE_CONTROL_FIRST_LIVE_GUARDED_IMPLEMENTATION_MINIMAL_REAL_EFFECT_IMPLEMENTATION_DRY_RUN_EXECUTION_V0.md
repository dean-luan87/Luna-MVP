# Luna — Navigation Governance Action Release Control First Live Guarded Implementation Minimal Real-Effect Implementation Dry-Run Execution v0（Implementation Skeleton：干跑执行链冻结）

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_IMPLEMENTATION_DRY_RUN_EXECUTION_V0.md`  
**性质**：Phase-Next-98：冻结 `minimal real-effect implementation skeleton` 的 **implementation dry-run execution**（只干跑顺序、不放权；可冻结、可回归）

基于（已具备）：
- implementation definition（冻结）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_IMPLEMENTATION_DEFINITION_V0.md`
- implementation skeleton（冻结 + 落代码）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_IMPLEMENTATION_SKELETON_V0.md`
- implementation non-effect wiring（冻结 + 最小实现）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_IMPLEMENTATION_NON_EFFECT_WIRING_V0.md`
- standard objects：`execution_state_v0` / `result_v0`

---

## 1. 文档定位（写死）

这份文档是：

- `release_control first live guarded implementation minimal real-effect implementation skeleton` 的 **dry-run execution** 设计文档。
- 当前目标：在 `implementation wiring == wired_ready` 的前提下，让未来真实实现层先把调用顺序跑通；但执行链只允许调用 skeleton 的占位接口（placeholder-safe / reported-placeholder），不产生任何真实副作用。

并且（本轮写死边界）：

- 当前不做真实 `release_control`。
- 当前不做真实 `rollback` / `interrupt`。
- 当前不做地图接入、不改路线。
- 当前不做语音/记忆联动。
- 当前不做中台真实迁移。
- 当前不改变现有主线行为。
- 当前 `side_effects_released` 仍强制锁死为 `false`（不允许打开）。

---

## 2. 为什么现在要做 implementation dry-run execution（写死理由）

- implementation skeleton 已存在，implementation wiring 已存在；但 wiring 只证明“合法入口成立”，并不证明未来真实实现层的执行顺序能跑通。
- 因此必须再做一层 implementation dry-run execution，验证未来真实实现层的：
  - 调用顺序（state → result → failure/exception closure）
  - 接口边界（只走占位接口）
  - 收口位置（标准化对象内可观测 trace，不吐散字段）
- 但当前仍不能放开任何真实副作用。

---

## 3. dry-run execution 的最小定义（写死）

Implementation dry-run execution：

- 不是真实 real-effect implementation
- 不是真实写入

它只是：

- “未来真实实现层执行顺序”的干跑执行链
- 只允许调用 implementation skeleton 的占位接口
- 不允许真实写入/不允许越权动作

---

## 4. 最小合法输入（写死；只允许标准化对象）

只允许消费（只读）：

- `navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_implementation_wiring_v0`
  - 必须 `wiring_status == "first_live_minimal_real_effect_implementation_wired_ready"`
- implementation skeleton identity / capability
  - 必须在位且仍为 skeleton / 非放权模式
- `execution_state_v0`
  - 在位
- `result_v0`
  - 在位
- failure/exception path
  - 语义上在位，可被占位调用（reported-placeholder / stop-safe）

并明确（写死）：

- 缺任一主前提，dry-run execution 不成立。
- 禁止直接读取 `request_* / approved_* / raw metadata` 作为输入来源。

---

## 5. 最小结果集合（写死；三态）

dry-run execution 的结果必须收敛成三态之一：

- `first_live_minimal_real_effect_implementation_dry_run_executed`
- `first_live_minimal_real_effect_implementation_dry_run_not_ready`
- `first_live_minimal_real_effect_implementation_dry_run_blocked`

并明确（写死）：

- `executed` 只表示未来真实实现层的最小执行链已在零副作用模式下跑通。
- 不表示真实写入已发生，也不表示副作用已发生。

---

## 6. 最小执行顺序（写死）

dry-run execution 成功时固定顺序必须是：

1) `execution_state_real_write_placeholder_call_from_implementation`
2) `result_object_real_write_placeholder_call_from_implementation`
3) `failure_or_exception_real_write_placeholder_closure_from_implementation`

并写死：

- 不允许倒序、跳步。
- 不允许在干跑链里插入 route / voice / memory / migration / rollback / interrupt。

---

## 7. 明确禁止（写死）

dry-run execution 不允许直接：

- 打开 `side_effects_released`
- 执行真实 `release_control`
- 改路线
- 触发语音播报
- 写记忆
- 触发中台真实迁移
- 自动触发 `rollback` / `interrupt`
- 越过标准对象吐散字段

---

## 8. 与现有链路的关系（写清；不能混用）

- 与 implementation wiring：
  - wiring 负责给 implementation skeleton 一个合法入口
  - dry-run execution 负责在合法入口上跑通未来真实实现顺序
  - `wired_ready` 不等于 `executed`
- 与 implementation skeleton：
  - skeleton 是未来真实实现壳子
  - dry-run execution 是它的第一条零副作用执行链
  - 两者不能混用
- 与 implementation definition：
  - definition 规定真实实现层边界
  - dry-run execution 只验证顺序与调用边界可走通
  - 当前仍不执行真实 implementation

---

## 9. 当前仍然不能做什么（写死）

- 不允许把 `side_effects_released` 打开
- 不允许真实 `release_control`
- 不允许真实 `rollback` / `interrupt`
- 不允许 route / voice / memory / migration
- 不允许把 `executed` 当作真实写入已开始

---

## 10. 当前不做（写死）

- 不做真实 real-effect implementation
- 不做地图接入
- 不做语音/记忆联动
- 不做中台真实迁移

---

## 11. 下一步边界（写死）

- 本轮之后，下一步才考虑：
  - first live guarded implementation minimal real-effect implementation gate / stub / true implementation proposal
- 当前不直接落真实实现。

