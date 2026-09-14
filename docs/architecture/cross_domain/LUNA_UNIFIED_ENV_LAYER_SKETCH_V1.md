# 统一环境层雏形方案（V1）

## 1. 目标

### 1.1 为什么现在适合抽「统一环境层雏形」

`sidewalk_env_summary_v1` 与 `retail_env_summary_v1` 已各自完成「**方案 → builder → 主线接入**」，并复用同一套方法（builder 化、dispatch 前稳定化、`summary_schema_version` 幂等、stale/ambiguous、与 `risk_summary_v1` 并列不互写）。详见《[LUNA_CROSS_DOMAIN_INPUT_LAYER_MATURITY_REVIEW_V1.md](./LUNA_CROSS_DOMAIN_INPUT_LAYER_MATURITY_REVIEW_V1.md)》。

若此时继续优先补 `find_item_intent_summary_v1` 或 `ocr_summary_v1`，会**继续堆局部能力**；而环境类输入若再出现第三条、第四条 `*_env_summary_v1`，各写各的 schema，**共性会再次散掉**。因此更适合先把「已经跑通的环境类共性」在**概念层**收口成统一环境层雏形，再决定实现顺序（最小 builder vs 意图/OCR）。

### 1.2 本方案解决什么问题

- 写清 **统一环境层的最小职责与边界**（吞什么、不吞什么）。
- 写清 **最小公共字段** 与 **派生视图**（sidewalk / retail）各自保留什么。
- 写清与 **risk / 意图 / OCR** 的 **并列关系** 与 **禁止互写**。
- 写清 **当前阶段明确不做** 的事项，避免方案膨胀成「大一统重构」。

本文件 **只做架构雏形与边界**，**不承诺**立即实现、不修改现有代码。

---

## 2. 当前现状

### 2.1 两条环境摘要已走通同一套模式

| 摘要键 | 稳定化方案 | Builder | 主线入口稳定化 |
|--------|------------|---------|----------------|
| `sidewalk_env_summary_v1` | 《[LUNA_SIDEWALK_ENV_SUMMARY_STABILIZATION_PLAN_V1.md](./LUNA_SIDEWALK_ENV_SUMMARY_STABILIZATION_PLAN_V1.md)》 | `build_sidewalk_env_summary_v1` | `LUNA_ENABLE_SIDEWALK_ENV_SUMMARY_STABILIZER_V1` |
| `retail_env_summary_v1` | 《[LUNA_RETAIL_ENV_SUMMARY_STABILIZATION_PLAN_V1.md](./LUNA_RETAIL_ENV_SUMMARY_STABILIZATION_PLAN_V1.md)》 | `build_retail_env_summary_v1` | `LUNA_ENABLE_RETAIL_ENV_SUMMARY_STABILIZER_V1` |

### 2.2 它们当前分别承担什么职责

- **sidewalk**：面向 **室外步行 / 通行相关** 场景；旁路深接入主要消费 `scene_candidate`、`path_confidence`、`is_outdoor` 等，映射到 `SidewalkEnvironmentInput`；稳定化输出额外携带时效与观测字段。
- **retail**：面向 **店内零售购物** 场景；旁路主要消费 `scene_type` / `scene_type_candidate`、`retail_context_confidence`、`shelf_visible`、`gating_passed` 等，映射到 `RetailEnvironmentInput`；稳定化语义与 sidewalk **对齐**（同一套 `summary_freshness` / TTL / 降权思想），阈值按零售裁剪。

### 2.3 为什么继续各长各的会开始散

- 每新增一个垂直 `*_env_summary_v1`，若**没有**上层「环境事实摘要」的**公共语义**，会出现：字段同名不同义、TTL 口径不一致、scene 标签体系分裂、回归对账维度增多。
- 统一环境层雏形的目的 **不是** 立刻合并代码，而是 **先固定公共抽象**，让派生视图有**可预期的向上挂靠点**。

---

## 3. 统一环境层最小职责

统一环境层（概念上可对应未来的 `unified_env_facts_v1` 或仅作为 **文档契约 + 内部中间表示**，实现阶段再定名）**只负责**：

| 负责 | 说明 |
|------|------|
| **环境事实摘要** | 「当前会话/观测下，与**物理环境与场景归属**相关的、可衰减的事实与弱推断」的单一语义层 |

**明确不负责**（与成熟度复盘一致）：

| 不负责 | 说明 |
|--------|------|
| **意图** | 用户要找什么、任务目标等 → 仍属 `find_item_intent_summary_v1` 等 |
| **OCR** | 文本识别结果与证据 → 仍属 `ocr_summary_v1` |
| **风险** | 安全与风险等级/类型 → 仍属 `risk_summary_v1`；治理模式与 env 摘要 **不同赛道** |
| **真实输出** | 播报/提交/仲裁结果 → 不在环境层定义 |

