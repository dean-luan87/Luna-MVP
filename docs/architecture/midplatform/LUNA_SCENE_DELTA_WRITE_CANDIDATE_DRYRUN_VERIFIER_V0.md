# Luna MidPlatform — Scene Delta Write Candidate Dry-Run Verifier v0

**Phase**: `Phase-MidPlatform-Scene-Delta-Write-Candidate-DryRun-Verifier-001`

## 目的

在 **不调用 Scene Delta 执行器、不落库、不写事实层** 的前提下，对 **`scene_delta_write_candidate_from_ocr`** 及其 gate / matrix / stub audit 做 **dry-run**：输出 **字段完备性报告**、**与 Scene Delta 概念路径的映射矩阵**（仅文档化映射，不生成可执行写入载荷）、**执行前风险摘要**、以及 **no-write audit**。

## 边界

- **禁止**：真实 Scene Delta 写入、MidPlatform 事实写入、WorldModel 写入、AI 解释、OCR provider 调用、OCR routing 变更、数据库写入、外部总线调用。
- **dry-run summary** 固定：`write_would_be_allowed=false`、`executor_invoked=false`、`database_write_invoked=false`（摘要层）；**no-write audit** 中 `scene_delta_executor_invoked=false`、`dry_run_executed=true`。

## 映射矩阵语义

映射表仅说明 **OCR 候选字段** 与未来 **Scene Delta 概念槽位** 的对应关系（例如 `scene_delta.observed_text_candidate`、`scene_delta.source_region_ref` 等），**不**代表已生成生产级 Scene Delta 文档或已通过执行器校验。

## 评测入口

见 [LUNA_EVALUATION_SCENE_DELTA_WRITE_CANDIDATE_DRYRUN_VERIFIER_V0.md](../evaluation/LUNA_EVALUATION_SCENE_DELTA_WRITE_CANDIDATE_DRYRUN_VERIFIER_V0.md)。
