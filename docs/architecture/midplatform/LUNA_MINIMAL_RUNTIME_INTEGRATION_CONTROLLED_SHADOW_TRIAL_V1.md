# Luna — Minimal Runtime Integration Controlled Shadow Trial v1

**Phase**：`Minimal-Runtime-Integration-Controlled-Shadow-Trial-v1-001`  
**性质**：controlled shadow trial only；按最小 runtime 形态执行 candidate 链，但不触发真实 side effect

## 目标

验证上一阶段定义好的 minimal runtime trial contract 能否在 shadow 模式下被 runner 执行：

- 受控样本输入是否能串起最小候选链
- 各模块是否只产出 candidate / shadow decision / shadow event
- runtime / write 边界是否继续锁死
- abort 条件是否可检测
- source_chain 是否可贯穿整条链路

## 覆盖

- 8 个 controlled input cases
- 104 个 shadow execution steps
- 8 个 shadow candidate traces
- 8 个 Speech Gate shadow decisions
- 8 个 VOP shadow events
- 8 个 abort checks
- observability trace + no-runtime / no-write 双 boundary report

## 主线位置

```text
Safety-Task-Arbitration-Policy-v1
  → Voice-Command-Ownership-Gate-Policy-v1
  → Voice-Interruption-Governance-DryRun-v1
  → Basic-Navigation-Guidance-Loop-Stabilization-Test-v1
  → Minimal-Runtime-Integration-Trial-Definition-v1
  → Minimal-Runtime-Integration-Controlled-Shadow-Trial-v1
  → Minimal-Runtime-Integration-Post-Shadow-Review-v1
  → Minimal-Runtime-Integration-Controlled-Output-Definition-v1
  → Minimal-Runtime-Integration-Text-Only-Controlled-Output-Trial-v1
```

## 核心结论

- minimal runtime trial definition 已可被 shadow runner 执行
- 最小链路可生成 runtime-shaped candidate trace，而不是直接触发 runtime
- Speech Gate / VOP 只留下 shadow decision / shadow event
- non-owner block、stale safety repeat、P0 safety protection 都在 shadow 路径中被保持
- abort / boundary / observability trace 可串起完整 source_chain

## 边界

- 不接真实 camera / microphone / ASR / TTS
- 不调用真实 Speech Gate / VOP runtime
- 不调用地图 API / GPS / OCR provider / detector / segmentation / tracking
- 不提交 Task Manager / task state，不触发 navigation action，不修改 route
- 不写 Memory / WorldModel / Fact / Scene Delta

## 下一推荐 Phase

**Minimal-Runtime-Integration-Post-Shadow-Review-v1** — 已完成  
**Minimal-Runtime-Integration-Controlled-Output-Definition-v1** — 已完成  
**Minimal-Runtime-Integration-Text-Only-Controlled-Output-Trial-v1**

注意：当前阶段只是把最小闭环以影子方式跑通，**仍不是 live runtime**。  
post-shadow review 已确认该阶段可以进入 controlled output definition；该 definition 现已完成，但下一步仍然只能是 text-only controlled output trial，不是 live runtime，也不是硬件/API enablement。

## 实现

- `capabilities/midplatform/minimal_runtime_integration_controlled_shadow_trial_v1.py`
- `tools/evaluation/midplatform/run_minimal_runtime_integration_controlled_shadow_trial_v1.py`
- `tools/evaluation/midplatform/verify_minimal_runtime_integration_controlled_shadow_trial_v1.py`
