# sidewalk_env_summary_v1 上游 context 稳定化方案（V1）

## 1. 目标

### 1.1 为什么现在要补稳定化

`sidewalk_nav_v1` 已在主线完成 **Level 1 / whitebox-only 深接入**（见《[LUNA_SIDEWALK_NAV_V1_DEEP_INTEGRATION_IMPLEMENTED_NOTE.md](./LUNA_SIDEWALK_NAV_V1_DEEP_INTEGRATION_IMPLEMENTED_NOTE.md)》），但其上游输入 `VoiceRuntimeContext.metadata["sidewalk_env_summary_v1"]` 目前只有**三个最小字段**，由主线在缺失时回落为 `unknown/0/false`。这会导致：

- 摘要**抖动大**：同一物理场景下若上游写入不一致，白盒结论会跳变；
- **可复用性差**：没有统一的时间戳、置信度衰减与来源标注，难以做回归与对账；
- **事实与推断混用**：`path_confidence`、`scene_candidate` 在管线未接全时容易被当成强事实使用。

本方案**不扩真实输出**、**不改 risk 优先压制关系**，只把「环境摘要应长成什么样、如何时效与衰减、如何与 risk 并行」写清楚，为后续**最小实现**提供边界。

### 1.2 本方案解决什么问题

- 明确 **sidewalk_env_summary_v1** 的字段分层（强事实 / 弱推断 / 仅白盒）；
- 明确 **TTL、刷新、降权、作废** 规则，减少无依据的“长期有效场景假设”；
- 明确与 **risk_summary_v1** 的边界：**并行、不互写、risk 仍优先**；
- 预留未来 **统一环境层** 时 sidewalk 摘要的迁移位置。

---

## 2. 当前现状

### 2.1 sidewalk_nav_v1 依赖的最小 context

主线从 `runtime_context.metadata["sidewalk_env_summary_v1"]` 读取 `dict`，并映射到 `SidewalkEnvironmentInput`（见 `voice_final_text_dispatcher.py::_maybe_attach_sidewalk_nav_v1_whitebox` 与 `sidewalk_nav_v1/evaluate.py`）：

| 字段 | 类型意图 | 缺失时主线行为 |
|------|----------|----------------|
| `scene_candidate` | 场景候选标签（字符串） | `"unknown"` |
| `path_confidence` | 路径/人行道相关置信度 [0,1] | `0.0` |
| `is_outdoor` | 是否在室外 | `false` |

旁路内部再经 `_classify_scene` 得到 `scene_type`、`sidewalk_detected`、`sidewalk_confidence`，并写入白盒 `scene_summary`（含 `classified_scene_type`）。

### 2.2 场景事实 vs 弱推断（当前口径）

| 内容 | 归类 | 说明 |
|------|------|------|
| 传感器/地图明确给出的「当前在室外」布尔 | **强事实**（若来源可信） | 需带来源与采集时间；当前常缺 |
| `scene_candidate == "outdoor_walkway"` | **弱推断或上游标签** | 依赖标注管线质量；V1 规则直接信任字符串 |
| `path_confidence` | **弱推断** | 无统一校准与来源时，不宜当硬阈值事实 |
| `classified_scene_type`、`sidewalk_detected` | **派生字段** | 由旁路从上述输入推出，属白盒观测，非独立真源 |

### 2.3 当前不稳定点

- **无时间维度**：摘要不要么全信要么全默认，无法表达“过期”或“变旧”；
- **无来源与版本**：同一 key 可能被多模块写入，无法对账；
- **与 risk 同挂在 `metadata` 下但无契约**：易出现“用 risk 字段修补 sidewalk”或反向污染的工程冲动（当前代码未做，但缺少文档约束）。

---

## 3. 建议字段分层（方案级，非本阶段实现承诺）

以下建议在**未来**实现 `sidewalk_env_summary_v1` 时采用；字段名可与实现微调，但分层语义应保留。

### 3.1 强事实字段（应可校验、可追责）

- `observed_at_ms` 或 `summary_timestamp_ms`：摘要生成或观测时间（UTC 毫秒）；
- `source`：单一主来源枚举（例如 `perception_v1` / `map_fusion_v1` / `manual_debug`）；
- `source_version` 或 `schema_version`：便于回放与回归对齐；
- （可选）`is_outdoor`：仅当来源为强感知/地图且带置信下限时写入；否则应标为推断。

### 3.2 弱推断字段（必须带置信或不确定性说明）

