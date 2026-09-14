# Phase-Next-159 — First Controlled Short-Window Real Trial Execute Boundary Matrix v0

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_LIVE_IMPLEMENTATION_CONTROLLED_TRIAL_PREPARATION_FIRST_CONTROLLED_SHORT_WINDOW_REAL_TRIAL_EXECUTE_BOUNDARY_MATRIX_V0.md`  
**用途**：将 execute 的进入条件、窗口边界、stop/abort 条件、final close 条件矩阵化，防止后续 execute implementation 漏掉硬边界。

---

## 矩阵字段（写死）

- **matrix_id**
- **layer**：`entry_to_execute | window_constraints | runtime_constraints | stop_abort | finalization`
- **boundary_type**：`entry_gate | started | release | window_timeout | unauthorized_scope | audit_failure | stop_abort | recovery | closure`
- **requirement**：要求描述（可被测试/审计）
- **must_hold**：必须成立（true/false）
- **violation_outcome**：违规必须产生的结果（stop/abort/illegal/no_go）
- **evidence_source**：关联证据来源（151/155/156/157/158/159）

---

## Boundary Matrix（v0）

| matrix_id | layer | boundary_type | requirement | must_hold | violation_outcome | evidence_source |
|---|---|---|---|---:|---|---|
| M-ENTRY-01 | entry_to_execute | entry_gate | 非默认路径显式入口（不得隐式触发） | true | stop/abort + no_go | 159 |
| M-ENTRY-02 | entry_to_execute | entry_gate | 显式 execute intent（与 prepare/define 区分） | true | stop/abort + no_go | 159 |
| M-ENTRY-03 | entry_to_execute | entry_gate | 显式人工确认/等价批准（不可绕过） | true | stop/abort + no_go | 159 / 156 / 157(A/B/J) |
| M-ENTRY-04 | entry_to_execute | entry_gate | readiness pack = GO（158）为进入 execute 的必要条件之一 | true | stop/abort + no_go | 158 |
| M-ENTRY-05 | entry_to_execute | entry_gate | guardrail loaded（155）且语义不被弱化 | true | stop/abort + no_go | 155 |
| M-START-01 | runtime_constraints | started | `start_event_observed` 为唯一 started 判据（不得新增） | true | stop/abort + no_go | 151 / 157(C/D/E) / 159 |
| M-RELEASE-01 | runtime_constraints | release | 未 started 不得 release（no_started_but_release） | true | stop/abort + no_go | 151 / 156 / 157(H probe) / 159 |
| M-RELEASE-02 | finalization | closure | closure 后 `side_effects_released=false`（se_not_recovered） | true | stop/abort + no_go | 151 / 156 / 157 / 159 |
| M-WIN-01 | window_constraints | window_timeout | execute 必须有最大持续时间上限，超时即 stop/abort | true | stop/abort | 155 / 156 / 157(F) / 159 |
| M-WIN-02 | window_constraints | window_timeout | execute 必须有最大尝试次数上限，超限即 stop/abort | true | stop/abort | 155 / 159 |
| M-WIN-03 | window_constraints | unauthorized_scope | execute 必须有最大范围原则，任何扩围即 stop/abort | true | stop/abort + no_go | 155 / 159 |
| M-WIN-04 | window_constraints | unauthorized_scope | side effects surfaces 不得新增，未授权即 stop/abort | true | stop/abort + no_go | 155 / 156 / 157(G) / 158 / 159 |
| M-AUDIT-01 | runtime_constraints | audit_failure | audit trace 必须存在且可审计，缺失即 stop/abort | true | stop/abort | 155 / 156 / 157(I) / 159 |
| M-STOP-01 | stop_abort | stop_abort | no_start_event_but_started 必须立即 stop/abort | true | stop/abort + no_go | 159 |
| M-STOP-02 | stop_abort | stop_abort | closure_missing 必须立即 stop/abort | true | stop/abort + no_go | 159 / 157(K probe) |
| M-FIN-01 | finalization | recovery | stop/abort 后必须 rollback/recovery（如适用）并 final close | true | no_go | 155 / 156 / 157(F/G/I) / 159 |
| M-FIN-02 | finalization | closure | success/failure/abort 均必须 closed=true | true | no_go | 151 / 156 / 157(D/E/F/G/I) / 159 |

