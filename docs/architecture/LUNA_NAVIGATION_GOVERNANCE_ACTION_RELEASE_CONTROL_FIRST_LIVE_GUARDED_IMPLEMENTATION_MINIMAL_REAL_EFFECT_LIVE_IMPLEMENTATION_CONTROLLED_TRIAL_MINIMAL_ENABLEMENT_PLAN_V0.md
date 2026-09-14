# Luna — Navigation Governance Action Release Control First Live Guarded Implementation Minimal Real-Effect Live Implementation Controlled Trial Minimal Enablement Plan v0（受控试运行最小启用方案冻结）

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_LIVE_IMPLEMENTATION_CONTROLLED_TRIAL_MINIMAL_ENABLEMENT_PLAN_V0.md`  
**性质**：Phase-Next-134：冻结“第一阶段受控真实 trial 如何最小启用”的 enablement plan（只定义、不启用；默认不开；不进入任何默认路径）

---

## 1. 文档定位（写死）

这是第一版 `live implementation minimal real-effect` 进入第一阶段受控真实 trial 的**最小启用方案**文档。当前目标是冻结：

- 从 `controlled_trial_go` 到 trial “最小启用/最小观测/最小熔断/最小回退”的策略边界

本轮边界写死：

- 本轮只做 controlled trial minimal enablement plan（定义冻结）
- 不做真实 trial 启用
- 不做默认路径启用
- 不做真实 rollback / interrupt
- 不接地图、不驱动语音/记忆、不改路线、不做中台真实迁移
- 不改变现有主线行为与输出

---

## 2. 为什么现在必须先定义 minimal enablement plan（写死理由）

当前已经具备：

- controlled trial admission gate（准入准备态）
- controlled trial go/no-go gate（本次 trial 启动决策）
- shadow evaluation gate（shadow 证据）
- rollout plan（总体试运行策略）

但仍缺：

- 一份真正回答“trial go 之后如何最小启用”的战术文档（开哪些开关、仍必须关哪些、最小范围怎么切、异常怎么熔断与回退）

如果不先冻结 enablement plan，后续最容易把 `controlled_trial_go` 直接等同于“真实 trial 已能安全开启”。

因此必须先冻结 minimal enablement plan，再决定是否真正开启 trial。

---

## 3. 最小定义（写死）

`release_control first live guarded implementation minimal real-effect live implementation controlled trial minimal enablement plan` 是：

- 在 `controlled_trial_go` 之后，用于最小范围启用第一阶段真实 trial 的策略文档
- 只定义如何启用，不直接执行真实 trial

核心定义（写死一句）：

> controlled trial minimal enablement plan 只定义“第一阶段受控真实 trial 如何最小启用”，不直接执行 trial。

---

## 4. 最小启用前提（写死；少任一项不得启用）

以下必须全部满足（少任一项不得启用）：

- controlled trial go/no-go gate 为 go：  
  `controlled_trial_go_no_go_status == first_live_minimal_real_effect_controlled_trial_go`
- controlled trial admission gate 为 admitted：  
  `controlled_trial_status == first_live_minimal_real_effect_controlled_trial_admitted`
- shadow evaluation gate 为 go：  
  `shadow_eval_status == first_live_minimal_real_effect_shadow_eval_go`
- real-write go/no-go gate 仍为 go：  
  `real_write_status == first_live_minimal_real_effect_real_write_go`
- live code path dry-run == executed
- live implementation non-effect wiring == wired_ready
- live implementation dry-run execution == executed
- rollout plan 已冻结（在位）
- first real code activation definition 已冻结（在位）
- runtime activation stub / runtime implementation stub 在位
- activation / commit / pre-commit / launch / admission 全链路 admitted/ready
- `side_effects_released == false`
- **显式 controlled-trial enablement approval / signal 存在**
- **默认开关仍为 false**

并写死：

- 缺任一主前提，必须拒绝启用（不得尝试“补救式扩权”）

---

## 5. 最小启用范围（写死为极小范围）

这一节必须写死为极小范围：

- **单动作**：仅 `release_control`
- **单允许面**：仅三类真实副作用：
  - `execution_state_real_write`
  - `result_object_real_write`
  - `exception_or_failure_real_write`
- **单环境**：仅受控 trial 环境
- **单版本**：固定版本（不可漂移）
- **单链路**：仅此 minimal real-effect live implementation 链
- **默认不开**：必须显式批准；不得进入任何真实默认路径

---

## 6. 最小观测面（写死；必须观测）

试运行必须观测至少包括：

- `side_effects_released` 是否被错误打开或未恢复
- state 写入成功率
- result 写入成功率
- exception/failure 收口率
- trial 中 blocked/fail/recover 比例（以标准对象统计）
- 写入顺序是否正确（state → result → exception/failure closure）
- 是否触碰禁止面（route/voice/memory/migration/rollback/interrupt/map/path side-effect source 等）
- 白盒可追踪性（能从标准对象追溯本次决策链与执行链）
- trial 后是否可立即回退（熔断与回退剧本可执行）

---

## 7. 最小成功判定（写死）

必须同时满足：

- 仅触达三类允许面
- 顺序正确
- 无越权副作用
- `side_effects_released` 在成功后恢复或确认回到 false
- failure path 未误触发
- 白盒可复盘

并强调（写死）：

- 成功不等于全量启用
- 成功不等于默认路径启用

---

## 8. 最小失败判定（写死）

任一触发即判失败并进入熔断/回退：

- 触碰任一禁止面
- 顺序错误
- `side_effects_released` 不能恢复为 false
- failure path 缺失或不可收口
- 写入失败后未按固定顺序收口
- 任一试图顺手做 rollback / interrupt / route / voice / memory / migration

---

## 9. 最小熔断与回退剧本（写死固定顺序）

发生失败或风险信号时，必须按固定顺序执行：

1. 立即停止 trial（撤销 enablement 信号 / 关 trial 开关）
2. 恢复 `side_effects_released=false`
3. 写失败/退出态 `execution_state`
4. 写失败 `result_object`
5. 写 `exception_or_failure`
6. 交还治理链

并明确（写死）：

- 熔断优先于任何补救
- 不允许失败后扩权补救
- 不允许保留半开启状态

---

## 10. 明确禁止（写死）

enablement plan 不允许放行：

- route change
- voice output
- memory write
- mid-platform real migration
- rollback
- interrupt
- map/path side-effect source
- 越过标准对象吐散字段
- 默认开启 side effects
- 默认开启 trial

---

## 11. 与现有链路关系（写清）

- 与 controlled trial go/no-go gate：gate 决定“本次能不能开始 trial”；enablement plan 定“允许开始之后如何最小启用”
- 与 rollout plan：rollout plan 定总体试运行策略；minimal enablement plan 定第一阶段最小启用战术
- 与真实最小写入代码：真实代码已存在；minimal enablement plan 不直接执行代码，只定义怎么最小启用它
- 与 shadow evaluation gate：shadow evaluation 是前置证据；enablement plan 是 trial 启动战术

---

## 12. 当前仍然不能做什么（写死）

- 不允许打开 `side_effects_released` 并进入任何默认路径
- 不允许真实默认启用
- 不允许 route / voice / memory / migration
- 不允许真实 rollback / interrupt
- 不允许把 enablement plan 当作 trial 已经开始

---

## 13. 当前不做（写死）

- 不做 trial 真实启用
- 不做默认路径开启
- 不做地图接入
- 不做语音/记忆联动
- 不做中台真实迁移

---

## 14. 下一步边界（写死）

- 本轮之后，下一步才考虑：
  - controlled trial minimal enablement implementation v0
- 再之后才考虑：
  - 第一阶段受控真实 trial 的最小启用实现
- 当前不直接启用真实写入

---

## 补充链接（只读）

- controlled trial first minimal real enablement definition v0：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_LIVE_IMPLEMENTATION_CONTROLLED_TRIAL_FIRST_MINIMAL_REAL_ENABLEMENT_DEFINITION_V0.md`

