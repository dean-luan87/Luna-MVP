# LUNA — Visual Text Relevance & Promotional Noise Filter v0

## Phase

- **Phase-ModelOCR-MidPlatform-Bridge-001-Fix**

## Purpose

定义在 MidPlatform evidence layer 中，对 OCR 可见文字进行“可追责的视觉相关性分类”，并据此决定：
- 是否进入 `MidPlatformTextExtractionCandidate`
- 默认的阻断层级（soft_block / hold_uncertain 等）
- 如何保留证据引用（不删除 evidence）
- 如何记录 `block_reason` 与 `retained_evidence_ref`

## Non-governance boundary

- 不实现 runtime：只定义合同与默认策略。
- 不在 OCR provider 层过滤：所有广告/促销/背景分类发生在 MidPlatform filtering/blocking 层。
- 不删除 evidence：允许通过 `eligible_for_recheck=true` 在任务上下文变化时重新评估。

## visual_text_relevance_class（分类字段冻结）

`visual_text_relevance_class` 取值必须来自：

- `task_relevant_text`
- `context_relevant_text`
- `world_context_text`
- `commercial_context_text`
- `advertisement_like_text`
- `promotional_text`
- `decorative_text`
- `illegible_text`
- `blurred_text`
- `scribble_or_graffiti_text`
- `decorative_or_stylized_text`
- `fragmented_text`
- `non_actionable_text`
- `meaning_uncertain_text`
- `user_requested_text`
- `irrelevant_or_noise_text`
- `uncertain_relevance_text`

参照：`LUNA_MIDPLATFORM_VISUAL_TEXT_RELEVANCE_CLASSIFICATION_TABLE_V0.md`（统一枚举对照表与默认策略）

## 分类定义（何时触发）

### 1) task_relevant_text
与当前任务直接相关，例如：出口、楼层、科室、窗口、挂号、编号、路线/站台/门牌、警示等。

触发线索（示例）：
- 与 task_context 关键词匹配
- 包含出口/楼层/科室/窗口/路线编号/警示等任务关键字
- 来自 task_hint_guided_crop（若存在）

### 2) context_relevant_text
对场景理解有帮助，但不一定直接完成任务（例如服务台、电梯厅、收费处等）。

触发线索（示例）：
- 与场景节点/流程相关
- 与 task 目标无强直接映射，但可能作为补充线索

### 3) world_context_text
非当前任务、但能丰富世界模型的“场景环境文本”，例如店名/品牌名、广告牌/海报、营业信息、公共标语、楼层商户信息等。

注：工程实现中可能仍以 `background_static_text` 等视觉特征作为触发信号，但在该 contract 字段里统一归口为 `world_context_text`。

触发线索（示例）：
- 多帧重复出现
- 与当前目标无方向/流程/编号/警示价值
- 多在固定位置且缺少任务触发信息

### 4) commercial_context_text
店铺活动、折扣、促销、营业时间、商品活动、新品信息、会员优惠等商业补充信息。

触发线索（示例）：
- 满减、折扣、会员价、第二杯优惠、营业时间等
- 与“当前找店/找餐饮/找咖啡/找药店/找服务柜台”等体验类任务目标相关

默认语义：丰富用户对环境的感知，但不替代 primary task decision。

### 5) advertisement_like_text
广告、促销、海报、折扣、活动宣传的“类广告”内容。

触发线索（示例）：
- 出现“优惠 / 折扣 / 满减 / 促销 / 新品 / 扫码 / 会员 / 立减 / 特价 / 活动”等词
- 大面积海报、易拉宝、商业屏幕展示
- 与 task_context 无关（默认）
- 文字区域来自 poster / storefront / screen / billboard 类对象
- 与任务无关但在背景中稳定出现

### 6) promotional_text
明确带商业促销倾向的文字（更偏“交易/优惠机制”）。

触发线索（示例）：
- 满减、店庆、新品上市、扫码领券、会员权益等

### 7) decorative_text
装饰性文字、艺术字、品牌口号。

触发线索（示例）：
- 装饰风格明显
- 不包含任务型编号/流程/警示/地点指向

### 8) user_requested_text
用户明确要求读取某个文字区域时，将该 evidence 升级为此类别。

触发线索（示例）：
- “读一下这个牌子”
- “看看上面写什么/这家店叫什么/屏幕上写什么”
- “这海报说什么/帮我念一下”

在本阶段：该升级只用于提高默认读取优先级；导航动作仍必须为 `null`，且是否进入任务链仍由中台判断。

### 9) irrelevant_or_noise_text
低置信度、重复、装饰性强或无法可靠判定的文本。

处理原则：保留 evidence 供证据复核，但默认不进入任务链。

### 10) uncertain_relevance_text
暂时无法判断是否相关，需要结合任务或后续帧确认。

触发线索（示例）：
- 文字置信度较低
- reading_order / line_order 不确定且文本较长
- 需要更强的上下文来确认任务价值

