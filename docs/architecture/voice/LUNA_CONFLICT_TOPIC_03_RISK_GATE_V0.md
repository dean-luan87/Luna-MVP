# 冲突专题 03：Risk Gate v0（设计冻结）

**文件**：`docs/architecture/voice/LUNA_CONFLICT_TOPIC_03_RISK_GATE_V0.md`  
**性质**：执行准入层（pre-submit admission layer）的下一专题设计（只做设计与口径冻结，不做实现）  
**不做**：实现 gate、不改主链行为、不接白盒、不接 provenance、不碰视觉解释实现、不扩 `resume/repeat`、不处理文本↔视角冲突、不做中台审核实现。  

上位约束（必须服从）：  
- `docs/architecture/voice/LUNA_CONFLICT_GOVERNANCE_CONSTITUTION_V0.md`  
- `docs/architecture/voice/LUNA_VOICE_PRE_SUBMIT_ADMISSION_LAYER_V0.md`  
- `docs/architecture/voice/LUNA_VOICE_MAINLINE_BASELINE.md`  

并强调：**宪法高于专题**；**主链事实高于辅助信号**；Risk Gate 不得绕过 No Fabrication；时空锚点仍只能消费中台统一基准。

---

## A. 专题定位

- 本专题只讨论：当系统判断存在**明确风险**时，是否允许继续进入 submit（未来 gate）。  
- 本专题当前只冻结：输入分层、口径边界、禁止项、未来落点（不实现）。  
- 本专题不处理：文本 vs 视角冲突、用户协商策略、中台审核实现、`resume/repeat` 高歧义意图策略、以及视觉解释层实现。

---

## B. 当前适用场景（v0）

至少覆盖三类：

1) **系统已有风险摘要，但用户仍要求继续**  
（例如用户坚持继续前进/继续执行，但风险摘要提示高风险）

2) **系统已有场景/环境摘要显示环境不稳定或危险**  
（例如环境摘要/风险摘要提示可能危险，但尚不足以形成“可拦截的风险事实”）

3) **主链准备继续输出/执行，但风险事实提示不宜继续**  
（例如即将进入 submit，但当前风险事实已达到高风险阈值——未来 gate 的典型触发点）

---

## C. 风险判断输入分层（v0）

### C1. 主链事实候选（可进入 admission layer 的风险事实来源候选）

> 目标：定义“未来哪些风险信息可以被视为主链可用事实”，但不等于当前立即可用。

- **`runtime_context.metadata["risk_summary_v1"]`**（候选）  
  - 当前在 `voice_final_text_dispatcher.py` 中已有“优先读 runtime_context，其次回退 event.metadata”的读取口径（`_risk_summary_v1_for_orchestrator_observation`）。  
  - 现状：更多用于旁路白盒/试点逻辑与观测；尚未作为 admission layer 的稳定 gate 依据冻结。

- **`event.metadata["risk_summary_v1"]`**（候选但更弱）  
  - 作为缺失回退来源存在，但其可信等级与注入路径需要专项评估后才能进入 gate。

**重要说明（写死）**：在风险事实尚未形成稳定 schema/可信注入路径前，Risk Gate 不得把这些候选直接当成可拦截依据。

### C2. 辅助信号（只能辅助，不能单独决定拦截）

以下均为辅助信号，不能单独触发风险拦截：

- V3 视角摘要承载：`luna_voice_vision_semantic_v3_input`（摘要键存在 ≠ 风险事实）  
- V2 `vision_shadow`（seen_not_interpreted / not_seen）  
- V2 语义与 shadow/assist：`semantic_v2_shadow`、`semantic_v2_assist_*`（语义不能替代风险事实）  
- `sidewalk_env_summary_v1` / `retail_env_summary_v1`（环境摘要 ≠ 风险结论；除非未来另有风险解释层与 schema 冻结）

### C3. 当前缺口（导致不能直接实现 Risk Gate）

当前至少缺少以下关键条件，因此仅能做专题设计冻结：

- **稳定、可冻结的风险 schema**：缺少“risk_gate_ready”级别的字段定义与版本约束（例如 schema_version、来源声明、有效期等）  
- **风险事实的注入责任边界**：缺少明确声明“risk_summary_v1 来自哪里、谁负责、如何回滚”的主链契约  
- **与主链输出/执行关系的最小映射**：缺少“哪些输出/执行类别在高风险时必须阻断”的冻结口径（本专题不展开实现，只冻结方向）  

