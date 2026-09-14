# Luna — Minimal Runtime Integration Trial Definition v1

**Phase**：`Minimal-Runtime-Integration-Trial-Definition-v1-001`  
**性质**：definition only；定义最小 runtime integration trial 边界；不执行 runtime

## 目标

定义 Luna 一期最小 runtime trial 的：

- 允许模块
- shadow-only 模块
- 禁止模块
- 输入 / 输出计划
- safety envelope
- abort / rollback 机制
- observability 要求
- GO / NO-GO 标准

## 结论

本阶段**不是** runtime enablement。  
本阶段只定义后续 controlled shadow trial 的入口、边界和中止条件。  
其后续 `Minimal-Runtime-Integration-Controlled-Shadow-Trial-v1` 已按 shadow 模式验证定义合同可落地。

## 未来最小 trial 主链

```
controlled sample input / stub frame
  → basic navigation / OCR / safety candidate generation
  → safety-task arbitration
  → speech candidate
  → speech gate shadow
  → VOP shadow / controlled output placeholder
  → structured logging / boundary / abort checks
```

## 当前明确禁止

- 真实 camera / microphone / ASR / TTS
- 真实 Speech Gate / VOP runtime
- 真实地图 / 高德 / GPS runtime
- 真实 OCR provider
- Task Manager commit / navigation action execution / route modification
- WorldModel / Memory / Fact / Scene Delta write
- 声纹 / 人脸 / 表情 runtime

## 下一推荐 Phase

**Minimal-Runtime-Integration-Controlled-Shadow-Trial-v1** — 已完成  
**Minimal-Runtime-Integration-Post-Shadow-Review-v1** — 已完成  
**Minimal-Runtime-Integration-Controlled-Output-Definition-v1**

注意：本阶段本身仍然只是定义，不执行。  
真实 live runtime 仍未开启；当前主线已完成 post-shadow review，下一步也只能进入 controlled output definition，而不是直接接入真实硬件或外部 API。

## 实现

- `capabilities/midplatform/minimal_runtime_integration_trial_definition_v1.py`
- `tools/evaluation/midplatform/run_minimal_runtime_integration_trial_definition_v1.py`
- `tools/evaluation/midplatform/verify_minimal_runtime_integration_trial_definition_v1.py`
