# Luna Voice — Output Plane Adapter for Guidance v1

**Phase**：`Voice-Output-Plane-Adapter-for-Guidance-v1-001`  
**性质**：Adapter dry-run only（`adapter_dryrun_only=true`）

## 目的

定义并 dry-run **Guidance Prompt → Voice Output Plane** 适配：

- `adapter mapping contract`（prompt_text → speech_text 等）
- `adapter payload candidate`
- `SpeechRequest payload candidate`
- `Speech Gate admission dry-run`
- `VOP submit dry-run`（延后，不调用）

## 当前 case

- **speech_text** = 「请先停稳，保持画面稳定。」
- **priority** = `P3_OCR_GUIDANCE`
- **admission_decision** = `ADMIT_AS_CANDIDATE`
- **final_decision** = `READY_FOR_FUTURE_VOP_SUBMIT`

## 边界

不调用 VOP、不提交 SpeechRequest、不 TTS、不写 STM。

## 前置

- [LUNA_VOICE_GUIDANCE_PROMPT_RUNTIME_DRYRUN_V1.md](./LUNA_VOICE_GUIDANCE_PROMPT_RUNTIME_DRYRUN_V1.md)
- [LUNA_VOICE_GUIDANCE_PROMPT_TEMPLATE_V1.md](./LUNA_VOICE_GUIDANCE_PROMPT_TEMPLATE_V1.md)

## 实现（midplatform fallback）

- `capabilities/midplatform/voice_output_plane_adapter_for_guidance_v1.py`
- `tools/evaluation/midplatform/run_voice_output_plane_adapter_for_guidance_v1.py`
- `tools/evaluation/midplatform/verify_voice_output_plane_adapter_for_guidance_v1.py`

## 评测

[LUNA_EVALUATION_VOICE_OUTPUT_PLANE_ADAPTER_FOR_GUIDANCE_V1.md](../evaluation/LUNA_EVALUATION_VOICE_OUTPUT_PLANE_ADAPTER_FOR_GUIDANCE_V1.md)

## 建议下一 phase

- Assisted Static Reading Mode 已完成：见 [LUNA_ASSISTED_STATIC_READING_MODE_V1.md](../midplatform/LUNA_ASSISTED_STATIC_READING_MODE_V1.md)  
- `Assisted-Static-Reading-Runtime-DryRun-v1`

## 与 Controlled Output Definition 的关系

该 adapter dry-run 合同为 `Minimal-Runtime-Integration-Controlled-Output-Definition-v1` 提供 VOP 输入侧参考。  
当前仍然只允许 candidate / shadow / text-only planning，不允许真实 VOP submit、真实 TTS 或真实音频播放。
