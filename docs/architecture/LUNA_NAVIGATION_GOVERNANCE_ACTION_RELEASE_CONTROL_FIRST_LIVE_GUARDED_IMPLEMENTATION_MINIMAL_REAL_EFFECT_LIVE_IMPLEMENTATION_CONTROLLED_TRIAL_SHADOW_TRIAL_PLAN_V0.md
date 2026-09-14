# Luna — Navigation Governance Action Release Control First Live Guarded Implementation Minimal Real-Effect Live Implementation Controlled Trial Shadow Trial Plan v0（旁路观察接入方案冻结）

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_LIVE_IMPLEMENTATION_CONTROLLED_TRIAL_SHADOW_TRIAL_PLAN_V0.md`  
**性质**：Phase-Next-139：冻结“真实 minimal trial enablement code”的 **shadow trial / observe-only** 旁路接入方案（只规划、不启用、不真实写入；不影响主链输出；默认不开）

基于（已具备）：

- 真实 minimal trial enablement code：`capabilities/governance/runtime/navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_real_enablement_v0.py`
- verify：`tools/verify_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_real_enablement_v0.py`
- controlled trial enablement implementation / dry-run / definition（在位 + 冻结）
- controlled trial admission / go-no-go / shadow evaluation（在位）
- 当前 `side_effects_released` 仍强制锁死为 `false`

---

## A. 文档定位（写死）

这是第一版 controlled trial real enablement code 的 shadow trial 方案文档。当前目标是冻结“真实 trial 启用代码旁路观察接入”的边界：

- 真实代码可以被旁路 observe-only 调用并产出 shadow 结果
- 但不允许其真实启用、不允许真实写入、不允许改变主链行为

本轮边界写死：

- 本轮只做 shadow trial plan（只规划）
- 不做真实主链接入执行
- 不做真实 trial 启用
- 不做默认路径开启
- 不做真实 rollback / interrupt
- 不接地图、不驱动语音/记忆、不改路线、不做中台真实迁移
- 不改变现有主线行为与输出

---

## B. 为什么现在必须先做 shadow trial（写死理由）

- 真实 minimal trial enablement code 已经存在，但目前是显式调用入口，尚未进入现有链路。
- 如果直接接主链进入真实启用，风险过高，且无法先验证输入稳定性与判断一致性。
- 因此必须先做 shadow trial / observe-only 接入，再决定是否进入真实启用。

---

## C. shadow trial 的最小定义（写死）

`release_control first live guarded implementation minimal real-effect live implementation controlled trial shadow trial` 是：

- 把真实 minimal trial enablement code **旁路挂到现有链路旁边**的观察接入方案
- 只允许运行判断与收集结果，不允许真实启用
- 不改变主链输出，不改变主链副作用

核心定义（写死一句）：

> shadow trial 只允许 observe-only 调用真实 minimal trial enablement code，并记录结果，不允许其真实生效。

---

## D. 最小接入位置判断（写死建议）

- 主链挂接优先继续通过 `capabilities/voice/runtime/voice_final_text_dispatcher.py` 的 **relevant-only metadata 分支**完成（只写一个新的 shadow trial 结果对象到 metadata）。
- shadow trial adapter 建议放在 `capabilities/governance/runtime/`，与真实 enablement code 同域，便于保持单一边界。
- 必须强制替换为 observe-only writer / no-op writer，避免任何真实写入。

---

## E. 最小合法输入（写死；只允许标准化对象）

shadow trial 只允许消费现有标准化对象与真实 trial 启用代码入口所需最小输入，包括但不限于：

- controlled trial go/no-go == go
- controlled trial admission == admitted
- shadow eval == go
- real-write go/no-go == go
- controlled trial enablement dry-run == executed
- controlled trial first minimal real enablement == ready
- `side_effects_released == false`
- **显式 shadow_trial approval / enable signal**（默认不开；语义在位）
- `execution_state_v0 / result_v0 / exception_or_failure_path_v0` 在位
- 真实 minimal trial enablement code identity/capability 在位

并明确（写死）：

- 禁止读取 `request_* / approved_* / raw metadata`
- 缺任一主前提，shadow trial 不成立（不得输出 shadow_trial_executed）

---

## F. 最小 shadow 行为（写死）

shadow 模式下只允许：

1) 调用真实 minimal trial enablement code 的输入校验逻辑  
2) 运行到“本来会写 state/result/exception”的判断分支（但必须替换为 observe-only）  
3) 把这些本来会发生的行为转换为 observe-only 记录  
4) 输出 shadow trial 结果对象  
5) 不修改主链最终结果对象中的真实业务语义

必须明确（写死）：

- 不允许真实写 `execution_state`
- 不允许真实写 `result_object`
- 不允许真实写 `exception_or_failure`
- 不允许打开 `side_effects_released`
- 不允许真实触发任何治理副作用
- 不允许真实开始 controlled trial

---

## G. 最小 shadow 输出（写死）

建议固定新增标准化对象写入：

- `result.metadata["navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_shadow_v0"]`

最小结构建议至少包括：

- `shadow_trial_attempted: true`
- `shadow_trial_scope: "...controlled_trial_shadow_v0"`
- `shadow_trial_status: shadow_trial_executed | shadow_trial_not_ready | shadow_trial_blocked`
- `would_have_entered_real_trial_enablement: true|false`
- `would_have_written_execution_state: true|false`
- `would_have_written_result_object: true|false`
- `would_have_written_exception_or_failure: true|false`
- `side_effects_released: false`
- `reason: "..."`

要求（写死）：

- 只反映“如果这次是真实启用，本会发生什么”
- 不新增时间/空间字段
- 不改变主链原有对象语义

---

## H. 最小对比/验证指标（写死）

shadow trial 观察至少应覆盖：

- 真实启用前提满足率
- `shadow_trial_executed / shadow_trial_not_ready / shadow_trial_blocked` 比例
- `would_have_entered_real_trial_enablement` 命中率
- signal 缺失率
- blocked 原因分布
- failed-like 路径分布
- 与现有 controlled trial gate 链的一致率
- 若进入异常分支，本会在哪一步失败（按固定顺序）

---

## I. 明确禁止（写死）

shadow trial 不允许：

- 打开 `side_effects_released`
- 真实写入 state/result/exception
- 改变主链输出
- route / voice / memory / migration
- rollback / interrupt
- 默认开启 shadow trial
- 越过标准对象吐散字段

---

## J. 与现有链路的关系（写清）

- 与真实 minimal trial enablement code：真实代码已存在；shadow trial 只是旁路观察接入，不是真实启用。
- 与 controlled trial minimal enablement plan：plan 定 trial 启用策略；shadow trial 是试运行前的旁路验证层。
- 与 controlled trial admission/go-no-go gate：它们决定 trial 条件是否允许；shadow trial 只验证“如果现在开始，真实 trial 启用代码会怎么判”。
- 与现有 dry-run：dry-run 是占位链/代码路径链演练；shadow trial 是对真实 trial 启用代码本体的 observe-only 接入。

---

## K. 当前仍然不能做什么（写死）

- 不允许打开 `side_effects_released`
- 不允许真实试运行
- 不允许真实写入
- 不允许默认启用
- 不允许真实 rollback / interrupt
- 不允许 route / voice / memory / migration
- 不允许把 shadow trial 结果当作真实 trial 结果

---

## L. 当前不做（写死）

- 不做真实主链接入
- 不做默认启用
- 不做真实 rollout 开启
- 不做地图接入
- 不做语音/记忆联动
- 不做中台真实迁移

---

## M. 下一步边界（写死）

- 本轮之后，下一步才考虑：
  - controlled trial shadow trial minimal implementation
- 再之后才考虑：
  - 是否在受控环境下开启真正的 first controlled trial
- 当前不直接启用真实 trial

