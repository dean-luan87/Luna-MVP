# Phase-Next-183 — Ultra-Governance Definition v0（宪法冻结；仅定义不实现）

**阶段名**：First Controlled Short-Window Real Trial Ultra-Governance Definition v0  
**性质**：Definition Freeze（宪法）；不是 runtime；不新增运行时放行能力  
**硬约束**：不启用默认路径；不进入 full controlled trial；不扩大真实 side effects 面；不修改既有冻结阶段结论与边界（151/155/158/159/162/163/166/167/170/171/174/175/178/179/182）  

---

## A. 背景与前置阶段结论引用（只引用，不改写）

当前闭合状态已成立（冻结事实）：
- 151：started/release/closure 基础边界冻结
- 155：short-window trial guardrail 冻结
- 158：real trial readiness pack = go
- 159：real trial execute definition 冻结
- 162：execute go/no-go pack = go
- 163：post-execute decision definition 冻结
- 166：post-execute decision go/no-go pack = go
- 167：post-decision governance definition 冻结
- 170：post-decision governance go/no-go pack = go
- 171：higher-order governance definition 冻结
- 174：higher-order governance go/no-go pack = go
- 175：meta-governance definition 冻结
- 178：meta-governance go/no-go pack = go
- 179：supra-governance definition 冻结
- 182：supra-governance go/no-go pack = go

并且：
- 默认路径仍未开启
- full controlled trial 仍未开始
- 当前无 hard blocker

---

## B. 本 definition 的适用范围（Scope）

本 definition 仅定义：
- “supra-governance 之后”的更高一层治理链：**ultra-governance** 的宪法边界（entry / prerequisites / outcomes / forbidden / post-safety）
- 何时允许进入“下一轮治理准备”（next-governance-preparation），以及其**不等价**于任何 runtime 自动推进

本 definition 明确不包含：
- ultra-governance runtime 实现
- retry/reopen/execute 的任何放行
- default-on / long-running / full controlled trial continuation 的任何许可
- 任何新的真实副作用窗口或 side_effects_released 放权机制

---

## C. 明确排除项（Non-Goals）

本阶段不做：
- 不进入 ultra-governance runtime
- 不新增运行时放行能力
- 不开启默认路径
- 不扩大真实 side effects 面
- 不修改 151/155/…/182 的任何冻结语义与结论
- 不把 definition 与 implementation 混写

---

## D. “first controlled short-window real trial ultra-governance” 的定义

**Ultra-Governance（v0）**：在 `supra-governance` 已合法完成且系统处于 **closed-safe** 的前提下，对“是否允许继续推进更高一层治理链（definition/pack）”做出的**只读、非默认入口、强约束**的治理判断层。

核心原则：
1. **ultra-governance != supra-governance completed**（是更高一层治理判断，不是前一层结束的别名）
2. **ultra-governance != retry runtime / reopen runtime / execute**
3. **ultra-governance != default-on / long-running approval / full controlled trial continuation**
4. ultra-governance outcome 只能落在受限集合中，且必须保持 closed-safe 与 no-next-runtime-now

---

## E. Ultra-Governance 的唯一进入条件（唯一入口）

Ultra-Governance 仅可在同时满足以下条件时进入：

1. **显式入口意图为真**（non-default entry）  
2. **supra-governance 已合法完成**（legality & completion 已被确认）  
3. **系统处于 closed-safe state**（进入前必须已闭合安全）  
4. **默认路径仍禁用**（default path disabled）  
5. **证据与审计 trace 可用**（至少达到 v0 最小证据要求；见 J）

任何缺失都必须视为非法进入尝试，并强制回落保守 outcome（见 I 与 Outcome Policy）。

---

## F. Governance 前前置条件（Prerequisites）

Ultra-Governance 前置条件必须满足：
- 不得重新定义 started 判据（151 冻结）
- 不得改变 guardrail allow/deny/abort policy（155 冻结）
- 不得对任何真实运行链条作出放行（不触发 execute/retry/reopen）
- 不得打开新的真实副作用窗口
- 不得启用默认路径

---

## G. 允许的 Ultra-Governance Outcome 白名单（Allowlist）

Ultra-Governance 允许输出的治理 outcome（v0）仅为以下五项（语义保持与前序治理链一致，不扩大含义）：
- `remain_closed_safe`
- `require_new_evidence_before_any_further_governance`
- `escalate_for_new_governance_definition`
- `allow_next_governance_preparation_under_same_guardrails`
- `block_further_real_action_until_manual_override`

强制不变量（所有 allowed outcomes 都必须满足）：
- `keeps_system_closed = true`
- `closed_safe_state_preserved = true`
- `allows_next_runtime_now = false`

---

## H. 禁止的 Ultra-Governance Outcome / 信号 黑名单（Denylist）

