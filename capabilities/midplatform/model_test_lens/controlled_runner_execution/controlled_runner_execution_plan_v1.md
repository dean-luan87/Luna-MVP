# Controlled Runner Execution Plan V1

**Phase:** `Phase-P1-Midplatform-Model-Test-Lens-Detection-OCR-Controlled-Runner-Execution-Planning-v1-001`  
**System ID:** `LunaModelTestLensControlledRunnerExecutionV1`  
**Status:** Planning only（本阶段不调用 Detection/OCR runner、不跑模型、不写 fact、不产生真实模型输出）

## 上游（全部 GO）

- Followup Runner Route UI Queue Execution  
- Detection/OCR Runner Manual Trigger Planning + UI Execution  
- Runner Invocation Admission Execution  
- Visual Expression System 冻结  
- `browser_runtime_guard_v1.js` 继承有效

## 五层关系（本阶段钉死）

| 层 | 语义 | 本阶段 |
|----|------|--------|
| `runner_task_candidate` | 可以考虑做什么 | 上游 GO |
| `runner_invocation_request` | 准备申请执行什么 | 上游 GO |
| `runner_invocation_admission` | 是否允许进入执行准备 | 上游 GO |
| `controlled_runner_execution_candidate` | **准备如何受控执行** — 执行计划/封装候选 | **本阶段规划终点** |
| `runner_execution` | 真正跑模型 | **禁止** |

**admitted request 只是允许进入执行准备，不等于执行。**  
**controlled_runner_execution_candidate 是执行计划候选，不是模型运行结果。**  
**runner output 后续必须进入 result envelope 与 fact admission，不能直接写 fact。**

## 核心链路（规划冻结）

```
runner_task_candidate (pinned)
        ↓
runner_invocation_request
        ↓
runner_invocation_admission (admission_decision = admitted)
        ↓
controlled_runner_execution_candidate    ← 本阶段规划终点
  (execution_status: planned_only / not_executed)
        ↓
runner_execution                       ← 未来受控执行阶段 only
        ↓
runner_output_envelope (result candidate)
        ↓
fact_admission                         ← 独立阶段，本阶段禁止
```

## 执行准入条件

仅当以下条件 **全部满足** 才可生成 `controlled_runner_execution_candidate`：

1. `runner_invocation_request` 存在且非 orphan  
2. `admission_decision === admitted`  
3. `execution_status === not_executed`  
4. `trace_chain` 完整（region → attention → route → task → request → admission）  
5. `requested_runner_type` 与 admission `route_match_verified` 一致  
6. source task 仍为 pinned，或 policy 允许 request snapshot 固化  
7. request 未 `cancelled` / 未 `rejected` / 未 `stale`

### 禁止

- pending / rejected / cancelled request 生成 execution candidate  
- orphan request 生成 execution candidate  
- admitted 直接调用 runner  
- UI 绕过 admission 生成 execution candidate

## Detection / OCR 输入边界

见：

- `detection_controlled_execution_input_policy_v1.json`  
- `ocr_controlled_execution_input_policy_v1.json`

### Detection 输入允许

- `region_crop` / `region_geometry_ref`  
- `source image / frame ref`  
- `prompt_label_candidate`（非 fact label）  
- 不确认 dynamic、不写 object fact

### OCR 输入允许

- `region_crop` / text-likely region ref  
- `source image / frame ref`  
- OCR target reason  
- human correction 仅 priority signal

### 输入禁止

- fact label、confirmed_dynamic、prompt_label as truth、human correction as ground truth

## 输出 Envelope 规划

见 `runner_output_envelope_policy_v1.json`。本阶段不产生真实输出，但规划 envelope 结构。

### Detection output（未来）

- `detection_result_candidate`  
- `object_detection_candidate`  
- `confidence`  
- `bbox` / `mask` / `region_relation`  
- `source_runner_execution_id`  
- `not_fact` · `needs_fact_admission`

### OCR output（未来）

- `ocr_text_candidate`  
- `text_region_candidate`  
- `confidence`  
- `reading_order_candidate`  
- `source_runner_execution_id`  
- `not_fact` · `needs_fact_admission`

### 输出禁止

- 直接写 fact、直接进入 navigation、覆盖 attention record、覆盖 segmentation label

## 错误隔离

见 `runner_error_policy_v1.json`。

错误类型：`timeout`、`runner_unavailable`、`invalid_crop`、`route_mismatch`、`schema_validation_failed`、`model_output_invalid`、`confidence_too_low`、`execution_cancelled`。

错误结果必须是 `runner_error_candidate`，**不得写 fact**。

## Fact Admission 分层

```
runner_execution_result ≠ fact
Detection/OCR 结果 → result candidate only
Fact 写入 → 单独 Fact Admission 阶段
```

禁止：execution candidate 写 fact、runner result 自动写 fact、OCR 文本自动成事实、Detection label 自动成事实类别。

## Visual Expression System

- execution candidate **不在主图画 box**  
- runner result 未来需独立 result layer owner  
- Detection/OCR 结果不得默认覆盖 segmentation boundary  
- 结果展示通过右侧结果候选区或 selected mode  
- 主图不新增 execution box（`no_execution_box_on_canvas`）

## UI 未来表达（本阶段不实现）

| 允许 | 禁止 |
|------|------|
| 生成受控执行候选 | 开始检测 |
| 准备 Detection 执行 | 立即 OCR |
| 准备 OCR 执行 | 执行完成 |
| 尚未运行 | 识别结果 |

## 推荐下一阶段

`Phase-P1-Midplatform-Model-Test-Lens-Detection-OCR-Controlled-Runner-Execution-UI-Execution-v1-001`  
（admitted request → 生成 execution candidate UI；仍不跑模型）
