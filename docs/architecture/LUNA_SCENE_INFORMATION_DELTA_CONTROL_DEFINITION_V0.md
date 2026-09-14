# LUNA — Scene Information Delta Control Definition v0

## Phase

- **Phase-MidPlatform-SceneDelta-001**

## Purpose（定义冻结；不做实现）

定义中台级“场景信息增量分流器（Scene Delta Control）”的定位与边界。

它不是“缓存”，而是中台的信息分流机制：

新输入进来 → 与历史处理结果对比 → 判断重复/变化/不确定/过期/任务相关 → 决定复用/忽略/局部更新/全量重处理/暂存/阻断。

在 v0 定义中，Scene Delta 的本质不是“判断有没有重复”，而是：

**在同一个时空锚点上**，判断信息是否重复、替换、消失、新增、过期、冲突。

核心价值：

- 避免 YOLO/OCR/后续链路对同一信息反复处理
- 保证真正变化的信息被捕捉
- 阻止重复/不确定/低价值证据污染中台、世界模型与任务链

## Non-governance boundaries（硬边界）

- 不实现 runtime
- 不接真实中台
- 不接 SceneTask/Fusion/Output
- 不做最终语义提炼
- 不执行导航动作（`navigation_action=null`）
- 不真实播报
- 不写入真实世界模型
- 不接推荐系统

## Applicability（适用输入类型）

Scene Delta 是**中台级通用分流器**，适用于但不限于：

- OCR raw text evidence
- YOLO detections
- YOLO × OCR bridge results
- WorldContextEvidence candidates
- AmbientContextCandidates
- VisualSymbolEvidence candidates
- 以及未来语音/地图/传感器等 evidence

## Core responsibilities（职责冻结）

1. **Spatiotemporal Delta Anchor（主机制）**
   - 在同一空间载体/区域上绑定证据，支持“固定位置内容演替”判断
2. **Repeated Evidence Compression / Incremental Storage（主机制）**
   - 对重复观察进行压缩与增量记录，减少重复处理，同时保留可审计轨迹
3. 判断信息是否已经处理过（dedupe / reuse）
4. 判断信息是否发生变化（changed / partial）
3. 判断变化是否有任务价值（task_context_changed 触发重评）
4. 决定是否进入后续候选链（allowed_to_downstream_candidate）
5. 决定是否复用旧结果（reuse_previous）
6. 决定是否暂存等待更多证据（hold_uncertain）
7. 决定是否因过期需要复核（expire_and_reprocess）
8. 对治理越界/缺失来源的输入进行阻断（block）

## Inputs/State/Decision（对象总览）

本阶段定义三类对象（详见后续合同与策略文档）：

- `SceneDeltaInput`：本次进入分流器的输入对象（含签名、锚点、引用、置信度）
- `SceneProcessedState`：历史处理状态（含签名、TTL、seen_count、last_output_refs）
- `SceneDeltaDecision`：分流决策（delta_status + delta_action + change_summary + 审计引用）

并新增两类核心政策模块（主机制）：

- `SpatiotemporalDeltaAnchor`：时空锚点与载体/位置稳定性画像
- `RepeatedEvidenceCompression`：重复证据压缩与增量存储（含冷存储与样本帧保留策略）

参照：

- `LUNA_SCENE_DELTA_SPATIOTEMPORAL_ANCHOR_POLICY_V0.md`
- `LUNA_SCENE_DELTA_REPEATED_EVIDENCE_COMPRESSION_POLICY_V0.md`
- `LUNA_SCENE_DELTA_INDIVIDUAL_AND_HIVE_STORAGE_POLICY_V0.md`

## Relationship to World Model（写死边界）

Scene Delta 不直接写世界模型。

它只决定：

- 是否值得重新生成 WorldContextEvidence candidate
- 是否复用旧候选
- 是否标记旧状态 expired/superseded
- 是否需要 revalidation

禁止：

- 直接持久化世界事实
- 直接影响任务路径/执行
- 直接共享给蜂巢（默认 shareable=false 的治理口径延续）

