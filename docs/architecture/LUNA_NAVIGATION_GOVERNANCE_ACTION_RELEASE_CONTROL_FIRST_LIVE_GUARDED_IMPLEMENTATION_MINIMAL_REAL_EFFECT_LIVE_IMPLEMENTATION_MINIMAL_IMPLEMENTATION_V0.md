# Luna — Navigation Governance Action Release Control First Live Guarded Implementation Minimal Real-Effect Live Implementation Minimal Implementation v0（第一版真实最小写入实现：最小实现方案冻结）

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_LIVE_IMPLEMENTATION_MINIMAL_IMPLEMENTATION_V0.md`  
**性质**：Phase-Next-118：在已冻结的 definition + admission & acceptance 基础上，把“第一版真实最小写入实现”推进为**最小实现方案**（仍然只允许三类真实副作用面；本轮优先冻结方案、不落真实实现代码）

基于（已具备）：
- live implementation definition v0：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_LIVE_IMPLEMENTATION_DEFINITION_V0.md`
- live implementation skeleton v0（代码占位）：`capabilities/governance/runtime/navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_skeleton_v0.py`
- live implementation stub v0（runtime 占位）：`capabilities/governance/runtime/navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_stub_v0.py`
- live implementation admission & acceptance v0：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_LIVE_IMPLEMENTATION_ADMISSION_AND_ACCEPTANCE_V0.md`
- activation contract v0：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_ACTIVATION_CONTRACT_V0.md`
- activation gate / activation dry-run（冻结 + 最小实现）
- admission / launch / pre-commit / commit 全链路对象（最小实现）
- 当前 `side_effects_released` 仍强制锁死为 `false`

---

## 1. 文档定位（写死）

这份文档是：

- 第一版 `release_control first live guarded implementation minimal real-effect live implementation` 的**最小真实写入实现方案**（Minimal Implementation Plan）。
- 它不是 gate，不是 dry-run，不是 stub，不是 skeleton；它回答的是：**第一版真实最小写入实现到底如何“最小落地”**（代码落点、三类写入由谁负责、最小顺序、最小测试、最小回退剧本）。

并且（本轮写死边界）：

- 本轮优先做方案冻结；不顺手扩展任何副作用面。
- 本轮不改变任何现有主线行为。
- 本轮不接地图、不改路线。
- 本轮不驱动语音/记忆。
- 本轮不触发中台真实迁移。
- 本轮不实现真实 `rollback` / `interrupt`。
- 本轮**不把 `side_effects_released` 从 false 改成 true**（即使方案里会描述“未来受控短时激活”的责任与接口，也不得实际打开）。

---

## 2. 为什么现在进入 minimal implementation（写死理由）

至少基于以下事实（写死）：

- definition 已冻结：真实实现本体边界、三类允许面、最小顺序已明确。
- skeleton 已存在：真实实现承载壳子已占位，且明确 `can_open_side_effects_released=False`、`can_real_write_* = False`。
- stub 已存在：runtime 占位层已存在，且当前只做 skeleton 委托与 placeholder-safe 输出。
- admission & acceptance 已冻结：准入门槛、验收口径、红线与固定回退顺序已写死。
- activation contract 已冻结：未来 side effects 受控打开的唯一合法机制已定义（但当前禁止打开）。
- 再继续补“规则类文档”的边际收益会快速下降；当前更需要把“真实最小实现怎么落地”明确下来，但仍然严格限制在三类允许面内。

---

## 3. 最小代码落点判断（写死结论 + 理由）

### 3.1 结论（写死）

第一版真实最小写入实现（live implementation）的**最小代码落点**应新增为独立文件：

- `capabilities/governance/runtime/navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_v0.py`

并新增配套 verify：

- `tools/verify_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_v0.py`

### 3.2 为什么要独立成 minimal implementation 文件（写死理由）

- **最连续**：与 skeleton / stub 同域（`capabilities/governance/runtime/`），语义上属于同一“live implementation”承载层家族。
- **最不容易失控**：独立文件可以把“唯一允许真实写入的入口”与 placeholder shell（skeleton/stub）物理隔离，减少误用/误接线风险。
- **最小侵入**：不需要修改现有 gate/dry-run 组件，不需要改变主线 dispatcher 行为；未来也可以在不接入主线的情况下先做局部白盒验证。
- **最利于回滚**：真实写入入口集中在单文件，可通过替换/禁用该模块快速止损，而不污染其它占位模块。

### 3.3 是否应该与 skeleton / stub 同文件（写死否）

- 不应与 skeleton/stub 同文件：skeleton/stub 当前硬边界是“永远不打开 side_effects_released、不真实写入”。把 minimal implementation 合并进去会破坏“占位层永远非动作”的可回归性与可信度。

---

## 4. 最小允许真实副作用面（写死）

第一版真实最小写入实现**只允许**三类真实副作用：

1) `execution_state_real_write`  
2) `result_object_real_write`  
3) `exception_or_failure_real_write`

除此以外全部禁止（写死），包括但不限于：

- route / proposal 改写
- voice 输出
- memory 写入
- map/path planning 真实副作用
- mid-platform real migration
- rollback / interrupt
- 任何超出标准化对象输出的“散字段落库/落盘/发网”

---

## 5. 三类真实副作用各由谁写（写死责任拆分）

