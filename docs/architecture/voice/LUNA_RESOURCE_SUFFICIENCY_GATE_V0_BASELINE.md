# Resource Sufficiency Gate v0 Baseline / Freeze（资源不足准入冻结面）

**文件**：`docs/architecture/voice/LUNA_RESOURCE_SUFFICIENCY_GATE_V0_BASELINE.md`  
**性质**：Topic 01 下已落地 gate 的阶段冻结面（可维护、可回归）  
**目标**：把当前已实现并验证通过的“资源不足 pre-submit 准入 gate”固定边界、输入、落点与验证入口，防止后续扩展漂移。  

上位约束（必须服从）：  
- `docs/architecture/voice/LUNA_CONFLICT_GOVERNANCE_CONSTITUTION_V0.md`  
- `docs/architecture/voice/LUNA_CONFLICT_TOPIC_01_USER_REQUEST_VS_SYSTEM_JUDGEMENT_V0.md`  
- `docs/architecture/voice/LUNA_VOICE_MAINLINE_BASELINE.md`  

---

## A. 当前基线范围

**当前只批准一个执行准入 gate**：Resource Sufficiency Gate v0  

**当前只覆盖两类资源条件**（最小集）：  
- `battery_ok`（电量是否足够）  
- `required_modules_ok`（必要模块是否可用）  

**当前未覆盖（明确不做）**：  
- 风险冲突 gate  
- 信息完整性 gate  
- 用户坚持继续执行时的协商策略  
- 中台审核关系  
- 白盒 / provenance  

---

## B. 当前系统定位

- 这是一个 **pre-submit execution admission gate**：只决定“是否允许进入 submit”。  
- 它**不是**主链裁决器：  
  - 不改 `dispatch_type`  
  - 不改 `bridge_decision.route`  
  - 不改 `proposal.device_action`  
- 它不改：reply / semantic shadow / assisted routing / vision shadow 的任何逻辑。  
- 它只影响：是否调用 `_maybe_submit_real_output_v1(...)`。

---

## C. 当前唯一输入来源（v0）

**只读**：`runtime_context.metadata["resource_status_v0"]`

建议最小结构（由外部/测试注入）：  

```json
{
  "battery_ok": true,
  "required_modules_ok": true,
  "reason": ""
}
```

硬约束：  
- **缺失该字段时**：默认不拦截（主链行为保持不变）  
- 本 gate **不允许**模块自造资源事实  
- 资源状态必须来自外部注入（中台/系统）或测试注入  

---

## D. 当前 gate 行为（写死）

### 通过条件

满足任一即放行：  
- `resource_status_v0` 缺失（或不是 dict）  
- `battery_ok == true` 且 `required_modules_ok == true`  

### 拒绝条件

当 `resource_status_v0` 存在且为 dict 时：  
- `battery_ok == false` → 拒绝  
- `required_modules_ok == false` → 拒绝  
- 两者都 false → 拒绝  

### 拦截范围（写死）

- gate 只拦截：`_maybe_submit_real_output_v1(...)`  
- gate 不改变：`dispatch_type` / `bridge_decision.route` / `proposal.device_action`

---

## E. `resource_gate_v0` 最小结构（metadata）

当 `resource_status_v0` **存在**时写入：`VoiceFinalTextDispatchResult.metadata["resource_gate_v0"]`

```json
{
  "gate_passed": true|false,
  "gate_reason": "ok|battery_insufficient|required_modules_unavailable|battery_and_modules",
  "gate_scope": "pre_submit_execution_admission_v0"
}
```

约束：  
- 缺失 `resource_status_v0` 时：当前默认 **不写** `resource_gate_v0`  
- 不包含 `timestamp/location/position/coordinate/lat/lng` 等字段  

---

## F. 当前明确禁止项（写死）

- 不允许辅助信号（语义/视觉/shadow/candidate 等）单独决定资源不足  
- 不允许资源状态缺失时脑补不足并拦截  
- 不允许资源 gate 改写主链裁决（route/dispatch/proposal）  
- 不允许在本 baseline 上直接扩展到风险 gate  
- 不允许在本 baseline 上顺手混入信息完整性 gate  
- 不允许把 gate 做成协商策略器  

---

## G. 当前验证入口（必须重跑）

改到以下任一处时必须重跑：gate 落点、`resource_status_v0` 读取方式、submit 准入逻辑。

- `tools/verify_voice_resource_gate_v0.py`  
- `tools/verify_voice_v1_minimal_flow.py`

这两个脚本构成当前阶段的最小验收入口。

---

## H. 下一阶段前置条件

- 若进入 **风险 gate**：必须单开专项设计与评审  
- 若进入 **信息完整性 gate**：必须单开专项设计与评审  
- 若进入 **协商/确认策略**：必须单开专项设计与评审  
- 后续任何扩展必须以本 baseline 为冻结面，不得直接叠加复杂逻辑

---

## 代码落点（事实索引）

- gate 逻辑：`capabilities/voice/runtime/voice_resource_gate_v0.py`  
- gate 落点：`capabilities/voice/runtime/voice_final_text_dispatcher.py`（`_apply_resource_sufficiency_gate_v0`；dispatch 后、submit 前）  
- 验证：`tools/verify_voice_resource_gate_v0.py`

