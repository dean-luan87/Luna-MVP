# Luna — Navigation Governance Action Release Control First Live Guarded Implementation Minimal Real-Effect Live Implementation Controlled Trial Preparation First Minimal Real Enablement Implementation v0（151→152 映射说明）

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_LIVE_IMPLEMENTATION_CONTROLLED_TRIAL_PREPARATION_FIRST_MINIMAL_REAL_ENABLEMENT_IMPLEMENTATION_V0.md`  
**性质**：Phase-Next-152：说明 152 runtime 如何逐条遵守 151 definition（非默认路径；短时窗口；可回滚；可复盘；不扩面）

---

## 1) 本阶段真正新增的 runtime 行为（写清）

- 新增显式入口：`run_first_live_controlled_trial_preparation_first_minimal_real_enablement_v0(...)`
- 新增 arming 层：输出 `armed_not_started=True`，但不宣称 started
- 新增唯一开始事件：在 start gate 通过后写入 `start_event_observed=True`（作为唯一 started 判据）
- 新增短时 side-effects window（局部语义）：仅在 started 后进入 `se=True` 语义窗口，并强制 recover
- 新增 closure：成功/失败路径都必须 recover 到 `side_effects_released=false`，并 `closed=True`

---

## 2) 152 如何映射并遵守 151（逐条对齐）

### 2.1 dry-run executed ≠ started / preparation_go ≠ started

- 152 仅将 `preparation_go`、`dry_run_executed` 作为 readiness 证据；未出现 `start_event_observed` 前绝不置 `real_enablement_started=True`。

### 2.2 start_event_observed 是唯一开始判据

- 152 在 trace 中写入 `start_event_observed`，并同时置 `start_event_observed=True` 与 `real_enablement_started=True`，作为唯一开始事件（对应 151-F）。

### 2.3 未 started 不得释放 side effects

- 152 只有在 `real_enablement_started=True` 之后才进入 `se=True` 的短时窗口语义，并在 payload 的 state 中体现窗口开关与最终回落。

### 2.4 started 后必须 closure；closure 后必须安全闭合

- 成功路径：写入 state/result → recover false → `closed=True`
- 失败路径：先 recover false → best-effort 失败收口写入 → `rollback_completed=True` 且 `closed=True`

---

## 3) 最小真实副作用面（写死）

152 只允许三类写入（通过注入 writers 执行）：

- `execution_state_real_write`
- `result_object_real_write`
- `exception_or_failure_real_write`（仅失败时）

其余副作用面一律禁止（route/voice/memory/migration/rollback/interrupt/map/path/散写）。

---

## 4) 默认路径与真实 controlled trial（明确仍未进入）

- 152 不接默认路径，入口必须显式调用
- 152 不扩展为真实 controlled trial，仅实现“preparation first minimal real enablement”的最小执法器

