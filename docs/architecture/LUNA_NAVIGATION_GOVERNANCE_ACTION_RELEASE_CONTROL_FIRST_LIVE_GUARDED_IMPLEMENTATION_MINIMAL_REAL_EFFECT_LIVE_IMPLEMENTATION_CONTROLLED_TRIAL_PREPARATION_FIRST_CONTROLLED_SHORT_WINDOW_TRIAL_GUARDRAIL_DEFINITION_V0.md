# Luna — Navigation Governance Action Release Control First Live Guarded Implementation Minimal Real-Effect Live Implementation Controlled Trial Preparation First Controlled Short-Window Trial Guardrail Definition v0（短窗试运行护栏宪法冻结）

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_LIVE_IMPLEMENTATION_CONTROLLED_TRIAL_PREPARATION_FIRST_CONTROLLED_SHORT_WINDOW_TRIAL_GUARDRAIL_DEFINITION_V0.md`  
**性质**：Phase-Next-155：只做 Guardrail Definition Freeze（trial 前护栏宪法）；不新增 trial runtime；不 default-on；不 full trial；不扩副作用面；不改 151/152/153/154 边界

---

## A. 背景与前置阶段结论引用（只读）

- **151**：started 边界冻结（唯一 `start_event_observed`）；release/closure 不变量冻结  
- **152**：first minimal real enablement runtime 已存在（显式入口；arming/start gate/window/closure）  
- **153**：shadowed validation/evaluation = go（started/release/closure 边界已验证）  
- **154**：进入下一阶段的治理决策包 = go（无 hard blocker；allowlist/denylist 已冻结）  
- 默认路径仍未开启；full controlled trial 仍未开始

---

## B. 本 guardrail 的适用范围（写死）

本 guardrail 仅适用于：

- “进入第一段 **controlled short-window real trial preparation** 之前与之期间”的护栏约束

本 guardrail 目标是把以下四种许可彻底剥离：

1) allowed to prepare  
2) allowed to arm  
3) allowed to start short-window trial  
4) allowed to widen scope  

---

## C. 明确排除项（哪些不属于本阶段；写死）

本阶段不做：

- 不新增 trial runtime / runner
- 不新增 default path
- 不把 154 的 go 写成“已经进入短窗 trial”
- 不放大真实副作用面
- 不延长当前短时 release window 的定义边界
- 不改写 151 唯一 start_event 判据
- 不改写 152 closure 机制
- 不改写 153 validation 口径
- 不改写 154 allowlist/denylist 结论
- 不把 definition 与 implementation 混写

---

## D. controlled short-window trial 的定义（写死）

**controlled short-window trial**：

- 仅在 **非默认路径**、**显式 intent**、**显式人工确认或等价批准** 下进入
- 仅用于 **短时、受控、可审计、可回滚、可收口** 的试运行窗口
- **不等于** full controlled trial
- **不等于** default-on
- **不等于** full release

---

## E. short-window 的时间/次数/范围边界定义（写死为“原则 + 上限必须存在”）

必须写死三类上限（具体数值可由后续阶段配置，但本定义要求“必须存在并可验证”）：

- **最大持续时间上限**：trial window 必须有最大时长，禁止无限持续  
- **最大尝试次数/最大并发上限**：必须限制尝试次数与并发，禁止无界扩大  
- **最大作用范围上限**：必须限制环境/版本/链路/流量面，禁止隐式扩围  

并写死：

- 未新增新一层治理定义前，不得扩大运行时长、运行频率、运行范围、副作用类别

---

## F. trial 允许的副作用白名单（写死）

trial 期间允许的真实副作用面 **只能**是已验证过的三类：

- `execution_state_real_write`
- `result_object_real_write`
- `exception_or_failure_real_write`（仅失败时）

并写死：

- 仍必须沿用 152 的短时 window 语义（started 后才允许进入；且必须回落）

---

## G. trial 禁止的副作用黑名单（写死）

绝对禁止：

- route / voice / memory / migration
- rollback / interrupt（作为真实治理动作扩面）
- map/path side-effect source
- 非标准对象吐散字段
- 任何新增真实副作用类别（未经新治理定义）
- default-on 触发通道

---

## H. start 前前置条件（写死）

进入 short-window trial 前必须满足（缺一不可）：

- 默认路径仍未开启（可验证）
- 154 go/no-go pack 结论为 go 或 conditional_go（且无 hard blocker）
- 151/152/153 的 started/release/closure 边界未被改写
- 显式 trial intent + 显式人工确认/等价批准在位
- readiness/admission/shadow/go-no-go/dry-run 等链路产物在位（沿用既有门控，不新增口径）

---

## I. trial 中持续满足条件（写死）

trial 期间必须持续满足：

- started 判据仍唯一：只能由 `start_event_observed` 触发 started
- 未 started 不得 release；release 仅在 started 后短时打开且必须回落
- 全程可观测、可审计、可复盘（trace/原因码/输出结构可定位到 started/release/closure）
- 任何异常必须可收口（禁止半开启状态）

---

## J. abort 触发条件（写死）

出现任一即 **立即 abort**：

- no_start_event_but_started
- no_started_but_release
- closure_missing（started 后未 closure）
- se_not_recovered（closure 后 se 未回落到 false 或等价安全闭合）
- unauthorized_side_effect_surface（触碰未授权副作用面）
- trial_window_timeout（超出最大窗口）
- trial_scope_expanded_without_definition（无新治理定义的扩围）
- audit_trace_missing_or_broken（审计链断裂/不可复盘）

---

## K. rollback / closure 强制要求（写死）

abort 之后必须：

- 立即停止继续尝试
- 强制 recover 到 `side_effects_released=false` 或等价安全闭合态
- 完成最小失败收口记录（不扩面、不引入新副作用类别）
- 最终 `closed=true`，不残留 started-but-unclosed

---

## L. 最小成功态（写死）

短窗 trial 的最小成功：

- 仅在白名单副作用面内运行
- started/release/closure 边界均未越界
- success path 与 failure path 均可稳定收口（通过审计证据可复盘）
- trial 结束后仍保持非默认、未扩围（试运行结束但未扩大）

---

## M. 最小失败态（写死）

短窗 trial 的最小失败：

- 本次试运行未满足继续放行条件
- 但已按 abort policy 完成收口闭环，并回到安全闭合态
- 不等于系统失败；不允许扩权补救

---

## N. 扩围禁止条款（写死）

未新增新一层治理定义前，禁止：

- 扩大窗口时长/次数/并发/范围
- 扩大副作用类别
- 将 short-window trial 演进为 full controlled trial
- 将非默认路径变成 default-on

---

## O. 与 default-on / full trial / full release 的边界（写死）

- short-window trial != full controlled trial  
- short-window trial != default-on  
- short-window trial != full release  

---

## P. 后续 implementation 必须遵守的 contract（写死）

后续任何 short-window trial implementation 必须：

- 不新增 runtime 放行能力之外的扩面
- 不改变 151/152 的 started/release/closure 判据与收口契约
- 不扩大副作用白名单
- 必须实现 abort triggers 的即时中止与收口
- 必须可审计、可复盘、可定位到边界类型（started/release/closure/window/scope/audit）

---

## Q. 验收标准（写死）

本 guardrail definition 通过验收，当且仅当：

- 明确写死 short-window 的窗口边界（必须存在上限）
- 明确写死白名单/黑名单
- 明确写死 start 前前置条件、trial 中持续条件
- 明确写死 abort triggers 与 recovery/closure 强制要求
- 明确写死扩围禁止条款
- 明确声明：本阶段不做 trial implementation、不新增运行时放行能力、不 default-on

