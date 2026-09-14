# unified env 最小接线实验方案（V1）

## 1. 目标

在《`LUNA_UNIFIED_ENV_MIN_WIRING_REVIEW_V1.md`》已给出“**具备进入最小接线实验资格**”的结论后，本方案定义一条**极保守**的接线实验路径，用于回答：

- unified env 是否能在**不改变任何行为**的前提下，为垂直 summary 提供**低风险补缺收益**
- 补缺是否稳定、是否值得继续投入（或仍应保持纯观察）

本方案只做实验设计，不做实现。

---

## 2. 实验边界（必须锁死）

### 2.1 unified env 的定位

- **只读参考 / 补缺来源**：unified env 只提供“可观测字段”的补缺，不成为任何旁路/主线的决策输入。

### 2.2 明确禁止（硬约束）

- **禁止覆盖垂直真源**：不得覆盖 `sidewalk_env_summary_v1` / `retail_env_summary_v1` 中已存在的字段值。
- **禁止驱动主线决策**：不得影响分流、orchestrator 顺序、gating、真实输出。
- **禁止触碰并列域**：不得读写/改写 `risk_summary_v1`、`find_item_intent_summary_v1`、`ocr_summary_v1`。
- **禁止替换**：不得将 unified 用作垂直 summary 的替代品；不得引入“统一替换/统一 schema 重构”。

---

## 3. 允许补缺的字段（白名单）与禁止补缺（黑名单）

### 3.1 白名单：允许补缺的“非决策性字段”

仅允许补缺以下字段（且仅在目标垂直 summary 缺失时补齐）：

- `summary_freshness`
- `ttl_ms`
- `confidence_weight`
- `age_ms`
- `inference_notes`

**原因**：上述字段属于“观测/时效/解释”层，补齐后主要提升可观测性与一致性，不应改变垂直语义本体。

### 3.2 黑名单：明确禁止补缺的字段

禁止由 unified 补缺/写入以下字段（即使垂直缺失也不补）：

- `scene_family`
- `scene_candidate`
- 任何会改变垂直语义归类的字段（如零售 `scene_type*`、人行道 `is_outdoor`、`path_confidence`）
- 任何可能参与 gating / 分流 / 输出决策的字段（哪怕当前实现未消费，也禁止先写）

**原因**：这些字段一旦被补，会形成隐性“接管”或改变旁路输入语义，违反本实验的“低风险补缺”边界。

---

## 4. 接线位置建议（最小侵入）

### 4.1 推荐位置

在 `dispatch_voice_final_text` 的以下阶段之间进行最小补缺（概念位置，具体实现时对齐现有函数调用顺序）：

1. `sidewalk_env_summary_v1` / `retail_env_summary_v1` 已完成稳定化（若开关开启）
2. `unified_env_summary_shadow_v1` 已计算/写入（或可从同源输入得到）
3. **在旁路编排（orchestrator）之前**，但补缺只能写入**独立 debug/whitebox 键**或“垂直 summary 的非决策字段子域”（见 §4.2），以确保不会影响旁路输入读取路径

### 4.2 推荐写入形态（避免污染垂直真源）

为了严格满足“不覆盖垂直真源”，建议优先写入**独立键**（而不是直接写回垂直 dict）：

- `metadata["unified_env_fill_shadow_v1"] = { ... }`
  - 记录：命中垂直源、补缺候选字段、哪些字段原来缺、最终补了什么

若必须把补缺结果与垂直 summary 同处一键，也只能写入：

- `metadata["sidewalk_env_summary_v1"]["_unified_fill_non_decision_v1"] = {...}`
- `metadata["retail_env_summary_v1"]["_unified_fill_non_decision_v1"] = {...}`

并且该子域**不得**被旁路消费（仅供观测与离线分析）。

### 4.3 幂等与回退

必须具备：

- **幂等**：同一轮/同一 request 不重复补缺、不产生累积变异（例如通过 `fill_schema_version` 或 `fill_applied=true` 标记）。
- **秒退**：独立开关控制（默认关闭）；关闭后完全零侵入、不落任何补缺痕迹。

---

## 5. 观测要求（最小 telemetry）

### 5.1 必须记录“发生了补缺”

无论补缺是否发生，都必须留痕一条“补缺尝试”记录，推荐写入独立键：

- `metadata["unified_env_fill_shadow_v1"]`

最小字段建议如下（字段名写死，便于后续 analyzer 扩展但当前不要求实现统计）：

- `fill_applied`：`true/false`
- `target_summary_key`：`"sidewalk_env_summary_v1"` 或 `"retail_env_summary_v1"`
- `fill_source`：固定为 `"unified_env_summary_shadow_v1"`
- `filled_fields`：字符串数组，列出本次实际补入的字段（只能来自白名单）
- `fill_blocked_reason`：字符串数组；当 `fill_applied=false` 或仅部分补入时，记录阻塞原因（例如 `target_has_value:<field>`、`blacklisted:<field>`、`family_candidate_mismatch`、`missing_unified_shadow`）
- `related_unified_schema_version`：例如 `"unified_env_summary_v1/1"`（用于对账）

> 约束：该记录只用于观测与离线分析，不得被旁路消费为输入。

### 5.2 补缺价值判断（口径）

至少定义两类口径，用于后续窗口评审：

- **有效补缺（effective_fill）**：
  - 垂直 summary 原本缺失白名单字段（例如缺 `summary_freshness`）
  - unified 成功补入 ≥ 1 个白名单字段
  - 且不触发任何覆盖（不改已有字段）
- **无效补缺（ineffective_fill）**：
  - 没有补到任何字段（`filled_fields=[]`），或
  - 虽补入字段，但后续窗口观察显示“无消费价值/无增益”（仅作为后续评审维度，不在本实验内自动裁决）

本实验阶段不要求自动打分，只要求把“发生了什么”记录清楚，能在窗口复盘时做人工裁决。

### 5.3 风险约束（更保守的补缺门禁）

写死一条保守门禁：

- **只要 unified 与垂直 summary 在 family/candidate 上不一致，本次补缺直接禁止**（`fill_applied=false`，`fill_blocked_reason` 含 `family_candidate_mismatch`）。

理由：当前实验目标是“低风险补缺”，而不是让 unified 介入语义归类；一旦出现不一致，补缺可能掩盖更深层错配，应该让样本进入错配桶而不是被补缺“抹平”。

### 5.4 观测产物（写到哪里）

本实验阶段不把补缺结果混入垂直 summary 的顶层字段，统一写入：

- `metadata["unified_env_fill_shadow_v1"]`

其中至少包含（与 §5.1 对齐）：

- `target_summary_key`
- `filled_fields`
- `fill_applied`
- `fill_blocked_reason`
- `related_unified_schema_version`

---

## 6. 当前阶段不做项（写死）

- 不覆盖垂直已有字段（即使 unified 给出不同值也不覆盖）
- 不补 `scene_family`
- 不补 `scene_candidate`
- 不驱动分流/决策/输出
- 不自动扩大白名单（新增补缺字段必须走评审）
- 不改 `risk_summary_v1` / `find_item_intent_summary_v1` / `ocr_summary_v1`
- 不把 `unified_env_fill_shadow_v1` 当正式数据源（只观测、只对照）

---

## 一句话收束

先把 unified env 的最小接线实验限制在“**只读补缺 + 独立留痕 + 不影响决策**”范围内，再用补缺观测结果判断它是否真的值得进入更深一层接线。

