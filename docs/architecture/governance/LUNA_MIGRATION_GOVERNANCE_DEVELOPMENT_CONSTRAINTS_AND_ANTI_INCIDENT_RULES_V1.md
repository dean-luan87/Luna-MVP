# Luna-Core 迁移整理问题复盘与后续开发约束 v1

**文档类型**：开发约束清单 / 反事故规则（非普通复盘）  
**文档 ID**：`migration_governance_development_constraints_v1`  
**适用范围**：主工程结构迁移及一切高风险 governance phase（planning / dry-run / review / roadmap / authorization / execution 链）  
**机器可读清单**：`migration_governance_development_constraints_v1_manifest.json`（同目录）  
**Verifier 引用**：后续每个 phase 的 `verify_*` 应声明 `governance_constraints_ref=migration_governance_development_constraints_v1` 并对照本清单相关章节；语义不一致则 **NO-GO**。

---

## 0. 文档目的

本轮主工程结构迁移并不是单纯的目录整理，而是一次**系统治理能力显影**。本文档将暴露的问题沉淀为**通用治理约束**，供后续 phase 的 capability、summary、readiness decision 与 verifier **强制引用**。

**禁止误读**：本文档 GO / 登记完成 ≠ 真实授权已释放 ≠ 真实执行已允许。

---

## 1. 本次迁移暴露出的核心问题

迁移过程中反复暴露出：权限语义、边界对象、证据链、成功声明、人工授权、文档同步、测试执行与术语解释等方面的缺口。

若不结构化沉淀，后续一旦进入真实 rollback rehearsal、真实文件迁移、真实 verifier rerun 或 batch arming，极易出现：

- 「规划通过」被误读为「可以执行」
- 「dry-run GO」被误读为「真实成功」
- 「review 结论」被误读为「授权已完成」

**因此**：后续开发必须把本次暴露的问题作为通用治理约束，而不是只服务于本次迁移链路。

---

## 2. 问题一：Planning / DryRun / Review / Roadmap / Authorization / Execution 语义边界不清

### 2.1 问题表现

此前阶段中，容易把以下概念混用：

- planning
- dry-run
- post-dryrun review
- roadmap decision
- authorization planning
- authorization granted
- execution allowed
- execution committed
- success claim

**严重风险**：某个阶段 `verifier=GO` 后，被误解为「可以进入真实执行」。

### 2.2 正确规则

后续所有 phase 必须明确**阶段类型**，并在 `summary` / `readiness decision` / `verifier` 中写死边界字段。

必须区分：

| 字段 | 含义 |
|------|------|
| `planning_only=true` | 只做规划，不执行 |
| `dryrun_only=true` | 只做模拟，不执行 |
| `review_only=true` | 只读审查，不执行 |
| `roadmap_decision_only=true` | 只做路线裁决，不释放权限 |
| `authorization_granted_now=false` | 未授权 |
| `execution_committed=false` | 未执行 |
| `real_*_allowed=false` | 真实能力未开放 |

### 2.3 后续开发约束（强制）

任何 phase 只要不是明确的真实执行阶段，**都必须包含**：

```
runtime_invoked=false
execution_committed=false
write_allowed=false
authorization_granted_now=false
real_rehearsal_execution_allowed=false
real_migration_execution_allowed=false
batch_arming_allowed=false
```

**Verifier 规则**：若阶段语义与 `final_decision` 不一致 → **NO-GO**。

---

## 3. 问题二：权限释放与路线裁决混淆

### 3.1 问题表现

Roadmap Decision 易被误解为「路线选中了，所以权限释放了」。例如选中 Pre-Authorization Planning 后，误判可进入真实 owner/operator approval 或真实 rehearsal。

### 3.2 正确规则

**路线裁决只回答「下一步做什么」，不等于「下一步权限已释放」。**

`Route selected` 只能表示：

- selected route is allowed for **planning**
- selected route is allowed for **dry-run**
- selected route is allowed for **review**
- selected route is allowed for **register**

**不能**表示：

- authorization granted
- execution allowed
- sandbox / branch may be created
- restore map may be generated
- verifier may be rerun
- evidence may be generated

### 3.3 后续开发约束（强制）

每个 Roadmap Decision 必须新增或保留：

- `PermissionNonReleaseMatrix` / `PermissionAuthorizationNonReleaseMatrix`
- `NonClaimsRegister`
- blocked routes / deferred routes
- selected route `permission_impact`（不得写 permission_release=true）

