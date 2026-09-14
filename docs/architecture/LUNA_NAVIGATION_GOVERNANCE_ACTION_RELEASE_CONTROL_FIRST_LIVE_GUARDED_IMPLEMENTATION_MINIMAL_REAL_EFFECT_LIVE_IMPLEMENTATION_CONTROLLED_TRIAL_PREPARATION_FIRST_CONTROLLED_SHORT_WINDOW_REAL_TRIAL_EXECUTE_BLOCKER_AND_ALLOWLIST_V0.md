# Phase-Next-162 — First Controlled Short-Window Real Trial Execute Blocker & Allowlist v0

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_LIVE_IMPLEMENTATION_CONTROLLED_TRIAL_PREPARATION_FIRST_CONTROLLED_SHORT_WINDOW_REAL_TRIAL_EXECUTE_BLOCKER_AND_ALLOWLIST_V0.md`  
**用途**：明确进入下一阶段 post-execute / trial decision chain 的白名单/黑名单边界，并列出 hard blockers 与 soft follow-ups。

---

## 1) 结论摘要

- **Hard blockers（当前）**：**None identified**
- **Soft follow-ups（当前）**：存在（不阻断 go/no-go 结论，但下一阶段必须附带）

---

## 2) 白名单（下一阶段允许做）

### 2.1 允许做（必须保持非默认路径）

- 在**非默认路径**下推进 post-execute / trial decision chain 的 **definition 或 go/no-go pack**（文档级冻结）
- 继续沿用 **唯一 started 判据**：`start_event_observed`
- 继续沿用 **execute intent + approval + readiness_go gate**
- 继续沿用短时 release window（final close 后 se=false）
- 继续沿用 **既有三类最小真实副作用面**（不扩 surfaces、不新增写入类别）
- 继续沿用 **stop/abort/recovery/final close 强制约束**

### 2.2 允许加强（只读与治理约束增强）

- 加强观测/审计/trace 的可读性与归档（只读，不写外部系统）
- 固化 runbook/checklist：人工确认点、次数限制、时间限制、升级策略（非 runtime）

---

## 3) 黑名单（下一阶段禁止做）

### 3.1 绝对禁止（违反即 NO_GO）

- **default-on / 默认路径**
- **full controlled trial**
- **扩大真实 side effects 面**（新增 surfaces、扩大写入类型、引入外部系统写入等）
- 修改 `start_event_observed` 的唯一 started 判据
- 绕过 execute intent / approval / readiness_go gate
- 去掉或弱化 stop/abort/recovery/final close 的硬要求
- 将 161 或 162 的 go 解释为“已批准长期运行”
- 在未新增治理定义前扩大时长/范围/频率/副作用类别

---

## 4) Hard Blockers（硬阻断项定义）

以下任一出现，必须视为 hard blocker（即便其他证据为 go）：

- started 判据不唯一（无 `start_event_observed` 却 started）
- 未 started 却 release
- 无 readiness_go 却 execute
- timeout / unauthorized / audit break 无法 stop/abort
- stop/abort 后不能 recovery
- final close 缺失或 final close 后 se 不回落为 false
- execute gate 可被绕过
- 默认路径存在误触发风险
- 下一阶段将实质扩大副作用面但缺少新增治理定义

---

## 5) Soft Follow-Ups（不阻断，但必须附带）

- **证据归档**：保存 161 工具输出结构化 JSON（作为 162 pack 附件/归档条目）
- **reason code 口径**：统一 post-execute decision chain 的 reason_code 命名（不改语义）
- **runbook**：人工确认点、回滚升级条件、暂停条件（非 runtime）

