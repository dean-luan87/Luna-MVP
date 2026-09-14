# Luna — Navigation Governance Action Release Control First Live Guarded Implementation Minimal Real-Effect Pre-Commit Dry-Run v0（最后预提交干跑层：设计冻结）

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_PRE_COMMIT_DRY_RUN_V0.md`  
**性质**：Phase-Next-104：冻结 `minimal real-effect` 在 `guarded launch gate == launch_admitted` 之后、真实最小写入实现之前的 **最后预提交干跑层（pre-commit dry-run）**（只预演、不真实写入；可冻结、可回归）

基于（已具备）：
- implementation definition / skeleton / implementation dry-run execution（已具备）
- admission gate（已具备设计冻结 + 最小实现）
- guarded launch dry-run（已具备设计冻结 + 最小实现）
- guarded launch gate（已具备设计冻结 + 最小实现）
- gates / simulation / wiring（已具备）
- standard objects：`execution_state_v0` / `result_v0`

---

## A. 文档定位（写死）

这份文档是：

- `release_control first live guarded implementation minimal real-effect` 的**最终预提交干跑层（pre-commit dry-run）**设计文档。
- 当前目标：冻结“从 guarded launch gate 到第一版真实最小写入实现”的最后预提交边界：谁来做最后顺序预演、预演前必须满足什么、预演结果是什么、预演本身不能做什么。

并且（本轮写死边界）：

- 当前不做 pre-commit dry-run 代码实现。
- 当前不做真实最小写入实现（不落真实 real-effect implementation）。
- 当前不做真实 `rollback` / `interrupt`。
- 当前不做地图接入、不改路线。
- 当前不做语音/记忆联动。
- 当前不做中台真实迁移。
- 当前不改变现有主线行为。
- 当前 `side_effects_released` 仍强制锁死为 `false`（不允许打开）。

---

## B. 为什么现在必须先定义 pre-commit dry-run（写死理由）

- 当前已经有 minimal real-effect admission gate implementation。
- 当前已经有 guarded launch dry-run implementation。
- 当前已经有 guarded launch gate implementation（可结构化产出 launch_admitted/not_admitted/blocked）。
- 但还没有一个明确的“最终放行之后、真实写入前最后一次预演”的层。
- 如果不先定义 pre-commit dry-run，后续很容易把 `launch_admitted` 误当成“可以直接进入真实写入”。

因此必须先冻结最后预提交干跑层，再考虑是否真的进入第一版最小真实写入实现。

---

## C. pre-commit dry-run 的最小定义（写死）

`release_control first live guarded implementation minimal real-effect pre-commit dry-run` 是：

- guarded launch gate 之后、真实第一版最小写入实现之前的最后预提交干跑层
- 只负责判断“是否具备进入真实最小写入实现前的最后顺序预演条件”

它不是：

- guarded launch gate 本身
- implementation dry-run execution 本身
- 真实执行器本身
- `rollback` / `interrupt` 预处理层

核心定义（写死一句）：

> pre-commit dry-run 只决定“是否具备进入真实最小写入实现前的最后预提交条件”，不直接执行任何真实动作，也不直接打开 `side_effects_released`。

---

## D. 最小合法输入（写死；只允许标准化对象）

pre-commit dry-run 只允许消费（只读）：

1) `first_live_guarded_implementation_minimal_real_effect_admission_gate_v0`
   - 必须 `admission_status == "first_live_minimal_real_effect_admitted"`
2) `first_live_guarded_implementation_minimal_real_effect_guarded_launch_gate_v0`
   - 必须 `launch_admission_status == "first_live_minimal_real_effect_launch_admitted"`
3) `first_live_enablement_approval_gate_v0`
   - 必须 `approval_status == "first_live_enablement_approved"`
4) `first_live_launch_dry_run_v0`
   - 必须 `launch_status == "first_live_launch_dry_run_ready"`
5) `live_release_gate_v0`
   - 必须 `live_release_status == "live_release_ready"`
6) `side_effect_release_gate_v0`
   - 必须 `side_effect_release_status == "side_effect_release_ready"`
7) `first_live_guarded_implementation_dry_effect_simulation_v0`
   - 必须 `simulation_status == "first_live_guarded_dry_effect_simulated"`
8) `first_live_guarded_implementation_minimal_real_effect_implementation_dry_run_execution_v0`
   - 必须 `execution_status == "first_live_minimal_real_effect_implementation_dry_run_executed"`
9) `execution_state_v0` 与 `result_v0`
   - 回传面在位
10) `side_effects_released`
   - 必须仍为 `false`
11) implementation skeleton identity / capability
   - 本体在位且仍为保守模式

并明确（写死）：

- 缺任一主前提，pre-commit dry-run 不成立。
- 禁止直接读取 `request_* / approved_* / raw metadata`。

---

## E. 最小结果集合（写死；三态）

pre-commit dry-run 的结果必须收敛成最小集合：

- `first_live_minimal_real_effect_pre_commit_ready`
- `first_live_minimal_real_effect_pre_commit_not_ready`
- `first_live_minimal_real_effect_pre_commit_blocked`

语义（写死）：

1) `first_live_minimal_real_effect_pre_commit_ready`
- 仅表示：已具备进入真实最小写入实现前的最后预提交条件
- 不表示真实写入已经发生
- 不表示副作用已经发生
- 不表示 `side_effects_released` 已经变成 `true`

2) `first_live_minimal_real_effect_pre_commit_not_ready`
- 当前前提条件缺失或尚未满足
- 不允许进入真实最小写入实现

3) `first_live_minimal_real_effect_pre_commit_blocked`
- 当前存在硬阻断 / 身份问题 / 一致性问题
- 明确不允许进入真实最小写入实现

---

## F. 明确禁止（写死）

pre-commit dry-run 不允许直接：

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

与 guarded launch gate：

- guarded launch gate 负责最终放行
- pre-commit dry-run 负责放行后的最后顺序预演条件检查
- `launch_admitted != pre_commit_ready`

与 implementation dry-run execution：

- implementation dry-run execution 负责真实实现层的零副作用顺序演练
- pre-commit dry-run 负责进入真实最小写入前的最后总检查
- 两者不能混用

与 implementation definition / plan：

- definition 定边界
- plan 定真实写入策略
- pre-commit dry-run 只做“进入真实写入前的最后预提交检查”
- 不替代 definition / plan

---

## H. 当前仍然不能做什么（写死）

- 不允许现在就把 `side_effects_released` 打开
- 不允许真实写入
- 不允许真实 `release_control`
- 不允许真实 `rollback` / `interrupt`
- 不允许 route / voice / memory / migration
- 不允许把 `first_live_minimal_real_effect_pre_commit_ready` 当作真实写入已发生

---

## I. 当前不做（写死）

- 不做 pre-commit dry-run 代码实现
- 不做真实最小写入实现
- 不做地图接入
- 不做语音/记忆联动
- 不做中台真实迁移

---

## J. 下一步边界（写死）

- 本轮之后，下一步才考虑：
  - minimal real-effect pre-commit dry-run 的 minimal implementation
- 再之后才考虑：
  - 第一版最小真实写入实现方案
- 当前不直接落真实实现

补充链接（最终 commit 放行门：设计冻结）：

- Phase-Next-106：Minimal Real-Effect Commit Gate v0：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_COMMIT_GATE_V0.md`

---

## K. 未来样例（仅说明，不落代码）

```json
{
  "release_control_first_live_guarded_implementation_minimal_real_effect_pre_commit_dry_run_scope": "navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_pre_commit_dry_run_v0",
  "pre_commit_status": "first_live_minimal_real_effect_pre_commit_ready|first_live_minimal_real_effect_pre_commit_not_ready|first_live_minimal_real_effect_pre_commit_blocked",
  "side_effects_released": false,
  "reason": "..."
}
```

