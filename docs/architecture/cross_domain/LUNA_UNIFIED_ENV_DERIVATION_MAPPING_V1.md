# sidewalk / retail 从 unified env summary 派生映射草案（V1）

## 1. 目标

### 1.1 为什么在 unified builder 落地后应先做派生映射草案

`unified_env_summary_v1` 已是**可运行**的最小 builder（见《[LUNA_UNIFIED_ENV_SUMMARY_V1_IMPLEMENTED_NOTE.md](./LUNA_UNIFIED_ENV_SUMMARY_V1_IMPLEMENTED_NOTE.md)》），但仍是**上层公共摘要**。若此时直接把 unified 接进主线或塞进现有 `build_sidewalk_*` / `build_retail_*`，容易在**未冻结投影规则**的情况下把派生关系**写死在代码里**，后续回退与双轨对比成本高。

本草案只做 **unified → sidewalk_env_summary_v1**、**unified → retail_env_summary_v1** 的**字段级映射与决策规则**，**不实现、不改代码、不接主线**。

### 1.2 本文件解决什么问题

- 写清 **sidewalk / retail 各自从 unified 继承什么**、**哪些必须继续来自垂直真源**。
- 写清 **冲突与覆盖** 时以谁为准。
- 写清 **哪些场景下 unified 只能当参考**，不能作为唯一输入。
- 给出 **当前阶段是否值得做主线派生接入** 的结论与后续选项。

---

## 2. sidewalk 派生映射

### 2.1 可直接来自 unified 的字段（概念对齐）

下列字段在 **语义上**与 unified 输出**同名或可直接拷贝**（派生实现时仍须把 `summary_schema_version` 写成 `sidewalk_env_summary_v1/1`，**不得**沿用 `unified_env_summary_v1/1` 作为 sidewalk 键的最终 schema 门禁）。

| sidewalk 字段 | unified 来源 | 说明 |
|---------------|----------------|------|
| `scene_candidate` | `scene_candidate` | 字符串一致传递；若仅走 unified，可与 unified 分类器输出一致。 |
| `event_timestamp` | `event_timestamp` | 同一观测时间口径（秒）。 |
| `summary_freshness` | `summary_freshness` | 若派生阶段**不再重算**，可直接拷贝；若与垂直信号重算并存，见 §4。 |
| `ttl_ms` | `ttl_ms` | 可拷贝；长期更优为 **sidewalk 专用 TTL**（env `LUNA_SIDEWALK_ENV_SUMMARY_TTL_MS`）与 unified 默认 **6000 ms** 显式择一策略。 |
| `confidence_weight` | `confidence_weight` | 可拷贝；若 sidewalk 侧重算 freshness，则应与 sidewalk 的 `_confidence_weight` 一致重算。 |
| `age_ms` | `age_ms` | 可拷贝（`now` 与 `event_timestamp` 一致时）。 |
| `inference_notes` | `inference_notes` | 可 **合并** unified 与 sidewalk 专用 note（实现阶段再定合并策略）；草案建议保留双方可追溯性。 |

### 2.2 必须继续保留的 sidewalk 垂直字段（unified 中不存在）

| 字段 | 说明 |
|------|------|
| `path_confidence` | 人行道/通行模型置信；**不等同**于 unified 的 `environment_confidence` 全语义，但 **可作为初值映射**：见 §4。 |
| `is_outdoor` | unified **不包含**；须继续由感知/规则或现有 sidewalk 上游提供，或由 **scene + 业务规则** 单独推断，**不得**从 `scene_family` 单独硬推。 |

### 2.3 unified 只能作为「参考来源」、不能直接当唯一真源的情况

| 情况 | 建议 |
|------|------|
| `scene_family == "retail"` | unified 面向 **店内零售**；与 `sidewalk_env_summary_v1` 契约**不一致**。不宜用 unified 单独填满 sidewalk dict；至多作为 **观测旁路** 或触发「降权 / 不写 sidewalk」策略。 |
| `scene_family == "unknown"` | 可拷贝公共时间与衰减字段，但 **`path_confidence` / `is_outdoor` 仍以垂直真源为准**；unified 的 freshness 与 sidewalk 内置规则可能不一致，**不宜**在未对齐规则前直接覆盖 sidewalk 稳定化输出。 |
| 上游已提供完整 `sidewalk_env_summary_v1`（含 schema） | **以现有垂直 summary 为准**；unified 仅用于对账、双轨对比，不覆盖。 |

---

## 3. retail 派生映射

### 3.1 可直接来自 unified 的字段（概念对齐）

| retail 字段 | unified 来源 | 说明 |
|-------------|----------------|------|
| `event_timestamp` | `event_timestamp` | 同一时间口径。 |
| `summary_freshness` | `summary_freshness` | 同 sidewalk：可直接拷贝或按 §4 与垂直重算择一。 |
| `ttl_ms` | `ttl_ms` | 可拷贝；长期建议与 **retail 专用 TTL**（`LUNA_RETAIL_ENV_SUMMARY_TTL_MS`）策略显式对齐。 |
| `confidence_weight` | `confidence_weight` | 同 sidewalk。 |
| `age_ms` | `age_ms` | 同 sidewalk。 |
| `inference_notes` | `inference_notes` | 可合并；retail 稳定化另有 `gating_passed` / `shelf_visible` 相关 note。 |

