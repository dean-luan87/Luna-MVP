# Luna — Navigation Governance Action Release Control Input Contract v0（Release Control 动作级输入契约：设计冻结）

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_INPUT_CONTRACT_V0.md`  
**性质**：Phase-Next-51：冻结 `release_control` 子动作未来**唯一允许消费**的动作级输入契约（不落代码、不触发真实动作）

基于（已具备）：
- release_control 最小定义冻结：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_MINIMAL_DEFINITION_V0.md`
- release_control 模块骨架：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_SKELETON_V0.md`
- 执行器总输入对象（冻结/实现）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_EXECUTOR_INPUT_OBJECT_V0.md`、`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_EXECUTOR_INPUT_OBJECT_IMPLEMENTATION_V0.md`
- 就绪门控（冻结/实现）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_EXECUTOR_READINESS_GATE_V0.md`、`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_EXECUTOR_READINESS_GATE_IMPLEMENTATION_V0.md`
- 接线边界（冻结/实现）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_EXECUTOR_WIRING_V0.md`、`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_EXECUTOR_WIRING_IMPLEMENTATION_V0.md`
- 输入契约占位输出：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_INPUT_CONTRACT_PLACEHOLDER_V0.md`
- 输入契约正式实现版：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_INPUT_CONTRACT_IMPLEMENTATION_V0.md`
- release_control 子动作就绪门控（冻结）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_READINESS_GATE_V0.md`
- release_control executor input bridge（冻结）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_EXECUTOR_INPUT_BRIDGE_V0.md`
- release_control executor input bridge（最小非动作实现）：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_EXECUTOR_INPUT_BRIDGE_IMPLEMENTATION_V0.md`

---

## A. 文档定位（写死）

- 这是 `release_control` 子动作的最小输入契约文档。
- 当前目标：冻结动作级输入面边界（可冻结、可回归）。
- 当前不做真实 `release_control` 实现。
- 当前不做 `rollback` / `interrupt`。
- 当前不做地图接入。
- 当前不做语音/记忆联动。
- 当前不改变现有主线行为（不改 route/proposal，不触发中台真实迁移）。

---

## B. 为什么现在必须先定义动作级输入契约

- 当前已经有治理动作执行器**总输入对象**（`navigation_governance_action_executor_input_v0`）。
- 但 `release_control` 作为第一类真实动作，不应直接“原样吃总输入对象所有字段”，否则容易：
  - 读取超出边界的字段（越权）
  - 顺手耦合 `rollback` / `interrupt` 逻辑（污染子动作边界）
  - 让子动作变成“隐式总执行器”（不可回归）
- 因此必须先冻结 `release_control` 的专属输入契约：**从总输入对象中裁切出它唯一允许消费的最小字段集合**。

---

## C. release_control 输入契约的最小定义（写死）

release_control 输入契约是：

- 从治理动作执行器总输入对象中，收束出 `release_control` 子动作**唯一允许消费**的最小输入面。

它不是（写死）：

- 总输入对象本身
- approval boundary
- readiness gate
- wiring 结果
- status object
- `rollback` / `interrupt` 的共享输入面

核心一句（写死）：

**release_control 只允许消费为它单独批准、单独约束、单独确认过的最小输入字段集合。**

---

## D. 最小主输入（写死）

1) implemented `navigation_governance_action_executor_input_v0`  
- 这是主输入来源。
- 且其中动作类型必须明确对应 `release_control`。

并写死：

- 若动作类型不是 `release_control`，则该输入契约不成立。
- 不能拿 `rollback_request` 或 `interrupt` 的对象兼容代替。

---

## E. 最小辅助依据（只作一致性校验；不得扩权）

以下仅用于确认链路仍在位与一致性（写死为辅助，不替代主输入）：

1) implemented `navigation_governance_action_executor_readiness_gate_v0`  
- 只用于确认当前仍处在“允许进入动作候选”的范围内（例如 `ready_candidate`）。

2) implemented `navigation_governance_action_executor_wiring_v0`  
- 只用于确认当前是否已合法接到 skeleton（例如 `wired_inactive` / `wired_action_ready`）。

3) implemented `navigation_governance_action_approval_status_v0`  
- 只用于确认批准层状态一致性（不等于真实批准链执行）。

4) implemented `navigation_governance_action_status_v0`  
- 只用于确认状态回传承载面在位（不等于动作已发生）。

写死约束：

- 这些都是辅助一致性依据；不得扩权为“直接可执行命令”。

---

## F. 明确禁止读取的内容（必须写死）

`release_control` 子动作不得直接读取：

- 任意普通 `request_*`
- 任意普通 `approved_*` 散字段（非标准化对象内的字段片段）
- 任意 raw metadata
- 任意地图 / 路径规划字段
- 任意语音输出字段
- 任意记忆写入字段
- 任意 `rollback` 专属字段
- 任意 `interrupt` 专属字段
- 任意中台迁移执行字段

解释（写死）：

- 这些字段不属于 `release_control` 子动作的最小输入契约。
- 读取它们会破坏动作边界，并把子动作变成越权入口。

---

## G. 最小字段类别（只定义类别，不做细表）

建议最小字段类别（收敛，不发散）：

1) **动作类型确认类**  
- 确认当前就是 `release_control`

2) **执行前提确认类**  
- 确认当前只是候选成立（readiness/wiring/在位性一致），不等于可立即执行

3) **约束确认类**  
- 明确当前仍受哪些硬约束约束（例如不改路线、不语音、不迁移等）

4) **目标控制面类**  
- 明确该动作作用的是“控制权交还上游”这一面，不扩展到路线或播报

---

## H. 最小必需类别（写死）

最小必需类别至少包括：

- 动作类型确认类
- 执行前提确认类
- 约束确认类

并写死：

- 没有这些，`release_control` 输入契约不成立。
- 目标控制面类可先做最小语义占位，但未来必不可少。

---

## I. 当前最小语义（写死）

当 `release_control` 输入契约成立时，只表示：

- 上游已为 `release_control` 子动作整理出最小合法输入面。
- `release_control` skeleton 未来可基于此设计正式消费。

它不表示：

- 真实 `release_control` 已执行
- 控制权已真实交还
- 路线已改变
- 中台已真实迁移

---

## J. 当前不允许做什么（必须写死）

- 不允许直接做真实 `release_control`
- 不允许借输入契约顺手做 `rollback` / `interrupt`
- 不允许读取地图/语音/记忆/迁移字段
- 不允许把输入契约成立当作动作已执行
- 不允许把输入契约当成总执行器输入对象的完全替代

---

## K. 与现有链路的关系（写清）

### 与 governance action executor input object

- 总输入对象是来源。
- `release_control input contract` 是其子动作级裁切输入面。
- 两者不能混用。

### 与 readiness / wiring

- readiness / wiring 提供辅助一致性依据。
- 但不直接替代子动作输入契约。

### 与 approval status / action status

- 只用于确认链路在位与一致性。
- 不直接构成动作主输入。

### 与 release_control skeleton

- skeleton 未来只应消费该动作级输入契约。
- 当前 skeleton 不执行真实动作。

---

## L. 当前不做（必须写死）

- 不做 input contract 代码实现
- 不做真实 `release_control`
- 不做 `rollback` / `interrupt`
- 不做地图接入
- 不做语音/记忆联动
- 不做中台真实迁移

---

## M. 下一步边界（写死）

- 本轮之后，下一步才考虑：
  - `release_control input contract` placeholder / implementation
- 再之后才考虑：
  - `release_control` 最小真实实现
- 当前不跨这两步

---

## N. 未来输入契约样例（仅说明，不落代码）

```json
{
  "release_control_input_contract_present": true,
  "release_control_input_contract_scope": "navigation_governance_action_release_control_input_contract_v0",
  "action_type_confirmed": "release_control",
  "execution_prerequisites_consistent": false,
  "constraint_profile": "release_control_minimal_constraints",
  "control_surface": "upstream_control_handover_only"
}
```

