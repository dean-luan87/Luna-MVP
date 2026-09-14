# Phase-Next-183 — Ultra-Governance Outcome Policy v0（Outcome 规则冻结）

**用途**：把 ultra-governance outcome 分类、前置条件、立即效果、升级/人工确认要求、以及“保持关闭 + 不自动进入下一 runtime”的硬约束写成规则，防止被错误推入真实动作或长期运行。  
**注意**：本文件是 policy（规则）；不是 runtime。  

---

## 字段（实现必须输出/可复盘）

每次 ultra-governance outcome 必须可复盘地提供以下字段（概念约束）：
- `governance_outcome_id`
- `outcome_description`
- `allowed_or_forbidden`
- `prerequisite_conditions`
- `immediate_effect`
- `requires_new_governance_definition`
- `requires_human_confirmation`
- `keeps_system_closed`
- `allows_next_runtime_now`
- `escalation_required`

---

## Allowed Outcomes（v0 白名单）

### 1) `remain_closed_safe`
- **allowed_or_forbidden**：allowed
- **prerequisite_conditions**：入口不显式 / 关键前置缺失 / 状态不一致 / 不明输入
- **immediate_effect**：保持闭合安全；拒绝进入任何真实动作链
- **requires_new_governance_definition**：false
- **requires_human_confirmation**：false
- **keeps_system_closed**：true
- **allows_next_runtime_now**：false
- **escalation_required**：false

### 2) `require_new_evidence_before_any_further_governance`
- **allowed_or_forbidden**：allowed
- **prerequisite_conditions**：无硬风险，但 evidence 不完整或 audit trace 不完整
- **immediate_effect**：要求补证据/补审计 trace；在补齐前不得推进下一治理准备
- **requires_new_governance_definition**：false
- **requires_human_confirmation**：false
- **keeps_system_closed**：true
- **allows_next_runtime_now**：false
- **escalation_required**：false

### 3) `escalate_for_new_governance_definition`
- **allowed_or_forbidden**：allowed
- **prerequisite_conditions**：继续推进必须扩窗/扩面/改变定义（widening_needed=true）或 definition gap 明确存在
- **immediate_effect**：要求进入“新治理定义链”而非继续运行；不得触发真实动作
- **requires_new_governance_definition**：true
- **requires_human_confirmation**：true（用于新定义冻结）
- **keeps_system_closed**：true
- **allows_next_runtime_now**：false
- **escalation_required**：true

### 4) `allow_next_governance_preparation_under_same_guardrails`
- **allowed_or_forbidden**：allowed
- **prerequisite_conditions**：
  - 显式入口
  - supra 合法完成
  - closed-safe 成立
  - default path disabled
  - evidence_complete & audit_trace_intact
  - 无边界违规/结构性风险
  - widening_needed=false
  - forbidden_signals 为空
- **immediate_effect**：允许推进更高层治理链的 **definition/pack** 准备；不授予任何运行时放行
- **requires_new_governance_definition**：false（下一阶段可定义更高层宪法，但不等于必须修改本层定义）
- **requires_human_confirmation**：true（进入下一治理准备时的人工确认点）
- **keeps_system_closed**：true
- **allows_next_runtime_now**：false（硬写死）
- **escalation_required**：false

### 5) `block_further_real_action_until_manual_override`
- **allowed_or_forbidden**：allowed
- **prerequisite_conditions**：出现 forbidden probes / 边界违规 / 结构性风险 / default path 风险
- **immediate_effect**：阻断任何进一步真实动作链，直到人工 override（治理层外部）明确处理
- **requires_new_governance_definition**：可能为 true（视阻断原因）
- **requires_human_confirmation**：true
- **keeps_system_closed**：true
- **allows_next_runtime_now**：false
- **escalation_required**：true（至少需要治理层升级或人工处理）

---

## Forbidden Outcomes / Forbidden Interpretations（v0 黑名单）

以下 outcome 或解释均为 forbidden（出现必须视为边界破坏，后续实现必须 no-go）：

- **forbidden_implicit_reopen**：任何形式的隐式 reopen
- **forbidden_implicit_retry_runtime**：任何形式的隐式 retry runtime
- **forbidden_scope_widen_after_governance**：未新增治理定义前扩大时长/范围/频率/副作用类别
- **forbidden_default_on_transition**：任何默认路径开启或默认进入治理/运行
- **forbidden_long_running_enablement**：把治理结论当成长周期运行许可
- **forbidden_full_trial_continuation**：把治理结论当作 full controlled trial continuation
- **forbidden_trigger_execute_from_governance**：治理阶段触发 execute/retry/reopen
- **forbidden_open_real_side_effects_window**：治理阶段打开新的真实副作用窗口
- **forbidden_reinterpret_182_go**：将 182 的 go 解释为“已批准继续真实运行”

---

## Post-Outcome Safety Requirements（统一硬约束）

无论输出何种 allowed outcome，都必须满足：
- `keeps_system_closed=true`
- `allows_next_runtime_now=false`
- `closed_safe_state_preserved=true`
- `default_path_enabled=false`
- 不得产生任何真实 side effects 放权或窗口扩大

