# unified env shadow / 双轨试验方案（V1）

## 1. 目标

### 1.1 为什么当前阶段更适合先做 shadow

《[LUNA_UNIFIED_ENV_DERIVATION_MAPPING_V1.md](./LUNA_UNIFIED_ENV_DERIVATION_MAPPING_V1.md)》已明确：在 **家族错配**、**TTL / freshness 语义未完全对齐**、**第三套语义层**与 **回退面** 等风险未澄清前，**不宜**将 unified env 做主线派生接入。

要回答的问题不是「技术上能不能接」，而是「**接了之后是否值得**替代或参与派生」。这依赖 **unified 与现有垂直 summary 的对照证据**，不能单靠方案推演。

### 1.2 本方案解决什么问题

- 规定 **shadow 在主线中的计算位置** 与 **只读落点**，确保 **不驱动** 现有 sidewalk / retail 输入与旁路行为。
- 规定 **对照对象、比对字段、样本与指标**，使试验可复现、可汇总。
- 规定 **试验结论边界**：何种结果可进入「最小接线」讨论，何种结果应 **维持双轨、不接主线**。
- **不承诺**本文件发布时即实现；实现可另立变更单，并遵守 §6 不做项。

---

## 2. shadow 位置（算在哪、写在哪、为何不驱动行为）

### 2.1 建议在主线的哪个阶段计算 unified env

**原则**：在 **sidewalk / retail 环境摘要已完成稳定化**（若 stabilizer 开启）之后、**旁路消费与 orchestrator 决策** 之前，用 **当前 `VoiceRuntimeContext` 的只读视图** 计算 unified。

**逻辑顺序（方案级）**：

1. 现有流程：`dispatch_voice_final_text` 入口 →（可选）`_maybe_stabilize_runtime_context_sidewalk_env_v1` / `_maybe_stabilize_runtime_context_retail_env_v1` → 后续分流与旁路。
2. **shadow 计算**：在上述稳定化 **之后** 追加一步：从 metadata 中 **读取**（不修改）`sidewalk_env_summary_v1`、`retail_env_summary_v1` 及会话时间等，构造 `build_unified_env_summary_v1(...)` 的输入；或 **并行** 用与生产一致的原始信号在**独立分支**中调用 unified（两种实现择一，以「与生产输入一致」为优先）。

**禁止**：在 shadow 路径中 **回写** `sidewalk_env_summary_v1` / `retail_env_summary_v1`；禁止用 unified 结果参与 **risk / 意图 / OCR** 任一路径。

### 2.2 结果写到哪里（只读 metadata / 白盒）

**建议落点（实现时二选一或并存）**：

| 落点 | 说明 |
|------|------|
| **独立 metadata 键** | 例如 `unified_env_summary_shadow_v1` 或 `debug_unified_env_summary_v1`，仅承载 unified **输出 dict**，供日志与白盒导出；**任何**旁路默认 **不得** 读取该键作输入。 |
| **白盒 / debug 结构** | 若工程已有 `VoiceWhitebox` 或 `metadata["debug"]` 约定，可将 **摘要哈希或精简字段** 写入，避免过大 payload。 |

**开关（建议）**：专用 env 开关，例如 `LUNA_ENABLE_UNIFIED_ENV_SHADOW_V1`（默认关）；与 stabilizer 开关 **正交**，避免「关 stabilizer 却算 shadow」时样本不可比——试验窗口内需 **记录** stabilizer 开关状态。

### 2.3 为什么不参与当前真实输入决策

- 旁路与主线已绑定 **`sidewalk_env_summary_v1`** / **`retail_env_summary_v1`** 契约；unified 尚未经对照验证，接入即构成 **第三套语义**（见派生映射草案）。
- shadow 仅用于 **观测与一致率**，避免 **污染** 生产 gating 与回归基线。

---

## 3. 对照对象

### 3.1 与 `sidewalk_env_summary_v1` 比什么

| 维度 | 比对内容 |
|------|----------|
| **家族与场景** | unified 的 `scene_family` 是否为 `walkway` 与 sidewalk 侧 `scene_candidate` / 业务预期 **一致**（见 §4.1）。 |
| **候选标签** | unified `scene_candidate` vs sidewalk `scene_candidate`（**字符串或归一化后**一致率）。 |
| **时间与衰减** | `event_timestamp`、`age_ms`；`summary_freshness` 是否 **同向**（同为 stale 等）；`ttl_ms` **差异分布**（unified 默认 6000 ms vs sidewalk 默认 5000 ms 会导致系统性偏差，统计时 **分层**说明）。 |
| **置信** | unified `environment_confidence` vs sidewalk `path_confidence`：**不做强行数值相等**，可做 **分桶相关性** 或 **定性**（见 §3.3）。 |
| **垂直独有** | `is_outdoor`：**仅记录** sidewalk 有、unified 无，**不参与** unified 对错判定。 |

### 3.2 与 `retail_env_summary_v1` 比什么

