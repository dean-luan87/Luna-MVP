# Luna — GO/NO_GO: Vision ROI Text-Bearing OCR Sample v0

**Phase**：`Phase-Vision-ROI-Text-Bearing-Sample-For-OCR-001`

## GO

- text-bearing ROI 经 OCR bridge 提交 RapidOCR；
- `text_joined` 非空、`empty_text=false`；
- reference-only candidate 生成；
- audit 边界完整；`verifier=GO`。

## CONDITIONAL_GO

- RapidOCR 路径执行但 `text_joined` 仍为空；
- fixture 不稳定但错误记录完整；
- 无越界行为。

## NO_GO

- 绕过 OCR bridge 直调 RapidOCR；
- 启用 PaddleOCR / 融合 / 写事实层 / 导航；
- audit 缺失或边界违反。
