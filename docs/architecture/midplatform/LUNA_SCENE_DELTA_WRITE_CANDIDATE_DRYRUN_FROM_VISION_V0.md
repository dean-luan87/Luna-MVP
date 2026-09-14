# Luna MidPlatform — Scene Delta Write Candidate Dry-Run from Vision v0

**Phase**：`Phase-MidPlatform-Scene-Delta-Write-Candidate-DryRun-Verifier-From-Vision-001`

## 目的

在 **不调用 Scene Delta 执行器、不落库、不写事实层** 的前提下，对 **`scene_delta_write_candidate_from_vision`** 及其 **Vision evidence 矩阵**、**gate stub**、**Vision audit** 做 **dry-run**：输出 **字段完备性报告**、**Vision → Scene Delta 概念路径映射矩阵**（仅文档化映射，不生成可执行写入载荷）、**风险摘要**、以及 **no-write audit**。

## 前置（须均为 GO）

- `Phase-MidPlatform-Scene-Delta-Write-Candidate-From-Vision-Ingest-Stub-001`  
- `Phase-Vision-Ingest-to-Product-Bus-ReadOnly-Replay-001`  
- `Phase-MidPlatform-Vision-Recognition-Evidence-ReadOnly-Ingest-Candidate-001`  

## 边界

- **禁止**：真实 Scene Delta 写入、MidPlatform 事实写入、WorldModel 写入、AI 解释、导航决策、真实视觉 / YOLO / Supervision 主线 / VLM / OCR、数据库写入、外部总线调用。  
- **dry-run summary**：`schema_version=scene_delta_write_candidate_dryrun_from_vision_summary_v0`；固定 **`write_would_be_allowed=false`**、**`executor_invoked=false`**、**`database_write_invoked=false`**。  
- **no-write audit**：`dry_run_executed=true`，**`scene_delta_executor_invoked=false`**，其余写路径与模型调用标志均为 **false**。

## 映射矩阵语义

映射表仅说明 **Vision stub 候选字段** 与未来 **Scene Delta 概念槽位** 的对应关系（例如 `scene_delta.observed_visual_candidate`、`scene_delta.source_frame_ref`、`scene_delta.spatial_evidence` 等），**不**代表已生成生产级 Scene Delta 或已通过执行器校验。

## 评测入口

见 [LUNA_EVALUATION_SCENE_DELTA_WRITE_CANDIDATE_DRYRUN_FROM_VISION_V0.md](../evaluation/LUNA_EVALUATION_SCENE_DELTA_WRITE_CANDIDATE_DRYRUN_FROM_VISION_V0.md)。

## 与 OCR 线的关系

与 [LUNA_SCENE_DELTA_WRITE_CANDIDATE_DRYRUN_VERIFIER_V0.md](./LUNA_SCENE_DELTA_WRITE_CANDIDATE_DRYRUN_VERIFIER_V0.md)（OCR）同构；输入文件名与 summary **schema_version** 为 Vision 专用。

## 与上一 phase 的关系

输入来自 **Vision write candidate stub** 产物（见 [LUNA_SCENE_DELTA_WRITE_CANDIDATE_FROM_VISION_V0.md](./LUNA_SCENE_DELTA_WRITE_CANDIDATE_FROM_VISION_V0.md)）。

## 建议下一跳

**Phase-MidPlatform-Scene-Delta-Executor-Trace-Stub-From-Generic-DryRun-001**：由 Vision（或 OCR）dry-run 目录生成 **generic executor trace stub**（与 OCR 专用 trace 入口并存），见 [LUNA_SCENE_DELTA_EXECUTOR_TRACE_STUB_GENERIC_DRYRUN_V0.md](./LUNA_SCENE_DELTA_EXECUTOR_TRACE_STUB_GENERIC_DRYRUN_V0.md) 与 `../evaluation/LUNA_EVALUATION_SCENE_DELTA_EXECUTOR_TRACE_STUB_GENERIC_DRYRUN_V0.md`。
