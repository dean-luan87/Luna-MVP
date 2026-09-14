# Phase-Next-158 — Controlled Short-Window Real Trial Readiness Blocker & Allowlist v0

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_LIVE_IMPLEMENTATION_CONTROLLED_TRIAL_PREPARATION_CONTROLLED_SHORT_WINDOW_REAL_TRIAL_READINESS_BLOCKER_AND_ALLOWLIST_V0.md`  
**用途**：明确下一阶段（进入第一次真实 controlled short-window real trial execute 的“准备/定义层”）允许与禁止的动作边界，并列出 hard blockers 与 soft follow-ups。

---

## 1) 结论摘要

- **Hard blockers（当前）**：**None identified**
- **Soft follow-ups（当前）**：存在（不阻断 readiness，但下一阶段必须附带）

---

## 2) 白名单（下一阶段允许做）

### 2.1 允许做（必须保持非默认路径）

- 在**非默认路径**下，推进“第一次真实 controlled short-window real trial”的 **execute definition / entry conditions / runbook**（文档级冻结）
- 继续沿用 **唯一 started 判据**：`start_event_observed`
- 继续沿用 **intent + approval gate**
- 继续沿用 **短时 release window**（closure 后 `side_effects_released=false`）
- 继续沿用 **已批准的最小真实副作用面**（不扩 surfaces、不新增写入类别）
- 继续沿用 **abort / recovery / closure 强制约束**（timeout/unauthorized/audit-break 必须 abort）

### 2.2 允许加强（只读与治理约束增强）

- 增加更强的观测、审计、人工确认、时间限制、次数限制（以 checklist/runbook 形式固化）
- 增加证据归档流程（保存 157 工具输出 JSON，保存入 pack 附件区）
- 增加“执行前人工确认点”（仍不等于 default-on）

---

## 3) 黑名单（下一阶段禁止做）

### 3.1 绝对禁止（违反即 NO_GO）

- **default-on / 默认路径**
- **full controlled trial**
- **扩大真实 side effects 面**（新增 surfaces、扩大写入类型、引入外部系统写入等）
- 修改 `start_event_observed` 的唯一 started 判据
- 绕过 intent / approval gate
- 去掉或弱化 abort / recovery / closure 的硬要求
- 将 157 go 或 158 go 解释为“已批准长期运行”
- 在未新增治理定义前扩大时长/范围/频率/副作用类别

### 3.2 禁止的语义偷换

- 把 “readiness 允许进入下一阶段定义” 写成 “已经开始真实 execute”
- 把 “短窗试运行” 扩成 “连续运行/长期放行”

---

## 4) Hard Blockers（硬阻断项定义）

以下任一出现，必须视为 hard blocker（即便其他证据为 go）：

- started 判据不唯一（无 `start_event_observed` 却 started）
- 未 started 却 release
- timeout / unauthorized / audit break 无法 abort
- abort 后不能 recovery
- closure 缺失或 closure 后 `side_effects_released` 不回落为 false
- intent / approval gate 可被绕过
- 默认路径存在误触发风险
- 下一阶段将实质扩大副作用面但缺少新增治理定义

