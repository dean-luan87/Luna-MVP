# Luna — Navigation Governance Action Release Control First Live Guarded Implementation Minimal Real-Effect Live Implementation Controlled Trial Preparation First Controlled Short-Window Real Trial Post-Decision Governance Definition v0

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_LIVE_IMPLEMENTATION_CONTROLLED_TRIAL_PREPARATION_FIRST_CONTROLLED_SHORT_WINDOW_REAL_TRIAL_POST_DECISION_GOVERNANCE_DEFINITION_V0.md`  
**阶段**：Phase-Next-167  
**性质**：**Post-Decision Governance Definition Freeze**（post-decision 之后更高一层治理链宪法）  
**非目标**：不是 governance runtime、不是运行时放行能力、不是 retry/reopen、不是 default-on、不是 full controlled trial continuation、不会扩大 side effects 面、不会修改 151/155/158/159/162/163/166 的冻结语义。

---

## A. 背景与前置阶段结论引用（151 / 155 / 158 / 159 / 162 / 163 / 166）

本 definition 只引用并继承既有冻结结论，不修改其语义：

- **151**：started/release/closure 基础边界冻结（`start_event_observed` 唯一 started 判据；close 后 se=false）
- **155**：short-window trial guardrail 冻结（allow/deny、window、abort/recovery/final close 强制）
- **158**：real trial readiness pack = go（readiness ≠ execute）
- **159**：execute definition 冻结（execute 唯一进入条件；stop/finalization policy）
- **162**：execute go/no-go pack = go（execute 合法性资格包；不等于长期运行批准）
- **163**：post-execute decision definition 冻结（allowed/forbidden outcomes；closed-safe；no-auto-retry）
- **166**：post-execute decision go/no-go pack = go（进入 post-decision governance chain 的资格与边界冻结）

---

## B. 适用范围（写死）

本 definition 仅适用于：

- **post-execute decision 已合法完成**之后的更高层治理：**post-decision governance**
- 仅用于后续 Phase-Next-168 的 post-decision governance implementation 必须遵守的宪法/合同

---

## C. 明确排除项（写死）

本阶段不做：

- 不新增 post-decision governance runtime
- 不开启默认路径
- 不扩大 side effects 面
- 不把 166 的 go 写成“已批准继续真实运行”
- 不触发 retry/reopen/下一次 execute
- 不进入 full controlled trial

---

## D. “first controlled short-window real trial post-decision governance”的定义（写死）

**post-decision governance** 指：在一次 post-execute decision **已合法完成且系统保持 closed-safe state** 的前提下，系统基于既有证据做更高层治理判断（例如 remain_closed / escalate / block / allow_next_governance_preparation），并且该治理判断不得成为隐式继续真实动作链的通道。

关键断言（写死）：

1. post-decision governance != post-execute decision completed  
2. post-decision governance != retry runtime  
3. post-decision governance != reopen runtime  
4. post-decision governance != default-on  
5. post-decision governance != full controlled trial continuation  
6. post-decision governance 只能在 decision 已合法完成且 closed-safe state 成立后进入  
7. 不得重新定义 started 判据  
8. 不得直接打开新的 real side-effects window  
9. 只能基于既有证据做治理判断，不得借 governance 名义扩大运行  

---

## E. post-decision governance 的唯一进入条件（写死）

进入 post-decision governance 的唯一入口必须同时满足：

1. **post-execute decision 已合法完成**（decision_completed=true，且决策流程可复盘）
2. **system remains closed-safe**（closed-safe state 成立；无 release window；无 auto retry）
3. **evidence available**（最小证据集合齐全；见 J）
4. **audit trace intact**（审计可复盘；缺失则不得输出“允许推进”的结论）
5. **default path still disabled**（默认路径仍未开启）
6. **post-execute decision go/no-go pack（166）为 go/conditional_go**（资格信号；不等于继续真实运行授权）

任一缺失 => 只能输出更保守 outcome（remain_closed_safe / require_new_evidence_before_any_further_governance / block…），不得输出“允许下一轮治理准备”。

---

## F. governance 前前置条件（写死）

governance 前必须具备：

- decision outcome classification（属于 163 allowlist）
- decision 的 forbidden blocking 证据（证明没有隐式 reopen/retry/widen/full-trial/default-on）
- closed-safe state 证据（keeps system closed）
- 是否需要新增治理定义的证据（例如 widening_needed 等）

---

## G. 允许的 governance outcome 白名单（写死）

governance outcome 只能落在受限集合内，例如：

- **remain_closed_safe**
- **escalate_for_new_governance_definition**
- **require_new_evidence_before_any_further_governance**
- **allow_next_governance_preparation_under_same_guardrails**
- **block_further_real_action_until_manual_override**

---

## H. 禁止的 governance outcome 黑名单（写死）

绝对禁止：

- implicit reopen
- implicit retry runtime
- implicit widening
- implicit full-trial continuation
- implicit default-on transition
- implicit long-running approval
- governance 阶段直接打开新的 real side-effects window
- governance 阶段直接触发下一次 real execute

---

## I. remain_closed / escalate / block / next-governance-preparation 的边界（写死）

### remain_closed_safe

当以下任一成立时必须 remain_closed_safe：

- evidence/audit 不完整
- closed-safe state 不可信
- decision outcome 本身要求 remain_closed（例如 retry_not_allowed… 且无升级路径输入）

### escalate_for_new_governance_definition

当需要改变 guardrail/范围/窗口/副作用类别/策略才能继续时，必须 escalate（进入新增治理定义链），禁止直接推进真实动作或隐式扩围。

### block_further_real_action_until_manual_override

当发现结构性安全问题或 default-on 风险时，必须 block，且不得进入任何真实动作链，直到人工 override/修复并重新走治理。

### allow_next_governance_preparation_under_same_guardrails

仅当以下全部成立时才允许：

- decision 已合法完成 + closed-safe state 可信
- evidence 完整且无越界迹象
- 不需要新增治理定义（same guardrails）
- 明确仍然 **不等于** 自动进入任何 runtime（仅允许推进“下一轮治理准备/定义/pack”）

### require_new_evidence_before_any_further_governance

当证据不足以支持任何推进/升级结论时，必须要求补充证据，保持 closed-safe。

---

## J. governance 输入要素与最小证据要求（写死）

最小证据集合（缺失则不得输出 allow_next_governance_preparation_under_same_guardrails）：

- decision_completed 证据
- allowed_outcome_selected 证据（属于 163 allowlist）
- forbidden_outcome_blocking 证据（无隐式 reopen/retry/widen/full-trial/default-on）
- closed-safe state 证据（keeps system closed）
- 是否需要新治理定义（widening_needed/structural issues）证据
- audit trace 可复盘

---

## K. governance 完成后的强制安全状态要求（写死）

无论 outcome：

- 系统必须保持 closed-safe state，除非后续治理明确批准进入新一轮真实动作（本 definition 不授予该能力）
- 不允许 hidden release window / hidden auto retry / hidden reopen / hidden execute trigger
- 必须保全证据供下一阶段治理裁决使用

---

## L. 最小成功态（写死）

最小成功态必须同时满足：

- outcome 属于白名单集合
- 证据满足最小集合
- governance 完成后保持 closed-safe state
- 不引入扩大运行范围/默认路径/自动触发通道

成功不等于 full release，只代表本次更高层治理判断成立。

---

## M. 最小失败态（写死）

最小失败态必须同时满足：

- 证据不足或审计破损无法支持任何推进结论
- outcome 必须落在 remain_closed_safe / require_new_evidence... / block...
- 系统保持 closed-safe state

失败不等于系统失败，只代表当前证据不足以支持进一步治理推进。

---

## N. “governance 完成但不扩围”的定义（写死）

满足以下全部即视为“完成但未扩围”：

- 默认路径仍禁用
- 未隐式开启 release window
- 未隐式触发 retry/execute
- outcome 不引入扩大时长/范围/频率/副作用类别
- 证据保全且可复盘

---

## O. 与 decision / retry / reopen / default-on / full controlled trial / full release 的边界（写死）

- post-execute decision（163/164/165/166）= 执行结束后的治理性判断（不执行真实动作）  
- post-decision governance（本 definition）= 更高层治理判断（仍不执行真实动作）  
- retry/reopen/default-on/full trial continuation = 禁止或不在范围内  

---

## P. 后续 implementation 必须遵守的 contract（写死）

后续任何 post-decision governance implementation（Phase-Next-168）：

- 必须满足本 definition 的唯一进入条件
- 只能输出白名单 outcomes，禁止黑名单 outcomes
- 不得打开新的 real side-effects window
- 不得隐式触发 retry/reopen/execute
- governance 完成后必须保持 closed-safe state 并保全证据
- 默认路径仍必须禁用

---

## Q. 验收标准（本阶段）

本阶段验收仅为文档冻结：

- [ ] 明确区分：decision complete / governance entry / allowed to open new governance chain / allowed to continue real action
- [ ] 写死唯一进入条件、allowed/forbidden outcomes、remain_closed/escalate/block/next-preparation 边界
- [ ] 写死 governance 不得隐式 reopen/retry/widen/full-trial/default-on/long-running approval
- [ ] 明确 governance 完成后的 closed-safe 强制要求
- [ ] README 索引已更新

并且必须明确声明：

- 默认路径仍未开启
- 本阶段未进入 full controlled trial
- 本阶段未新增运行时放行能力
- 本阶段只冻结 post-decision governance definition，不做 implementation

