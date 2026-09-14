# Luna Evaluation & Test Board — Levels 0–9 & Gate Policy v0

**Phase**：`Phase-Luna-Evaluation-Test-Board-001`  
**定位**：**Luna 全局** 分级测试与准入闸门；**非 OCR 专属**。OCR 仅为首批映射对象之一。

**关键禁令**：**benchmark GO、smoke GO、单次跑通** 均 **不得** 解释为 **上线许可**、**默认 provider 切换许可** 或 **release 完成**。上线与 shadow 仅能在 **Level 9** 及配套审计下讨论。

**Level 9（Shadow / Release Gate）后置**：仅当 Level 0–8 中 **本模块策略所要求的必要等级** 均已满足（或已文档化豁免并审批）后，才允许进入 **Level 9** 的 shadow / release gate 测试与评审。

---

## Level 0：Static Contract Test

- **目标**：文档、schema、config、字段、索引、禁止项齐全。  
- **运行模型**：否。  
- **GO**：静态 verifier 无 blocker，policy matrix 完整。

## Level 1：Smoke Test

- **目标**：1–3 样本，工具链可启动并落盘。  
- **GO**：可运行、无越界；**注意：Smoke GO 不代表质量通过。**

## Level 2：Functional Test

- **目标**：3–20 样本，核心功能按 contract 输出。  
- **GO**：链路完整、结构正确。

## Level 3：Labeled / Ground Truth Test

- **目标**：带 GT 的质量评测（通常 20–50 起）。  
- **GO**：样本量、GT 覆盖率、类别覆盖达标；**GO 仅表示评测完成，生产阈值另文定义。**

## Level 4：Batch / Recovery Test

- **目标**：拆批、续跑、崩溃捕获与合并指标。  
- **必须覆盖**：`batch_size ∈ {1,5,10}`（或模块等价拆批）、crash capture、resume、merge metrics。  
- **GO**：全量完成，或崩溃可定位且报告完整（**CONDITIONAL_GO** 可接受但须列明缺口）。

## Level 5：Interrupt / Cancellation Test

- **目标**：用户取消、超时、优先级抢占、降级中断等。  
- **GO**：见 `LUNA_EVALUATION_INTERRUPT_AND_RECOVERY_TEST_POLICY_V0.md`。

## Level 6：Long-Run Stability Test

- **目标**：30min / 1h / 4h / 8h / 24h soak（后期）等档位。  
- **GO**：见 `LUNA_EVALUATION_LONG_RUN_STABILITY_TEST_POLICY_V0.md`。

## Level 7：Scenario / Task-Type Performance Test

- **目标**：分任务类型的延迟、成功率、资源画像。  
- **GO**：见 `LUNA_EVALUATION_TASK_TYPE_PERFORMANCE_TEST_POLICY_V0.md`。

## Level 8：Cross-Modal / STCM Test

- **目标**：OCR / Vision / Voice / STCM 的 deadline、过期丢弃、语音通知等 **时空间一致性**。  
- **GO**：见 `LUNA_EVALUATION_CROSS_MODAL_STCM_TEST_POLICY_V0.md`。

## Level 9：Shadow / Release Gate Test（后置）

- **目标**：shadow 无副作用、routing 不变、diff 审计、回滚、kill switch、release checklist。  
- **GO**：无副作用、可回滚、审计完整；**且** 前置等级门槛已满足。

---

## 回归策略（摘要）

- **Level 0–2**：每次 contract / 工具链变更 **必跑** 静态或 smoke。  
- **Level 3+**：按模块 **risk tier** 与变更面触发 **全量或抽样** 回归；**batch / 长稳 / 中断** 按发布节奏 **阶梯触发**。  
- **失败升级**：低等级 NO_GO **冻结** 高等级结论直至修复或正式豁免。

---

## PaddleOCR 首批映射（示例，非排他）

| 既有 phase / 能力 | 对应 Level |
|-------------------|------------|
| PaddleOCR-Controlled-Trial-001 | 1 / 2 |
| API-Adapter-Contract-001 | 2 |
| Evidence Alignment | 2 |
| Bridge Pack Consumer Static | 0 / 2 |
| Evaluation Benchmark | 2 |
| Labeled Set Evaluation | 3 |
| Batch Recovery | 4 |
| Provider Governance Standard | 0 |
| STCM / Event Skeleton | 0（设计）/ 8（联测） |

**当前状态（叙述级，以各专项 verifier 为准）**：benchmark pipeline 可视为 **Level 2 向 GO**；labeled set 质量 **Level 3 CONDITIONAL_GO**；stability recovery **Level 4 IMPLEMENTED / PENDING_RUN**；**禁止** 在 Level 3/4 稳定性未补齐前进 **shadow provider**（Level 9 前置未满足）。
