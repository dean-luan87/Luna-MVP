# Response Submit Template Interface v0 — Baseline / Freeze（冻结）

**文件**：`docs/architecture/voice/LUNA_RESPONSE_SUBMIT_TEMPLATE_V0_BASELINE.md`  
**性质**：主线已落地的“响应型 submit 统一接口面”冻结面（不是协商器，不是新 gate）。  

上位约束（必须服从）：  
- `docs/architecture/voice/LUNA_VOICE_MAINLINE_BASELINE.md`  
- `docs/architecture/voice/LUNA_VOICE_PRE_SUBMIT_ADMISSION_LAYER_V0.md`  
- `docs/architecture/voice/LUNA_CONFLICT_GOVERNANCE_CONSTITUTION_V0.md`  
- `docs/architecture/voice/LUNA_CONTINUE_REQUEST_CONFIRMATION_RESPONSE_V0_BASELINE.md`（当前唯一纳入的模板场景冻结面）  

---

## A. 当前基线范围（写死）

当前只冻结一件事：**Response Submit Template Interface v0（统一入口）**。

当前只纳入 1 个已存在模板场景（不扩类型）：  
- `continue_request_info_confirm_v0`（Continue Request + Information Confirmation Gate 命中时的固定确认模板）

当前未做（明确不做）：  
- 协商器 / 多模板中心 / 插件系统  
- 新 gate（Resource/Risk/Required-Fields 等）  
- 模型接入、视觉解释、白盒/provenance  
- `resume/repeat` 行为实现  

当前明确未纳入（写死）：  
- Resource Gate 拒绝模板  
- Risk 提示模板  
- 通用协商模板  
- `resume/repeat` 模板  
- 多模板分流系统

---

## B. 当前系统定位（写死）

- 这是一个**响应型 submit 统一接口**。  
- 它只负责：“被 gate 拦住后如何做响应型输出（解释/澄清/确认/拒绝模板）”。  
- 它不是主链裁决器。  
- 它不是执行型 submit。  
- 它不是协商器。  
- 它不改变 gate 结果。  
- 它不改变 `dispatch_type`。  
- 它不改变 `bridge_decision.route`。  
- 它不改变 `proposal.device_action`。  

---

## C. 执行型 submit vs 响应型 submit（冻结口径）

### 1) 执行型 submit（execution-kind）

- 用于主链任务/动作/正常流程推进  
- 受 admission layer gate 约束  
- **不得**被响应型模板绕过或替代

### 2) 响应型 submit（response-kind）

- 用于解释、澄清、确认、拒绝等系统响应  
- **不代表**原任务被放行  
- **不改变** gate 结果 / dispatch / route / proposal  
- v0 仅通过白名单 guard profile 放行已批准模板  
- v0 必须在 metadata 中明确：`submit_kind = "response_only"`

---

## D. 当前统一入口（代码事实）

统一入口函数（v0）：  
- `capabilities/voice/runtime/voice_final_text_dispatcher.py::_maybe_submit_response_template_v0(...)`

模板注册与规格（v0）：  
- `capabilities/voice/runtime/voice_response_submit_template_v0.py`  
  - `ResponseTemplateIdV0 = "continue_request_info_confirm_v0"`  
  - `get_response_submit_template_spec_v0(...)`

说明：  
- v0 仅注册 1 个模板 id；未注册的 id 必须不触发、不出声。  
- 统一入口必须经 `guard_v1_speakable_text(..., profile=spec.guard_profile)` 白名单放行。

兼容入口（wrapper，写死）：  
- Continue-request 的旧例外路径仅保留为 wrapper：  
  `capabilities/voice/runtime/voice_final_text_dispatcher.py::_maybe_submit_continue_request_info_confirmation_template_v0(...)`  
- 后续新增模板场景**不得**再直接写零散 submit 例外逻辑，必须接入统一入口。

---

## E. 当前 metadata 结构（冻结）

当响应型 submit 发生时，写入：  
- `result.metadata["response_submit_template_v0"]`

最小结构（v0）：  

```json
{
  "response_submitted": true,
  "response_type": "confirmation_template",
  "template_id": "continue_request_info_confirm_v0",
  "submit_kind": "response_only"
}
```

约束：  
- 未触发时可不写  
- 不加入 timestamp/location/coordinate 等字段  
- 不膨胀成诊断系统  

---

## F. 当前模板约束（写死）

- 当前只允许已批准模板通过统一接口（v0 仅 `continue_request_info_confirm_v0`）。  
- guard 仍以白名单/批准 profile 方式控制；统一接口**不等于**放宽出声权限。  
- 不允许未注册模板借此通道直接出声。  

---

## G. 当前明确禁止项（写死）

- 不允许把响应型 submit 误当作任务继续执行（不得视为执行型放行）。  
- 不允许在本 baseline 上直接扩成协商器。  
- 不允许把 gate 拦截后的任何输出都强行接入此接口（必须先有口径与冻结面）。  
- 不允许未经专题设计直接增加第二个模板类型。  
- 不允许因为用户继续请求就绕过 Information Gate。  

---

## H. 当前验证入口（必须重跑）

改到以下任一项时必须重跑：模板注册、guard profile 白名单、统一入口落点、metadata 结构。

- `tools/verify_response_submit_template_v0.py`  
- `tools/verify_continue_request_response_v0.py`  
- `tools/verify_voice_v1_minimal_flow.py`

---

## I. 与主线计划的关系

- 本 baseline 对应 `docs/architecture/voice/LUNA_VOICE_MAINLINE_NEXT_STEP_EXECUTION_PLAN_V0.md` 中的**第一落点**：把“被 gate 拦住后如何回应”工程化并收口成接口面。  
- 当前只完成最小接口面与回归入口，不代表已进入完整响应策略系统。  

---

## J. 后续接入纪律（写死）

任何新增响应型模板，必须先：  
1) 有专题/口径（或明确归属到已有专题的新增冻结面）  
2) 有最小实现  
3) 有 baseline/freeze  
4) 再纳入统一接口（注册 template_id + guard profile 白名单 + 回归脚本）  

禁止：直接把实验性模板挂到统一接口。  

---

## K. 为什么这还不是协商器/不等于放宽 gate

- 统一入口只做“**如何 submit 这句响应模板**”，不做“如何与用户协商”。  
- 统一入口不改变 admission gate 裁决，不放行执行型 submit。  
- v0 模板范围被写死为 1 个 template_id，且由 guard profile 白名单严格限制。

