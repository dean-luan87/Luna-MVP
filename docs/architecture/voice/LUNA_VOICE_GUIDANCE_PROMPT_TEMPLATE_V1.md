# Luna Voice — Guidance Prompt Template v1

**Phase**：`Voice-Guidance-Prompt-Template-v1-001`  
**性质**：模板与语音治理接口定义（`template_only=true`）

## 目的

定义 OCR / 阅读恢复类 **语音提示模板**、**语音优先级**、**短期记忆挂载 contract**、**用户问询复述规则** 与 **Voice Output Plane 未来 adapter**；提示必须经既有 Voice Output / Speech Gate，**不得绕过**。

## 核心原则

1. Prompt template ≠ TTS；prompt candidate ≠ SpeechRequest  
2. OCR guidance = `P3_OCR_GUIDANCE`；安全播报 `P0_SAFETY_CRITICAL` 永远优先  
3. 用户主动问询时可复述，依赖短期记忆 contract  
4. 本阶段不触发 TTS、不调用 VOP、不提交 SpeechRequest  

## 语音治理集成（只读引用）

- `docs/architecture/voice/LUNA_VOICE_PRE_SUBMIT_ADMISSION_LAYER_V0.md`  
- `docs/architecture/voice/LUNA_VOICE_MAINLINE_BASELINE.md`  
- `docs/architecture/LUNA_VOICE_OUTPUT_PRIORITY_EXPIRY_SUPPRESSION_POLICY_V0.md`  
- `docs/architecture/LUNA_NAVIGATION_OUTPUT_PRIORITY_AND_SUPPRESSION_POLICY_V0.md`  

## 当前 case（dry-run）

- **selected_primary_prompt** = `hold_still`  
- **selected_prompt_text** = 「请先停稳，保持画面稳定。」  
- **selected_priority** = `P3_OCR_GUIDANCE`  

## 实现位置（future relocation）

- Capability：`capabilities/midplatform/voice_guidance_prompt_template_v1.py` → 未来 `capabilities/voice/`  
- Runner / Verifier：`tools/evaluation/midplatform/` → 未来 `tools/evaluation/voice/`  

## 评测

- [LUNA_EVALUATION_VOICE_GUIDANCE_PROMPT_TEMPLATE_V1.md](../evaluation/LUNA_EVALUATION_VOICE_GUIDANCE_PROMPT_TEMPLATE_V1.md)  
- [LUNA_EVALUATION_VOICE_GUIDANCE_PROMPT_TEMPLATE_V1_GO_NO_GO_PACK_V0.md](../evaluation/LUNA_EVALUATION_VOICE_GUIDANCE_PROMPT_TEMPLATE_V1_GO_NO_GO_PACK_V0.md)  

## 前置

- [LUNA_USER_GUIDANCE_RECOVERY_RUNTIME_DRYRUN_V1.md](../midplatform/LUNA_USER_GUIDANCE_RECOVERY_RUNTIME_DRYRUN_V1.md)

## 建议下一 phase

- Runtime dry-run 已完成：见 [LUNA_VOICE_GUIDANCE_PROMPT_RUNTIME_DRYRUN_V1.md](./LUNA_VOICE_GUIDANCE_PROMPT_RUNTIME_DRYRUN_V1.md)  
- `Voice-Output-Plane-Adapter-for-Guidance-v1`
