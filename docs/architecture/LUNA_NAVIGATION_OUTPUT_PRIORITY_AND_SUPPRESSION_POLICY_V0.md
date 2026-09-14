# Phase-Expression-001 — Navigation Output Priority & Suppression Policy v0（优先级与抑制策略冻结）

**目标**：写死输出优先级与抑制规则，防止噪音式播报与过期播报；并确保“安全优先、不过期、不放权、不误导”。  

---

## 1) 总原则（写死）

- **Safety warning beats normal navigation**：安全提醒优先于普通导航
- **Critical/high may suppress low**：高优先级可压制低优先级（尤其 status confirmation）
- **Stale must not be spoken**：过期输出不得播报（即使高优先级）
- **Low confidence must not speak as certainty**：低置信不得确定化
- **Repetition must be rate-limited**：重复提醒必须限频/抑制
- **Help prompt is candidate-only**：求助提示仅候选，不触发任何真实动作
- **Silence is valid**：无输出也是合法输出（`output_type=silence`）
- **No execute/release/retry/reopen leakage**：输出层禁止出现触发语义；`allows_execute_now` 必须为 false

---

## 2) 优先级排序（写死）

priority 枚举从高到低：
1. `critical`
2. `high`
3. `medium`
4. `low`
5. `silent`

当 `priority` 相同，排序 tie-breaker（从高到低）：
1. `output_type=safety_warning` 优先
2. 更接近过期（更短的 `expires_at - now`）优先（但不允许过期播报）
3. `generated_at` 更新者优先

---

## 3) 抑制规则（写死）

### 3.1 过期抑制（Hard）
- 若 `now >= expires_at`：必须抑制，`suppression_reason="stale"`
- 过期的 `critical/high` 也必须抑制（不允许“过期但高优先级仍播报”）

### 3.2 安全压制普通导航（Hard）
- 若存在 `priority in {critical, high}` 且 `output_type=safety_warning` 的候选，
  - 则同一输出轮次内，`navigation_instruction_candidate` 与 `status_confirmation` 必须被抑制或延后
  - 被抑制者必须标注 `suppression_reason="suppressed_by_safety_warning"`

### 3.3 重复抑制（Hard）
- 若同一 `message_template_id`（或同一 `reason_codes` 组合）在 `repeat_policy.min_repeat_interval_ms` 内已输出过一次：
  - 必须抑制，`suppression_reason="repeat_rate_limited"`

### 3.4 低置信抑制/降级（Hard）
- 若 `confidence < low_confidence_threshold`：
  - 不得输出 `navigation_instruction_candidate` 的“确定性指令”文本
  - 必须输出 `low_confidence_notice` 或 `ask_for_help_prompt`（由 degraded policy 决定）
  - 如仍保留原候选，必须抑制并标注 `suppression_reason="low_confidence_degraded"`

### 3.5 静默（Hard）
- 若所有候选均被抑制或不存在有效候选：
  - 输出一个 `output_type=silence` 的候选作为合法结果（`priority=silent`）

---

## 4) 明确禁止（Hard）

任一出现即应在验证中计为泄漏与 illegal：
- 任何形式的 execute/release/retry/reopen/default-on/override/grant-control 语义
- `allows_execute_now=true`
- 过期内容被标记为可播报