- `scene_candidate`：保留，但建议增加 `scene_candidate_confidence`（0–1）或与 `source` 绑定解释；
- `path_confidence`：明确为**路径/可通行性模型输出**，不是 risk；
- `inference_notes`（短字符串枚举列表）：如 `["rule_fallback", "low_light"]`，供白盒与聚合，不进入播报。

### 3.3 仅供白盒使用的字段

- `debug` / `raw_features_ref`：指针或哈希，指向离线包/日志，不承诺稳定 API；
- 旁路写入的 `scene_summary.classified_*`：已在白盒内，**不应回写**进 `sidewalk_env_summary_v1`（避免循环）。

---

## 4. 时效与衰减（建议规则）

### 4.1 建议 TTL（按来源分级）

| 来源类型 | 建议 TTL | 说明 |
|----------|----------|------|
| 高频视觉/定位 | 0.5–2 s | 与帧率/定位频率对齐；过期即降权 |
| 地图/区域推断 | 5–30 s | 变化慢，但仍需过期，避免“人已进室内仍当室外” |
| 手工/调试注入 | 显式 TTL 或由会话结束清除 | 防止污染长会话 |

具体数值在实现阶段按硬件与管线再定；本方案只要求：**必须有 TTL 概念**，禁止“一次写入永久有效”。

### 4.2 何时刷新

- 新的观测与旧摘要**同源同 schema** 且时间更新 → **整段替换**（或按字段合并策略在实现文档中写死）；
- 来源切换 → 建议**作废旧摘要**再写新摘要，避免混源拼接。

### 4.3 何时降权

- 超过 TTL 但未收到新观测：不删除 key 时可写入 `stale=true` + `stale_reason="ttl_expired"`（方案字段），旁路侧对 stale 摘要**不提升** `sidewalk_detected` 置信；
- 连续多帧与上一摘要冲突：降权或标 `ambiguous=true`，由白盒记录，不强行选边。

### 4.4 何时直接作废

- 会话结束 / `session_id` 变更；
- 显式 `reset` 信号（例如场景切换、用户退出导航上下文）；
- 摘要 schema 版本不兼容（`schema_version` 不匹配）。

---

## 5. 与 risk_summary_v1 的关系

### 5.1 并行存在

- `sidewalk_env_summary_v1`：描述**环境与通行相关**输入；
- `risk_summary_v1`：描述**安全与风险**输入；
- 两者**并列**挂在 `VoiceRuntimeContext.metadata`，由 orchestrator 顺序与旁路各自只读，**不互相合并为单一 dict**。

### 5.2 哪些字段不能互相覆盖

- **禁止**用 `risk_summary_v1` 的字段去填充或修正 `scene_candidate` / `path_confidence` / `is_outdoor`（反之亦然）；
- **禁止**在 sidewalk 摘要中写入 `risk_level` 等风险语义（风险只读 `risk_summary_v1`）；
- 若未来需要“风险导致的场景不可用”，应通过 **risk 压制旁路输出**（现有 `output_suppressed_by_risk` 路径），而不是改环境摘要。

### 5.3 为什么 risk 仍然优先

- 安全链优先级高于通行提示是产品与安全边界；
- 当前实现已写死：high/critical 或 `risk_interrupt_preempt` 时压下 sidewalk 普通导航提示；稳定化方案**不改变**该顺序。

---

## 6. 后续演进边界

### 6.1 未来统一环境层时 sidewalk 的位置

建议演进为：

- **统一环境层**（例如 `unified_env_context_v1`）产出：时间、坐标系、室内外、可通行区域摘要等；
- **sidewalk_env_summary_v1** 作为其**派生视图（view）**：只保留人行道导航需要的子集 + 派生置信度；
- `sidewalk_nav_v1` 仍只依赖 **sidewalk 视图 + risk_summary_v1**，不直接依赖统一层全量字段，避免旁路膨胀。

### 6.2 当前阶段明确不做

- 不实现上述字段（本文件仅为方案）；
- 不让 sidewalk 进入真实输出候选；
- 不调整 orchestrator 顺序与 risk 压制规则；
- 不接真实视觉/地图管线（与现有 implemented note 一致）。

---

## 一句话收束

先把 **sidewalk_env_summary_v1** 的字段分层、时效衰减及与 **risk_summary_v1** 的并行边界写清楚，再决定是否进入上游环境摘要的**最小实现**与统一环境层演进。
