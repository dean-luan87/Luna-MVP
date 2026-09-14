# Luna — Controlled Frame File Metadata Boundary DryRun v1

**Phase**：`Phase-Controlled-Frame-File-Metadata-Boundary-DryRun-v1-001`  
**性质**：metadata/file-boundary decision simulation only（不执行任何真实文件操作）  
**输出目录**：`_eval_out/controlled_frame_file_metadata_boundary_dryrun_v1_smoke_v0/`

## 阶段目标

在 File Metadata Boundary Planning 之后，本阶段通过 dry-run **模拟**以下决策结果，验证 planning policy 是否稳定：

- PathLegalityDecisionCandidate
- FileExistenceDecisionCandidate（`existence_status=not_checked`）
- ExternalMetadataDecisionCandidate
- HashPolicyDecisionCandidate
- FixtureRegistryDecisionCandidate
- ManifestToFileMetadataMappingDecisionCandidate

## 硬边界（必须保持）

- 不 stat；不打开文件；不读取图像/视频内容  
- 不解析 EXIF；不 probe 视频；不计算真实 hash 或 perceptual hash  
- 不调用视觉/OCR/tracking/map/crossing runtime  
- 不写 WorldModel / Memory / Fact / Library  

## 场景矩阵（≥18）

覆盖 path allowed/restricted/blocked、declared metadata、hash policy、EXIF/video probe blocked、pHash deferred、fixture registry candidate、manifest mapping candidate、敏感 metadata 需人工复核。

## 下一阶段

- `final_decision=CONTROLLED_FRAME_FILE_METADATA_BOUNDARY_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW`
- `recommended_next_phase=Phase-Controlled-Frame-File-Metadata-Boundary-Post-DryRun-Review-v1-001`

Post-DryRun Review 之后进入 Closure；Closure 后再判断是否进入「文件存在性检查 guarded planning」，仍不直接进入图像读取。

## 实施状态

`Phase-Controlled-Frame-File-Metadata-Boundary-Post-DryRun-Review-v1-001` 已以 **review-only** 形式落地并通过 smoke verifier：确认 dry-run 严格遵守 planning policy 且无真实文件操作；`ready_for_closure=true`。

`Phase-Controlled-Frame-File-Metadata-Boundary-Closure-v1-001` 已关账本 dry-run 所属治理链。
