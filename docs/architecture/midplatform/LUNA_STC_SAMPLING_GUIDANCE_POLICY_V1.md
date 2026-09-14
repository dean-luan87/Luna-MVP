# Luna — STC Sampling Guidance Policy v1

**Phase**：`STC-Sampling-Guidance-Policy-v1-001`

## 目的

定义 **STC 与 OCR/阅读引导** 的连接规则，固定两条触发主线（本阶段仅 policy，不执行 runtime）：

**A. Safety-triggered OCR / marker scan** — 后台默认、高优先级、短标识/图标优先，禁止默认全文 OCR。  
**B. Task-triggered OCR / confirmation scan** — 由中台任务链 + STC + 地理位置/路径进度预判，OCR 不得自主决定启动时机。

## 前置

- [LUNA_USER_GUIDANCE_RECOVERY_POLICY_V1.md](./LUNA_USER_GUIDANCE_RECOVERY_POLICY_V1.md)
- [LUNA_OCR_TASK_ORIENTED_CAPABILITY_PRINCIPLE_V0.md](../ocr/LUNA_OCR_TASK_ORIENTED_CAPABILITY_PRINCIPLE_V0.md)

## 边界

`policy_only=true`；不采样、不 OCR、不 TTS、不硬件、不调用真实地图 API、不写事实。

## 实现

- `capabilities/midplatform/stc_sampling_guidance_policy_v1.py`
- `tools/evaluation/midplatform/run_stc_sampling_guidance_policy_v1.py`
- `tools/evaluation/midplatform/verify_stc_sampling_guidance_policy_v1.py`

## 评测

[LUNA_EVALUATION_STC_SAMPLING_GUIDANCE_POLICY_V1.md](../evaluation/LUNA_EVALUATION_STC_SAMPLING_GUIDANCE_POLICY_V1.md)

## 建议下一 phase

- `Vision-Capture-Governance-v1`
- `User-Guidance-Recovery-Runtime-DryRun-v1`
