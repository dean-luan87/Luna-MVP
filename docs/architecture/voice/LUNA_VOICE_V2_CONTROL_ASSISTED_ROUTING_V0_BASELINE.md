# Luna Voice V2 — Control Assisted Routing v0 Baseline（冻结面）

**定位**：把当前已验证通过的 `control.stop` / `control.cancel` “受控辅助信号消费机制”冻结为阶段基线。  
**目标**：形成可维护、可复跑的观察基线，防止后续横向复制 helper 导致边界漂移。  
**硬要求**：主链行为不变；语义层不拥有独立裁决权；不接模型；不扩 reply；不碰视觉；不改长链编排。

---

## A. 当前基线范围

**当前仅批准（已闭环验证通过）**：
- `control.stop`
- `control.cancel`

**当前未批准（写死禁止）**：
- `control.resume`（**暂缓**：与 `task_lifecycle` 的「继续任务/继续」存在天然歧义，需单独冲突治理设计）
- `control.repeat`
- `control.end_conversation`
- `confirm.*`
- `ask.*`
- `unknown`

---

## B. 当前系统定位

- 这是 **Control Assisted Routing v0** 的“观察基线 + 受控消费”冻结面。  
- **语义层只是辅助信号**：只能在“主链已成立事实”的前提下，被主链消费为确认信号。  
- **不是主链裁决器**：不得改写 `dispatch_voice_final_text(...)` 的分流结果。  
- **不是执行驱动层**：不得触发 stop/cancel 的执行，不改 `submit`，不改 proposal 业务含义。  
- **不是 reply 控制层**：不得扩对话能力边界。

---

## C. 四层结构（当前已完成）

当前控制类的受控辅助机制固定为四层：

1. **semantic intent recognition**  
   - 来源：`RuleBasedSemanticConverterV2`  
   - 承载：`VoiceInputEvent.metadata["luna_voice_semantic_v2"]`

2. **semantic shadow consume（影子消费）**  
   - 承载：`VoiceFinalTextDispatchResult.metadata["semantic_v2_shadow"]`  
   - 作用：只读对照语义与主链分流关系，不改任何行为

3. **semantic assist candidate（辅助候选）**  
   - stop：`metadata["semantic_v2_assist_v0"]`（`semantic_intent="control.stop"`）  
   - cancel：`metadata["semantic_v2_assist_v0_cancel"]`（`semantic_intent="control.cancel"`）  
   - 作用：在严格准入条件成立时，标记“可被消费的辅助信号候选”

4. **semantic assist consumption（辅助信号消费）**  
   - stop：`metadata["semantic_v2_assist_consumption_v0"]`  
   - cancel：`metadata["semantic_v2_assist_consumption_v0_cancel"]`  
   - 作用：**只在主链已明确为对应 device_action** 且 candidate=true 时，标记“辅助信号已被主链消费（确认信号）”

**状态**：
- `control.stop`：1–4 全部完成  
- `control.cancel`：1–4 全部完成

---

## D. 准入与消费规则（保守写死）

### D1. assist candidate（stop/cancel 同构）

candidate 必须同时满足：
- `semantic_intent` **严格匹配**（`control.stop` 或 `control.cancel`）
- `semantic_v2_shadow.shadow_status == "matches_current_flow"`
- `dispatch_type == "short_controlled_input"`
- `bridge_decision.route == BridgeRouteType.DEVICE_CONTROL`
- 语义包 `confidence >= 0.8`

否则一律 `assist_candidate=false` 或不写（当前实现对 stop/cancel 均写入 no-signal / false 结构）。

### D2. assist consumption（比 candidate 更严格）

consumption 必须同时满足：
- 对应的 `assist_candidate == true`
- `dispatch_type == "short_controlled_input"`
- `bridge_decision.route == BridgeRouteType.DEVICE_CONTROL`
- **主链 proposal 事实已明确**：
  - stop：`DeviceActionProposal.device_action == "stop"`
  - cancel：`DeviceActionProposal.device_action == "cancel"`
- 明确语义：这不是“semantic says X therefore do X”，而是“main flow already is X, semantic assist present, therefore mark consumed”

---

## E. 当前验证入口（改链路必须重跑）

**语义层（规则 v0）验证**：
- `tools/verify_semantic_converter_v2_rule_based.py`

**shadow consume 验证**：
- `tools/verify_semantic_converter_v2_shadow_consume.py`

**stop**：
- candidate：`tools/verify_semantic_converter_v2_assist_stop_candidate.py`
- consumption：`tools/verify_semantic_converter_v2_assist_stop_consumption.py`

**cancel**：
- consumption（含 candidate+consumption 镜像验证）：`tools/verify_semantic_converter_v2_assist_cancel_consumption.py`

**V1 主链闭环（必须不被破坏）**：
- `tools/verify_voice_v1_minimal_flow.py`

---

## F. 当前明确禁止项（写死）

- 不允许语义层独立裁决 stop/cancel  
- 不允许改写 `dispatch_voice_final_text(...)` 的 route / dispatch_type  
- 不允许改 proposal 的业务语义（proposal 仍为 Voice→Core 候选，不可直接执行）  
- 不允许绕过 No Fabrication Rule  
- 不允许自造系统级时间/空间锚点（禁止在 assist/cosumption metadata 中加入 timestamp/location/position/coordinate 等字段）  
- 不允许直接扩展到 `control.resume`（必须先做冲突治理设计，不得沿用 stop/cancel 模板机械复制）

---

## G. 下一阶段前置条件（扩第三个 intent 前必须满足）

- 以本 baseline 作为**冻结面**：新增第三个 intent 前，必须明确写出该 intent 的冲突面、主链事实来源、以及为何不会让语义夺权。  
- 若未来要接 `control.resume`：必须先单独设计与 `task_lifecycle` 的冲突治理（尤其是“继续/继续任务”歧义），不得按 stop/cancel 模板直接复制。

