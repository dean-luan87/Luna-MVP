# Luna OCR ROI-First Input Policy v0

**Phase**: `Phase-OCR-Input-Size-Governance-001`

## 0. 实证索引

`paddleocr_failed_sample_isolation_v0`（`size_sensitive`：`labeled_007`、`labeled_019`、`labeled_010`）表明：**缩小默认工作集（ROI）** 是降低整图 native 风险的第一道工程手段。

## 1. 实证依据

`paddleocr_failed_sample_isolation_v0`：**整图原分辨率**在多个样本上触发 **SIGSEGV** 或极端耗时。缩小输入面积是降低 native 风险的首要手段；**ROI-first** 将默认工作集限制在可控区域。

## 2. 策略

1. **实时路径**：`roi_first_required=true`（见配置）；若无可靠 ROI，须走 **显式全图降级**（用户确认 / async / evaluation），且仍受 **像素预算** 约束。  
2. ROI 来源：应用层 bbox、上一帧跟踪、STCM 给出的空间锚点等；**不得**伪造 ROI 以绕过 Gate。  
3. 多 ROI：按 orchestrator 优先级调度；每个 ROI 单独过 Gate 与预算。  
4. **reading_order**：不得在**低置信**时强行推断全局阅读顺序；须在 evidence 中标注不确定性（与 tiling 文档一致）。

## 3. 禁止

- 默认把「整张大图」作为实时 OCR 的首发路径。  
- 无 ROI 且无用户/策略授权的全图实时 OCR。
