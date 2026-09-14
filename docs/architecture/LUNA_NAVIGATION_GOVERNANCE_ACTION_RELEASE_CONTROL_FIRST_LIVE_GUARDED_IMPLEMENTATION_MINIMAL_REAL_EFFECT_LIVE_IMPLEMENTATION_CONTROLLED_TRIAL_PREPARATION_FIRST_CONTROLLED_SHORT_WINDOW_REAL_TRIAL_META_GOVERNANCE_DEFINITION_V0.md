# Phase-Next-175 — First Controlled Short-Window Real Trial Meta-Governance Definition v0

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_LIVE_IMPLEMENTATION_CONTROLLED_TRIAL_PREPARATION_FIRST_CONTROLLED_SHORT_WINDOW_REAL_TRIAL_META_GOVERNANCE_DEFINITION_V0.md`  
**阶段**：Phase-Next-175  
**性质**：**Meta-Governance Definition Freeze（宪法）**  
**非目标**：不是 meta-governance runtime、不是运行时放行能力、不是 retry/reopen、不是 default-on、不是 long-running approval、不是 full controlled trial continuation、不会扩大真实 side effects 面。  
**冻结继承**：不修改 151 / 155 / 158 / 159 / 162 / 163 / 166 / 167 / 170 / 171 / 174 的任何已冻结结论与边界语义。

---

## A. 背景与前置阶段结论引用（151 / 155 / 158 / 159 / 162 / 163 / 166 / 167 / 170 / 171 / 174）

本 definition 仅引用并继承既有冻结结论：

- **151**：started/release/closure 基础边界冻结（唯一 started 判据；闭合安全态基线）  
- **155**：short-window trial guardrail 冻结（allow/deny/abort/recovery/final close）  
- **158**：readiness pack = go（readiness ≠ execute ≠ 继续真实运行）  
- **159**：execute definition 冻结  
- **162**：execute go/no-go pack = go（合法性资格，不等于长期运行批准）  
- **163**：post-execute decision definition 冻结（allow/deny outcome；closed-safe；no-auto-retry）  
- **166**：post-execute decision go/no-go pack = go（进入后续治理链资格信号；不等于继续真实运行授权）  
- **167**：post-decision governance definition 冻结（entry/allowlist/denylist/closed-safe/no-next-runtime-now）  
- **170**：post-decision governance go/no-go pack = go（进入 higher-order 治理链资格成立；仍非真实继续运行批准）  
- **171**：higher-order governance definition 冻结（higher-order entry/allowlist/denylist/closed-safe/no-next-runtime-now）  
- **174**：higher-order governance go/no-go pack = go（进入 meta-governance 的资格成立；仍非真实继续运行批准）  

---

## B. 适用范围（写死）

本 definition 仅适用于：

- **higher-order governance** 已合法完成之后的下一层：**meta-governance**  
- 为后续 Phase-Next-176 的 meta-governance implementation 提供必须遵守的宪法/合同

---

## C. 明确排除项（写死）

本阶段不做：

- 不新增 meta-governance runtime
- 不开启默认路径
- 不打开新的 real side-effects window
- 不触发 retry/reopen/execute
- 不进入 full controlled trial
- 不把 174 的 go 写成“已批准继续真实运行”
- 不混写 definition 与 implementation

---

## D. “first controlled short-window real trial meta-governance”的定义（写死）

**meta-governance** 指：在 higher-order governance **已合法完成且系统保持 closed-safe state** 的前提下，系统仅基于既有证据与审计链做更高层治理判断（remain_closed / require_new_evidence / escalate / block / allow_next_governance_preparation），并且该判断不得成为隐式继续真实动作链或扩围的通道。

关键断言（写死）：

1. meta-governance != higher-order governance completed  
2. meta-governance != retry runtime  
3. meta-governance != reopen runtime  
4. meta-governance != default-on  
5. meta-governance != full controlled trial continuation  
6. meta-governance 只能在 higher-order governance 已合法完成且 closed-safe state 成立后进入  
7. 不得重新定义 started 判据（继承 151）  
8. 不得直接打开新的 real side-effects window  
9. 只能基于既有证据做治理判断，不得借治理名义扩大运行  

---

## E. meta-governance 的唯一进入条件（写死）

进入 meta-governance 的唯一入口必须同时满足：

1. **higher-order governance 已合法完成**（governance_completed=true 且治理流程可复盘）  
2. **system remains closed-safe**（closed-safe 成立；无 release window；无 auto retry/reopen）  
3. **evidence available**（最小证据集合齐全；见 J）  
4. **audit trace intact**（审计可复盘；缺失不得输出“允许推进”类结论）  
5. **default path still disabled**（默认路径仍未开启）  
6. **higher-order governance go/no-go pack（174）为 go/conditional_go**（资格信号；不等于继续真实运行授权）  

任一缺失 => 只能输出保守 outcome（remain_closed_safe / require_new_evidence... / block...），不得输出“允许下一轮治理准备”。

---

## F. governance 前前置条件（写死）

meta-governance 前必须具备：

- higher-order outcome classification（属于 allowlist）  
- higher-order 的 forbidden blocking 证据（无隐式 reopen/retry/widen/full-trial/default-on/long-running）  
- closed-safe state 证据（keeps system closed）  
- 是否需要新增治理定义的证据（widening_needed / structural issues / manual override needed）  

---

## G. 允许的 meta-governance outcome 白名单（写死）

meta-governance outcome 只能落在受限集合内：

- **remain_closed_safe**
- **require_new_evidence_before_any_further_governance**
- **escalate_for_new_governance_definition**
- **allow_next_governance_preparation_under_same_guardrails**
- **block_further_real_action_until_manual_override**

---

## H. 禁止的 meta-governance outcome 黑名单（写死）

绝对禁止：

- implicit reopen
- implicit retry runtime
- implicit widening
- implicit full-trial continuation
- implicit default-on transition
- implicit long-running approval
- meta-governance 阶段直接打开新的 real side-effects window
- meta-governance 阶段直接触发下一次 real execute

---

## I. remain_closed / require_new_evidence / escalate / next-governance-preparation / block 的边界（写死）

### remain_closed_safe

当以下任一成立时必须 remain_closed_safe：

- evidence/audit 不完整
- closed-safe state 不可信
- higher-order outcome 本身要求 remain_closed 且无升级输入

### require_new_evidence_before_any_further_governance

当证据不足以支持任何推进/升级结论时，必须要求补充证据并保持 closed-safe。

### escalate_for_new_governance_definition

当继续前需要改变 guardrail/范围/窗口/频率/副作用类别/策略（即任何“扩围/扩窗/扩频/扩面”）时，必须 escalate（进入新增治理定义链），禁止直接推进真实动作或隐式扩围。

### block_further_real_action_until_manual_override

当发现结构性安全问题、default-on 风险或 forbidden probe 时，必须 block，且不得进入任何真实动作链，直到人工 override/修复并重新走治理。

### allow_next_governance_preparation_under_same_guardrails

仅当以下全部成立时才允许：

- higher-order governance 已合法完成 + closed-safe state 可信  
- evidence 完整且无越界迹象  
- 不需要新增治理定义（same guardrails）  
- 明确仍然 **不等于** 自动进入任何 runtime（仅允许推进下一轮治理准备/definition/pack）  

---

## J. meta-governance 输入要素与最小证据要求（写死）

最小证据集合（缺失则不得输出 allow_next_governance_preparation_under_same_guardrails）：

- higher-order governance_completed 证据（可复盘）  
- closed-safe state 证据（keeps system closed）  
- higher-order outcome 属于 allowlist 的证据  
- forbidden blocking 证据（无隐式 reopen/retry/widen/full-trial/default-on/long-running）  
- widening_needed / structural issues / manual override 证据  
- audit trace 可复盘  
- 默认路径仍禁用的证据  

---

## K. governance 完成后的强制安全状态要求（写死）

无论 outcome：

- 系统必须保持 closed-safe state（本 definition 不授予打开 release window 的能力）
- 不允许 hidden release window / hidden auto retry / hidden reopen / hidden runtime continuation
- 必须保全证据供下一阶段治理裁决使用

---

## L. 最小成功态（写死）

最小成功态必须同时满足：

- outcome 属于 allowlist  
- 证据满足最小集合  
- governance 完成后保持 closed-safe state  
- 不引入扩大运行范围/默认路径/自动触发通道  

成功不等于 full release，只代表本次更高层治理判断成立。

---

## M. 最小失败态（写死）

最小失败态必须同时满足：

- 证据不足或审计破损无法支持推进结论  
- outcome 必须落在 remain_closed_safe / require_new_evidence... / block...  
- 系统保持 closed-safe state  

失败不等于系统失败，只代表当前证据不足以支持进一步治理推进。

---

## N. “meta-governance 完成但不扩围”的定义（写死）

满足以下全部即视为“完成但未扩围”：

- 默认路径仍禁用  
- 未隐式开启 release window  
- 未隐式触发 retry/execute/reopen  
- outcome 不引入扩大时长/范围/频率/副作用类别  
- 证据保全且可复盘  

---

## O. 与 lower-order governance / retry / reopen / default-on / full controlled trial / full release 的边界（写死）

- lower-order（higher-order governance）= 依据 171/172/173/174 的受限治理层  
- meta-governance（本 definition）= 更高层治理判断（仍不执行真实动作）  
- retry/reopen/default-on/long-running/full trial continuation/full release = 禁止或不在范围内  

---

## P. 后续 implementation 必须遵守的 contract（写死）

后续任何 meta-governance implementation（Phase-Next-176）：

- 必须满足本 definition 的唯一进入条件  
- 只能输出 allowlist outcomes，禁止 denylist outcomes  
- 不得打开新的 real side-effects window  
- 不得隐式触发 retry/reopen/execute  
- governance 完成后必须保持 closed-safe state 并保全证据  
- 默认路径仍必须禁用  

---

## Q. 验收标准（本阶段）

本阶段验收仅为 definition 冻结：

- [ ] 写死唯一进入条件与 required evidence  
- [ ] 写死 allowlist/denylist outcomes  
- [ ] 写死 remain_closed / require_new_evidence / escalate / block / next-preparation 边界  
- [ ] 写死 closed-safe 强制要求 + no-next-runtime-now 语义边界  
- [ ] README 索引已更新  

并且必须明确声明：

- 默认路径仍未开启  
- 本阶段未进入 full controlled trial  
- 本阶段未新增运行时放行能力  
- 本阶段只冻结 meta-governance definition，不做 implementation  

