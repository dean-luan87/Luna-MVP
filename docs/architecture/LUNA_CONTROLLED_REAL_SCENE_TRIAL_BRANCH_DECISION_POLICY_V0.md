# Phase-RealSceneReview-001 — Controlled Real Scene Trial Branch Decision Policy v0（分流决策策略冻结）

**目的**：定义 RealSceneTrial-001 之后，何时进入 Fix Sprint、何时允许受控扩场景准备、何时暂停推进。  
**关键写死**：**fixture-only evidence 不允许作为扩场景依据**。  

---

## 0) 三类分流（写死）

### A. Fix Sprint（推荐默认）
用于修正“影响扩场景但不触发 hard blocker”的问题。

### B. Controlled Scope Expansion Preparation
仅在证据充分且无阻断时，才允许进入“扩受控场景的准备阶段”（仍不开放用户、不 full controlled trial）。

### C. Pause Real Scene Progression
出现硬阻断或证据不可信时暂停真实场景推进，回到链路修正。

---

## 1) 分流进入条件（写死）

### A. Fix Sprint（CONDITIONAL_GO）
进入条件：
- 无 hard blocker
- 但存在扩场景阻塞型 soft follow-up，例如：
  - evidence 仍为 fixture/replay，缺少 controlled live 的真实 run evidence
  - abort/fallback/degraded 未在真实 run 下被验证（只有文档冻结）
  - operator notes / risk events / archive manifest 不完整或不可复现
  - trace 可读性不足（虽“有”，但不便复盘）
  - 模型 candidate 价值弱（不影响安全边界，但影响推进价值）

**禁止**：Fix Sprint 期间不扩场景，不新增 run（除非后续阶段另行定义）。

### B. Controlled Scope Expansion Preparation（GO）
进入条件（必须同时满足）：
- evidence 完整且可信
- evidence 类型至少包含：**controlled live input 的真实 run evidence（非 fixture）**
- 无 hard blocker
- 无阻塞型 soft follow-up
- scope 未漂移（scope_drift=0）
- 隐私边界未触发（privacy_boundary_violation=0）
- no execute leakage / no default-on / no side effects expansion
- trace/replay/whitebox 完整，post-run summary 可复现

### C. Pause Real Scene Progression（NO_GO）
进入条件（任一满足）：
- hard blocker 出现（execute 泄漏 / default-on / side effects expansion / scope drift / 隐私违规 / 无法中止 / trace/replay 断裂）
- evidence 不可信或不可归档
- abort 失败或无法保证安全中止

---

## 2) 输出（分流结果必须包含，写死）

分流决策输出必须包含：
- `decision`（A/B/C）
- `decision_reason_codes`（数组）
- `hard_blockers`（数组）
- `soft_followups`（数组）
- `next_phase_recommendation`
- 明确声明：
  - 仍不开放用户测试
  - 仍不进入 full controlled trial
  - 默认路径仍未开启
  - side effects 面不扩大

