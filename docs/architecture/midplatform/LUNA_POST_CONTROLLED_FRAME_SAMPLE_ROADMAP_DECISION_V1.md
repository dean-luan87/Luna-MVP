# Luna — Post Controlled Frame Sample Roadmap Decision v1

**Phase**：`Phase-Post-Controlled-Frame-Sample-Roadmap-Decision-v1-001`  
**性质**：roadmap-decision-only / prioritization-only / boundary-freeze-only  
**输出目录**：`_eval_out/post_controlled_frame_sample_roadmap_decision_v1_smoke_v0/`

## 阶段目标

本阶段在 `Controlled Frame Sample` 链 closure 之后，做一次正式路线裁决，回答：

- 当前主线状态是什么（样例链是否已关账、是否仍是 manifest-only）
- 下一步是否应该进入真实图像读取（答案：**不应该直接进入**）
- 下一步是否应先补齐“文件存在性检查 / 路径合法性 / 外部 metadata 边界 / 真实 hash 策略 / fixture registry”
- Gate Taxonomy / 中台治理 / 鲁棒性 / 离线分布式等路线是否需要插队（答案：记录为后续，但不插队实现）

最终推荐下一阶段：

- `Phase-Controlled-Frame-File-Metadata-Boundary-Planning-v1-001`

## 强边界（必须冻结）

本阶段**只做路线裁决**，严禁扩展为实现阶段：

- 不读取真实图像/视频内容；不打开图片/视频文件；不解码视频；不抽帧
- 不计算真实 hash（仅讨论策略与治理边界）
- 不调用相机、不调用视觉模型、不调用 OCR provider、不提交 OCRRequest
- 不调用地图 API / 高德 API / GPS runtime
- 不调用 tracking runtime / optical flow runtime / crossing runtime
- 不触发 Navigation Action；不提交 Task State；不调用 Speech Gate / VOP / TTS
- 不写 `WorldModel / Memory / Fact / Library`；不做 entity resolution / fact admission / memory consolidation / library commit

## 核心结论（路线裁决）

样例链 closure 的含义是：**manifest-level governance 已闭环**，但这不等于：

- 真实图像/视频读取已开放
- 文件打开、视频解码、抽帧、真实 hash 计算已开放
- 视觉/OCR/tracking/map/crossing runtime 已开放
- 生产推理/训练已开放
- WorldModel/Memory/Fact/Library 写入已开放

因此下一步不能从 manifest 直接跳到 image read。更稳的路线是先补齐：

- **Controlled Frame File Existence / Metadata Boundary Planning**

该路线仍然强调：**不读取图像内容**，只在治理层定义“文件存在性与外部 metadata 边界”。

## 产物概览

runner 必须输出（详见 evaluation 文档）：

- `summary.json`
- `input_root_matrix.json`
- `current_controlled_frame_sample_status_summary.json`
- `route_option_matrix.json` / `priority_ranking.json`
- `recommended_next_phase_decision.json` / `next_phase_recommendation.json`
- `boundary_freeze.json`
- `non_claims_register.json`
- `governance_debt_roadmap_register.json`
- `deferred_*_register.json`（Gate taxonomy、resilience/offline、WML/emotion）
- `no_runtime_boundary_report.json` / `no_write_boundary_report.json`

## 通过条件（概念级）

当 verifier=GO 时：

- `final_decision=POST_CONTROLLED_FRAME_SAMPLE_ROADMAP_DECISION_READY_FOR_FILE_METADATA_BOUNDARY_PLANNING`
- `recommended_next_phase=Phase-Controlled-Frame-File-Metadata-Boundary-Planning-v1-001`

## 实施状态

`Phase-Controlled-Frame-File-Metadata-Boundary-Planning-v1-001` 已以 **planning-only** 形式落地并通过 smoke verifier：定义 file/metadata 边界与 16+ 场景矩阵，仍不 stat、不打开文件、不读图像/视频内容、不计算真实 hash。

