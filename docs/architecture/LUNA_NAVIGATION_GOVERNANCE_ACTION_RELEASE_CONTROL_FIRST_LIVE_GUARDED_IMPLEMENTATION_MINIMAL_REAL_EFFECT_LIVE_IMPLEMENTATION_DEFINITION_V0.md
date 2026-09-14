# Luna — Navigation Governance Action Release Control First Live Guarded Implementation Minimal Real-Effect Live Implementation Definition v0（第一版真实最小写入实现本体：定义冻结）

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_LIVE_IMPLEMENTATION_DEFINITION_V0.md`  
**性质**：Phase-Next-114：冻结 `minimal real-effect` 第一版**真实最小写入实现本体（live implementation）**的边界定义（只定义、不落代码；可冻结、可回归）

基于（已具备）：
- activation contract（冻结）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_ACTIVATION_CONTRACT_V0.md`
- activation gate implementation（已具备）
- activation dry-run implementation（已具备）
- commit / pre-commit / launch / admission 全链路对象（已具备）
- implementation definition / skeleton / wiring / implementation dry-run execution（已具备）
- 当前 `side_effects_released` 仍强制锁死为 `false`（不允许打开）

---

## 1. 文档定位（写死）

这份文档是：

- `release_control first live guarded implementation minimal real-effect` 的第一版**真实实现本体定义**文档。
- 当前目标：冻结“从 activation dry-run 到未来真实最小写入实现”的实现边界：它到底是什么、最小消费什么输入、最小允许什么真实副作用、最小顺序是什么、失败时如何立即收口（包含恢复 `side_effects_released=false` 的要求）。

并且（本轮写死边界）：

- 当前不做真实代码实现（不落 live implementation）。
- 当前不做真实 `rollback` / `interrupt`。
- 当前不做地图接入、不改路线。
- 当前不做语音/记忆联动。
- 当前不做中台真实迁移。
- 当前不改变现有主线行为。

---

## 2. 为什么现在必须先定义 live implementation definition（写死理由）

- 当前已经有 activation contract。
- 当前已经有 activation gate implementation。
- 当前已经有 activation dry-run implementation。
- 但还没有一个明确的“第一版真实最小写入实现本体”的定义。
- 如果不先冻结 live implementation definition，后续很容易把 skeleton / stub / gate / dry-run 与真实实现揉在一起，导致边界扩权与 `side_effects_released` 打开逻辑失控。

因此必须先冻结真实实现本体边界，再考虑 skeleton / stub / minimal implementation。

---

## 3. live implementation 的最小定义（写死）

`release_control first live guarded implementation minimal real-effect live implementation` 是：

- activation dry-run 之后、未来真实最小写入真正发生的实现本体
- 只负责执行被 activation contract 明确允许的三类真实副作用

它不是：

- activation gate 本身
- activation dry-run 本身
- activation contract 本身
- rollback / interrupt 执行器
- route / voice / memory / migration 实现器

核心定义（写死一句）：

> live implementation 只允许执行 activation contract 明确允许的真实最小写入，不得扩展到任何额外副作用面。

---

## 4. 最小合法输入（写死；只允许标准化对象）

live implementation 只允许消费（只读）：

- admission gate == admitted
- guarded launch gate == launch_admitted
- pre-commit dry-run == pre_commit_ready
- commit gate == commit_admitted
- commit dry-run == commit_ready
- activation gate == activation_admitted
- activation dry-run == activation_ready
- approval / launch / live release / side-effect release 全部 ready/approved
- dry-effect simulation == simulated
- implementation dry-run execution == executed
- execution_state_v0 / result_v0 在位
- side_effects_released：激活前仍为 false
- 明确的 activation / live execution signal（语义在位，不实现来源机制）
- implementation skeleton identity / capability 在位且作为边界依据

并写死：

- 禁止读取 `request_* / approved_* / raw metadata`。
- 缺任一主前提，不得进入 live implementation。

---

## 5. 最小允许真实副作用范围（写死）

live implementation 仅允许三类真实副作用：

1) `execution_state_real_write`
2) `result_object_real_write`
3) `exception_or_failure_real_write`

除此以外全部禁止。

---

## 6. 最小真实写入顺序（写死）

### 正常路径（写死）

1) 确认 `side_effects_released == false`
2) 进入未来受控激活态（语义：仅允许最小 real-write）
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
- 不允许失败后保留半开启的 side effects 状态

---

## 7. 最小成功判定（写死）

最小成功需同时满足：

- 只在三类允许面内发生真实写入
- 顺序符合合同（state → result；异常路径按固定收口）
- 未触碰任何禁止面
- failure path 未误触发
- 可追踪、可复盘、可立即止损

并明确：

- 成功不等于业务全链路完成
- 不等于中台真实迁移完成

---

## 8. 最小失败判定（写死）

任一成立即判失败：

- 任一禁止面被触碰
- 任一写入顺序错误
- 任一 failure path 缺失或不可收口
- 任一无法恢复 `side_effects_released=false`
- 任一试图顺手做 `rollback` / `interrupt` / route / voice / memory / migration

---

## 9. 明确禁止（写死）

live implementation 不允许直接：

- route change
- voice output
- memory write
- mid-platform real migration
- rollback
- interrupt
- map/path planning side-effect source
- 越过标准对象吐散字段

---

## 10. 与现有链路的关系（写清）

- 与 activation contract：contract 定义允许面与顺序；live implementation 是未来唯一允许执行这些真实写入的本体。
- 与 activation gate：gate 判断能否进入受控激活；live implementation 在被允许后真实执行最小写入。
- 与 activation dry-run：dry-run 是最后一次零副作用演练；live implementation 才是真正的第一版真实写入实现。
- 与 definition / plan / skeleton / stub：本 definition 定“真实实现本体边界”；后续 skeleton/stub 只是承载位，不等于真实实现本体。

---

## 11. 当前仍然不能做什么（写死）

- 不允许现在就把 `side_effects_released` 打开
- 不允许真实写入
- 不允许真实 `release_control`
- 不允许真实 `rollback` / `interrupt`
- 不允许 route / voice / memory / migration
- 不允许把 definition 当作真实实现已存在

---

## 12. 当前不做（写死）

- 不做 live implementation 代码实现
- 不做 live implementation skeleton 代码实现
- 不做 live implementation stub 代码实现
- 不做真实最小写入实现
- 不做地图接入
- 不做语音/记忆联动
- 不做中台真实迁移

---

## 13. 下一步边界（写死）

- 本轮之后，下一步才考虑：
  - minimal real-effect live implementation skeleton v0
- 补充链接：
  - Phase-Next-117：Minimal Real-Effect Live Implementation Admission & Acceptance v0（准入与验收红线：冻结）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_LIVE_IMPLEMENTATION_ADMISSION_AND_ACCEPTANCE_V0.md`
- 再之后才考虑：
  - minimal real-effect live implementation stub v0
- 再之后才考虑：
  - 第一版真实最小写入实现的最小实现方案
- 当前不直接落真实实现

