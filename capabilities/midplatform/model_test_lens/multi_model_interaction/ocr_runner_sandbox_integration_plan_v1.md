# OCR Runner Sandbox Integration Plan V1

**Phase:** `Phase-P1-Midplatform-Multi-Model-Interaction-MobileSAM-OCR-Runner-Sandbox-Integration-Planning-v1-001`  
**System ID:** `LunaMidplatformMobileSamOcrRunnerSandboxIntegrationPlanningV1`  
**Status:** Planning only（本阶段不执行 OCR runner · 不生成真实 OCR result）

## 上游 GO

| 基线 | 决策 |
|------|------|
| MobileSAM Single Model Execution Integration | GO |
| MobileSAM → OCR Exploration Smoke | GO |
| MobileSAM-OCR Controlled Execution Planning | GO |
| MobileSAM-OCR Controlled Execution UI Execution | GO |

## 本阶段终点

**OCR Runner Sandbox Integration Plan** — 不是 OCR execution，不是 OCR result，不是 fact。

未来阶段将允许 `ocr_runner_execution=true`，但本阶段仅规划 Sandbox 边界与协议。

## 冻结链路

```
OCR Task Candidate
  ↓
OCR Invocation Request
  ↓
OCR Admission
  ↓
OCR Controlled Execution Candidate
  ↓
OCR Runner Sandbox                    ← 本阶段规划终点（接入方案）
  ↓
OCR Runtime                           （未来）
  ↓
OCR Result Envelope                   （未来）
  ↓
Midplatform Fusion                    （未来）
  ↓
Fact Admission                        （未来，不自动）
```

## 核心要钉死的 5 件事

### 1. 唯一入口：OCR Controlled Execution Candidate

OCR runner **只能**从 `ocr_controlled_execution_candidate` 进入。

**禁止入口：**

- UI 直接 POST OCR runner
- MobileSAM result 直调 OCR runner
- OCR task candidate 直调 OCR runner
- Human Correction 直调 OCR runner

### 2. OCR 输入 = 受控裁剪区域

**允许：**

- `source_image_ref`
- `source_region_id`
- `region_crop_ref`
- `region_geometry_ref`
- `source_ocr_execution_candidate_id`
- `source_ocr_task_candidate_id`
- `source_analysis_record_id`
- `ocr_target_reason`
- `trace_chain`

**禁止：**

- confirmed text / fact label
- 路牌断言 / confirmed_object_type / confirmed_sign_type
- human correction as truth
- navigation context
- MobileSAM prompt_label as fact

原则：OCR 只收到「这里值得做文字观察」，不是「这里是什么文字」。

### 3. OCR 输出 = OCR Result Envelope

**必须字段：**

- `text_candidate_list`
- `text_region_candidate`
- `reading_order_candidate`
- `confidence`
- `source_ocr_execution_id`
- `needs_fact_admission`
- `not_fact`

**禁止：** 直接进入 fact / 导航指令 / confirmed_sign

`completed` 只代表 runner 完成，**不代表 text fact**。

### 4. 错误 = OCR Runner Error Candidate

错误类型：`timeout` · `runner_unavailable` · `invalid_crop` · `empty_text` · `low_confidence` · `invalid_output_schema` · `unreadable_region` · `route_mismatch` · `cancelled`

错误必须：`not_fact` · `not_navigation_decision` · 可追溯至 execution candidate · `recoverable` 标记

**禁止：** 污染 Result Layer / Fact Layer

### 5. 多模型融合晚于 OCR Envelope

```
MobileSAM geometry candidate + OCR text candidate
  ↓
multimodal_evidence_candidate
  ↓
Fact Admission
```

不是 OCR 一跑完就确认「这是路牌」。

## OCR Runner Sandbox 职责

| 方法 | 职责 |
|------|------|
| `validate_ocr_execution_candidate()` | 校验 candidate 状态、trace、准入边界 |
| `build_ocr_adapter_input()` | 从 candidate 构建 adapter input（无 fact 字段） |
| `prepare_ocr_execution()` | 生成 execution record（pending），不写 result |
| `validate_ocr_runner_output()` | 校验 runner 原始输出 schema |
| `build_ocr_result_envelope()` | 包装为 ocr_result_envelope |
| `build_ocr_runner_error_candidate()` | 隔离错误，不写 fact |

本阶段仅定义接口与 schema，**不实现 runtime 调用**。

## Runner Bridge Contract（8787）

- 入口：`POST /api/v1/controlled-execution/ocr/run`（规划，本阶段未实现）
- 仅 Sandbox 可调用，UI 禁止直调
- 请求携带 `ocr_adapter_input` + `ocr_execution_id`
- 响应：`ocr_result_envelope` 或 `ocr_runner_error_candidate`
- 超时、schema validation、error response 见 `ocr_local_runner_bridge_contract_v1.json`

## Human Correction Runtime 分流（OCR result 之后）

| 用户反馈 | 归因 | 出口 |
|----------|------|------|
| 文字读错了 | OCR model_error | OCR training_candidate pending_review |
| 选错区域了 | MobileSAM region_selection_error | MobileSAM rerun_candidate |
| 这块不该读 | OCR route_strategy_error / attention_priority_error | route policy / priority signal |
| 以后多读公交站牌 | user_preference | preference_memory candidate |

禁止：用户纠错直接改 OCR result / 直接训练 OCR / 用户输入作 fact text（非 ground truth）

## 本阶段禁止

- 调用 OCR runner / 跑 OCR 模型 / 生成真实 OCR result
- 写 fact / 导航决策
- 改变 Visual Expression System
- 主图新增 OCR box / preview
- 重构既有治理链

## 产出

见 `schemas/multi_model_interaction/` 与 `ocr_runner_sandbox_types_v1.py`

## 下一阶段

`Phase-P1-Midplatform-Multi-Model-Interaction-MobileSAM-OCR-Runner-Sandbox-Integration-Execution-v1-001`（建议）

顺序：OCR Sandbox 接入 → OCR Runtime → OCR Result Envelope → MobileSAM+OCR Fusion
