# Luna — Navigation Governance Action Release Control First Live Guarded Implementation Minimal Real-Effect Live Implementation Controlled Trial Preparation First Controlled Short-Window Real Trial Execute Implementation v0

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_LIVE_IMPLEMENTATION_CONTROLLED_TRIAL_PREPARATION_FIRST_CONTROLLED_SHORT_WINDOW_REAL_TRIAL_EXECUTE_IMPLEMENTATION_V0.md`  
**阶段**：Phase-Next-160  
**性质**：第一版真实 short-window real trial execute runtime（实现），严格受 151/155/158/159 约束。  
**非目标**：不 default-on、不 full controlled trial、不扩大 side effects 面、不改写 151/155/158/159 冻结语义。

---

## 1) 本阶段新增产物

- **160 runtime**：`capabilities/governance/runtime/navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_preparation_first_controlled_short_window_real_trial_execute_v0.py`
- **160 verifier**：`tools/verify_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_preparation_first_controlled_short_window_real_trial_execute_v0.py`

---

## 2) 160 如何映射 159 execute definition（逐条对齐）

### 2.1 非默认路径 + 显式 execute intent

- 160 runtime 强制 `explicit_short_window_real_trial_execute_intent_v0` 为 dict，否则 `aborted`（`execute_without_explicit_intent`）。

### 2.2 显式人工确认/等价批准

- 160 runtime 强制 `explicit_short_window_real_trial_execute_approval_v0` 为 dict，否则 `aborted`（`execute_without_explicit_approval`）。

### 2.3 readiness=go（158）

- 160 runtime 强制 `readiness_go_no_go_pack_v0` 为 dict 且 `overall_evaluation == "go"`，否则 `aborted`（`execute_without_readiness_go`）。

### 2.4 guardrail loaded（155）与窗口/次数可审计

- 160 runtime 强制 `guardrail_definition_v0` 存在（最小信号）；
- 强制 `execute_window_max_ms / observed_elapsed_ms` 可转换为 int 且上限成立，否则 `aborted`（`audit_trace_missing_or_broken` / `execute_window_timeout`）；
- 强制 `execute_attempts_max / execute_attempts_observed` 可审计且不超限，否则 `aborted`（`audit_trace_missing_or_broken` / `execute_attempts_exceeded`）。

### 2.5 唯一 `start_event_observed` 判据不变（151）

- 160 runtime **不自造** started；而是复用 152 enablement 运行时，只有其产生 `start_event_observed` 且 `real_enablement_started` 才会将其映射为 `controlled_short_window_real_trial_execute_started=true`。
- 若出现 `started=true` 但 `start_event_observed=false`，立即 `aborted`（`no_start_event_but_started`）。

### 2.6 side effects 白名单面不扩（仅三类）

- 160 runtime 对 intent 的 `requested_surfaces` 做 allowlist 校验，只允许：
  - `execution_state_real_write`
  - `result_object_real_write`
  - `exception_or_failure_real_write`
- 任一未授权 surface => `aborted`（`unauthorized_side_effect_surface`）。
- 实际真实写入仍由 152 的 writer 注入完成，因此副作用面不会扩出既有三类。

### 2.7 stop/abort + rollback/recovery/final close（159）

- 160 runtime 统一 `_abort()` 收口：`rollback_completed=true`、`recovery_completed=true`、`closed=true`、`side_effects_released=false`。
- 对以下非法态强制 abort：
  - 未 started 却 release（`no_started_but_release`）
  - started 但缺 closure（`closure_missing`）
  - closure 后 se 未回落（`se_not_recovered`）

---

## 3) 160 新增 runtime 行为（相对 156）

- 引入 **readiness_go**（158）作为 execute 的硬前置条件（进入真实 execute 之前必须 readiness=go）。
- 引入 execute 维度的 **attempt constraints**（`execute_attempts_max/execute_attempts_observed`）。
- 引入 execute 维度的 **scope allowlist**（可选：`allowed_scopes_v0` + `requested_scope`）。

以上均为“执行边界宪法”在 runtime 入口层的具体化，不改变 151/155/159 的语义。

---

## 4) 仍未进入/仍禁止的事项（写死）

- 默认路径仍未开启
- 未进入 full controlled trial
- 未扩大真实 side effects 面
- 未提供自动连续触发通道
- 160 的成功不等于 full release，仅代表一次受控短窗真实执行在边界内闭合

---

## 5) 验证（verifier 覆盖）

160 verifier 覆盖 A–M 场景，重点断言：

- 无 intent / 无 approval / 无 readiness_go => 不得 started
- 无 started 不得 release；entry se=true 必须被拒绝
- window 超时 / surfaces 越权 / audit 破损 => 必须 abort 并 closed 且 se=false
- success / failure 均必须 final close 且 se=false
- default_path_probe：结构性依赖显式 intent，不存在隐式入口
- closure_break_probe：合成非法态必须被识别为 illegal（供后续审计层使用）

