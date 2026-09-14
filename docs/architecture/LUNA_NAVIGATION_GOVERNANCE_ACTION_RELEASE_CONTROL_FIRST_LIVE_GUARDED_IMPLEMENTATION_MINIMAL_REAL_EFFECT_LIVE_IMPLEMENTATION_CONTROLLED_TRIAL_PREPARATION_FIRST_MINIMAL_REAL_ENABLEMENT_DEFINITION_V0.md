# Luna — Navigation Governance Action Release Control First Live Guarded Implementation Minimal Real-Effect Live Implementation Controlled Trial Preparation First Minimal Real Enablement Definition v0（真实启用“何时算开始”边界冻结）

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_LIVE_IMPLEMENTATION_CONTROLLED_TRIAL_PREPARATION_FIRST_MINIMAL_REAL_ENABLEMENT_DEFINITION_V0.md`  
**性质**：Phase-Next-151：只做 Definition Freeze；把“可开始”和“已开始”彻底剥离；不写真实启用实现、不改默认路径、不释放 side effects

---

## A. 背景与当前已闭合事实（只读）

当前已成立：

- preparation minimal enablement plan 已冻结（Phase-Next-148）
- preparation minimal enablement implementation 已存在（Phase-Next-149）
- preparation minimal enablement dry-run 已执行并走通（Phase-Next-150）
- preparation real code 已存在（Phase-Next-144）
- preparation shadow / shadow evaluation / admission / go-no-go 链已存在（Phase-Next-145/146/147 等）
- `side_effects_released` 仍为 `false`
- 默认路径仍未开启
- 真实 preparation / 真实 controlled trial 仍未开始

本阶段唯一目标：

- 冻结 **“preparation minimal enablement dry-run executed 之后，第一阶段真实 preparation minimal enablement 真正开始”的边界**，避免混淆：
  1) `preparation_go`
  2) `preparation_enablement_dry_run_executed`
  3) `real_preparation_minimal_enablement_started`

---

## B. 本 definition 的作用范围（写死）

本 definition 仅回答：

- **何时才算真实 preparation minimal enablement “开始”（started）**
- “开始”的唯一判定标准（唯一 start event）
- `side_effects_released` 何时才允许进入“受控短时真实启用窗口”
- 启用后的最小成功态、最小失败态、最小收口点分别是什么
- “armed 但未 started / started 但未 committed / aborted / rollback_completed / closed”的边界含义与迁移规则

---

## C. 明确排除项（不属于本阶段；写死）

本阶段不做：

- 不写真实 enablement runtime 代码（不实现真实启用 runner）
- 不写真实 controlled trial 执行器
- 不切默认路径
- 不把 `side_effects_released` 改为 `true`
- 不新增任何会触发真实副作用的调用
- 不修改既有 dry-run 结果语义
- 不把 definition 和 implementation 混写到一起

---

## D. 核心术语定义（写死）

以下术语在本项目中 **必须按本节语义解释**：

- **preparation_go**：`preparation go/no-go gate == go` 的状态事实，表示“本次允许尝试进入 preparation 启用流程的 arming/起始门判断”，**不等于 started**。
- **dry_run_executed**：`preparation minimal enablement dry-run == executed` 的状态事实，只证明“入口顺序可零副作用演练”，**不等于 started**。
- **armed**：满足 start gate 的所有前置条件，且已获得显式 real enablement 启动意图，但 **尚未观测到 start event**；可视为“已 armed 但未 started”。
- **real_enablement_started**：满足“真实开始唯一判据（F）”后的状态事实；在该事实成立前，任何实现不得宣称 started。
- **side_effects_released**：治理链的副作用放权布尔语义。默认必须为 `false`；只有在本 definition 明确允许的 start gate 之后，才允许进入“短时受控窗口语义”（实现层可用局部语义表示），并必须可恢复为 `false`。
- **committed**：最小真实启用的“核心写入动作集合”已完成，且进入可验证的最小成功或最小失败收口链；**committed 不等于默认路径启用**。
- **aborted**：在 started 之后，但在 committed 之前或期间发生判定性失败/熔断，触发固定收口路径并放弃继续推进。
- **rollback_completed**：在 aborted 或失败收口路径下，按定义的回退闭环完成（至少包括恢复/确认 `side_effects_released=false` 与必要的失败写入收口）。
- **closed**：收口完成且系统回到可验证安全闭合态（等价于“可继续由上游治理链接管”，并且 **side_effects_released=false 或等价安全闭合**）。

---

## E. 状态边界与不变量（强制；写死）

### 必须写死的区分结论

1. `dry-run executed ≠ real enablement started`  
2. `preparation_go ≠ real enablement started`  
3. `real enablement started` 必须有单独且唯一的 start event  
4. `side_effects_released` 只能在明确定义的 start gate 后进入允许态（短时受控窗口）  
5. `armed` 是真实开始前的预备态，不得等同于 started  
6. 一旦 started，必须存在最小观测窗口、最小失败收口路径、最小回滚闭环  
7. 最小成功不等于完成 trial，只代表第一段真实受控启用成立  
8. 最小失败不等于系统失败，而是第一段真实受控启用未满足成立条件并完成收口  
9. 最小收口点必须把系统带回 `side_effects_released=false` 或等价安全闭合态  
10. 后续任何 implementation 不得绕过本 definition 直接宣称 started

### 强制不变量（写死）

- 在 `start_event_observed` 之前，**不得视为** `real_enablement_started`
- 在 `real_enablement_started` 之前，`side_effects_released` **不得进入 true**（即使语义窗口，也必须由 start gate 授权）
- dry-run 产物不得作为 `real_enablement_started` 的证据
- shadow evaluation 通过只说明具备进入起始门判断资格，不代表已经开始
- go-no-go 通过只说明允许尝试进入 armed，不代表 started
- `real_enablement_started` 一旦成立，必须存在对应的 closure path
- closure 完成后，系统必须回到可验证的安全闭合状态

---

## F. “真实开始”的唯一判定标准（写死；唯一开始判据）

**唯一开始判据**：

> 当且仅当“真实启用执行入口（Real Enablement Execution Entry）”被显式调用，并且该入口在通过其 **real-input acceptance** 后，**观测到 start event**：`start_event_observed == true`，此时才可判定 `real_preparation_minimal_enablement_started == true`。

解释（写死约束）：

- start event 必须是实现层可记录、可复盘、可唯一识别的事件（例如 trace 中出现固定标记 `start_event_observed`，或等价的“进入受控短时启用窗口”的单点事件）。
- 仅有 `preparation_go`、`dry_run_executed`、`shadow_eval_go` 等前置事实，不构成 started 证据。

---

## G. side_effects_released 的前置条件（写死）

`side_effects_released` 允许进入“受控短时真实启用窗口语义”的必要前置条件（缺一不可）：

- 已满足 `preparation_go`（最终启动门通过）
- enablement dry-run 已 executed（证明入口顺序可演练）
- shadow evaluation gate 已 go（影子观察质量线通过）
- admission gate 已 admitted（准备态资格成立）
- 本次 **real enablement start signal/approval** 明确存在（显式意图）
- 且 **start event 已被观测**（F）

并写死：

- 在 start event 之前，任何层级不得打开或等价地宣称 `side_effects_released=true`
- start event 之后的窗口必须是短时、可恢复，并以“恢复/确认 false”为最低收口要求

---

## H. 最小成功态定义（写死）

**最小成功态（minimal_success_reached）**：

- started 已成立（F）
- 在允许的最小写入面内完成最小成功收口：
  - 至少完成 `execution_state_real_write` 与 `result_object_real_write`（且无越权副作用）
  - 并完成最小收口点（J）：恢复/确认 `side_effects_released=false` 或等价安全闭合

写死：

- 最小成功不等于“完成 trial”
- 最小成功不等于“默认路径启用”

---

## I. 最小失败态定义（写死）

**最小失败态（minimal_failure_reached）**：

- started 已成立（F），但最小成功条件未满足
- 且已进入固定失败收口路径并完成必要收口写入（至少包含失败态 state/result 与 exception_or_failure 的记录），并完成最小收口点（J）

写死：

- 最小失败不等于系统整体失败
- 最小失败必须收口到可验证安全状态

---

## J. 最小收口点定义（写死）

**最小收口点（minimal_closure_point）**：

- 系统已恢复/确认 `side_effects_released=false`（或等价安全闭合态）
- 且已完成“成功或失败”的最小可复盘记录闭环
- 且交还治理链继续接管（不残留半开启状态）

---

## K. 允许的状态迁移 / 禁止的状态迁移（写死）

### 允许迁移（示意；写死规则）

- readiness/pre-start → arming → started → (minimal_success | minimal_failure) → closed
- started → aborted → rollback_completed → closed

### 禁止迁移（写死）

- `dry_run_executed` → `started`（禁止：缺少唯一 start event）
- `preparation_go` → `started`（禁止：缺少唯一 start event）
- `shadow_eval_go` → `started`（禁止：影子评估不是开始事件）
- `armed` → `committed`（禁止：未 started 不得 committed）
- 任意状态 → “默认路径开启”（本 definition 不允许把 started/committed 解释为默认路径开启）

---

## L. 与 dry-run、shadow、admission、go-no-go 的关系（写死）

- dry-run：证明“入口顺序可演练”，不提供 started 证据
- shadow：证明“真实代码旁路可观察”，不提供 started 证据
- shadow evaluation gate：提供“影子质量线是否过关”的证据，不提供 started 证据
- admission gate：提供“准备态资格是否成立”的证据，不提供 started 证据
- go/no-go gate：提供“本次是否允许尝试进入 arming”的证据，不提供 started 证据

---

## M. 后续真实 implementation 必须遵守的契约（写死）

后续任何真实 enablement implementation（Phase-Next-152 及以后）必须遵守：

- 任何地方不得把 `dry_run_executed` / `preparation_go` / `shadow_eval_go` 当作 started
- 必须显式产出并可复盘 `start_event_observed`（唯一开始事件）
- 必须保证在最小收口点（J）后回到 `side_effects_released=false` 或等价安全闭合态
- 必须提供最小失败收口闭环：aborted/rollback_completed/closed
- 禁止扩面到 route/voice/memory/migration/rollback/interrupt/map/path side-effect source

---

## N. 验收标准（写死）

本 definition 通过验收，当且仅当：

- 文档明确冻结：
  - 唯一开始判据（F）
  - `side_effects_released` 放行条件（G）
  - 最小成功/失败/收口点定义（H/I/J）
  - 允许/禁止迁移（K）
- 明确写死：`preparation_go` 与 `dry_run_executed` 都不等于 started
- 明确排除：不写真实 enablement implementation，不切默认路径，不释放 side effects

