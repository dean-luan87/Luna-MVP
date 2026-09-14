# Luna — Navigation Governance Action Release Control First Live Guarded Implementation Minimal Real-Effect Live Implementation Controlled Trial Preparation First Controlled Short-Window Real Trial Execute Definition v0

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_LIVE_IMPLEMENTATION_CONTROLLED_TRIAL_PREPARATION_FIRST_CONTROLLED_SHORT_WINDOW_REAL_TRIAL_EXECUTE_DEFINITION_V0.md`  
**阶段**：Phase-Next-159  
**性质**：**Execute Definition Freeze**（第一次真实 controlled short-window real trial 的执行边界宪法）  
**非目标**：不是 execute implementation、不是 execute runtime 放行能力、不是 default-on、不是 full controlled trial、不会扩大 side effects 面、不会执行真实 trial。

---

## A. 背景与前置阶段结论引用（151 / 155 / 158）

本 definition 只引用并继承既有冻结结论，不修改其语义：

- **151**：started / release / closure 边界冻结，`start_event_observed` 为唯一 started 判据  
- **155**：short-window trial guardrail 宪法冻结（allow/deny、window、abort/recovery/closure 强制）  
- **158**：controlled short-window real trial readiness pack = **GO**（readiness ≠ execute）

并依赖已成立实现与审计事实（不在本阶段复写实现）：

- **156**：first controlled short-window trial runtime 已存在  
- **157**：short-window trial shadowed validation/evaluation = **GO**

---

## B. 适用范围（写死）

本 definition 仅适用于：

- **第一次真实** controlled short-window real trial 的 **execute**（真实执行）边界定义
- 仅用于后续 Phase-Next-160 的 execute implementation 必须遵守的宪法/合同

---

## C. 明确排除项（写死）

本阶段不做：

- 不进入真实 short-window real trial execute
- 不新增/修改任何 runtime 放行能力
- 不开启默认路径
- 不扩大副作用面（side effects surfaces / 写入类型）
- 不修改 151/155/158 的冻结结论

---

## D. “first controlled short-window real trial execute”的定义（写死）

**execute** 指：在满足全部进入条件后，系统允许在**短窗口**内发生**已批准的最小真实副作用**（不扩面），并且对任一越界立即 stop/abort，最终必须回到 `side_effects_released=false`（或等价安全闭合态）的受控执行。

关键断言（写死）：

1. **execute != readiness**（readiness=go 只是必要条件之一，不是 execute 已开始）
2. **execute != default-on**（不得默认触发）
3. **execute != full controlled trial**（不意味着进入 full 试运行）
4. **execute started** 仍以 **151 的 `start_event_observed`** 为唯一判据（不得新增 started 判据）

---

## E. execute 的唯一进入条件（写死）

进入 “第一次真实 controlled short-window real trial execute” 的唯一入口必须同时满足：

1. **非默认路径显式入口**（必须由显式调用触发，不得隐式/自动触发）
2. **显式 execute intent**（与“prepare/define”意图区分；必须声明进入 execute）
3. **显式人工确认/等价批准**（不可被默认配置替代；不可绕过）
4. **readiness pack = GO（158）**（且 pack 未过期/未被 supersede）
5. **guardrail loaded（155）** 且执行器护栏启用（不改变护栏语义）
6. **仍满足 151 started/release/closure 前置约束**（尤其是 `start_event_observed` 唯一性与 closure 强制）

任一缺失即 **禁止进入 execute**（必须 stop/abort，且不得 release）。

---

## F. execute 前前置条件（写死）

execute 进入前必须具备：

- 明确的 **trial window 上限**（最大持续时间）与可审计的计时参数  
- 明确的 **最大尝试次数**（attempts）与 **最大范围/最大频率原则**  
- 明确的 **side effects surfaces 白名单**（不得超出 155/156/158 已批准范围）
- 明确的 **审计 trace/证据输出**（audit 不可缺失；缺失即 stop/abort）
- 明确的 **stop/abort policy** 与 **finalization**（见本阶段 stop policy 文档）

---

## G. execute 中允许动作白名单（写死）

仅允许（且必须保持非默认路径）：

- 执行第一次真实短窗 trial 的 execute implementation（后续阶段实现），但**只能**在既有最小允许副作用面内运作
- 继续沿用 151 的唯一 started 判据：`start_event_observed`
- 继续沿用 intent + approval gate（不得弱化）
- 继续沿用短时 release window + 强制 closure
- 允许加强只读观测、trace、审计证据组织、人工确认点、次数/时间限制（不得引入新副作用面）

---

## H. execute 中禁止动作黑名单（写死）

绝对禁止：

- default-on / 默认路径触发
- full controlled trial
- 扩大真实 side effects 面（新增 surfaces、扩大写入类型、外部系统写入等）
- 修改唯一 started 判据（不得新增 started 判据）
- 绕过 intent / approval gate
- 去掉 stop/abort/recovery/final close 硬要求
- 在未新增治理定义前扩大时长/次数/范围/频率/副作用类别
- 将 158=go 解释为“已批准长期运行”

---

## I. execute 的时间/次数/范围边界（写死）

execute 必须具备并强制执行：

- **最大持续时间上限**（short-window；不得无界持续）
- **最大尝试次数**（上限必须明确；超限即 stop/abort）
- **最大范围原则**（scope 只能在预定义的最小范围内；任何扩围即 stop/abort）
- **最大频率原则**（避免快速重复导致事实上的长时运行；越界即 stop/abort）
- **副作用类别上限**：不得超出既有白名单（不得新增类别/面）

---

## J. execute stop / abort 触发条件（写死）

任一出现必须立即 stop/abort（且不得继续执行）：

- no_start_event_but_started
- no_started_but_release
- closure_missing
- se_not_recovered（closure 后仍为 true）
- unauthorized_side_effect_surface
- execute_window_timeout
- execute_scope_expanded_without_definition
- audit_trace_missing_or_broken
- execute_without_explicit_approval
- execute_without_readiness_go

触发后必须进入 rollback/recovery/final close（见 stop policy 文档）。

---

## K. rollback / recovery / closure 强制要求（写死）

无论 success / failure / abort：

- 必须完成 rollback（如适用）与 recovery（如适用）
- 必须 final close 到安全闭合态：
  - `side_effects_released=false`（或等价安全闭合态）
  - 不残留半开启状态
- 必须产出最小复盘证据（audit/trace）

---

## L. 最小成功态（写死）

最小成功态必须同时满足：

- execute 在短窗内完成预期最小动作（不扩面）
- 未触发任何越界 stop/abort
- final close 完成：`side_effects_released=false`
- 证据齐全可复盘（intent/approval/start_event/window/audit/close）

成功 **不等于** full release，只代表第一次真实短窗试运行在护栏下成立。

---

## M. 最小失败态（写死）

最小失败态必须同时满足：

- 明确失败原因（reason/trigger 可审计）
- 已执行 stop/abort（如适用）
- rollback/recovery/final close 完成：`side_effects_released=false`
- 不残留半开启状态

失败 **不等于** 系统失败，只代表本次真实试运行未满足继续放行条件。

---

## N. “execute 完成但未扩大”的定义（写死）

满足以下全部即视为“完成但未扩围”：

- 非默认路径
- 仍以 `start_event_observed` 为唯一 started 判据
- side effects surfaces 未新增
- 时间/次数/范围/频率均未越界
- 成功/失败/abort 均完成 final close（se=false）
- 未引入通道使其自动滑向 full controlled trial 或 default-on

---

## O. 与 readiness / default-on / full controlled trial / full release 的边界（写死）

- readiness（158）= 具备进入 execute 的准备资格（必要条件之一）  
- execute（本 definition）= 真实短窗执行（更强约束、更强 stop/close）  
- default-on = 禁止  
- full controlled trial / full release = 不在本 definition 范围内，禁止“语义滑坡”

---

## P. 后续 implementation 必须遵守的 contract（写死）

后续任何 execute implementation（Phase-Next-160）：

- 必须满足本 definition 的唯一进入条件
- 必须沿用 151 的 started 判据（不得新增）
- 必须沿用 155 的 guardrail allow/deny/abort/recovery/closure 语义（不得弱化）
- 必须证明不会开启默认路径
- 必须证明不会扩大 side effects 面
- 必须在任何 stop/abort 后回到 se=false（或等价安全闭合态）

---

## Q. 验收标准（本阶段）

本阶段验收仅为文档冻结：

- [ ] 本文档明确区分：readiness_go / allowed_to_define_execute / real_execute_started  
- [ ] 写死唯一进入条件、白/黑名单、时间/次数/范围/频率边界、stop triggers、final close 要求  
- [ ] 明确 execute ≠ readiness ≠ default-on ≠ full trial  
- [ ] 明确后续 implementation 的 no-go 条件  
- [ ] README 索引已更新

并且必须明确声明：

- 默认路径仍未开启
- 本阶段未进入真实 short-window real trial execute
- 本阶段未新增运行时放行能力
- 本阶段只冻结 execute definition，不做 implementation

