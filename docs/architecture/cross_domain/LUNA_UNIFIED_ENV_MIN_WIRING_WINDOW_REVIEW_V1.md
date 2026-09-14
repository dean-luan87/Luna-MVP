# unified env 最小接线实验首个观察窗口结论归档（V1）

## 1. 窗口输入与产物

- **窗口 JSONL**：`analyze_unified_env_shadow_out/window_unified_env_min_wiring_v1.jsonl`
- **分析输出**：
  - `analyze_unified_env_shadow_out/analyze_unified_env_min_wiring_v1_20260410T073505Z.json`
  - `analyze_unified_env_shadow_out/analyze_unified_env_min_wiring_v1_20260410T073505Z.md`

说明：本窗口用于验证“最小接线实验”在边界锁死下的真实行为分布（补缺发生率、阻断原因分布、是否出现有效补缺）。窗口规模仍小，结论以“是否值得继续保留实验开关”优先。

---

## 2. 关键统计（本窗口）

- **row_count**：5
- **fill_applied_count**：1
- **effective_fill_count**：1
- **ineffective_fill_count**：4
- **blocked_family_candidate_mismatch_count**：0

### 2.1 filled_fields 分布

本窗口唯一一次有效补缺补齐了白名单五字段（完整补齐）：

- `summary_freshness`
- `ttl_ms`
- `confidence_weight`
- `age_ms`
- `inference_notes`

### 2.2 fill_blocked_reason 分布

阻断几乎全部来自“垂直已有值，不允许覆盖”（边界健康）：

- `target_has_value:summary_freshness`（4）
- `target_has_value:ttl_ms`（4）
- `target_has_value:confidence_weight`（4）
- `target_has_value:age_ms`（4）
- `target_has_value:inference_notes`（4）

---

## 3. 判断与解读

### 3.1 是否真的出现有效补缺

**是**：出现 1 次 effective fill，且补齐字段严格落在白名单内。

### 3.2 阻断是否主要集中在合理原因

**是**：主要阻断原因为 `target_has_value:*`，符合“不覆盖垂直真源”的硬边界。

### 3.3 实验是否有净正收益（初判）

初判为：**有轻微正收益，但仍需扩大窗口确认**。

- 正收益：在“垂直缺观测字段”的场景里 unified 能补齐白名单字段，且未越界。
- 不足：当前有效补缺样本数少，是否稳定出现仍需更大真实窗口。

---

## 4. 三选一结论

**结论：继续维持最小接线实验（保持当前边界不放松）。**

理由：本窗口已出现有效补缺且阻断理由健康；在未扩大窗口前撤回会过早丢失证据累积能力。

---

## 5. 下一步最小动作

- 扩大真实窗口（同开关）跑更长窗口，重点观察：
  - `fill_applied_count` 是否稳定 > 0
  - effective fill 是否集中于某类“垂直缺观测字段”场景
  - 是否出现 `family_candidate_mismatch` 大规模阻断（若出现需回溯家族护栏或输入构造）

---

## 一句话收束

最小接线实验在首个窗口中已出现有效补缺且边界健康；先继续保留实验开关并扩大窗口，再用数据决定是否撤回到纯 shadow 或扩大补缺范围。

