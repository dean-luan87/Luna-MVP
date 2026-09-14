# Luna — Controlled Frame File Metadata Boundary Planning v1

**Phase**：`Phase-Controlled-Frame-File-Metadata-Boundary-Planning-v1-001`  
**性质**：planning-only / schema / policy / boundary（不执行任何真实文件操作）  
**输出目录**：`_eval_out/controlled_frame_file_metadata_boundary_planning_v1_smoke_v0/`

## 阶段目标

在 `Controlled Frame Sample` manifest-level closure 之后，本阶段定义“manifest placeholder → file metadata candidate”的中间层，包括：

- 未来文件存在性检查边界（当前不执行）
- 路径合法性边界（repo fixture / eval_out / user upload / blocked patterns）
- 外部 metadata 可读字段边界（仅 declared metadata，不读文件系统 metadata）
- 真实 hash 计算策略（当前不计算；placeholder 允许）
- fixture registry 与 entry schema
- manifest → file metadata candidate 升级路径

## 硬边界（必须保持）

- 不 stat 文件；不打开文件；不读取图像/视频内容  
- 不解码视频；不抽帧；不解析 EXIF；不 probe 视频  
- 不计算真实 hash；perceptual hash 继续 deferred（属于内容分析）  
- 不调用视觉模型 / OCR / tracking / map / crossing runtime  
- 不写 `WorldModel / Memory / Fact / Library`；不生成视觉/OCR/tracking 结果  
- 不调用 `Speech Gate / VOP / TTS`

## 核心产物

- `controlled_frame_file_metadata_boundary_planning_policy.json`
- `file_existence_check_policy.json`
- `path_legality_policy.json`
- `external_metadata_boundary_policy.json`
- `real_hash_computation_policy.json`
- `fixture_registry_policy.json` / `fixture_registry_entry_schema.json`
- `manifest_to_file_metadata_candidate_mapping_policy.json`
- `file_metadata_candidate_schema.json`
- `controlled_frame_file_metadata_boundary_planning_scenario_matrix.json`（≥16 场景）
- `file_metadata_boundary_matrix.json`

## 场景矩阵（最低 16 项）

覆盖 path allowed/restricted/blocked、declared metadata、hash policy、EXIF/video probe blocked、perceptual hash deferred、fixture registry candidate。

## 下一阶段

当 verifier=GO 时：

- `final_decision=CONTROLLED_FRAME_FILE_METADATA_BOUNDARY_PLANNING_READY_FOR_DRYRUN`
- `recommended_next_phase=Phase-Controlled-Frame-File-Metadata-Boundary-DryRun-v1-001`

注意：下一阶段 dry-run 也只能**模拟** metadata/file-boundary 决策，不得做真实文件操作。

## 实施状态

`Phase-Controlled-Frame-File-Metadata-Boundary-DryRun-v1-001` 已以 **dryrun-only** 形式落地并通过 smoke verifier：18 场景决策模拟完成，仍不 stat、不打开文件、不读图像/视频、不解析 EXIF、不 probe 视频、不计算真实 hash。推荐下一阶段为 Post-DryRun Review。

`Phase-Controlled-Frame-File-Metadata-Boundary-Post-DryRun-Review-v1-001` 已以 **review-only** 形式落地：审计 planning+dryrun 对齐与无文件操作边界，推荐进入 Closure。

`Phase-Controlled-Frame-File-Metadata-Boundary-Closure-v1-001` 已关账：File Metadata Boundary 链对当前主线正式 closure，仍禁止真实文件操作与 runtime。
