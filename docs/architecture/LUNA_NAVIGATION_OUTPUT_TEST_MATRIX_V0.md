# Phase-Expression-001 — Navigation Output & Timing Control Test Matrix v0（A–M）

**目的**：矩阵化覆盖安全提醒、普通导航、低置信、超时、重复抑制、人工求助、静默、禁止语义阻断等核心用例。  

---

## 约定（统一）

- 输入：mock 的 scene/task/fusion candidates（以 dict 表示）  
- 输出：`navigation_output_candidate` 列表 + 抑制信息（suppression_reason）  
- 共同硬约束：所有输出候选 `allows_execute_now=false`；不得出现 execute/release/retry/reopen 语义  

---

## A. critical_safety_warning_case
- **输入**：高风险候选（`output_type=safety_warning`，`priority=critical`，reason_codes 含 `risk_immediate`）
- **预期**：
  - 输出安全提醒候选
  - `priority in {critical, high}`
  - 未过期

## B. normal_navigation_instruction_case
- **输入**：普通导航候选（`output_type=navigation_instruction_candidate`，`priority=medium`，confidence 高）
- **预期**：输出导航指令候选；不过期；不包含不确定性措辞强制化

## C. safety_suppresses_normal_case
- **输入**：同时存在安全提醒（critical/high）与普通导航（medium）
- **预期**：
  - 安全提醒输出
  - 普通导航被抑制或延后，`suppression_reason="suppressed_by_safety_warning"`

## D. stale_output_discard_case
- **输入**：任意候选已过期（expires_at <= now）
- **预期**：不得播报；`suppression_reason="stale"`；最终输出应可为 silence

## E. dynamic_event_timeout_case
- **输入**：动态事件安全提醒（reason_codes 含 `dynamic_event`）且过期
- **预期**：抑制；不得播报；记录 dynamic_timeout 指标命中

## F. low_confidence_notice_case
- **输入**：普通导航候选但 `confidence < low_confidence_threshold`
- **预期**：
  - 输出 `low_confidence_notice`（或对原候选抑制并降级）
  - 不得输出确定性指令文本

## G. ask_for_help_case
- **输入**：高不确定/复杂环境（reason_codes 含 `needs_human_assistance` 或 confidence 极低）
- **预期**：输出 `ask_for_help_prompt`；`requires_human_help=true`

## H. repeat_suppression_case
- **输入**：短时间内重复相同模板/原因的候选（触发 repeat_policy）
- **预期**：后续重复候选被抑制；`suppression_reason="repeat_rate_limited"`

## I. silence_valid_case
- **输入**：无有效候选或全被抑制
- **预期**：输出 `output_type=silence` 作为合法输出

## J. forbidden_execute_output_case
- **输入**：message_text_candidate 含 execute/release/retry/reopen 等禁词，或 allows_execute_now=true
- **预期**：阻断/抑制；计入 leakage；系统仍保持 `allows_execute_now=false`

## K. priority_order_case
- **输入**：多个候选不同 priority（critical/high/medium/low）
- **预期**：排序正确（priority order valid）

## L. expired_but_high_priority_case
- **输入**：`priority=critical` 但过期
- **预期**：仍不得播报（expired_high_priority_block）

## M. help_prompt_rate_limit_case
- **输入**：连续求助提示候选（短时间内重复）
- **预期**：限频生效；重复被抑制（repeat_rate_limited）

