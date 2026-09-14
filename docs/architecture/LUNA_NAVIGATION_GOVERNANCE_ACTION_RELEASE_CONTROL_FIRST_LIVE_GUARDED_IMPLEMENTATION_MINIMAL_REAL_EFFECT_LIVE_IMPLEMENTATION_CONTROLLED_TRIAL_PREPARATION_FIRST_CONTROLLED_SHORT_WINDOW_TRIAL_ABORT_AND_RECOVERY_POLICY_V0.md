# Luna — Navigation Governance Action Release Control First Live Guarded Implementation Minimal Real-Effect Live Implementation Controlled Trial Preparation First Controlled Short-Window Trial Abort And Recovery Policy v0（中止与恢复硬策略冻结）

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_LIVE_IMPLEMENTATION_CONTROLLED_TRIAL_PREPARATION_FIRST_CONTROLLED_SHORT_WINDOW_TRIAL_ABORT_AND_RECOVERY_POLICY_V0.md`  
**性质**：Phase-Next-155：把 short-window trial 期间的 abort/rollback/recovery/final close 写成硬规则，防止 started 后无法及时收口（无代码）

---

## Abort Policy Schema（写死字段）

每条 abort trigger 必须具备：

- abort_trigger_id
- trigger_description
- boundary_type: started | release | closure | window_timeout | unauthorized_scope | audit_failure
- immediate_action
- rollback_required
- recovery_required
- final_safe_state_required
- escalation_required

---

## Abort Triggers（写死至少覆盖以下）

### 1) no_start_event_but_started

- **abort_trigger_id**: `no_start_event_but_started`
- **trigger_description**: 未观测到 start_event_observed 却出现 started
- **boundary_type**: started
- **immediate_action**: 立即 abort，停止所有继续尝试
- **rollback_required**: 是
- **recovery_required**: 必须恢复/确认 se=false
- **final_safe_state_required**: closed=true 且无半开启状态
- **escalation_required**: 是（人工确认/升级）

### 2) no_started_but_release

- **abort_trigger_id**: `no_started_but_release`
- **trigger_description**: 未 started 即出现 side_effects window/release
- **boundary_type**: release
- **immediate_action**: 立即 abort
- **rollback_required**: 是
- **recovery_required**: 必须恢复/确认 se=false
- **final_safe_state_required**: closed=true
- **escalation_required**: 是

### 3) closure_missing

- **abort_trigger_id**: `closure_missing`
- **trigger_description**: started 后未能进入 closure，出现 started-but-unclosed
- **boundary_type**: closure
- **immediate_action**: 立即 abort
- **rollback_required**: 是
- **recovery_required**: 必须恢复/确认 se=false
- **final_safe_state_required**: closed=true
- **escalation_required**: 是

### 4) se_not_recovered

- **abort_trigger_id**: `se_not_recovered`
- **trigger_description**: closure 后 side_effects_released 未回落为 false（或等价安全闭合）
- **boundary_type**: closure
- **immediate_action**: 立即 abort + 强制恢复
- **rollback_required**: 是
- **recovery_required**: 必须恢复/确认 se=false（不可跳过）
- **final_safe_state_required**: closed=true
- **escalation_required**: 是

### 5) unauthorized_side_effect_surface

- **abort_trigger_id**: `unauthorized_side_effect_surface`
- **trigger_description**: 触碰未授权副作用面（非三类允许面）
- **boundary_type**: unauthorized_scope
- **immediate_action**: 立即 abort
- **rollback_required**: 是
- **recovery_required**: 必须恢复/确认 se=false
- **final_safe_state_required**: closed=true
- **escalation_required**: 是

### 6) trial_window_timeout

- **abort_trigger_id**: `trial_window_timeout`
- **trigger_description**: short-window 超时（超过最大持续时间上限）
- **boundary_type**: window_timeout
- **immediate_action**: 立即 abort
- **rollback_required**: 是
- **recovery_required**: 必须恢复/确认 se=false
- **final_safe_state_required**: closed=true
- **escalation_required**: 视情况（可选）

### 7) trial_scope_expanded_without_definition

- **abort_trigger_id**: `trial_scope_expanded_without_definition`
- **trigger_description**: 未新增治理定义即扩围（时长/次数/并发/范围/副作用类别）
- **boundary_type**: unauthorized_scope
- **immediate_action**: 立即 abort
- **rollback_required**: 是
- **recovery_required**: 必须恢复/确认 se=false
- **final_safe_state_required**: closed=true
- **escalation_required**: 是

### 8) audit_trace_missing_or_broken

- **abort_trigger_id**: `audit_trace_missing_or_broken`
- **trigger_description**: 审计 trace 缺失或不可复盘（无法定位 started/release/closure 边界）
- **boundary_type**: audit_failure
- **immediate_action**: 立即 abort
- **rollback_required**: 是
- **recovery_required**: 必须恢复/确认 se=false
- **final_safe_state_required**: closed=true
- **escalation_required**: 是

---

## Recovery / Closure 强制要求（写死）

abort 或试运行结束后必须：

1) 停止继续尝试（熔断优先）  
2) 恢复/确认 `side_effects_released=false`（或等价安全闭合态）  
3) 写最小复盘证据（不得扩面）  
4) `closed=true`（不得残留半开启状态）  