**Verifier 必须校验**：

- selected route 不得释放真实执行权限
- blocked route 不得被 `final_decision` 越级跳过
- `final_decision` 不得直接指向真实 execution，除非前置真实授权链已完成并被审查通过

---

## 4. 问题三：Success Claim 与 Verifier GO 混淆

### 4.1 问题表现

`verifier=GO` 被理解为「阶段成功」，进而误读为「系统行为成功」。在 rollback rehearsal 场景尤其危险。

| 误解 | 事实 |
|------|------|
| DryRun GO | ≠ 真实 rehearsal 成功 |
| Review GO | ≠ 授权完成 |
| Roadmap GO | ≠ execution 可开始 |
| Verifier GO | ≠ 可 success claim |

### 4.2 正确规则

**Verifier GO** 只能表示「该阶段自身约束通过」，不能自动推出真实世界结果。

成功声明必须有独立 gate：

```
success_claim_allowed=false
success_claim_blocked=true
success_conditions_met=false
real_execution_observed=false
evidence_generated=false
verifier_rerun_executed=false
```

### 4.3 后续开发约束（强制）

凡涉及 rollback、migration、execution、WorldModel / Memory / Fact / Library write 的 phase，必须有 **Success Claim Gate**。

`summary` 的 non-claim 必须显式包含：

> GO only means this phase passed its scoped checks. It does not mean real execution is authorized, completed, or successful.

---

## 5. 问题四：边界对象没有全部显式化

### 5.1 问题表现

大量边界对象此前只是隐含约定，例如：protected assets、HR boundary、DnAE、eval_out、phase verdict table、README status、downstream handoff、rollback checkpoint、verifier artifacts、human review queue。

### 5.2 正确规则

所有边界对象必须进入**结构化审查**，不能只写在文档描述中。

### 5.3 后续开发约束（强制）

涉及迁移、回滚、归档、合并、重命名、文档同步的 phase，必须包含（按场景选用）：

- `BoundaryFreezeReviewMatrix`
- `ProtectedScopeMatrix`
- `HR_DnAE_BoundaryMatrix`
- `FileOperationBoundaryReport`
- `NoWriteBoundaryReport`

必须明确：是否允许 read / stat / open / write / move / delete / rename / merge / 生成新 artifact / 修改上游文档状态。

**没有边界矩阵的迁移 phase，不允许 GO。**

---

## 6. 问题五：Owner / Operator 授权机制缺失

### 6.1 问题表现

此前默认「开发者运行脚本即可」；真实 rollback rehearsal 或真实迁移必须有 owner/operator 授权模型。

缺口包括：owner explicit approval、operator acknowledgement、execution window、abort authority、scope confirmation、protected boundary acknowledgement、success claim limitation acknowledgement、real migration / batch arming non-authorization acknowledgement。

### 6.2 正确规则

真实执行前必须区分（**字段不可互相替代**）：

- owner approval
- operator acknowledgement
- execution window opened
- authorization granted
- execution allowed
- execution committed

### 6.3 后续开发约束（强制）

任何真实执行链必须有：

- `OwnerOperatorApprovalRequirementMatrix`
- `ExecutionWindowAuthorizationPlanning`
- `AbortAuthorityPolicy`
- `AuthorizationNonReleaseReviewMatrix`
- `OwnerOperatorApprovalEvidencePlan`

真实授权前必须保持：

```
owner_approval_granted_now=false
operator_acknowledgement_granted_now=false
execution_window_opened_now=false
authorization_granted_now=false
```

---

## 7. 问题六：Evidence Chain 不完整

### 7.1 问题表现

policy / matrix / summary / verifier_report 可生成，但 evidence 边界不稳定：真实 rehearsal 后何种 evidence、谁生成、是否可用于 success claim / rollback audit，缺乏统一规则。

### 7.2 正确规则

Evidence 必须分层（**用途不可混用**）：

1. evidence candidate  
2. dry-run evidence  
3. review evidence  
4. runtime evidence  
5. success-claim evidence  
6. audit evidence  

### 7.3 后续开发约束（强制）

高风险 phase 必须声明：

```
evidence_candidate_only
not_runtime_evidence
not_success_claim
evidence_generation_authorized_now
evidence_generated_now
evidence_can_support_success_claim
```

