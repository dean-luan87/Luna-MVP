# Phase-Expression-001 — Navigation Output Timing Window Policy v0（时效窗口策略冻结）

**目标**：写死不同输出类型的有效期与过期处理，保证“过期不播报、动态事件短窗、普通导航中窗、求助限频”。  

---

## 1) 总原则（写死）

- 输出必须带 `generated_at` 与 `expires_at`（或 `validity_window_ms` 可推导）
- `now >= expires_at` 必须抑制（`suppression_reason="stale"`）
- 动态事件/高风险提示的窗口必须短；过期不得继续播报
- 任意候选即使 `priority=critical/high` 也不能越过“过期不播报”原则

---

## 2) 统一默认窗口（v0 固定值）

以下为 v0 固定默认值（毫秒）：

- `safety_warning`（critical safety warning）：`validity_window_ms = 2500`
- `dynamic_event_warning`（映射到 `safety_warning`，reason_codes 含 dynamic）：`validity_window_ms = 1500`
- `navigation_instruction_candidate`：`validity_window_ms = 8000`
- `status_confirmation`：`validity_window_ms = 12000`
- `low_confidence_notice`：`validity_window_ms = 5000`
- `ask_for_help_prompt`：`validity_window_ms = 10000`
- `wait_or_observe`：`validity_window_ms = 3000`
- `silence`：`validity_window_ms = 2000`

说明（写死约束）：
- “dynamic_event_warning”在 v0 中不新增 output_type，仅通过 `reason_codes` 标识为 dynamic，并使用更短窗口。

---

## 3) 重复播报间隔（v0 固定值）

repeat_policy（v0 固定建议）：
- `safety_warning`：`min_repeat_interval_ms = 3000`
- `navigation_instruction_candidate`：`min_repeat_interval_ms = 6000`
- `status_confirmation`：`min_repeat_interval_ms = 10000`
- `low_confidence_notice`：`min_repeat_interval_ms = 8000`
- `ask_for_help_prompt`：`min_repeat_interval_ms = 20000`
- `wait_or_observe`：`min_repeat_interval_ms = 5000`
- `silence`：`min_repeat_interval_ms = 0`

---

## 4) 过期处理（写死）

- **过期即抑制**：不得“补播报”
- **动态事件过期**：只能抑制并要求上游重新生成（由上游链路产生新候选）
- **普通导航过期**：抑制；允许下一个循环生成新导航候选

