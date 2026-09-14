# Luna — Basic Functional Loop Runtime Logic Audit and Correction v1

**Phase**：`Basic-Functional-Loop-Runtime-Logic-Audit-and-Correction-v1-001`  
**性质**：audit / correction / governance only；**非** runtime

## 双链结构

| 链路 | 触发条件 | 目的 |
|------|----------|------|
| **Baseline Safety Loop** | 无任务 / 无目标 | 安全视觉、风险感知、有限安全 OCR、安全语音候选 |
| **Task-Driven Loop** | 有任务 / 目标 / 用户意图 | 目标化观察、OCR、人工协助、导航提示 |

无任务时底层能力（视觉/OCR 等）仍以 **baseline** 模式工作，用于安全保障；**不得**执行目标任务或 generic text OCR。

## 本阶段修正项

1. Baseline vs Task-Driven 分流  
2. Task-Aware Scheduling → **Observation Request** 缺口与 stub  
3. Vision evidence lifecycle  
4. OCR joint gate  
5. Speech output path（Speech Gate → VOP）  
6. Safety vs Task arbitration  
7. Navigation guidance vs action 边界  
8. Information lifecycle 缺口登记  
9. Memory system 边界 deferred  

## 下一推荐 Phase

**Task-Observation-Request-Contract-v1** — 已完成（见 `LUNA_TASK_OBSERVATION_REQUEST_CONTRACT_V1.md`）  
**Vision-OCR-Evidence-Ingest-Integration-Check-v1** — 下一集成检查

## 实现

- `capabilities/midplatform/basic_functional_loop_runtime_logic_audit_correction_v1.py`
- `tools/evaluation/midplatform/run_basic_functional_loop_runtime_logic_audit_correction_v1.py`
- `tools/evaluation/midplatform/verify_basic_functional_loop_runtime_logic_audit_correction_v1.py`
