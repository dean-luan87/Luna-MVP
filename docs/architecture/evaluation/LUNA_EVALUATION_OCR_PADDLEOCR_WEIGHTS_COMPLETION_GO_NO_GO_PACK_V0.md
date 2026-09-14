# LUNA Evaluation — PaddleOCR Weights Completion Go/No-Go Pack v0

## GO

- 六个计划文件均在 repo 内存在。  
- **Weights-001 snapshot** `verdict: GO`，`missing_count=0`。  
- **Weights snapshot verifier** GO。  
- **Completion verifier**（Weights-003）`completion_verdict: GO`。  
- pinned candidate **sha256 全非空**；`runtime_default_enabled` / `mainline_provider` 仍为 **false**。  
- **无** PaddleOCR 构造、**无** OCR 推理、**无** routing 变更。

## CONDITIONAL_GO

- 权重仍缺或 sha 未齐；**缺失/missing 报告完整**；prepare 计划可执行。  
- **Completion verdict: CONDITIONAL_GO**。

## NO_GO

- **未授权**下载或 **静默**拉取。  
- 文件缺失却 **伪造** snapshot GO / pinned 完成。  
- snapshot 声称 **GO** 但 **sha256 不完整**（integrity 冲突）。  
- 调用 PaddleOCR **推理**、替换 RapidOCR、改主线 routing、将 PaddleOCR 设为 **默认** provider。
