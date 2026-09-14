# Phase-Next-159 — First Controlled Short-Window Real Trial Execute Stop And Finalization Policy v0

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_LIVE_IMPLEMENTATION_CONTROLLED_TRIAL_PREPARATION_FIRST_CONTROLLED_SHORT_WINDOW_REAL_TRIAL_EXECUTE_STOP_AND_FINALIZATION_POLICY_V0.md`  
**用途**：把 execute 期间的 stop / abort / rollback / recovery / final close 写成硬规则，防止 started 后无法及时终止与收口。  
**说明**：本 policy 是 159 definition 的强制附录，后续 execute implementation（Phase-Next-160）必须遵守。

---

## 1) 字段（写死）

每条 stop/abort policy 至少包含：

- **stop_trigger_id**
- **trigger_description**
- **boundary_type**：
  - `entry_gate | started | release | stop_abort | recovery | closure | window_timeout | unauthorized_scope | audit_failure`
- **immediate_action**：`stop | abort`（二选一；v0 默认 abort 表示立即进入收口链）
- **rollback_required**：true/false
- **recovery_required**：true/false
- **final_safe_state_required**：true/false（v0 必须为 true）
- **escalation_required**：true/false（是否需要人工升级/决策层介入）

---

## 2) 总则（写死）

- **任何 stop/abort 都必须以 final close 收口**：
  - `side_effects_released=false`（或等价安全闭合态）
  - 不残留半开启状态
- **execute != readiness**：readiness=go 不等于 execute 已开始；缺任何 execute 进入条件即必须 abort。
- **start_event_observed 唯一性不可破坏**：一旦检测到 started 与 start_event 不一致，立即 abort。
- **越界优先级最高**：越界触发不允许被“继续尝试/重试”覆盖；必须 stop/abort 后再进入下一轮治理。

---

## 3) Stop / Abort Trigger 列表（v0，写死）

| stop_trigger_id | trigger_description | boundary_type | immediate_action | rollback_required | recovery_required | final_safe_state_required | escalation_required |
|---|---|---|---|---:|---:|---:|---:|
| execute_without_readiness_go | 未满足 158 readiness=go 却进入 execute | entry_gate | abort | false | true | true | true |
| execute_without_explicit_approval | 未有显式人工确认/等价批准却进入 execute | entry_gate | abort | false | true | true | true |
| execute_without_explicit_intent | 未声明 execute intent（混同 prepare/define） | entry_gate | abort | false | true | true | true |
| default_path_triggered | default-on/默认路径触发 execute | entry_gate | abort | false | true | true | true |
| no_start_event_but_started | 无 `start_event_observed` 却出现 started | started | abort | true | true | true | true |
| no_started_but_release | 未 started 却出现 release（se=true） | release | abort | true | true | true | true |
| unauthorized_side_effect_surface | 请求/触达未授权 side effect surface | unauthorized_scope | abort | true | true | true | true |
| execute_window_timeout | execute 超过最大持续时间上限 | window_timeout | abort | true | true | true | true |
| execute_attempts_exceeded | execute 超过最大尝试次数 | window_timeout | abort | true | true | true | true |
| execute_scope_expanded_without_definition | scope 扩围但无新增治理定义 | unauthorized_scope | abort | true | true | true | true |
| audit_trace_missing_or_broken | 审计 trace 缺失/不可审计 | audit_failure | abort | true | true | true | true |
| closure_missing | started 后无法完成 closure | closure | abort | true | true | true | true |
| se_not_recovered | closure 后 se 仍为 true（未回落） | closure | abort | true | true | true | true |

---

## 4) Finalization（收口硬要求，写死）

任何 stop/abort 后必须：

1. **停止进一步执行**（不得继续执行写入）
2. **rollback**（如适用）：撤销本次短窗内产生的最小写入影响（在允许范围内）
3. **recovery**（如适用）：恢复到可再次评估的安全状态
4. **final close**（必须）：
   - `side_effects_released=false`
   - `closed=true`（或等价闭合标志）
   - 不残留半开启状态
5. **最小复盘证据**（必须）：
   - stop_trigger_id
   - intent/approval/readiness 引用
   - window 参数与观测值
   - surfaces 请求与实际触达
   - closure 结果

---

## 5) “哪些条件下后续 implementation 必须直接 no_go”（写死）

后续 execute implementation（Phase-Next-160）只要出现任一即 **必须 no_go**（不得进入真实执行）：

- 任何形式的 default-on 风险
- 可绕过 execute intent 或人工确认/等价批准
- started 判据不唯一（非 `start_event_observed`）
- 未 started 却 release
- 无法在 timeout/unauthorized/audit_failure 时 abort
- abort 后无法完成 rollback/recovery/final close
- closure 后 `side_effects_released` 不能回落为 false
- 任何扩大 side effects 面的行为而无新增治理定义

---

## 6) 明确声明（写死）

- 默认路径仍未开启
- 本阶段未进入真实 short-window real trial execute
- 本阶段未新增运行时放行能力
- 本阶段只冻结 execute stop/finalization policy，不做 implementation

