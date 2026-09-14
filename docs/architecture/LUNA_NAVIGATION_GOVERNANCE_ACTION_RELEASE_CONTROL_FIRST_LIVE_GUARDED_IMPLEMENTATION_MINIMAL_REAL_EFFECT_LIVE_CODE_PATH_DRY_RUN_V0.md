# Luna — Navigation Governance Action Release Control First Live Guarded Implementation Minimal Real-Effect Live Code Path Dry-Run v0（真实代码路径：零副作用干跑冻结）

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_LIVE_CODE_PATH_DRY_RUN_V0.md`  
**性质**：Phase-Next-125：冻结第一版真实代码壳子（minimal code skeleton）在进入真实写入前的**最后一次代码路径级零副作用演练层**（只干跑、不真实写入；不接入 dispatcher；可冻结、可回归）

基于（已具备）：
- live implementation definition / skeleton / stub（冻结 + 在位）
- live implementation minimal code skeleton（在位）
- live implementation non-effect wiring（在位）
- live implementation dry-run execution（在位）
- live runtime activation stub（在位）
- first real write rollout plan（冻结）
- real-write go/no-go gate（冻结）
- activation / commit / pre-commit / launch / admission 全链路对象（在位）
- 当前 `side_effects_released` 仍强制锁死为 `false`

---

## A. 文档定位（写死）

这是第一版 live implementation minimal code skeleton 的**代码路径级 dry-run**设计文档。当前目标是冻结“从 real-write go/no-go gate 到未来真实最小写入代码真正执行前”的最后代码路径演练边界。当前不做真实实现、不做真实 rollout、不做 rollback/interrupt、不做地图/语音/记忆/中台迁移、不改变现有主线行为。

---

## B. 为什么现在必须先做 live code path dry-run（写死理由）

- minimal code skeleton 已存在。
- go/no-go gate 已存在。
- 但还没有一个对象明确回答：**未来真实代码壳子的调用顺序是否已经零副作用走通**，以及 **recover_side_effects_false_placeholder 是否被纳入固定顺序**。
- 如果不先做 code path dry-run，后续最容易从 `real_write_go` 直接跳进真实代码，缺少最后一次代码路径级演练。

---

## C. 最小定义（写死）

`release_control first live guarded implementation minimal real-effect live code path dry-run` 是：

- future real minimal write code body 进入真实执行前的最后**代码路径级零副作用演练层**
- 只负责判断代码路径固定顺序是否可走通
- 不执行任何真实写入

---

## D. 最小合法输入（写死；只允许标准化对象）

只允许消费（只读）：

- live implementation definition 已冻结
- live implementation skeleton 已存在
- live implementation stub 已存在
- live implementation minimal code skeleton 已存在
- live implementation admission & acceptance 条件全部满足
- live implementation minimal implementation plan 已冻结
- live implementation non-effect wiring == `first_live_minimal_real_effect_live_wired_ready`
- live implementation dry-run execution == `first_live_minimal_real_effect_live_dry_run_executed`
- live runtime activation stub 已存在
- first real write rollout plan 已冻结
- real-write go/no-go gate == `first_live_minimal_real_effect_real_write_go`
- activation / commit / pre-commit / launch / admission 全链路 admitted/ready
- execution_state / result / exception_or_failure path 在位
- `side_effects_released == false`

并写死：

- 缺任一主前提，code path dry-run 不成立
- 禁止读取 `request_* / approved_* / raw metadata`

---

## E. 最小结果集合（写死；三态）

必须收敛为三态之一：

- `first_live_minimal_real_effect_live_code_path_dry_run_executed`
- `first_live_minimal_real_effect_live_code_path_dry_run_not_ready`
- `first_live_minimal_real_effect_live_code_path_dry_run_blocked`

并明确（写死）：

- `executed` 只表示未来真实代码路径已经能零副作用走通
- 不表示真实写入已发生
- 不表示 `side_effects_released` 已打开
- 不表示真实 rollout 已开启

---

## F. 最小演练顺序（写死）

代码路径级固定顺序（不得倒序、不得跳步）：

1) `accept_first_live_minimal_real_effect_live_code_input`  
2) `perform_first_live_execution_state_real_write_placeholder`  
3) `perform_first_live_result_object_real_write_placeholder`  
4) `perform_first_live_exception_or_failure_real_write_placeholder`  
5) `perform_first_live_recover_side_effects_false_placeholder`  

并写死：

- 不得夹带任何额外副作用面

---

## G. 明确禁止（写死）

code path dry-run 不允许直接：

- 打开 `side_effects_released`
- 执行真实写入
- 执行真实 `release_control`
- route / voice / memory / migration
- rollback / interrupt
- 越过标准对象吐散字段

---

## H. 与现有链路的关系（写清）

- 与 minimal code skeleton：skeleton 是代码壳子；code path dry-run 是对这个壳子的调用顺序演练。
- 与 live implementation dry-run execution：那是 runtime 占位路径演练；这里是未来真实代码骨架路径演练。
- 与 go/no-go gate：go/no-go gate 决定能不能开始；code path dry-run 决定开始前代码路径是否已零副作用走通。
- 与 rollout plan：rollout plan 定未来试运行策略；code path dry-run 不替代 rollout 策略。

---

## I. 当前仍然不能做什么（写死）

- 不允许打开 `side_effects_released`
- 不允许真实写入
- 不允许真实 `release_control`
- 不允许真实 rollout
- 不允许真实 `rollback` / `interrupt`
- 不允许 route / voice / memory / migration
- 不允许把 `...code_path_dry_run_executed` 当作真实代码已执行

---

## J. 当前不做（写死）

- 不做真实 live implementation 代码
- 不做真实 rollout 开启
- 不做地图接入
- 不做语音/记忆联动
- 不做中台真实迁移

---

## K. 下一步边界（写死）

- 本轮之后，下一步才考虑：
  - 第一版真实最小写入代码是否真正落地
- 若落地：只允许最小实现，不允许扩面
- 当前不直接落真实实现

补充链接（冻结链路）：

- Phase-Next-126：First Real Code Activation Definition v0（真实代码开始执行边界定义冻结）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_LIVE_IMPLEMENTATION_FIRST_REAL_CODE_ACTIVATION_DEFINITION_V0.md`

