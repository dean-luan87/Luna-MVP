# Phase-Expression-001 — Navigation Output Candidate Contract v0（输出候选契约冻结）

**目的**：冻结输出候选 contract，确保输出层消费上游 scene/task/fusion candidates 后，只产出结构化“播报候选”，并严格保持不放权（`allows_execute_now=false`）。  
**性质**：contract；candidate-only；不触发真实执行。  

---

## 1) 总原则（写死）

- 输出必须结构化（JSON 可解析），不得直接自由文本进入播报链
- 所有 output candidate **必须** `allows_execute_now=false`
- 输出候选不等于真实执行；输出层不得打开 release window 或触发 retry/reopen

---

## 2) navigation_output_candidate（v0 schema）

字段（v0 写死最小集合）：
- `output_candidate_id`
- `source_candidate_id`
- `source_type`（枚举）
  - `scene_task`
  - `fusion`
  - `risk`
  - `degraded`
  - `help_prompt`
- `output_type`（枚举）
  - `safety_warning`
  - `navigation_instruction_candidate`
  - `status_confirmation`
  - `low_confidence_notice`
  - `ask_for_help_prompt`
  - `wait_or_observe`
  - `silence`
- `priority`（枚举）
  - `critical`
  - `high`
  - `medium`
  - `low`
  - `silent`
- `message_template_id`
- `message_text_candidate`
- `validity_window_ms`
- `generated_at`
- `expires_at`
- `repeat_policy`
- `suppression_reason`
- `requires_user_confirmation`
- `requires_human_help`
- `confidence`
- `reason_codes`
- `allows_execute_now`（写死：false）

---

## 3) 硬禁止（Hard Denylist）

输出候选中禁止出现（任一出现即 no-go）：
- execute/release/retry/reopen/default-on/override/grant control 语义
- `allows_execute_now=true`
- 过期信息被标记为可播报（stale 不得 speak）

---

## 4) 系统消费方式（写死）

- 输出层只做“播报候选生成/排序/抑制/过期丢弃/降级/求助提示”
- 不得将输出候选映射为真实执行触发条件

