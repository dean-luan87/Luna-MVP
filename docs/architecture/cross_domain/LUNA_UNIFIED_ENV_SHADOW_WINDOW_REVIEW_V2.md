# unified env shadow 第二观察窗口（真实主线 trace）结论归档（V2）

## 1. 本轮目标与结论

目标：基于真实主线运行时落盘的 `unified_env_shadow_snapshot` JSONL，跑 `tools/analyze_unified_env_shadow_v1.py` 得到第二窗口指标与错配样本，并据此更新结论。

**本轮结论（三选一）**：继续双轨观察，暂不建议接线。

依据：第二窗口（snapshot）在 **family 护栏修正前** `scene_family_match_rate=0.8`，且错配集中在“字符串诱导的家族错配”。在 **按最小护栏修正后**（见 `unified_env_summary_v1` 的 hint 冲突护栏），用同一份窗口输入重跑对照，`scene_family_match_rate` 提升到 **1.0**，`family_mismatch_count` 下降到 **0**；`scene_candidate_match_rate` 仍为 **1.0**（candidate 未被破坏）。

---

## 2. 窗口输入与产物（V2）

### 2.1 原始 snapshot JSONL（主线落盘）

- `analyze_unified_env_shadow_out/unified_env_shadow_snapshot_v1_window2.jsonl`

该文件每行形态为：
`{\"type\":\"unified_env_shadow_snapshot\",\"data\":{...}}`

### 2.2 analyzer 输入扁平化（供脚本消费）

由于 analyzer 的 `--input-jsonl` 期望每行是 `{id,event_timestamp,metadata}`，本窗口将 snapshot JSONL 扁平化为：

- `analyze_unified_env_shadow_out/unified_env_shadow_snapshot_v1_window2_flat.jsonl`

### 2.3 analyzer 输出

- **修前（baseline）**：
  - `analyze_unified_env_shadow_out/analyze_unified_env_shadow_v1_20260410T063302Z.json`
  - `analyze_unified_env_shadow_out/analyze_unified_env_shadow_v1_20260410T063302Z.md`
- **修后（使用 `--use-dispatcher-attach` 以复用主线 shadow 输入逻辑 + hint 护栏）**：
  - `analyze_unified_env_shadow_out/analyze_unified_env_shadow_v1_20260410T065739Z.json`
  - `analyze_unified_env_shadow_out/analyze_unified_env_shadow_v1_20260410T065739Z.md`

---

## 3. 本窗口指标（V2）

### 3.1 修前（baseline）

- **fixture_count**：5
- **scene_family_match_rate**：0.8
- **scene_candidate_match_rate**：1.0
- **family_mismatch_count**：1
- **candidate_mismatch_count**：0
- **unified_helpful_fill_count**：0
- **freshness_alignment_summary**：`{\"equal\": 5}`

### 3.2 修后（family 护栏最小收紧）

- **fixture_count**：5
- **scene_family_match_rate**：1.0
- **scene_candidate_match_rate**：1.0
- **family_mismatch_count**：0
- **candidate_mismatch_count**：0
- **unified_helpful_fill_count**：0
- **freshness_alignment_summary**：`{\"equal\": 5}`

---

## 4. 主要错配样本类型（V2）

修前与 V1 一致，错配主要集中在**字符串诱导的家族错配**：

- `family:unified=retail,vertical_expected=unknown,source=sidewalk`

即：垂直来源命中 sidewalk，但 `scene_candidate` 字符串携带 retail 标签时，unified 的关键词分类会跨桶。

修后：该错配在本窗口中 **消失**（`family_mismatch_count=0`）。

```json
{
  "id": "optional",
  "event_timestamp": 123.0,
  "metadata": {
    "sidewalk_env_summary_v1": { "...": "..." },
    "retail_env_summary_v1": { "...": "..." },
    "unified_env_summary_shadow_v1": { "...": "..." }
  }
}
```

其中：
- `metadata` 是本轮 voice 主线可观测的 metadata 快照（或等价的 runtime_context.metadata 子集）。
- 至少应包含一条垂直摘要（sidewalk 或 retail）以及 shadow key，才能做“命中垂直源 → 期望家族”对照。

---

## 5. 当前阶段判断

### 5.1 是否进入最小接线评审

**暂不进入**（仍保持双轨）。虽然本窗口修后 `scene_family_match_rate` 已提升至 1.0，但样本量仍小，且本轮修正属于“最小护栏”验证，需要扩大真实窗口确认：\n\n- 提升是否在更大窗口中稳定\n- 是否引入新的未知错配类型\n\n在稳定性确认前，不建议进入最小接线评审。

---

## 6. 下一步建议（仍不接线）

- 扩大真实窗口样本量（同开关，跑更长窗口），复用 analyzer 输出错配样本桶，确认：\n  - 家族一致率是否稳定上升/稳定在更高水平\n  - 错配是否仍高度集中在“字符串诱导”这一类\n  - `unified_helpful_fill_count` 是否在更大窗口里出现稳定价值
- 若后续一致率显著提高且错配可隔离，再进入“最小接线评审”（仍先从只读/补缺开始）。

---

## 7. 三选一（本轮）

**继续双轨观察，暂不建议接线。**

---

## 一句话收束

第二窗口已可基于 snapshot JSONL 跑通，但核心家族一致率仍不足以进入接线评审；继续双轨观察、扩大真实窗口样本量后再判断。

