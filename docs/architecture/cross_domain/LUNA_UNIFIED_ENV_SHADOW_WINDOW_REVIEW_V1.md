# unified env shadow 首个观察窗口结论归档（V1）

## 1. 窗口输入与产物

- **窗口 JSONL**：`analyze_unified_env_shadow_out/window_unified_env_shadow_v1_20260410T060924Z.jsonl`
- **analyzer 输出**：
  - `analyze_unified_env_shadow_out/analyze_unified_env_shadow_v1_20260410T060935Z.json`
  - `analyze_unified_env_shadow_out/analyze_unified_env_shadow_v1_20260410T060935Z.md`

说明：本窗口用于验证「shadow 对照链路」端到端可跑通（可回放 JSONL → 产出统计与样本桶）。后续应替换为真实主线 trace 窗口（同 schema 的 JSONL 行）复跑，结论才可用于接线评审。

---

## 2. 三个关键问题的结果（本窗口）

### 2.1 scene_family_match_rate 是否可接受

- **scene_family_match_rate**：**0.8**（4/5）
- **family_mismatch_count**：**1**

解读：在该小窗口内，统一家族与「由命中垂直 summary 推导的期望家族」多数一致；但已出现典型的**字符串诱导错配**样本（见 §3）。

### 2.2 candidate_mismatch_count 主要集中在哪些样本

- **scene_candidate_match_rate**：**1.0**
- **candidate_mismatch_count**：**0**

解读：本窗口中 unified 的 `scene_candidate` 与 shadow 输入候选完全一致（符合当前 shadow 设计：候选来自命中垂直源的 candidate 字段）。

### 2.3 unified_helpful_fill_count 是否有实际价值

- **unified_helpful_fill_count**：**1**
- 命中样本：`w4_vertical_weak_missing_freshness`（垂直侧缺 `summary_freshness` / `summary_schema_version`，unified 仍能产出结构化 freshness+schema）

解读：说明 unified 具备**补缺潜力**（至少能在垂直较弱时补齐观测字段），但需在真实窗口上确认该类样本的**占比**与**误补风险**。

---

## 3. 主要错配样本类型（本窗口）

- **family mismatch**：`w5_mismatch_like`
  - 现象：垂直来源命中为 sidewalk，但 `scene_candidate` 字符串为 `retail_shelf`，导致 unified 判为 `retail`；而垂直侧「保守期望」为 `unknown`。
  - 解读：这是典型的「**家族错配风险仍在**」的实例：当垂直 dict 的 candidate 字符串携带跨域标签时，unified 的关键词分类会发生跨桶。

---

## 4. 三选一结论（本窗口）

**结论：继续双轨观察（不建议接线）。**

理由（对应当前阶段边界）：本窗口规模小且为回放样本，已能证明 analyzer 与样本桶机制有效，但不足以支撑进入最小接线评审；同时已出现家族错配样本，需在真实窗口上量化其频率与可控性。

---

## 5. 下一步建议（最小动作）

- **用真实主线窗口 JSONL 复跑**：优先选包含 sidewalk/retail 的近期窗口，复用同一 analyzer 输出结构。
- 复跑后再判断是否进入：
  - **维持双轨**（若错配集中且不可解释/不可控）
  - **最小接线实验评审**（若家族一致率、freshness 同向率稳定且错配可解释/可隔离）

---

## 一句话收束

先用真实窗口把 unified env 的一致率与错配类型量化出来，再决定是否值得进入最小接线实验评审；当前仍以双轨观察为主。

