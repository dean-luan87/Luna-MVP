# Spatiotemporal Continuity Reserve M0（时空间连续性接口预留层 M0）交付

## 1. 定位（写死）

时空间连续性属于内部强影响因子，会影响候选可信度、active path 延续、hypothesis 保留与用户反馈是否打断路径。  
本轮只做 **接口预留 + 结果性影响摘要**：

- 后端保留连续性影响表达位
- 结构树可轻挂接连续性影响摘要
- 前端默认只展示“连续性对当前结果的影响”

明确不做：连续帧跟踪算法、复杂评分系统、时间衰减/空间继承模型重构、多帧轨迹重建与调试台。

## 2. 交付件

- 实现：`decision_monitor/spatiotemporal_continuity_reserve.py`
- 接入：`decision_monitor/schema.py` + `decision_monitor/builder.py`（字段 `spatiotemporal_continuity_reserve`）
- 结构树轻挂接：`decision_monitor/reasoning_structure_tree.py`（root 摘要附一句 continuity）
- Console：`tools/reasoning_console_aggregator.py` + `tools/reasoning_console_server.py`
- 单测：`tests/test_spatiotemporal_continuity_reserve.py`
- smoke/JSONL：`tools/smoke_spatiotemporal_continuity_reserve.py`

## 3. 数据结构：SpatiotemporalContinuityReserveResult

- continuity_support_level（high/medium/low/broken/unknown）
- continuity_influence_reason（一句话影响摘要）
- continuity_preserved / continuity_broken
- continuity_affected_module
- continuity_source_summary（轻摘要）
- continuity_debug_note（前端默认不主展示）
- continuity_reserve_applied

## 4. 最小规则（M0）

- **反馈打断**：有 raw feedback 且 next_effect!=none → broken
- **弱连续性**：blocked/severe issue → low
- **粗继承**：无 feedback、趋势稳定、存在推荐格/主建议 → medium/high
- 否则 unknown

## 5. CONTRACT 强约束（写死）

时空间连续性属于内部强影响因子。后续必须进入白盒与结构树依据层；前端默认只展示其对当前决策的结果性影响，不默认直出底层 continuity 原始细节。

## 6. 结论（M0）

连续性接口预留层已占坑并接入 frame/JSONL/Console；当前仅输出影响摘要，为后续 continuity 引擎展开预留接口。