---

## 4. 最小公共字段建议

以下为 **统一环境层**建议具备的 **最小公共字段**（名称可在实现时微调，**语义**应保留）。派生视图（sidewalk / retail）可 **扩展** 垂直字段，但应能 **映射回** 下列公共语义。

| 字段 | 角色 |
|------|------|
| `scene_family` | 粗粒度场景族（例如区分「室外通行」「零售店内」「未知」），用于路由与观测聚合，**不是**细标签全集 |
| `scene_candidate` | 细粒度场景候选标签（与现有 sidewalk/retail 命名可对齐或别名映射） |
| `environment_confidence` | **统一语义下的**环境整体置信（0–1）；派生视图中可与 `path_confidence`、`retail_context_confidence` **对照映射**，不强制同名合并到一线 dict |
| `event_timestamp` | 环境观测/摘要生效时间（与现有 builder 中 `event_timestamp` 一致） |
| `summary_freshness` | `fresh` / `stale` / `ambiguous` |
| `ttl_ms` | 本摘要适用的时间窗 |
| `confidence_weight` | 与年龄、冲突、过期联动的消费侧权重 |
| `source` | 主来源枚举，便于对账与回放 |

**建议一并保留的契约字段**（与现实现一致）：

- `summary_schema_version`（含 `…/1` 前缀，幂等门禁）
- （可选）`age_ms`、`inference_notes`、垂直专用 debug 指针等——**垂直字段不进统一层必选**，留在派生视图即可

---

## 5. 派生视图关系

### 5.1 `sidewalk_env_summary_v1` 如何从统一环境层派生（未来）

- **逻辑上**：先有（或并行计算）统一环境层的 **公共子集**，再 **投影** 为 sidewalk 专用 dict：保留 `is_outdoor`、`path_confidence`、室外相关 `inference_notes` 等；**公共字段**从统一层拷贝或一次性填充。
- **不变量**：派生后的 `sidewalk_env_summary_v1` 仍须满足现有稳定化方案与白盒契约；**不**因为统一层出现而改变「与 risk 并列、不互写」的规则。

### 5.2 `retail_env_summary_v1` 如何从统一环境层派生（未来）

- **逻辑上**：从统一环境层投影出 `scene_type` / `shelf_visible` / `gating_passed` 等零售专用字段；**公共时效字段**与 sidewalk **同源语义**。
- **不变量**：零售 **多级 TTL**（货架 vs 门店）可在派生层或 builder 参数层裁剪；统一层提供 **时间语义与 freshness 口径**，不强制一步到位的多级策略实现。

### 5.3 当前阶段为什么仍保留两个独立 summary

- **旁路消费契约已冻结在各自键上**（`sidewalk_nav_v1` / `retail_find_item_v1`），主线稳定化已按 **单键 replace** 接入；贸然合并为单键会破坏回归与开关策略。
- **统一环境层 V1** 先以 **文档与中间表示** 固定边界；待有明确实现里程碑时，再讨论「是否增加第三键 `unified_env_*`」或「builder 内部先算统一再投影」，**本阶段不选型**。

---

## 6. 与其他 summary 的并列关系

以下键在 `VoiceRuntimeContext.metadata` 中 **并列存在**，由各自 builder/上游写入，由 orchestrator 与旁路 **只读各自契约**：

| 键 | 与统一环境层关系 |
|----|------------------|
| `risk_summary_v1` | **并列**；统一环境层 **不读、不写、不覆盖** |
| `find_item_intent_summary_v1` | **并列**；意图 **不得** 与环境摘要互写 |
| `ocr_summary_v1` | **并列**；OCR **不得** 与环境摘要互写 |

**禁止**：用 risk 字段修补 `scene_*`；用环境摘要覆盖意图或 OCR；在环境 dict 内写入 risk 语义或 OCR 正文。

---

## 7. 当前阶段不做项（写死）

| 不做 | 说明 |
|------|------|
| **大一统 schema 重构** | 不一次性合并 sidewalk/retail 为单一对外 schema |
| **主线代码迁移** | 不基于本文件改 `dispatch_voice_final_text`、不重接旁路 |
| **意图 / OCR 合流** | 不把意图或 OCR 并入统一环境层或 env summary 单键 |
| **地图 / 知识接入** | 不作为本雏形阶段的交付内容 |
| **多场景大而全分类体系** | `scene_family` 仅保留粗桶；不全集枚举天下场景 |

---

## 一句话收束

先把 **统一环境层雏形** 的边界与公共字段写清楚，再决定后续是先做 **最小 unified builder / 中间表示**，还是继续补 **意图 / OCR** 摘要层；本阶段 **不重构** 现有 `sidewalk_env_summary_v1` / `retail_env_summary_v1` 实现。
