# Luna Voice V2 — Assisted Consumption Interface v0（受控消费接口面冻结）

**文件**：`docs/architecture/voice/LUNA_VOICE_V2_ASSISTED_CONSUMPTION_INTERFACE_V0.md`  
**性质**：V2 受控消费接口面 v0（冻结口径，收口 stop/cancel 已落地逻辑；不扩能力）  

上位约束（必须服从）：  
- `docs/architecture/voice/LUNA_VOICE_MAINLINE_BASELINE.md`  
- `docs/architecture/voice/LUNA_VOICE_MAINLINE_NEXT_STEP_EXECUTION_PLAN_V0.md`  
- `docs/architecture/voice/LUNA_VOICE_V2_CONTROL_ASSISTED_ROUTING_V0_BASELINE.md`  
- `docs/architecture/voice/LUNA_CONFLICT_GOVERNANCE_CONSTITUTION_V0.md`（主链事实高于辅助信号、No Fabrication 等）  

---

## A. 文档定位

- 这是 **V2 受控消费接口面**的冻结文档。  
- 当前目标是：把已落地的 `control.stop` / `control.cancel` 的 assist candidate / assist consumption 逻辑，从“平行复制的镜像实现”收口成**正式、最小、可冻结的接口口径**。  
- 这不是扩新 intent。  
- 这不是实现更强裁决。  
- 这不是让语义层夺权。  

---

## B. 当前接口面范围（写死）

当前只批准两个意图进入受控消费接口面：
- `control.stop`
- `control.cancel`

当前明确未批准（写死禁止）：
- `control.resume`
- `control.repeat`
- `control.end_conversation`
- `confirm.*`
- `ask.*`
- `unknown`

---

## C. 当前统一消费层级（四层结构，stop/cancel 均已具备）

1) **semantic recognition**  
- 来源：`RuleBasedSemanticConverterV2`  
- 承载：`VoiceInputEvent.metadata["luna_voice_semantic_v2"]`

2) **semantic shadow consume**（影子消费，只读对照）  
- 承载：`VoiceFinalTextDispatchResult.metadata["semantic_v2_shadow"]`  
- 作用：记录语义与当前主链分流关系，不改任何行为

3) **assist candidate**（辅助候选，受控准入）  
- stop：`metadata["semantic_v2_assist_v0"]`  
- cancel：`metadata["semantic_v2_assist_v0_cancel"]`

4) **assist consumption**（辅助消费：只在主链已成立事实之上“确认式消费”）  
- stop：`metadata["semantic_v2_assist_consumption_v0"]`  
- cancel：`metadata["semantic_v2_assist_consumption_v0_cancel"]`

写死说明：  
- 本接口面 v0 只冻结 **第 3、4 层**（candidate/consumption）的统一结构与准入口径。  
- 第 1、2 层仍服从既有 V2 baseline（不在本文件扩大范围）。  

---

## D. 当前最小统一结构（接口面统一结构，不要求立刻大重构）

> 目标：先冻结 stop/cancel 的共同结构面，让后续新增/维护不靠复制粘贴“漂移”。

### D1. assist candidate（共同最小结构）

stop/cancel 的候选结构共同关注以下字段：
- `assist_candidate`（bool）
- `semantic_intent`（string；`control.stop` 或 `control.cancel`）
- `assist_reason`（string；简短可枚举）
- `confidence`（float；来自语义包）

现有落点（代码事实）：  
- stop：`semantic_v2_assist_v0`  
- cancel：`semantic_v2_assist_v0_cancel`

### D2. assist consumption（共同最小结构）

stop/cancel 的消费结构共同关注以下字段：
- `assist_consumed`（bool）
- `semantic_intent`（string；`control.stop` 或 `control.cancel`）
- `consumption_scope`（string；confirmation-only 的作用域标签）
- `consumption_reason`（string；简短可枚举）

现有落点（代码事实）：  
- stop：`semantic_v2_assist_consumption_v0`  
- cancel：`semantic_v2_assist_consumption_v0_cancel`

---

## E. 当前统一准入条件（写成统一口径）

### E1. assist candidate 的共同条件（stop/cancel 同构）

candidate 必须同时满足：
- `semantic_intent` 命中允许集（仅 `control.stop` / `control.cancel`）  
- `semantic_v2_shadow.shadow_status == "matches_current_flow"`  
- `dispatch_type == "short_controlled_input"`  
- `bridge_decision.route == BridgeRouteType.DEVICE_CONTROL`  
- 语义包 `confidence >= 0.8`

否则：`assist_candidate=false`（或不写；当前实现为写入 false/no-signal 结构）。  

### E2. assist consumption 的共同条件（比 candidate 更严格）

consumption 必须同时满足：
- 对应 `assist_candidate == true`  
- `dispatch_type == "short_controlled_input"`  
- `bridge_decision.route == BridgeRouteType.DEVICE_CONTROL`  
- **主链 proposal 事实已明确对应 device_action**：  
  - stop：`DeviceActionProposal.device_action == "stop"`  
  - cancel：`DeviceActionProposal.device_action == "cancel"`  

写死解释：  
- 这不是“semantic says X therefore do X”，而是“main flow already is X + assist present，因此记录 consumed”。  

---

## F. 当前工程边界（写死）

- 受控消费不是主链裁决。  
- 受控消费不是执行放行。  
- 受控消费只是在“主链已成立事实”上做**确认信号消费**。  
- 不允许辅助层独立产生 stop/cancel 行为。  
- 不允许由此推导出 `resume` 可直接复制（见 §G）。  

---

## G. 为什么现在不扩 `resume`（必须写死）

- “继续/恢复”与以下语义存在天然歧义：继续任务 / 继续播报 / 继续对话 / 覆盖 gate。  
- 当前缺少稳定的 task context / lifecycle / reference binding 主链事实结构。  
- 因此不能把 stop/cancel 模板直接复制到 `control.resume`；必须先做专项冲突治理与主链事实约束设计。  

---

## H. 当前验证入口（最小回归入口，写死）

改到 assisted candidate / consumption 的字段、条件、落点时必须重跑：  
- `tools/verify_semantic_converter_v2_assist_stop_candidate.py`  
- `tools/verify_semantic_converter_v2_assist_stop_consumption.py`  
- `tools/verify_semantic_converter_v2_assist_cancel_consumption.py`  
- `tools/verify_voice_v1_minimal_flow.py`

---

## I. 后续接入纪律（写死）

任何新 intent 纳入受控消费接口面，必须先：  
1) 有专题/冲突分析（含歧义与主链事实来源）  
2) 有最小实现（不夺权）  
3) 有 baseline/freeze  
4) 最后才可纳入本接口面（更新允许集与验证入口）  

禁止：先复制 stop/cancel 模板再补文档。  