未经真实授权和真实生成的 evidence，**不能**支撑 success claim。

---

## 8. 问题七：Documentation Sync 成本过高且易漏

### 8.1 问题表现

每 phase 需同步：architecture README、evaluation README、phase verdict table、Implementation Status、downstream handoff、GO/NO-GO pack、evaluation / governance 文档。人工成本高且易遗漏。

### 8.2 正确规则

文档同步本身应成为**可验证对象**，不能仅靠人工记忆。

### 8.3 后续开发约束（强制）

后续 phase 应有（按场景）：

- `DocumentationSyncPlan`
- `DocumentationSyncMatrix`
- `ImplementationStatusUpdateMatrix`
- `DownstreamHandoffUpdateMatrix`
- `PhaseVerdictTableUpdateCheck`

Verifier 必须校验关键文档同步是否**被声明**（长期可自动化）。

**长期建议 phase**：`Phase-Documentation-Sync-Automation-Planning-v1-001`

---

## 9. 问题八：Test Harness 与 Verifier Rerun 仍停留在 planning / dry-run 层

### 9.1 问题表现

多次规划 verifier rerun、rollback verifier、migration test suite，但真实测试执行仍未释放。主线仍处于**治理准备阶段**，不是执行验证阶段。

### 9.2 正确规则

必须区分：

- verifier plan  
- verifier dry-run evaluation  
- verifier authorization  
- verifier execution  
- verifier result evidence  

### 9.3 后续开发约束（强制）

测试相关 phase 必须明确：

```
subprocess_invoked=false/true   # 按阶段
verifier_rerun_authorized_now
verifier_rerun_executed_now
test_execution_allowed
test_result_evidence_generated
```

真实测试执行前，相关字段必须为 **false**。

**长期建议 phase**：`Phase-Main-Project-Structure-Migration-Test-Harness-Execution-Authorization-Planning-v1-001`

---

## 10. 问题九：术语误读已成为主要治理风险

### 10.1 问题表现

越接近真实 rollback rehearsal，**术语误读**往往比技术实现风险更大。

高风险术语：planning、authorization、approval、allowed、ready、GO、success、evidence、candidate、dry-run、simulated、review、roadmap。

### 10.2 正确规则

高风险术语必须有 **canonical meaning**，不允许在不同 phase 中随意解释。

### 10.3 后续开发约束（强制）

必须保留 `PermissionAndAuthorizationTerminologyReview`，至少检查：

- planning vs authorization granted  
- dry-run evaluation vs actual approval  
- simulated decision vs executable decision  
- candidate name vs created sandbox/branch  
- restore map candidate vs generated restore map  
- verifier plan/evaluation vs subprocess execution  
- evidence candidate/evaluation vs generated evidence  
- success claim blocked vs success achieved  
- roadmap readiness vs real execution readiness  

**术语 review 不通过 → phase 不得 GO。**

---

## 11. 问题十：治理对象膨胀，需统一治理债登记

### 11.1 问题表现

policy、matrix、gate、review、decision、non-claim、issue register、verifier report 数量上升后，治理对象碎片化、重复化、难维护。

### 11.2 正确规则

发现问题不能只在当前 phase 补字段，必须进入 **Governance Debt Register** 统一归档。

### 11.3 后续开发约束（强制）

以下情况**必须登记治理债**：

- 同一字段多 phase 语义不统一  
- 边界对象靠文档约定而非 verifier 校验  
- GO 结论可能被误读为 execution allowed  
- candidate artifact 被误用为 executable artifact  
- 手工文档更新流程反复出现  
- 测试/verifier 被规划多次但无真实执行授权  
- owner/operator 判断靠自然语言而非结构化 approval matrix  

---

## 12. 建议登记的治理债分类（9 类）

| ID | 类别 | 说明 |
|----|------|------|
| GD-01 | `permission_semantics_debt` | 权限、授权、执行字段边界不清 |
| GD-02 | `boundary_object_debt` | protected / HR / DnAE / eval_out / verdict table 等无统一边界注册表 |
| GD-03 | `evidence_chain_debt` | candidate / runtime / success evidence 生命周期不统一 |
| GD-04 | `success_claim_debt` | GO、review pass、success claim 隔离不足 |
| GD-05 | `owner_operator_debt` | approval、acknowledgement、abort authority 缺统一协议 |
| GD-06 | `test_harness_debt` | 测试执行、verifier rerun、subprocess 无真实执行治理链 |
| GD-07 | `documentation_sync_debt` | README、phase table、handoff 过度依赖人工 |
| GD-08 | `terminology_debt` | planning / dry-run / ready / granted / success 等需统一语义表 |
| GD-09 | `automation_candidate_debt` | phase registry、doc sync、verdict table、boundary checks 可自动化 |

