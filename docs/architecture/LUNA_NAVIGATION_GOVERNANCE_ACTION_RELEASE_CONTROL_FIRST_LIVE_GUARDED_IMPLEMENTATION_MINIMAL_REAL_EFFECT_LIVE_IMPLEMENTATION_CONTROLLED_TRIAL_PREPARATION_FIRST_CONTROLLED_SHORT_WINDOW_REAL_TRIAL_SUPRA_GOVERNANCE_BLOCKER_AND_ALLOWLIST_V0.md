# Phase-Next-182 — Supra-Governance Blocker And Allowlist v0（白/黑名单与阻断项冻结）

**目的**：明确“进入下一层更高治理链/后续治理定义链”时，允许做什么、禁止做什么、以及 hard blockers / soft follow-ups 的判定口径。  
**注意**：本文件是治理边界与清单，不是 runtime 放行逻辑，不授予任何新的运行时权限。  

---

## 1) 下一阶段允许动作白名单（Allowlist）

以下仅指 **下一阶段更高层治理链** 的动作类型（definition / pack），且必须满足非默认路径与 closed-safe 要求：

- **A1. Governance definition / constitution drafting（只读治理层）**  
  - 允许在明确“非默认入口”前提下，推进更高层治理链的 definition v0（例如 Phase-Next-183 的定义冻结）。
- **A2. Governance go/no-go pack drafting（证据归档/决策包）**  
  - 允许形成更高层治理链进入资格的 go/no-go pack（不触发任何真实动作）。
- **A3. Evidence/trace/runbook strengthening（只读增强）**  
  - 允许加强证据矩阵、原因码、审计 trace 可读性与归档。
- **A4. Shadowed validation/evaluation expansion（只读审计层扩展）**  
  - 允许增加更多只读验证场景（不改 runtime 语义，不开启默认路径）。

**必须继续沿用的硬前提（不可削弱）**：
- legal meta-governance completion prerequisite
- closed-safe prerequisite
- allowed supra-governance outcome allowlist only
- forbidden supra-governance blocking
- closed-safe-state preservation
- **no-next-runtime-now**（`allows_next_runtime_now=false`）
- default path disabled（非默认路径）

---

## 2) 下一阶段禁止动作黑名单（Denylist）

以下任一出现，都视为越界（至少 hard blocker；视情况直接 NO_GO）：

- **D1. default-on / 启用默认路径**（任何形式）
- **D2. implicit reopen**（直接或间接）
- **D3. implicit retry runtime**（直接或间接）
- **D4. implicit widening**（扩窗/扩面/扩频/扩副作用类别，且未新增治理定义）
- **D5. implicit full controlled trial continuation**（把治理结论当成“继续真实运行链”）
- **D6. implicit long-running enablement**（把短窗治理滑向长期运行许可）
- **D7. 修改 allowed outcome / forbidden blocker 的语义**（破坏 179/180/181 的边界一致性）
- **D8. governance 阶段打开新的 real side-effects window**（任何真实副作用放权）
- **D9. governance 阶段直接触发下一次 real execute / retry / reopen**
- **D10. 将 181 或 182 的 go 解释为“已批准继续真实运行”**

---

## 3) Hard Blockers（硬阻断项）

满足以下任一条，必须判定为 **hard_blocker**（并在 pack 中转 NO_GO 或阻断进入下一阶段）：

- **HB1**：无 legal meta-governance completion 却进入 supra-governance  
- **HB2**：输出 forbidden supra-governance outcome 或 allowlist 外 outcome  
- **HB3**：governance 后破坏 closed-safe state（`closed_safe_state_preserved!=true` 或 `keeps_system_closed!=true`）  
- **HB4**：`allow_next_governance_preparation_under_same_guardrails` 被实现成自动进入下一阶段 runtime（`allows_next_runtime_now==true` 或等价通道）  
- **HB5**：出现隐式 reopen / retry runtime / widen / long-running / default-on  
- **HB6**：默认路径存在误触发风险（可复现）  
- **HB7**：下一阶段将实质扩大副作用面却无新治理定义支撑

**当前 hard blockers：none observed**  
依据：Phase-Next-181 overall_evaluation=go 且关键完整性指标均 pass。

---

## 4) Soft Follow-Ups（软补强项，不阻断）

以下属于 **soft_followup**，不影响当前安全边界成立，但建议在下一阶段前/中补齐：

- **SF1**：reason codes / audit trace 的可读性与归档一致性进一步增强  
- **SF2**：runbook（人工确认点、回溯入口、证据链接）更明确  
- **SF3**：增加额外只读场景覆盖（例如更多组合 forbidden_signals/证据缺失组合），但不改变 runtime 语义

---

## 5) 当前结论对外解释模板（防误读）

- **允许进入下一阶段**：仅允许进入“更高层治理链 definition/pack”，不含任何真实运行放行。  
- **禁止推断**：不得把 go/no-go pack 的 GO 理解为 retry/reopen/execute/full trial/long-running 的批准。  

