# Luna Voice — Guidance Prompt Runtime DryRun v1

**Phase**：`Voice-Guidance-Prompt-Runtime-DryRun-v1-001`  
**性质**：语音治理链 dry-run（`runtime_dryrun_only=true`）

## 目的

验证 OCR/阅读恢复 **prompt candidate** 如何经治理链 dry-run：

`prompt selection` → `priority arbitration` → `safety suppression` → `cooldown/repetition` → `STM mount candidate` → `SpeechRequest candidate` → `Speech Gate pre-submit`

不触发 TTS、不调用 VOP、不提交 SpeechRequest、不写 STM。

## 当前 case 结论

- **final_decision** = `GENERATE_SPEECH_REQUEST_CANDIDATE_ONLY`
- **selected_prompt** = `hold_still` / 「请先停稳，保持画面稳定。」
- **selected_priority** = `P3_OCR_GUIDANCE`
- **submit_allowed_later** = true（经 pre-submit dry-run）

## 前置

- [LUNA_VOICE_GUIDANCE_PROMPT_TEMPLATE_V1.md](./LUNA_VOICE_GUIDANCE_PROMPT_TEMPLATE_V1.md)
- [LUNA_USER_GUIDANCE_RECOVERY_RUNTIME_DRYRUN_V1.md](../midplatform/LUNA_USER_GUIDANCE_RECOVERY_RUNTIME_DRYRUN_V1.md)

## 实现（midplatform fallback）

- `capabilities/midplatform/voice_guidance_prompt_runtime_dryrun_v1.py`
- `tools/evaluation/midplatform/run_voice_guidance_prompt_runtime_dryrun_v1.py`
- `tools/evaluation/midplatform/verify_voice_guidance_prompt_runtime_dryrun_v1.py`

## 评测

- [LUNA_EVALUATION_VOICE_GUIDANCE_PROMPT_RUNTIME_DRYRUN_V1.md](../evaluation/LUNA_EVALUATION_VOICE_GUIDANCE_PROMPT_RUNTIME_DRYRUN_V1.md)

## 建议下一 phase

- Adapter 已完成：见 [LUNA_VOICE_OUTPUT_PLANE_ADAPTER_FOR_GUIDANCE_V1.md](./LUNA_VOICE_OUTPUT_PLANE_ADAPTER_FOR_GUIDANCE_V1.md)  
- `Assisted-Static-Reading-Mode-v1`
