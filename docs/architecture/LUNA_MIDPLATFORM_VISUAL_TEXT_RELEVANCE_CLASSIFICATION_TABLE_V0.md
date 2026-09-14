# LUNA — Visual Text Relevance Classification Table v0

## Purpose

为 Phase-ModelOCR-MidPlatform-Bridge-001-Fix 的实现与审计提供统一枚举表，避免在落地时混用：
`world_context_text` / `commercial_context_text` / `promotional_text` / `advertisement_like_text` / ambient 和 readout 等语义边界。

本表不引入 runtime，仅整理现有合同中的默认策略与字段语义。

参照：`LUNA_MIDPLATFORM_TO_WORLD_CONTEXT_FIELD_MAPPING_V0.md`（字段口径对齐映射）

## Table（统一枚举与默认策略）

> 注：此处 `navigation_action_allowed` 在本阶段统一冻结为 `false`（不接 runtime，不生成导航动作）。
>
> 进一步注：`ambient_context_text` 与 `experience_enrichment_text` 在本阶段通常作为 ambient 路由的派生上下文类型使用（用于实现映射与审计），不一定由 OCR 分类器直接产出为 `visual_text_relevance_class`。

| visual_text_relevance_class | display_name | definition | examples | default_taskchain_policy | default_world_model_policy | default_ambient_policy | ttl_policy | revalidation_required | user_requested_override_allowed | navigation_action_allowed | speech_policy | retention_policy |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| task_relevant_text | Primary Task Text | 直接影响当前任务，例如出口、门牌、科室、窗口、站台、警示、路线编号。 | 出口/楼层/科室编号/警示牌/站台号 | allowed_as_candidate | scene_local_candidate | none | scene_local_ttl | false | true | false | controlled_by_output_governance | retain_evidence_and_candidate_for_trace |
| context_relevant_text | Task Support Text | 辅助理解环境与流程，帮助完成任务但不直接决定路径。 | 服务台/电梯厅/营业时间/排队入口/楼层导视 | allowed_with_validation | scene_local_candidate | none | scene_local_ttl | true | true | false | controlled_by_output_governance | retain_evidence_and_candidate_for_validation |
| world_context_text | World Context Text | 丰富世界模型的环境知识，例如店铺名称、品牌、公共标语、商户分布、楼层导视。 | 麦当劳/品牌名/公共标语/楼层商户信息 | blocked_by_default | scene_local_candidate | none | scene_local_ttl | true | true | false | controlled_by_output_governance_or_suppressed | retain_evidence_ref_for_audit_and_recheck |
| commercial_context_text | Commercial Context Text | 丰富体感但不驱动任务：店铺活动、折扣、促销、营业信息、新品、会员优惠。 | 第二杯半价/满减/会员价/营业时间/新品 | blocked_by_default | no_persistent_write_by_default | allowed_as_ambient_candidate | short_ttl | true | true | false | silent_by_default_or_user_requested_only | retain_evidence_ref_for_audit_and_recheck |
| promotional_text | Promotional Text | 强促销交易类信息，例如扫码领券、限时秒杀、满减规则。 | 扫码领券/限时秒杀/满199减50 | blocked_by_default | no_persistent_write_by_default | allowed_as_ambient_candidate | short_ttl | true | true | false | silent_by_default_or_user_requested_only | retain_evidence_ref_for_audit_and_recheck |
| advertisement_like_text | Advertisement-like Text | 泛广告/灯箱/海报/轮播屏等可能与地点无强关系，但仍具环境感知价值。 | 墙面海报/灯箱广告/轮播屏文字 | soft_block | no_persistent_write_by_default | allowed_if_context_match | short_ttl | true | true | false | silent_by_default_or_user_requested_only | retain_evidence_ref_for_audit_and_recheck |
| ambient_context_text | Ambient Context Text | 作为 ambient 输出路由的上下文类型（通常由广告/商业/环境补充信息派生）。 | 商场氛围提示/公共活动语 | blocked_by_default | no_persistent_write_by_default | allowed_as_ambient_candidate | short_ttl | true | true | false | silent_by_default_or_user_requested_only | retain_evidence_ref_for_audit_and_recheck |
| experience_enrichment_text | Experience Enrichment Text | 在用户任务允许、信息量不高、场景合适时的体验增强补充（通常由 commercial/ambient 派生）。 | 该店特色饮品提示/轻量体感增强语 | blocked_by_default | no_persistent_write_by_default | allowed_as_ambient_candidate | short_ttl | true | true | false | low_priority_hint_or_silent_by_default | retain_evidence_ref_for_audit_and_recheck |
| decorative_text | Decorative Text | 装饰性文字、艺术字、品牌口号等，不替代任务判断。 | 艺术字口号/装饰牌匾 | blocked_by_default | no_write_or_low_priority_candidate | none | short_ttl | true | true | false | controlled_by_output_governance_or_suppressed | retain_evidence_ref_for_audit_and_recheck |
| illegible_text | Low-Value / Illegible Visual Text | 文字疑似存在，但 OCR 结果不可可靠读取；不可执行、不可审计语义闭环。 | “??”/乱码/过度涂抹的疑似字符 | blocked_by_default (hold_uncertain) | no_write_by_default | none | short_ttl | true | true | false | silent_by_default | retain_evidence_ref_for_audit_and_recheck |
| blurred_text | Low-Value / Blurred Visual Text | 模糊、抖动、过曝、遮挡导致不可读或低置信。 | 模糊招牌/抖动文字 | blocked_by_default (hold_uncertain) | no_write_by_default | none | short_ttl | true | true | false | silent_by_default | retain_evidence_ref_for_audit_and_recheck |
| scribble_or_graffiti_text | Low-Value / Scribble or Graffiti | 涂鸦、随手写、墙面乱写，意图不明、稳定性差。 | 墙面涂写/随手符号 | blocked_by_default (soft_block) | no_write_by_default (optional: low_priority_candidate under multi-frame+revalidation) | none | null_or_short_ttl | true | true | false | silent_by_default | retain_evidence_ref_for_audit |
| decorative_or_stylized_text | Low-Value / Decorative or Stylized | 艺术字/装饰字/Logo 化文字，OCR 可能读错或语义不稳定。 | 艺术化 Logo 字体 | blocked_by_default (hold_uncertain) | no_write_by_default | none | null_or_short_ttl | true | true | false | user_requested_only | retain_evidence_ref_for_audit_and_recheck |
| fragmented_text | Low-Value / Fragmented Text | 只读到半截、断裂、被遮挡的文字；等待后续帧补全。 | 半截标语/遮挡断裂字 | blocked_by_default (hold_uncertain) | no_write_by_default | none | short_ttl | true | true | false | silent_by_default | retain_evidence_ref_for_audit_and_recheck |
| non_actionable_text | Low-Value / Non-actionable Visual Text | 可读但对当前任务、世界模型、商业上下文都没有明确价值。 | 读得出来但与任务无关的短语 | blocked_by_default (soft_block) | no_write_by_default | none | null_or_short_ttl | false | true | false | silent_by_default | retain_evidence_ref_for_audit |
| meaning_uncertain_text | Low-Value / Meaning Uncertain Visual Text | 读到了文字但无法判断其含义、用途或真实性；不得强行解释。 | 无法判断用途的短句 | blocked_by_default (hold_uncertain) | no_write_by_default | none | short_ttl | true | true | false | silent_by_default | retain_evidence_ref_for_audit_and_recheck |
| irrelevant_or_noise_text | Irrelevant or Noise | 低置信度、重复背景、装饰性强或无法可靠判定阅读顺序的文本。 | 低置信重复字/装饰背景串/顺序不明长句 | blocked | no_write | none | null_or_short_ttl | false | false | false | silent | retain_evidence_ref_for_audit |
| uncertain_relevance_text | Uncertain Relevance | 暂时无法判断是否相关，需要结合任务或后续帧确认。 | 置信度低/顺序不确定/上下文缺失 | hold_uncertain | no_write | none | short_ttl | true | true | false | silent_by_default | retain_evidence_ref_for_audit_and_recheck |
| user_requested_text | User Requested Readout | 用户明确请求“读一下这个牌子/看看广告写什么/这家店叫什么”等临时提升为可读信息。 | “念一下这个活动牌” | allowed_as_readout_candidate | user_confirmed_write_by_governance | allowed_as_ambient_candidate (optional) | short_ttl_or_persistent_requires_revalidation | true | true | false | user_requested_only | retain_evidence_ref_for_audit_and_recheck |

## Field semantics（字段约束要点）

- `default_taskchain_policy`：表示是否允许进入任务链主候选/需要验证/或作为 readout candidate。
- `default_world_model_policy`：表示是否默认写入世界模型、以及是否“持久化型写入”。
- `default_ambient_policy`：表示是否进入 ambient context candidate（体感增强候选）。
- `navigation_action_allowed`：本阶段统一冻结为 `false`（不接 runtime，不生成导航动作）。
- `speech_policy`：本阶段只定义策略归类，不接真实播报系统。

