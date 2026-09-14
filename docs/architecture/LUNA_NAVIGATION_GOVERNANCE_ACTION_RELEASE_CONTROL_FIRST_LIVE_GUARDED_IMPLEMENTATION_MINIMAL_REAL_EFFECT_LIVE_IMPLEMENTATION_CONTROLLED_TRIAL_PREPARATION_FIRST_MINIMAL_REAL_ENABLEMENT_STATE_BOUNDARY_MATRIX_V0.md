# Luna — Navigation Governance Action Release Control First Live Guarded Implementation Minimal Real-Effect Live Implementation Controlled Trial Preparation First Minimal Real Enablement State Boundary Matrix v0（状态边界矩阵冻结）

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_LIVE_IMPLEMENTATION_CONTROLLED_TRIAL_PREPARATION_FIRST_MINIMAL_REAL_ENABLEMENT_STATE_BOUNDARY_MATRIX_V0.md`  
**性质**：Phase-Next-151：结构化矩阵化冻结“可开始 vs 已开始”的边界与迁移不变量（无代码）

---

## 1) 层级划分（建议分层；写死边界）

### Layer 1: readiness / pre-start（不等于 started）

- plan_frozen
- implementation_present
- dry_run_executed
- admission_ready
- shadow_evaluated
- go_no_go_ready

### Layer 2: arming（已 armed 但未 started）

- preparation_go_issued
- start_gate_satisfied
- armed_not_started

### Layer 3: first real enablement（开始窗口）

- start_event_observed
- side_effects_released_window_open
- real_enablement_started
- minimal_real_effect_observing

### Layer 4: outcome / closure（结果与收口）

- minimal_success_reached
- minimal_failure_reached
- aborted
- rollback_completed
- closed

---

## 2) 状态矩阵（写死判据与不变量）

| 状态 | 必要前置（缺一不可） | 唯一证据/判据 | side_effects_released 允许态 | 最小收口要求 |
|---|---|---|---|---|
| dry_run_executed | enablement runner 存在；dry-run signal 存在；顺序链走通 | dry-run status == executed | 禁止进入 true | N/A |
| preparation_go_issued | go/no-go gate == go；显式 go signal | preparation_go_no_go_status == go | 禁止进入 true | N/A |
| armed_not_started | preparation_go_issued；shadow_eval_go；admission_admitted；dry_run_executed；显式 start intent（signal） | start gate satisfied but start_event not observed | 禁止进入 true | N/A |
| start_event_observed | armed_not_started 且真实执行入口被显式调用并通过 real-input acceptance | **唯一开始事件**（definition F） | 允许进入“短时受控窗口语义”（必须可恢复） | 必须可回到 se=false |
| real_enablement_started | start_event_observed | started == true（不得用其它证据替代） | 允许（短时受控） | 必须有 closure path |
| minimal_success_reached | started 且最小成功写入完成 | state+result 写入完成且无越权；可复盘 | 必须恢复/确认 se=false | closed |
| minimal_failure_reached | started 但最小成功未成立 | 失败路径收口完成且可复盘 | 必须恢复/确认 se=false | closed |
| aborted | started 后触发熔断 | abort decision + 进入收口路径 | 必须恢复/确认 se=false | rollback_completed 或 closed |
| rollback_completed | aborted 后回退闭环完成 | rollback completed evidence | 必须为 false | closed |
| closed | 收口完成 | 可验证安全闭合态 | 必须为 false（或等价安全闭合） | 终态 |

---

## 3) 禁止迁移（写死）

- `dry_run_executed -> real_enablement_started`（禁止：缺少 start_event_observed）
- `preparation_go_issued -> real_enablement_started`（禁止：缺少 start_event_observed）
- `shadow_eval_go -> real_enablement_started`（禁止：影子评估不是开始事件）
- `armed_not_started -> committed`（禁止：未 started 不得 committed）

