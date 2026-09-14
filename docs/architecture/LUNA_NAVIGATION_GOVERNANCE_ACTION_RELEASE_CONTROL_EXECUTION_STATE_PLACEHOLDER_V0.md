# Luna — Navigation Governance Action Release Control Execution State Placeholder v0（子动作执行过程状态对象占位输出）

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_EXECUTION_STATE_PLACEHOLDER_V0.md`  
**性质**：Phase-Next-65：把 `navigation_governance_action_release_control_execution_state_v0` 实体化为只读占位输出（落代码；不可执行）

关联：
- execution state 边界冻结：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_EXECUTION_STATE_V0.md`
- release_control skeleton：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_SKELETON_V0.md`
- 输入契约实现版：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_INPUT_CONTRACT_IMPLEMENTATION_V0.md`
- 状态对象实现版：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_STATUS_OBJECT_IMPLEMENTATION_V0.md`
- 子动作 wiring（实现）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_WIRING_IMPLEMENTATION_V0.md`
- 结果对象实现版：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_RESULT_OBJECT_IMPLEMENTATION_V0.md`

---

## A. 文档定位（写死）

- 这是 `release_control` 子动作标准化执行状态对象的只读占位设计。
- 当前目标：让系统真正产出统一的 `release_control execution state` 占位。
- 当前不做真实 `release_control`。
- 当前不做 `rollback` / `interrupt`。
- 当前不接地图。
- 当前不驱动语音/记忆。
- 当前不改变现有主线行为。

---

## B. 为什么现在要做 placeholder

- `release_control execution state` 边界已经冻结。
- `release_control skeleton` 已存在。
- `release_control` 输入契约实现版、状态对象实现版、子动作 wiring、结果对象实现版都已存在。
- 但系统里还没有统一的 `release_control execution state` 输出位；若缺失，后续真实接入会回到临时过程状态字段并污染“过程面 vs 结果面”的边界。
- 因此必须先把 `release_control execution state` “实体化”为占位输出。

---

## C. placeholder 的最小定义（写死）

- 它不是 `release_control` 执行器。
- 不是动作完成事件。
- 不是控制权已交还事实。
- 只是“`release_control` 子动作标准化执行状态对象”的只读占位实例。
- 作用：验证系统未来能否把 `release_control` 子动作执行过程状态收束成统一回传对象。

---

## D. 当前最小输入（写死：只读标准化对象）

必须只读（缺一则 relevant-only 不写）：

1) `navigation_governance_action_release_control_status_v0`（主输入；仅当存在且合法才进入组装）  
2) `navigation_governance_action_release_control_wiring_v0`（一致性确认：仍处在合法接线链路内）  

可选只读（仅辅助一致性校验，不得扩权）：

- `navigation_governance_action_release_control_result_v0`
- `navigation_governance_action_release_control_readiness_gate_v0`

写死：不允许脑补；这些只是 placeholder 组装依据，不代表真实 `release_control` 已运行。

---

## E. 当前最小输出位（写死）

写入：

- `result.metadata["navigation_governance_action_release_control_execution_state_v0"]`

最小结构（建议）：

```json
{
  "release_control_execution_state_present": true,
  "release_control_execution_state_scope": "navigation_governance_action_release_control_execution_state_v0",
  "release_control_execution_state": "not_started_placeholder|blocked_placeholder|unresolved_placeholder",
  "action_type_confirmed": "release_control",
  "effect_state": "unknown_not_applied",
  "route_binding_ready": false,
  "consume_mode": "read_only"
}
```

要求（写死）：
- 不加时间/空间字段
- 不膨胀成复杂对象
- 只表达“统一 execution state 已形成占位实例”

---

## F. 当前最小字段组织原则（写死）

- 执行状态类：只能占位，不得伪装 `executing/completed_candidate/failed` 真实事实
- 动作类型确认类：必须明确就是 `release_control`
- 异常/阻断状态类：只能占位，不得伪装真实失败处理已发生
- 执行影响类：只能用 `unknown_not_applied` 等占位表达
- 回传绑定/路由类：只能 ready/not-ready 占位，不做真实绑定

---

## G. 当前最小结果语义（写死）

当 `navigation_governance_action_release_control_execution_state_v0` 被产出时，只表示：

- 系统已能为未来 `release_control` 子动作预留统一执行状态对象承载位
- 后续真实 `release_control` 模块可基于该对象设计正式回传

它不表示（写死）：

- 真实 `release_control` 已执行
- 控制权已真实交还
- 路线已改变
- 中台已真实迁移
- 最终结果对象已成立

---

## H. 当前不允许做什么（写死）

- 不允许真实 `release_control`
- 不允许借该 execution state 顺手做 `rollback` / `interrupt`
- 不允许直接改路线
- 不允许直接触发语音播报
- 不允许直接触发中台真实迁移
- 不允许把 `release_control_execution_state_present == true` 当动作已执行

---

## I. 与现有链路的关系（写清）

与 release_control input contract：
- input contract 是执行前输入面  
- execution state placeholder 是执行过程面占位  
- 两者不能混用

与 release_control status object：
- status object 偏子动作状态观察面  
- execution state placeholder 偏执行过程面占位  
- 两者不能混用，也不能互相替代

与 release_control result object：
- result object 偏最终结果面  
- execution state placeholder 偏过程面  
- 两者不能混用，也不能用 result object 替代 execution state

与 release_control wiring：
- wiring 是进入子动作层前的接线结果  
- execution state placeholder 发生在动作过程之中（语义位置）  
- 不能跨层替代

与 release_control skeleton：
- skeleton 未来应通过该对象回传执行过程状态  
- 当前 skeleton 不执行真实动作

---

## J. 代码落点（本轮落地）

- Builder：`capabilities/governance/runtime/navigation_governance_action_release_control_execution_state_placeholder_v0.py`
- 聚合写入：`capabilities/voice/runtime/voice_final_text_dispatcher.py`

