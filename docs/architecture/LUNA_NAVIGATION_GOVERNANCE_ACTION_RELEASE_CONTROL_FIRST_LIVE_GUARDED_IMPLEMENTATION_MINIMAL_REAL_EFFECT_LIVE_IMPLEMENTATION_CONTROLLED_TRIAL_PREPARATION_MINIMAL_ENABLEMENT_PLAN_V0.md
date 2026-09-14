# Luna — Navigation Governance Action Release Control First Live Guarded Implementation Minimal Real-Effect Live Implementation Controlled Trial Preparation Minimal Enablement Plan v0（准备态最小启用方案冻结）

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_LIVE_IMPLEMENTATION_CONTROLLED_TRIAL_PREPARATION_MINIMAL_ENABLEMENT_PLAN_V0.md`  
**性质**：Phase-Next-148：在 `preparation go/no-go == go` 之后，冻结第一阶段真实 preparation 的最小启用战术（可最小启用但默认仍不开；只定义不执行）

---

## 1. 文档定位（写死）

这是第一版 controlled trial preparation 进入真实 preparation 的最小启用方案文档。当前目标是冻结：

- 从 `preparation go` 到“第一阶段真实 preparation 最小启用”的策略边界

本轮边界写死：

- 本轮只做 controlled trial preparation minimal enablement plan（策略文档）
- 不做真实 preparation 启用
- 不做默认路径启用
- 不做真实 rollback / interrupt
- 不接地图、不驱动语音/记忆、不改路线、不做中台真实迁移
- 不改变现有主线行为与输出

---

## 2. 为什么现在必须先定义 preparation minimal enablement plan（写死理由）

当前已经具备：

- preparation shadow evaluation gate（影子评估）
- preparation go/no-go gate（最终启动门）
- preparation real code（真实最小写入代码存在但未主链接入）

但仍缺：

- 一份真正回答“preparation go 之后如何最小启用、如何最小观测、如何最小熔断/回退”的战术文档

如果不先冻结 enablement plan，后续最容易把 `preparation_go` 直接等同于“真实 preparation 已经能安全开启”。

---

## 3. 最小定义（写死）

`release_control first live guarded implementation minimal real-effect live implementation controlled trial preparation minimal enablement plan` 是：

- 在 `preparation_go` 之后，用于最小范围启用第一阶段真实 preparation 的策略文档
- **只定义如何启用，不直接执行真实 preparation**

---

## 4. 最小启用前提（写死；缺一不可）

少任一项不得启用：

- `controlled_trial_preparation_go_no_go_status == first_live_minimal_real_effect_controlled_trial_preparation_go`
- `controlled_trial_preparation_shadow_eval_status == first_live_minimal_real_effect_controlled_trial_preparation_shadow_eval_go`
- `controlled_trial_preparation_status == first_live_minimal_real_effect_controlled_trial_preparation_admitted`
- `controlled_trial_preparation_dry_run_status == first_live_minimal_real_effect_controlled_trial_preparation_dry_run_executed`
- `controlled_trial_go_no_go_status == first_live_minimal_real_effect_controlled_trial_go`
- `controlled_trial_status == first_live_minimal_real_effect_controlled_trial_admitted`
- `real_write_go_no_go_status == first_live_minimal_real_effect_real_write_go`
- runtime activation stub / runtime implementation stub 在位
- `side_effects_released == false`（进入前必须为 false）
- **显式 preparation enablement approval / signal 在位**
- 默认开关仍为 false（显式启用、显式调用、显式回退）

---

## 5. 最小启用范围（写死为极小范围）

启用范围写死：

- **单动作**：仅 `release_control`
- **单允许面**：仅三类真实副作用（严格写死）
  - `execution_state_real_write`
  - `result_object_real_write`
  - `exception_or_failure_real_write`
- **单环境**：仅受控 preparation 环境（非默认）
- **单版本**：固定单版本
- **单链路**：固定单链路（显式入口，不扩散到其它调用面）
- **默认不开**：必须显式批准/信号

---

## 6. 最小观测面（必须观测）

至少必须观测并可白盒复盘：

- `side_effects_released` 是否被错误打开或未恢复到 false
- state 写入成功率
- result 写入成功率
- exception/failure 收口率（失败是否按固定顺序收口）
- preparation 中 blocked / failed / recovered 比例
- 执行顺序是否符合“state -> result -> recover(false)”与失败收口顺序
- 是否触碰禁止面（route/voice/memory/migration/rollback/interrupt/map/path）
- 是否可立即回退（无半开启状态）

---

## 7. 最小成功判定（写死）

满足以下全部才算“最小成功”：

- 只触达三类允许面
- 顺序正确
- 无越权副作用
- `side_effects_released` 在成功后恢复/确认回到 false
- failure path 未误触发/或触发可解释且收口完备
- 白盒可追踪/可复盘

并明确（写死）：

- 成功不等于全量启用
- 成功不等于默认路径启用

---

## 8. 最小失败判定（写死）

任一满足即判失败（必须熔断/回退）：

- 触碰任一禁止面
- 顺序错误
- `side_effects_released` 不能恢复为 false
- failure path 缺失或不可收口
- 写入失败后未按固定顺序收口
- 任一试图顺手做 rollback / interrupt / route / voice / memory / migration

---

## 9. 最小熔断与回退剧本（写死固定顺序）

固定顺序（必须写死）：

1) 立即停止 preparation（停止继续尝试；不扩权补救）  
2) 恢复/确认 `side_effects_released=false`  
3) 写失败/退出态 `execution_state`  
4) 写失败 `result_object`  
5) 写 `exception_or_failure`  
6) 交还治理链  

并明确（写死）：

- 熔断优先于任何补救
- 不允许失败后扩权补救
- 不允许保留半开启状态

---

## 10. 明确禁止（写死）

本 enablement plan 不允许放行：

- route change
- voice output
- memory write
- mid-platform real migration
- rollback
- interrupt
- map/path side-effect source
- 越过标准对象吐散字段
- 默认开启 side effects
- 默认开启 preparation
- 默认开启 trial

---

## 11. 与现有链路关系（写清）

- 与 preparation go/no-go gate：gate 定“本次能不能开始 preparation”；enablement plan 定“允许开始之后如何最小启用”
- 与 preparation shadow evaluation gate：shadow evaluation 是前置证据；enablement plan 是 preparation 启动战术
- 与真实 minimal preparation code：真实代码已存在；本 plan 不直接执行代码，只定义怎么最小启用它
- 与 controlled trial minimal enablement plan：后者更上游；本 plan 更下游、更接近真实 preparation 启动

---

## 12. 当前仍然不能做什么（写死）

- 不允许默认打开 `side_effects_released`
- 不允许真实默认启用
- 不允许 route / voice / memory / migration
- 不允许真实 rollback / interrupt
- 不允许把 enablement plan 当作 preparation 已经开始

---

## 13. 当前不做（写死）

- 不做 preparation 真实启用
- 不做默认路径开启
- 不做地图接入
- 不做语音/记忆联动
- 不做中台真实迁移

---

## 14. 下一步边界（写死）

- 本轮之后，下一步才考虑：
  - controlled trial preparation minimal enablement implementation（enablement runner 占位/最小实现）
- 再之后才考虑：
  - 第一阶段真实 preparation 的最小启用实现
- 当前不直接启用真实 preparation

