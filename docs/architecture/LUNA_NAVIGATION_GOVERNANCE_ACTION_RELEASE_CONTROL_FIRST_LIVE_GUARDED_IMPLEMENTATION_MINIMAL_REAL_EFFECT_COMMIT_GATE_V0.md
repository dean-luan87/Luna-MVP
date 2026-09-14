# Luna — Navigation Governance Action Release Control First Live Guarded Implementation Minimal Real-Effect Commit Gate v0（最终 Commit 放行门：设计冻结）

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_COMMIT_GATE_V0.md`  
**性质**：Phase-Next-106：冻结 `minimal real-effect` 在 `pre_commit_status == pre_commit_ready` 之后、真实最小写入实现之前的 **最终 commit 放行门（commit gate）**（只放行、不执行；可冻结、可回归）

基于（已具备）：
- implementation definition / skeleton / implementation dry-run execution（已具备）
- admission gate（已具备设计冻结 + 最小实现）
- guarded launch gate（已具备设计冻结 + 最小实现）
- pre-commit dry-run（已具备设计冻结 + 最小实现）
- gates / simulation / wiring（已具备）
- standard objects：`execution_state_v0` / `result_v0`

---

## A. 文档定位（写死）

这份文档是：

- `release_control first live guarded implementation minimal real-effect` 的**最终 commit 放行门（commit gate）**设计文档。
- 当前目标：冻结“从 pre-commit dry-run 到第一版真实最小写入实现”的最后 commit 边界：谁来最终 commit 放行、放行前必须满足什么、放行结果是什么、commit gate 本身不能做什么。

并且（本轮写死边界）：

- 当前不做 commit gate 代码实现。
- 当前不做真实最小写入实现（不落真实 real-effect implementation）。
- 当前不做真实 `rollback` / `interrupt`。
- 当前不做地图接入、不改路线。
- 当前不做语音/记忆联动。
- 当前不做中台真实迁移。
- 当前不改变现有主线行为。
- 当前 `side_effects_released` 仍强制锁死为 `false`（不允许打开）。

---

## B. 为什么现在必须先定义 commit gate（写死理由）

- 当前已经有 minimal real-effect admission gate implementation。
- 当前已经有 guarded launch gate implementation。
- 当前已经有 pre-commit dry-run implementation（可结构化产出 pre_commit_ready/not_ready/blocked）。
- 但还没有一个明确的“谁来最终 commit 放行第一版最小真实写入实现”的门。
- 如果不先定义 commit gate，后续很容易把 `pre_commit_ready` 误当成“可以直接进入真实写入”。

因此必须先冻结最终 commit 放行门，再考虑是否真的进入第一版最小真实写入实现。

---

## C. commit gate 的最小定义（写死）

`release_control first live guarded implementation minimal real-effect commit gate` 是：

- pre-commit dry-run 之后、真实第一版最小写入实现之前的最终 commit 放行门
- 只负责判断“是否 commit 放行第一版最小真实写入实现”

它不是：

- pre-commit dry-run 本身
- guarded launch gate 本身
- implementation definition / plan 本身
- 真实执行器本身
- rollback / interrupt commit 门

核心定义（写死一句）：

> commit gate 只决定“是否 commit 放行第一版最小真实写入实现”，不直接执行任何动作，也不直接打开 `side_effects_released`。

---

## D. 最小合法输入（写死；只允许标准化对象）

commit gate 只允许消费（只读）：

1) `first_live_guarded_implementation_minimal_real_effect_admission_gate_v0`
   - 必须 `admission_status == "first_live_minimal_real_effect_admitted"`
2) `first_live_guarded_implementation_minimal_real_effect_guarded_launch_gate_v0`
   - 必须 `launch_admission_status == "first_live_minimal_real_effect_launch_admitted"`
3) `first_live_guarded_implementation_minimal_real_effect_pre_commit_dry_run_v0`
   - 必须 `pre_commit_status == "first_live_minimal_real_effect_pre_commit_ready"`
4) `first_live_enablement_approval_gate_v0`
   - 必须 `approval_status == "first_live_enablement_approved"`
5) `first_live_launch_dry_run_v0`
   - 必须 `launch_status == "first_live_launch_dry_run_ready"`
6) `live_release_gate_v0`
   - 必须 `live_release_status == "live_release_ready"`
7) `side_effect_release_gate_v0`
   - 必须 `side_effect_release_status == "side_effect_release_ready"`
8) `first_live_guarded_implementation_dry_effect_simulation_v0`
   - 必须 `simulation_status == "first_live_guarded_dry_effect_simulated"`
9) `first_live_guarded_implementation_minimal_real_effect_implementation_dry_run_execution_v0`
   - 必须 `execution_status == "first_live_minimal_real_effect_implementation_dry_run_executed"`
10) `execution_state_v0` 与 `result_v0`
   - 回传面在位
11) `side_effects_released`
   - 必须仍为 `false`
12) 明确的 commit 主体 / commit 信号（语义在位）
   - 必须存在
   - 当前只做语义定义，不实现来源机制
13) implementation skeleton identity / capability
   - 本体在位与能力边界依据（必须保守、不可越权）

并明确（写死）：

- 缺任一主前提，commit gate 不成立。
- 禁止直接读取 `request_* / approved_* / raw metadata`。

---

## E. 最小结果集合（写死；三态）

commit gate 的结果必须收敛成最小集合：

- `first_live_minimal_real_effect_commit_admitted`
- `first_live_minimal_real_effect_commit_not_admitted`
- `first_live_minimal_real_effect_commit_blocked`

语义（写死）：

1) `first_live_minimal_real_effect_commit_admitted`
- 仅表示：允许进入第一版最小真实写入实现
- 不表示真实写入已经发生
- 不表示副作用已经发生
- 不表示 `side_effects_released` 已经变成 `true`

2) `first_live_minimal_real_effect_commit_not_admitted`
- 当前 commit 信号缺失或条件未满足
- 不允许进入真实最小写入实现

3) `first_live_minimal_real_effect_commit_blocked`
- 当前存在硬阻断 / 身份问题 / 一致性问题
- 明确不允许进入真实最小写入实现

---

## F. 明确禁止（写死）

commit gate 不允许直接：

- 打开 `side_effects_released`
- 执行真实 `release_control`
- 执行真实写入
- 改路线
- 触发语音播报
- 写记忆
- 触发中台真实迁移
- 自动触发 `rollback` / `interrupt`
- 越过标准对象吐散字段

---

## G. 与现有链路的关系（写清；不能混用）

与 pre-commit dry-run：

- pre-commit dry-run 负责最终放行前的最后预提交检查
- commit gate 负责最终 commit 放行是否进入真实最小写入实现
- `pre_commit_ready != commit_admitted`

与 guarded launch gate：

- guarded launch gate 负责发车后最终放行
- commit gate 负责进入真实最小写入实现前的最终 commit 决策
- `launch_admitted != commit_admitted`

与 implementation definition / plan：

- definition 定边界
- plan 定真实写入策略
- commit gate 只做“是否 commit 放行这一层”
- 不替代 definition / plan

---

## H. 当前仍然不能做什么（写死）

- 不允许现在就把 `side_effects_released` 打开
- 不允许真实写入
- 不允许真实 `release_control`
- 不允许真实 `rollback` / `interrupt`
- 不允许 route / voice / memory / migration
- 不允许把 `first_live_minimal_real_effect_commit_admitted` 当作真实写入已发生

---

## I. 当前不做（写死）

- 不做 commit gate 代码实现
- 不做真实最小写入实现
- 不做地图接入
- 不做语音/记忆联动
- 不做中台真实迁移

---

## J. 下一步边界（写死）

- 本轮之后，下一步才考虑：
  - minimal real-effect commit gate 的 minimal implementation
- 补充链接：
  - Phase-Next-109：Minimal Real-Effect Activation Contract v0（side effects 受控激活合同：设计冻结）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_ACTIVATION_CONTRACT_V0.md`
- 再之后才考虑：
  - 第一版最小真实写入实现方案
- 当前不直接落真实实现

---

## K. 未来样例（仅说明，不落代码）

```json
{
  "release_control_first_live_guarded_implementation_minimal_real_effect_commit_gate_scope": "navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_commit_gate_v0",
  "commit_admission_status": "first_live_minimal_real_effect_commit_admitted|first_live_minimal_real_effect_commit_not_admitted|first_live_minimal_real_effect_commit_blocked",
  "side_effects_released": false,
  "reason": "..."
}
```

