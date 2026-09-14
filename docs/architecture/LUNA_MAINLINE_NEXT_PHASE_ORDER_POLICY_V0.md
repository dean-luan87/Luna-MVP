# LUNA Mainline — Next Phase Order Policy v0

## 冻结原则

1. **无路线图不扩音**：未冻结集成顺序前，不把 **Voice** 或 **OCRBridge** 的接线范围随意扩大。  
2. **语音缺口优先于 Bridge 接线**：完整语音交互当前为 **主线完整性大缺口**（StatusReview 登记）。  
3. **Bridge 深设计 ≠ 立即接线**：OCRBridge 设计/RFC 已完成，**真实 implementation** 依赖 MidPlatform **接收策略** phase；默认 **shadow** 仍排在 **B** 之后。  
4. **增强不打断主线**：PaddleOCR、真实样本补全 **不得**打断 E→B 主轴。

## 变更机制

若需调整顺序，须 **ADR** 说明对 MidPlatform、语音缺口与 OCR 证据链的影响；**不得**口头绕过冻结矩阵。
