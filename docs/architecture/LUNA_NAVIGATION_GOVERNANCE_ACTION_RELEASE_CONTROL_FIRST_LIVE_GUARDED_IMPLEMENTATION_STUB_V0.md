# Luna — Navigation Governance Action Release Control First Live Guarded Implementation Stub v0（第一版真实受控实现：stub 承载位）

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_STUB_V0.md`  
**性质**：Phase-Next-85：把 guarded implementation definition 推进为“可进入、可观测、但仍不放权”的 guarded implementation stub（落代码；不触发真实动作）

关联：
- guarded implementation definition（冻结）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_DEFINITION_V0.md`
- approval gate（最小实现）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_ENABLEMENT_APPROVAL_GATE_IMPLEMENTATION_V0.md`
- launch dry-run（最小实现）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_LAUNCH_DRY_RUN_IMPLEMENTATION_V0.md`
- runtime contract / stub：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_MINIMAL_RUNTIME_CONTRACT_V0.md`、`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_MINIMAL_RUNTIME_STUB_V0.md`

---

## A. 文档定位（写死）

- 这是 `release_control first live guarded implementation` 的 stub 设计与落地文档。
- 当前目标：把 guarded implementation definition 推进到 guarded stub（最后一层代码承载位）。
- 当前不做真实 `release_control`。
- 当前不做 `rollback` / `interrupt`。
- 当前不做地图接入。
- 当前不做语音/记忆联动。
- 当前不触发中台真实迁移。
- 当前不改变现有主线行为（不改 route/proposal）。

---

## B. 为什么现在要做 guarded implementation stub

- guarded implementation definition 已冻结。
- 如果没有 guarded stub，后续会直接从定义文档跳到真实实现，缺少最后一次可演练、可观测的代码承载位。
- 因此必须先有一个“可进入、可观测、但不放权”的 stub。

---

## C. guarded implementation stub 的最小定义（写死）

- 它不是真实 `release_control`。
- 它不是 approval gate / launch dry-run / side-effect release gate。
- 它只是“第一版真实受控实现”的代码占位层。
- 只负责承载：入口检查、允许面占位、止损退出占位。

---

## D. guarded implementation stub 最小能力面（写死 5 个）

1) **stub 身份**：固定 identity / scope  
2) **guarded 输入接口占位**：未来只接受合法输入；当前不真实消费  
3) **execution state 受控更新接口占位**：未来只允许最小真实推进；当前只允许 safe placeholder update  
4) **result object 受控更新接口占位**：未来只允许最小真实写入；当前只允许 safe placeholder update  
5) **止损 / 退出接口占位**：未来按定义顺序止损；当前只返回 stop-safe / exit-safe / reported-placeholder  

---

## E. 默认行为（写死）

- 默认可识别 `guarded implementation candidate`
- 默认不打开 `side_effects_released`
- 默认不触发真实 `release_control`
- 默认不触发 route / voice / memory / migration
- 默认只返回 `guarded_stub_ready|guarded_stub_not_ready|guarded_stub_blocked|not_implemented`

---

## F. 与现有链路的关系（写清）

与 launch dry-run：
- launch dry-run 是真实执行前最后检查
- guarded implementation stub 是第一版真实受控实现的代码承载位
- 两者职责不同

与 approval gate：
- approval gate 决定是否批准第一次真实试运行
- guarded implementation stub 才是批准之后未来要进入的代码承载位
- `approved != entered_guarded_implementation`

与 side-effect release contract：
- contract 规定真实副作用只能落在哪些面
- guarded implementation stub 必须受它约束
- 当前仍不真正放权

---

## G. 当前不允许做什么（必须写死）

- 不允许把 `side_effects_released` 打开
- 不允许真实 `release_control`
- 不允许真实 `rollback` / `interrupt`
- 不允许改路线
- 不允许触发语音播报
- 不允许写记忆
- 不允许触发中台真实迁移
- 不允许绕过 guarded implementation definition / runtime contract

---

## H. 代码落点（本轮落地）

- `capabilities/governance/runtime/navigation_governance_action_release_control_first_live_guarded_implementation_stub_v0.py`

