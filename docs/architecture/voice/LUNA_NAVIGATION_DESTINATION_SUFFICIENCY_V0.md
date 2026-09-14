# Navigation Destination Sufficiency v0（导航目的地参数充足性专题）

**文件**：`docs/architecture/voice/LUNA_NAVIGATION_DESTINATION_SUFFICIENCY_V0.md`  
**性质**：导航主流程下的参数充足性专题（只做设计与口径冻结，不做实现）  

上位约束（必须服从）：  
- `docs/architecture/LUNA_WORLD_ENTRY_PRINCIPLE_V0.md`  
- `docs/architecture/voice/LUNA_VOICE_MAINLINE_BASELINE.md`  
- `docs/architecture/voice/LUNA_CONFLICT_GOVERNANCE_CONSTITUTION_V0.md`  

并写死：No Fabrication Rule 继续成立；主链事实高于辅助信号；记忆/语义/视觉不能直接替代 destination 确认；统一时空锚点原则继续成立。

---

## A. 专题定位

- 这是导航主流程下的**参数充足性专题**。  
- 当前只讨论：`start_navigation` 的 **destination 是否足够**。  
- 当前不实现：地图接入、复杂地点解析、记忆补地点、视觉补地点、完整多轮导航对话管理。  

---

## B. 当前问题定义（写死）

- 当前语音主线已经能产出：`TaskActionProposal(task_action="start_navigation")`，并到达 `navigation_handoff_v0`。  
- 当前 handoff 的结果为：`handoff_status="not_ready"` 且 `reason="missing_destination"`。  
- 因此断点已从“线程/边界接线”收缩为“**目的地参数不足**”。  

---

## C. destination 的最小定义（极保守）

什么才算“足够启动导航”的 destination（v0 极保守，写死）：

- destination 必须是**可唯一指向**的导航目标。至少应具备以下之一：  
  1) **明确地点名称**，且主链已有**唯一绑定事实**（不是模糊口头指代）  
  2) **明确 `place_id / destination_id / target_id`** 等可唯一标识  
  3) **明确且已确认**的导航目标引用（可追踪的 reference_id/绑定 id）

明确不算足够（写死示例）：  
- “去那里 / 去那个地方 / 帮我导航过去 / 就去刚才那个”  
- 仅有视觉摘要提示“像某个地点”  
- 仅有历史记忆“可能常去某地”  

---

## D. 主链事实 vs 辅助信号（分层）

### D1. 主链事实候选（当前可作为 destination 候选的主链事实）

> 目标：列出“可以被当作候选”的事实源，但不等于可直接启动。

- **当前句用户输入文本**：`VoiceInputEvent.wake_word_stripped | normalized_text | raw_text`（仅文本事实）  
- **BridgeDecision 与 proposal**：`bridge_decision.route == TASK_LIFECYCLE`、`proposal.task_action == "start_navigation"`  
- **proposal 的显式目标字段**（若未来出现）：`place_id / destination_id / target_id / reference_id`（当前 Stage-1 多数为缺失）  
- **navigation_handoff_v0.reason**：例如 `missing_destination`（这是“缺口事实”，不是目标事实）

### D2. 辅助信号（只能辅助形成“候选”，不能直接变成已确认 destination）

- **semantic_v2 payload**：当前结构包含 `entities/references/ambiguities/requires_followup` 等容器，但规则版 v0 不产出地点绑定（且不得脑补）  
- **VoiceV1SessionStateAnchor.last_user_text/last_system_text**：可作为回看线索，但 v0 不允许用它“自动补地点”  
- **视觉摘要/V3 输入包**：可作为背景，但不允许替代 destination  

写死原则：辅助信号不能单独把 destination 变成“已确认且唯一”的启动条件。

---

## E. 最小处理口径（工程化规则）

1) **destination 明确且唯一**  
- 才有资格进入未来“真正导航启动”（handoff_status 可为 started）。  

2) **destination 缺失**  
- 不得启动导航。  
- 应要求用户补充 destination（至少落到“要求确认/追问”）。  

3) **destination 有候选但不唯一**  
- 不得启动导航。  
- 必须进入确认路径；不允许强判。  

4) **destination 仅来自语义推断 / 历史记忆 / 视觉线索**  
- 当前阶段只可作为候选提示。  
- 不得直接启动导航。  

---

## F. 最小响应等级映射（5 档）

- **直接执行**：destination 明确且唯一（且不触发资源/信息 gate）  
- **提示后执行**：v0 不主动使用（除非 destination 已唯一且只是提示成本/提醒）  
- **要求确认**：缺 destination / destination 不唯一（默认）  
- **保守降级**：用户拒绝补充但仍可给出“如何提供目的地”的提示，不启动  
- **明确拒绝**：用户持续拒绝提供必要信息且无法安全启动（或触碰底线约束）

---

## G. 当前明确禁止项（写死）

- 不允许因为语义层“像是识别到地点”就直接构造 destination  
- 不允许因为历史记忆里“可能常用地点”就直接启动导航  
- 不允许视觉摘要替代 destination  
- 不允许把本专题做成地图解析系统  
- 不允许在本专题里顺手实现 `resume/repeat`  

---

## H. 推荐的最小未来落点（只选一个，不实现）

**唯一推荐未来落点**：在 `attempt_navigation_start_handoff_v0(...)` 之前（或其中），增加一个 `destination_sufficiency_check_v0`（只做“是否足够/是否需要确认”的判定），并把结果写入 metadata 供响应型模板消费。  

为什么选这里：  
- 最连续：紧贴 handoff，离真实启动最近，不影响主链分流与 gate。  
- 最不易失控：只决定“是否具备启动条件/是否需确认”，不做地点解析、不接地图。  

---

## I. 下一步最小实现建议（只给 1 个方向）

**建议最先落地**：先做 “destination sufficiency check 的只读评估器 v0”（只写 metadata，不启动导航、不改主链裁决），为后续固定追问模板提供稳定触发依据。  

