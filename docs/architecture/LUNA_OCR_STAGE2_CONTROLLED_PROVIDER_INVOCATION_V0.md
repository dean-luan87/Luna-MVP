# LUNA — OCR Stage-2 Controlled Provider Invocation v0

## Phase

- **Phase-Mainline-GuardedTrial-011**

## Goal

在 **Phase-010 approval gate=GO** 的前提下，允许一次最小真实 OCR provider 调用：

- 单张冻结 input image → raw_text candidate
- 仅写 TRW（trace/replay/whitebox）与 post-trial report

## Hard boundaries

- 禁止 `semantic_interpretation_enabled=true`
- 禁止 MidPlatform / SceneDelta / WorldContextEvidence
- 禁止 SceneTask/Fusion/Output
- 禁止 navigation / TTS / Qwen / world write / hive upload
- 禁止 camera / video stream
- 禁止真实网络请求（如 provider 需要网络 → fallback/not_available）

## Tools

- `tools/run_ocr_stage2_controlled_provider_trial_v0.py`
- `tools/verify_ocr_stage2_controlled_provider_trial_v0.py`

