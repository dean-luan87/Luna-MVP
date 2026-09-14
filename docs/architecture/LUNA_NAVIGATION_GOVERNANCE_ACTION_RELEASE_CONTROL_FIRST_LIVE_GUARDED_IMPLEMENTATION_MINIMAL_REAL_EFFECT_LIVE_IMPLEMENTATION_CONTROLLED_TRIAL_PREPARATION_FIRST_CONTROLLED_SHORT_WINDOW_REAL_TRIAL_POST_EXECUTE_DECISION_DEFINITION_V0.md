# Luna — Navigation Governance Action Release Control First Live Guarded Implementation Minimal Real-Effect Live Implementation Controlled Trial Preparation First Controlled Short-Window Real Trial Post-Execute Decision Definition v0

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_LIVE_IMPLEMENTATION_CONTROLLED_TRIAL_PREPARATION_FIRST_CONTROLLED_SHORT_WINDOW_REAL_TRIAL_POST_EXECUTE_DECISION_DEFINITION_V0.md`  
**阶段**：Phase-Next-163  
**性质**：**Post-Execute Decision Definition Freeze**（第一次真实 short-window execute 结束后的决策宪法）  
**非目标**：不是 post-execute decision runtime、不是运行时放行能力、不是 default-on、不是 full controlled trial continuation、不会扩大 side effects 面、不会修改 151/155/158/159/162 的冻结语义。

---

## A. 背景与前置阶段结论引用（151 / 155 / 158 / 159 / 162）

本 definition 只引用并继承既有冻结结论，不修改其语义：

- **151**：started/release/closure 基础边界冻结（`start_event_observed` 唯一 started 判据；closure 后 se=false）
- **155**：short-window trial guardrail 冻结（allow/deny、window、abort/recovery/final close 强制）
- **158**：real trial readiness pack = go（readiness ≠ execute）
- **159**：real trial execute definition 冻结（execute 唯一进入条件；stop/finalization policy）
- **162**：execute go/no-go pack = go（进入 post-execute decision chain 的资格与边界冻结；不等于批准长期运行）

并依赖已成立实现与审计事实（不在本阶段复写实现）：

- **160**：first real trial execute runtime 已存在  
- **161**：execute shadowed validation/evaluation = go

---

## B. 适用范围（写死）

本 definition 仅适用于：

- **第一次真实** controlled short-window real trial execute 结束之后的 **post-execute decision**（治理性决策）
- 仅用于后续 Phase-Next-164 的 post-execute decision implementation 必须遵守的宪法/合同

---

## C. 明确排除项（写死）

本阶段不做：

- 不新增 post-execute decision runtime
- 不开启默认路径
- 不扩大 side effects 面
- 不把 162 的 go 写成“已批准继续运行/重复运行/长期运行”
- 不触发任何新的 real side-effects release window
- 不进入 full controlled trial

---

## D. “first controlled short-window real trial post-execute decision”的定义（写死）

**post-execute decision** 指：在一次真实 execute **已合法 final close**（se=false 且 closed=true）之后，系统基于**既有证据**对下一步治理动作做受限决策，并且该决策 **不得** 以任何形式隐式开启下一轮真实执行或扩大运行范围。

关键断言（写死）：

1. post-execute decision != execute completed（“执行结束”不等于“可决策继续”）
2. post-execute decision != readiness（readiness=go 不等于决策可推进）
3. post-execute decision != default-on（不得默认触发）
4. post-execute decision != full controlled trial continuation（不得语义滑坡）
5. post-execute decision **只能**在 execute 已合法 final close 后进入
6. post-execute decision 不得重新定义 started 判据
7. post-execute decision 不得直接打开新的 real side-effects window
8. post-execute decision 只能基于已存在证据做治理判断，不得借 decision 名义扩大运行

---

## E. post-execute decision 的唯一进入条件（写死）

进入 post-execute decision 的唯一入口必须同时满足：

1. **execute 已合法 final close**：`closed=true` 且 `side_effects_released=false`（或等价安全闭合态）
2. **evidence available**：至少具备最小证据集合（见 J）
3. **audit trace intact**：审计/trace 可复盘；缺失即不允许做“继续/重试”类决策
4. **execute legality previously established**：引用 162 execute go/no-go pack（go/conditional_go）作为前置资格信号
5. **default path still disabled**：默认路径仍未开启（作为进入 decision 的硬前提）

任一缺失 => 只能输出 **remain_closed_safe** 或 **escalate_for_new_governance_definition**（不得 retry_now）。

---

## F. post-execute decision 前前置条件（写死）

decision 前必须具备：

- execute 结果分类（success/failure/abort + reason/trigger）
- closure 完整性证据（closed=true 且 se=false）
- 边界越界证据（若发生越界必须可定位）
- stop/abort/recovery/final close 的执行证据（如适用）
- 默认路径仍禁用的证据

---

## G. 允许的 decision outcome 白名单（写死）

post-execute decision 的 outcome 只能落在以下受限集合内：

- **remain_closed_safe**
- **retry_not_allowed_until_new_definition**
- **retry_allowed_under_same_guardrails**
- **escalate_for_new_governance_definition**
- **stop_and_block_further_real_action**

并且必须满足 outcome policy（见后续 policy 文档）。

---

## H. 禁止的 decision outcome 黑名单（写死）

绝对禁止：

- **implicit_reopen**（隐式重开 release window）
- **implicit_execute_retry**（隐式触发下一次真实 execute）
- **implicit_widening**（隐式扩大时长/范围/频率/副作用类别）
- **implicit_full_trial_continuation**（隐式进入 full controlled trial）
- **implicit_default_on_transition**（隐式过渡到默认路径）

---

## I. retry / escalate / stop / remain_closed 的边界（写死）

### remain_closed_safe

当以下任一成立时，必须 remain_closed_safe：

- 证据不完整/审计破损
- execute 未合法 final close（不满足 se=false/closed=true）
- 任一 hard violation（started/release/final close 语义被破坏）

### retry_allowed_under_same_guardrails

仅当以下全部成立时才允许（且只是“允许重试”的治理结论，不等于自动重试）：

- execute 已合法 final close
- 未发生任何越界（或越界被明确归类为“外部噪声且不影响边界”，并有证据支持）
- 仍处于相同 guardrail 定义与相同副作用面（不扩）
- 有明确人工确认/审批点（后续 implementation 需显式要求）

### retry_not_allowed_until_new_definition

当存在以下任一时，必须禁止在现有定义下重试：

- 越界发生（timeout/unauthorized/audit failure/closure 风险）
- 需要扩大窗口/次数/范围/频率/副作用类别才能重试
- 需要改变任何 151/155/159 冻结语义才能继续

### escalate_for_new_governance_definition

当需要改变定义/护栏/范围才能继续时，必须 escalate（进入新增治理定义链），禁止直接重试。

### stop_and_block_further_real_action

当出现安全风险或默认路径误触发风险等结构性问题时，必须 stop 并阻断进一步真实动作，直到修复并重新走治理链。

---

## J. post-execute decision 输入要素与最小证据要求（写死）

最小证据集合（缺失则不得给出 retry_allowed_under_same_guardrails）：

- execute status（success/failure/aborted）
- stop/abort trigger（如适用）
- `start_event_observed` 与 started 状态一致性证据
- final close 证据：`closed=true` 且最终 `side_effects_released=false`
- surfaces 证据：未触达未授权 surfaces（或越界已被记录并阻断）
- audit trace：可复盘（trace/order/reason）

---

## K. decision 完成后的强制安全状态要求（写死）

无论 outcome：

- 系统必须保持 **closed-safe state**，除非后续治理明确批准进入新一轮 execute（本 definition 不授予该能力）
- 不允许任何 hidden release window / hidden auto retry / hidden escalation into runtime
- 必须保全证据（供下一阶段治理裁决使用）

---

## L. 最小成功态（写死）

最小成功态必须同时满足：

- decision outcome 属于白名单集合
- decision 依赖的证据满足最小集合
- decision 完成后保持 closed-safe state
- 未引入扩大运行范围/默认路径/自动重试通道

成功 **不等于** full release，只代表一次 post-execute 治理判断成立。

---

## M. 最小失败态（写死）

最小失败态必须同时满足：

- 证据不足或审计破损导致无法给出允许继续/重试的结论
- outcome 必须落在 remain_closed_safe 或 escalate_for_new_governance_definition（或 stop_and_block）
- 系统保持 closed-safe state

失败 **不等于** 系统失败，只代表当前证据不足以支持进一步真实动作。

---

## N. “decision 完成但不扩围”的定义（写死）

满足以下全部即视为“完成但未扩围”：

- 默认路径仍禁用
- 未隐式开启任何 release window
- 未隐式触发 retry/execute
- outcome 不引入扩大时长/范围/频率/副作用类别
- 证据保全且可复盘

---

## O. 与 execute / readiness / default-on / full controlled trial / full release 的边界（写死）

- readiness（158）= 进入 execute 的准备资格  
- execute（159/160/161/162）= 真实短窗执行与其合法性审计/治理  
- post-execute decision（本 definition）= 执行结束后的治理判断（不执行真实动作）  
- default-on = 禁止  
- full controlled trial continuation / full release = 不在本 definition 范围内，禁止“语义滑坡”

---

## P. 后续 implementation 必须遵守的 contract（写死）

后续任何 post-execute decision implementation（Phase-Next-164）：

- 必须满足本 definition 的唯一进入条件（尤其是 execute 已合法 final close）
- 只能输出白名单 outcome；禁止黑名单 outcome
- 不得打开新的 real side-effects window
- 不得隐式触发 retry/execute
- decision 结束后必须保持 closed-safe state 并保全证据
- 默认路径仍必须禁用

---

## Q. 验收标准（本阶段）

本阶段验收仅为文档冻结：

- [ ] 明确区分：execute finished / execute legally closed / decision complete / allowed to retry/escalate/stop
- [ ] 写死唯一进入条件、allowed/forbidden outcomes、retry/escalate/stop/remain_closed 边界
- [ ] 写死 decision 不得隐式 reopen/retry/widen/full-trial/default-on
- [ ] 明确 decision 完成后的强制 closed-safe state
- [ ] README 索引已更新

并且必须明确声明：

- 默认路径仍未开启
- 本阶段未进入 full controlled trial
- 本阶段未新增运行时放行能力
- 本阶段只冻结 post-execute decision definition，不做 implementation

