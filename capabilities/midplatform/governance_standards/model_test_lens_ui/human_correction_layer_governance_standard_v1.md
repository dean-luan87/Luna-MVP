# Human Correction Layer Governance Standard V1

**Standard ID:** `HumanCorrectionLayerGovernanceStandardV1`  
**Phase:** `Phase-P1-Midplatform-Model-Test-Lens-Human-Correction-Layer-Planning-v1-001`  
**Upstream:** Luna Observation Lens V1 Closure GO

## 定位

Human Correction Layer 是 Luna Observation Lens 的 **人工纠错治理层**。它连接：

```
模型结果 → 人指出错误 → 结构化 correction record
→ TestBoard / Error Registry / Future Training Set Candidate
→ 后续同类场景重点复测
```

## 治理原则

1. **Correction candidate only** — 用户指错不成为 fact。  
2. **Envelope immutable** — 原始 envelope 只读引用。  
3. **Model output immutable** — HUD 展示层不覆盖模型输出字段。  
4. **TestBoard required** — 每条 session 写入受保护 TestBoard 记录。  
5. **Training gate** — 训练/强化前必须 owner + quality + consent review。  
6. **V1 layout preserved** — 纠错入口为轻量叠加，不改变 V1 七区布局。

## TestBoardProtectedArtifactRuleV1 追加规则（36 条）

在既有 6 条全局规则之上，Human Correction Layer 追加：

1. Human Correction Layer is a first-class Luna Observation Lens extension.  
2. Corrections are correction candidates only, not facts.  
3. Corrections must not modify original envelope.  
4. Corrections must not overwrite model output.  
5. Corrections must not write semantic layer.  
6. Corrections must not write facts.  
7. Corrections must not trigger runtime.  
8. Corrections must not call output adapter.  
9. Corrections must not trigger navigation/action/speech.  
10. Corrections must not mutate registry.  
11. Corrections must not auto-enter training.  
12. Corrections must not auto-become ground truth.  
13. Corrections must not auto-become RL reward.  
14. Correction records require source_envelope_ref.  
15. Correction records require correction_type.  
16. Correction records require correction_target.  
17. Correction records require candidate_only and not_fact.  
18. Training signals require not_auto_training_data.  
19. Training signals require needs_owner_review.  
20. Hard case candidates require governance review before dataset promotion.  
21. Regression test candidates require benchmark owner approval.  
22. Correction session must write TestBoard.  
23. TestBoard correction artifacts are protected.  
24. TestBoard correction records are non-deletable.  
25. Cleanup must not delete correction TestBoard artifacts.  
26. Luna Observation Lens V1 layout must be preserved.  
27. Central HUD must remain largest visual region.  
28. Object chip bar correction entry must be lightweight.  
29. Correction drawer must default collapsed.  
30. Developer JSON for corrections is hidden by default.  
31. UI must not execute models during correction capture.  
32. UI must not use live camera/microphone for correction.  
33. UI must not fetch external URLs for correction.  
34. Failure patterns may feed Model Improvement Queue as candidates only.  
35. Sensitive corrections require consent review.  
36. Future model pages must reuse Luna Observation Lens V1 + correction slots.

## 禁止矩阵

| 操作 | 允许 | 说明 |
|------|------|------|
| 创建 correction record | ✓ | candidate_only |
| 修改 envelope | ✗ | 只读引用 |
| 覆盖 HUD 模型字段 | ✗ | 叠加层展示 |
| 写 fact | ✗ | not_fact |
| 写 semantic | ✗ | |
| 触发 runtime | ✗ | |
| 自动训练 | ✗ | 需 review gate |
| 写 TestBoard | ✓ | protected |

## Schema 注册

| Schema | Path |
|--------|------|
| Record | `schemas/human_correction/human_correction_record_schema_v1.json` |
| Target | `schemas/human_correction/human_correction_target_schema_v1.json` |
| Taxonomy | `schemas/human_correction/human_correction_feedback_taxonomy_v1.json` |
| Training Signal | `schemas/human_correction/human_correction_training_signal_schema_v1.json` |

## 下游队列（候选，非自动）

- Correction Registry  
- Failure Pattern Registry  
- Hard Case Dataset Candidate  
- Model Improvement Queue  
- Regression Test Candidate  

## 执行阶段

`Phase-P1-Midplatform-Model-Test-Lens-Human-Correction-Layer-UI-Execution-And-Post-Review-v1-001`
