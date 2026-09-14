# LUNA Mainline — Option Comparison Matrix v0

| ID | 名称 | 目标 | 主要限制 | 默认优先级 |
|----|------|------|------------|------------|
| **E** | Mainline-IntegrationPlan-001 | 统一下一阶段顺序与禁止项 | planning_only | 1 |
| **B** | VoiceInteraction-Readiness-001 | 语音主链 readiness | 未签 readiness 前不接全链 | 2 |
| **A** | OCRBridge-Implementation-001 shadow | Shadow 序列化绑定 | 不 forward MidPlatform；不写事实层 | 3 |
| **D** | EvaluationTools-OCR-RealSamples-001 | 真实样本 + 标注 | evaluation_only | 4 |
| **C** | PaddleOCR-Readiness-001 | Paddle 中文增强 readiness | 不替换 RapidOCR 主位 | 5 |

机器可读：`mainline_option_comparison_matrix.json`（由 `run_mainline_integration_plan_v0.py` 生成）。
