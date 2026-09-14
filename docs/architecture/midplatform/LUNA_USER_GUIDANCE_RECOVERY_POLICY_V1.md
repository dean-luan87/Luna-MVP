# Luna — User Guidance Recovery Policy v1

**Phase**：`User-Guidance-Recovery-Policy-v1-001`

## 目的

在 OCR v1/v2 全 empty、bridge 可达的前提下，**只定义** OCR 动态阅读失败后的用户引导恢复策略：输入达标范围、失败原因分类、可修复性、用户/系统/外部援助动作候选与硬件预留；**不**执行 TTS、硬件、OCR 或 runtime action。

## 架构原则

- [LUNA_OCR_TASK_ORIENTED_CAPABILITY_PRINCIPLE_V0.md](../ocr/LUNA_OCR_TASK_ORIENTED_CAPABILITY_PRINCIPLE_V0.md)
- 前置：[LUNA_OCRREQUEST_GATED_SUBMISSION_FROM_MULTIFRAME_V2.md](../ocr/LUNA_OCRREQUEST_GATED_SUBMISSION_FROM_MULTIFRAME_V2.md)

## 边界

- `policy_only=true`；`threshold_is_policy_placeholder=true`
- 禁止：TTS、用户引导执行、硬件、OCR、crop、EP、Semantic、SV、事实写入

## 实现

- `capabilities/midplatform/user_guidance_recovery_policy_v1.py`
- `tools/evaluation/midplatform/run_user_guidance_recovery_policy_v1.py`
- `tools/evaluation/midplatform/verify_user_guidance_recovery_policy_v1.py`

## 评测

[LUNA_EVALUATION_USER_GUIDANCE_RECOVERY_POLICY_V1.md](../evaluation/LUNA_EVALUATION_USER_GUIDANCE_RECOVERY_POLICY_V1.md)

## 建议下一 phase

- [LUNA_STC_SAMPLING_GUIDANCE_POLICY_V1.md](./LUNA_STC_SAMPLING_GUIDANCE_POLICY_V1.md)（已完成：安全/任务双触发 STC 策略）
- `Vision-Capture-Governance-v1`
- `User-Guidance-Recovery-Runtime-DryRun-v1`
- `Vision-Capture-Governance-v1`
