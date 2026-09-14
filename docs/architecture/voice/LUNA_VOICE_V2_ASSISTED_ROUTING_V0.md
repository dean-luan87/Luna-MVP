# Luna Voice V2 — Semantic V2 Assisted Routing v0（仅控制类）设计与最小接入准备

**目标**：基于现有 `RuleBasedSemanticConverterV2` 与 `semantic_v2_shadow`（影子消费），为“控制类 intent”定义**受控消费准入规则**与**唯一最小落点**，让 V2 语义仅作为**辅助信号**被记录/观察与未来可控接入准备。本轮**不改变**任何 dispatch/submit/reply 行为。

**前置已存在**：
- `RuleBasedSemanticConverterV2` 产出：`ev.metadata["luna_voice_semantic_v2"]`
- shadow consume 产出：`result.metadata["semantic_v2_shadow"]`
- V1 最小闭环与硬约束：`guard_v1_speakable_text`、`VoiceV1SessionStateAnchor`
- 主分流：`dispatch_voice_final_text(...)`

---

## A. 定位

- **Assisted Routing v0 只覆盖控制类 intent**（见 §B），并且只作为**辅助信号**参与“候选标记/观测对照”。  
- **语义层不是最终裁决器**：不允许让 V2 直接接管 `dispatch_voice_final_text` 的分流决策。  
- **不是**全面语义驱动主链；不是问答/任务/视觉接入方案；不引入模型。  
- **不改变主链行为**：本轮只做设计与最小接入准备（metadata/TODO 级别），不改变 route、execution_class、submit、guard。

---

## B. 当前仅允许覆盖的 intent

**只允许**（控制类 v0 范围）：
- `control.stop`
- `control.resume`
- `control.repeat`
- `control.cancel`

**暂不允许**（必须显式禁止）：
- `control.end_conversation`
- `confirm.*`
- `ask.*`
- `unknown`

---

## C. 受控消费原则（写死）

- **已有主链明确控制路径时**：语义层最多提供**佐证/观测**，不得夺权。  
  - 例：当前已存在白名单 shortcut → `BridgeDecision.route=DEVICE_CONTROL/TASK_LIFECYCLE` 的路径时，V2 不得改变其 route 或执行权限建议。
- **主链不明确时**：语义层也不能直接夺权，只能进入“候选辅助”（metadata 标记），不触发执行、不改分流。  
- **不得绕过 No Fabrication Rule**：语义辅助不能把“像 stop”当成 stop；不确定宁可不用。  
- **不得绕过 guard / submit / 主链安全边界**：语义辅助永远不直接触发 submit，不修改输出候选。  
- **不得自造系统级时空锚点**：不得生成 timestamp/location/coordinate 等系统事实字段；只能消费上游/中台注入（若未来存在）。

---

## D. 准入条件（必须具体，v0 最小规则）

定义 v0 的“可被标记为语义辅助候选（semantic_assist_candidate=true）”的准入条件。**注意：本轮仅设计，不实际改路由。**

### D1. 语义侧前置条件
- `semantic_intent` ∈ {`control.stop`, `control.resume`, `control.repeat`, `control.cancel`}
- `confidence` ≥ **0.8**（规则强命中）

### D2. 与当前主链结果的保守一致性条件
必须满足以下 **全部**（保守收窄）：
- `result.dispatch_type == "short_controlled_input"`  
- `result.bridge_decision.route == BridgeRouteType.DEVICE_CONTROL`  
- `result.metadata["semantic_v2_shadow"].shadow_status == "matches_current_flow"`  

> 解释：v0 只允许在“主链已走受控短链且明确是 device_control”时，语义作为佐证被标记为候选。  
> 这避免了语义把“任务态继续（task_resume）”误当作“继续播报（device resume）”而夺权。

### D3. 会话/模式保守约束（不依赖脑补）
为避免语义越权，在 v0 中额外约束（只读事实）：
- `event.router_decision != "reject"`（已是短链路径的事实前提）
- 不基于 `VoiceV1SessionStateAnchor` 做“补全推断”。锚点仅可用于未来观测（例如用户是否在 waiting_user），**不能**作为准入放宽理由。

### D4. 输出形式（本轮仅作为 metadata 标记）
当满足准入条件时，仅写入 **metadata 标记**（下一轮落地；本轮不做行为接管）：

```json
{
  "semantic_v2_assist_v0": {
    "enabled": true,
    "candidate": true,
    "semantic_intent": "control.stop",
    "confidence": 0.8,
    "gates_passed": [
      "intent_allowed",
      "confidence>=0.8",
      "shadow_matches_current_flow",
      "dispatch_short_controlled_input",
      "bridge_route_device_control"
    ],
    "note": "v0_assist_candidate_only_no_behavior_change"
  }
}
```

未满足时可记录 `candidate=false` + 简短 `note`，用于统计与对照，但仍不改行为。

---

## E. 明确禁止的场景（单列）

- **不允许**因语义层单独命中就直接执行 stop/cancel/resume/repeat。  
- **不允许**用语义层改写用户未明确表达的控制意图（例如把“别这样”当 stop）。  
- **不允许**在多义输入上强判控制类（例如“继续”在任务态更可能是 task_resume；v0 不允许语义夺权）。  
- **不允许**在时空锚点缺失时自行补上下文事实（例如推断用户位置/时间）。  
- **不允许**绕过 guard/submit 的任何硬边界。

---

## F. 推荐最小落点（只选一个）

**唯一推荐落点**：`capabilities/voice/runtime/voice_final_text_dispatcher.py` 内，在 `_maybe_attach_semantic_shadow_v2(...)` 之后紧邻处，增加 **仅 metadata 级别**的辅助候选标记（下一轮实现，本轮只留 TODO/占位）。

理由（代码事实）：
- 此时已同时拥有：`event`、`result.dispatch_type`、`bridge_decision.route`、`semantic_v2_shadow` 结论；
- 可以把准入判断的结果写入 `VoiceFinalTextDispatchResult.metadata`，**不改变返回对象其它语义**；
- 不需要动 `voice_input_router` / `voice_input_to_bridge_decision` / 长链编排。

**本轮要求**：先只做文档 + TODO，不直接改 route，不执行 assisted control。

---

## G. 下一轮若做最小行为接入，应怎么做（只给 1 个方向）

从 **`control.stop`** 开始（最小、最安全）：
- 仅在主链已判定 `DEVICE_CONTROL` 且 `shadow_status=="matches_current_flow"` 的场景里，将 `semantic_v2_assist_v0.candidate=true` 作为**白盒观测 + 统计分桶**信号；  
- 仍由现有白名单 shortcut / BridgeDecision 路径执行，不允许 semantic 直接触发执行；  
- 逐步验证：是否能降低“短语变体导致的未命中”概率（例如未来把“停一下”等变体纳入白名单或由语义辅助提示白名单扩充），但不让语义直接改路由。

---

## 硬约束（必须继续成立）

### 约束 1：No Fabrication Rule
- 语义辅助不能因为“像 stop”就当 stop；不确定宁可不用，不准强用。

### 约束 2：统一时空锚点原则
- 语义辅助层不得自造时间/空间锚点；若将来需要上下文，只能消费中台注入基准。

