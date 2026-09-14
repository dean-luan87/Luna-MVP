# LUNA — Scene Delta Repeated Evidence Compression Policy v0

## Phase

- **Phase-MidPlatform-SceneDelta-001**

## Purpose（本阶段只做定义）

将“重复证据压缩（Repeated Evidence Compression / Incremental Storage）”提升为 Scene Delta 的**主机制**：减少重复处理，同时保留可审计、可复现、可用于世界变化分析的连续轨迹。

## RepeatedEvidenceCompression（冻结 schema）

```json
{
  "compression_record_id": "rec_001",
  "compression_scope": "individual_local | hive_group | world_context_region",
  "anchor_ref": "sta_001",

  "canonical_evidence_ref": "evidence_001",
  "duplicate_evidence_refs": [],
  "duplicate_count": 12,

  "first_seen_at": null,
  "last_seen_at": null,

  "content_signature": null,
  "spatial_signature": null,

  "compression_method": "signature_dedup | delta_encoding | rolling_window_summary | canonical_ref",

  "storage_policy": {
    "retain_full_first_observation": true,
    "retain_full_last_observation": true,
    "retain_delta_only_for_duplicates": true,
    "retain_sample_frames": "first_last_or_periodic",
    "raw_evidence_cold_storage": true
  },

  "usage": {
    "reuse_previous_result": true,
    "skip_reprocessing": true,
    "available_for_world_change_analysis": true
  }
}
```

## Compression principles（写死）

1. 首次出现保留完整 evidence（canonical）
2. 后续重复出现只记录 delta / seen_count / last_seen_at（避免重复处理）
3. 内容未变化时不重复 OCR/不重复候选生成（复用旧结果）
4. 位置未变但内容变化：记录 content delta（content_replaced）
5. 内容未变但位置变化：记录 spatial delta（same_content_new_place）
6. 同一内容多位置出现：记录 multi-location pattern（用于世界变化分析）
7. 定期保留样本帧（first/last/periodic），避免压缩后不可审计
8. 原始 evidence 允许进入冷存储（不丢审计能力）
9. 个体本地压缩与蜂巢群体压缩必须分层（见 storage policy）

## Non-governance boundaries（硬边界）

- 压缩记录不得被当作“世界事实写入”
- 不实现真实上传/共享
- 不接 runtime/不进下游

