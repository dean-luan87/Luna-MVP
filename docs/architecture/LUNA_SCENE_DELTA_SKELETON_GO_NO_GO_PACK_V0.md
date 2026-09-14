# LUNA — Scene Delta Skeleton GO/NO-GO Pack v0

## Phase

- **Phase-MidPlatform-SceneDelta-002**

## GO conditions（必须全部满足）

- skeleton 可运行（evaluate 脚本可产出完整 outputs）
- sample_matrix 覆盖核心场景（见 skeleton test matrix）
- `SceneDeltaInput` 生成且 schema 合规（candidate_only / allows_execute_now=false）
- `SpatiotemporalDeltaAnchor` 生成
- `SceneDeltaDecision` 生成
- `RepeatedEvidenceCompression` 在重复/复用场景下生成（含 canonical_evidence_ref）
- trace/replay/whitebox 非空
- verifier 通过
- content lifecycle 分支可触发：
  - `content_replaced`
  - `content_removed`
- 边界成立：
  - `world_model_write_invoked=false`
  - `hive_upload_invoked=false`
  - `navigation_action=null`
  - `real_tts_invoked=false`
  - `runtime_invoked=false`

## CONDITIONAL_GO（允许但必须记录）

- 部分复杂用例（如 carrier_removed/added 的世界变化候选）未覆盖，但：
  - 核心 schema/边界成立
  - 压缩审计链要求成立

## NO_GO（任一触发即 NO_GO）

- 缺时空锚点仍进入正常路径（未触发 block/hold）
- 缺 signature 仍判定 unchanged/same_content_same_place
- 压缩记录无 `canonical_evidence_ref`
- 压缩后不可追溯（缺 first/last/duplicate_count/样本帧或 cold storage ref）
- `hive_upload_invoked=true`
- `world_model_write_invoked=true`
- 生成 `navigation_action`
- `real_tts_invoked=true`
- 触发 runtime/接入真实中台/进入下游

