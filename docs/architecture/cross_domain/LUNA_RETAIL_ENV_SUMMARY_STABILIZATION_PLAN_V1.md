# retail_env_summary_v1 上游 context 稳定化方案（V1）

## 1. 目标

### 1.1 为什么当前要补稳定化

`retail_find_item_v1` 已在主线完成 **Level 1 / whitebox-only 深接入**（见《[LUNA_RETAIL_FIND_ITEM_V1_DEEP_INTEGRATION_IMPLEMENTED_NOTE.md](./LUNA_RETAIL_FIND_ITEM_V1_DEEP_INTEGRATION_IMPLEMENTED_NOTE.md)》），上游从 `VoiceRuntimeContext.metadata["retail_env_summary_v1"]` 读取环境摘要，并映射到 `RetailEnvironmentInput`。当前问题与 sidewalk 类似：

- **缺时间维度**：无法表达「环境判断已过期」，易把上一货架/上一门店的状态带到下一轮；
- **事实与推断混用**：`retail_context_confidence`、`shelf_visible`、`gating_passed` 来源不一，却可能被等同对待；
- **与意图、OCR、风险多条并行 dict 缺少契约**：易出现「用意图修补环境」或「用环境覆盖意图」的工程冲动。

本方案**不扩真实输出**、**不改 risk 优先压制**、**不做 OCR 真执行**，只定义 **retail_env_summary_v1** 的字段分层、时效、衰减及与邻域摘要的边界，为后续 **最小 builder + 主线接入** 提供依据。

### 1.2 这份方案解决什么问题

- 明确 **retail 环境摘要**最小应包含哪些字段、哪些是强事实、哪些是弱推断；
- 明确 **TTL / 刷新 / 降权 / 作废** 规则，减少跨轮次污染；
- 明确与 **find_item_intent_summary_v1**、**risk_summary_v1** 的并行关系与禁止互写；
- 预留 **统一环境层** 下零售摘要的迁移位置。

---

## 2. 当前现状

### 2.1 retail_find_item_v1 依赖的最小 context（环境侧）

主线 `voice_final_text_dispatcher.py::_maybe_attach_retail_find_item_v1_whitebox` 从 `retail_env_summary_v1` 读取：

| 字段（主线读取名） | 映射到 `RetailEnvironmentInput` | 缺失时行为 |
|--------------------|-----------------------------------|------------|
| `scene_type_candidate` 或 `scene_type` | `scene_type` | `"unknown"` |
| `retail_context_confidence` | `retail_context_confidence` | `0.0` |
| `shelf_visible` | `shelf_visible` | `false` |
| `gating_passed`（可选，且须为 bool） | `gating_passed` | `None`（由模块内规则推断） |

> 说明：`ocr_summary_v1` 与 **环境摘要分离**，由主线另键读取；本方案聚焦 **retail_env_summary_v1**，不在此合并 OCR 语义。

### 2.2 环境事实 vs 弱推断（当前口径）

| 内容 | 归类 | 说明 |
|------|------|------|
| 门店/楼层级 POI 或地图围栏命中（若上游可信） | **强事实（带源）** | 当前常未接入；若接入应带来源与时间 |
| `scene_type` / `scene_type_candidate` 为 `retail_shelf` / `retail_aisle` | **弱推断或标签** | 依赖感知/规则质量 |
| `retail_context_confidence` | **弱推断** | 无统一校准时不宜当硬阈值事实 |
| `shelf_visible` | **弱推断**（视觉） | 帧级波动大，需时效与衰减 |
| `gating_passed` 由上游显式给出 | **可视为强断言（带责）** | 若为模块推断则仍属弱推断 |

### 2.3 当前不稳定点

- 无 **观测时间** 与 **TTL**，跨轮次易「粘住」旧场景；
- 无 **来源 / schema 版本**，难做回归对账；
- `gating_passed` 与 `scene_type`+`confidence` 可能 **不一致**，缺少显式 `ambiguous` 状态；
- 与 **find_item_intent_summary_v1** 同挂 `metadata`，若无文档约束，易出现字段串用。

---

## 3. 建议字段分层（方案级）

以下为未来 `retail_env_summary_v1` 稳定化后的建议形态；实现阶段可微调命名，**分层语义**应保留。

### 3.1 强事实字段（应可校验、可追责）

- `event_timestamp`（或 `observed_at_ms`）：环境观测时间；
- `source`：如 `store_map_v1` / `perception_retail_v1` / `manual_debug`；
- `summary_schema_version`：如 `retail_env_summary_v1/1`；
- （可选）`venue_id` / `floor_id`：若地图层可提供且稳定。

### 3.2 弱推断字段（须配合置信与不确定性）

- `scene_type` 或 `scene_type_candidate`：与现主线兼容，保留其一为主、另一作别名仅过渡期；
- `retail_context_confidence`：整体「当前像零售购物场景」的置信；
- `shelf_visible`：货架/价签区域是否可见；
- `gating_passed`：若由上游给出，建议同时带 `gating_reason` 枚举（白盒用）；
- `inference_notes`：短枚举列表（如 `["low_light", "motion_blur"]`），**不进入播报**。

