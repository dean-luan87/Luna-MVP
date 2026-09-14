# Phase-Next-157 — First Controlled Short-Window Trial Shadowed Validation Test Matrix v0

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_LIVE_IMPLEMENTATION_CONTROLLED_TRIAL_PREPARATION_FIRST_CONTROLLED_SHORT_WINDOW_TRIAL_SHADOWED_VALIDATION_TEST_MATRIX_V0.md`  
**目标**：把 Phase-Next-156 短窗 trial runtime 的验证场景与预期（started/release/abort/recovery/closure）矩阵化，供 157 工具与报告对齐复盘。

---

## 覆盖原则（写死）

- 157 只做验证/评估，不扩 156，不改变 151/155/156 语义
- `start_event_observed` 仍是唯一 started 判据
- `side_effects_released` 只允许在合法 started 后短窗打开，且 closure 后必须回落为 false
- timeout/unauthorized/audit-break 必须触发 abort，且 abort 必须能收口（recovery + closure）

---

## 场景矩阵（A–K）

说明：

- **explicit_entry**：是否通过显式入口调用（157 工具对真实 runtime 场景均为 true；对 synthetic probe 为 false）
- **intent/approval**：是否提供且被 runtime 识别为 seen
- **start_event_observed**：是否应出现
- **started**：是否允许出现
- **side_effects_released**：是否允许最终为 true（本矩阵默认要求“最终为 false”）
- **abort_trigger_id**：如应 abort，触发原因
- **closure**：是否必须为 true
- **illegal**：是否应被识别为 illegal（用于合成/探测类场景）

| 场景 | 名称 | explicit_entry | intent_seen | approval_seen | start_event_observed | started | abort_trigger_id | rollback | recovery | closure | illegal |
|---|---|---:|---:|---:|---:|---:|---|---:|---:|---:|---:|
| A | no_explicit_intent | true | false | true | false | false | (n/a) | false | false | true | false |
| B | no_approval | true | true | false | false | false | (n/a) | false | false | true | false |
| C | armed_but_not_started | true | true | true | false | false | (n/a) | false | false | true | false |
| D | legal_short_window_success | true | true | true | true | true | (n/a) | false | false | true | false |
| E | legal_short_window_failure | true | true | true | true | true | (n/a) | true | (optional) | true | false |
| F | window_timeout | true | true | true | false | false | trial_window_timeout | false | false | true | false |
| G | unauthorized_surface | true | true | true | false | false | unauthorized_side_effect_surface | false | false | true | false |
| H | illegal_release_before_started | false | true | true | false | false | (n/a) | false | false | false | true |
| I | missing_audit_trace | true | true | true | false | false | audit_trace_missing_or_broken | false | false | true | false |
| J | default_path_probe | true | false | true | false | false | (n/a) | false | false | true | false |
| K | closure_break_probe | false | true | true | true | true | (n/a) | false | false | false | true |

---

## 关键断言（用于 157 评价口径）

- **entry gate integrity**：A/B/J 必须全部“不 started、不 release、closed”
- **started boundary integrity**：任一出现 `started=true` 都必须同时满足 `start_event_observed=true`
- **release boundary integrity**：任何 `release=true` 都必须发生在 `started=true` 之后；且 closure 后必须回落为 false
- **abort integrity**：F/G/I 必须 abort 并收口（closed=true, se=false）
- **closure integrity**：D/E 必须 closed=true；K 必须被判 illegal（started 但未 closed）

