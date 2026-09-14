# 冲突专题 04：Continue / Proceed Request Handling v0（设计冻结）

**文件**：`docs/architecture/voice/LUNA_CONFLICT_TOPIC_04_CONTINUE_REQUEST_HANDLING_V0.md`  
**性质**：冲突治理宪法 v0 之下的专题设计冻结（只做设计，不做实现）  
**目标（写死）**：把“用户要求继续/按我说的做/别停，但系统已有 gate 或判断不应继续”时的**最小响应策略口径**钉死，作为后续实现基线。  

上位约束（必须服从）：  
- `docs/architecture/voice/LUNA_CONFLICT_GOVERNANCE_CONSTITUTION_V0.md`（宪法高于专题）  
- `docs/architecture/voice/LUNA_VOICE_PRE_SUBMIT_ADMISSION_LAYER_V0.md`（gate 顺序与边界冻结）  
- `docs/architecture/voice/LUNA_VOICE_MAINLINE_BASELINE.md`（主线冻结面与硬约束）  

并强调（写死）：  
- **gate 结果高于用户继续偏好**  
- **主链事实高于辅助信号**  
- **No Fabrication Rule 继续成立**  
- **时空锚点只能消费中台统一基准**  

---

## A. 专题定位

- 这是冲突治理下的“继续请求（continue/proceed）”专题。  
- 只讨论：用户表达“继续执行/按我说的做/别停”时的**最小响应策略**。  
- 当前不实现：完整协商器。  
- 当前不实现：`resume` 执行逻辑（包括任务继续、设备继续、对话继续等）。  
- 当前不做：文本 vs 视角冲突处理。  
- 当前不做：中台审核实现。  

---

## B. 当前适用场景（v0）

至少覆盖三类：

1) **用户明确要求继续，但 Resource Gate 已拦截**  
- 例：电量/必要模块不足导致 `resource_gate_v0.gate_passed=false`，用户仍说“继续/按我说的做”。

2) **用户明确要求继续，但 Information Confirmation Gate 已拦截**  
- 例：存在指代词且无唯一绑定事实导致 `information_confirmation_gate_v0.gate_passed=false`，用户仍说“继续/就按那个做”。

3) **用户明确要求继续，且未来存在高风险候选，但当前尚未正式有 Risk Gate**  
- 例：`risk_summary_v1_gate_ready_eval_v0` 可观测到信息，但现阶段不允许据此拦截；用户说“别停/继续”时只能提示并为后续专题留接口。

---

## C. “继续请求”的最小输入组成（v0）

定义最小判断输入（概念结构）：

- **`user_request`**  
  - 当前句文本：`VoiceInputEvent.raw_text / normalized_text / wake_word_stripped`  
  - 路由决策：`router_decision`、`shortcut_id`、`is_task_mode`

- **`mainline_facts`**（唯一可作为主要依据）  
  - `dispatch_type`  
  - `bridge_decision.route`  
  - `proposal.device_action`（若存在，仅作事实）  

- **`admission_gate_status`**（以冻结的 gate 结果为准）  
  - `resource_gate_v0`（来自 `LUNA_RESOURCE_SUFFICIENCY_GATE_V0_BASELINE.md`）  
  - `information_confirmation_gate_v0`（来自 `LUNA_INFORMATION_CONFIRMATION_GATE_V0_BASELINE.md`）  

- **`session_state_anchor`**（只读事实锚，不做推断）  
  - `VoiceV1SessionStateAnchor.waiting_for_user / conversation_status / last_system_text / interrupted`

- **`semantic_output`**（只能辅助识别“继续意图”，不得夺权）  
  - `event.metadata["luna_voice_semantic_v2"]` 中的 `intent`（尤其 `control.resume`、`confirm.yes/no`）  

- **`supporting_signals`**（辅助信号，不能单独放行/拒绝）  
  - `semantic_v2_shadow / assist`（观测/对照）  
  - `risk_summary_v1_gate_ready_eval_v0`（只读观测；非 gate）  

硬约束（写死）：  
- **主链事实与已存在 gate 结果优先**。  
- 语义层仅辅助识别用户表达，不能单独决定“继续执行”。  
- 辅助信号不能单独放行继续执行，也不能绕过 gate。  

---

## D. 继续请求的最小处理口径（工程化规则）

1) **当前无 gate 拦截**  
- 系统按主链正常处理。  
- 本专题不额外夺权、不新增裁决。  

