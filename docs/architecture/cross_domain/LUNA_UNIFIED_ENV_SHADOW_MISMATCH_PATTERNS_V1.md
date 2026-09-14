# unified env shadow 错配模式清单（V1）

## 1. 目标

在已有两轮窗口（V1 回放窗口、V2 snapshot 真实窗口）对照结果的基础上，把 unified env 的“错配”归因收口成**可操作的错误模式清单**，用于决定下一步是：

- **路线 A**：对 unified 的 `scene_family` 归类规则做小修正（优先）
- **路线 B**：不改 builder，继续扩大双轨窗口观察（备选）

本文件只做**错配归因清单**，不提出接线方案，不改代码。

---

## 2. 数据来源（两轮窗口）

- **窗口 V1（回放验证）**
  - analyzer：`analyze_unified_env_shadow_out/analyze_unified_env_shadow_v1_20260410T060935Z.json`
  - 结论归档：`LUNA_UNIFIED_ENV_SHADOW_WINDOW_REVIEW_V1.md`
- **窗口 V2（snapshot 真实主线）**
  - analyzer：`analyze_unified_env_shadow_out/analyze_unified_env_shadow_v1_20260410T063302Z.json`
  - 结论归档：`LUNA_UNIFIED_ENV_SHADOW_WINDOW_REVIEW_V2.md`

共同结论（高信号）：

- **candidate 层稳定**：`scene_candidate_match_rate = 1.0`
- **family 层不稳**：`scene_family_match_rate = 0.8`
- **错配模式重复出现**：同一类型在两轮均出现

---

## 3. 错配模式清单（V1）

### P0：字符串诱导的家族错配（重复出现）

- **定义**：命中垂直来源为 `sidewalk`（shadow 输入来自 `sidewalk_env_summary_v1.scene_candidate`），但 `scene_candidate` 字符串携带 `retail_*`（或其它 retail marker）时，unified 关键词归类为 `retail`；而垂直侧保守期望家族为 `unknown`（或 walkway）。
- **两轮均出现的样本形态**：
  - V1：`w5_mismatch_like`（`vertical_source=sidewalk`，`scene_candidate=retail_shelf`）
  - V2：`vertical_source=sidewalk` 且 `scene_candidate=retail_shelf` 的同型错配（见 V2 analyzer mismatch 样本）
- **根因假设**（面向后续修正）：unified 的 family 分类器基于 `scene_candidate` 的关键词匹配，缺少“来源域约束 / 交叉校验”，导致 candidate 字符串跨域污染时跨桶。
- **建议处置优先级**：最高（该模式会直接拉低 family 一致率；且可通过规则收紧/加护栏解决）。

### P1：hint 误导型错配（当前未在两轮窗口中观察到）

- **定义**：`raw_family_hint` 在 `scene_candidate` 不明确时将 family 归类到 walkway/retail，但与垂直侧强信号冲突。
- **当前状态**：两轮窗口均未出现明确证据（样本中未使用 hint 驱动 family）。
- **下一步**：扩大窗口时继续监控；若出现则单列统计“hint 介入次数与误导率”。

### P2：unknown 回落不合理（当前未在两轮窗口中观察到）

- **定义**：垂直侧强置信（例如 `path_confidence` / `retail_context_confidence` 高），但 unified 仍回落 `unknown` 或 `ambiguous`，导致 unified_unknown_vertical_confident 类样本增多。
- **当前状态**：两轮窗口未出现该类样本（`unified_unknown_but_vertical_confident=false`）。
- **下一步**：扩大窗口后再判断是否需要增强“unknown → family”的保守提升规则。

### P3：垂直侧弱导致的“伪错配”（补缺相关）

- **定义**：垂直 summary 缺少 `summary_schema_version` / `summary_freshness` 等稳定化字段，导致对照侧“期望家族/时效”推导不完整；unified 产出结构化结果时看似不一致，但本质是垂直缺字段。
- **证据**：
  - V1：出现 `unified_helpful_fill_count=1`（缺 freshness/schema 的垂直样本）
  - V2：`unified_helpful_fill_count=0`（本轮真实窗口未体现）
- **解读**：补缺价值可能是**偶发**或样本量不足；需要更大真实窗口才能判断其稳定性。

---

## 4. 结论（面向下一步）

### 4.1 当前最该修的不是 candidate，而是 family

两轮一致结论表明：**candidate 层稳定**，问题收缩在 **scene_family 归类规则**，且 P0 模式已重复出现。

### 4.2 二选一建议

- **倾向路线 A（小修正）**：先针对 P0 加一层“来源域护栏/收紧 retail marker 边界”的最小修正，再继续双轨观察验证 family 是否显著提升。
- **路线 B（继续观察）**：若担心修正规则引入新错配，可先扩大窗口（但当前已不是“没看到问题”，而是“问题重复出现”。）

---

## 一句话收束

unified env 目前更适合做参考/观察层；错配已收敛为以 **P0（字符串诱导的家族错配）** 为主的可修问题。下一步更适合先做 `scene_family` 规则的小修正，再继续双轨观察验证。

