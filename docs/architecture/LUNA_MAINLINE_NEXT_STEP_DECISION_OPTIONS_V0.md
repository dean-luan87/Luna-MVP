# LUNA Mainline — Next Step Decision Options v0

以下选项 **仅登记**，**本工具不执行**。

| Option | 名称 | 摘要 |
|--------|------|------|
| **A** | OCRBridge-Implementation-001 | `OcrEvidencePack` **shadow** 序列化绑定；仍 **不**转发 MidPlatform。 |
| **B** | VoiceInteraction-Readiness-001 | 盘点完整语音交互：ASR、多轮、语义上下文、Qianwen 主线调用缺口。 |
| **C** | PaddleOCR-Readiness-001 | PaddleOCR provider readiness + manifest；**不**替换 RapidOCR 主位。 |
| **D** | EvaluationTools-OCR-RealSamples-001 | 真实样本 + 人工标注，抬高 OCR-006 边界可信度。 |
| **E** | Mainline-IntegrationPlan-001 | YOLO / OCR / Voice 三线汇总为下一阶段 **集成路线图**。 |

**默认建议顺序（可改）**：先 **E**（路线图），再 **A**（shadow 绑定）；若语音优先级更高则 **B**。
