# LUNA — MidPlatform OCR Bridge Future Branches v0

## Phase

- **Phase-ModelOCR-MidPlatform-Bridge-003**

## Purpose

列出 Bridge `closed_v0` 之后的可选分支，避免在 closure 阶段引入新功能或误触 runtime。

## Candidate future branches（仅列举，不进入）

1. **Real MidPlatform readiness**
   - 真实中台接线 readiness gate（仍需严格边界与回滚）
2. **Scene delta control implementation**
   - `SceneInformationDeltaControl` 正式实现与窗口策略
3. **World context evidence write readiness**
   - `WorldContextEvidence` 从 candidate-only 走向可控写入（需 revalidation 与 trust）
4. **Task relevance classifier upgrade**
   - 从 placeholder/keyword/hint 走向可评测的 relevance classifier
5. **Commercial / ambient enrichment evaluator**
   - ambient 输出的上下文匹配、抑制、TTL 与 speech 政策完善
6. **Low-value uncertainty recheck loop**
   - `requires_better_frame` 驱动的复核闭环（不强行解释）
7. **Visual symbol evidence bridge**
   - 与 `Phase-WorldModel-VisualSymbolEvidence-*` 的桥接（符号证据并行分支）
8. **Hive evidence pack future branch**
   - 共享证据包/隐私边界/可分享策略（目前冻结为 shareable=false）