| 维度 | 比对内容 |
|------|----------|
| **家族** | unified `scene_family` 为 `retail` 与 retail 侧 `scene_type` / `scene_type_candidate` 是否 **一致向**（如均为货架/通道语义）。 |
| **候选 / 类型** | unified `scene_candidate` 与 `scene_type_candidate`（归一化后）一致率或 **冲突标注**。 |
| **置信** | unified `environment_confidence` vs `retail_context_confidence`：同 §3.1，**定性 + 分桶** 为主。 |
| **垂直独有** | `shelf_visible`、`gating_passed`：**只记在样本上下文**，不用于惩罚 unified。 |

### 3.3 哪些字段只做定性比对

- `path_confidence` ↔ `environment_confidence`、`retail_context_confidence` ↔ `environment_confidence`：**语义不完全等价**，以 **分桶 / 方向一致** 为主，不设硬阈值「必须相等」。
- `inference_notes`：**集合重叠** 或 **关键词共现**（如 `ttl_expired`）可作辅助，**不做**逐字完全一致率。

### 3.4 哪些字段可以做一致率统计

- `scene_family`（相对「由垂直 summary 推导的期望家族」或 **人工标注子集**）。
- `scene_candidate`（归一化字符串相等或 **编辑距离** 阈值内算一致）。
- `summary_freshness`（三值 **完全相等** 比例，及 **stale 同向率**）。

---

## 4. 最小评估指标

| 指标 | 定义建议 |
|------|----------|
| **scene family 一致率** | 在 **可同时对照** 的样本上，unified 的 `scene_family` 与「由垂直 summary + 映射规则得到的期望家族」一致的比例；**家族错配**（如 unified=retail 且当前仅强化 sidewalk 场景）单独计数。 |
| **candidate 一致率** | `scene_candidate`（及 retail 侧与 unified 对齐后的字符串）归一化后相等比例。 |
| **freshness / TTL 对齐情况** | `summary_freshness` 完全一致率；**stale 同向率**（均为 stale 或均非 stale）；`ttl_ms` **差值分布**（解释系统性偏差）。 |
| **补缺是否有效** | 垂直 summary **缺键** 时，若用 unified **仅作记录** 是否补全观测字段；**不**改变行为，只统计「若将来补缺，字段是否可用」。 |
| **错配样本数** | 家族冲突、candidate 冲突、freshness 反向（一 stale 一 fresh）等 **分类计数** 与 **示例 ID 列表**（便于复盘）。 |

**样本**：优先 **回放 / 合成 fixture**（可复现），再扩 **小流量试点**；每样本附带 **stabilizer 开关状态** 与 **时间戳**。

---

## 5. 试验结论边界

### 5.1 何种结果算「可继续考虑最小接线实验」

同时满足倾向（阈值实现阶段可调，此处为 **方向**）：

- **scene family / candidate** 在目标场景切片上 **一致率达到约定下限**（例如家族一致率与候选一致率均 **显著高于** 随机/基线），且 **错配样本可解释**（可归因于映射规则而非随机噪声）。
- **freshness** 以 **同向** 为主，**系统性 TTL 偏差** 已有文档化解释或已统一计算口径。
- **错配样本** 规模与类型 **可接受**（不主导尾部风险），且 **无** 大规模家族反向（unified 与垂直对同一场景给出 **互斥** 业务结论）。

→ 可进入 **「最小接线实验」** 设计（仍 **独立开关**、**不写回** 垂直键或仅 **补缺**），见派生映射草案 §4。

### 5.2 何种结果算「继续维持双轨，不接主线」

满足任一条即倾向 **不接**：

- **家族错配** 或 **candidate 冲突** 比例 **高**，且与 **TTL/freshness 未对齐** 强相关。
- unified 与垂直 summary **频繁反向**（freshness / 置信方向），且 **无法** 用映射或 TTL 统一解释。
- **补缺** 引入 **新的观测噪声**（例如时间戳不一致导致假 stale）。

→ **继续 shadow / 双轨**，优先 **迭代映射规则与输入构造**；或转 **意图 / OCR** 等并列能力（与成熟度复盘一致），**不**强行接 unified。

---

## 6. 当前阶段不做项（本方案范围）

| 不做 | 说明 |
|------|------|
| **主线派生接入** | unified 不写回、不替代 `sidewalk_env_summary_v1` / `retail_env_summary_v1` 作为唯一真源。 |
| **unified 替代现有 summary** | 旁路与稳定化路径 **不变**。 |
| **统一 schema 大重构** | 不合并 metadata 键、不大改对外契约。 |
| **行为驱动** | unified **不得** 改变旁路判定、orchestrator、risk、真实输出。 |

---

## 7. 后续分叉（不预设）

| 分叉 | 条件（与 §5 呼应） |
|------|---------------------|
| **A：进入最小接线实验** | shadow 指标与错配可接受，见 §5.1。 |
| **B：继续双轨；先补其他输入层** | shadow 一般或错配显著，见 §5.2；可转 `find_item_intent_summary_v1` / `ocr_summary_v1` 等（与业务优先级一致）。 |

**当前不拍板** A/B；以本试验 **落地结果** 为准。

---

## 一句话收束

先把 unified env 放在 **shadow / 双轨观察态**：**算出来、记下来、不驱动行为**，用对照指标决定 **是否值得** 做最小接线；**不要**在证据不足时硬接主线。
