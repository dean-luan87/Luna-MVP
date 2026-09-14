# 统一环境层最小 builder 方案（V1）

## 1. 目标

### 1.1 为什么下一步应先做「最小 builder 方案」

《[LUNA_UNIFIED_ENV_LAYER_SKETCH_V1.md](./LUNA_UNIFIED_ENV_LAYER_SKETCH_V1.md)》已在**概念层**固定统一环境层的职责与公共字段。`sidewalk_env_summary_v1` 与 `retail_env_summary_v1` 也已证明 **环境类摘要** 的 builder + 稳定化模式可行。

若优先补 `find_item_intent_summary_v1` 或 `ocr_summary_v1`，会**继续增加并列模块**，却缺少**上层骨架**；意图/OCR 将来应挂在哪一层、与环境的边界如何对账，会反复争论。因此更有价值的是：先把 **最小 unified env builder** 的 **放置位置、输入、输出、派生关系** 写死，再进入实现与逐步挂靠。

### 1.2 本方案解决什么问题

- 回答 **最小 unified env builder 放在哪**（建议落点，非实现承诺）。
- 回答 **输入什么 / 输出什么**（第一版可接受的信号与契约字段）。
- 回答 **sidewalk / retail 如何从 unified 结果派生**，以及 **为何仍保留两个独立 summary key**。
- 写清 **第一版只支持哪些 `scene_family`**，以及 **明确不进 unified builder** 的内容。
- 写清 **当前阶段不做** 的主线接入与迁移，避免方案越界成重构。

本文件 **只做方案**，**不修改代码**、**不重构** 现有 `sidewalk_env_summary_v1` / `retail_env_summary_v1` 接入。

---

## 2. 最小 builder 职责

| 维度 | 说明 |
|------|------|
| **输入** | 若干 **原始环境信号**（见 §4），允许来自感知、规则或调试注入；不要求地图或知识库。 |
| **输出** | 一份 **统一环境摘要** `dict`（见 §5），仅表达环境事实与可衰减置信，带 `summary_schema_version` 幂等门禁语义。 |
| **不负责** | **意图**（`find_item_intent_summary_v1`）、**OCR**（`ocr_summary_v1`）、**风险**（`risk_summary_v1`）、**真实输出**（播报/提交/仲裁）。 |
| **不负责** | 替代或合并现有 sidewalk/retail builder 的**对外契约**；第一版仅定义 **可复用的中间层**，见 §6、§8。 |

---

## 3. 建议落点（放在哪）

**方案级建议**（实现阶段可微调路径，但应与其它 cross-domain context builder 同族）：

- **模块**：`capabilities/cross_domain/context/unified_env_summary_v1.py`（或与现有 `sidewalk_env_summary_v1.py` / `retail_env_summary_v1.py` **同目录并列**）。
- **入口函数名（建议）**：`build_unified_env_summary_v1(...)` → `dict`。
- **依赖方向**：unified builder **可**在实现时 **内部复用** 与 sidewalk/retail 已对齐的 TTL/stale/降权 **纯函数**（若已抽取）；**禁止** unified 反向依赖旁路或 risk。

**不做的落点**：不把 unified builder 塞进 `voice_final_text_dispatcher` 的 **第一版方案**（见 §8）；主线仍只稳定化既有的两个 key。

---

## 4. 最小输入建议（第一版）

第一版只接受 **能支撑 §7 两类 `scene_family`** 的最小信号，避免「大而全枚举」前置进入输入面。

| 输入（概念） | 说明 |
|--------------|------|
| `raw_scene_candidate` | 上游给出的场景候选字符串（可与现 sidewalk `scene_candidate` 或 retail `scene_type_candidate` **同源或别名**）。 |
| `raw_environment_confidence` | 原始环境整体置信（0–1）；若仅有一侧置信（如 `path_confidence` / `retail_context_confidence`），实现时可 **映射进** 该统一输入。 |
| `event_timestamp` | 观测或摘要时间；缺失时的 fallback 策略与现 sidewalk/retail builder **对齐**（如会话事件时间）。 |
| `source` | 主来源枚举（与现稳定化方案一致口径，如 `perception_*` / `manual_debug` 等）。 |
| （可选）`raw_family_hint` | 若上游已能区分 walkway vs retail，可作为 **弱提示**；**不得**单独决定 family 而不经 §7 规则校验。 |
| （可选）`ttl_override_ms` | 与现 builder 一致：允许 env/会话级覆盖默认 TTL。 |

**明确不作为 unified 第一版输入**：意图字段、OCR 文本、risk 任意字段、地图 POI/知识条目。

---

## 5. 最小输出建议（统一摘要字段）

统一 builder 产出的 `dict` **至少**包含下列字段（名称与《雏形》§4 对齐；实现时可增 `age_ms` 等观测字段，但 **不** 作为对外承诺变更 sidewalk/retail 键内容）。

