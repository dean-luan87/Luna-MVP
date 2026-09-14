# Luna — User Guidance Recovery Runtime DryRun v1

**Phase**：`User-Guidance-Recovery-Runtime-DryRun-v1-001`

## 目的

将 Vision Capture Runtime 的 `USER_GUIDANCE_OR_STATIC_CAPTURE` 转为 **guidance plan**、**prompt candidates**、**response state transitions** 与升级候选（static / system / external / fallback / long-term），**不执行** TTS、Voice Output Plane、真实引导、摄像头、OCR 或硬件。

## 当前 case 结论（dry-run）

- **selected_primary_path** = `ASSISTED_STATIC_CAPTURE_GUIDANCE`
- **internal_recrop_should_stop** = true
- **recommended_next_phase** = `Voice-Guidance-Prompt-Runtime-DryRun-v1`（模板阶段已完成：见 [LUNA_VOICE_GUIDANCE_PROMPT_TEMPLATE_V1.md](../voice/LUNA_VOICE_GUIDANCE_PROMPT_TEMPLATE_V1.md)）

## 前置

- [LUNA_VISION_CAPTURE_RUNTIME_DRYRUN_V1.md](./LUNA_VISION_CAPTURE_RUNTIME_DRYRUN_V1.md)
- [LUNA_USER_GUIDANCE_RECOVERY_POLICY_V1.md](./LUNA_USER_GUIDANCE_RECOVERY_POLICY_V1.md)

## 边界

`runtime_dryrun_only=true`；`runtime_tts_invoked=false`；`voice_output_plane_invoked=false`。

## 实现

- `capabilities/midplatform/user_guidance_recovery_runtime_dryrun_v1.py`
- `tools/evaluation/midplatform/run_user_guidance_recovery_runtime_dryrun_v1.py`
- `tools/evaluation/midplatform/verify_user_guidance_recovery_runtime_dryrun_v1.py`

## 评测

[LUNA_EVALUATION_USER_GUIDANCE_RECOVERY_RUNTIME_DRYRUN_V1.md](../evaluation/LUNA_EVALUATION_USER_GUIDANCE_RECOVERY_RUNTIME_DRYRUN_V1.md)
