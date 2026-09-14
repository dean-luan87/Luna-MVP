# Luna — Navigation Governance Action Release Control Input Contract Placeholder v0（动作级输入契约占位输出）

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_INPUT_CONTRACT_PLACEHOLDER_V0.md`  
**性质**：Phase-Next-52：把 `release_control` 动作级输入契约实体化为只读占位输出（落代码；不可执行）

关联：
- 输入契约冻结：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_INPUT_CONTRACT_V0.md`
- release_control 最小定义冻结：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_MINIMAL_DEFINITION_V0.md`
- release_control skeleton：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_SKELETON_V0.md`
- 执行器总输入对象（实现）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_EXECUTOR_INPUT_OBJECT_IMPLEMENTATION_V0.md`
- readiness gate（实现）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_EXECUTOR_READINESS_GATE_IMPLEMENTATION_V0.md`
- wiring（实现）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_EXECUTOR_WIRING_IMPLEMENTATION_V0.md`
- 输入契约正式实现版：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_INPUT_CONTRACT_IMPLEMENTATION_V0.md`

---

## A. 文档定位（写死）

- 这是 `release_control` 子动作标准化输入契约的只读占位设计。
- 当前目标：让系统真正产出统一的 `release_control` 输入契约占位。
- 当前不做真实 `release_control`。
- 当前不做 `rollback` / `interrupt`。
- 当前不接地图。
- 当前不驱动语音/记忆。
- 当前不改变现有主线行为。

---

## B. 为什么现在要做 placeholder

- `release_control` 输入契约边界已经冻结，且 `release_control` skeleton 已存在。
- 执行器总输入对象、readiness、wiring 都已存在并可产出对象。
- 但系统里还没有统一的 `release_control` 动作级输入承载位；若缺失，后续真实接入会回到临时字段。
- 因此先把输入契约“实体化”为占位输出，验证未来可从总输入对象裁切出 `release_control` 唯一合法输入面。

---

## C. placeholder 的最小定义（写死）

- 它不是 `release_control` 执行器。
- 不是动作执行命令。
- 不是控制权已交还事实。
- 它只是“`release_control` 动作级输入契约”的只读占位实例。

---

## D. 当前最小输入（写死：只读标准化对象）

必须只读（缺一则 relevant-only 不写）：

1) `navigation_governance_action_executor_input_v0`（implemented）  
- 且动作类型必须是 `release_control`

2) `navigation_governance_action_executor_readiness_gate_v0`（只作一致性确认）

3) `navigation_governance_action_executor_wiring_v0`（只作一致性确认）

可选只读（仅辅助一致性校验，不得扩权）：

- `navigation_governance_action_approval_status_v0`
- `navigation_governance_action_status_v0`

写死：

- 若动作类型不是 `release_control`，则 placeholder 不成立。
- 不允许脑补；这些只是 placeholder 组装依据，不代表真实 `release_control` 已运行。

---

## E. 当前最小输出位（写死）

写入：

- `result.metadata["navigation_governance_action_release_control_input_v0"]`

最小结构（不加时间/空间字段，不膨胀复杂对象）：

```json
{
  "release_control_input_present": true,
  "release_control_input_scope": "navigation_governance_action_release_control_input_v0",
  "action_type_confirmed": "release_control",
  "execution_prerequisites_consistent": false,
  "constraint_profile": "release_control_placeholder_minimal_constraints",
  "control_surface": "upstream_control_handover_only",
  "consume_mode": "read_only"
}
```

---

## F. 当前最小字段组织原则（写死）

- 动作类型确认类：必须明确就是 `release_control`
- 执行前提确认类：当前只能占位，**不得**伪装成“可立即执行”
- 约束确认类：只给最小约束占位表达
- 目标控制面类：只允许“上游控制权交还”这一控制面
- 不允许扩展到路线、播报、记忆、中台迁移

---

## G. 当前最小结果语义（写死）

产出该对象只表示：

- 系统已能为未来 `release_control` 子动作预留统一输入契约承载位
- 后续真实模块可基于该对象设计正式消费

不表示：

- 真实 `release_control` 已执行
- 控制权已真实交还
- 路线已改变
- 中台已真实迁移

---

## H. 当前不允许做什么（写死）

- 不允许真实 `release_control`
- 不允许借该输入契约顺手做 `rollback` / `interrupt`
- 不允许直接改路线
- 不允许直接触发语音播报
- 不允许直接触发中台真实迁移
- 不允许把 `release_control_input_present == true` 当动作已执行或可立即执行

---

## I. 与现有链路的关系（写清）

- 总输入对象是来源；placeholder 是子动作级裁切输入面；两者不能混用。
- readiness / wiring 只是辅助一致性依据，不替代输入契约。
- skeleton 未来只应消费该动作级输入契约；当前不执行真实动作。
- action status 是执行后回传面；当前 placeholder 是执行前输入面；两者不能混用。

---

## J. 代码落点（本轮落地）

- Builder：`capabilities/governance/runtime/navigation_governance_action_release_control_input_placeholder_v0.py`
- 聚合写入：`capabilities/voice/runtime/voice_final_text_dispatcher.py`

