# Luna Voice V3 — 视角—语义转换接口与边界（Vision-to-Semantic Bridge）v0

**目标**：把“视角相关事实（摘要级）”转成 **V2 语义层可消费** 的结构化输入，并把接口/边界/禁止项钉死。  
**本轮只做**：接口与边界设计（不接真实视觉模型、不扩 reply、不改长链编排、不让视觉结果驱动对话或行为）。  

**前置骨架已存在**：
- V1：语音最小闭环、真实性闸门（No Fabrication）、最薄会话状态锚 `VoiceV1SessionStateAnchor`
- V2：`SemanticConverterV2` 承载层 + 规则版 + shadow consume + control assisted routing baseline（stop/cancel）

---

## A. 定位

- **V3 的职责**：把“视角相关事实（以摘要形式提供）”转换为语义层可消费的 **结构化输入包**（可裁决、可观测、可降级）。  
- **它不是**：
  - 视觉模型本体（不负责检测/识别/分割/OCR 推理）
  - detector/OCR 原始输出直通层
  - 事实生成器
  - 对话/行为驱动层
- **硬边界**：
  - 不能绕过 **No Fabrication Rule**
  - 不能绕过 **统一时空锚点原则**（只消费中台统一基准，不自造）

---

## B. 当前允许进入语义层的视觉输入类型（摘要级）

V3 v0 **只允许“摘要级”输入**进入语义层（避免 raw 结果污染主链裁决）。允许的类型建议限定为：

- **场景摘要（scene summary）**：如 indoor/outdoor、retail/walkway/unknown 等“低维场景候选 + 置信”
- **风险摘要（risk summary）**：风险等级/类型/方向/距离带/置信等（不得强行升格为确定事实）
- **任务相关摘要（task-relevant summary）**：只包含与当前任务推进直接相关的低维事实（例如“货架可见”这种布尔/置信）
- **低维环境事实摘要（environment facts）**：少量白名单字段（低维、可解释、可回滚）

**明确不允许**：原始 detector box 列表、逐帧目标清单、raw OCR 文本全量、未稳定化的多源融合结果，直接输入语义主链。

---

## C. 建议的最小输入结构（VisionSemanticInputPack v0）

该输入包是“给语义层消费”的 **只读辅助输入**，不直接对用户输出。

建议最小结构（字段名可调整，但保持小而硬）：

```json
{
  "pack_version": "vision_semantic_input_v0",
  "source_summary_type": "sidewalk_env_summary_v1|retail_env_summary_v1|risk_summary_v1|unified_env_fill_shadow_v1|unknown",
  "scene_type": "walkway|retail|unknown",
  "task_relevant_facts": {},
  "risk_facts": {},
  "environment_facts": {},
  "uncertainties": [],
  "confidence": 0.0,
  "platform_time_anchor_ref": null,
  "platform_space_anchor_ref": null
}
```

字段约束：
- `task_relevant_facts / risk_facts / environment_facts`：只允许 **白名单低维字段**（避免把 detector/raw OCR 结构塞进来）
- `uncertainties`：视觉证据不足/冲突时必须填（短句即可）
- `confidence`：0..1；低置信不得伪装高置信
- `platform_*_anchor_ref`：只允许 **引用中台注入的统一锚点**（ref/ID/opaque token），不得由本层生成时间戳/坐标

---

## D. 建议的最小输出目标（供语义层消费，不对用户直出）

V3 的输出目标不是“对用户讲看到什么”，而是为语义层提供可控辅助，未来**最多**影响：
- `references` 解析辅助（例如“那个货架/前面”这类指代是否可能成立）
- `ambiguities` 判断（视觉证据不足时提示追问）
- `requires_followup` 判断
- 轻量 `safety_flags`（仅作为标记，不直接驱动行为）

**本轮明确不做**：不接行为、不接回复生成、不改 assisted routing 的控制类裁决边界。

---

## E. 硬边界（必须写死）

- **视觉证据不足**：不得包装成确定事实，必须进入 `uncertainties`，并降低 `confidence`
- **检测结果 ≠ 可说给用户的事实**：任何视觉摘要只能作为语义层内部辅助输入，不可直通对话事实
- **原始框/分类/OCR 原文**：不得直接进入语义主链输入（除非未来单独审计批准并加稳定化层）
- **时空锚点**：
  - 本层不得自造系统级时间戳/空间坐标
  - 若需时空信息，只能消费中台统一下发基准（ref），不得推断“当前位置/当前时间”
- **不得替用户补足对象/地点/状态**：不能因为“看起来像”就补全用户没说清的引用对象

---

## F. 当前禁止项（v0 写死）

- 不直接把 detector/raw OCR/raw vision boxes 输入语义层主链
- 不直接驱动 reply
- 不直接驱动 stop/cancel 等控制类裁决（尤其不能越过 V2 baseline）
- 不直接替代用户输入（视觉不是用户意图）
- 不直接改 `dispatch_voice_final_text(...)` route / proposal / submit / guard

---

## G. 推荐最小接入位置（只给一个）

**唯一推荐接入点（v0）**：`VoiceInputSessionManager.process_final_text_with_dispatch` 中，位于：
- `begin_from_event(ev)` 之后
- `SemanticConverterV2.convert(...)` 调用之前

在该位置引入“只读桥接步骤”（未来实现，不在本轮落代码）：  
从 `runtime_context.metadata` 中读取 **已被中台/上游注入的摘要键**，构建 `VisionSemanticInputPack v0`，并写入：
- `ev.metadata["luna_voice_vision_semantic_v3_input"] = <pack>`

然后 `SemanticConverterV2` 仅作为“可选输入”读取该 pack（不改现有 V2 规则版 intent 集合）。

**理由（代码事实）**：
- V2 语义转换器的唯一接入点在 `process_final_text_with_dispatch`，这里最适合把“视觉摘要输入”挂进 `VoiceInputEvent.metadata`，保证全链可携带、可观测。

---

## H. 与现有 V2 的关系（写死）

- V3 视角—语义桥接层是 **V2 语义转换器的上游辅助输入**，不是平级裁决器  
- 它只能辅助 `references/ambiguities/requires_followup` 等判断  
- 当前不直接改 V2 规则版 intent 集合，也不允许把视觉摘要变成控制类裁决信号  

---

## 约束 1：No Fabrication Rule（继续生效）

- 视觉侧不确定必须进入 `uncertainties`  
- 不允许把“疑似看到”包装成“已经确认”  
- 不允许为了流畅对话把视觉线索升格为确定事实  

## 约束 2：统一时空锚点原则（继续生效）

- 任何视觉语义桥接层都不得自造系统级时间戳或空间坐标  
- 若需引用时空信息，只能引用中台下发的统一锚点（ref/opaque token）

