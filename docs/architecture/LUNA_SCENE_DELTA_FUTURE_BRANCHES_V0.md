# LUNA — Scene Delta Future Branches v0

## Phase

- **Phase-MidPlatform-SceneDelta-003**

## Purpose

列出 `closed_v0` 之后的可选分支，避免 closure 阶段引入新功能或误触 runtime。

## Candidate future branches（仅列举，不进入）

1. **SceneDelta evidence expansion**
   - 扩充样本与输入类型覆盖（screen/carrier_removed/contradicted 等）
2. **SceneDelta real upstream integration**
   - 与真实上游 evidence pipeline 的接线定义（仍需严格边界）
3. **WorldContextEvidence write readiness**
   - 从 candidate-only 走向可控写入（revalidation/trust/TTL）
4. **Hive candidate packaging definition**
   - hive_group_candidate → verified_pack 的隐私/验证/门控定义
5. **Task context dynamic reevaluation implementation**
   - task_context_changed 的真实实现与评测
6. **Advanced compression / cold storage**
   - delta encoding / rolling window summary 的更完整实现
7. **Contradicted evidence resolution**
   - 冲突证据的“并存/降级/复核”策略与 verifier 扩展

8. **Uncertain evidence user confirmation insert task**
   - 存疑证据的“用户确认插入任务”（只在低优先级空档问；短窗口；不打断导航/安全/主任务；超时不追问）：`docs/architecture/LUNA_UNCERTAIN_EVIDENCE_USER_CONFIRMATION_INSERT_TASK_POLICY_V0.md`

9. **Human Interaction Validation Layer**
   - 人机互动验证层：对用户反馈做 truth-type 分类，避免“用户反馈直接覆盖事实”，并为情感引擎预留接口：`docs/architecture/LUNA_HUMAN_INTERACTION_VALIDATION_LAYER_CONTRACT_V0.md`

