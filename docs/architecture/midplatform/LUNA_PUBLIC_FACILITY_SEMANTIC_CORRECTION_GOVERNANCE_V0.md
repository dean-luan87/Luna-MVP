# Luna — Public Facility Semantic Correction Governance v0

**Phase**：`Phase-PublicFacility-Semantic-Correction-Governance-001`

## 判断

公共设施类图像**不应默认进入 OCR 主链**。核心价值是**设施语义**（电梯、出口、洗手间等），而非读出错别字。

## 证据分流

| 优先 | 类型 |
|------|------|
| 主链 | PublicFacilityEvidence、FacilitySemanticCandidate、VisualSymbolEvidence |
| 辅助 | OCRTextEvidence（仅 auxiliary） |

## 纠错三档 + 中台裁决

1. **L1** 规则/词典（EXIT、Toilet、Elevator…）
2. **L2** 设施语义库（图标 + 场景 + POI）
3. **L3** 模型纠错候选（仅 candidate，不定事实）

中台混合裁决：规则保稳定、模型保召回、中台管边界与是否可播报。`raw_ocr_text` 必须保留。

## 与 Poster 线并列

| 线 | 策略 |
|----|------|
| Poster / 广告 | segment_first → 区域 OCR |
| Public Facility | semantic_first → OCR 辅助 |

## 评测

[LUNA_EVALUATION_PUBLIC_FACILITY_SEMANTIC_CORRECTION_GOVERNANCE_V0.md](../evaluation/LUNA_EVALUATION_PUBLIC_FACILITY_SEMANTIC_CORRECTION_GOVERNANCE_V0.md)

## 建议下一跳

**PublicFacility Runtime DryRun** 已完成（见 [LUNA_PUBLIC_FACILITY_RUNTIME_DRYRUN_V0.md](./LUNA_PUBLIC_FACILITY_RUNTIME_DRYRUN_V0.md)）。后续：Benchmark Collector Real Values Smoke 或 facility metrics 字段扩展。