以下均为 forbidden（任何出现都必须阻断，并触发保守/阻断 outcome；不得继续推进真实运行链）：
- `implicit_reopen`
- `implicit_retry_runtime`
- `implicit_widening`
- `implicit_full_trial_continuation`
- `implicit_default_on_transition`
- `implicit_long_running_enablement`
- `open_release_window`
- `trigger_execute` / `trigger_retry` / `trigger_reopen`
- `enable_default_path` / `enable_long_running`

---

## I. remain_closed / require_new_evidence / escalate / next-prep / block 的硬边界（v0）

Ultra-Governance 在判断时必须遵循下列硬规则（不可被实现“弱化”为自动推进）：

1. **remain_closed_safe**：当入口不显式、或关键前置缺失、或出现 allowlist 外/不明 outcome 时必须选择  
2. **require_new_evidence_before_any_further_governance**：当无硬风险但证据不完整/审计 trace 不完整时必须选择  
3. **escalate_for_new_governance_definition**：当继续推进必须扩窗/扩面/改变定义（widening/definition gap）时必须选择  
4. **block_further_real_action_until_manual_override**：当出现边界违规、结构性风险、或任何 forbidden probe 时必须选择  
5. **allow_next_governance_preparation_under_same_guardrails**：仅当证据完备、无边界违规、无 widening 需求、且保持 closed-safe/no-next-runtime-now 时允许选择；并且该 outcome **不等价**于自动进入下一 runtime，只表示“允许准备更高层治理链的定义/pack”

---

## J. Ultra-Governance 输入要素与最小证据要求（Minimal Inputs / Evidence）

Ultra-Governance（v0）最小输入面必须包含（概念层要求；实现不得少于此）：
- `supra_governance_completed_seen`（或等价字段）
- `supra_governance_legality_seen`
- `closed_safe_state_seen`
- `evidence_complete_seen`
- `audit_trace_intact_seen`
- `default_path_enabled == false`
- `forbidden_signals`（若存在则必须阻断）

最小证据要求（v0）：
- 能复盘 supra-governance 的 outcome 分类与证据完整性
- 能证明未开启默认路径、未进入 full controlled trial、未扩大真实 side effects

---

## K. Governance 完成后的强制安全状态要求（Post-Governance Safety State）

ultra-governance 完成后必须强制保持：
- 系统仍处于 closed-safe
- 不存在隐藏的 release window
- 不存在隐藏的 auto retry/reopen
- 不存在隐藏的 runtime continuation
- 证据与审计 trace 被保留用于下一治理步骤（只读归档，不写入真实执行状态）

---

## L. 最小成功态（Minimal Success）

满足以下即为 v0 的最小成功态：
- 在显式入口 + supra 合法完成 + closed-safe + 证据完整 + 默认路径禁用下，输出 `allow_next_governance_preparation_under_same_guardrails`
- 且始终保持：closed-safe + no-next-runtime-now + allowlist only + forbidden blocked

---

## M. 最小失败态（Minimal Failure）

任一出现即为 v0 的最小失败态（后续实现必须判定 no-go）：
- 非法进入被放行（非显式入口却进入治理）
- allowlist 外 outcome 被输出
- forbidden probes 未被阻断
- governance 后 closed-safe 被破坏
- `allow_next_governance_preparation_under_same_guardrails` 被实现成自动进入下一 runtime
- 默认路径存在误触发风险

---

## N. “governance 完成但不扩围”的定义（No Expansion）

ultra-governance 完成的含义仅为：
- 给出更高层治理判断（definition/pack 的推进资格）
- 仍保持：不扩时长、不扩频率、不扩范围、不扩副作用类别  
在未新增更高层治理定义前，任何“因一次治理合法而扩大运行”的行为都属于越界。

---

## O. 与 lower-order governance / retry / reopen / default-on / full trial 的边界

硬边界写死（v0）：
- ultra-governance != retry runtime
- ultra-governance != reopen runtime
- ultra-governance != default-on
- ultra-governance != full controlled trial continuation
- ultra-governance 不得直接打开新的 real side-effects window
- ultra-governance 不得触发下一次 real execute

---

## P. 后续 implementation 必须遵守的 contract（仅契约，不实现）

未来 ultra-governance runtime（不在本阶段）必须满足：
- 非默认入口（显式意图为真）
- 仅在 supra 合法完成且 closed-safe 后可进入
- outcome 仅白名单五项
- forbidden probes 全阻断
- 运行后强制 closed-safe
- `allows_next_runtime_now=false` 恒成立（不得自动推进下一 runtime）
- 禁止默认路径误触发
- 不扩大真实 side effects 面

---

## Q. 验收标准（本阶段）

本阶段验收仅包含：
- 本 definition 文档完成并冻结（v0）
- 与 boundary matrix / outcome policy 文档一致（无语义冲突）
- README 索引可定位到三份 183 文档
- 明确声明：
  - 默认路径仍未开启
  - 本阶段未进入 full controlled trial
  - 本阶段未新增运行时放行能力
  - 本阶段只冻结 ultra-governance definition，不做 implementation

