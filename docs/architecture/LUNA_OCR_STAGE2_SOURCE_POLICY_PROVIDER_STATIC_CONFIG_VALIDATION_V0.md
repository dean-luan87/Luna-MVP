# LUNA — OCR Stage-2 Source Policy / Provider Static Config Validation v0

## Phase

- **Phase-Mainline-GuardedTrial-009**

## Goal

在不调用任何真实 OCR provider 的前提下，完成 OCR Stage-2 的“试验材料静态校验”：

- source policy 入口与 policy id
- provider manifests（静态配置存在且可解析）
- raw_text candidate schema 合同
- fallback / not_available 策略材料
- RequestTrace/TRW 合同材料（stage mapping + shadow adapter + TRW validator）
- controlled provider runbook（**009 不允许执行**）

## Forbidden

- 禁止 provider 推理/联网/SDK 调用
- 禁止 MidPlatform / SceneDelta / WorldContextEvidence

