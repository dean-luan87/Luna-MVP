# LUNA — Visual Text Relevance → World Evidence Route Table v0

## Phase

- Phase-WorldModel-ContextEvidence-001-Fix
- Route Table Alignment v0

## Purpose

定义 `visual_text_relevance_class` 到中台候选路由，以及到世界证据（`WorldContextEvidence`）的写入策略路由。

本阶段只定义路由与字段映射，不实现 runtime。

## Mapping（路由表）

> 约定：navigation_action_allowed=false、默认不改变 primary task decision；仅用户明确请求可提升为 readout 语义（仍不生成导航动作）。

| visual_text_relevance_class | evidence_route（中台） | world_evidence_route（世界合同） | evidence_type（world.content.entity_type 取值占位） | default_task_planning_impact | default_world_model_write_policy | default_ttl_policy | revalidation_required | allowed_when_user_requested | navigation_action_allowed | speech_policy |
|---|---|---|---|---|---|---|---|---|---|---|
| task_relevant_text | task_candidate | optional_scene_local_candidate | none/route-dependent | weak/none | scene_local_candidate | scene_local_ttl | true | true | false | controlled_by_output_governance |
| context_relevant_text | task_supporting_candidate(+validation) | optional_scene_local_candidate | none/route-dependent | weak/none | scene_local_candidate | scene_local_ttl | true | true | false | controlled_by_output_governance |
| world_context_text | world_context_candidate | WorldContextEvidence | store_business / place_public_info（占位） | none | scene_local_candidate | scene_local_ttl | true | true | false | controlled_by_output_governance_or_suppressed |
| commercial_context_text | ambient_context_candidate | WorldContextEvidence（commercial_activity subset） | store_business_hours/store_promotion（占位） | none | low_priority_candidate | short_ttl | true | true | false | silent_by_default_or_user_requested_only |
| promotional_text | ambient_context_candidate | WorldContextEvidence（commercial_activity subset） | store_promotion（占位） | none | low_priority_candidate | short_ttl | true | true | false | silent_by_default_or_user_requested_only |
| advertisement_like_text | ambient_context_candidate_or_blocked | WorldContextEvidence（仅当生成候选） | store_ambient_ad（占位） | none | low_priority_candidate | short_ttl | true | true | false | silent_by_default_or_user_requested_only |
| ambient_context_text | ambient_context_candidate | WorldContextEvidence（non-persistent or short TTL） | place_ambient（占位） | none | no_write_or_low_priority_candidate（占位） | short_ttl | true | true | false | silent_by_default_or_user_requested_only |
| experience_enrichment_text | ambient_context_candidate | WorldContextEvidence（experience enrichment subset） | experience_hint（占位） | none | no_write_or_low_priority_candidate（占位） | short_ttl | true | true | false | low_priority_hint_or_silent_by_default |
| decorative_text | blocked_or_low_priority | optional_world_context_evidence | none/route-dependent | none | no_write_or_low_priority_candidate | short_ttl（若生成） | true | true | false | controlled_by_output_governance_or_suppressed |
| irrelevant_or_noise_text | blocked | none | none | none | no_write | none | false | false | false | silent |
| uncertain_relevance_text | hold_uncertain | none/until_validated | none | none | no_write | short_ttl(placeholder) | true | false | false | silent |
| user_requested_text | readout_candidate(+ambient optional) | WorldContextEvidence（短 TTL 或需复核持久化） | route-dependent | none/weak | user_confirmed_write (only if confirmed) | short_ttl/persistent_requires_revalidation（占位） | true | true | false | user_requested_only |

## Notes（重要说明）

1) `evidence_route` 与 `world_evidence_route` 分离
- 中台候选是输出控制（是否进入任务链/是否进入 ambient 候选）。
- 世界证据是时间空间信任生命周期合同（字段集合见 `LUNA_WORLD_CONTEXT_SPATIOTEMPORAL_EVIDENCE_CONTRACT_V0.md`）。

2) 商业证据默认短 TTL + revalidation
- 避免旧促销/营业信息污染生活变化图谱。

3) 不允许用广告/促销改变导航主路径
- 与 `task_planning_impact=none/weak` 强绑定，禁止默认影响推荐与导航。

