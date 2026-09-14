# MobileSAM Single Model Execution Integration Plan V1

**Phase:** `Phase-P1-Midplatform-Model-Test-Lens-MobileSAM-Single-Model-Execution-Integration-v1-001`  
**System ID:** `LunaModelTestLensMobileSAMSingleModelExecutionIntegrationV1`  
**Status:** Integration Planning + Controlled Execution（本阶段**首次允许** `runner_execution`，但**仅限 MobileSAM**、**仅限测试环境**）

## 上游冻结（全部 GO，不再改治理架构）

```
Observation → Attention → Task Candidate → Invocation Request
    → Admission → Execution Candidate → [本阶段] Runner Execution
    → Result Envelope → Fact Admission（暂不自动）
```

- Detection/OCR Controlled Runner Execution UI Execution = GO  
- Local Runner Bridge Service Skeleton（8787）= GO  
- MobileSAM real local image inference trial = GO  
- Visual Expression System 冻结  
- Human Correction = priority signal only  

**本阶段不重构治理链，只补最后一段：Execution Candidate → Runner Sandbox → MobileSAM → Result Envelope。**

## 为什么先接 MobileSAM

MobileSAM 是当前链路最完整的单模型：

- segmentation region / mask / region_id  
- model_test_result_envelope  
- Observation Attention / Visual Expression  
- Task Candidate / Route / Admission / Execution Candidate（可扩展至 Segmentation rerun）  
- Local Runner Bridge + `mobilesam_image_runner_v1` + envelope adapter  

适合验证：**中台是否真的可以控制一个模型**，而不是页面直接调模型。

## 完整执行链路（本阶段钉死）

```
controlled_runner_execution_candidate
  (execution_status: ready_for_execution_review | planned_only)
        ↓
Runner Sandbox（仅 MobileSAM · 仅测试环境 · 须 trace）
        ↓
Model Adapter Input（image_ref + region_ref + task_type + constraints + trace_chain）
        ↓
MobileSAM Adapter（mobilesam_runner_to_envelope_adapter_v1）
        ↓
MobileSAM Inference（mobilesam_image_runner_v1 · 8787 或受控 Python 入口）
        ↓
segmentation_result_envelope
        ↓
result_candidate（candidate_only · needs_fact_admission）
        ↓
UI Result Layer / Future Fact Admission（本阶段不自动写 fact）
```

## 1. Model Adapter

中台与模型之间的适配层。**禁止**把内部 store 对象直接丢给 runner。

### 标准输入（`model_adapter_input_schema_v1.json`）

```json
{
  "image_ref": "local-file://...",
  "region_ref": "region://entity_023",
  "task_type": "segmentation",
  "model_id": "mobile_sam",
  "constraints": {
    "candidate_only": true,
    "no_fact_write": true,
    "no_navigation_decision": true
  },
  "trace_chain": [ "...完整治理链..." ],
  "source_execution_candidate_id": "crec_segmentation_..."
}
```

### 禁止

- 直接传递 `requestStore` / `executionStore` 内部对象  
- 输入含 fact label / confirmed object / navigation context  
- 无 trace_chain 的 adapter 调用  

## 2. Runner Sandbox

**第一次** `runner_execution = true`，但必须受限：

| 允许 | 禁止 |
|------|------|
| 仅 `model_id = mobile_sam` | Detection / OCR / Depth / Tracking |
| 仅 `test_environment`（localhost 8787 或受控 trial） | 生产 runtime / 外网 |
| 仅 `controlled_runner_execution_candidate` 来源 | UI 直接调用模型 |
| 必须带完整 `trace_chain` | bypass admission |
| execution_status 非 cancelled/blocked | bypass execution candidate |
| 输出必须经 envelope | runner output 直写 UI / fact |

### 拒绝场景

- Execution Candidate `cancelled` / `blocked` → **no runner execution**  
- Admission 非 admitted → **no runner execution**  
- trace_chain 不完整 → **runner_error_candidate**  

