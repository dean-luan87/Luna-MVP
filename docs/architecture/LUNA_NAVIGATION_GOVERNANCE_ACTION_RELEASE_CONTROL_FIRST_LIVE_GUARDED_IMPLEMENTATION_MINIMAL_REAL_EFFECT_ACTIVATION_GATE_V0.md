# Luna — Navigation Governance Action Release Control First Live Guarded Implementation Minimal Real-Effect Activation Gate v0（side effects 受控激活门：设计冻结）

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_ACTIVATION_GATE_V0.md`  
**性质**：Phase-Next-110：把 activation contract 从“规则文档”推进为“判断门定义”，冻结 `minimal real-effect` 在未来 side effects 受控激活之前的 **activation gate**（只定义 gate，不落代码；可冻结、可回归）

基于（已具备）：
- activation contract（冻结）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_ACTIVATION_CONTRACT_V0.md`
- commit gate implementation（已具备）
- commit dry-run implementation（已具备）
- pre-commit / launch / admission 链路（冻结 + 最小实现）
- implementation definition / skeleton / wiring / implementation dry-run execution（冻结 + 最小实现）

---

## 1. 文档定位（写死）

这份文档是：

- `release_control first live guarded implementation minimal real-effect` 的 **activation gate** 设计冻结文档。
- 当前目标：冻结“从 activation contract 到未来 side effects 受控激活”的 gate 边界：谁来判断、输入是什么、输出是什么、gate 不能做什么。

并且（本轮写死边界）：

- 当前不做真实代码实现（不落 activation gate minimal implementation）。
- 当前不做真实 `rollback` / `interrupt`。
- 当前不做地图接入、不改路线。
- 当前不做语音/记忆联动。
- 当前不做中台真实迁移。
- 当前不改变现有主线行为。
- 当前 `side_effects_released` 仍强制锁死为 `false`（不允许打开）。

---

## 2. 为什么现在必须先定义 activation gate（写死理由）

- 当前已经有 activation contract（只定义规则）。
- activation contract 不是判断对象；如果不先定义 activation gate，后续很容易把“activation_ready 判断逻辑”揉进真实最小写入实现，导致 `side_effects_released` 的打开判断被实现层直接消费而失控。

因此必须先冻结 activation gate，再考虑其最小实现或任何真实实现。

---

## 3. activation gate 的最小定义（写死）

`release_control first live guarded implementation minimal real-effect activation gate` 是：

- activation contract 之后、未来 side effects 受控激活之前的统一判断门
- 只负责判断“是否允许进入 side effects 受控激活”

它不是：

- activation contract 本身
- commit gate 本身
- 真实执行器本身
- rollback / interrupt 激活门

核心定义（写死一句）：

> activation gate 只决定“是否允许进入 side effects 受控激活”，不直接执行任何真实写入，也不直接把 `side_effects_released` 改成 `true`。

---

## 4. 最小合法输入（写死；只允许标准化对象）

activation gate 只允许消费（只读）：

- admission gate == admitted
- guarded launch gate == launch_admitted
- pre-commit dry-run == pre_commit_ready
- commit gate == commit_admitted
- commit dry-run == commit_ready
- approval / launch / live release / side-effect release 全部 ready/approved
- dry-effect simulation == simulated
- implementation dry-run execution == executed
- execution_state_v0 / result_v0 在位
- side_effects_released == false
- activation signal（语义在位，不实现来源机制）
- implementation skeleton identity / capability 在位且保守

并写死：

- 缺任一主前提，activation gate 不成立。
- 禁止直接读取 `request_* / approved_* / raw metadata`。

---

## 5. 最小结果集合（写死；三态 gate）

activation gate 的结果必须收敛成最小集合：

- `first_live_minimal_real_effect_activation_admitted`
- `first_live_minimal_real_effect_activation_not_admitted`
- `first_live_minimal_real_effect_activation_blocked`

并明确语义（写死）：

- `activation_admitted`：仅表示未来真实实现已被允许进入 side effects 受控激活前状态  
  不表示真实写入已发生、不表示副作用已发生、不表示 `side_effects_released == true`
- `activation_not_admitted`：当前 activation 前提或 activation signal 缺失/未满足，不允许进入受控激活
- `activation_blocked`：硬阻断 / 身份问题 / 一致性问题（保守阻断）

---

## 6. 明确禁止（写死）

activation gate 不允许直接：

- 打开 `side_effects_released`
- 执行真实写入
- 执行真实 `release_control`
- 改路线
- 触发语音播报
- 写记忆
- 触发中台真实迁移
- 自动触发 `rollback` / `interrupt`
- 越过标准对象吐散字段

---

## 7. 与现有链路的关系（写清；不能混用）

与 activation contract：

- contract 定义规则
- activation gate 负责统一判断规则是否成立
- 两者不能混用

与 commit gate / commit dry-run：

- commit gate 与 commit dry-run 负责真实写入前最后放行与最后干跑
- activation gate 负责 side effects 受控激活前的判断门
- `commit_ready != activation_admitted`

与 implementation definition / plan：

- definition 定边界
- plan 定真实写入策略
- activation gate 只做“是否允许进入受控激活”
- 不替代 definition / plan

---

## 8. 当前仍然不能做什么（写死）

- 不允许现在就把 `side_effects_released` 打开
- 不允许真实写入
- 不允许真实 `release_control`
- 不允许真实 `rollback` / `interrupt`
- 不允许 route / voice / memory / migration
- 不允许把 `activation_admitted` 当作真实写入已发生

---

## 9. 当前不做（写死）

- 不做 activation gate 代码实现
- 不做真实最小写入实现
- 不做地图接入
- 不做语音/记忆联动
- 不做中台真实迁移

---

## 10. 下一步边界（写死）

- 本轮之后，下一步才考虑：
  - minimal real-effect activation gate 的 minimal implementation
- 补充链接：
  - Phase-Next-112：Minimal Real-Effect Activation Dry-Run v0（最终 activation 级零副作用演练层：设计冻结）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_ACTIVATION_DRY_RUN_V0.md`
- 再之后才考虑：
  - 第一版真实最小写入实现方案
- 当前不直接落真实实现

