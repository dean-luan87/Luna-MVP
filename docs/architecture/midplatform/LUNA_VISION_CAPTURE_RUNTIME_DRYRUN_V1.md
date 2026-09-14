# Luna — Vision Capture Runtime DryRun v1

**Phase**：`Vision-Capture-Runtime-DryRun-v1-001`

## 目的

在 **Vision Capture Governance v1** 策略已定义的前提下，对当前 case 做 **受控 runtime dry-run**：模拟从 intake → readiness → capture decision 的可执行路径，**不执行**摄像头、采样、OCR、TTS、硬件或事实写入。

## 当前 case 结论（dry-run）

- **recommended_capture_decision** = `USER_GUIDANCE_OR_STATIC_CAPTURE`
- **internal_recrop_should_stop** = true
- **dynamic_reocr_allowed_now** = false

## 前置

- [LUNA_VISION_CAPTURE_GOVERNANCE_V1.md](./LUNA_VISION_CAPTURE_GOVERNANCE_V1.md)
- [LUNA_OCR_ACTIVATION_GOVERNANCE_POLICY_V1.md](./LUNA_OCR_ACTIVATION_GOVERNANCE_POLICY_V1.md)

## 边界

`runtime_dryrun_only=true`；所有 candidate 的 `runtime_action_committed=false`。

## 实现

- `capabilities/midplatform/vision_capture_runtime_dryrun_v1.py`
- `tools/evaluation/midplatform/run_vision_capture_runtime_dryrun_v1.py`
- `tools/evaluation/midplatform/verify_vision_capture_runtime_dryrun_v1.py`

## 评测

[LUNA_EVALUATION_VISION_CAPTURE_RUNTIME_DRYRUN_V1.md](../evaluation/LUNA_EVALUATION_VISION_CAPTURE_RUNTIME_DRYRUN_V1.md)

## 建议下一 phase

- `Voice-Guidance-Prompt-Template-v1`（User Guidance Recovery Runtime DryRun v1 已完成）
- `Vision-Capture-Runtime-GuardedTrial-v1`