## 3. Output Envelope

MobileSAM 输出**不能**直接回主图 segmentation layer 或写 fact。

```
MobileSAM raw output
    ↓
segmentation_result_envelope
    ↓
result_candidate
    ↓
Result Layer（右侧结果候选区）/ Future Fact Admission
```

### 示例字段

```json
{
  "envelope_type": "segmentation_result_envelope",
  "source_model": "MobileSAM",
  "model_version": "...",
  "source_runner_execution_id": "rex_mobile_sam_...",
  "source_execution_candidate_id": "crec_...",
  "region_id": "entity_023",
  "mask_ref": "artifact://...",
  "confidence": 0.92,
  "candidate_only": true,
  "not_fact": true,
  "needs_fact_admission": true
}
```

### 禁止

- runner output 直写 fact  
- runner output 覆盖 Observation Attention record  
- runner output 覆盖 segmentation boundary owner  
- 主图新增 execution box / detection preview（`no_execution_box_on_canvas`）

## 4. 错误隔离

模型异常必须进入 `runner_error_candidate`，不得污染事实层：

| 错误类型 | 示例 |
|----------|------|
| `timeout` | 推理超时 |
| `runner_unavailable` | 8787 未启动 |
| `invalid_crop` | region crop 无效 |
| `empty_mask_output` | 输出空 mask |
| `schema_validation_failed` | envelope schema 不匹配 |
| `execution_cancelled` | candidate 已取消仍尝试执行 |
| `trace_chain_incomplete` | trace 断裂 |
| `sandbox_policy_violation` | 非 MobileSAM / 非测试环境 |

## 5. Human Correction 验证

### 正确链路

```
Human Correction（priority signal）
    ↓
Observation Attention boost
    ↓
new task candidate
    ↓
new invocation request → admission → execution candidate
    ↓
MobileSAM rerun（新 execution，非修改旧结果）
```

### 错误链路（禁止）

```
Human Correction → 直接修改模型结果 / envelope / segmentation label
```

## 6. 验证场景（Integration 阶段）

### 正常路径

Pinned Task → Request → Admission → Execution Candidate → Sandbox → MobileSAM → Result Envelope

### 拒绝路径

- cancelled execution candidate → no runner execution  
- rejected admission → no sandbox entry  

### 异常路径

- 空 mask / 超时 / schema 不匹配 → runner_error_candidate  

## 7. 产出文件

| 文件 | 用途 |
|------|------|
| `mobile_sam_single_model_execution_integration_plan_v1.md` | 本文件 |
| `mobile_sam_single_model_execution_integration_types_v1.py` | 常量与边界 |
| `runner_sandbox/runner_sandbox_v1.py` | 沙箱入口（受控执行） |
| `schemas/.../model_adapter_input_schema_v1.json` | Adapter 输入 |
| `schemas/.../runner_sandbox_policy_v1.json` | 沙箱策略 |
| `schemas/.../segmentation_result_envelope_schema_v1.json` | 输出 envelope |
| `schemas/.../mobile_sam_controlled_execution_input_policy_v1.json` | MobileSAM 输入边界 |
| `governance_standards/.../mobile_sam_single_model_execution_integration_governance_standard_v1.md` | 治理标准 |
| `review_model_test_lens_mobile_sam_single_model_execution_integration_planning_v1.py` | Planning review |

## 8. 本阶段不做

- 不接 Detection / OCR / Depth / Tracking  
- 不自动 Fact Admission  
- 不改 Observation Attention priority 计算  
- 不改 Visual Expression segmentation boundary owner  
- 不做多模型协同调度  
- 页面内不执行模型（仍走 8787 / Python sandbox）  

## 9. 下一阶段

`Phase-P1-Midplatform-Single-Model-Interaction-Validation-v1-001`  
验证中台能否根据模型结果重新调度模型。

再之后：MobileSAM + Detection + OCR + Depth + Tracking 多模型协同。
