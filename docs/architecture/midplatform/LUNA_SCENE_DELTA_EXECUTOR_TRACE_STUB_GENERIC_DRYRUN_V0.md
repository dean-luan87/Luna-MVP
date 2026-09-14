# Luna MidPlatform — Scene Delta Executor Trace Stub from Generic Dry-Run v0

**Phase**：`Phase-MidPlatform-Scene-Delta-Executor-Trace-Stub-From-Generic-DryRun-001`

## 目的

将 **executor trace stub** 从仅绑定 OCR dry-run summary schema，升级为 **generic dry-run 输入**：在同一套逻辑下支持

- **OCR** dry-run 目录（`scene_delta_write_candidate_dryrun_summary.json` + `schema=scene_delta_write_candidate_dryrun_summary_v0`）  
- **Vision** dry-run 目录（`scene_delta_write_candidate_dryrun_from_vision_summary.json` + `schema_version=scene_delta_write_candidate_dryrun_from_vision_summary_v0`）

自动解析 **mapping / risk / no-write audit** 文件名与 **write candidate + gate** 路径（来自 dry-run summary 的 `paths`），生成 **`scene_delta_executor_trace_stub_generic_v0`**、**8 步 planned step matrix**、**input compatibility** 与 **generic audit**。

## 边界

- **禁止**：真实 Scene Delta 执行器、Scene Delta 写入、数据库、事实层 / WorldModel、AI 解释、导航决策、真实视觉 / OCR provider 调用。  
- **不改变** 既有 OCR 专用入口：`run_scene_delta_executor_trace_stub_from_dryrun_v0.py` 仍生成 `scene_delta_executor_trace_stub_v0` 与旧文件名；本 phase **新增** generic 产物与 runner。

## 与上一 phase 的关系

- OCR dry-run：[LUNA_SCENE_DELTA_WRITE_CANDIDATE_DRYRUN_VERIFIER_V0.md](./LUNA_SCENE_DELTA_WRITE_CANDIDATE_DRYRUN_VERIFIER_V0.md)  
- Vision dry-run：[LUNA_SCENE_DELTA_WRITE_CANDIDATE_DRYRUN_FROM_VISION_V0.md](./LUNA_SCENE_DELTA_WRITE_CANDIDATE_DRYRUN_FROM_VISION_V0.md)

## 评测入口

见 [LUNA_EVALUATION_SCENE_DELTA_EXECUTOR_TRACE_STUB_GENERIC_DRYRUN_V0.md](../evaluation/LUNA_EVALUATION_SCENE_DELTA_EXECUTOR_TRACE_STUB_GENERIC_DRYRUN_V0.md)。

## 建议下一跳

**Phase-MidPlatform-Scene-Delta-Executor-Mock-Handshake-Generic-Trace-001**：消费 **generic trace stub** 做内存 mock 握手，见 [LUNA_SCENE_DELTA_EXECUTOR_MOCK_HANDSHAKE_GENERIC_TRACE_V0.md](./LUNA_SCENE_DELTA_EXECUTOR_MOCK_HANDSHAKE_GENERIC_TRACE_V0.md)。
