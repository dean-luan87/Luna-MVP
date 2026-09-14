# LUNA — MidPlatform OCR Bridge Skeleton Test Matrix v0

## Phase

- **Phase-ModelOCR-MidPlatform-Bridge-002**

## Scope

仅覆盖离线 skeleton 的合同字段与边界门控：

## Test matrix（示意，后续 verifier 落地）

1) evidence input 生成
- evidence inputs JSON 可解析为列表
- 每个 evidence input 保持 candidate_only=true、semantic disabled、no execution

2) delta control 占位
- `scene_delta_control_results.json` 非空
- 每个 delta 结果包含签名字段：`crop_signature/text_signature/layout_signature/object_signature`

3) filtering/blocking 占位
- `filter_results.json` 非空
- `block_applied/block_level/block_reason` 字段齐全

4) candidate 输出边界
- `midplatform_text_extraction_candidates.json`：每个 candidate 满足合同中的 candidate_only=true、semantic_summary=null、navigation_action=null
- `world_context_evidence_candidates.json`：字段包含 observed_at/observed_where/trust/lifecycle/world_model_policy
- `ambient_context_candidates.json`：短 TTL、requires_revalidation=true、navigation_action=null

5) trace/replay/whitebox 可追溯
- 三份 JSONL 文件非空且可解析

6) verifier GO/NO-GO
- 未引入 semantic_summary / navigation_action 非 null
- 未触发使能执行（allows_execute_now=true）或 TTS/下游调用

