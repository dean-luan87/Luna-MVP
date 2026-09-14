# Luna — Basic Navigation Guidance Loop Stabilization Test v1

**Phase**：`Basic-Navigation-Guidance-Loop-Stabilization-Test-v1-001`  
**性质**：多治理层联合 dry-run stabilization test；不是 runtime enablement

## 目标

把以下已完成阶段接入同一个 stabilization test：

- `Basic-Navigation-Guidance-Loop-DryRun-v1`
- `Safety-Task-Arbitration-Policy-v1`
- `Voice-Command-Ownership-Gate-Policy-v1`
- `Voice-Interruption-Governance-DryRun-v1`

验证 safety / navigation / OCR / user interruption / ownership gate / priority / freshness / context preservation 是否稳定、自洽、无越权、无 runtime 副作用。

## 覆盖

- 24 个 stabilization scenarios
- 24 个 stabilization decision candidates
- 8 个 conflict / preservation / boundary matrices
- no-runtime / no-write 双 boundary report

## 主线位置

```
Safety-Task-Arbitration-Policy-v1
  → Voice-Command-Ownership-Gate-Policy-v1
  → Voice-Interruption-Governance-DryRun-v1
  → Basic-Navigation-Guidance-Loop-Stabilization-Test-v1
  → Minimal-Runtime-Integration-Trial-Definition-v1
  → Minimal-Runtime-Integration-Controlled-Shadow-Trial-v1
  → Minimal-Runtime-Integration-Post-Shadow-Review-v1
```

## 核心结论

- baseline safety loop 仍可在无任务时运行
- task-driven loop 需要 task context
- safety_active 时可 suppress/delay 低优先级 navigation / OCR / clarification / human assistance
- P0/P1 safety speech 不会被普通 interruption 取消
- ownership gate 继续拦截旁人 / 电话 / 聊天 / 外放 / 广播
- interruption 后 `task_context` / `pending_confirmation` 保留
- stale speech 不作为当前事实复述

## 边界

- 不接真实摄像头 / ASR / 录音 / 声纹 / 人脸 / 表情
- 不停止真实 TTS
- 不调用真实 Speech Gate / VOP / 地图 API / GPS runtime
- 不提交 Task Manager / Midplatform task state
- 不写 WorldModel / Memory / Fact

## 下一推荐 Phase

**Minimal-Runtime-Integration-Trial-Definition-v1** — 已完成  
**Minimal-Runtime-Integration-Controlled-Shadow-Trial-v1** — 已完成  
**Minimal-Runtime-Integration-Post-Shadow-Review-v1**

注意：本阶段仅证明 dry-run / candidate / handoff 链路稳定，**不等于真实 runtime 已启用**。

## 实现

- `capabilities/midplatform/basic_navigation_guidance_loop_stabilization_test_v1.py`
- `tools/evaluation/midplatform/run_basic_navigation_guidance_loop_stabilization_test_v1.py`
- `tools/evaluation/midplatform/verify_basic_navigation_guidance_loop_stabilization_test_v1.py`