2) **被 Resource Gate 拦截**  
- 用户继续请求不得直接放行。  
- 必须明确告知资源不足（不伪装可执行）。  
- 响应优先落到：**明确拒绝** 或 **保守降级**。  
- 禁止：用户坚持覆盖资源不足。  

3) **被 Information Confirmation Gate 拦截**  
- 用户继续请求不得直接放行。  
- 必须优先要求确认/补齐必要信息。  
- 禁止：跳过必要确认。  

4) **未来若存在高风险候选（但尚未有正式 Risk Gate）**  
- 当前阶段只允许“提示/风险提醒”，不得据候选直接拒绝或拦截 submit。  
- 必须为后续 Risk Gate / 协商器保留接口（专题级口径，不在本轮实现）。  

---

## E. 最小响应等级映射（5 档）

将宪法的 5 档响应映射到本专题（v0 口径）：

- **直接执行**：无 gate 拦截；主链按既定逻辑继续。  
- **提示后执行**：本专题 v0 不主动引入；仅在“无 gate 拦截且存在轻提示”时由主链/其他专题决定。  
- **要求确认**：Information Confirmation Gate 拦截时（至少）。  
- **保守降级**：Resource Gate 拦截但存在可替代的“非执行型安全输出”时（例如仅提示、不执行）。  
- **明确拒绝**：Resource Gate 拦截且无安全替代；或继续请求试图覆盖宪法底线/硬约束时。

明确口径（写死示例规则）：  
- **资源不足** → 通常落到“明确拒绝/保守降级”。  
- **信息不足** → 至少落到“要求确认”。  
- **无 gate 拦截** → 不额外升级处理。  

---

## F. 当前明确禁止项（写死）

- 不允许因为用户说“继续”就覆盖 Resource Gate  
- 不允许因为用户坚持就跳过 Information Confirmation Gate  
- 不允许仅凭 `semantic_v2` 命中 `control.resume` 就实现继续执行  
- 不允许在本专题里顺手实现 `resume/repeat` 的行为逻辑（仅讨论响应口径）  
- 不允许在本专题里混入文本 vs 视角冲突处理  

---

## G. 推荐的最小未来落点（只做设计，不实现）

**唯一推荐未来落点（v0）**：在 `dispatch_voice_final_text(...)` 内，**既有 gate 结果形成后、submit 之前**，增加一个“Continue/Proceed 响应策略层（只生成响应决策/模板，不改 dispatch）”。  

为什么是这里：  
- 已具备 `dispatch_type/route/proposal` 与 `resource_gate_v0/information_confirmation_gate_v0` 等主链事实；  
- 能在不改主链分流的前提下，输出“拒绝/要求确认/保守降级”的响应策略；  
- 避免把冲突治理塞进 `SemanticConverterV2`（防止语义层夺权）。  

本轮只冻结落点，不实现。

---

## H. 为什么 `resume` 还不能直接实现（必须写死）

`继续/恢复（resume）` 具有天然歧义，当前不可直接实现行为逻辑：

- “继续”可能指：  
  - 继续任务（task lifecycle：暂停→恢复）  
  - 继续设备输出（例如继续播报）  
  - 继续对话（只是让系统继续说）  
  - 继续执行某个被 gate 拦下的动作（试图覆盖 gate）  
- 当前缺少稳定的：  
  - reference binding / 目标对象绑定结构（尤其 Topic 02 仍极保守）  
  - task context / task lifecycle 的主链 schema（可作为“恢复哪个任务”的事实依据）  
  - 冲突治理策略器与执行层闭环（继续之后到底做什么、如何证明已执行）  
- 因此：本专题只能先定义“继续请求的响应口径”，不能直接实现 `resume` 行为。

---

## I. 下一步最小实现建议（只给 1 个方向）

**建议最先落地**：当 **Information Confirmation Gate 拦截**时的固定“要求确认”响应模板 v0（只影响可说话提示范围，不改变主链分流与 gate 裁决）。  

**状态**：上述方向已以 **Continue Request Confirmation Response v0** 落地并冻结，见 §J。

---

## J. 已冻结实现（Baseline / Freeze）

- **Continue Request Confirmation Response v0 Baseline**（触发条件、唯一模板、**响应型 submit vs 执行型 submit**、验证入口）：  
  `docs/architecture/voice/LUNA_CONTINUE_REQUEST_CONFIRMATION_RESPONSE_V0_BASELINE.md`  

写死口径：该实现是 **响应型 submit 例外路径**，不是任务继续、不是 `resume` 行为，也不放宽 Information Gate 对**执行型 submit**的拦截。

