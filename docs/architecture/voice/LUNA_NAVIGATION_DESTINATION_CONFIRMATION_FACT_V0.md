# Navigation Destination Confirmation Fact v0（导航目的地确认完成事实专题）

**文件**：`docs/architecture/voice/LUNA_NAVIGATION_DESTINATION_CONFIRMATION_FACT_V0.md`  
**性质**：导航主流程下的“destination confirmation fact”专题（只做设计与口径冻结，不做实现）  

上位约束（必须服从）：
- `docs/architecture/LUNA_WORLD_ENTRY_PRINCIPLE_V0.md`
- `docs/architecture/voice/LUNA_VOICE_MAINLINE_BASELINE.md`
- `docs/architecture/voice/LUNA_CONFLICT_GOVERNANCE_CONSTITUTION_V0.md`
- `docs/architecture/voice/LUNA_NAVIGATION_DESTINATION_SUFFICIENCY_V0.md`
- `docs/architecture/voice/LUNA_NAVIGATION_DESTINATION_BINDING_V0.md`
- `docs/architecture/voice/LUNA_NAVIGATION_DESTINATION_BOUND_FACT_V0.md`

并写死（继续成立）：
- **No Fabrication Rule**：不得把“像确认的语气词/语义命中 confirm.yes”当作已确认事实。
- **主链事实高于辅助信号**：语义/记忆/视觉只能辅助，不得替代 confirmation fact。
- **统一时空锚点原则**：本专题不引入任何模块自造的时间/空间字段（timestamp/坐标/定位）。

---

## A. 专题定位

- 这是导航主流程下的 **destination confirmation fact** 专题。
- 当前只讨论：**“用户确认已完成”如何形成主链事实**（可承载、可冻结、可被后续 bound 升级消费）。
- 当前不实现：
  - bound 升级
  - 地图解析/地点检索/地图接入
  - 历史记忆补地点
  - 视觉补地点
  - 真实导航启动

---

## B. 当前问题定义

当前主链已能做到（工程事实）：
- 在缺目的地语境下承载 `destination_candidate_v0`（只读候选承载）
- 输出 `destination_bound_check_v0`（只读评估：是否出现显式绑定字段 + 语义歧义观察）

当前缺口（写死）：
- 还缺“**确认完成事实**”这一层：即便用户说“对/没错/就是这个”，主链仍没有一个**结构化事实位**把“确认已完成”沉淀下来。
- 没有 confirmation fact，就无法在后续把 candidate 稳定升级到 future bound：因为缺少“用户确实认可当前 candidate”的主链证据。

---

## C. confirmation fact 的最小定义（极保守）

`destination_confirmation_fact_v0`（确认完成事实）必须满足：
1) 当前存在明确的 `destination_candidate_v0`（candidate_present=true，且 candidate_text 非空）。  
2) 用户当前输入是对**该 candidate**的确认，而不是新的候选、否定/修正或无关话语。  
3) 当前不存在明显歧义/冲突信号（本 v0 冻结口径，不实现算法；但写死“有歧义则不得生成确认完成事实”）。  
4) 确认结果可形成一个**结构化、主链可消费的事实位**（见 §F），并可被后续 bound 升级逻辑引用。

明确不等价（写死）：
- confirmation fact **不等于** 用户说了“对”。  
- confirmation fact **不等于** `confirm.yes` intent 命中。  
- confirmation fact **不等于** candidate 存在。  

---

## D. 哪些输入可以构成 confirmation fact（分类口径，v0 只设计不实现）

### D1. 明确确认型输入（未来可候选）

示例：
- “对”
- “对，就是这个”
- “没错”
- “是的，去那里”

写死约束：
- 这些话本身仍**不自动**构成 confirmation fact。  
- 必须依赖：
  - 已存在 candidate
  - 以及“上下文一致性”可被主链确认（例如没有出现新的目的地文本、没有否定/修正信号、没有明显歧义）。

### D2. 否定/修正型输入（不能形成 confirmation fact）

示例：
- “不是”
- “不对”
- “不是那个”
- “换一个地方”

口径（写死）：
- 这些输入不能生成 confirmation fact；它们意味着当前 candidate 失效或需重新候选/重新确认。

### D3. 新地点补充型输入（更像新的 candidate，不是 confirmation fact）