写死责任如下：

- `execution_state_real_write`：由 **live implementation minimal implementation** 负责调用“唯一允许的 execution_state writer”接口完成写入。
- `result_object_real_write`：由 **live implementation minimal implementation** 负责调用“唯一允许的 result writer”接口完成写入。
- `exception_or_failure_real_write`：由 **live implementation minimal implementation** 负责调用“唯一允许的 exception/failure writer”接口完成写入。

并写死：

- writers 的具体落点与实现（例如落盘/落库/发网）**不在本方案中展开**，因为本轮仍禁止真实写入；但必须保证未来 writers 也只在三类允许面内产生效果，且必须受 `side_effects_released` 的受控短时激活约束。

---

## 6. 谁负责 side_effects_released 的“受控短时激活”与恢复（写死）

写死责任：

- **Activation Contract** 定义“唯一允许如何受控打开”的规则与顺序。
- **Activation Gate / Dry-Run** 决定是否允许进入该合同，并演练（零副作用）激活序列。
- **Live Implementation Minimal Implementation** 作为真实写入本体，负责在写入前后执行“受控短时激活/恢复”的最小闭环。

写死约束：

- 激活必须显式、短时、可恢复；任何异常都必须优先恢复 `side_effects_released=false`。
- 禁止默认开启；禁止半开启悬挂。
- 本轮不实现、也不触发该激活；只冻结“未来责任与顺序”。

---

## 7. 最小真实写入顺序（写死）

### 7.1 正常路径（写死）

1) 确认 `side_effects_released == false`  
2) 进入受控短时激活（仅三类允许面）  
3) 写 `execution_state`（real-write）  
4) 写 `result_object`（real-write）  
5) 恢复或确认 `side_effects_released=false`  
6) 交还治理链

### 7.2 异常路径（写死）

1) **立即**恢复 `side_effects_released=false`  
2) 写失败/退出态 `execution_state`（real-write）  
3) 写失败 `result_object`（real-write）  
4) 写 `exception_or_failure`（real-write）  
5) 交还治理链

### 7.3 禁止项（写死）

- 禁止先 result 后 state  
- 禁止先做其它副作用再补对象  
- 禁止半开启 `side_effects_released` 悬挂  
- 禁止 failure path 中“扩权补救”  

---

## 8. 最小实现前提（写死收束）

第一版真实最小写入实现**只有在以下全部成立时才允许进入**（写死；少任一项不得进入）：

- activation gate == `activation_admitted`
- activation dry-run == `activation_ready`
- live implementation admission & acceptance 条件全部满足
- skeleton / stub 在位（且 identity 可验证）
- `side_effects_released == false`
- activation signal / live execution signal 在位（语义在位；不得由 raw metadata 直驱）
- `execution_state_v0 / result_v0 / exception_or_failure path` 在位
- 其它全链路对象（admission/launch/pre-commit/commit）均为 admitted/ready

---

## 9. 最小测试矩阵（写死最少覆盖）

写死至少覆盖以下用例（均为白盒可复盘）：

1) 正常路径通过（state → result；最终 side_effects_released 可恢复为 false）  
2) activation signal 缺失（不得进入；应返回 not_admitted/not_ready 类结果；不得写入）  
3) `side_effects_released != false`（必须阻断；不得进入；不得写入）  
4) state 写入失败（必须走异常路径：先恢复 false，再写失败 state/result/exception）  
5) result 写入失败（必须走异常路径：先恢复 false，再补齐失败 state/result/exception 的固定收口）  
6) exception path 收口失败（必须判为红线失败；仍需尝试优先恢复 false；不得扩权补救）  
7) 任一步骤后是否能恢复 `side_effects_released=false`（强制断言）  
8) V1 最小闭环回归（不改主线行为前提下，验证“非动作链仍可运行 + 新实现不接入主线”）

---

## 10. 最小止损与回退剧本（写死）

写死固定回退顺序（与 admission & acceptance 对齐）：

1) 任一异常/红线：**先**恢复 `side_effects_released=false`  
2) **再**写失败/退出态 `execution_state`  
3) **再**写失败 `result_object`  
4) **再**写 `exception_or_failure`  
5) **再**交还治理链  

并写死：

- 不允许失败后扩权补救（例如为了“补救成功”而打开更多副作用面）。
- 不允许失败后保留半开启状态。

---

## 11. 当前仍然不能做什么（写死）

本方案冻结不改变以下禁止项：

- 不允许 route / voice / memory / migration
- 不允许 rollback / interrupt
- 不允许把 minimal implementation 当成全量实现
- 不允许默认开启 `side_effects_released`
- 不允许把真实最小写入入口接入现有主线 dispatcher（本轮仅冻结方案）

---

## 12. 下一步边界（写死）

本轮之后才考虑：

- 是否落第一版真实最小写入实现代码（新增 `..._live_implementation_v0.py` 与 verify）
- 若落代码：只允许最小实现，不允许扩面；失败路径优先级高于成功路径；且仍不得影响现有主线行为

补充链接（冻结链路）：

- Phase-Next-122：First Real Write Rollout Plan v0（第一次真实最小写入试运行上线方案冻结）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_LIVE_IMPLEMENTATION_FIRST_REAL_WRITE_ROLLOUT_PLAN_V0.md`

