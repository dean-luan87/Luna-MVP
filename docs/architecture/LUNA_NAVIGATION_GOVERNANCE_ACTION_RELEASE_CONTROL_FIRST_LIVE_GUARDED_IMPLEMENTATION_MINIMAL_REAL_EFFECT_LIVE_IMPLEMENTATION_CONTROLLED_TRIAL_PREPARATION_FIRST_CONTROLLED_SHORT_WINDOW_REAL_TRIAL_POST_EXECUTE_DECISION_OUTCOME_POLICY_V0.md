# Phase-Next-163 — First Controlled Short-Window Real Trial Post-Execute Decision Outcome Policy v0

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_LIVE_IMPLEMENTATION_CONTROLLED_TRIAL_PREPARATION_FIRST_CONTROLLED_SHORT_WINDOW_REAL_TRIAL_POST_EXECUTE_DECISION_OUTCOME_POLICY_V0.md`  
**用途**：把 post-execute decision 的 outcome 分类、前置条件、立即效果、升级要求、保持关闭要求写成硬规则，防止 execute 刚结束就被错误推入下一轮 real action。

---

## 1) 字段（写死）

每条 outcome policy 至少包含：

- **decision_outcome_id**
- **outcome_description**
- **allowed_or_forbidden**：`allowed | forbidden`
- **prerequisite_conditions**：前置条件（必须可审计）
- **immediate_effect**：立即效果（只允许治理性输出；不得触发真实执行/放权）
- **requires_new_governance_definition**：true/false
- **requires_human_confirmation**：true/false
- **keeps_system_closed**：true/false（allowed outcome 必须为 true）
- **allows_retry_now**：true/false（仅表达“允许重试”治理结论；不是自动重试）
- **escalation_required**：true/false

---

## 2) Allowed Outcomes（写死）

### remain_closed_safe

- **allowed_or_forbidden**：allowed
- **prerequisite_conditions**：
  - execute 已 final close（或 evidence 不足以证明已 final close）
  - 或 audit/证据不完整
- **immediate_effect**：保持 closed-safe；输出“保持关闭”的治理结论
- **requires_new_governance_definition**：false
- **requires_human_confirmation**：false
- **keeps_system_closed**：true
- **allows_retry_now**：false
- **escalation_required**：false

### retry_allowed_under_same_guardrails

- **allowed_or_forbidden**：allowed
- **prerequisite_conditions（必须全部满足）**：
  - execute 已合法 final close（closed=true 且 se=false）
  - audit trace intact 且最小证据集合齐全
  - 未发生任何越界（unauthorized/timeout/audit_failure/closure 风险）
  - 仍在同一 guardrail/同一副作用面白名单内（不扩）
  - 需要显式人工确认/等价批准（后续实现必须强制）
- **immediate_effect**：输出“允许在相同护栏下重试”的治理结论（不触发自动重试）
- **requires_new_governance_definition**：false
- **requires_human_confirmation**：true
- **keeps_system_closed**：true
- **allows_retry_now**：true
- **escalation_required**：false

### retry_not_allowed_until_new_definition

- **allowed_or_forbidden**：allowed
- **prerequisite_conditions**：
  - 发生越界或证据不足以排除越界风险
  - 或需要扩大窗口/次数/范围/频率/副作用类别
  - 或需要改变 151/155/159 冻结语义才能继续
- **immediate_effect**：输出“禁止在现有定义下重试”的治理结论
- **requires_new_governance_definition**：true（若要继续）
- **requires_human_confirmation**：false
- **keeps_system_closed**：true
- **allows_retry_now**：false
- **escalation_required**：true

### escalate_for_new_governance_definition

- **allowed_or_forbidden**：allowed
- **prerequisite_conditions**：
  - 继续前需要新增治理定义（例如扩大范围/窗口/副作用类别/或调整策略）
- **immediate_effect**：输出“必须升级进入新增治理定义链”的治理结论
- **requires_new_governance_definition**：true
- **requires_human_confirmation**：true
- **keeps_system_closed**：true
- **allows_retry_now**：false
- **escalation_required**：true

### stop_and_block_further_real_action

- **allowed_or_forbidden**：allowed
- **prerequisite_conditions**：
  - 发现结构性安全问题（例如 default-on 风险、门控可绕过、final close 不可信等）
- **immediate_effect**：输出“阻断进一步真实动作”的治理结论，并要求修复后重新走治理链
- **requires_new_governance_definition**：true（修复后）
- **requires_human_confirmation**：true
- **keeps_system_closed**：true
- **allows_retry_now**：false
- **escalation_required**：true

---

## 3) Forbidden Outcomes（写死）

### forbidden_implicit_reopen

- **allowed_or_forbidden**：forbidden
- **outcome_description**：任何形式的隐式重开 release window
- **keeps_system_closed**：false（因此禁止）

### forbidden_implicit_retry

- **allowed_or_forbidden**：forbidden
- **outcome_description**：decision 阶段隐式触发下一次真实 execute / 自动重试
- **keeps_system_closed**：false（因此禁止）

### forbidden_scope_widen_after_single_execute

- **allowed_or_forbidden**：forbidden
- **outcome_description**：仅因一次 execute 成功/完成而扩大时长/频率/范围/副作用类别
- **keeps_system_closed**：不适用（禁止）

### forbidden_implicit_full_trial_continuation

- **allowed_or_forbidden**：forbidden
- **outcome_description**：将 post-execute decision 作为进入 full controlled trial continuation 的隐式通道

### forbidden_implicit_default_on_transition

- **allowed_or_forbidden**：forbidden
- **outcome_description**：将 decision 作为开启默认路径/默认运行的隐式通道

---

## 4) 决策完成后的强制安全状态（写死）

对所有 allowed outcomes：

- `keeps_system_closed` 必须为 true
- decision 不得触发任何真实执行/写入/放权窗口开启
- 证据必须保全（供下一阶段治理裁决使用）

