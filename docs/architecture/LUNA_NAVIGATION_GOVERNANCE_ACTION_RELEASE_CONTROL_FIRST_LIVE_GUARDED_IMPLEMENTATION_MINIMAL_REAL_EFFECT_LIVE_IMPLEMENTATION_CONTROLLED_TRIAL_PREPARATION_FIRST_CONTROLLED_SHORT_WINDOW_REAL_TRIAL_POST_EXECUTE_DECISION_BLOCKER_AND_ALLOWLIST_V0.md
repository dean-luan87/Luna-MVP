# Phase-Next-166 — First Controlled Short-Window Real Trial Post-Execute Decision Blocker & Allowlist v0

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_LIVE_IMPLEMENTATION_CONTROLLED_TRIAL_PREPARATION_FIRST_CONTROLLED_SHORT_WINDOW_REAL_TRIAL_POST_EXECUTE_DECISION_BLOCKER_AND_ALLOWLIST_V0.md`  
**用途**：明确进入下一阶段 post-decision governance chain 的白名单/黑名单边界，并列出 hard blockers 与 soft follow-ups。

---

## 1) 结论摘要

- **Hard blockers（当前）**：**None identified**
- **Soft follow-ups（当前）**：存在（不阻断 go/no-go 结论，但下一阶段必须附带）

---

## 2) 白名单（下一阶段允许做）

### 2.1 允许做（必须保持非默认路径）

- 在**非默认路径**下推进 post-decision governance chain 的 **definition 或 go/no-go pack**（文档级冻结）
- 继续沿用 **execute legal final close prerequisite**
- 继续沿用 **allowed outcome 白名单**
- 继续沿用 **forbidden outcome blocking**
- 继续沿用 **closed-safe-state preservation**
- 继续沿用 **no-auto-retry**（retry_allowed != auto retry）
- 加强证据归档、人工确认、runbook、审计说明（只读/治理层增强）

---

## 3) 黑名单（下一阶段禁止做）

### 3.1 绝对禁止（违反即 NO_GO）

- **default-on / 默认路径**
- **implicit reopen**
- **implicit execute retry / auto retry**
- **implicit widening**（扩大时长/范围/频率/副作用类别）
- **implicit full controlled trial continuation**
- 修改 decision 白名单/黑名单语义
- decision 阶段直接打开新的 real side-effects window
- 将 165 或 166 的 go 解释为“已批准继续真实运行/重复运行/长期运行”
- 在未新增治理定义前扩大时长/范围/频率/副作用类别

---

## 4) Hard Blockers（硬阻断项定义）

以下任一出现，必须视为 hard blocker：

- 无 legal final close 却进入 decision
- 输出 forbidden outcome（或存在任何隐式 reopen/retry/widen/full-trial/default-on 通道）
- decision 后破坏 closed-safe state
- retry_allowed 被实现成自动重试（allows_retry_now=true 或等价）
- 默认路径存在误触发风险
- 下一阶段将实质扩大副作用面但缺少新增治理定义

---

## 5) Soft Follow-Ups（不阻断，但必须附带）

- **证据归档**：保存 165 工具输出结构化 JSON（作为 166 pack 附件/归档条目）
- **reason code 口径**：统一 post-decision governance chain 的 reason_code 命名（不改语义）
- **runbook**：人工确认点、升级策略、证据审核清单（非 runtime）

