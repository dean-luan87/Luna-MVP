# LUNA — Scene Delta Control GO/NO-GO Pack v0

## Phase

- **Phase-MidPlatform-SceneDelta-001**

## Scope

本阶段只做“Scene Delta 定义冻结”，不做任何 runtime 或接线实现。

## Phase-MidPlatform-SceneDelta-001-Fix linkage

本阶段的 verifier 定义补丁见：

- `docs/architecture/LUNA_SCENE_DELTA_VERIFIER_TEST_MATRIX_V0.md`

## GO conditions（必须全部满足）

1. **定位清晰**
   - Scene Delta 是中台级信息分流器，不是 OCR 缓存
2. **input/state/decision schema 明确**
   - `SceneDeltaInput` / `SceneProcessedState` / `SceneDeltaDecision` contract 冻结
3. **动作语义明确**
   - `reuse_previous / ignore_duplicate / partial_update / full_reprocess / hold_uncertain / expire_and_reprocess / block`
4. **signature comparison 规则明确**
   - 各 input_type 的 signature priority + 比较结果类 + 默认映射
5. **task_context_changed 重评规则明确**
   - 内容未变也可触发重评与重新路由
6. **世界模型关系边界明确**
   - 不直接写世界模型，仅决定候选是否重算/复用/过期/revalidation
7. **监控与可观测性字段明确**
   - metrics + trace/replay/whitebox 最小字段冻结
8. **Non-governance boundaries 写死**
   - 不实现 runtime、不接真实中台、不进下游、不做语义提炼、不导航、不播报、不写世界模型

9. **Spatiotemporal anchor（主机制）定义完整**
   - `SpatiotemporalDeltaAnchor` schema 明确
   - 固定空间载体的内容演替/下架/替换/频繁更新面可表达

10. **Repeated evidence compression（主机制）定义完整**
   - canonical evidence / 增量记录 / 冷存储 / 样本帧保留策略明确
   - 压缩不破坏审计链，可用于世界变化分析

11. **Individual vs hive storage 分层清楚**
   - storage_level / shareable_to_hive / 隐私与 cross-luna validation 状态冻结
   - 明确本阶段不实现真实上传/共享

12. **verifier matrix（001-Fix）覆盖完整**
   - 覆盖新增/重复/替换/移除/过期/冲突/压缩/个体与蜂巢边界
   - hard blockers 明确
   - no runtime / no upload / no world write / no navigation / no TTS 写死

## CONDITIONAL_GO（允许但必须 honest 记录）

- 若某些阈值仅能给出建议范围（v0 不实现），允许以“建议值”冻结，但必须明确“非实现”

## NO_GO conditions（任一出现即 NO_GO）

- 未对重复信息分流（无 duplicate / reuse 概念）
- 无 previous state 概念
- 无 signature comparison
- 无 task_context_changed 规则
- 直接写世界模型
- 直接执行导航/播报
- 本阶段实现 runtime 或接线到真实中台/下游

（追加 NO_GO）

- 没有时空间信息（仅文本去重，无法表达同一空间节点的内容演替）
- 重复信息压缩后不可追溯（破坏审计链）
- 个体/蜂巢存储边界不清（默认可共享/可上传）
- 把压缩记录直接当世界事实写入
- 本阶段实现真实上传/共享

（追加 NO_GO：verifier 缺失/覆盖不全）

- 缺少 Scene Delta verifier test matrix（定义不完整）
- 未覆盖时空锚点核心用例（海报栏/公告栏等）
- 未覆盖重复压缩审计链要求
- 未覆盖 individual/hive storage boundary
- 允许压缩后不可追溯
- 允许本阶段上传/写世界模型/执行导航/真实播报