---

## D. 最小处理口径（工程化规则）

1) **无明确风险事实**  
- 不因“看起来像危险”就拦截。  
- 不因辅助信号（语义/视觉摘要/影子）就拦截。  

2) **风险事实存在但不足以形成 gate 依据**  
- 只能提示或保留为辅助信号/观测字段。  
- 不得直接拦 submit。  

3) **风险事实足够明确（未来 gate 候选条件）**  
- 允许进入未来 Risk Gate 的准入条件候选：\n
  - 风险字段来源明确、schema 稳定、注入路径可信\n
  - 风险等级达到 high（见 §E）\n
- 本轮只定义“条件候选”，不落实现。

并明确：  
- 风险 gate（若未来加入）必须高于用户“继续”的偏好（宪法优先级）。  
- 但风险 gate 不能靠辅助信号单独触发。

---

## E. 风险等级最小分层建议（极小）

仅建议一个最小分层（不扩复杂体系）：  
- `none`  
- `warning`  
- `high`  

写死口径：  
- 只有当未来能形成**明确、稳定、主链可用**的 `high` 风险事实时，才值得进入 gate 拦截条件候选。  
- `warning` 级别在 v0 不应被设计为“可拦截 submit”的条件（最多提示/观测）。

---

## F. 当前明确禁止项（写死）

- 不允许仅凭视觉摘要“像危险”就拦截  
- 不允许仅凭语义层或 shadow/assist 推断就拦截  
- 不允许把 `risk_summary_v1` 在当前阶段直接当作可执行 gate 条件，除非未来先形成稳定 schema 与注入责任边界  
- 不允许在本专题里顺手实现文本 vs 视角冲突  
- 不允许在本专题里顺手实现用户协商逻辑  

---

## G. 推荐的最小未来落点（只做设计，不实现）

**唯一推荐未来落点（v0）**：仍落在 pre-submit admission layer：`dispatch_voice_final_text(...)` 之后、`_maybe_submit_real_output_v1(...)` 之前，作为**第三个 admission gate**。  

为什么是这里：  
- 此处不改主链裁决（dispatch_type/route/proposal 已成事实），只影响 submit 准入，符合 admission layer 的边界。  
- 与现有 admission layer 风格一致（Resource / Information）。  

与前两 gate 的相对位置（建议）：  
- **建议先保持现有顺序冻结不动**（Resource → Information），Risk Gate 作为第三个 gate 追加在其后。  
- 若未来要把 Risk Gate 提前（更符合安全优先级），必须单开专项评审“顺序调整”，不得在实现阶段随意插队。

---

## H. 与现有 admission layer 的关系

当前 admission layer 已冻结为：  
1) Resource Sufficiency Gate v0（能不能执行）  
2) Information Confirmation Gate v0（是否已足够明确到可以执行）  

Risk Gate（若未来加入）必须明确：  
- 它只影响 submit 准入，不改主链裁决；  
- 不能依赖辅助信号触发；  
- 与前两 gate 的顺序调整必须专项评审（见 §G）。

---

## I. 下一步最小实现建议（只给 1 个方向）

**建议最先落地**：`risk_summary_v1` 的 **schema 冻结与 gate-ready 可用性评估**（不做 gate）。  

理由：  
- 在没有稳定 schema 与注入责任边界前，实现 Risk Gate 会违反“主链事实高于辅助信号”的约束；  
- 先把 risk_summary_v1 从“观测/试点输入”推进到“可作为主链事实候选”的冻结面，才能进入 gate 实现阶段。

---

## J. 前置契约索引（Risk Gate 之前必须冻结）

- `risk_summary_v1` Gate-Ready Contract v0：  
  `docs/architecture/voice/LUNA_RISK_SUMMARY_V1_GATE_READY_CONTRACT.md`  

写死口径：在 Risk Gate 进入任何实现轮次前，必须先冻结并遵守上述契约；否则 `risk_summary_v1` 仍只属于观测/试点输入，不能进入 admission layer 的 gate 条件候选。

---

## K. 已冻结基线（Topic 03 当前唯一已落地阶段）

- `risk_summary_v1` Gate-Ready Eval v0 Baseline / Freeze（只读评估层，不是 Risk Gate）：  
  `docs/architecture/voice/LUNA_RISK_SUMMARY_V1_GATE_READY_EVAL_V0_BASELINE.md`

