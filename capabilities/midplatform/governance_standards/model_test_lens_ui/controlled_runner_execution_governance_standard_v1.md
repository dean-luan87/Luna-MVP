# Controlled Runner Execution Governance Standard V1

**Standard ID:** `ControlledRunnerExecutionGovernanceStandardV1`  
**Phase:** `Phase-P1-Midplatform-Model-Test-Lens-Detection-OCR-Controlled-Runner-Execution-Planning-v1-001`

## 定位

规划从 **admitted `runner_invocation_request`** 到 **`controlled_runner_execution_candidate`** 的受控执行链路。本阶段终点为 execution candidate，不是 runner 执行。

## 五层关系

| 层 | 语义 |
|----|------|
| `runner_task_candidate` | 可以考虑做什么 |
| `runner_invocation_request` | 准备申请执行什么 |
| `runner_invocation_admission` | 是否允许进入执行准备 |
| `controlled_runner_execution_candidate` | 准备如何受控执行 |
| `runner_execution` | 真正跑模型（本阶段禁止） |

## Schema 注册

| Schema | Path |
|--------|------|
| Execution Candidate | `schemas/controlled_runner_execution/controlled_runner_execution_candidate_schema_v1.json` |
| Detection Input | `schemas/controlled_runner_execution/detection_controlled_execution_input_policy_v1.json` |
| OCR Input | `schemas/controlled_runner_execution/ocr_controlled_execution_input_policy_v1.json` |
| Output Envelope | `schemas/controlled_runner_execution/runner_output_envelope_policy_v1.json` |
| Error Policy | `schemas/controlled_runner_execution/runner_error_policy_v1.json` |

## 核心边界

- **admitted request** 是生成 execution candidate 的唯一入口  
- **execution candidate ≠ runner execution**  
- **runner output ≠ fact** — 须经 fact admission  
- **错误 → runner_error_candidate**，不写 fact  
- **主图不新增 execution box**

## Negative Guards

`no_runner_execution`, `execution_candidate_not_runner_execution`, `execution_candidate_requires_admitted_request`, `runner_output_requires_envelope`, `runner_output_requires_fact_admission_before_fact_write`, `runner_error_does_not_write_fact`, `no_visual_expression_mutation`, `no_execution_box_on_canvas`, `browser_runtime_guard_inherited`
