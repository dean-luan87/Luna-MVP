# Luna — Navigation Governance Action Release Control First Live Guarded Implementation Skeleton v0（第一版真实受控实现：专用代码骨架冻结）

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_SKELETON_V0.md`  
**性质**：Phase-Next-87：冻结 `release_control` 第一版真实 guarded implementation 的 **专用代码骨架**（可冻结、可回归；当前仍不可放权、不可执行真实副作用）

基于（已具备）：
- guarded implementation definition（冻结）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_DEFINITION_V0.md`
- guarded implementation stub（承载位/演练壳子）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_STUB_V0.md`
- admission & acceptance（准入与验收总则冻结）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_ADMISSION_AND_ACCEPTANCE_V0.md`
- enablement approval gate / launch dry-run / release gates（冻结/最小实现）：见 definition 文档“基于（已具备）”段落
- minimal runtime contract（冻结）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_MINIMAL_RUNTIME_CONTRACT_V0.md`
- execution state / result（实现）：  
  `docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_EXECUTION_STATE_IMPLEMENTATION_V0.md`、  
  `docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_RESULT_OBJECT_IMPLEMENTATION_V0.md`

---

## A. 文档定位（写死）

这份文档是：

- `release_control first live guarded implementation` 的 **专用代码骨架**（skeleton）设计与落地文档。
- 当前目标：在 definition / stub / admission&acceptance 之后，把未来第一版真实 guarded implementation 的“专用实现壳子”独立出来，避免后续把 stub 硬改成真实实现导致边界混乱。

并且（本轮写死边界）：

- 当前不做真实 `release_control`。
- 当前不做真实 `rollback` / `interrupt`。
- 当前不做地图接入、不改路线。
- 当前不做语音/记忆联动。
- 当前不做中台真实迁移。
- 当前不改变现有主线行为。
- 当前 `side_effects_released` 仍强制锁死为 `false`（不允许打开）。

---

## B. 为什么现在要做 skeleton（写死理由）

当前已经具备：

- definition 已冻结（受控落地定义清晰）
- stub 已存在（可进入、可观测、但仍不放权的演练承载位）
- admission & acceptance 已冻结（什么时候允许开始写真实实现、如何验收/止损/回退已写死）

但仍缺少：

- 一个真正面向“未来真实实现”的 **专用模块壳子**（实现入口骨架）。

如果没有独立 skeleton，后续真实实现只能在 stub 上硬改，导致：

- stub 语义（演练壳子）
- skeleton 语义（未来真实实现壳子）
- guarded implementation 语义（受控真实实现）

混在一个文件里，标准对象、门控、回退与禁止面容易“被顺手绕过”。

因此必须先做 skeleton，把未来实现落点独立占出来，但继续保持不可放权、不可执行真实副作用。

---

## C. skeleton 的最小定义（写死）

`first live guarded implementation skeleton`：

- 不是 stub
- 不是 gate
- 不是 runtime contract
- 不是最终真实实现

它只是：

- “未来第一版真实 guarded implementation 的专用代码骨架（实现入口壳子）”

---

## D. skeleton 最小能力面（写死 5 项）

Skeleton 必须至少具备以下五类等价能力（均为占位接口；当前不执行真实副作用）：

1) skeleton 身份  
   - 固定 identity / scope
2) guarded implementation 输入接口占位  
   - 未来只接受 “approval + launch ready + release gates ready + state/result/failure 在位” 等合法输入  
   - 当前不真实消费，返回 skeleton_inactive / not_implemented
3) execution state 真实更新接口占位  
   - 未来允许真实推进（受 runtime contract 约束）  
   - 当前只返回 placeholder-safe / not_implemented
4) result object 真实写入接口占位  
   - 未来允许真实写入（受 runtime contract 约束）  
   - 当前只返回 placeholder-safe / not_implemented
5) failure / stop / exit 接口占位  
   - 未来按 admission & acceptance 的止损顺序执行  
   - 当前只返回 stop-safe / exit-safe / reported-placeholder（不吞语义）

---

## E. 默认行为（写死）

Skeleton 的默认行为必须写死为：

- 默认不打开 `side_effects_released`
- 默认不触发真实 `release_control`
- 默认不触发 `rollback` / `interrupt`
- 默认不触发 route / voice / memory / migration
- 默认只返回 `not_implemented` / `skeleton_inactive` / `placeholder-safe`

---

## F. 与现有链路的关系（写清；不能混用）

与 stub：

- stub 是“可进入、可观测、不可放权”的演练承载位
- skeleton 是“未来真实实现的专用壳子”
- 两者不能混用，也不能互相替代
- 真实实现不得直接在 stub 上硬改落地

与 admission & acceptance：

- admission & acceptance 决定何时允许真正开始写真实实现，以及写完如何验收/止损/回退
- skeleton 只是未来承接真实实现的模块位置
- 当前 skeleton **不等于** 已通过准入、也不表示允许开始真实实现

与 runtime contract / execution state / result object：

- skeleton 未来必须受 runtime contract 约束
- 未来只能通过标准对象（execution state / result object / failure path）写真实副作用
- 当前仍然不允许真实写入（全部 placeholder-safe）

---

## G. 当前不允许做什么（必须写死）

- 不允许把 `side_effects_released` 打开（必须保持 `false`）
- 不允许真实 `release_control`
- 不允许真实 `rollback` / `interrupt`
- 不允许 route / voice / memory / migration
- 不允许绕过 admission & acceptance / runtime contract / standard objects
- 不允许 skeleton 伪装成真实 live implementation（No Fabrication Rule）
- 不引入新的时间/空间字段，不接地图、不引入坐标依赖（统一时空锚点原则）

---

## H. 建议落点（写清）

Skeleton 最小、最连续、最不容易失控的落点是：

- `capabilities/governance/runtime/navigation_governance_action_release_control_first_live_guarded_implementation_skeleton_v0.py`

理由（写死）：

- 与现有 stub 同一模块域（`capabilities/governance/runtime/`），最连续、最小改动。
- 与 stub 分文件，避免语义混用（演练壳子 vs 未来实现壳子）。
- 保持所有真实副作用锁死（`side_effects_released=false`），并以默认返回 `not_implemented / placeholder-safe` 防止滑向真实实现。

