# LUNA — MidPlatform OCR Bridge Capability Status Matrix v0

## Phase

- **Phase-ModelOCR-MidPlatform-Bridge-003**

## Purpose

矩阵化 Bridge-002/002-Fix 的“已完成能力”和“禁止/未连接能力”，作为 `closed_v0` 的收口口径。

## Capability status（冻结）

| capability | status | notes |
|---|---|---|
| evidence_input | done | `MidPlatformOCREvidenceInput` contract-only skeleton（candidate_only） |
| delta_control | done_skeleton | 仅 skeleton：signatures + hold/reuse/full 占位决策 |
| filtering_blocking | done_skeleton | block_level/block_reason/retention 规则冻结 |
| visual_text_relevance | done_skeleton | relevance 分类 + 默认路由/阻断冻结 |
| world_context_candidate | done_skeleton | `WorldContextEvidence` candidate-only + TTL/revalidation 口径冻结 |
| ambient_context_candidate | done_skeleton | `AmbientContextCandidate` candidate-only + short_ttl/revalidation 冻结 |
| low_value_uncertain_handling | done_skeleton | illegible/blurred/graffiti/fragmented/stylized 等默认不进任务链，不写事实 |
| upstream_input_parsing | validated_offline | sample_matrix / yolo_ocr_bridge_root / ocr_benchmark_root 已验证可解析（只离线） |
| runtime | not_allowed | 本阶段明确禁止 |
| real_midplatform | not_connected | 不接真实中台 |
| downstream | not_allowed | 不接 SceneTask/Fusion/Output/推荐系统 |
| world_model_write | not_allowed | 不写真实世界模型持久层 |
| semantic_summary | not_allowed | 必须为 null |
| navigation_action | not_allowed | 必须为 null |
| real_tts | not_allowed | 禁止真实播报 |

