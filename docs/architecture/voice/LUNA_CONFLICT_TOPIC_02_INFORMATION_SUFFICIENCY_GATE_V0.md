# 冲突专题 02：信息完整性冲突 / Information Sufficiency Gate v0（设计冻结）

**文件**：`docs/architecture/voice/LUNA_CONFLICT_TOPIC_02_INFORMATION_SUFFICIENCY_GATE_V0.md`  
**性质**：冲突治理宪法 v0 之下的第二个执行准入专题（只做设计与口径冻结）  
**不做**：实现 gate、不改主链行为、不接白盒、不接 provenance、不碰视觉解释、不扩 `resume/repeat`、不处理文本↔视角冲突。  

上位约束（必须服从）：  
- `docs/architecture/voice/LUNA_CONFLICT_GOVERNANCE_CONSTITUTION_V0.md`  
- `docs/architecture/voice/LUNA_VOICE_MAINLINE_BASELINE.md`  

并强调：**宪法高于专题**；**主链事实高于辅助信号**；**历史记忆只能辅助，不得替代必要确认**。

---

## A. 专题定位

- 本专题只讨论：**必要信息不足时不得直接执行**。  
- 本专题不处理：资源不足（已由 Topic 01 下的 Resource Gate 覆盖）、风险冲突、文本 vs 视角冲突、以及 `resume/repeat` 等高歧义意图策略。  
- 本专题目标：给出 **Information Sufficiency Gate v0** 的最小边界、输入、口径与未来落点（仅设计，不实现）。

---

## B. 当前适用场景（v0）

至少覆盖三类典型缺口：

1) **用户意图存在，但执行对象不明确**  
- 例：“帮我停一下”“继续那个”“去那里”——执行对象/目标引用未明确。

2) **用户意图存在，但关键参数缺失**  
- 例：需要目标地点、任务对象、执行范围、确认对象等关键参数。

3) **用户意图存在，但上下文承接不足**  
- 例：“这个/那个/刚才那个”无法在当前主链事实内被唯一指代。

---

## C. 必要信息 vs 非必要信息（定义写死）

### C1. 必要信息（Required）

**缺失时不得执行，必须补齐**。满足任一即视为“必要信息”：

- 会直接改变执行结果或安全边界的信息  
- 作为执行准入的关键参数  
- 用户引用对象的唯一指代依据（若无则不可执行）

示例（按类别，不强制穷举）：  
- 执行对象（对谁/对什么做）  
- 目标对象（找什么/拿什么/确认什么）  
- 目标地点（去哪里）  
- 当前任务引用对象（“继续哪个任务/哪个阶段/哪个目标”）  

### C2. 非必要信息（Optional）

**缺失时不必立即阻断**，可以参考：历史记忆、当前上下文、保守推理；但必须满足：

- 不能直接当作“执行事实”写入或触发不可逆执行  
- 一旦这些补充会影响执行决策，必须经用户确认  
- 不得违反宪法第一、第二原则与 No Fabrication

---

## D. 当前最小判断输入（v0）

概念结构（不要求当前实现具备全部字段）：  

- `user_request`：用户显式表达（原文与已归一化文本）  
- `mainline_facts`（主要依据）：  
  - `VoiceInputEvent`：raw/normalized/current_mode/router_decision/shortcut_id 等  
  - `dispatch_type`、`bridge_decision.route`、`proposal.device_action`（若存在）  
- `semantic_output`（辅助发现缺失项，不替代事实）：  
  - `intent` / `ambiguities` / `requires_followup` / `confidence`  
- `session_state_anchor`：`VoiceV1SessionStateAnchor`（只读事实锚）  
- `context_references`：用户显式引用（如“这个/那个/刚才那个”）  
- `supporting_signals`（只辅助）：`semantic_v2_shadow`、V3 pack、`vision_shadow` 等  

写死约束：  
- 用户显式输入与 `mainline_facts` 优先  
- `semantic_output` 可提示“缺什么”，但不得补成可执行事实  
- supporting_signals 不得单独补齐 Required 信息

---

## E. 最小处理口径（工程化规则）

1) **必要信息完整**  
- 可继续进入执行链（不代表一定执行；仍须过资源/风险等其它 gate）

2) **必要信息缺失**  
- **不得执行**  
- 优先要求补充必要信息  
- 可给出最小追问或确认（但不在本专题内定义具体对话模板）

3) **非必要信息缺失**  
- 可保守继续  
- 可参考历史/上下文，但不得把推断当事实执行  
- 若补充会影响执行决策，必须经用户确认

4) **引用歧义（指代不唯一）**  
- 不得强判  
- 优先进入确认路径（`requires_followup` / confirmation），或保守降级  
- 不允许脑补“这个/那个”具体指向

---

## F. 最小响应等级映射（5 档）

- **直接执行**：必要信息完整，且无其它 gate 阻断  
- **提示后执行**：必要信息完整但存在轻微不确定（不影响安全与结果）  
- **要求确认**：必要信息缺失或引用歧义；或补充信息将影响决策  
- **保守降级**：缺口较大但可提供安全替代（例如仅提示/仅建议不执行）  
- **明确拒绝**：关键必要信息无法补齐且会触碰安全/底线或导致不可逆错误执行

口径写死：**“必要信息缺失”通常至少落到“要求确认”**；严重缺失/高不确定可落到降级/拒绝。

---

## G. 当前明确禁止项（写死）

- 不允许因为历史记忆存在就跳过必要确认  
- 不允许因为语义层给了高置信 intent 就脑补执行对象/目标地点  
- 不允许视觉摘要替代用户提供的关键对象信息  
- 不允许在本专题里顺手实现 `resume/repeat` 的具体冲突策略  
- 不允许把本专题做成大而全对话管理系统

---

## H. 推荐的最小未来落点（只做设计，不实现）

**唯一推荐未来落点（v0）**：与 Resource Gate 一致风格——在 `dispatch_voice_final_text(...)` 之后、`_maybe_submit_real_output_v1(...)` 之前，作为第二个 admission gate（Information Sufficiency Gate）。  

理由：  
- 此处已拥有 `dispatch_type/bridge_decision/proposal` 等 **mainline_facts**；  
- 可以在不改分流的前提下，仅影响“是否允许进入 submit”；  
- 与 Resource Gate 形成可组合的准入链，不把治理塞进语义层（避免语义夺权）。

本轮仅冻结该落点建议，不改代码。

---

## I. 下一步最小实现建议（只给 1 个方向）

**建议最先落地**：引用对象缺失/歧义时的 **confirmation gate v0**（只做“阻断 submit + 标记需要确认”的最小链路）。  

理由：  
- 最容易与 Required/Optional 的定义对齐；  
- 最不依赖视觉解释与复杂模型；  
- 最能形成可回归闭环（缺失→阻断→确认）。

---

## J. 已冻结 Gate Baseline（Index）

- Information Confirmation Gate v0 Baseline / Freeze  
  `docs/architecture/voice/LUNA_INFORMATION_CONFIRMATION_GATE_V0_BASELINE.md`

