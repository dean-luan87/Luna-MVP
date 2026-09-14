# STC Sampling Guidance Policy v1 GO/NO_GO Pack v0

## GO

- Safety + Task 双触发策略；geolocation/route pre-activation；validity/stale/retry/motion/static/dynamic scope
- OCR Activation + Vision Capture governance link
- 不采样、不 OCR、不 TTS、不硬件、不地图 API

## CONDITIONAL_GO

- 距离/时间窗口为 placeholder；未执行 runtime sampling

## NO_GO

- 运行 OCR / TTS / 硬件 / 真实地图 API / 写事实 / routing 变更