示例：
- 用户直接说一个新地点（如“人民广场”）或重新报目的地

口径（写死）：
- 这类输入应被当作新的候选文本（candidate），而不是确认完成事实。
- confirmation 的目标必须是“对既有 candidate 的确认”，不是“新候选的提出”。

---

## E. 主链事实 vs 辅助信号（分层）

### E1. 主链事实候选（允许参与形成 confirmation fact 的事实源）

- `destination_candidate_v0`（主链已承载）
- 用户当前句文本事实：`VoiceInputEvent.wake_word_stripped / normalized_text / raw_text`
- `proposal.task_action == "start_navigation"`（语境事实）
- 未来承载位：`destination_confirmation_fact_v0`（本专题定义，不实现）

### E2. 辅助信号（只能辅助判断“像确认/像否定/像歧义”，不能替代 confirmation fact）

- `semantic_v2.intent == "confirm.yes" / "confirm.no"`（规则版已覆盖“对/是/好/不是/不要”等）
- `semantic_v2.ambiguities / requires_followup`
- `VoiceV1SessionStateAnchor.*`（上下文线索）
- 视觉/记忆背景

写死结论：
- `confirm.yes` 只能作为“可能在确认”的辅助信号，**不能脱离 candidate**直接生成 confirmation fact。

---

## F. 最小 confirmation 结构建议（future 主链可消费层；仅设计不实现）

建议极小结构（克制，不做大 schema）：

```json
{
  "confirmation_present": true,
  "confirmation_target": "destination_candidate_v0",
  "confirmation_reason": "user_confirmed_existing_candidate_without_new_candidate_text",
  "confirmation_scope": "navigation_destination_confirmation_fact_v0"
}
```

约束（写死）：
- 不引入时空字段。
- `confirmation_target` 只能指向“已存在的 candidate 承载位”，不得指向语义猜测或视觉线索。
- 未满足 §C 的最小定义时不得写入（只能停留在 candidate/辅助信号层）。

---

## G. 与 bound 的关系（必须写死）

- confirmation fact **不是** bound。  
- confirmation fact 是 candidate → bound 升级所需的一个前置事实层。  
- future bound 升级必须同时参考：
  - candidate（候选内容）
  - confirmation fact（确认完成）
  - 显式绑定依据/唯一性规则（见 bound fact 专题）
- future handoff 仍然只消费 bound，不消费 confirmation fact 本身。

---

## H. 当前明确禁止项（写死）

- 不允许因为 `semantic_v2` 命中 `confirm.yes` 就自动确认 destination
- 不允许没有 candidate 就生成 confirmation fact
- 不允许历史记忆直接替代确认
- 不允许视觉摘要直接替代确认
- 不允许把本专题做成多轮对话管理系统
- 不允许在本专题里顺手实现真实导航启动

---

## I. 推荐的最小未来落点（只选一个；本轮只设计不实现）

**唯一推荐落点**：在 `destination_candidate_v0` 已存在的前提下，在 `dispatch_voice_final_text(...)` 的 `short_controlled_input` 分支增加一个只读的 `destination_confirmation_fact_check_v0`：
- 输入：candidate + 当前句文本事实 +（可选）semantic_v2 confirm 意图/歧义线索
- 输出：只写 `metadata["destination_confirmation_fact_v0"]`（结构如 §F），不改 route/proposal/handoff/submit 行为

为什么选这里：
- 最连续：与 candidate/bound_check 同处短链结果，语境明确。
- 最不易失控：先形成事实位，再谈升级/确认模板，不直接跳转到 bound 或真实启动。

---

## J. 为什么现在还不能直接升级为 bound（写死）

- 现在只有 candidate 与 bound_check，没有 confirmation fact。
- 没有确认完成的结构化承载位，就无法证明用户真的认可当前 candidate。
- 因此不能从“听到对/confirm.yes”直接升级到 bound，更不能跳到真实导航启动。

---

## K. 下一步最小实现建议（只给 1 个方向）

**建议最先落地**：先做 `destination_confirmation_fact_v0` 的只读承载与评估器（`destination_confirmation_fact_check_v0`）：
- 仅在 candidate 已存在的语境下，观察“当前句是否像确认/否定/新候选”
- 满足冻结口径才写入 confirmation fact（否则不写）
- 不做 bound 升级、不接地图/记忆/视觉、不启动导航