### 11) illegible_text（新增）
文字疑似存在，但 OCR 结果不可可靠读取（不可执行、不可解释）。

### 12) blurred_text（新增）
模糊、抖动、过曝、遮挡导致不可读或低置信。

### 13) scribble_or_graffiti_text（新增）
涂鸦/随手写/墙面乱写，意图不明、稳定性差。

### 14) decorative_or_stylized_text（新增）
艺术字/装饰字/Logo 化文字；OCR 可能读错或含义不稳定。

### 15) fragmented_text（新增）
只读到半截、断裂、被遮挡的文字；无法形成可审计语义闭环。

### 16) non_actionable_text（新增）
可读但对当前任务、世界模型、商业上下文没有明确价值；不进入默认语义链。

### 17) meaning_uncertain_text（新增）
读到了文字，但无法判断其含义、用途或真实性；不得强行解释。

## Mapping to blocking & candidate strategy（分层处理默认规则）

策略原则：不删除证据，只阻断默认进入任务链；但非当前任务文本可进入 WorldModelContextEvidence（世界模型环境知识候选），并可在任务/用户上下文变化时重新激活。

1) task_relevant_text
- 允许进入 `MidPlatformTextExtractionCandidate`
- `task_relevance_status=potentially_relevant`（建议口径）
- 默认不产生 block_reason

2) context_relevant_text
- 可进入候选，但必须 `requires_further_validation=true`
- block_level 默认不阻断为 hard；更接近“soft 进入候选”

3) world_context_text
- 默认 `block_level=soft_block`
- evidence 保留；`allowed_to_task_candidate=false`
- 可进入 WorldModelContextEvidence（由 world context policy 决定 TTL 与写入策略）

4) commercial_context_text / promotional_text
- 默认 `block_level=soft_block`
- `block_reason` 分别为 `commercial_context_text | promotional_text`
- evidence 保留，不进入任务链（除非任务上下文明确要求识别店铺/广告/商品）
- 默认进入 `ambient_context_candidate`（ambient commercial context / experience enrichment 候选），并保持不驱动 primary task decision
- TTL 短 + 必须 revalidation（避免长期污染世界模型）

5) advertisement_like_text
- 默认 `block_level=soft_block`
- `block_reason=advertisement_like_text`
- evidence 保留，不进入任务链
- 默认进入 `ambient_context_candidate`（context_type=ambient_context_text），并保持不驱动 primary task decision
- TTL 短 + 必须 revalidation

6) decorative_text
- 默认 `block_level=soft_block` 或 `hold_uncertain`（由 evidence uncertainty 决定）

7) uncertain_relevance_text
- 默认 `block_level=hold_uncertain`
- 不进入任务链，等待后续帧或任务上下文确认

8) 低价值/不确定视觉文本（新增枚举）
- `illegible_text / blurred_text / fragmented_text / meaning_uncertain_text`
  - 默认 `block_level=hold_uncertain`
  - 不进入任务链
  - 不写世界模型持久层
  - 允许后续更清晰帧重新识别（保留 evidence ref 用于审计）
- `scribble_or_graffiti_text`
  - 默认 `block_level=soft_block`
  - 不进入任务链
  - 默认不写世界模型持久层（如需更进一步需多帧稳定与需要 revalidation 的额外治理条件）
- `decorative_or_stylized_text / non_actionable_text`
  - 默认 `block_level=hold_uncertain | soft_block`（由不可执行与不确定边界决定）
  - 用户明确要求读取时，可临时提升为 readout（`user_requested_text`），但必须保留 uncertainty 标记

参照：`LUNA_MIDPLATFORM_LOW_VALUE_UNCERTAIN_VISUAL_TEXT_HANDLING_POLICY_V0.md`

## task_context_override（任务上下文覆盖，允许重新激活）

- 当 task_context 明确出现“识别店铺名称/广告内容/商品名称”等强意图时：
  - 允许将 `commercial_context_text / advertisement_like_text / promotional_text / world_context_text` 由默认阻断状态重新分类为可用候选
  - 该行为必须记录：
    - `reclassified_count` 增量（或同等审计字段）
    - `task_context_override_count` 增量
    - 仍保留原始 evidence 的 trace/replay/whitebox 引用

## user_intent_override（用户明确请求读取）

- 当 user_intent 明确为“读一下这个牌子/看看上面写什么/这家店叫什么/屏幕上写什么/这个海报说什么/帮我念一下”：
  - 将对应 evidence 升级为 `user_requested_text`
  - 允许进入 readout candidate（但 `navigation_action` 必须为 `null`；本合同阶段不实现 runtime）
  - 对商业补充信息：允许产生 ambient/user_requested readout（navigation_action 仍为 `null`）
  - 商业信息仍需遵循 TTL + revalidation，避免长期污染（见世界模型/商业政策文档）

