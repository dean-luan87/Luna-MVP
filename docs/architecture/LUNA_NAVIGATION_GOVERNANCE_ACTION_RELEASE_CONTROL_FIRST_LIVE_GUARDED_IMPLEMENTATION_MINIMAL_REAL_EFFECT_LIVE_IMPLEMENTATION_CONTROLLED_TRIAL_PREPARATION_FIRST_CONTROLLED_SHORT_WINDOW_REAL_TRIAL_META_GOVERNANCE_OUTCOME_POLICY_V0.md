# Phase-Next-175 — Meta-Governance Outcome Policy v0

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_LIVE_IMPLEMENTATION_CONTROLLED_TRIAL_PREPARATION_FIRST_CONTROLLED_SHORT_WINDOW_REAL_TRIAL_META_GOVERNANCE_OUTCOME_POLICY_V0.md`  
**阶段**：Phase-Next-175  
**用途**：把 meta-governance outcome 分类、前置条件、立即效果、升级要求、保持关闭要求写成硬规则，防止 higher-order governance 结束后被错误推入真实动作或长期运行。

---

## 1) 字段（写死）

每条 outcome policy 至少包含：

- **governance_outcome_id**
- **outcome_description**
- **allowed_or_forbidden**：`allowed | forbidden`
- **prerequisite_conditions**：前置条件（必须可审计）
- **immediate_effect**：立即效果（只允许治理性输出；不得触发真实执行/放权）
- **requires_new_governance_definition**：true/false
- **requires_human_confirmation**：true/false
- **keeps_system_closed**：true/false（allowed outcome 必须为 true）
- **allows_next_runtime_now**：true/false（必须为 false）
- **escalation_required**：true/false

---

## 2) Allowed Outcomes（写死）

### remain_closed_safe

- **allowed_or_forbidden**：allowed  
- **prerequisite_conditions**：evidence/audit 不完整，或 closed-safe 不可信  
- **immediate_effect**：保持 closed-safe；输出“保持关闭”的治理结论  
- **requires_new_governance_definition**：false  
- **requires_human_confirmation**：false  
- **keeps_system_closed**：true  
- **allows_next_runtime_now**：false  
- **escalation_required**：false  

### require_new_evidence_before_any_further_governance

- **allowed_or_forbidden**：allowed  
- **prerequisite_conditions**：证据不足以支持任何推进/升级结论  
- **immediate_effect**：要求补证据；保持 closed-safe  
- **requires_new_governance_definition**：false  
- **requires_human_confirmation**：true  
- **keeps_system_closed**：true  
- **allows_next_runtime_now**：false  
- **escalation_required**：false  

### escalate_for_new_governance_definition

- **allowed_or_forbidden**：allowed  
- **prerequisite_conditions**：继续前需要新增治理定义（扩窗/扩面/改护栏/改策略/改副作用类别等）  
- **immediate_effect**：输出“必须升级进入新增治理定义链”的结论（不触发真实动作）  
- **requires_new_governance_definition**：true  
- **requires_human_confirmation**：true  
- **keeps_system_closed**：true  
- **allows_next_runtime_now**：false  
- **escalation_required**：true  

### allow_next_governance_preparation_under_same_guardrails

- **allowed_or_forbidden**：allowed  
- **prerequisite_conditions（必须全部满足）**：  
  - higher-order governance 已合法完成且 closed-safe state 成立  
  - 证据完整且无越界迹象  
  - 不需要新增治理定义（same guardrails）  
- **immediate_effect**：仅允许推进“下一轮治理准备/definition/pack”（仍非 runtime）  
- **requires_new_governance_definition**：false  
- **requires_human_confirmation**：true  
- **keeps_system_closed**：true  
- **allows_next_runtime_now**：false  
- **escalation_required**：false  

### block_further_real_action_until_manual_override

- **allowed_or_forbidden**：allowed  
- **prerequisite_conditions**：结构性安全问题、default-on 风险或 forbidden probe  
- **immediate_effect**：阻断进一步真实动作；要求人工 override/修复并重新走治理  
- **requires_new_governance_definition**：true（修复后）  
- **requires_human_confirmation**：true  
- **keeps_system_closed**：true  
- **allows_next_runtime_now**：false  
- **escalation_required**：true  

---

## 3) Forbidden Outcomes（写死）

### forbidden_implicit_reopen

- **allowed_or_forbidden**：forbidden  
- **outcome_description**：任何形式的隐式重开 release window  

### forbidden_implicit_retry_runtime

- **allowed_or_forbidden**：forbidden  
- **outcome_description**：隐式进入 retry runtime 或自动触发下一次真实执行  

### forbidden_scope_widen_after_governance

- **allowed_or_forbidden**：forbidden  
- **outcome_description**：仅因一次治理合法就扩大时长/频率/范围/副作用类别  

### forbidden_default_on_transition

- **allowed_or_forbidden**：forbidden  
- **outcome_description**：将治理阶段作为开启默认路径/默认运行的隐式通道  

### forbidden_long_running_enablement

- **allowed_or_forbidden**：forbidden  
- **outcome_description**：将治理阶段作为长期运行/持续放权的隐式批准通道  

---

## 4) 强制安全状态（写死）

对所有 allowed outcomes：

- `keeps_system_closed` 必须为 true  
- `allows_next_runtime_now` 必须为 false  
- 不得触发任何真实执行/写入/放权窗口开启  
- 证据必须保全（供下一阶段治理使用）  

