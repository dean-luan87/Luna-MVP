# Luna — Navigation Governance Action Release Control First Live Guarded Implementation Minimal Real-Effect Live Implementation Controlled Trial Preparation Shadow Plan v0（准备态真实代码 shadow 旁路观察接入方案冻结）

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_LIVE_IMPLEMENTATION_CONTROLLED_TRIAL_PREPARATION_SHADOW_PLAN_V0.md`  
**性质**：Phase-Next-145：把“真实 minimal preparation code”以 shadow / observe-only 方式旁路挂到主链边上观察（只收集判断结果与一致性；不真实启用；不真实写入；不改主链行为）

---

## 1. 文档定位（写死）

这是第一版 `controlled trial preparation real code` 的 shadow 方案文档。当前目标是冻结：

- 真实 preparation 启用代码的**旁路观察接入边界**

本轮边界写死：

- 本轮只做 preparation shadow plan
- 不做真实主链接入执行
- 不做真实 preparation 启用
- 不做真实 trial 启用
- 不做默认路径开启
- 不做真实 rollback / interrupt
- 不接地图、不驱动语音/记忆、不改路线、不做中台真实迁移
- 不改变现有主线行为与输出

---

## 2. 为什么现在必须先做 preparation shadow（写死理由）

当前已经具备：

- 真实 minimal preparation code 已存在（但仍是显式入口，未接默认路径）

如果直接接主链，风险过高，且无法先验证：

- 主链输入是否稳定满足真实 preparation code 的前提
- 若旁路挂接，会出现多少 not_ready / blocked / failed
- 判断结果与现有 preparation gate / dry-run / controlled trial gate 链是否一致
- 若本会进入真实 preparation，最常见失败点是什么

因此必须先做 shadow / observe-only 接入，再决定是否进入真实启用。

---

## 3. shadow 的最小定义（写死）

`release_control first live guarded implementation minimal real-effect live implementation controlled trial preparation shadow` 是：

- 把真实 minimal preparation code 旁路挂到现有链路旁边的观察接入方案
- 只允许运行判断与收集结果，不允许真实启用
- 不改变主链输出，不改变主链副作用

---

## 4. 最小接入位置判断（冻结方向）

建议方向（写死）：

- shadow adapter 放在 `capabilities/governance/runtime/`
- 主链若未来需要挂接，仍通过 dispatcher 的 relevant-only metadata 分支完成（本轮不做挂接）
- 真实 preparation code 必须被强制替换为 observe-only writer / no-op writer

---

## 5. 最小合法输入（写死；只允许标准对象）

preparation shadow 只允许消费现有标准化对象与真实 preparation code 入口所需最小输入，包括但不限于：

- `controlled_trial_preparation_status == first_live_minimal_real_effect_controlled_trial_preparation_admitted`
- `controlled_trial_preparation_dry_run == first_live_minimal_real_effect_controlled_trial_preparation_dry_run_executed`
- `controlled_trial_go_no_go == first_live_minimal_real_effect_controlled_trial_go`
- `controlled_trial_first_minimal_real_enablement == first_live_minimal_real_effect_controlled_trial_real_enablement_ready`
- `side_effects_released == false`
- **显式 preparation_shadow enable signal**
- `execution_state_v0 / result_v0 / exception_or_failure_path_v0` 在位
- 真实 minimal preparation code identity / capability 在位（可导入）

并明确（写死）：

- 禁止读取 `request_* / approved_* / raw metadata`
- 缺任一主前提，preparation shadow 不成立

---

## 6. 最小 shadow 行为（写死）

只允许：

1) 调用真实 minimal preparation code 的输入校验逻辑/执行入口（但注入 no-op writers）  
2) 运行到“本来会写 state/result/exception”的判断分支  
3) 把本来会发生的写入转换为 observe-only 记录  
4) 输出 preparation shadow 标准化对象  

必须明确（写死）：

- 不允许真实写 `execution_state`
- 不允许真实写 `result_object`
- 不允许真实写 `exception_or_failure`
- 不允许打开 `side_effects_released`
- 不允许真实触发任何治理副作用
- 不允许真实开始 preparation / trial

---

## 7. 最小 shadow 输出（写死建议）

建议固定新增 metadata 对象（本轮先冻结对象结构，不做主链挂接）：

- `result.metadata["navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_preparation_shadow_v0"]`

最小结构建议至少包括：

- `preparation_shadow_attempted: true`
- `preparation_shadow_scope: "...preparation_shadow_v0"`
- `preparation_shadow_status: preparation_shadow_executed | preparation_shadow_not_ready | preparation_shadow_blocked`
- `would_have_entered_real_preparation_enablement: true|false`
- `would_have_written_execution_state: true|false`
- `would_have_written_result_object: true|false`
- `would_have_written_exception_or_failure: true|false`
- `side_effects_released: false`
- `reason: "..."`

---

## 8. 最小对比/验证指标（写死）

至少观察：

- 真实 preparation 启用前提满足率
- `preparation_shadow_executed / not_ready / blocked` 比例
- `would_have_entered_real_preparation_enablement` 命中率
- signal 缺失率
- blocked 原因分布
- failed-like 路径分布
- 与现有 preparation gate / dry-run 结果一致率
- 若进入异常分支，本会在哪一步失败

---

## 9. 明确禁止（写死）

preparation shadow 不允许：

- 打开 `side_effects_released`
- 真实写入 state/result/exception
- 改变主链输出
- route / voice / memory / migration
- rollback / interrupt
- 默认开启 preparation shadow
- 越过标准对象吐散字段

---

## 10. 与现有链路的关系（写清）

- 与真实 minimal preparation code：真实代码已存在；preparation shadow 只是旁路观察接入，不是真实启用
- 与 preparation dry-run：dry-run 是占位链演练；preparation shadow 是对真实代码本体的 observe-only 接入
- 与 preparation admission gate：gate 决定准备态资格；shadow 只验证“如果现在开始，真实 preparation 代码会怎么判”
- 与 controlled trial shadow/evaluation 链：preparation shadow 更下游、更接近真实 preparation 启用

---

## 11. 当前不做（写死）

- 不做真实主链接入
- 不做默认启用
- 不做真实 rollout 开启
- 不做地图接入
- 不做语音/记忆联动
- 不做中台真实迁移

---

## 12. 下一步边界（写死）

- 本轮之后，下一步才考虑：
  - controlled trial preparation shadow minimal implementation
- 再之后才考虑：
  - 是否在受控环境下开启真正的 preparation
- 当前不直接启用真实 trial / preparation

