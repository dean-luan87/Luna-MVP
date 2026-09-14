# Phase-RealSceneFix-001 — Real Scene Operator Notes & Risk Events Template v0（人工记录模板冻结）

**目的**：定义 controlled live run 的 operator notes 与 risk events 的最低记录模板，确保真实 run 可复盘、可归档、可审计。  

---

## 1) operator notes（最低字段）

operator notes 至少记录（建议 JSON 或 Markdown 结构化）：
- `operator_id`
- `safety_observer_id`
- `record_owner_id`
- `environment_summary`（白天/人流/路况等）
- `scenario_summary`（Option A + 简述）
- `observed_behavior_summary`（系统输出候选/抑制/降级摘要）
- `unexpected_behavior`（如有）
- `manual_intervention`（如有；描述+时间戳）
- `abort_used`（bool）
- `fallback_used`（bool）
- `degraded_used`（bool）
- `privacy_issue_observed`（bool）
- `follow_up_required`（bool + 简述）

---

## 2) risk events（最低字段）

risk events 以 JSONL 记录，每条事件至少包含：
- `event_id`
- `timestamp_ms`
- `risk_type`
- `risk_level`（low/medium/high/critical）
- `source`（枚举：`operator` / `system` / `observer`）
- `description`
- `action_taken`
- `linked_trace_id`（可为空，但建议提供）
- `resolved`（bool）

---

## 3) 无风险事件的处理（写死）

若无风险事件：
- `risk_events.jsonl` 仍必须存在
- 必须写入一条声明记录：
  - `risk_events_status=none_observed`
  - timestamp_ms
  - source=record_owner

不得缺失文件、不得以“空缺”代替“none_observed”。

