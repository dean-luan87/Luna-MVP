# Navigation Destination Bound Fact v0（导航目的地绑定事实专题）

**文件**：`docs/architecture/voice/LUNA_NAVIGATION_DESTINATION_BOUND_FACT_V0.md`  
**性质**：导航主流程下的“destination bound fact”专题（只做设计与口径冻结，不做实现）  

上位约束（必须服从）：
- `docs/architecture/LUNA_WORLD_ENTRY_PRINCIPLE_V0.md`
- `docs/architecture/voice/LUNA_VOICE_MAINLINE_BASELINE.md`
- `docs/architecture/voice/LUNA_CONFLICT_GOVERNANCE_CONSTITUTION_V0.md`
- `docs/architecture/voice/LUNA_NAVIGATION_DESTINATION_SUFFICIENCY_V0.md`
- `docs/architecture/voice/LUNA_NAVIGATION_DESTINATION_BINDING_V0.md`

并写死（继续成立）：
- **No Fabrication Rule**：不得把“像地点的文本 / 语义高置信猜测”升格为 destination 已绑定事实。
- **主链事实高于辅助信号**：语义/记忆/视觉只能辅助，不得替代 bound fact。
- **统一时空锚点原则**：本专题不引入任何模块自造的时间/空间字段（timestamp/坐标/定位）。

---

## A. 专题定位

- 这是导航主流程下的 **destination bound fact** 专题。
- 当前只讨论：`destination_candidate_v0` 在什么条件下才允许升级为 `destination_bound`。
- 当前不实现：
  - 地点解析 / 地点检索 / 地图接入
  - 历史记忆补地点
  - 视觉补地点
  - 真实导航启动

---

## B. 当前问题定义

当前工程事实（已落地）：
- 主链能形成 `TaskActionProposal(task_action="start_navigation")` 并进入 `navigation_handoff_v0`。
- 缺 destination 时：
  - `destination_sufficiency_eval_v0` 以“只看显式绑定字段”的口径判定 `missing_destination`
  - 系统能触发固定模板 `navigation_missing_destination_confirm_v0` 要求用户补充目的地
- 主链已能在严格语境下承载 `destination_candidate_v0`（只读、可观察、不可直接启动）

当前断点（写死）：
- handoff 仍不能消费 candidate（也不应消费）。
- 当前缺的是一套被冻结的“**candidate → bound**”升级规则：什么叫唯一、什么叫已确认、什么情况下必须停留在 candidate。

---

## C. destination_bound 的最小定义（极保守）

`destination_bound`（绑定事实）必须满足：
1) **存在明确的 candidate**（例如 `destination_candidate_v0.candidate_present == true` 且 `candidate_text` 非空）。  
2) **candidate 未被系统判定为明显歧义**（本 v0 冻结口径，不实现歧义算法；但写死“有歧义则不可升级”）。  
3) **存在明确的确认依据或显式绑定依据**（二选一，但必须是主链可复核的事实）：  
   - **显式绑定依据**：出现 `place_id / destination_id / target_id / reference_id` 这类可被 handoff 消费的稳定字段（来源不在本专题规定）。  
   - **确认依据**：用户在后续轮次提供了可被主链识别的“确认完成”事实（本 v0 只定义原则，不实现识别器）。  
4) 绑定后可形成 **handoff 可消费** 的稳定字段结构（见 §F），并可被观察与复盘。

明确不等价（写死）：
- `destination_bound` **不等于** “文本里像地点”。  
- `destination_bound` **不等于** “candidate 已存在”。  
- `destination_bound` **不等于** “语义层高置信”。  

---

## D. candidate vs bound 的升级条件（冻结口径，仅规则不实现）

### D1. 不能升级（必须停留在 candidate）

以下任一成立，必须停留在 candidate：
- 只有一句“像地点”的文本（只有 `candidate_text`，无显式绑定字段、无确认完成事实）。
- candidate 明显歧义（例如多个目标、指代不明、需要限定但缺失）。
- 只有语义高置信/辅助信号（semantic/anchor/vision/memory），但没有主链绑定依据。
- 需要确认但确认尚未完成（本 v0 默认 `requires_confirmation=true`）。

### D2. 可进入确认候选（仍不能升级）

满足：
- `destination_candidate_v0` 已承载（candidate present）
- 但尚缺确认完成事实或显式绑定字段  

