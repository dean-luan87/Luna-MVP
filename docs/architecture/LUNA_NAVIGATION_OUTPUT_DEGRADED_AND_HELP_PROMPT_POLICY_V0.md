# Phase-Expression-001 — Navigation Output Degraded & Help Prompt Policy v0（降级与求助策略冻结）

**目标**：在低置信/冲突/复杂环境下，输出必须保守、不误导；必要时输出“求助提示候选”，但不触发任何真实动作。  

---

## 1) 总原则（写死）

- 低置信不得假装确定：不得把不确定事实表达为确定指令
- 在高风险或冲突无法消解时，允许输出求助提示（candidate-only）
- 求助提示必须限频（避免噪音）
- 任何降级/求助都必须保持 `allows_execute_now=false`

---

## 2) v0 阈值（固定）

- `low_confidence_threshold = 0.55`
- `help_prompt_trigger_threshold = 0.35`

解释（写死）：阈值仅用于 v0 验证与行为冻结；后续可在不破坏 contract 的前提下调整（通过新版本 policy）。

---

## 3) 低置信降级规则（写死）

当候选满足任一条件时，必须触发降级：
- `confidence < low_confidence_threshold`
- `reason_codes` 包含：
  - `conflict_unresolved`
  - `risk_ambiguous`
  - `scene_uncertain`

降级输出要求：
- 必须输出 `output_type=low_confidence_notice`，并在 `message_text_candidate` 中包含不确定性表达（例如“我不确定/可能/建议先观察”）
- 不得输出“确定性导航指令”文本（validation 会用关键字规则近似检查）
- `requires_user_confirmation=true`（v0 固定）

---

## 4) 求助提示规则（写死）

触发条件（任一满足即可）：
- `confidence < help_prompt_trigger_threshold`
- `reason_codes` 包含：
  - `needs_human_assistance`
  - `complex_environment`
  - `high_risk_no_safe_action`

输出要求：
- 输出 `output_type=ask_for_help_prompt`
- `requires_human_help=true`
- `priority` 不得高于 `high`（避免覆盖 critical safety warning）
- 必须限频：参照 timing window policy 的 `ask_for_help_prompt min_repeat_interval_ms`

---

## 5) 与安全提醒的关系（写死）

- 若同轮同时存在 `safety_warning`（critical/high）与 `ask_for_help_prompt`：
  - 先输出安全提醒；求助提示可被抑制或延后（由 suppression policy 执行）

