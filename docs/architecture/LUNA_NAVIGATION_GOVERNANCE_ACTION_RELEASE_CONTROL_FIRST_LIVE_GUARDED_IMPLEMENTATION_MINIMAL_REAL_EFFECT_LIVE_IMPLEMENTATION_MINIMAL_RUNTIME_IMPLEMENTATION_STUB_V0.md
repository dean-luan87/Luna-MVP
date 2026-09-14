# Luna — Navigation Governance Action Release Control First Live Guarded Implementation Minimal Real-Effect Live Implementation Minimal Runtime Implementation Stub v0（运行态入口占位：冻结）

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_LIVE_IMPLEMENTATION_MINIMAL_RUNTIME_IMPLEMENTATION_STUB_V0.md`  
**性质**：Phase-Next-127：冻结“第一版真实代码真正开始执行之后”的 runtime 入口层占位（minimal runtime implementation stub；只占位、不执行；默认不开；可冻结、可回归）

基于（已具备）：
- first real code activation definition v0（冻结）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_LIVE_IMPLEMENTATION_FIRST_REAL_CODE_ACTIVATION_DEFINITION_V0.md`
- live runtime activation stub v0（在位）
- live implementation definition / skeleton / stub / minimal code skeleton（冻结 + 在位）
- wiring / runtime dry-run / code path dry-run（在位）
- rollout plan / go-no-go gate（冻结）
- 当前 `side_effects_released` 仍强制锁死为 `false`

---

## 1. 文档定位（写死）

这是第一版 live implementation minimal implementation 的 **minimal runtime implementation stub** 设计文档。当前目标是冻结“从 first real code activation definition 到未来真实最小写入实现进入 runtime”的承接边界：谁来承接运行态入口、最小接口是什么、当前必须如何保持完全非动作。

并写死：

- 本轮只做 runtime implementation stub（占位）。
- 不做真实代码执行、不做真实 rollout 启用。
- 不做真实 `rollback` / `interrupt`。
- 不接地图、不驱动语音/记忆、不改路线、不做中台真实迁移。
- 不改变现有主线行为。

---

## 2. 为什么现在必须先做 runtime implementation stub（写死理由）

- first real code activation definition 已存在（定义了何时算真正开始执行）。
- live runtime activation stub 已存在（承接受控短时激活语义占位）。
- 但还缺一个单独的 runtime implementation stub 去承接“真实代码真正开始执行之后的第一层运行态入口”。
- 如果不先做 stub，后续最容易把 activation definition、activation stub、真实实现本体揉在一起，造成边界混淆与回归困难。

因此必须先单独占住 runtime implementation stub 层：它是未来真实实现进入运行态后的第一层承接位。

---

## 3. 最小定义（写死）

`release_control first live guarded implementation minimal real-effect live implementation minimal runtime implementation stub` 是：

- future real minimal write implementation 进入 runtime 后的第一层运行时占位承接层
- 当前只负责占位与返回 placeholder-safe 结果
- 不执行任何真实写入

---

## 4. 最小合法输入（写死；只允许标准化对象）

只允许消费（只读）：

- live implementation definition 已冻结
- live implementation skeleton 已存在
- live implementation stub 已存在
- live implementation minimal code skeleton 已存在
- live implementation admission & acceptance 已冻结
- live implementation minimal implementation plan 已冻结
- live implementation non-effect wiring == `first_live_minimal_real_effect_live_wired_ready`
- live implementation dry-run execution == `first_live_minimal_real_effect_live_dry_run_executed`
- live runtime activation stub 已存在
- first real write rollout plan 已冻结
- real-write go/no-go gate == `first_live_minimal_real_effect_real_write_go`
- live code path dry-run == `first_live_minimal_real_effect_live_code_path_dry_run_executed`
- first real code activation definition 已冻结
- activation / commit / pre-commit / launch / admission 全链路 admitted/ready
- execution_state / result / exception_or_failure path 在位
- `side_effects_released == false`

并写死：

- 缺任一主前提，runtime implementation stub 不成立
- 禁止读取 `request_* / approved_* / raw metadata`

---

## 5. 必须提供的最小接口（写死建议）

建议至少包括：

- `get_release_control_first_live_guarded_implementation_minimal_real_effect_live_runtime_implementation_stub_identity()`
- `accept_first_live_minimal_real_effect_runtime_implementation_input(...)`
- `enter_first_live_runtime_implementation_placeholder(...)`
- `perform_first_live_runtime_execution_state_placeholder(...)`
- `perform_first_live_runtime_result_placeholder(...)`
- `perform_first_live_runtime_exception_or_failure_placeholder(...)`
- `exit_first_live_runtime_implementation_placeholder(...)`
- `raise_first_live_minimal_real_effect_runtime_implementation_stub_exception(...)`

---

## 6. 当前接口共同约束（写死）

所有接口当前必须满足：

- 返回 `inactive / not_implemented / placeholder-safe`
- `side_effects_released` 必须保持 `false`
- 不允许声称真实写入已发生
- 不允许触发真实 `release_control`
- 不允许触发真实 rollout
- 不允许 route / voice / memory / migration
- 不允许 `rollback` / `interrupt`

---

## 7. 与现有链路关系（写清；不能混用）

- 与 first real code activation definition：definition 定“什么时候算真正开始执行”；runtime implementation stub 是开始执行后的第一层运行时占位承接层。
- 与 live runtime activation stub：activation stub 承接受控短时激活语义；runtime implementation stub 承接激活后的运行态入口语义；两者不能混用。
- 与 minimal code skeleton：skeleton 是代码体骨架；runtime implementation stub 是运行时占位层。
- 与 future real implementation body：未来真实实现只能通过该层进入 runtime，不得绕过。

---

## 8. 当前仍然不能做什么（写死）

- 不允许打开 `side_effects_released`
- 不允许真实写入
- 不允许真实 `release_control`
- 不允许真实 rollout
- 不允许真实 `rollback` / `interrupt`
- 不允许 route / voice / memory / migration
- 不允许把 runtime implementation stub 当作真实实现已存在

---

## 9. 当前不做（写死）

- 不做真实 runtime implementation
- 不做真实最小写入实现
- 不做地图接入
- 不做语音/记忆联动
- 不做中台真实迁移

---

## 10. 下一步边界（写死）

- 本轮之后，下一步才考虑：
  - live implementation first minimal real write code v0
- 当前不直接落真实实现

