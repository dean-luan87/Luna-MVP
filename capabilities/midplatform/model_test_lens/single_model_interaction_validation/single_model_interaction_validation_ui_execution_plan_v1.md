# Single Model Interaction Validation — UI Execution Plan V1

**Phase:** `Phase-P1-Midplatform-Single-Model-Interaction-Validation-UI-Execution-v1-001`  
**Upstream GO:** `P1_MIDPLATFORM_MODEL_TEST_LENS_SINGLE_MODEL_INTERACTION_VALIDATION_PLANNING_GO`

## 目标

在 Result Layer 透明展示中台二次理解过程，让人看懂「中台为什么这么做」。

**不增加模型能力：** 不接 OCR · 不跑 Detection · 不写 fact · 不修改 mask · 不自动训练

## 右侧面板结构

```
结果候选区
    ↓
中台二次理解（Midplatform Analysis Record Card）
    ↓
纠错分析（Case 2 Attribution）
```

## Case 1 UI

- Result Candidate：MobileSAM · Segmentation Result Candidate · 区域几何信息 · candidate_only
- 中台分析：区域特征 · OCR route candidate · 原因（值得进一步文字观察）
- **禁止文案：** MobileSAM 推荐 OCR / 确认这是路牌

## Case 2 UI

- Human Correction → 中台归因 → 建议出口
- boundary_error → model_error → training pending + rerun
- 「不用看」→ attention_priority_error → priority_signal · 训练：否

## 模块

| 文件 | 用途 |
|------|------|
| `midplatform_interaction_copy_v1.js` | 文案 |
| `midplatform_result_processor_v1.js` | Case 1 处理 |
| `midplatform_interaction_panel_v1.js` | 分析卡片 + Trace |
| `midplatform_interaction_state_v1.js` | UI 状态包 |

## Trace

Case 1: Image → Segmentation Region → Execution → Result Envelope → Midplatform Analysis → OCR Task Candidate  
Case 2: User Correction → Correction Record → Attribution → Policy/Training exit