---

## 12.5 新阶段治理标准复用规则（强制）

### 12.5.1 规则

**English**：New phase must reuse existing governance standard unless it proves a new governance need.

**中文**：新阶段必须复用已有治理标准，除非证明存在新的治理需求。

### 12.5.2 正确规则

后续每个新 phase **默认复用**已有治理标准与 artifact 模式，包括但不限于：

- `migration_governance_development_constraints_v1`（阶段边界、non-claims、verifier 语义）
- `layered_capability_stack_standard_v1` + `layered_governance_mapping_v1`
- Constitution-Bus / Capability-Bus / Provider Abstraction / Controlled Runtime 等已 GO 标准
- 既有 `capability + run + verify` 三件套与 `governance_constraints_ref` 引用方式
- 既有 boundary matrix、blocked paths、non-claims register 模式

**不得**为每个新 phase 重复发明一套平行治理框架，除非该 phase 能证明：

1. 已有标准无法覆盖其 scoped 检查需求；且  
2. 缺口属于**新的治理需求**（非重复命名、非重复 matrix）；且  
3. 新治理产物以 **extension / addendum / binding** 形式登记，而非替换历史标准。

### 12.5.3 后续开发约束（强制）

新 phase 的 planning / dry-run / review 产物必须显式声明：

- `governance_constraints_ref`（指向已有约束源）
- 复用了哪些已有标准（`reused_governance_standards` 或等价字段）
- 若引入新治理 artifact：必须说明 `new_governance_need_proven=true` 及证明摘要
- 若未引入新治理 artifact：`new_governance_need_proven=false`

**Verifier 规则**：若 phase 重复定义与已有标准等价的平行 policy/schema，且未证明新治理需求 → **NO-GO**。

---

## 13. 后续开发强制检查清单（Pre-Phase Gate）

每个高风险 phase **开始前**必须能明确回答以下 21 项；任一无法回答 → **不得 GO**：

1. 这是 planning、dry-run、review、roadmap、authorization，还是 execution？  
2. 是否有真实授权释放？  
3. 是否有真实执行动作？  
4. 是否有 file operation？  
5. 是否有 subprocess？  
6. 是否有 runtime？  
7. 是否修改 protected / HR / DnAE？  
8. 是否写 WorldModel / Memory / Fact / Library？  
9. 是否生成 evidence？  
10. evidence 是否能支撑 success claim？  
11. `verifier=GO` 是否可能被误读？  
12. `final_decision` 是否越级？  
13. selected route 是否释放权限？  
14. `ready` 是 ready for next planning/review，还是 ready for execution？  
15. 是否需要 owner/operator approval？  
16. 是否需要 execution window？  
17. 是否需要 abort authority？  
18. 是否需要 non-claims？  
19. 是否需要 terminology review？  
20. 是否需要登记 governance debt？  
21. 是否已复用已有治理标准？若未复用，是否已证明新的治理需求？  

---

## 14. 后续建议（与 Roadmap Decision 对齐）

**优先 phase**：

`Phase-Main-Project-Structure-Migration-Governance-Debt-Register-v1-001`

目标：**不是**继续推进真实 rollback rehearsal，而是把本轮问题结构化登记为治理债，形成：

- debt register  
- severity matrix  
- ownership / future phase mapping  
- blocked progression rules  
- automation candidate list  
- required verifier additions  
- documentation sync improvement list  
- terminology canonical table  

在 **Governance Debt Register 完成之前**：

- 不建议进入真实 owner/operator approval request  
- 不建议进入真实 rollback rehearsal execution  

---

## 15. 结论

本次问题不是「某个 phase 写错了」，而是 Luna-Core 已进入**受控工程系统阶段**，必须把治理能力产品化。否则 planning / dry-run / review / execution 的误读风险会随规模指数放大。

**本清单为后续 verifier 的规范性引用源**；与具体 phase 文档冲突时，以本清单的「正确规则」与「强制检查清单」为准，并登记 governance debt 修正 phase 文档。
