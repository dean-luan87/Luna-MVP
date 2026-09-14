# Luna 架构文档 — Vision

| 文档 | 作用 |
|------|------|
| [LUNA_VISION_VIDEO_FRAME_MINIMAL_INGEST_V0.md](./LUNA_VISION_VIDEO_FRAME_MINIMAL_INGEST_V0.md) | 视频帧最小离线 ingest 骨架（envelope / 采样 / audit）与边界。 |
| [LUNA_VISION_FRAME_INPUT_GOVERNANCE_V0.md](./LUNA_VISION_FRAME_INPUT_GOVERNANCE_V0.md) | **帧输入治理**：trace 之后、ROI stub 之前；`eligible_for_recognition` 恒 false。 |
| [LUNA_VISION_FRAME_ROI_PROPOSAL_AND_SEGMENTATION_STUB_V0.md](./LUNA_VISION_FRAME_ROI_PROPOSAL_AND_SEGMENTATION_STUB_V0.md) | **ROI proposal + segmentation stub**：规则 ROI、`vision_provider_input_pack_v0`、ROI crop 与坐标变换（不接 YOLO / 真实分割 / Supervision 主线）。 |
| [LUNA_VISION_LIGHTWEIGHT_RECOGNITION_ADAPTER_SELECTION_V0.md](./LUNA_VISION_LIGHTWEIGHT_RECOGNITION_ADAPTER_SELECTION_V0.md) | **Recognition adapter selection 骨架**：registry、默认 stub、selection report、synthetic 结果与 audit（不接真实模型）。 |
| [LUNA_VISION_RECOGNITION_EVIDENCE_PACK_V0.md](./LUNA_VISION_RECOGNITION_EVIDENCE_PACK_V0.md) | **VisionRecognitionEvidencePack v0**：stub 结果 → Luna 证据包（`not_fact` / synthetic）。 |
| [LUNA_VISION_RECOGNITION_EVIDENCE_READONLY_CONSUMER_V0.md](./LUNA_VISION_RECOGNITION_EVIDENCE_READONLY_CONSUMER_V0.md) | **Evidence 只读消费者**：遍历 / 聚合 consumer_view，不写事实层。 |
| [LUNA_VISION_EXTERNAL_SUPERVISION_ADAPTER_EXPERIMENT_V0.md](./LUNA_VISION_EXTERNAL_SUPERVISION_ADAPTER_EXPERIMENT_V0.md) | **外部实验**：Roboflow Supervision 作为 ROI/tracking 候选（非主线、非默认 Vision）。 |
| [LUNA_VISION_SUPERVISION_STRUCTURE_REFERENCE_ANALYSIS_V0.md](./LUNA_VISION_SUPERVISION_STRUCTURE_REFERENCE_ANALYSIS_V0.md) | **Supervision 结构参考分析**：Detections/tracker/zone → Luna 映射、风险边界、A/B 计划（不接主线）。 |
| [LUNA_VISION_DETECTION_EVIDENCE_SCHEMA_V0.md](./LUNA_VISION_DETECTION_EVIDENCE_SCHEMA_V0.md) | **VisionDetectionEvidence v0**：Luna 自有检测候选证据 schema 与 Supervision 字段对齐。 |
| [LUNA_VISION_SUPERVISION_ADAPTER_AB_TEST_V0.md](./LUNA_VISION_SUPERVISION_ADAPTER_AB_TEST_V0.md) | **Supervision adapter A/B**：rule_stub vs supervision_synthetic 结构对比（evaluation-only）。 |
| [LUNA_VISION_GATED_YOLO_CANDIDATE_ADAPTER_V0.md](./LUNA_VISION_GATED_YOLO_CANDIDATE_ADAPTER_V0.md) | **Gated YOLO candidate adapter**：evaluation-only YOLO → VisionDetectionEvidence v0。 |
| [LUNA_VISION_GATED_YOLO_REAL_SMOKE_V0.md](./LUNA_VISION_GATED_YOLO_REAL_SMOKE_V0.md) | **Gated YOLO real smoke**：本地权重真实推理 → VisionDetectionEvidence v0（禁止触网）。 |
| [LUNA_VISION_YOLO_REAL_POSITIVE_SAMPLE_SMOKE_V0.md](./LUNA_VISION_YOLO_REAL_POSITIVE_SAMPLE_SMOKE_V0.md) | **YOLO 正样本 real smoke**：可检测图像上产出 detection 并转 evidence。 |
| [LUNA_VISION_YOLO_EVIDENCE_PACK_INTEGRATION_STUB_V0.md](./LUNA_VISION_YOLO_EVIDENCE_PACK_INTEGRATION_STUB_V0.md) | **YOLO evidence pack integration**：真实 YOLO evidence 打入 recognition pack（evaluation-only）。 |
| [LUNA_VISION_YOLO_EVIDENCE_READONLY_CONSUMER_V0.md](./LUNA_VISION_YOLO_EVIDENCE_READONLY_CONSUMER_V0.md) | **YOLO evidence read-only consumer**：实际消费 YOLO evidence pack。 |
| [LUNA_VISION_YOLO_EVALUATION_CHAIN_CLOSURE_V0.md](./LUNA_VISION_YOLO_EVALUATION_CHAIN_CLOSURE_V0.md) | **YOLO 评测链闭环归档**：phase/lineage/no-write/non-claims。 |
| [LUNA_VISION_ROI_TO_OCR_REQUEST_BRIDGE_V0.md](./LUNA_VISION_ROI_TO_OCR_REQUEST_BRIDGE_V0.md) | **Vision ROI → OCRRequest bridge**：从 ROI 生成 OCRRequest candidate，不调用 OCR、不融合。 |
| [LUNA_VISION_MAINLINE_PHASE_ORDER_AND_INPUT_GATE_V0.md](./LUNA_VISION_MAINLINE_PHASE_ORDER_AND_INPUT_GATE_V0.md) | Vision 主线 **合法 phase 顺序**、禁止从 Frame Trace 直跳识别、`vision_provider_input_pack_v0` 占位。 |
| [LUNA_VISION_FRAME_TRACE_STREAM_REGISTRY_V0.md](./LUNA_VISION_FRAME_TRACE_STREAM_REGISTRY_V0.md) | 在 ingest 之上建立 **stream registry** + **frame trace** + lineage + 采样一致性（只读）。 |
| [LUNA_RETURN_TO_VISION_MAINLINE_PREPLAN_V1.md](./LUNA_RETURN_TO_VISION_MAINLINE_PREPLAN_V1.md) | 视角强化回归前置规划与复用审计；冻结 preplan 结论与风险边界。 |
| [LUNA_RETURN_TO_VISION_MAINLINE_PLANNING_V1.md](./LUNA_RETURN_TO_VISION_MAINLINE_PLANNING_V1.md) | 视角强化主线正式规划冻结；明确 roadmap、复用承诺、禁建清单、边界矩阵与第一批 phase。 |
| [LUNA_CONTROLLED_FRAME_INPUT_PLANNING_V1.md](./LUNA_CONTROLLED_FRAME_INPUT_PLANNING_V1.md) | 受控帧输入 planning；定义 frame source、intake gate、quality gate、privacy tagging、STC/freshness 与 downstream handoff 边界。 |
| [LUNA_CONTROLLED_FRAME_INPUT_DRYRUN_V1.md](./LUNA_CONTROLLED_FRAME_INPUT_DRYRUN_V1.md) | 受控帧输入 dry-run；用模拟 metadata 验证 frame candidate 是否能通过 intake/quality/privacy/freshness/handoff 候选链，并复核 dual-device placeholder 仍为 placeholder。 |
| [LUNA_CONTROLLED_FRAME_INPUT_POST_DRYRUN_REVIEW_V1.md](./LUNA_CONTROLLED_FRAME_INPUT_POST_DRYRUN_REVIEW_V1.md) | 受控帧输入 post-dryrun review；正式审查 planning + dry-run 是否稳定、边界是否成立，以及是否已具备进入 closure 的 readiness。 |
| [LUNA_CONTROLLED_FRAME_INPUT_CLOSURE_V1.md](./LUNA_CONTROLLED_FRAME_INPUT_CLOSURE_V1.md) | 受控帧输入 closure；正式冻结 planning + dry-run + review 三层闭环的状态、边界、non-claims、deferred capability pool 与下一阶段建议。 |
| [LUNA_CONTROLLED_FRAME_SAMPLE_PLANNING_V1.md](./LUNA_CONTROLLED_FRAME_SAMPLE_PLANNING_V1.md) | 受控样例 planning（manifest-level）；定义样例 manifest/schema/source policy/privacy precheck/manual review gate/file boundary/usage policy/mapping policy；不读取真实图像内容。 |
| [LUNA_CONTROLLED_FRAME_SAMPLE_DRYRUN_V1.md](./LUNA_CONTROLLED_FRAME_SAMPLE_DRYRUN_V1.md) | 受控样例 dry-run（manifest-metadata-only）；验证 sample manifest 能否通过 source/privacy/manual-review/usage/mapping stub，并生成 sample-level dry-run 结果；不读取真实图像内容。 |
| [LUNA_CONTROLLED_FRAME_SAMPLE_POST_DRYRUN_REVIEW_V1.md](./LUNA_CONTROLLED_FRAME_SAMPLE_POST_DRYRUN_REVIEW_V1.md) | 受控样例 post-dryrun review（review-only）；审查 planning+dryrun 稳定性与边界成立，并给出 closure readiness 决策。 |
| [LUNA_CONTROLLED_FRAME_SAMPLE_CLOSURE_V1.md](./LUNA_CONTROLLED_FRAME_SAMPLE_CLOSURE_V1.md) | 受控样例 closure（closure-only）；关账 planning+dryrun+post-review 并冻结边界/non-claims/deferred pool；不等于真实图像读取或视觉 runtime。 |
| [LUNA_CONTROLLED_FRAME_FILE_METADATA_BOUNDARY_PLANNING_V1.md](./LUNA_CONTROLLED_FRAME_FILE_METADATA_BOUNDARY_PLANNING_V1.md) | 受控文件 metadata 边界 planning（planning-only）；定义文件存在性/路径合法性/declared metadata/hash/fixture registry 边界；不 stat、不打开、不读内容、不算真实 hash。 |
| [LUNA_CONTROLLED_FRAME_FILE_METADATA_BOUNDARY_DRYRUN_V1.md](./LUNA_CONTROLLED_FRAME_FILE_METADATA_BOUNDARY_DRYRUN_V1.md) | 受控文件 metadata 边界 dry-run（simulation-only）；模拟 path/metadata/hash/fixture/mapping 决策候选；不 stat、不打开、不读内容。 |
| [LUNA_CONTROLLED_FRAME_FILE_METADATA_BOUNDARY_POST_DRYRUN_REVIEW_V1.md](./LUNA_CONTROLLED_FRAME_FILE_METADATA_BOUNDARY_POST_DRYRUN_REVIEW_V1.md) | 受控文件 metadata 边界 post-dryrun review（review-only）；审计 planning+dryrun 一致性与无文件操作边界。 |
| [LUNA_CONTROLLED_FRAME_FILE_METADATA_BOUNDARY_CLOSURE_V1.md](./LUNA_CONTROLLED_FRAME_FILE_METADATA_BOUNDARY_CLOSURE_V1.md) | 受控文件 metadata 边界 closure（closure-only）；关账 planning+dryrun+post-review，冻结 no-file-op 边界。 |
| [LUNA_CONTROLLED_FRAME_FILE_EXISTENCE_CHECK_GUARDED_PLANNING_V1.md](./LUNA_CONTROLLED_FRAME_FILE_EXISTENCE_CHECK_GUARDED_PLANNING_V1.md) | 文件存在性检查 guarded planning（planning-only）；定义未来 existence check 的 gate/授权/路径范围/审计/失败与回滚策略；本阶段不执行 exists/stat/open/read。 |
| [LUNA_CONTROLLED_FRAME_FILE_EXISTENCE_CHECK_GUARDED_DRYRUN_V1.md](./LUNA_CONTROLLED_FRAME_FILE_EXISTENCE_CHECK_GUARDED_DRYRUN_V1.md) | 文件存在性检查 guarded dry-run（simulation-only）；模拟 gate/授权/路径范围/审计/失败与回滚决策；不调用 exists/stat/open/read。 |
| [LUNA_CONTROLLED_FRAME_FILE_EXISTENCE_CHECK_GUARDED_POST_DRYRUN_REVIEW_V1.md](./LUNA_CONTROLLED_FRAME_FILE_EXISTENCE_CHECK_GUARDED_POST_DRYRUN_REVIEW_V1.md) | 文件存在性检查 guarded post-dryrun review（review-only）；审计 planning+dryrun 对齐与 no-file-operation/no-runtime 边界，给出 closure readiness。 |
| [LUNA_CONTROLLED_FRAME_FILE_EXISTENCE_CHECK_GUARDED_CLOSURE_V1.md](./LUNA_CONTROLLED_FRAME_FILE_EXISTENCE_CHECK_GUARDED_CLOSURE_V1.md) | 文件存在性检查 guarded closure（closure-only）；正式关账 planning+dryrun+post-review，冻结 no-exists/no-stat/no-open/no-read/no-hash，且明确真实 exists/stat 仍不可用。 |
| [LUNA_CONTROLLED_FRAME_FILE_STAT_GUARDED_PLANNING_V1.md](./LUNA_CONTROLLED_FRAME_FILE_STAT_GUARDED_PLANNING_V1.md) | 文件 stat guarded planning（planning-only）；定义未来 guarded stat 的 gate/授权/路径范围/隐私预检/metadata 暴露边界/审计/失败与回滚/映射边界；本阶段不调用 stat/exists/open/read/hash。 |
| [LUNA_CONTROLLED_FRAME_FILE_STAT_GUARDED_DRYRUN_V1.md](./LUNA_CONTROLLED_FRAME_FILE_STAT_GUARDED_DRYRUN_V1.md) | 文件 stat guarded dry-run（simulation-only）；模拟 stat gate 决策、路径范围分类、metadata 暴露边界、authorization、audit trace、failure/rollback/mapping；不调用 stat/exists/open/read/hash。 |
| [LUNA_CONTROLLED_FRAME_FILE_STAT_GUARDED_POST_DRYRUN_REVIEW_V1.md](./LUNA_CONTROLLED_FRAME_FILE_STAT_GUARDED_POST_DRYRUN_REVIEW_V1.md) | 文件 stat guarded post-dryrun review（review-only）；审计 planning+dryrun 对齐、场景覆盖与 no-file-operation/no-runtime/no-write 边界，给出 closure readiness。 |
| [LUNA_CONTROLLED_FRAME_FILE_STAT_GUARDED_CLOSURE_V1.md](./LUNA_CONTROLLED_FRAME_FILE_STAT_GUARDED_CLOSURE_V1.md) | 文件 stat guarded closure（closure-only）；正式关账 planning+dryrun+post-review，冻结 no-stat/no-exists/no-open/no-read/no-hash/no-runtime/non-claims；明确真实 `stat` 仍不可用。 |
| [LUNA_TASK_AWARE_VISUAL_FOCUS_POLICY_V1.md](./LUNA_TASK_AWARE_VISUAL_FOCUS_POLICY_V1.md) | 任务感知视觉焦点 policy；定义 `SceneSketchCandidate`、`VisualFocusPlan`、`VisualFocusSlot`、`ViewQualityCandidate`、`ActiveViewAdjustmentCandidate` 与视觉候选生命周期。 |
| [LUNA_WORLD_OBSERVATION_AND_ENTITY_FEATURE_POLICY_V1.md](./LUNA_WORLD_OBSERVATION_AND_ENTITY_FEATURE_POLICY_V1.md) | 后台世界观察与实体特征候选 policy；定义 `WorldObservationCandidate`、`WorldEntityFeatureCandidate`、`ObjectIdentityCandidate`、临时设施候选与 `WorldModel / Memory / Library` handoff placeholder。 |
| [LUNA_SELECTIVE_TRACKING_ADAPTER_POLICY_V1.md](./LUNA_SELECTIVE_TRACKING_ADAPTER_POLICY_V1.md) | 选择性追踪适配器 policy；定义 `TrackingRequestCandidate`、`TrackletCandidate`、tracking budget / admission / lifecycle，以及外部 adapter future registry。 |
| [LUNA_VISUAL_OCR_MAP_TASK_FEEDBACK_DRYRUN_V1.md](./LUNA_VISUAL_OCR_MAP_TASK_FEEDBACK_DRYRUN_V1.md) | 视觉 / OCR / 地图 / 记忆 / tracking candidate / 任务反馈 dry-run；把多条 policy 串成中台反馈候选链。 |

