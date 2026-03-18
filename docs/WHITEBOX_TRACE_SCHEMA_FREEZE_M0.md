# Whitebox Trace Schema Freeze M0（Luna 统一白盒轨迹模板冻结）

## §1 文档定位

本文档为 **Luna 白盒轨迹模板冻结文档**（M0）。  
它不是单模块 delivery、不是调试手册、不是 roadmap；而是后续模块白盒化输出的**统一基线与约束**。

---

## §2 为什么需要白盒模板

- **只有结果不够**：推荐/选择/推进必须能解释“为什么”。  
- **需要过程可解释**：支持调试、经验治理、风险审计与对外演示。  
- **防止分裂**：若各模块各写各的 trace，字段不可复用、Viewer/审计不可维护。  

---

## §3 当前冻结的统一白盒模板（五块骨架）

所有模块白盒化输出优先复用以下五块骨架；允许模块扩展字段，但不得绕开骨架。

### A. reasoning_steps（推理过程）

最小字段：
- `step_index`
- `step_name`
- `step_input_summary`
- `step_output_summary`

### B. weight_allocation（权重分配）

最小字段（统一抽象）：
- `target_id`（或 `cell_id` / `candidate_id` 等同义目标标识）
- `target_human_label`
- `weight_total`
- `weight_components`（字典/列表，记录各项分值）
- `weight_reason`

### C. exclusion_log（排除逻辑）

最小字段：
- `excluded_target_id`
- `excluded_target_human_label`
- `excluded_reason`
- `excluded_at_stage`（例如 primary_selection / secondary_selection）

### D. interaction_trace（互动过程）

最小字段：
- `system_prompt_summary`
- `system_followup_summary`
- `user_feedback_raw`
- `mapped_confirmation_type`
- `next_effect`
- `interaction_effect_on_result`

### E. result_summary（结果摘要）

最小字段：
- `whitebox_summary`
- `whitebox_applied`

---

## §3a 白盒分层原则（写死）

- **白盒必须可审计**：内部调试、审计、经验治理用，保留完整内容（reasoning_steps、weight_allocation、exclusion_log、interaction_trace、raw summary）。
- **其中一部分必须可用户可见**：用于未来线上与用户交互（为什么我这么判断、我优先看哪里、为什么没选另一条路径、你刚才的反馈让我改了什么判断）。
- **用户可见白盒是“解释映射层”**：不得把 weight_components 等原始 JSON 直出给用户；必须产出一组**用户可见解释字段**（短句、可理解），真实映射内部白盒原因，但不泄露内部分值/结构细节。

即：**内部白盒层**（完整 trace）与 **用户可见白盒层**（解释短句）并存；用户可见层是解释映射，不是原始日志直出。

---

## §4 模板字段的语义边界

- **reasoning_steps**：解释推理路径（输入→输出），不要求细节全量结构化，但必须可读可审计。  
- **weight_allocation**：显式规则/权重/分值构成；当前可为规则权重（非学习权重）。  
- **exclusion_log**：说明“没选谁”与排除依据；不能只记录选中的目标。  
- **interaction_trace**：说明系统提示与用户反馈如何影响结果（或无互动）。  
- **summary/applied**：提供 runtime/viewer 的快速摘要与是否生效标志。  

---

## §5 当前哪些模块已接入该模板

- **已接入（正式样板）**：
  - Grid-driven Search Expansion 的白盒轨迹 `grid_search_whitebox_trace`（Grid Search Whitebox Trace M0）。
  - Recheck Planner 的白盒轨迹 `recheck_whitebox_trace`（Recheck Whitebox Trace M0）。
  - Action Hint 的白盒轨迹 `action_hint_whitebox_trace`（Action Hint Whitebox Trace M0，含用户可见解释层；单测 + smoke/JSONL 已闭环）。
- **未接入**：其余模块尚未白盒化，但后续应优先复用本模板。

---

## §6 后续模块接入要求（优先复用模板）

后续若进入 Luna 正式能力链路且涉及“建议/选择/排除/用户反馈驱动推进”，应优先沿用本模板：

- Recheck Planner（补证建议）
- Action Hint（引导提示生成）
- Confirmation 推进层（反馈→推进）
- Experience / Evidence 治理（经验候选升格/排除）
- Local Task Space Grid 进阶版本
- 未来局部环境模型的搜索层/建议层

---

## §7 当前边界

- 本文冻结的是**结构**，不是要求所有模块拥有相同的 weight 项集合。  
- 当前不代表全系统所有模块已白盒化。  
- 模块可扩展字段，但必须置于统一五块骨架之下，且不得改名/改语义；若必须变更，需显式修订本文档与 CONTRACT。  

---

## §8 白盒模板最小示例（基于 Grid Search Expansion）

以下为结构示意（字段名以统一模板为准，内容仅示例）：  

- reasoning_steps（4 条）：
  - 1) read_context: flow=container_check_flow; focus=right_mid; container=center_front → strategy=container_priority
  - 2) select_primary: container 优先 → primary=center_front
  - 3) select_secondary: primary adjacent + 补 focus → secondary=[left_mid, center_mid, right_mid]
  - 4) compose_hint: “如果中前区没有，再看左中区或中间区”

- weight_allocation（3 条）：
  - center_front total=0.70 comps={container_priority_score:+0.70}
  - right_mid total=0.20 comps={focus_bonus:+0.20}
  - left_back total=-0.30 comps={weak_relevance_penalty:-0.10, non_adjacent_penalty:-0.20}

- exclusion_log（1 条）：
  - excluded=left_back reason=non_adjacent_or_weak_relevance at=secondary_selection

- interaction_trace（1 条）：
  - no_interaction_this_frame

- result_summary（1 条）：
  - whitebox_summary=primary=center_front; secondary=...; excluded=...
  - whitebox_applied=true

---

## §9 命名约定（写死）

正式白盒结果字段命名采用：
- `*_whitebox_trace`

例如：
- `grid_search_whitebox_trace`
- `recheck_whitebox_trace`
- `action_hint_whitebox_trace`

---

## §10 结论

**Luna 统一白盒轨迹模板已冻结**。后续正式模块白盒化应优先按本模板输出“结果 + 过程”的可解释轨迹；模块扩展允许，但不得绕开统一骨架。

