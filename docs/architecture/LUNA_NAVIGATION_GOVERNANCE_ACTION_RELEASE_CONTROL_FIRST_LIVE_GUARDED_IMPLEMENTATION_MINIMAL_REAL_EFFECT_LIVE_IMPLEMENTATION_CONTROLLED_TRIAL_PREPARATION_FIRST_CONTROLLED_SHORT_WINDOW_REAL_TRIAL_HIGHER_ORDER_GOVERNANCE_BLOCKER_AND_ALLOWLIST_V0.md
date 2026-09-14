# Phase-Next-174 — Higher-Order Governance Blocker And Allowlist v0

**文件**：`docs/architecture/LUNA_NAVIGATION_GOVERNANCE_ACTION_RELEASE_CONTROL_FIRST_LIVE_GUARDED_IMPLEMENTATION_MINIMAL_REAL_EFFECT_LIVE_IMPLEMENTATION_CONTROLLED_TRIAL_PREPARATION_FIRST_CONTROLLED_SHORT_WINDOW_REAL_TRIAL_HIGHER_ORDER_GOVERNANCE_BLOCKER_AND_ALLOWLIST_V0.md`  
**阶段**：Phase-Next-174  
**用途**：冻结“进入下一阶段治理链/后续治理定义链”的白名单、黑名单、hard blockers 与 soft follow-ups。  

---

## 1) Hard Blockers（当前）

**结论：无已知 hard blocker**（以 173 overall_evaluation=go 为基线）。

必须强调：hard blocker 的“无”不等于“允许真实继续运行”，只表示“进入下一阶段治理链资格成立”。

---

## 2) Soft Follow-Ups（当前）

- **证据归档可读性**：增强 reason codes 与证据束组织（只读/文档/工具层）
- **runbook 强化**：增强人工确认说明（不改变 runtime 行为）

---

## 3) Allowlist（下一阶段允许做）

### 白名单（允许进入下一阶段的动作类型）

- **非默认路径**下推进更高层治理链的 **definition** 或 **go/no-go pack**（治理性、只读）
- 继续沿用并不得改写：
  - legal lower-order completion prerequisite
  - closed-safe prerequisite
  - allowed higher-order governance outcome allowlist
  - forbidden higher-order blocking
  - closed-safe-state preservation
  - no-next-runtime-now（`allows_next_runtime_now=false`）
- 允许加强审计/证据说明/runbook（只读增强）

### 进入下一阶段的最小前置条件（硬前置）

- 默认路径仍禁用
- 172 runtime 未被改写
- 173 validation 口径不被改写，且可复盘

---

## 4) Denylist（下一阶段禁止做）

### 黑名单（绝对禁止）

- default-on
- implicit reopen
- implicit retry runtime
- implicit widening
- implicit full controlled trial continuation
- implicit long-running enablement
- 修改 governance 白/黑名单语义
- governance 阶段直接打开新的 real side-effects window
- governance 阶段直接触发下一次 real execute
- 将 173 或 174 的 go 解释为“已批准继续真实运行”
- 未新增治理定义前扩大时长/范围/频率/副作用类别

---

## 5) 结果消费契约（给下一阶段）

下一阶段治理链必须把本 allowlist/denylist 当作硬约束：

- 任何触碰 denylist 的尝试 => 必须直接 no_go，并保持 closed-safe state
- 任何“允许推进”的表述必须显式写明：不等于 retry/reopen/default-on/long-running/full trial/full release

