# MobileSAM → OCR Controlled Execution Plan V1

**Phase:** `Phase-P1-Midplatform-Multi-Model-Interaction-MobileSAM-OCR-Controlled-Execution-Planning-v1-001`  
**System ID:** `LunaMidplatformMobileSamOcrControlledExecutionPlanningV1`  
**Status:** Planning only（本阶段不执行 OCR runner）

## 上游 GO

| 基线 | 决策 |
|------|------|
| MobileSAM Single Model Execution Integration | GO |
| Single Model Interaction Validation UI Execution | GO |
| MobileSAM → OCR Exploration Smoke | GO |

## 本阶段终点

**OCR Controlled Execution Candidate** — 不是 OCR execution，不是 OCR result，不是 fact。

## 冻结链路

```
Image
  ↓
MobileSAM Controlled Execution
  ↓
Segmentation Result Envelope
  ↓
Result Candidate
  ↓
Midplatform Processing
  ↓
OCR Route Candidate
  ↓
OCR Task Candidate
  ↓
OCR Invocation Request
  ↓
OCR Admission
  ↓
OCR Controlled Execution Candidate   ← 本阶段终点
  ↓
OCR Runner Execution（未来）
  ↓
OCR Result Envelope
  ↓
Midplatform Fusion
  ↓
Fact Admission（未来，不自动）
```

## 核心设计目标

1. OCR 输入来自中台生成的 OCR task candidate  
2. OCR 不直接读取 MobileSAM 原始输出  
3. OCR 不由 MobileSAM 直接调用  
4. OCR request 必须经过 invocation request → admission → controlled execution candidate  
5. OCR output 未来必须进入 OCR Result Envelope  
6. OCR result ≠ fact  

## OCR 输入边界

OCR 只接受：「这里值得做文字观察」  
禁止：「这里是什么文字」/ confirmed text / fact label / 这是路牌

## Human Correction 双模型分流

| 归因 | 出口 |
|------|------|
| OCR model_error | OCR training_candidate pending_review |
| MobileSAM region_selection_error | MobileSAM rerun_candidate |
| OCR route_strategy_error | OCR route policy update |
| attention_priority_error | priority_update_signal |
| user_preference | preference_memory candidate |

禁止：直接训练 OCR / 改 OCR result / 改 MobileSAM mask / 用户输入作 OCR truth

## 本阶段禁止

- 调用 OCR 模型 / 生成 OCR result / **不写 fact**
- 自动确认文字 / 修改 MobileSAM 结果  
- 改变 Visual Expression System / 重构治理链  
- 主图绘制 OCR box（`no_ocr_box_on_canvas`）

## 产出

见 `schemas/multi_model_interaction/` 与 `multi_model_interaction/mobile_sam_ocr_controlled_execution_types_v1.py`

## 下一阶段

`Phase-P1-Midplatform-Multi-Model-Interaction-MobileSAM-OCR-Controlled-Execution-UI-Execution-v1-001`