则：
- 允许进入“确认路径”（例如固定追问/确认模板；不在本专题实现）
- **仍不得升级为 bound**

### D3. 可升级为 bound（未来条件）

当且仅当同时满足：
- candidate 已存在且稳定（承载位存在）
- 不存在明显歧义
- 且满足“显式绑定依据”或“确认依据”之一（见 §C）

才允许升级为 bound（本轮只定义，不实现）。

---

## E. 主链事实 vs 辅助信号（分层）

### E1. 主链事实候选（允许参与 bound 升级的事实源）

- `destination_candidate_v0`（当前已落地，主链可观察）
- `destination_sufficiency_eval_v0`（显式绑定字段是否出现的只读评估）
- `proposal.task_action == "start_navigation"`（语境事实）
- **未来可能出现的显式绑定字段**：`place_id / destination_id / target_id / reference_id`
- **未来可能出现的“确认完成事实”**：用户确认型输入被主链识别并沉淀为结构化字段（本 v0 不实现）

### E2. 辅助信号（不能直接替代 bound）

- `semantic_v2 payload`：可提示歧义/需要 followup，但不能单独作为 bound 升级依据
- `VoiceV1SessionStateAnchor`：可提供上下文线索，但不能自动补地点或自动升级
- 视觉/记忆：只能背景提示，不能直接替代 bound

---

## F. 最小 bound 结构建议（future handoff 可消费层；仅设计不实现）

建议使用极小结构（克制，不做大 schema）：

```json
{
  "destination_bound": true,
  "binding_key": "destination_id",
  "binding_value": "dest_123",
  "binding_reason": "explicit_binding_field_present_and_nonempty",
  "requires_confirmation": false,
  "bound_scope": "navigation_destination_bound_fact_v0"
}
```

约束（写死）：
- `binding_key/binding_value` 必须可复核、可被后续模块消费（例如 id 型字段）。
- 不引入坐标/定位/时间戳等时空字段。
- 未满足升级条件时不得写入（只能停留在 candidate）。

---

## G. handoff 消费边界（必须写死）

未来 `navigation_handoff_v0` 的消费纪律（写死）：
- **只能消费 `destination_bound` 层**（bound fact）。
- **不得消费裸 `destination_candidate_v0`**。
- **不得消费语义高置信候选**（semantic_v2 intent/entities 等）。
- **不得消费视觉/记忆线索本身**。

当前工程对齐提示（事实）：
- 当前 `navigation_handoff_v0` 仅检查 `proposal.metadata["destination"/"end"/"target"]` 是否存在；这不是 bound fact（只是松散文本），因此在本专题口径下仍不应视为“可启动绑定事实”。

---

## H. 当前明确禁止项（写死）

- 不允许因为 candidate 看起来合理就直接升级为 bound
- 不允许因为语义高置信就升级为 bound
- 不允许历史记忆直接替代绑定
- 不允许视觉摘要直接替代绑定
- 不允许把本专题做成地点解析系统
- 不允许在本专题里顺手实现真实导航启动

---

## I. 推荐的最小未来落点（只选一个；本轮只设计不实现）

**唯一推荐落点**：在 `destination_candidate_v0` 已存在之后，新增一个只读的 `destination_bound_check_v0`（评估器）：
- 输入：`destination_candidate_v0` +（若出现）显式绑定字段 + 最小确认完成事实（未来）
- 输出：只写一个 `destination_bound_eval_v0`（或同等最小结果）到 metadata，**不改变任何主链行为**

为什么选这里：
- 最连续：紧贴 candidate 承载之后，目标单一（只评估是否具备升级条件）。
- 最不易失控：先评估，再决定是否引入确认模板或升级写入；避免直接启动。

---

## J. 为什么现在还不能直接启动真实导航（写死）

- 现在只有 `destination_candidate_v0`，没有 `destination_bound`。
- 没有稳定的“确认完成事实”沉淀结构与升级路径。
- handoff 尚未实现“只消费 bound”的契约（目前仅松散看 `proposal.metadata`）。
- 因此不能从 candidate 直接跳到真实导航启动。

---

## K. 下一步最小实现建议（只给 1 个方向）

**建议最先落地**：先做 `destination_bound_check_v0` 的只读评估器：
- 只输出“是否具备升级条件/缺口原因”（例如缺显式绑定字段、缺确认完成事实、歧义未消除）
- 不写 bound，不改 handoff，不启动导航

