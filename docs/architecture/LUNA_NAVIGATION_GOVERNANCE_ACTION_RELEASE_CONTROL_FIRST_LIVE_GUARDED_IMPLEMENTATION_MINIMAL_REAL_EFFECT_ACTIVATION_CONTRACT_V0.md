# Luna — Navigation Governance Action Release Control First Live Guarded Implementation Minimal Real-Effect Activation Contract v0（side effects 受控激活合同：设计冻结）

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_ACTIVATION_CONTRACT_V0.md`  
**性质**：Phase-Next-109：冻结 `minimal real-effect` 在 `commit_dry_run_status == commit_ready` 之后、真实最小写入实现真正开始之前，`side_effects_released` **唯一允许如何受控打开**的 activation contract（只冻结合同，不落代码；可冻结、可回归）

基于（已具备）：
- commit gate（冻结 + 最小实现）
- commit dry-run（冻结 + 最小实现）
- pre-commit dry-run（冻结 + 最小实现）
- guarded launch gate / dry-run（冻结 + 最小实现）
- admission gate（冻结 + 最小实现）
- implementation definition / skeleton / wiring / implementation dry-run execution（冻结 + 最小实现）
- standard objects：`execution_state_v0` / `result_v0`

---

## A. 文档定位（写死）

这份文档是：

- `release_control first live guarded implementation minimal real-effect` 的 **activation contract** 设计冻结文档。
- 当前目标：冻结“从 commit dry-run 到未来真实最小写入实现内部，`side_effects_released` 如何唯一受控激活”的合同：由谁激活、激活前提、激活范围、失败收口规则、禁止面。

并且（本轮写死边界）：

- 当前不做真实代码实现（不落 activation gate / activation contract implementation）。
- 当前不做真实 `rollback` / `interrupt`。
- 当前不做地图接入、不改路线。
- 当前不做语音/记忆联动。
- 当前不做中台真实迁移。
- 当前不改变现有主线行为。

---

## B. 为什么现在必须先定义 activation contract（写死理由）

- 当前已经有 commit gate implementation。
- 当前已经有 commit dry-run implementation。
- 但还没有一份明确的“`side_effects_released` 何时允许打开、由谁打开、打开后最小允许哪些真实副作用、失败时如何立即关闭”的合同。
- 如果不先定义 activation contract，后续真实实现最容易失控的点就是 `side_effects_released` 的打开条件与扩权滑坡。

因此必须先冻结 activation contract，再考虑是否真的进入第一版真实最小写入实现。

---

## C. activation contract 的最小定义（写死）

`release_control first live guarded implementation minimal real-effect activation contract` 是：

- commit dry-run 之后、真实第一版最小写入实现内部，**唯一允许讨论** `side_effects_released` 从 `false` 进入受控激活的合同。
- 只定义：激活条件、激活范围、失败收口规则。

它不是：

- commit gate 本身
- commit dry-run 本身
- implementation definition / plan 本身
- 真实执行器本身
- rollback / interrupt 合同

核心定义（写死一句）：

> activation contract 只定义 `side_effects_released` 的唯一受控激活规则，不直接执行任何真实写入实现。

---

## D. 最小合法输入（写死；只允许标准化对象）

activation contract 只允许消费（只读）：

1) `first_live_guarded_implementation_minimal_real_effect_admission_gate_v0`  
   - 必须 `admission_status == "first_live_minimal_real_effect_admitted"`
2) `first_live_guarded_implementation_minimal_real_effect_guarded_launch_gate_v0`  
   - 必须 `launch_admission_status == "first_live_minimal_real_effect_launch_admitted"`
3) `first_live_guarded_implementation_minimal_real_effect_pre_commit_dry_run_v0`  
   - 必须 `pre_commit_status == "first_live_minimal_real_effect_pre_commit_ready"`
4) `first_live_guarded_implementation_minimal_real_effect_commit_gate_v0`  
   - 必须 `commit_admission_status == "first_live_minimal_real_effect_commit_admitted"`
5) `first_live_guarded_implementation_minimal_real_effect_commit_dry_run_v0`  
   - 必须 `commit_dry_run_status == "first_live_minimal_real_effect_commit_ready"`
6) `first_live_enablement_approval_gate_v0`  
   - 必须 approved
7) `first_live_launch_dry_run_v0`  
   - 必须 ready
8) `live_release_gate_v0`  
   - 必须 ready
9) `side_effect_release_gate_v0`  
   - 必须 ready
10) `first_live_guarded_implementation_dry_effect_simulation_v0`  
   - 必须 simulated
11) `first_live_guarded_implementation_minimal_real_effect_implementation_dry_run_execution_v0`  
   - 必须 executed
12) `execution_state_v0` 与 `result_v0`  
   - 回传面在位
13) `side_effects_released`  
   - 激活前必须仍为 `false`
14) 明确的 activation 主体 / activation signal（语义在位）  
   - 必须存在
   - 当前只做语义定义，不实现来源机制
15) implementation skeleton identity / capability  
   - 本体在位且仍为保守边界依据

并明确（写死）：

- 缺任一主前提，activation contract 不成立。
- 禁止直接读取 `request_* / approved_* / raw metadata`。

---

## E. 最小结果集合（写死；三态）

activation contract 的结果必须收敛成最小集合：

- `first_live_minimal_real_effect_activation_ready`
- `first_live_minimal_real_effect_activation_not_ready`
- `first_live_minimal_real_effect_activation_blocked`

语义（写死）：

1) `first_live_minimal_real_effect_activation_ready`
- 仅表示：未来真实最小写入实现已具备受控激活 `side_effects_released` 的合同前提
- 不表示真实写入已发生
- 不表示副作用已发生
- 不表示 `side_effects_released == true`

2) `first_live_minimal_real_effect_activation_not_ready`
- 当前 activation 前提或 activation signal 缺失
- 不允许进入受控激活

3) `first_live_minimal_real_effect_activation_blocked`
- 当前存在硬阻断 / 身份问题 / 一致性问题
- 明确不允许进入受控激活

---

## F. 最小允许激活后的范围（写死；极克制）

即使未来 activation contract 成立，激活后也只允许这三类真实副作用：

1) `execution_state_real_write`
2) `result_object_real_write`
3) `exception_or_failure_real_write`

除此以外一律禁止。

---

## G. 激活后的最小顺序（写死）

### 正常路径（写死）

1) 激活前确认仍为 `side_effects_released=false`
2) 进入未来受控激活态（语义：允许最小 real-write）
3) 真实写 `execution_state`
4) 真实写 `result_object`
5) 交还治理链

### 异常路径（写死）

1) 立即恢复 `side_effects_released=false`
2) 真实写 `execution_state`（失败/退出态）
3) 真实写 `result_object`（失败结果）
4) 真实写 `exception_or_failure`
5) 交还治理链

并明确（写死）：

- 不允许先写 result 后写 state
- 不允许先做 route/voice/memory/migration 再补写对象
- 不允许失败后保留半开启的 side effect 状态

---

## H. 明确禁止（写死）

activation contract 不允许直接定义或放行：

- route change
- voice output
- memory write
- mid-platform real migration
- rollback
- interrupt
- map/path planning side-effect source
- 越过标准对象吐散字段

---

## I. 与现有链路的关系（写清；不能混用）

与 commit gate：

- commit gate 负责最终 commit 放行
- activation contract 负责 commit 之后，未来真实实现中 side effects 如何唯一受控激活
- `commit_admitted != activation_ready`

与 commit dry-run：

- commit dry-run 负责最后一次零副作用 commit 级演练
- activation contract 负责定义未来真实实现中 side effects 的唯一激活合同
- `commit_ready != activation_ready`

与 implementation definition / plan：

- definition 定边界
- plan 定真实写入策略
- activation contract 只做“`side_effects_released` 如何唯一受控激活”
- 不替代 definition / plan

---

## J. 当前仍然不能做什么（写死）

- 不允许现在就把 `side_effects_released` 打开
- 不允许真实写入
- 不允许真实 `release_control`
- 不允许真实 `rollback` / `interrupt`
- 不允许 route / voice / memory / migration
- 不允许把 `first_live_minimal_real_effect_activation_ready` 当作真实写入已发生

---

## K. 当前不做（写死）

- 不做 activation contract 代码实现
- 不做真实最小写入实现
- 不做地图接入
- 不做语音/记忆联动
- 不做中台真实迁移

---

## L. 下一步边界（写死）

- 本轮之后，下一步才考虑：
  - Phase-Next-110：Minimal Real-Effect Activation Gate v0（side effects 受控激活判断门：设计冻结）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_ACTIVATION_GATE_V0.md`
  - Phase-Next-112：Minimal Real-Effect Activation Dry-Run v0（最终 activation 级零副作用演练层：设计冻结）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_ACTIVATION_DRY_RUN_V0.md`
  - 或 minimal real-effect activation contract 的 minimal implementation
- 再之后才考虑：
  - 第一版最小真实写入实现方案
- 当前不直接落真实实现

---

## M. 未来样例（仅说明，不落代码）

```json
{
  "release_control_first_live_guarded_implementation_minimal_real_effect_activation_contract_scope": "navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_activation_contract_v0",
  "activation_status": "first_live_minimal_real_effect_activation_ready|first_live_minimal_real_effect_activation_not_ready|first_live_minimal_real_effect_activation_blocked",
  "side_effects_released": false,
  "allowed_real_effects": [
    "execution_state_real_write",
    "result_object_real_write",
    "exception_or_failure_real_write"
  ],
  "reason": "..."
}
```

