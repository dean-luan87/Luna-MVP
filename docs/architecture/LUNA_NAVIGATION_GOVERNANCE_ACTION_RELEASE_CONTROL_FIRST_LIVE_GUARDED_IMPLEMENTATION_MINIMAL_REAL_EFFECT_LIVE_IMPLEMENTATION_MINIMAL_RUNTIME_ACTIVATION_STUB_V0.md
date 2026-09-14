# Luna — Navigation Governance Action Release Control First Live Guarded Implementation Minimal Real-Effect Live Implementation Minimal Runtime Activation Stub v0（短时受控激活占位：冻结）

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_LIVE_IMPLEMENTATION_MINIMAL_RUNTIME_ACTIVATION_STUB_V0.md`  
**性质**：Phase-Next-121：冻结第一版 `live implementation minimal implementation` 中最敏感的“短时受控激活 side_effects_released”承载位（runtime activation stub；只占位、不激活；可冻结、可回归）

基于（已具备）：
- live implementation definition v0（冻结）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_LIVE_IMPLEMENTATION_DEFINITION_V0.md`
- live implementation skeleton v0（在位）：`capabilities/governance/runtime/navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_skeleton_v0.py`
- live implementation stub v0（在位）：`capabilities/governance/runtime/navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_stub_v0.py`
- live implementation admission & acceptance v0（冻结）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_LIVE_IMPLEMENTATION_ADMISSION_AND_ACCEPTANCE_V0.md`
- live implementation minimal implementation plan v0（冻结）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_LIVE_IMPLEMENTATION_MINIMAL_IMPLEMENTATION_V0.md`
- live implementation non-effect wiring v0（冻结 + 最小实现）
- live implementation dry-run execution v0（冻结 + 最小实现）
- activation contract / gate / dry-run（冻结 + 最小实现）
- activation / commit / pre-commit / launch / admission 全链路对象（最小实现）
- 当前 `side_effects_released` 仍强制锁死为 `false`

---

## 1. 文档定位（写死）

这份文档是：

- 第一版 `release_control first live guarded implementation minimal real-effect live implementation minimal implementation` 的 **minimal runtime activation stub** 设计冻结文档。
- 当前目标：冻结“从 dry-run execution → 未来真实最小写入实现中的短时受控激活层”的边界，让最敏感动作有一个独立运行时承载位（但当前仍完全非动作）。

并且（本轮写死边界）：

- 本轮只做 minimal runtime activation stub（占位）。
- 不做真实 runtime activation（不打开 side_effects_released）。
- 不做真实写入。
- 不触发真实 `release_control`。
- 不触发真实 `rollback` / `interrupt`。
- 不接地图、不改路线。
- 不驱动语音/记忆。
- 不触发中台真实迁移。
- 不改变现有主线行为。

---

## 2. 为什么现在必须先做 runtime activation stub（写死理由）

- 当前 live implementation dry-run execution 已存在，且证明“runtime 顺序可以零副作用演练”。
- activation contract 已存在，定义了未来唯一允许的受控激活规则（但当前禁止打开）。
- 但还缺一个单独的运行时占位层去承接最敏感的语义瞬间：
  - `side_effects_released: false -> （受控短时激活语义） -> 恢复 false`
- 如果不先占住 stub，后续最容易把这段逻辑直接塞进 live implementation 本体，导致边界失控与回退困难。

因此必须先单独占住 runtime activation stub 层：未来真实实现只能通过该层进入受控短时激活语义，不得绕过。

---

## 3. 最小定义（写死）

`release_control first live guarded implementation minimal real-effect live implementation minimal runtime activation stub` 是：

- future live implementation 中承接“短时受控激活 side_effects_released”语义的 runtime 占位层
- 当前只负责占位、返回 placeholder-safe 结果
- 当前不执行任何真实激活，不改变 `side_effects_released`

---

## 4. 最小合法输入（写死；只允许标准化对象）

runtime activation stub 只允许消费（只读）：

- live implementation definition 已冻结
- live implementation skeleton 已存在
- live implementation stub 已存在
- live implementation admission & acceptance 条件全部满足（通过上游对象体现）
- live implementation minimal implementation plan 已冻结
- live implementation non-effect wiring == wired_ready
- live implementation dry-run execution == executed
- activation contract / gate / dry-run 已满足
- execution_state / result / exception_or_failure path 在位
- `side_effects_released == false`

并明确（写死）：

- 缺任一主前提，runtime activation stub 不成立（不得声称可进入激活语义）。
- 禁止读取 `request_* / approved_* / raw metadata`。

---

## 5. 必须提供的最小接口（写死建议）

最小接口建议至少包括：

- `get_release_control_first_live_guarded_implementation_minimal_real_effect_live_runtime_activation_stub_identity()`
- `accept_first_live_minimal_real_effect_runtime_activation_input(...)`
- `enter_live_runtime_activation_placeholder(...)`
- `exit_live_runtime_activation_placeholder(...)`
- `raise_first_live_minimal_real_effect_runtime_activation_stub_exception(...)`

---

## 6. 当前接口共同约束（写死）

所有接口当前必须满足：

- 返回 `inactive / not_implemented / placeholder-safe`
- `side_effects_released` 必须保持 `false`
- 不允许声称真实激活已发生
- 不允许触发真实写入
- 不允许触发真实 `release_control`
- 不允许 route / voice / memory / migration
- 不允许 `rollback` / `interrupt`

---

## 7. 与现有链路关系（写清；不能混用）

- 与 activation contract：contract 定义未来唯一允许的激活规则；runtime activation stub 是其运行时占位承接层。
- 与 live implementation stub：live implementation stub 是本体 runtime 占位；runtime activation stub 是其中最敏感激活动作的专用占位层。
- 与 live implementation dry-run execution：dry-run execution 负责最小顺序演练；runtime activation stub 负责未来真实实现里的“短时受控激活”承接位。
- 与 future live implementation：未来真实实现只能通过该层进入短时受控激活语义，不得绕过。

---

## 8. 当前仍然不能做什么（写死）

- 不允许打开 `side_effects_released`
- 不允许真实写入
- 不允许真实 `release_control`
- 不允许真实 `rollback` / `interrupt`
- 不允许 route / voice / memory / migration
- 不允许把 runtime activation stub 当作真实激活已存在

---

## 9. 当前不做（写死）

- 不做真实 runtime activation
- 不做 live implementation minimal implementation
- 不做地图接入
- 不做语音/记忆联动
- 不做中台真实迁移

---

## 10. 下一步边界（写死）

- 本轮之后，下一步才考虑：
  - live implementation minimal implementation v0 的最小真实实现
- 当前不直接落真实实现

