# LUNA Mainline — Integration Plan v0 (Phase-Mainline-IntegrationPlan-001)

## 目的

在 **StatusReview-001** 已澄清各域状态后，**冻结下一阶段主线执行顺序**与 **选项边界**，避免 OCR / Voice / OCRBridge / Evaluation 各线无序穿插。

## 边界（硬）

- **仅**路线图与策略文档；**不**实现功能、**不**接 runtime、**不**调 provider。  
- **不**接 MidPlatform / 白盒 / SceneDelta / WorldContext；**不**改 OCR routing。

## 默认执行顺序（冻结建议）

1. **E** — 本阶段：集成计划冻结（当前文档 + 工具产物）。  
2. **B** — `VoiceInteraction-Readiness-001`：完整语音交互主链 readiness。  
3. **A** — `OCRBridge-Implementation-001` **shadow**：证据包序列化绑定；**暂缓**至 B 之后（MidPlatform 接收策略未落地前避免为接线而接线）。  
4. **D** — `EvaluationTools-OCR-RealSamples-001`：可与 B 并行设计，**不抢**主线资源。  
5. **C** — `PaddleOCR-Readiness-001`：增强项置后；**不**替换 RapidOCR 主位。

## 工具

- `tools/run_mainline_integration_plan_v0.py`  
- `tools/verify_mainline_integration_plan_v0.py`

## 结论（产品层）

**先 E，再 B，A 暂缓**；C/D 按上列优先级与并行策略执行。
