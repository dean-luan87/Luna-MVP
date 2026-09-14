# 中风险场景样本库（采集指引）

用于触发 **EDGE → SAFE_EDGE → CAUTION** 的素材类型，便于验证 SAFE_EDGE_to_CAUTION_ratio（理想 0.3–0.6）和系统提前预警能力。

---

## 目标

- 出现明显的 **SAFE → CAUTION**，但不至于持续高危。
- 观察：CAUTION 前是否先出现 SAFE_EDGE、持续几秒、比例是否在 30%–60%。

---

## 推荐素材类型

| 类型 | 说明 | 预期表现 |
|------|------|----------|
| **人行道 + 行人穿行** | 固定机位或慢速前进，行人横穿或靠近 | 行人进入视野 → EDGE/SAFE_EDGE → 若持续接近 → CAUTION |
| **商场/地铁入口** | 人流进出、多目标移动 | 多目标、遮挡变化 → 间歇 EDGE/CAUTION |
| **复杂路口** | 十字/丁字、车/人混行 | 多方向运动、盲区变化 → SAFE_EDGE 与 CAUTION 交替 |
| **多目标移动** | 室内多人、室外多人/车 | 目标数↑、轨迹交叉 → risk_score 与 CAUTION 占比上升 |
| **遮挡/光照变化** | 进出隧道、树影、逆光 | 短暂 EDGE/SAFE_EDGE，可用于测试振荡与恢复 |

---

## 采集建议

- **时长**：单段 1–3 分钟即可，便于 suite 跑完。
- **标注**：文件名或目录可带 `medium_` 前缀，例如 `medium_mall_01.mp4`、`medium_crossing_01.mp4`。
- **与 easy 的区分**：easy 以“空旷、单目标、少遮挡”为主；medium 刻意增加行人/多目标/路口/入口等要素。

---

## 纳入 Suite

采集后加入回归：

```bash
python3 tools/run_trace_suite.py \
  --video video-1m01s.mp4 --label easy_01 \
  --video video-2m01s.mp4 --label easy_02 \
  --video medium_mall_01.mp4 --label medium_01 \
  --output logs/trace_report.json
```

查看报告中的 **SAFE_EDGE_to_CAUTION_ratio**、**CAUTION_ratio**、**mode_values_seen** 即可判断中风险行为是否符合预期。

---

## 高风险（hard）参考

- **用途**：验证系统能稳定进入 CAUTION、且 SAFE_EDGE 不干扰判断。
- **素材**：持续密集人流、快速接近目标、夜间/低照度、复杂路口长时间等。
- **预期**：risk_score 与 EDGE/CAUTION 明显升高；若仍多为 SAFE，则阈值可能过保守。
