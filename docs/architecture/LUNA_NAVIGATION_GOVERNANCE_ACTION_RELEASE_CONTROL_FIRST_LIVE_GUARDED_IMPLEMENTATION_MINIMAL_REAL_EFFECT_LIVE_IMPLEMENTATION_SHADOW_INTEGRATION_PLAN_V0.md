# Luna — Navigation Governance Action Release Control First Live Guarded Implementation Minimal Real-Effect Live Implementation Shadow Integration Plan v0（旁路观察接入方案冻结）

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_LIVE_IMPLEMENTATION_SHADOW_INTEGRATION_PLAN_V0.md`  
**性质**：Phase-Next-129：冻结“第一版真实最小写入代码”的 **shadow / observe-only** 旁路接入方案（只规划、不启用、不真实写入；不影响主链输出；默认不开）

基于（已具备）：
- 真实最小写入代码（显式入口）：`capabilities/governance/runtime/navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_v0.py`
- verify：`tools/verify_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_v0.py`
- live implementation definition / skeleton / stub / minimal code skeleton（冻结 + 在位）
- wiring / runtime dry-run / code path dry-run（在位）
- runtime activation stub / runtime implementation stub（在位）
- rollout plan / go-no-go gate / first real code activation definition（冻结）
- 当前 `side_effects_released` 仍强制锁死为 `false`

---

## A. 文档定位（写死）

这是第一版 `live implementation first minimal real write code` 的 **shadow integration 方案**文档。当前目标是冻结“真实代码旁路观察接入”的边界：如何挂到现有链路旁边、如何收集判断结果与一致性信息、但不让它真实写入、不让它改变主链行为。

并写死：

- 本轮只做 shadow integration plan（不落代码实现）。
- 不做真实接主链执行、不做真实 rollout 启用。
- 不做真实 `rollback` / `interrupt`。
- 不接地图、不驱动语音/记忆、不改路线、不做中台真实迁移。
- 不改变现有主线行为与输出。

---

## B. 为什么现在必须先做 shadow integration（写死理由）

- 第一版真实最小写入代码已经存在，但目前是显式调用入口，尚未进入现有链路。
- 如果直接接主链，风险过高，且难以先验证输入稳定性与判断一致性（尤其是 signal 缺失、blocked 分布、would-have-write 预测与链路对象一致性）。
- 因此必须先做 shadow / observe-only 接入方案冻结，再决定是否进入任何受控实现或启用。

---

## C. shadow integration 的最小定义（写死）

`release_control first live guarded implementation minimal real-effect live implementation shadow integration` 是：

- 把真实最小写入代码**旁路挂到现有链路旁边**的观察接入方案
- 只允许运行判断与收集结果，不允许真实写入
- 不改变主链输出，不改变主链副作用

核心定义（写死一句）：

> shadow integration 只允许 observe-only 调用真实最小写入代码，并记录结果，不允许其真实生效。

---

## D. 最小接入位置判断（写死建议）

### D1. 最小挂接位置（建议）

- 主链挂接优先继续通过 `capabilities/voice/runtime/voice_final_text_dispatcher.py` 的 **relevant-only metadata 分支**完成（只写一个新的 shadow 结果对象到 metadata）。

### D2. shadow adapter / helper 的落点（建议）

- shadow adapter（若后续进入最小实现）建议放在：
  - `capabilities/governance/runtime/`（与真实最小写入代码同域，便于保持单一边界）
  - 或 `capabilities/mid_platform/runtime/`（若更偏“中台聚合与观测层”）

### D3. 为什么这个位置最小、最连续、最不容易失控（写死理由）

- dispatcher 侧 relevant-only 挂载只追加 metadata，不改变主链业务语义与输出。
- shadow adapter 可以强制使用 observe-only writer / no-op writer，避免任何真实写入路径。
- 物理隔离：shadow 观察层 ≠ 真实启用层。

---

## E. 最小合法输入（写死；只允许标准化对象）

shadow integration 只允许消费现有标准化对象与真实代码入口所需最小输入，包括但不限于：

- real-write go/no-go gate == `first_live_minimal_real_effect_real_write_go`
- live code path dry-run == `first_live_minimal_real_effect_live_code_path_dry_run_executed`
- activation / commit / pre-commit / launch / admission 全链路 admitted/ready
- `side_effects_released == false`
- **显式 shadow approval / shadow enable signal**（语义在位）
- state / result / exception_or_failure path 在位
- 真实最小写入代码 identity / capability 在位

并明确（写死）：

- 禁止读取 `request_* / approved_* / raw metadata`
- 缺任一主前提，shadow integration 不成立（不得输出 shadow_executed）

---

## F. 最小 shadow 行为（写死）

shadow 模式下只允许：

1) 调用真实最小写入代码的**输入校验逻辑**（例如 `accept_*`）  
2) 运行到“本来会写 state/result/exception”的判断分支（但必须替换为 observe-only）  
3) 把这些本来会发生的行为转换为 observe-only 记录  
4) 输出 shadow 结果对象  
5) 不修改主链最终结果对象中的真实业务语义  

必须明确（写死）：

- 不允许真实写 `execution_state`
- 不允许真实写 `result_object`
- 不允许真实写 `exception_or_failure`
- 不允许打开 `side_effects_released`
- 不允许真实触发任何治理副作用

---

## G. 最小 shadow 输出（写死）

建议固定新增标准化对象写入：

- `result.metadata["navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_shadow_v0"]`

最小结构建议至少包括：

- `..._attempted: true`
- `..._scope: "navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_shadow_v0"`
- `shadow_status: shadow_executed | shadow_not_ready | shadow_blocked`
- `would_have_entered_real_write: true|false`
- `would_have_written_execution_state: true|false`
- `would_have_written_result_object: true|false`
- `would_have_written_exception_or_failure: true|false`
- `side_effects_released: false`
- `reason: "..."`

要求（写死）：

- 只反映“如果这次是真实执行，本会发生什么”
- 不新增时间/空间字段
- 不改变主链原有对象语义

---

## H. 最小对比/验证指标（写死）

shadow 观察至少应覆盖：

- 真实代码前提满足率
- `shadow_executed / shadow_not_ready / shadow_blocked` 比例
- `would_have_entered_real_write` 命中率
- signal 缺失率（shadow approval / real-write approval）
- blocked 原因分布
- 与现有 gate / dry-run 结果的一致率（例如 go/no-go、code path dry-run executed）
- 若进入异常分支，本会在哪一步失败（按固定顺序）

---

## I. 明确禁止（写死）

shadow integration 不允许直接：

- 打开 `side_effects_released`
- 真实写入 state/result/exception
- 改变主链输出
- route / voice / memory / migration
- rollback / interrupt
- 默认开启 shadow
- 越过标准对象吐散字段

---

## J. 与现有链路的关系（写清）

- 与真实最小写入代码：真实代码已存在；shadow integration 只是旁路观察接入，不是真实启用。
- 与 rollout plan：rollout plan 定试运行策略；shadow integration 是试运行前的旁路验证层。
- 与 go/no-go gate：gate 决定未来能否开始真实写入；shadow integration 只验证“如果现在开始，真实代码会怎么判”。
- 与现有 dry-run：dry-run 是占位链/代码路径链演练；shadow integration 是对真实代码本体的 observe-only 接入。

---

## K. 当前仍然不能做什么（写死）

- 不允许打开 `side_effects_released`
- 不允许真实写入
- 不允许真实 `release_control`
- 不允许真实 rollout
- 不允许真实 `rollback` / `interrupt`
- 不允许 route / voice / memory / migration
- 不允许把 shadow 结果当作真实执行结果

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
  - shadow integration minimal implementation（observe-only adapter/runner + metadata relevant-only 接入）
- 再之后才考虑：
  - 是否在受控环境下开启真正的 first real write
- 当前不直接启用真实写入

