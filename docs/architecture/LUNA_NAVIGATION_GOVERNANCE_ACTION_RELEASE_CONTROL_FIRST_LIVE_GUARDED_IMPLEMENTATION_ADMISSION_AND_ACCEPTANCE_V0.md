# Luna — Navigation Governance Action Release Control First Live Guarded Implementation Admission & Acceptance v0（第一版真实受控实现：准入与验收总则冻结）

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_ADMISSION_AND_ACCEPTANCE_V0.md`  
**性质**：Phase-Next-86：冻结 `release_control` 第一版真实 guarded implementation 真正开始写代码前的 **准入条件 / 验收条件 / 止损红线 / 回退判据**（只写总则、不落真实实现、不触发真实动作；可冻结、可回归）

基于（已具备）：
- guarded implementation definition（冻结）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_DEFINITION_V0.md`
- guarded implementation stub（承载位）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_STUB_V0.md`
- enablement approval gate（冻结/最小实现）：  
  `docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_ENABLEMENT_APPROVAL_GATE_V0.md`、  
  `docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_ENABLEMENT_APPROVAL_GATE_IMPLEMENTATION_V0.md`
- launch dry-run（冻结/最小实现）：  
  `docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_LAUNCH_DRY_RUN_V0.md`、  
  `docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_LAUNCH_DRY_RUN_IMPLEMENTATION_V0.md`
- live release gate（冻结/最小实现）：  
  `docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_LIVE_RELEASE_GATE_V0.md`、  
  `docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_LIVE_RELEASE_GATE_IMPLEMENTATION_V0.md`
- side-effect release contract / gate（冻结/最小实现）：  
  `docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_SIDE_EFFECT_RELEASE_CONTRACT_V0.md`、  
  `docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_SIDE_EFFECT_RELEASE_GATE_IMPLEMENTATION_V0.md`
- minimal runtime contract（冻结）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_MINIMAL_RUNTIME_CONTRACT_V0.md`
- execution state / result（实现）：  
  `docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_EXECUTION_STATE_IMPLEMENTATION_V0.md`、  
  `docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_RESULT_OBJECT_IMPLEMENTATION_V0.md`

---

## A. 文档定位（写死）

这份文档是：

- `release_control` 第一版真实 guarded implementation 的 **准入与验收总则**（admission & acceptance governance）。
- 当前目标：一次性冻结“什么时候允许开始写第一版真实 guarded implementation、写到什么算通过、碰到什么必须立刻止损、失败后如何判定必须回退”的标准（可冻结、可回归）。

这份文档不是：

- guarded implementation 的实现代码。
- runtime contract（运行时合同）本身。
- enablement plan（启用/灰度/回退方案）本身。
- approval gate / launch dry-run / release gate 本身。

并且（本轮写死边界）：

- 当前不做真实 `release_control`。
- 当前不做真实 `rollback` / `interrupt`。
- 当前不做地图接入、不改路线。
- 当前不做语音/记忆联动。
- 当前不做中台真实迁移。
- 当前不改变现有主线行为。
- 当前 `side_effects_released` 仍强制锁死为 `false`（不允许打开）。

---

## B. 为什么现在必须先定义 admission & acceptance（写死理由）

当前已经具备：

- guarded implementation definition（定义冻结）
- guarded implementation stub（承载位在位）
- approval gate / launch dry-run / live release gate / side-effect release gate（冻结 + 最小实现）
- minimal runtime contract（运行时顺序与禁止面冻结）
- execution state / result object / failure path（实现/承载位在位）

但目前仍缺少一份明确的“总则”来回答：

- **什么叫允许开始写第一版真实 guarded implementation**（准入门槛）
- **什么叫实现通过验收**（验收标准）
- **什么情况必须立刻止损**（红线）
- **失败后怎么判定必须回退**（回退判据与固定顺序）

如果不先冻结这份总则，后续真实实现很容易出现：

- 标准边写边改，准入与验收漂移，最终失控。
- “实验性真实实现”滑成“默认实现”。

因此：必须先冻结 admission & acceptance，再考虑进入第一版真实实现的代码落地。

---

## C. admission 的最小定义（写死）

`first live guarded implementation admission` 是：

- 允许第一版真实 guarded implementation **开始进入代码落地** 的前置准入门槛（pre-implementation admission threshold）。

它不是：

- approval gate 本身（approval gate 只解决“是否批准试运行”）。
- launch dry-run 本身（dry-run 只解决“发车前最后检查是否 ready”）。
- runtime contract 本身（contract 只解决“运行时顺序与禁止面”）。
- guarded implementation stub 本身（stub 只提供承载位）。

---

## D. 最小准入条件（写死；少任一项不得进入真实实现）

进入第一版真实 guarded implementation（开始写真实实现代码）之前，以下条件必须全部满足（少任一项，不得进入）：

1) `first_live_enablement_approval_gate.approval_status == "first_live_enablement_approved"`  
2) `first_live_launch_dry_run.launch_status == "first_live_launch_dry_run_ready"`  
3) `live_release_gate.live_release_status == "live_release_ready"`  
4) `side_effect_release_gate.side_effect_release_status == "side_effect_release_ready"`  
5) `guarded implementation stub` 已验证通过（承载位可执行、不可越权路径已验证）  
6) `execution_state_v0`、`result_v0`、`exception / failure path` 在位且可收口  
7) 回退路径已验证可立即执行（包含恢复 `side_effects_released=false` 的可达性验证）  
8) 默认开关仍为 `false`：必须在显式批准后，才允许进入真实实现分支（不允许“默认进入/默认启用”）

