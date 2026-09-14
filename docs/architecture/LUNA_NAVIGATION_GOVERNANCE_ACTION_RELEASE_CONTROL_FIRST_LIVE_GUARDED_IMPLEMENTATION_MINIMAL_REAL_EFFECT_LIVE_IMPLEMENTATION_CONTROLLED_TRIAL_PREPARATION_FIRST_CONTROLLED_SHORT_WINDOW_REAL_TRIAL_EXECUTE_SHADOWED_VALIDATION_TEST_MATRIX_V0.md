# Phase-Next-161 — First Controlled Short-Window Real Trial Execute Shadowed Validation Test Matrix v0

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_LIVE_IMPLEMENTATION_CONTROLLED_TRIAL_PREPARATION_FIRST_CONTROLLED_SHORT_WINDOW_REAL_TRIAL_EXECUTE_SHADOWED_VALIDATION_TEST_MATRIX_V0.md`  
**目标**：把 Phase-Next-160 真实 execute runtime 的验证场景与预期（entry/started/release/stop/abort/recovery/final close）矩阵化，供 161 工具与报告对齐复盘。

---

## 覆盖原则（写死）

- 161 只做验证/评估，不扩 160，不改变 151/155/158/159/160 语义
- `start_event_observed` 仍是唯一 started 判据
- `side_effects_released` 仅允许在合法 started 后短时打开，且 final close 后必须回落为 false
- timeout/unauthorized/audit-failure/readiness 缺失 必须 stop/abort 且收口（closed=true, se=false）

---

## 场景矩阵（A–M）

说明：

- **explicit_entry**：是否通过显式入口调用（161 工具对真实 runtime 场景均为 true；对 synthetic probe 为 false）
- **intent/approval/readiness_go**：是否提供且被 runtime 识别为 seen
- **start_event_observed**：是否应出现
- **started**：是否允许出现
- **abort_trigger_id**：如应 abort，触发原因
- **final_close**：是否必须为 true
- **illegal**：是否应被识别为 illegal（用于合成/探测类场景）

| 场景 | 名称 | explicit_entry | intent_seen | approval_seen | readiness_go_seen | start_event_observed | started | abort_trigger_id | rollback | recovery | final_close | illegal |
|---|---|---:|---:|---:|---:|---:|---:|---|---:|---:|---:|---:|
| A | no_execute_intent | true | false | false | false | false | false | execute_without_explicit_intent | true | true | true | false |
| B | no_approval | true | true | false | false | false | false | execute_without_explicit_approval | true | true | true | false |
| C | no_readiness_go | true | true | true | false | false | false | execute_without_readiness_go | true | true | true | false |
| D | armed_but_not_started | true | true | true | true | false | false | (n/a) | false | false | true | false |
| E | legal_real_trial_execute_success | true | true | true | true | true | true | (n/a) | false | (implicit) | true | false |
| F | legal_real_trial_execute_failure | true | true | true | true | true | true | (n/a) | true | (implicit) | true | false |
| G | execute_window_timeout | true | true | true | true | false | false | execute_window_timeout | true | true | true | false |
| H | unauthorized_surface | true | true | true | true | false | false | unauthorized_side_effect_surface | true | true | true | false |
| I | missing_audit_trace | true | true | true | true | false | false | audit_trace_missing_or_broken | true | true | true | false |
| J | illegal_release_before_started | false | true | true | true | false | false | (n/a) | false | false | false | true |
| K | execute_without_readiness_go | true | true | true | false | false | false | execute_without_readiness_go | true | true | true | false |
| L | default_path_probe | true | false | false | false | false | false | execute_without_explicit_intent | true | true | true | false |
| M | final_close_break_probe | false | true | true | true | true | true | (n/a) | false | false | false | true |

---

## 关键断言（用于 161 评价口径）

- **entry gate integrity**：A/B/L 必须全部“不 started、不 release、final_close=true”
- **readiness gate integrity**：C/K 必须 abort 且 `abort_trigger_id=execute_without_readiness_go`
- **started boundary integrity**：任一出现 `started=true` 都必须同时满足 `start_event_observed=true`
- **release boundary integrity**：任何 `release=true` 都必须发生在 `started=true` 之后；且 final close 后必须回落为 false
- **stop/abort integrity**：G/H/I 必须 stop/abort 并收口（closed=true, se=false）
- **final close integrity**：E/F 必须 final_close=true；M 必须被判 illegal（started 但未 final_close）

