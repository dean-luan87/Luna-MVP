# Luna — Post File Metadata Boundary Roadmap Decision v1

**Phase**：`Phase-Post-File-Metadata-Boundary-Roadmap-Decision-v1-001`  
**性质**：roadmap-decision-only / prioritization-only / boundary-freeze-only  
**输出目录**：`_eval_out/post_file_metadata_boundary_roadmap_decision_v1_smoke_v0/`

## 阶段目标

本阶段在 `Controlled Frame File Metadata Boundary` 链 closure 之后，做一次正式路线裁决，回答：

- 当前主线状态是什么（metadata boundary 链是否已关账、是否仍是 simulation-only）
- 下一步是否应该直接进入真实文件操作（答案：**不应该直接进入**）
- 下一步是否应先推进“文件存在性检查（existence check）”的 **guarded planning**（答案：**应该优先推进**）
- Real metadata read / real hash / EXIF / video probe / image read 等更高风险路线是否需要插队（答案：记录为后续，但本阶段不插队实现）

最终推荐下一阶段：

- `Phase-Controlled-Frame-File-Existence-Check-Guarded-Planning-v1-001`

## 强边界（必须冻结）

本阶段**只做路线裁决**，严禁扩展为实现阶段：

- 不执行文件存在性检查（不 `stat` / 不 `exists` / 不 `open` / 不 `read`）
- 不读取真实图像/视频内容；不打开图片/视频文件；不解码视频；不抽帧
- 不解析 EXIF；不 probe 视频；不计算真实 hash（仅讨论策略与路线）
- 不调用相机、不调用视觉模型、不调用 OCR provider、不提交 OCRRequest
- 不调用地图 API / 高德 API / GPS runtime
- 不调用 tracking runtime / optical flow runtime / crossing runtime
- 不触发 Navigation Action；不提交 Task State；不调用 Speech Gate / VOP / TTS
- 不写 `WorldModel / Memory / Fact / Library`；不做 entity resolution / fact admission / memory consolidation / library commit

## 核心结论（路线裁决）

metadata boundary closure 的含义是：**已冻结“无文件操作”的 metadata 边界治理链**，但这不等于：

- 文件存在性检查已开放
- stat/open/read 已开放
- 真实 metadata 读取（含 EXIF / video probe）已开放
- 真实 hash / pHash 计算已开放
- 真实图像/视频读取、解码、抽帧已开放
- 视觉/OCR/tracking/map/crossing runtime 已开放
- WorldModel/Memory/Fact/Library 写入已开放

因此下一步不能从 metadata boundary 直接跳到 stat/open/read。更稳的最小下一步是先完成：

- **File Existence Check Guarded Planning**（仍是 planning-only；不执行存在性检查）

## 产物概览

runner 必须输出（详见 evaluation 文档）：

- `summary.json`
- `input_root_matrix.json`
- `current_file_metadata_boundary_status_summary.json`
- `route_option_matrix.json` / `priority_ranking.json`
- `recommended_next_phase_decision.json` / `next_phase_recommendation.json`
- `boundary_freeze.json`
- `non_claims_register.json`
- `governance_debt_roadmap_register.json`
- `deferred_*_register.json`（Gate taxonomy、resilience/offline、WML/emotion）
- `no_runtime_boundary_report.json` / `no_write_boundary_report.json` / `no_file_operation_boundary_report.json`

## 通过条件（概念级）

当 verifier=GO 时：

- `final_decision=POST_FILE_METADATA_BOUNDARY_ROADMAP_DECISION_READY_FOR_FILE_EXISTENCE_CHECK_GUARDED_PLANNING`
- `recommended_next_phase=Phase-Controlled-Frame-File-Existence-Check-Guarded-Planning-v1-001`

## 实施状态

`Phase-Controlled-Frame-File-Existence-Check-Guarded-Planning-v1-001` 已以 **planning-only** 形式落地并通过 smoke verifier：只定义未来 existence check 的 gate/授权/路径范围/审计/失败与回滚策略；当前仍不允许调用 `exists/stat/open/read/hash`，不进入任何 runtime。