| 字段 | 说明 |
|------|------|
| `scene_family` | 粗桶，**第一版仅** `walkway` \| `retail` \| `unknown`（见 §7）。 |
| `scene_candidate` | 细粒度候选标签，与输入对齐或经归一化后的字符串。 |
| `environment_confidence` | 统一语义下 0–1 环境整体置信。 |
| `event_timestamp` | 与输入/fallback 一致。 |
| `summary_freshness` | `fresh` \| `stale` \| `ambiguous`。 |
| `ttl_ms` | 本摘要适用时间窗。 |
| `confidence_weight` | 与年龄、过期、冲突一致的消费侧权重。 |
| `source` | 主来源。 |
| `summary_schema_version` | 建议前缀 `unified_env_summary_v1/1`（实现时与现 `sidewalk_env_summary_v1/`、`retail_env_summary_v1/` **并列命名空间**，避免误幂等）。 |

---

## 6. 派生关系

### 6.1 `sidewalk_env_summary_v1` 如何从 unified 结果派生

- **逻辑**：以 unified 输出为 **公共子集**，再 **追加** sidewalk 专用字段：`is_outdoor`、`path_confidence`（可与 `environment_confidence` 映射或分轨）、以及既有白盒所需别名。
- **约束**：派生 dict 仍须满足《[LUNA_SIDEWALK_ENV_SUMMARY_STABILIZATION_PLAN_V1.md](./LUNA_SIDEWALK_ENV_SUMMARY_STABILIZATION_PLAN_V1.md)》对强/弱字段分层的语义；**不**把 risk/意图/OCR 写入。

### 6.2 `retail_env_summary_v1` 如何从 unified 结果派生

- **逻辑**：以 unified 输出为公共子集，再 **追加** retail 专用字段：`scene_type` / `scene_type_candidate`、`shelf_visible`、`gating_passed` 等。
- **约束**：与《[LUNA_RETAIL_ENV_SUMMARY_STABILIZATION_PLAN_V1.md](./LUNA_RETAIL_ENV_SUMMARY_STABILIZATION_PLAN_V1.md)》一致；多级 TTL 可在 **retail 派生层** 裁剪，unified 层可提供 **单档默认 TTL** 作为基线。

### 6.3 当前阶段为什么仍保留两个独立 summary key

- 旁路与主线稳定化已绑定 **`metadata["sidewalk_env_summary_v1"]`** 与 **`metadata["retail_env_summary_v1"]`**；秒退开关与回归均以 **单键 replace** 为粒度。
- 第一版 unified builder 定位为 **中间层或未来挂靠点**：**不**要求立刻新增第三 metadata 键或改写 dispatch；待 **实现与验证** 完成后再决策「是否由现有 builder 内部先调 unified 再投影」。

---

## 7. 第一版支持范围（scene_family）

| `scene_family` | 含义 | 备注 |
|----------------|------|------|
| `walkway` | 室外通行 / 人行道相关环境（与 sidewalk 垂直域对应） | 与 `scene_candidate` 细标签配合使用 |
| `retail` | 零售店内购物环境（与 retail 垂直域对应） | 同上 |
| `unknown` | 无法可靠归入上两类 | **默认兜底**；不引入第三类业务 family |

**明确暂不进入第一版**：车载、室内非零售、工业、医疗等任何 **第三业务 family**；若输入似非 walkway/retail，**归入 `unknown`**，并可通过 `summary_freshness=ambiguous` 表达不确定，而非扩张枚举。

---

## 8. 明确不进 unified builder（第一版）

| 不进 | 说明 |
|------|------|
| **意图** | `find_item_intent_summary_v1` 全量语义 |
| **OCR** | `ocr_summary_v1` 全量语义 |
| **risk** | `risk_summary_v1` 任意字段 |
| **地图 / 知识** | POI、围栏、知识图谱等 |
| **大而全场景枚举** | 仅在 `walkway` / `retail` / `unknown` 三桶内运作；细分类留在 `scene_candidate` 字符串层，不建全集 taxonomy |
| **重构现有接入** | 不改 `build_sidewalk_env_summary_v1` / `build_retail_env_summary_v1` 的对外行为作为本方案交付；派生策略留待 **实现任务** |

---

## 9. 当前阶段不做项（写死）

| 不做 | 说明 |
|------|------|
| **统一层主线接入** | 不在 `dispatch_voice_final_text` 首段新增 unified 的 metadata 写入或稳定化开关 |
| **现有 summary 迁移** | 不要求 sidewalk/retail 立即改为「先 unified 再投影」 |
| **意图 / OCR 融合** | 不向 unified 输入或输出合并意图、OCR |
| **地图 / 知识接入** | 不作为本阶段范围 |
| **多场景全集分类体系** | 与 §7 一致，仅两业务 family + unknown |

---

## 10. 建议后续顺序（非本文件交付物）

1. 本方案评审定稿 → **统一环境层最小 builder 实现**（单测 + 与 sidewalk/retail 逻辑对齐的纯函数优先）。
2. 再决策是否让 `build_sidewalk_env_summary_v1` / `build_retail_env_summary_v1` **内部**调用 unified 并投影（**仍保留**两 key）。
3. 再评估 **意图 / OCR** 摘要层与 metadata 并列扩展。

---

## 一句话收束

先把 **统一环境层最小 builder** 的 **落点、输入、输出、派生方式与 walkway/retail 两 family 边界** 写清楚，再进入实现；**第一版不碰** 主线接入与既有 summary 迁移，**不并** 意图、OCR、risk。
