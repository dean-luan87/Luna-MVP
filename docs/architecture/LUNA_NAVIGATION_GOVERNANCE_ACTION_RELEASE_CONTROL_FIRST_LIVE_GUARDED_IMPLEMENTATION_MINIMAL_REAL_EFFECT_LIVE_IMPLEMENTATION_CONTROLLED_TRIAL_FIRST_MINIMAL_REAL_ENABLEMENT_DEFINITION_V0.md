# Luna — Navigation Governance Action Release Control First Live Guarded Implementation Minimal Real-Effect Live Implementation Controlled Trial First Minimal Real Enablement Definition v0（trial 真正开始启用边界冻结）

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_LIVE_IMPLEMENTATION_CONTROLLED_TRIAL_FIRST_MINIMAL_REAL_ENABLEMENT_DEFINITION_V0.md`  
**性质**：Phase-Next-137：冻结“第一阶段受控真实 trial 真正开始启用”的严格边界定义（只定义、不落真实启用代码；不进默认路径；不改变主线行为）

---

## 1. 文档定位（写死）

这是第一版 controlled trial minimal enablement 的“真实启用开始”定义文档。当前目标是冻结：

- 从 `enablement dry-run == executed` 到“第一阶段受控真实 trial 真正开始启用”的边界

本轮边界写死：

- 本轮只做 first minimal real enablement definition（设计冻结）
- 不做真实 trial 启用代码
- 不做默认路径启用
- 不做真实 rollback / interrupt
- 不接地图、不驱动语音/记忆、不改路线、不做中台真实迁移
- 不改变现有主线行为与输出

---

## 2. 为什么现在必须先定义 first minimal real enablement（写死理由）

当前已经具备：

- controlled trial admission/go-no-go（决策链已闭合）
- controlled trial enablement implementation（运行时承接位）
- controlled trial enablement dry-run（runtime 零副作用演练）

但仍缺：

- 一个明确的定义去回答：“第一阶段受控真实 trial 什么时候才算真正开始”

如果不先定义，后续最容易把：

- `controlled_trial_go`
- `enablement ready`
- `enablement_dry_run_executed`
- “trial 已开始”

混为一体。

因此必须先冻结 first minimal real enablement definition，再考虑任何真实启用代码。

---

## 3. 最小定义（写死）

`release_control first live guarded implementation minimal real-effect live implementation controlled trial first minimal real enablement` 是：

- 从 `controlled trial enablement dry-run == executed` 到第一阶段受控真实 trial 真正进入启用态的**边界定义**
- 只定义真实启用开始的前提、进入条件、允许面与失败收口
- 不等于真实 trial 已成功完成，不等于默认路径开启

---

## 4. 最小合法输入（写死；只允许标准对象）

只允许消费（只读）：

- controlled trial go/no-go gate == go  
  `controlled_trial_go_no_go_status == first_live_minimal_real_effect_controlled_trial_go`
- controlled trial admission gate == admitted  
  `controlled_trial_status == first_live_minimal_real_effect_controlled_trial_admitted`
- shadow evaluation gate == go  
  `shadow_eval_status == first_live_minimal_real_effect_shadow_eval_go`
- real-write go/no-go gate == go  
  `real_write_status == first_live_minimal_real_effect_real_write_go`
- live code path dry-run == executed
- live implementation wiring == wired_ready
- live implementation dry-run execution == executed
- controlled trial minimal enablement implementation 在位
- controlled trial enablement dry-run == executed  
  `dry_run_status == first_live_minimal_real_effect_controlled_trial_enablement_dry_run_executed`
- rollout plan 已冻结
- first real code activation definition 已冻结
- runtime activation stub / runtime implementation stub 在位
- activation / commit / pre-commit / launch / admission 全链路 admitted/ready
- `side_effects_released == false`
- **显式 real-enable approval / signal 存在**
- **默认开关仍为 false**

并明确（写死）：

- 缺任一主前提，first minimal real enablement 不成立
- 禁止读取 `request_* / approved_* / raw metadata`

---

## 5. 最小状态集合（写死）

最小状态集合收敛为：

- `first_live_minimal_real_effect_controlled_trial_real_enablement_ready`
- `first_live_minimal_real_effect_controlled_trial_real_enablement_not_ready`
- `first_live_minimal_real_effect_controlled_trial_real_enablement_blocked`

并明确（写死）：

- `...real_enablement_ready` 只表示第一阶段受控真实 trial 已具备开始启用条件
- 不表示真实 trial 已完成
- 不表示默认路径已启用
- 不表示 `side_effects_released` 已长期开启

---

## 6. 最小允许面（写死）

未来真实启用开始后，最小允许触达的面（只允许三类）：

- `execution_state_real_write`
- `result_object_real_write`
- `exception_or_failure_real_write`

除此以外全部禁止。

---

## 7. 最小开始条件（写死）

只有在以下条件同时满足时，才允许“跨入真实 trial 启用开始”：

- `side_effects_released == false`
- 所有上游 gate / dry-run / rollout / approvals 均满足（见第 4 节）
- 显式 real-enable approval/signal 在位

并明确（写死）：

- 进入开始启用态不等于成功完成
- 一旦进入后，必须仍受 activation contract、first real code activation definition、live implementation definition 约束

---

## 8. 最小失败收口（写死固定顺序）

任一异常必须按固定顺序收口：

1) 先恢复 `side_effects_released=false`  
2) 再写失败/退出态 `execution_state`  
3) 再写失败 `result_object`  
4) 再写 `exception_or_failure`  
5) 再交还治理链

并明确（写死）：

- 不允许失败后扩权补救
- 不允许保留半开启状态

---

## 9. 明确禁止（写死）

first minimal real enablement definition 不允许放行：

- route change
- voice output
- memory write
- mid-platform real migration
- rollback
- interrupt
- map/path planning side-effect source
- 越过标准对象吐散字段
- 默认开启 `side_effects_released`
- 默认开启 trial

---

## 10. 与现有链路的关系（写清）

- 与 controlled trial go/no-go gate：gate 定“本次能不能开始 trial”；definition 定“trial 真正开始启用”的精确定义
- 与 controlled trial enablement implementation：implementation 定运行时承接位；definition 定启用起点边界
- 与 controlled trial enablement dry-run：dry-run 证明启用入口零副作用可走通；definition 定义何时真正跨入真实 trial 启用
- 与 rollout plan：rollout plan 定 trial 启动策略；definition 定 trial 启用起点边界

---

## 11. 当前仍然不能做什么（写死）

- 不允许现在就打开 `side_effects_released`
- 不允许真实 trial 启用
- 不允许默认路径启用
- 不允许真实 rollback / interrupt
- 不允许 route / voice / memory / migration
- 不允许把本定义文档当作真实 trial 已开始

---

## 12. 当前不做（写死）

- 不做真实启用代码
- 不做真实默认启用
- 不做地图接入
- 不做语音/记忆联动
- 不做中台真实迁移

---

## 13. 下一步边界（写死）

- 本轮之后，下一步才考虑：
  - controlled trial first minimal real enablement code v0
- 若进入代码，只允许最小实现，不允许扩面
- 当前不直接启用真实 trial