并明确写死：

- 少任一项，不得进入真实实现。
- 当前阶段只冻结规则：**不允许真正开始真实实现代码**。

---

## E. 最小允许实现范围（写死；极度克制）

第一版真实 guarded implementation **只允许**真实落地（真实 side effect）：

1) `execution state` 的真实推进  
2) `result object` 的真实写入  
3) `exception / failure path` 的真实写入  

并写死：

- 第一版真实实现最多只允许这三类真实 side effect。
- 除上述三类之外，其他一律视为越权 side effect（直接触发止损红线）。

---

## F. 最小验收条件（写死）

第一版真实 guarded implementation 的最小验收条件至少包括：

- `execution state` 按 runtime contract 规定顺序推进（不跳步、不倒序、不并行穿透）
- `result object` 按 runtime contract 规定顺序写出（不吐散字段、不绕过标准对象）
- `failure path` 正确：可触发、可收口、可追踪、不会缺失
- 未触碰任何禁止面（见 I、J）
- 白盒可追踪（可通过标准对象与状态推进链复盘）
- 可立即回退到 `side_effects_released=false`（回退判据与路径可达）
- 未将“实验性真实实现”扩成“业务动作/默认实现”

---

## G. 最小止损红线（写死；触碰即失败）

触碰以下任一项，必须立即止损，判定本次实现不通过：

- 任一越权 side effect（超出 E 允许范围）
- 任一对象未按顺序更新（execution state / result object 任一倒序、跳步、绕过）
- 任一 failure path 缺失或不可收口
- 任一无法回退（无法立即恢复 `side_effects_released=false` 或无法按固定顺序收口）
- 任一试图顺手做 `rollback` / `interrupt` / route / voice / memory / migration
- 任一试图绕过标准对象吐散字段（字段散射、非标准出口）

---

## H. 最小回退判据与固定顺序（写死）

一旦触碰止损红线（G）或任一准入条件不满足（D），必须立即判定：

- 当前实现不通过（fail）。
- 立即恢复 `side_effects_released=false`（强制回到锁死态）。

回退收口顺序必须固定为：

1) 恢复 `side_effects_released=false`  
2) 写 `execution state`（记录退出/止损态）  
3) 写 `result object`（写出失败结果与最小可追踪原因）  
4) 走 `exception / failure path`（完成收口，不允许悬挂）  
5) 交还治理链（回到治理链入口，不允许转入业务动作）  

并写死：

- 止损与回退优先于任何“补救扩权”。
- 不允许失败后临时扩实现范围。

---

## I. 继续禁止的 side effect（必须写死；即使未来进入真实实现也仍禁止）

即使未来满足准入并进入第一版真实 guarded implementation，也仍然禁止：

- route（改路线 / 改 proposal / 改主线行为）
- voice（语音播报/驱动）
- memory（写记忆/驱动记忆联动）
- mid-platform real migration（中台真实迁移/真实联动）
- `rollback`
- `interrupt`
- map/path planning side effect source（读取地图/路径规划作为副作用来源）
- 越过标准对象吐散字段（非标准对象、非标准出口扩散）

---

## J. 与现有链路的关系（写清边界；不能混用）

与 approval gate：

- approval gate 决定“是否批准进入第一次试运行线”
- admission & acceptance 决定“是否允许开始写第一版真实实现，以及写完如何验收/止损/回退”

与 guarded implementation stub：

- stub 是代码承载位（让链路可接、可跑最小形态）
- admission & acceptance 是开始真实落地前的总则（写死准入/验收/止损/回退标准）
- 两者不能互相替代

与 runtime contract：

- runtime contract 规定运行时顺序与禁止面
- admission & acceptance 规定实现前的准入与实现后的验收、红线与回退判据

---

## K. 当前仍然不能做什么（必须写死）

- 不允许现在就开始第一版真实 guarded implementation 的真实代码实现。
- 不允许把 `side_effects_released` 从 `false` 改成 `true`。
- 不允许触发真实 `release_control`。
- 不允许触发真实 `rollback` / `interrupt`。
- 不允许地图接入、不允许改路线。
- 不允许驱动语音/记忆联动。
- 不允许中台真实迁移。
- 不允许把这份总则当成“实现已存在”。

---

## L. 当前不做（必须写死）

- 不做 admission & acceptance 的代码实现。
- 不做真实 `release_control`。
- 不做真实 `rollback` / `interrupt`。
- 不做地图接入。
- 不做语音/记忆联动。
- 不做中台真实迁移。
- 不做扩展业务逻辑（不把实验性实现扩为业务动作）。

---

## M. 下一步边界（写死）

- 本轮（Phase-Next-86）结束后，下一步才考虑：
  - Phase-Next-87：first live guarded implementation skeleton v0：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_SKELETON_V0.md`
  - 再之后才考虑：第一版真实 guarded implementation 的真正代码实现方案（implementation plan / approach）
- 当前不直接落真实实现。

