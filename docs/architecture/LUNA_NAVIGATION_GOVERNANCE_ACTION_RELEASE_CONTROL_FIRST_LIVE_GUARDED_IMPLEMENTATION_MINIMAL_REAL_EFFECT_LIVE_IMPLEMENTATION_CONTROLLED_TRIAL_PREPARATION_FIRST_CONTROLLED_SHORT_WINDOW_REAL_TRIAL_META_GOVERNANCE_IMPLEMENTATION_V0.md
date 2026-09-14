# Phase-Next-176 — First Controlled Short-Window Real Trial Meta-Governance Implementation v0

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_LIVE_IMPLEMENTATION_CONTROLLED_TRIAL_PREPARATION_FIRST_CONTROLLED_SHORT_WINDOW_REAL_TRIAL_META_GOVERNANCE_IMPLEMENTATION_V0.md`  
**阶段**：Phase-Next-176  
**性质**：meta-governance **runtime 第一版实现**（只读、治理性、非默认入口）  
**受约束**：151 / 155 / 158 / 159 / 162 / 163 / 166 / 167 / 170 / 171 / 174 / 175（不得改写其冻结语义）

---

## 0) 本阶段做了什么（写死）

在 **175 meta-governance constitution** 不被破坏的前提下，实现第一版 meta-governance runtime，使系统能够在 **higher-order governance 已合法完成且 closed-safe 成立** 后，基于证据输出受限治理 outcome，并保证：

- governance 入口受控、非默认  
- 只能输出 175 白名单 outcome  
- 任一 forbidden outcome / 隐式 reopen / 隐式 runtime continuation 必须阻断  
- governance 后系统仍保持 closed-safe state  
- 不开启新的 real action / 不扩大 side effects 面  

---

## 1) 代码落点（唯一 runtime + verifier）

### 1.1 唯一 runtime（本阶段唯一）

- `capabilities/governance/runtime/navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_preparation_first_controlled_short_window_real_trial_meta_governance_v0.py`

对外提供：

- `run_meta_governance_v0(...) -> dict`

### 1.2 verifier（场景矩阵验证）

- `tools/verify_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_preparation_first_controlled_short_window_real_trial_meta_governance_v0.py`

覆盖 A–M 场景（no legal higher-order completion / closed-safe not preserved / evidence incomplete / clean case / violations / widening needed / forbidden probes / default path probe / require evidence / structural block）。

---

## 2) 176 如何逐条映射 175 constitution（硬约束落地）

### 2.1 Non-default explicit entry（175: E）

- runtime 要求 `explicit_meta_governance_entry_intent_v0=True`  
- 若缺失（explicit=False）=> `illegal_state_detected=true` 且 outcome 强制为 `remain_closed_safe`

### 2.2 只有 higher-order governance 已 legal complete 且 closed-safe 后才能进入（175: E/F/J）

runtime 的 entry gate 同时要求：

- `higher_order_governance_completed_seen=true`
- `higher_order_governance_legality_seen=true`
- `closed_safe_state_seen=true`
- `higher_order_governance_go_no_go_pack_v0 in {go, conditional_go}`
- `default_path_enabled=false`

任一不满足 => governance 不得推进，只能落为安全 outcome（remain_closed_safe / require_new_evidence / block）。

### 2.3 只允许白名单 meta-governance outcome（175: G）

runtime 只会选择以下 outcome：

- remain_closed_safe
- require_new_evidence_before_any_further_governance
- escalate_for_new_governance_definition
- allow_next_governance_preparation_under_same_guardrails
- block_further_real_action_until_manual_override

并对异常路径兜底：若 outcome 不在 allowlist，强制回落到 `remain_closed_safe` 并标记非法。

### 2.4 forbidden outcome 被真正阻断（175: H）

runtime 读取 `forbidden_signals/forbidden_probes/forbidden_meta_governance_signals`，若包含（例如 `implicit_reopen` / `implicit_retry_runtime` / `implicit_widening` / `implicit_long_running_enablement` 等），则：

- `forbidden_meta_governance_outcome_blocked=true`
- `illegal_state_detected=true`
- outcome 强制 `block_further_real_action_until_manual_override`

### 2.5 governance 后仍保持 closed-safe state（175: K）

runtime 强制写死：

- `keeps_system_closed=true`
- `allows_next_runtime_now=false`
- `closed_safe_state_preserved=true`

并且 runtime 本身不做任何真实副作用操作（只读治理输出）。

---

## 3) Meta-Governance runtime 输出字段（满足 Phase-Next-176 要求）

runtime 输出包含至少这些语义字段：

- explicit_meta_governance_entry_seen
- higher_order_governance_completed_seen
- higher_order_governance_legality_seen
- closed_safe_state_seen
- evidence_complete_seen
- boundary_violation_seen
- allowed_meta_governance_outcome_selected
- forbidden_meta_governance_outcome_blocked
- human_confirmation_required
- requires_new_governance_definition
- allows_next_runtime_now
- closed_safe_state_preserved
- illegal_state_detected
- governance_completed

---

## 4) 仍未进入的范围（写死）

本实现明确不包含、也不隐式触发：

- retry runtime / reopen runtime
- widening / 扩窗 / 扩面
- default-on
- long-running enablement
- full controlled trial continuation
- 任何 real side-effects window 的开启
- 任何下一次 execute 的自动触发

---

## 5) 验收声明（按阶段约束逐条）

- 默认路径仍未开启（runtime 必须显式入口才可进入）  
- 本阶段未进入 full controlled trial  
- 本阶段未扩大真实 side effects 面（只读治理）  
- 本阶段只是 first meta-governance implementation，不代表自动继续运行（`allows_next_runtime_now=false` 写死）  