Vision 评测命令与产物索引见：`../evaluation/` 下 Vision 相关文档。

当前主线已完成 `Map / Location Read-Only Context Policy v1`、`Controlled Frame Input` 链（planning/dryrun/review/closure）、`Crossing Decision` 链（governance/dryrun/review/closure）、`Controlled Frame Sample` 链（planning/dryrun/review/closure）、`File Metadata Boundary` 链（planning/dryrun/review/closure）、`File Existence Check Guarded` 链（planning/dryrun/review/closure），并完成对应 roadmap decisions（含 `Post File Metadata Boundary` 与 `Post File Existence Check`）。  
当前已完成并通过 `File Stat Guarded` 链（planning/dryrun/review/closure），其核心含义为：完成 `stat gate` 的治理闭环，但 **真实 `stat` 仍不可用**。  
当前已完成并通过：`Phase-Post-File-Stat-Roadmap-Decision-v1-001`（roadmap-decision-only；显式选择先做 Gate Taxonomy；不进入真实 `stat` trial）。  
当前已完成并通过：`Phase-Gate-Taxonomy-and-Requirement-Framework-Planning-v1-001`（planning-only；冻结全局 gate taxonomy 与 Gate Constitution；不实现 gate runtime，不改既有 gate，不合并 gate）。  
当前已完成并通过：`Phase-Luna-Project-Structure-Governance-and-Modularization-Planning-v1-001`（planning-only；项目结构治理与模块化规划；不移动文件/不合并模块/不进入 runtime）。  
当前已完成并通过：`Phase-Luna-Project-Module-Inventory-and-Structure-Map-DryRun-v1-001`（dry-run-only；7391 条资产归位表；每条含 `future_life_system_mapping`；仍不做任何实际迁移）。  
当前已完成并通过：`Phase-Luna-Project-Structure-Consolidation-Planning-v1-001`（consolidation planning-only；冻结 merge/archive/split/keep/defer + 批次序列；仍不执行真实迁移）。  
当前已完成并通过：`Phase-Luna-Project-Structure-Consolidation-DryRun-v1-001`（B0–B6 模拟 + 冲突/复核/禁止自动执行/回滚计划；仍不移动文件）。  
当前已完成并通过：`Phase-Luna-Project-Structure-Consolidation-Post-DryRun-Review-v1-001`（三类结论：acceptable/plan_revision/permanent；仍不执行真实迁移）。  
当前已完成并通过：`Phase-Luna-Project-Structure-Consolidation-Closure-v1-001`（Planning→DryRun→Post-Review 闭环收口；仍不等于真实迁移）。  
当前已完成并通过：`Phase-Luna-Project-Structure-Consolidation-Roadmap-Decision-v1-001`（路线裁决；选中 Protected Asset and Human Review Resolution Planning；仍不直接迁移）。  
当前已完成并通过：`Phase-Protected-Asset-and-Human-Review-Resolution-DryRun-v1-001`（240 HR + 914 DNAE 模拟；1154 audit/rollback；仍不执行 human review / 不移动文件）。  
当前推荐下一阶段：`Phase-Protected-Asset-and-Human-Review-Resolution-Post-DryRun-Review-v1-001`（审查 dry-run 三类阻断是否完整）。
当前下游导航闭环对接 dry-run 见：`../midplatform/LUNA_BASIC_NAVIGATION_LOOP_VISION_STRENGTHENING_DRYRUN_V1.md`。
