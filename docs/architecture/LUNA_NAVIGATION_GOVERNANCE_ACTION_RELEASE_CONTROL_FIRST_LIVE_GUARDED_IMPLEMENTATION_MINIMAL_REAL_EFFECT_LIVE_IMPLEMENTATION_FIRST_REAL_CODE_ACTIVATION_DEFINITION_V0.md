# Luna — Navigation Governance Action Release Control First Live Guarded Implementation Minimal Real-Effect Live Implementation First Real Code Activation Definition v0（真实代码开始执行：边界冻结）

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_LIVE_IMPLEMENTATION_FIRST_REAL_CODE_ACTIVATION_DEFINITION_V0.md`  
**性质**：Phase-Next-126：冻结“第一版真实最小写入代码真正开始执行”的严格边界定义（只定义、不落真实实现；默认不开；可冻结、可回归）

基于（已具备）：
- live implementation definition / skeleton / stub（冻结 + 在位）
- live implementation minimal code skeleton（在位）
- live implementation non-effect wiring（在位）
- live implementation dry-run execution（在位）
- live runtime activation stub（在位）
- first real write rollout plan（冻结）
- real-write go/no-go gate（冻结）
- live code path dry-run（冻结 + 最小实现）
- 当前 `side_effects_released` 仍强制锁死为 `false`

---

## 1. 文档定位（写死）

这是第一版 `live implementation minimal implementation` 的“**真实代码开始执行**”定义文档。当前目标是冻结“从 code path dry-run 到第一版真实代码真正开始执行”的边界：开始前必须满足什么、开始那一刻系统状态应是什么、开始后最小允许发生什么、失败时必须如何立即收口。

并写死：

- 本轮只做 definition 冻结，不做真实代码实现、不做真实 rollout 启用。
- 不做真实 `rollback` / `interrupt`。
- 不接地图、不驱动语音/记忆、不改路线、不做中台真实迁移。
- 不改变现有主线行为。

---

## 2. 为什么现在必须先定义 first real code activation（写死理由）

- code path dry-run 已存在：证明未来真实代码壳子路径能零副作用走通。
- real-write go/no-go gate 已存在：证明“是否允许开始”已冻结。
- rollout plan 已存在：证明“如何受控试运行”已冻结。
- 但仍缺一份明确的定义去回答：**第一版真实代码什么时候才算真正开始执行**，以避免把以下四者混为一体：
  - go/no-go 通过
  - rollout approval
  - activation allowed
  - real execution start

因此必须先冻结 first real code activation definition，再考虑真实代码落地。

---

## 3. 最小定义（写死）

`release_control first live guarded implementation minimal real-effect live implementation first real code activation` 是：

- 从 `live code path dry-run == executed` 到“第一版真实最小写入代码真正进入执行态”的边界定义。
- 只定义真实代码开始执行的前提、进入条件、允许面与失败收口。
- 不等于真实代码已经写完，不等于业务全链路完成，不等于中台迁移完成。

---

## 4. 最小合法输入（写死；只允许标准化对象）

只允许消费（只读）：

- live implementation definition 已冻结
- live implementation skeleton / stub / minimal code skeleton 已存在
- live implementation admission & acceptance 已冻结
- live implementation minimal implementation plan 已冻结
- live implementation non-effect wiring == wired_ready
- live implementation dry-run execution == executed
- live runtime activation stub 已存在
- first real write rollout plan 已冻结
- real-write go/no-go gate == go
- live code path dry-run == executed
- activation / commit / pre-commit / launch / admission 全链路 admitted/ready
- execution_state / result / exception_or_failure path 在位
- `side_effects_released == false`
- **显式 real-code-activation approval / signal 存在**
- **默认开关仍为 false（默认不开）**

并明确（写死）：

- 缺任一主前提，first real code activation 不成立。
- 禁止读取 `request_* / approved_* / raw metadata` 作为直驱依据。

---

## 5. 最小状态集合（写死；三态）

最小状态集合收敛为三态：

- `first_live_minimal_real_effect_real_code_activation_ready`
- `first_live_minimal_real_effect_real_code_activation_not_ready`
- `first_live_minimal_real_effect_real_code_activation_blocked`

并明确（写死）：

- `...activation_ready` 只表示“第一版真实代码已具备开始执行条件”。
- 不表示真实写入已经完成。
- 不表示 rollout 已默认开启。
- 不表示 `side_effects_released` 已长期开启。

---

## 6. 最小允许面（写死）

第一版真实代码一旦真正开始执行（进入 activation scope 后）**只允许**触达三类真实副作用：

- `execution_state_real_write`
- `result_object_real_write`
- `exception_or_failure_real_write`

除此以外全部禁止（route/voice/memory/migration/rollback/interrupt/map 等）。

---

## 7. “真正开始执行”的最小开始条件（写死）

写死区分以下边界：

- **准备态**：go/no-go == go、rollout plan 冻结在位、code path dry-run 已 executed、activation gate/dry-run 满足、`side_effects_released==false`，但尚未进入任何真实激活语义。
- **真正开始执行（real execution start）**：仅当满足全部上游前提且 `side_effects_released==false`，并收到 **显式 real-code-activation approval/signal** 后，才允许通过 `live runtime activation stub` 所代表的“唯一激活承载位语义”进入受控短时激活范围。

并写死：

- 进入开始执行态 **不等于成功完成**。
- 一旦进入后，必须仍受 activation contract 与 live implementation definition 的顺序/允许面约束。

---

## 8. 最小失败收口（写死）

任一异常必须按固定顺序收口：

1) **先恢复 `side_effects_released=false`**  
2) 写失败/退出态 `execution_state`  
3) 写失败 `result_object`  
4) 写 `exception_or_failure`  
5) 交还治理链  

并明确（写死）：

- 不允许失败后扩权补救
- 不允许保留半开启状态

---

## 9. 明确禁止（写死）

first real code activation definition 不允许放行以下任何内容：

- route change
- voice output
- memory write
- mid-platform real migration
- rollback
- interrupt
- map/path planning side-effect source
- 越过标准对象吐散字段
- 默认开启 `side_effects_released`

---

## 10. 与现有链路的关系（写清）

- 与 go/no-go gate：gate 定“能不能开始”；本 definition 定“开始的精确定义（何时算真正进入真实执行）”。
- 与 rollout plan：rollout plan 定试运行策略；本 definition 定真实代码开始执行的边界（起点/终点/成功失败最小态）。
- 与 code path dry-run：dry-run 证明代码路径零副作用可走通；本 definition 定义何时真正跨入真实执行。
- 与 live implementation minimal implementation plan：plan 定实现方式；本 definition 定执行起点边界与失败收口规则。

---

## 11. 当前仍然不能做什么（写死）

- 不允许现在就打开 `side_effects_released`
- 不允许真实写入
- 不允许真实 `release_control`
- 不允许真实 rollout 默认开启
- 不允许真实 `rollback` / `interrupt`
- 不允许 route / voice / memory / migration
- 不允许把 definition 当作真实代码已执行

---

## 12. 当前不做（写死）

- 不做真实代码实现
- 不做真实 rollout 开启
- 不做地图接入
- 不做语音/记忆联动
- 不做中台真实迁移

---

## 13. 下一步边界（写死）

- 本轮之后，下一步才考虑：
  - 第一版真实最小写入代码的最小实现
- 若进入代码：只允许最小实现，不允许扩面
- 当前不直接落真实实现

