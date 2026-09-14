# Luna — Navigation Governance Action Release Control First Live Guarded Implementation Minimal Real-Effect Live Implementation First Real Write Rollout Plan v0（第一次真实最小写入：试运行上线方案冻结）

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_LIVE_IMPLEMENTATION_FIRST_REAL_WRITE_ROLLOUT_PLAN_V0.md`  
**性质**：Phase-Next-122：冻结第一版真实最小写入实现的**试运行上线方案（rollout plan）**（只定义如何灰度/观测/止损/回退；默认不开；本轮不做真实启用、不落真实实现代码）

基于（已具备）：
- live implementation definition v0（冻结）
- live implementation skeleton / stub（在位）
- live implementation admission & acceptance（冻结）
- live implementation minimal implementation plan（冻结）
- live implementation non-effect wiring（在位；可判 wired_ready）
- live implementation dry-run execution（在位；可判 executed）
- live runtime activation stub（在位；占位）
- activation contract / gate / dry-run（冻结 + 最小实现）
- activation / commit / pre-commit / launch / admission 全链路对象（最小实现）
- 当前 `side_effects_released` 仍强制锁死为 `false`

---

## 1. 文档定位（写死）

这份文档是：

- 第一版 `release_control first live guarded implementation minimal real-effect live implementation minimal implementation` 的**试运行上线方案（rollout plan）**文档。
- 当前目标：冻结“如果未来真的要开启第一版真实最小写入，应该如何最小范围试运行”的策略边界：灰度策略、观测面、成功/失败判定、止损与回退剧本。

并且（本轮写死边界）：

- 本轮只做 rollout plan 设计冻结。
- 不做真实代码实现（不落 live implementation minimal implementation）。
- 不做真实 rollout 启用（默认仍不开）。
- 不做真实 `rollback` / `interrupt` 实现。
- 不接地图、不改路线。
- 不驱动语音/记忆。
- 不触发中台真实迁移。
- 不改变现有主线行为。

---

## 2. 为什么现在必须先定义 rollout plan（写死理由）

- 目前 definition / skeleton / stub / admission & acceptance / wiring / dry-run / runtime activation stub 已在位。
- 再继续补占位层的边际收益很低。
- 真正缺的是“第一版真实写入怎么试运行”：如何灰度、如何观测、如何止损、如何回退。
- 如果不先冻结 rollout plan，后续最容易在没有灰度和止损策略的情况下直接进入真实写入。

因此必须先冻结 rollout plan，再决定是否进入真实最小实现代码。

---

## 3. rollout plan 的最小定义（写死）

`release_control first live guarded implementation minimal real-effect live implementation first real write rollout plan` 是：

- 第一版真实最小写入实现未来试运行时的**灰度、观测、止损、回退**总方案。
- 它只定义“如何受控试运行”，不等于真实实现已存在，也不等于真实 rollout 已开启。

核心定义（写死一句）：

> rollout plan 只定义“第一版真实最小写入如何受控试运行”，不直接执行任何真实写入。

---

## 4. 最小 rollout 前提（写死；少任一项不得试运行）

以下必须全部满足（少任一项不得试运行）：

- live implementation definition 已冻结
- live implementation skeleton 已存在
- live implementation stub 已存在
- live implementation admission & acceptance 已冻结
- live implementation minimal implementation plan 已冻结
- live implementation non-effect wiring == `first_live_minimal_real_effect_live_wired_ready`
- live implementation dry-run execution == `first_live_minimal_real_effect_live_dry_run_executed`
- live runtime activation stub 已存在
- activation gate == admitted
- activation dry-run == ready
- commit gate == admitted
- commit dry-run == ready
- pre-commit dry-run == ready
- guarded launch gate == admitted
- admission gate == admitted
- execution_state / result / exception_or_failure path 在位
- `side_effects_released == false`
- **显式 rollout approval 存在**
- **默认开关仍为 false（默认不开）**

并写死：

- 禁止读取 `request_* / approved_* / raw metadata` 作为直驱依据。
- rollout approval 必须是显式、可审计、可撤销的信号（语义在位即可；本轮不落实现）。

---

## 5. 最小 rollout 范围（写死为极小范围）

范围必须写死为“极小”：

- **单动作**：仅 `release_control`
- **单实现面**：仅三类允许真实副作用：
  - `execution_state_real_write`
  - `result_object_real_write`
  - `exception_or_failure_real_write`
- **单链路**：仅这条最小真实写入链（不得扩面到其它链路）
- **单环境**：仅受控试运行环境
- **单版本**：仅固定版本（不可漂移）
- **默认不开**：必须显式批准；不得进入任何真实默认路径

---

## 6. 最小观测面（写死；必须观测）

试运行必须观测至少包括：

- `side_effects_released` 是否曾被错误打开或未恢复
- state 写入是否成功
- result 写入是否成功
- exception/failure path 是否可收口
- 顺序是否正确（state → result → exception/failure closure）
- 是否触碰禁止面（route/voice/memory/migration/rollback/interrupt 等）
- 白盒可追踪性（可定位到每一步）
- 试运行后是否可立即回退

---

## 7. 最小成功判定（写死）

最小成功需同时满足：

- 仅触达三类允许面
- 顺序正确
- 无越权副作用
- failure path 未误触发
- `side_effects_released` 能在成功后恢复或确认回到 false
- 白盒可复盘

并写死：

- 成功不等于业务全链路完成
- 不等于中台迁移完成

---

## 8. 最小失败判定（写死）

任一成立即失败：

- 触碰任一禁止面
- 顺序错误
- `side_effects_released` 不能恢复为 false
- failure path 缺失或不可收口
- 任一写入失败后未按固定顺序收口
- 任一试图顺手做 `rollback / interrupt / route / voice / memory / migration`

---

## 9. 最小止损与回退剧本（写死固定顺序）

固定顺序（写死）：

1) **立即停止试运行**  
2) **恢复 `side_effects_released=false`**  
3) 写失败/退出态 `execution_state`  
4) 写失败 `result_object`  
5) 写 `exception_or_failure`  
6) 交还治理链  

并写死：

- 回退优先于任何补救
- 不允许失败后扩权补救
- 不允许保留半开启状态

---

## 10. 明确禁止（写死）

rollout plan 不允许放行以下任何内容：

- route change
- voice output
- memory write
- mid-platform real migration
- rollback
- interrupt
- map/path planning side-effect source
- 越过标准对象吐散字段
- 默认开启 side_effects

---

## 11. 与现有链路的关系（写清）

- 与 minimal implementation plan：plan 定技术实现最小范围；rollout plan 定未来试运行策略（灰度/观测/止损/回退）。
- 与 admission & acceptance：admission & acceptance 定“能不能开始做真实实现”；rollout plan 定“未来真实实现怎么灰度开启”。
- 与 dry-run / wiring / stub / skeleton：它们负责占位、接线、演练；rollout plan 负责未来第一次真实写入的试运行策略。

---

## 12. 当前仍然不能做什么（写死）

- 不允许现在就打开 `side_effects_released`
- 不允许真实写入
- 不允许真实 `release_control`
- 不允许真实 `rollback` / `interrupt`
- 不允许 `route / voice / memory / migration`
- 不允许把 rollout plan 当作真实 rollout 已开启

---

## 13. 当前不做（写死）

- 不做真实 rollout 开启
- 不做真实最小写入实现代码
- 不做地图接入
- 不做语音/记忆联动
- 不做中台真实迁移

---

## 14. 下一步边界（写死）

- 本轮之后，下一步才考虑：
  - 是否进入第一版真实最小写入实现代码
- 若进入代码：只允许最小实现，不允许扩面
- 当前不直接落真实实现

补充链接（冻结链路）：

- Phase-Next-123：Real-Write Go/No-Go Gate v0（真实写入启动最终闸门冻结）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_LIVE_IMPLEMENTATION_REAL_WRITE_GO_NO_GO_GATE_V0.md`
- Phase-Next-126：First Real Code Activation Definition v0（真实代码开始执行边界定义冻结）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_LIVE_IMPLEMENTATION_FIRST_REAL_CODE_ACTIVATION_DEFINITION_V0.md`

