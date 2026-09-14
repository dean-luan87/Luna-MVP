# Luna — Vision Capture Governance v1

**Phase**：`Vision-Capture-Governance-v1-001`

## 目的

在 OCR Activation 已回答「是否启动 OCR」之后，定义 **Vision Capture 输入治理**：被激活后如何获得可用输入；不达标时如何在以下路径间分流（policy only）：

1. 继续采样  
2. 请求更高质量帧  
3. 请求 zoom / autofocus / exposure / resampling（placeholder）  
4. 用户引导  
5. assisted static reading  
6. 放弃当前 OCR action  
7. expired / historical candidate  
8. 回到视觉语义主路径  

## 核心原则

- Capture governance 是**输入治理**，不是摄像头 runtime。  
- **Capture readiness ≠ OCR success**。  
- Stale capture 阻断当前 action，可进入五类长期候选（与 OCR Activation 一致）。  
- **Visual semantic remains first path**。  

## 前置

- [LUNA_OCR_ACTIVATION_GOVERNANCE_POLICY_V1.md](./LUNA_OCR_ACTIVATION_GOVERNANCE_POLICY_V1.md)
- [LUNA_STC_SAMPLING_GUIDANCE_POLICY_V1.md](./LUNA_STC_SAMPLING_GUIDANCE_POLICY_V1.md)
- [LUNA_USER_GUIDANCE_RECOVERY_POLICY_V1.md](./LUNA_USER_GUIDANCE_RECOVERY_POLICY_V1.md)

## 边界

`governance_policy_only=true`；不调用摄像头、不采新帧、不 OCR、不 TTS、不硬件、不写事实。

## 实现

- `capabilities/midplatform/vision_capture_governance_v1.py`
- `tools/evaluation/midplatform/run_vision_capture_governance_v1.py`
- `tools/evaluation/midplatform/verify_vision_capture_governance_v1.py`

## 评测

[LUNA_EVALUATION_VISION_CAPTURE_GOVERNANCE_V1.md](../evaluation/LUNA_EVALUATION_VISION_CAPTURE_GOVERNANCE_V1.md)

## 建议下一 phase

- `Vision-Capture-Runtime-GuardedTrial-v1`（Runtime DryRun v1 已完成）
- `User-Guidance-Recovery-Runtime-DryRun-v1`
- `Hardware-Camera-Control-Contract-v1`
