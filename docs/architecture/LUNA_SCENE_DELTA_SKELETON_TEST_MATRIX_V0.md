# LUNA — Scene Delta Skeleton Test Matrix v0

## Phase

- **Phase-MidPlatform-SceneDelta-002**

## Purpose

冻结 skeleton 的最小验收矩阵（对齐 001-Fix verifier A–R 的可测子集），确保实现不漂移。

## Test matrix（A–R 最小可测子集）

- **A**: new_content_same_place → full_reprocess/partial_update
- **B**: same_content_same_place → reuse_previous/ignore_duplicate（并产出 compression record）
- **C**: content_replaced 记录（previous/current content refs）
- **C2**: content_removed 记录（previous content ref 存在；requires_revalidation=true）
- **H**: expired_content_recheck → expire_and_reprocess + requires_revalidation=true
- **I**: task_context_changed → full_reprocess/partial_update + task_context_changed=true
- **J/K**: compression 保留审计字段（canonical/first/last/duplicate_count/retained_sample_refs or cold storage ref）
- **L**: 默认 individual_local（shareable_to_hive=false；不实现上传）
- **M/N/O/P/R**: 边界：no hive upload / no world write / navigation_action=null / real_tts_invoked=false / runtime_invoked=false

## Sample coverage（本阶段 sample_matrix 最少覆盖）

- same_content_same_place
- new_content_same_place
- duplicate_evidence_compression
- expired_content_recheck
- task_context_changed_reprocess
- low_confidence_hold_uncertain
- missing_anchor_hard_block

