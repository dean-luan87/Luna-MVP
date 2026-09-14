# LUNA — WorldContextEvidence Candidate Skeleton Go/No-Go Pack v0

## Phase

- **Phase-WorldModel-ContextEvidence-002**

## Scope

离线骨架（offline skeleton）：

- 输入：MidPlatform OCR Bridge（closed_v0）与 SceneDelta（closed_v0）的输出根，或 sample_matrix
- 输出：WorldContextEvidence candidate + CommercialActivityEvidence candidate + WorldChangeEvent candidate + trace/replay/whitebox

## Hard boundaries（硬禁止）

任何一条触发即 **NO_GO**：

- 真实世界模型写入（`world_model_write_invoked=true`）
- 蜂巢上传（`hive_upload_invoked=true`）
- 产生导航动作（`navigation_action != null`）
- 真实 TTS（`real_tts_invoked=true`）
- 推荐调用（`recommendation_invoked=true`）
- 进入 SceneTask/Fusion/Output 链路（本阶段禁止）

## GO conditions（必须满足）

- skeleton 可运行（evaluate 工具可产出全量文件）
- `WorldContextEvidenceCandidate` 至少生成 1 条（任意输入方式）
- `observed_at/observed_where` 字段存在
- `trust/lifecycle/world_model_policy` 字段存在
- commercial/promo 路由能生成 `CommercialActivityEvidenceCandidate`（在 midplatform 输入或 sample_matrix 输入下）
- SceneDelta 的 `content_replaced/content_removed` 能映射到 `WorldChangeEvent candidate`（在 scenedelta 输入下）
- `trace/replay/whitebox` 非空
- verifier 通过（`tools/verify_world_context_evidence_candidate_v0.py --output-root ...` 返回 0）

## CONDITIONAL_GO（允许）

满足 GO 的全部硬边界与 schema，但以下覆盖不足可标记为 CONDITIONAL_GO：

- 仅跑通一种 input_type（例如只跑 sample_matrix）
- 某些 delta_status 在当前输入根中不存在，导致无法验证对应映射（但映射函数存在）

## NO_GO（判定）

除 Hard boundaries 外，以下任意一条也为 **NO_GO**：

- 缺失 observed_at/observed_where
- 缺失 trust/lifecycle/world_model_policy
- duplicate/uncertain 被当作可持久事实（写策略越权）
- commercial/promo 候选标记为可用于 primary task decision

