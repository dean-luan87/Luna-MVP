# MobileSAM Single Model Execution Integration Governance Standard V1

**Standard ID:** `MobileSamSingleModelExecutionIntegrationGovernanceStandardV1`  
**Phase:** `Phase-P1-Midplatform-Model-Test-Lens-MobileSAM-Single-Model-Execution-Integration-v1-001`

## 1. 阶段定位

Luna 从「模型治理框架」进入「真实 AI Runtime」的**第一个单模型节点**。

- **首次允许** `runner_execution = true`
- **仅限** MobileSAM
- **仅限** 测试环境（localhost 8787 / controlled trial）
- **不重构** 已冻结的六层治理链

## 2. 入口条件

| 条件 | 要求 |
|------|------|
| execution candidate | 必须存在且非 cancelled/blocked |
| admission | `admitted` at create |
| trace_chain | 完整（≥7 stages） |
| model | `mobile_sam` only |
| environment | `test_environment` only |

## 3. 禁止路径

- UI 直接调用模型（页面 `page_must_not_execute_model` 保持）  
- bypass admission  
- bypass execution candidate  
- Human Correction 直接修改模型结果  
- runner output 直写 fact  
- runner output 覆盖 segmentation boundary / attention record  

## 4. 输出治理

所有 MobileSAM 输出必须经过：

`segmentation_result_envelope` → `result_candidate` →（未来）Fact Admission

主图仅保留 Segmentation boundary + Observation marker；结果走 Result Layer。

## 5. 错误治理

异常 → `runner_error_candidate`，`runner_error_does_not_write_fact = true`。

## 6. Human Correction

- 允许：priority signal → attention boost → new task → new execution candidate → MobileSAM rerun  
- 禁止：correction → 修改 envelope / mask / segmentation label  

## 7. 继承守卫

- Constitution / Midplatform negative guard baseline  
- Visual Expression System guards  
- Followup Runner Route guards  
- Manual Trigger / Admission / Controlled Execution guards  
- `browser_runtime_guard_v1.js`  

## 8. 本阶段新增守卫

- `mobile_sam_only_runner_execution`  
- `test_environment_only`  
- `execution_candidate_required_for_runner_execution`  
- `adapter_input_normalized`  
- `runner_output_requires_envelope`  
- `runner_output_not_fact`  
- `cancelled_execution_candidate_no_runner_execution`  
- `human_correction_must_not_modify_model_result`  
- `no_execution_box_on_canvas`  
