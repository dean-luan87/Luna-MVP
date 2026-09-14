# LUNA Mainline — Integration Dependency Matrix v0

## 语义边（摘要）

- **E → B**：先冻结顺序，再展开语音 readiness（避免结构散掉）。  
- **E → A**：先冻结顺序，再进入 OCRBridge shadow（避免「为接线而接线」）。  
- **MidPlatform 接收 OcrEvidencePack（未来 phase）→ A 的 forward**：真实转发的前置；**shadow A** 不依赖生产 MidPlatform，但 **forward** 必须依赖。  
- **D → OCR-006**：强化边界可信度；可与 B **并行规划**，不抢占 E/B 执行带宽。  
- **C → OCR-012**：不得破坏 RapidOCR 主 provider 地位。

完整边表：`mainline_dependency_matrix.json`。
