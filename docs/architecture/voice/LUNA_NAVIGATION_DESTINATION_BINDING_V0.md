# Navigation Destination Binding v0（导航目的地绑定专题）

**文件**：`docs/architecture/voice/LUNA_NAVIGATION_DESTINATION_BINDING_V0.md`  
**性质**：导航主流程下的“destination 绑定”专题（只做设计与口径冻结，不做实现）  

上位约束（必须服从）：
- `docs/architecture/LUNA_WORLD_ENTRY_PRINCIPLE_V0.md`
- `docs/architecture/voice/LUNA_VOICE_MAINLINE_BASELINE.md`
- `docs/architecture/voice/LUNA_CONFLICT_GOVERNANCE_CONSTITUTION_V0.md`
- `docs/architecture/voice/LUNA_NAVIGATION_DESTINATION_SUFFICIENCY_V0.md`

并写死（继续成立）：
- **No Fabrication Rule**：不得因为“文本看起来像地点 / 语义高置信”就把地点当作已绑定事实。
- **主链事实高于辅助信号**：语义/记忆/视觉只能作为辅助信号，不能替代“已绑定 destination”的主链事实。
- **统一时空锚点原则**：本专题不引入任何模块自造的时间/空间字段（timestamp/坐标/定位）。

---

## A. 专题定位

- 这是导航主流程下的**destination 绑定**专题。
- 当前只讨论：**用户补充一句目的地之后，主链如何形成“可被 handoff 接受的 destination 候选/绑定事实”**。
- 当前不实现：
  - 地图解析 / 地点检索 / POI 搜索
  - 历史记忆补地点
  - 视觉补地点
  - 复杂多轮导航对话管理（状态机、候选列表、消歧轮询等）

---

## B. 当前问题定义

已完成事实链（当前工程事实）：
- `TaskActionProposal(task_action="start_navigation")` 已能形成并进入 `navigation_handoff_v0`。
- 当 `destination_sufficiency_eval_v0` 判定缺目的地（`reason="missing_destination"`）时，系统能触发固定模板 `navigation_missing_destination_confirm_v0` 提示用户补充目的地。

当前断点（写死）：
- 主链仍缺一个“**把用户补充的目的地接住**”的绑定层：用户即使补了一句地点，主链仍没有稳定的**结构化承载位**来把“候选/绑定事实”沉淀下来并供后续 handoff 消费。
- 因此断点已从“是否追问”进入“**如何形成 destination 绑定事实**”。

---

## C. destination binding 的最小定义（极保守）

本专题定义两层对象，必须严格区分：

1) **destination candidate（目的地候选）**：  
- 仅表示“用户可能表达了一个目的地/目标”。  
- 允许以**文本形态**出现（例如用户补充一句“去星巴克”），但必须进入一个结构化承载位才算“候选已被主链接住”。  
- candidate 不等于可启动导航。

2) **destination bound fact（目的地已绑定事实）**：  
- 表示“主链已接受该目的地作为当前导航目标（可供后续 handoff 消费）”。  
- **已绑定不等于文本像地点**；必须满足至少：
  - 有一个明确的候选内容（candidate）。
  - 候选进入了结构化承载位（可被观察、可被后续流程引用）。
  - 候选未被系统判定为明显歧义/不确定（本 v0 只冻结口径，不实现算法）。
  - 若歧义未消除：只能停留在 candidate，**不得**升级为 bound fact。

---

## D. 候选 vs 已绑定（分界线，写死）

### D1. destination candidate（候选）

- 允许来源：
  - 当前句用户补充的目的地文本表达（仅文本事实）。
  -（未来）通过非常保守的规则把文本“像目的地”识别出来，但这仍然只生成 candidate，不生成 bound。
- 最小能力：
  - 可暂存（有承载位）
  - 可标记是否需要确认（requires_confirmation）
- 禁止：
  - candidate 直接触发真实导航启动
  - candidate 直接等价为 place_id / destination_id 等唯一绑定

### D2. destination bound fact（已绑定事实）

- 仅当满足更严格条件时才允许从 candidate 升级。
- handoff（未来）**只能消费 bound fact**，不得消费裸 candidate。
- bound fact 的价值是“可被后续模块可靠引用”，因此必须保守、可复核、可观察。

---

## E. 主链事实 vs 辅助信号（分层）

### E1. 主链事实候选（当前已有/未来建议的主链层）

当前已有（工程事实）：
- **当前句文本事实**：`VoiceInputEvent.raw_text / normalized_text / wake_word_stripped`
- **主链意图事实**：`proposal.task_action == "start_navigation"`
- **目的地充足性评估事实**：`result.metadata["destination_sufficiency_eval_v0"]`
- **handoff 断点事实**：`result.metadata["navigation_handoff_v0"]`（例如 `reason="missing_destination"`）

未来建议新增（本轮只设计，不实现）：
- **destination_candidate 承载位**（见 §G）：把“用户补充的一句目的地”以保守结构写入主链可观察处。
- **destination_binding 承载位**（见 §G）：仅在满足升级条件时写入 bound fact。

### E2. 辅助信号（只能辅助，不能替代绑定事实）