### 3.3 稳定化派生字段（仅供消费与观测）

由 **builder/stabilizer** 写入，**不应**由感知模块直接伪造：

- `summary_freshness`：`fresh` | `stale` | `ambiguous`；
- `ttl_ms`、`confidence_weight`、`age_ms`；
- 与 sidewalk 方案对齐语义，**阈值按零售场景单独裁剪**（见 §4）。

### 3.4 仅供白盒的字段

- `debug` / `raw_features_ref`：离线对账指针；
- 旁路 `retail_find_item_v1` 白盒内的 `task_evidence` 等：**不回写**进 `retail_env_summary_v1`（避免循环）。

---

## 4. 时效与衰减（零售场景裁剪）

零售与「室外步行」不同：人移动较慢，但 **货架级视觉** 变化快、**门店级** 上下文变化慢。建议 **分级 TTL（方案）**：

| 层级 | 建议 TTL 量级 | 说明 |
|------|----------------|------|
| 货架/价签视觉（shelf_visible、近景） | 0.5–3 s | 与帧率对齐；过期则降权或标 stale |
| 通道/货架区域 scene（retail_aisle / retail_shelf） | 3–15 s | 允许短空窗；过期标 stale |
| 门店/地图级「在店内」 | 30–120 s | 仍必须过期，避免离店后仍当店内 |

### 4.1 刷新

- 新观测与旧摘要 **同源、schema 一致** 且时间更新 → **整段替换**；
- **来源切换** → 建议先作废再写新摘要，避免混源。

### 4.2 降权

- 超 TTL：`summary_freshness=stale`，`confidence_weight→0`（或极低），旁路 **不提升** gating 置信；
- `scene_type` 与 `shelf_visible` 短期冲突 → `ambiguous`，不强行选边。

### 4.3 作废

- 会话结束 / `session_id` 变更；
- 显式离店/场景重置信号；
- schema 版本不兼容。

**实现阶段**可先用 **单一 TTL + 环境变量覆盖**（与 sidewalk V1 一致），再按管线拆多级。

---

## 5. 与 find_item_intent_summary_v1 的关系

### 5.1 并行存在

- **retail_env_summary_v1**：描述「是否处在可找货的零售环境、通道/货架上下文是否可信」；
- **find_item_intent_summary_v1**：描述「用户是否在找货、找什么、是否需要读标签、OCR 预算」等 **意图与任务态**。

两者 **并列** 于 `VoiceRuntimeContext.metadata`，由主线分别映射到 `RetailEnvironmentInput` 与 `FindItemIntentInput`。

### 5.2 哪些字段不能互相覆盖

- **禁止**把 `query`、`active`、`user_requested_reading` 等写入 `retail_env_summary_v1`；
- **禁止**把 `scene_type`、`shelf_visible` 等写入 `find_item_intent_summary_v1`；
- **禁止**用意图「推测」环境（例如因 active=true 就把 scene 改为 retail_shelf）。

### 5.3 为什么必须分层

- **环境**与**意图**生命周期不同：用户可能「在店内但暂时不问找货」或「问找货但环境尚未确认」；
- 分层后，白盒可对账 **gating 失败** 与 **无意图** 等组合原因，避免单一 dict 无法解释失败路径。

---

## 6. 与 risk_summary_v1 的关系

### 6.1 并列存在

- `risk_summary_v1` 仅用于 **安全压制**（high/critical、`risk_interrupt_preempt`），与零售环境摘要 **并列**。

### 6.2 risk 仍然优先

- 与现实现一致：高风险时 **压制零售外显**，但不要求改写 `retail_env_summary_v1` 字段；
- **禁止**用 risk 字段填充/修正零售环境字段；**禁止**用零售环境摘要覆盖 risk。

### 6.3 禁止互写/互覆盖

- 与《[LUNA_SIDEWALK_ENV_SUMMARY_STABILIZATION_PLAN_V1.md](./LUNA_SIDEWALK_ENV_SUMMARY_STABILIZATION_PLAN_V1.md)》中 risk 边界 **同口径**。

---

## 7. 后续演进边界

### 7.1 统一环境层中的位置

建议演进为：

- **统一环境层** 产出：室内外、区域、POI、粗粒度可通行语义等；
- **retail_env_summary_v1** 作为其 **零售场景派生视图**：只保留找货链需要的子集 + 稳定化字段；
- `retail_find_item_v1` 仍主要消费 **retail 视图 + 意图摘要 +（可选）OCR 摘要 + risk**，避免旁路直接依赖统一层全量字典。

### 7.2 当前阶段明确不做

- 不实现本方案中的 builder / 主线接入（后续独立指令）；
- 不让 retail 进入真实输出候选；
- 不改 orchestrator 顺序与 risk 压制；
- 不接 OCR 真执行、不做地图融合大重构。

---

## 一句话收束

先把 **retail_env_summary_v1** 的字段分层、零售场景裁剪下的 TTL/衰减、以及与 **意图摘要 / risk** 的并行边界写清楚，再进入 **最小实现 + 主线接入**，使三条旁路 **上游输入层成熟度** 对齐。
