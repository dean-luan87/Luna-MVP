# Single Model Interaction Validation Plan V1

**Phase:** `Phase-P1-Midplatform-Single-Model-Interaction-Validation-v1-001`  
**System ID:** `LunaMidplatformSingleModelInteractionValidationV1`  
**Status:** Planning + Validation（本阶段**不接 OCR/Detection 真模型**，只验证中台二次调度）

## 架构分界点（已跨过）

| 之前 | 现在 |
|------|------|
| 中台能不能**治理**模型进入系统 | 中台能不能在治理边界内**驱动**模型运行 |
| `runner_execution` 禁止 | `runner_execution=true`（仅 MobileSAM + 沙箱） |
| 单向：中台 → 模型 | 闭环：中台 → 模型 → 结果候选 → **中台重新理解** → 下一任务 |

**本阶段目标：** 验证模型结果能否成为中台下一轮决策输入，而非继续测试 MobileSAM 本身。

## 第一轮闭环（Case 1）

```
街景图片
    ↓
MobileSAM（已 GO）
    ↓
segmentation_result_envelope
    ↓
Result Layer / Result Candidate
    ↓
Midplatform Processing（本阶段新增）
    ↓
Observation Re-evaluation Candidate
    ↓
followup_model_route_candidate
    ↓
OCR task candidate（仅候选，不跑 OCR）
```

## 第二轮闭环（Case 2 — 更验证中台本体）

```
MobileSAM segmentation_result_envelope
    ↓
用户纠错（Human Correction Layer）
    ↓
Midplatform Correction Analysis（归因 / 分类 / 路由）
    ↓
分流：
  · 模型问题 → training_candidate (pending_review) + model_rerun_candidate
  · 策略问题 → routing_policy_update_candidate
  · 优先级问题 → attention_policy_update_candidate + priority_signal
  · 用户偏好 → user_preference_update_candidate
```

**禁止：** 用户纠错 → 直接训练模型 / 修改 mask

## Human Correction 中台入口（与 priority signal 一致）

```
用户纠错 → Human Correction Layer → Midplatform Analysis → 决定用途
  ① 调整任务策略
  ② 调整模型路由
  ③ 生成训练数据（净化后 + pending_review）
  ④ 模型复跑候选
```

训练吃的是 **Human Correction Dataset（净化后）**，不是 **Raw Log**。

**关键原则：** MobileSAM 只说「区域在哪里」，不说「这是路牌」。  
中台结合 region geometry、appearance candidate、task context、policy 决定「这个区域值得 OCR」。

## 五能力验证矩阵

### 1. Result Envelope → 中台输入

```
MobileSAM output → Result Envelope → Result Candidate → Midplatform Processing
```

禁止：`MobileSAM output → 直接 UI 路由`

### 2. Result Candidate 不污染 Observation

- Observation Attention 原始记录保持 `candidate`
- `segmentation_result` **不得覆盖** attention record
- 模型结果只是 **new evidence**，写入 `observation_update_candidate`

### 3. 中台二次调度（核心）

```
Result Candidate → Observation Re-evaluation → OCR task candidate
```

禁止：`MobileSAM → OCR API`（pipeline bypass）

### 4. Human Correction 闭环

```
MobileSAM → Result Candidate
用户纠错 → priority signal（非 ground truth）
    → new task candidate → MobileSAM rerun（未来）
```

禁止：`用户纠正 → 修改 mask`

### 5. Trace 闭环

```
Image → Segmentation Region → Execution Candidate → Runner Execution
    → Result Envelope → Observation Update → New Task Candidate
```

## 本阶段不做

- 不接 OCR / Detection 真模型  
- 不写 fact  
- 不自动 Fact Admission  
- 不让 MobileSAM 输出直接覆盖 segmentation boundary owner  
- 不做多模型协同（留待下一阶段）

## 通过后扩展路径

1. MobileSAM + OCR（第一个双模型互动）  
2. MobileSAM + Detection + OCR + Depth + Tracking  

## 产出文件

| 文件 | 用途 |
|------|------|
| `single_model_interaction_validation_plan_v1.md` | 本文件 |
| `single_model_interaction_validation_types_v1.py` | 常量 |
| `result_to_midplatform_processor_v1.py` | Case 1 处理逻辑（规划参考实现） |
| `schemas/.../result_envelope_midplatform_input_schema_v1.json` | 结果进入中台输入 |
| `schemas/.../observation_re_evaluation_from_result_policy_v1.json` | 观察再评估策略 |
| `schemas/.../followup_route_from_result_policy_v1.json` | 从结果生成 route |
| `schemas/.../interaction_trace_closure_policy_v1.json` | Trace 闭环 |
| `schemas/.../case_mobilesam_to_ocr_route_validation_v1.json` | Case 1 规格 |
| `schemas/.../case_mobilesam_correction_midplatform_validation_v1.json` | Case 2 纠错分流 |
| `human_correction/correction_midplatform_analyzer_v1.py` | 纠错归因与路由 |
| `static_site/human_correction_midplatform_analyzer_v1.js` | UI 中台分析层 |
| `governance_standards/.../single_model_interaction_validation_governance_standard_v1.md` | 治理标准 |
| `review_model_test_lens_single_model_interaction_validation_planning_v1.py` | Planning review |

## 下一阶段

`Phase-P1-Midplatform-Single-Model-Interaction-Validation-UI-Execution-v1-001`  
在 Result Layer 展示「中台二次调度候选」UI，仍不跑 OCR。