当前已有但受限：
- `semantic_v2 payload`：目前 `semantic_converter_v2.py` 的规则版只覆盖控制/确认/问询；`entities/references/ambiguities/requires_followup` 结构存在，但**当前实现不产出地点实体**，且按 No Fabrication 不允许用语义“猜”地点就升级绑定。
- `VoiceV1SessionStateAnchor`：`last_user_text / last_system_text / conversation_status` 可提供上下文线索，但 v0 禁止用它“自动补地点/自动绑定”。
- `vision_semantic`（V3 输入包）与任何视觉摘要：v0 禁止把视觉线索升格为绑定事实。

写死结论：
- 辅助信号最多用于“提示可能需要确认/是否继续追问/候选是否不可靠”，不能替代“已绑定 destination”主链事实。

---

## F. 最小处理口径（工程化规则，v0 冻结口径）

1) **用户补充内容明显不足以构成目的地**（如“那里”“随便”“就去那个”）  
- 不得绑定（不得产生 bound fact）。  
- 允许：继续保持 missing/不充分，并继续要求补充（响应模板不在本专题扩展）。

2) **用户补充了一个看起来像目的地的表达**（如“去星巴克”）  
- 允许：形成 `destination_candidate`（文本候选 + 克制字段）。  
- 禁止：自动等价为 `destination_bound`（仍需唯一性/歧义消除的冻结规则支撑）。

3) **候选明显唯一且无歧义（未来条件）**  
- 才有资格从 candidate 升级为 bound fact。  
- v0 仅冻结“需要这一步”，不实现判定算法与证据来源。

4) **候选存在歧义**（多个地点/指代不明/缺少必要限定）  
- 不得升级为 bound fact。  
- 应进入确认路径（本专题不实现确认管理，只冻结“不升级”）。

5) **历史记忆 / 视觉 / 语义高置信**  
- 当前阶段只能辅助提示。  
- 不得直接升级绑定（不得生成 bound fact）。

---

## G. 最小绑定结构建议（克制结构，不做大 schema）

建议在主链可观察处引入一个极小承载结构（示例命名，可调整，但必须克制）：

### G1. destination_candidate_v0（候选承载）

```json
{
  "destination_candidate_text": "去星巴克",
  "requires_confirmation": true,
  "binding_reason": "user_provided_candidate_text_unverified",
  "candidate_scope": "navigation_destination_binding_v0"
}
```

约束：
- 只允许承载**文本候选**，不引入地图 id、不引入坐标、不引入系统定位。
- `requires_confirmation` 默认为 true（保守），除非未来冻结“唯一且无歧义”的条件。

### G2. destination_binding_v0（已绑定事实承载）

```json
{
  "destination_bound": true,
  "binding_key": "destination_id",
  "binding_value": "dest_123",
  "requires_confirmation": false,
  "binding_reason": "explicit_binding_field_present_and_nonempty",
  "binding_scope": "navigation_destination_binding_v0"
}
```

约束：
- 仅当出现明确、可复核的绑定字段（如 `destination_id/place_id/target_id/reference_id`）且满足升级条件时才允许写入。
- v0 不规定这些 id 的来源（地图/手工/外部系统），只规定“**一旦出现，也必须走结构化承载与升级口径**”。

---

## H. 推荐的最小未来落点（只选一个；本轮只设计，不实现）

**唯一推荐落点**：在 `dispatch_voice_final_text(...)` 的 `short_controlled_input` 分支中，紧贴 `TaskActionProposal(start_navigation)` 已形成之后，引入一个 **`destination_binding_check_v0`**（或同等最小承载写入点）：
- 输入：当前句文本事实 + 当前 `bridge_decision.proposal` + 现有 `destination_sufficiency_eval_v0` 结果
- 输出：只写 metadata 承载位（`destination_candidate_v0` / `destination_binding_v0`），不改 route/proposal/handoff/submit 行为

为什么选这里（写死理由）：
- 最连续：离 `proposal.task_action` 最近，语境最明确（当前就是 start_navigation）。
- 最不易失控：只写入结构化承载与评估，不会牵引地图/记忆/视觉。
- 最易观测：与 `destination_sufficiency_eval_v0`、`navigation_handoff_v0` 并列放在同一主链结果元数据下，便于复盘“候选→绑定→handoff”的前置链路。

---

## I. 为什么现在还不能直接做自动启动（写死）

即使用户补了一句地点，也不能直接启动真实导航，因为当前缺少：
- 稳定的 **destination binding 事实结构**（candidate/bound 的承载位尚未冻结并落地）。
- “唯一性/歧义消除”的冻结规则与证据来源。
- 确认后的升级路径（candidate → bound）与相应的确认纪律。
- handoff 的消费契约（handoff 只能消费 bound fact）尚未以代码约束写死。

因此：当前阶段只能先把“候选/绑定事实如何形成、如何升级、何时不升级”钉死，再考虑自动启动。

---

## J. 下一步最小实现建议（只给 1 个方向）

**建议最先落地**：先实现一个“destination_candidate 承载与只读评估器 v0”：
- 仅在 `start_navigation` 上下文（且刚经历 missing_destination 追问）时，把用户补充的一句文本以 `destination_candidate_v0` 写入 metadata（只读、可观察）。
- 同时输出一个极小评估结果（是否明显不足/是否需要确认），但**不升级为 bound**、不触发真实导航、不接地图/记忆/视觉。

