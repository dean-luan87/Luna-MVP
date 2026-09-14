# Vision Capture Runtime DryRun v1 GO/NO_GO Pack v0

## GO

- 当前 case intake + readiness + decision trace
- final decision = USER_GUIDANCE_OR_STATIC_CAPTURE
- internal_recrop_should_stop=true；不继续 dynamic re-OCR
- 无 camera/OCR/TTS/hardware/fact write

## CONDITIONAL_GO

- 部分 upstream 缺失但有 missing 记录；仅 candidate dry-run

## NO_GO

- 摄像头/新帧/OCR/TTS/硬件/写 WM/SceneDelta/routing 变更/benchmark claim
