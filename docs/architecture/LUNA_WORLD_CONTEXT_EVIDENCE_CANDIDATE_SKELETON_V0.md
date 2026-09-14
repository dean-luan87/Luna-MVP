# LUNA — WorldContextEvidence Candidate Skeleton v0

## Phase

- **Phase-WorldModel-ContextEvidence-002**

## Purpose

在严格非 runtime 的边界下，将已闭合（`closed_v0`）的：

- MidPlatform OCR Bridge 输出（过滤/分类后的证据）
- Scene Delta 输出（delta decisions / anchors / compression）

转换为 **WorldContextEvidence candidate**（离线候选），并生成可审计的 `trace/replay/whitebox`。

## ContextEvidence-003 关联（对齐增强）

从 Phase-WorldModel-ContextEvidence-003 起，本 skeleton 增强以下字段以支持“知道自己来自哪里、属于哪里”：

- `observed_where_source` / `spatial_anchor_confidence` / `anchor_status`
- `source_reference_chain` / `missing_source_refs` / `source_ref_integrity_status`
- `source_layers`（区分 sensing/bridge/midplatform/scene_delta/candidate）

强制：不伪造 GPS；缺失锚点必须 honest degrade（revalidation + no/low write）。

## Non-governance boundary（强制）

本阶段只做离线候选骨架（offline skeleton）：

- 不接真实 runtime
- 不写入真实世界模型（`world_model_write_invoked=false`）
- 不上传蜂巢（`hive_upload_invoked=false`）
- 不进入 SceneTask/Fusion/Output
- 不执行导航动作（`navigation_action=null`）
- 不真实播报（`real_tts_invoked=false`）
- 不接推荐系统（`recommendation_invoked=false`）
- 不生成最终语义结论（只产出候选与审计日志）

## Inputs

### A) `midplatform_ocr_bridge_root`

输入为一个 OCR Bridge 的 `output_root`，至少应包含：

- `midplatform_ocr_evidence_inputs.json`
- `filter_results.json`

### B) `scene_delta_root`

输入为一个 SceneDelta 的 `output_root`，至少应包含：

- `scene_delta_decisions.json`
- `scene_delta_trace.jsonl`

### C) `sample_matrix`

用于最小覆盖的离线样本：

- `datasets/world_context_evidence_samples_v0/sample_matrix.json`

## Outputs

在 `output_root` 下输出（离线文件）：

- `world_context_evidence_summary.json`
- `world_context_evidence_candidates.json`
- `commercial_activity_evidence_candidates.json`
- `world_change_event_candidates.json`
- `trust_and_lifecycle_records.json`
- `world_context_evidence_trace.jsonl`
- `world_context_evidence_replay.jsonl`
- `world_context_evidence_whitebox.jsonl`
- `evaluation_notes.md`

## WorldContextEvidenceCandidate（最小字段）

本阶段产物遵循 Phase-WorldModel-ContextEvidence-001 的口径（candidate-only 形态），并额外强制 governance 字段存在且为“全禁止”：

- `candidate_only=true`
- `governance.world_model_write_invoked=false`
- `governance.hive_upload_invoked=false`
- `governance.navigation_action=null`
- `governance.real_tts_invoked=false`
- `governance.recommendation_invoked=false`

## Mapping overview（骨架级）

### MidPlatform（OCR Bridge）

以 `filter_results.visual_text_relevance_class` 为路由依据，并受 `allowed_for_world_context_candidate / allowed_for_ambient_context_candidate` 门控：

- `world_context_text` → `evidence_type=text_context`，`ttl_policy=scene_local_ttl`
- `commercial_context_text/promotional_text` → `evidence_type=commercial_activity`，`ttl_policy=short_ttl`，并生成 `CommercialActivityEvidenceCandidate`
- `advertisement_like_text` → `evidence_type=ambient_context`，`ttl_policy=short_ttl`
- `uncertain/low-value` → `evidence_type=unknown`，`write_policy=no_write`，`evidence_status=uncertain_candidate`，`requires_revalidation=true`

### SceneDelta

以 `delta_status` 驱动 lifecycle，并在 `content_replaced/content_removed/expired/...` 时生成 `WorldChangeEvent` 候选：

- `content_replaced` → `world_change_event` candidate
- `content_removed` → `world_change_event` candidate（生命周期走 expired_candidate + requires_revalidation）
- `expired` → `expired_candidate` + `requires_revalidation=true`
- `duplicate/uncertain` → 不生成“持久事实”（本阶段全部 `write_policy=no_write`）

