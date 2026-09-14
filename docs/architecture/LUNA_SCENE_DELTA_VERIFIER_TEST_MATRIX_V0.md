# LUNA — Scene Delta Verifier Test Matrix v0

## Phase

- **Phase-MidPlatform-SceneDelta-001-Fix**

## Purpose（本阶段只补 verifier 定义）

补齐 Scene Delta 的 verifier 测试矩阵与验收规则，重点覆盖：

- 时空锚点（SpatiotemporalDeltaAnchor）作为主机制
- signature comparison（内容/载体/空间变化的判定）
- RepeatedEvidenceCompression（减少重复处理但不破坏审计链）
- individual vs hive storage policy（默认不上传、不共享；蜂巢候选必须有隐私/验证字段）
- 过期/冲突/不确定的处理边界
- 严格 non-governance 禁止项（no runtime/no upload/no world write/no navigation/no TTS）

硬边界：

- 不实现 runtime
- 不接真实中台
- 不进入下游
- 不写真实世界模型
- 不上传蜂巢
- 不执行导航动作
- 不真实播报

## Hard blockers（硬阻断；任一触发即 NO_GO）

- `missing_spatiotemporal_anchor`
- `missing_signature_inputs`
- `compression_without_audit_ref`
- `hive_candidate_without_privacy_policy`
- `world_write_attempted`
- `hive_upload_attempted`
- `navigation_action_generated`
- `runtime_invoked`
- `raw_duplicate_deleted_without_trace`
- `contradicted_evidence_overwrites_fact`

## Test matrix (A–R)

### A. new_content_same_place
- **given**:
  - 同一 `spatiotemporal_anchor_id`
  - 旧 `content_signature` != 新 `content_signature`
- **expect**:
  - `delta_status=new_content_same_place`
  - `delta_action in {full_reprocess, partial_update}`
  - 不允许直接写世界模型事实（candidate-only）

### B. same_content_same_place
- **given**: 同一 anchor + 同一 `content_signature`
- **expect**:
  - `delta_action in {reuse_previous, ignore_duplicate}`
  - `duplicate_evidence_compressed_count` 增加（或等价压缩记录产生）

### C. content_replaced（海报栏 A→B）
- **given**: 海报栏旧内容 A，新内容 B（同 anchor）
- **expect**:
  - `delta_status=content_replaced`
  - `previous_content_ref` / `current_content_ref` 存在（replay 可追责）

### D. content_removed
- **given**: 固定载体仍在，但旧内容消失
- **expect**:
  - `delta_status=content_removed`
  - 旧 evidence/state 可被标为 stale/superseded（candidate-only）

### E. carrier_removed
- **given**: 海报栏/围挡/告示牌载体消失
- **expect**:
  - `delta_status=carrier_removed`
  - `world_change_candidate_created=true`（candidate-only）

### F. carrier_added
- **given**: 新出现固定载体（新 anchor）
- **expect**:
  - `delta_status=carrier_added`
  - `spatiotemporal_anchor_created_count` 增加

### G. frequently_changing_surface
- **given**: 同一 anchor 多次内容变化
- **expect**:
  - `stability_profile.content_stability=frequently_changing`
  - `expected_update_frequency` 不得写死为 stable

### H. expired_content_recheck
- **given**: `commercial_short_ttl` 到期
- **expect**:
  - `delta_action=expire_and_reprocess`
  - `requires_revalidation=true`

### I. task_context_changed_reprocess
- **given**: 内容未变，但任务上下文变化
- **expect**:
  - `delta_status=task_context_changed`
  - `delta_action in {full_reprocess, partial_update}`
  - `change_summary.task_context_changed=true`

### J. duplicate_compression_preserves_audit
- **given**: 多条重复 evidence 被压缩
- **expect**:
  - `canonical_evidence_ref` 存在
  - `duplicate_evidence_refs` 或 `duplicate_count` 存在
  - `first_seen_at` / `last_seen_at` 存在
  - `retained_sample_refs` 存在（first/last/periodic）

### K. compression_does_not_delete_required_evidence
- **given**: 压缩发生且配置 cold storage
- **expect**:
  - 仍可追溯原始 evidence（或 cold storage ref）
  - 缺失则触发 `compression_without_audit_ref`

### L. individual_storage_only_by_default
- **given**: 默认压缩记录/存储策略
- **expect**:
  - `storage_level=individual_local`
  - `shareable_to_hive=false`
  - 不得出现真实上传动作（见 R）

### M. hive_candidate_requires_privacy_policy
- **given**: `storage_level=hive_group_candidate`
- **expect**:
  - 必须有 `privacy_risk_level / requires_anonymization / cross_luna_validation_status`
  - 缺失则触发 `hive_candidate_without_privacy_policy`

### N. contradicted_evidence
- **given**: 新证据与旧证据冲突
- **expect**:
  - `delta_status=contradicted`
  - 不得直接覆盖旧世界事实（candidate-only；触发 revalidation）
  - `requires_revalidation=true`

### O. low_confidence_unstable
- **given**: 低置信度反复变化（unstable）
- **expect**:
  - `delta_action=hold_uncertain`
  - 不得进入世界模型事实

### P. no_spatiotemporal_anchor
- **given**: 缺 `observed_at/observed_where` 或缺 anchor_signature
- **expect**:
  - 不得进入 Scene Delta 正常路径
  - `hard_block`（`missing_spatiotemporal_anchor`）或 `insufficient_anchor`（若实现阶段允许软失败）

### Q. no_signature_comparison
- **given**: 缺 content/object/spatial 等必要比较字段
- **expect**:
  - 不得判定 `unchanged`
  - `hold_uncertain` 或 `hard_block`（`missing_signature_inputs`）

### R. no_runtime_no_upload_no_world_write
- **expect (all tests)**:
  - `runtime_invoked=false`
  - `hive_upload_invoked=false`
  - `world_model_write_invoked=false`
  - `navigation_action=null`
  - `real_tts_invoked=false`

## Verdict guidance

- 任一 Hard blocker 触发 → **NO_GO**
- 若缺少核心用例覆盖（A–R）→ **NO_GO**