### 3.2 与 unified 的语义映射（非同名拷贝）

| retail 字段 | unified 来源 | 说明 |
|-------------|----------------|------|
| `scene_type` / `scene_type_candidate` | `scene_candidate` + `scene_family` | 仅当 `scene_family == "retail"`（或 unified 的 candidate 已能规范为 `retail_shelf` / `retail_aisle`）时，可向 retail 的规范化字符串 **投影**；否则维持 `unknown` 或 **不以 unified 强行填货架标签**。 |
| `retail_context_confidence` | `environment_confidence` | **初值映射**候选；retail 侧仍有 **shelf / gating** 参与 freshness 规则，见 §4。 |

### 3.3 必须继续保留的 retail 垂直字段（unified 中不存在）

| 字段 | 说明 |
|------|------|
| `shelf_visible` | 视觉/感知专用；**不能**从 unified 派生。 |
| `gating_passed` | 门闸/策略 bool；**不能**从 unified 派生。 |

### 3.4 unified 只能作为「参考来源」的情况

| 情况 | 建议 |
|------|------|
| `scene_family == "walkway"` | 与 retail 契约不一致；**不要**单靠 unified 写 `retail_env_summary_v1`；至多双轨观测。 |
| `scene_family == "unknown"` | `scene_type` 与 `retail_context_confidence` **以垂直真源为准**；unified 可作交叉检查。 |
| 上游已提供稳定化 `retail_env_summary_v1` | **以垂直 summary 为准**；unified 不覆盖。 |

---

## 4. 覆盖与保留规则

### 4.1 unified 字段与现有垂直字段冲突时

| 原则 | 说明 |
|------|------|
| **垂直真源优先** | 当 `metadata` 中已存在由感知链写入的 **sidewalk / retail 专用 dict**（且带各自 `summary_schema_version`）时，**派生层不得**用 unified 整段覆盖，除非产品明确「unified 优先」且另有开关（本阶段 **不引入**）。 |
| **家族不一致则不硬并** | `scene_family` 与目标 summary 类型不一致时（如 unified=retail 却要写 sidewalk），**不执行**「直接投影为唯一输出」；仅允许 **参考** 或 **并行观测**。 |
| **时效与置信** | `summary_freshness` / `confidence_weight`：若同时存在 unified 与垂直 builder 重算结果，草案建议 **以目标域 builder（sidewalk 或 retail）的语义为准**；unified 结果可用于 **shadow diff**，不默认覆盖。 |

### 4.2 哪些字段允许由 unified「覆盖」或填充（未来实现时）

| 目标 | 允许范围 |
|------|----------|
| 仅 **填充缺失键** | 当垂直 dict 缺少 `event_timestamp` / `ttl_ms` 等时，可用 unified **补缺**，并打 `inference_notes` 说明来源。 |
| **初值** | `path_confidence` ← `environment_confidence`（walkway 家族且策略允许时）；`retail_context_confidence` ← `environment_confidence`（retail 家族且策略允许时）。 |

### 4.3 哪些字段必须以垂直 summary / 上游为准

| 字段域 | 必须以垂直为准 |
|--------|------------------|
| sidewalk | `is_outdoor`；有争议时 **`path_confidence`** 以感知链为准。 |
| retail | `shelf_visible`、`gating_passed`；**货架级 scene 标签** 以感知或现网规则为准，unified 仅辅助。 |
| 双方 | 各自 `summary_schema_version` 命名空间 **保持独立**（`sidewalk_env_summary_v1/1`、`retail_env_summary_v1/1`）。 |

---

## 5. 当前阶段结论

### 5.1 是否建议直接进入「主线派生接入」

**不建议**在本草案未经过评审、也未做 **shadow / 双轨** 验证前，将 unified 派生写入 `dispatch_voice_final_text` 或替换现有稳定化路径。

**原因简述**：

- **家族错配**（walkway vs retail）与 **垂直专用字段**（`is_outdoor`、`shelf_visible`、`gating_passed`）会导致「看似统一、实则混源」的 metadata。
- **TTL 默认值**（unified 6000 ms vs sidewalk 5000 / retail 8000）与 **freshness 判定规则** 尚未在实现层对齐，直接接线易把差异写死。
- 现有主线已依赖 **单键 replace** 与 **秒退开关**；过早接 unified 会增加 **第三套语义**，回退面变大。

### 5.2 下一步更适合做什么

| 选项 | 说明 |
|------|------|
| **双轨 / shadow** | 在日志或 debug metadata 中并行记录 unified 输出与现有 sidewalk/retail builder 输出，**不改**主链消费契约。 |
| **最小实验接线** | 若后续要验证，仅加 **开发开关**、**只读旁路**，且明确不写回 `sidewalk_env_summary_v1` / `retail_env_summary_v1`。 |
| **保持双轨、不接主线** | 继续把 unified 当 **库能力**，派生规则冻结在本文件后再决策。 |

---

## 一句话收束

先把 **unified → sidewalk / retail** 的**继承、垂直保留、冲突与仅参考**规则写清楚，再决定是否做 **shadow 对比**或 **最小实验接线**；**当前不建议**直接把 unified 派生结果接进主线替代现有 builder。
