# Phase-Perception-001 — Navigation Perception Baseline Test Matrix v0（测试矩阵冻结）

**目的**：把 Perception-001 的测试场景与预期输出/指标矩阵化，确保 baseline 可复现、可验收、可停止。  
**注意**：本矩阵允许 mock/fixture/replay，不要求真机或工业级指标。  

---

## 场景矩阵（A–M）

| 场景 | 覆盖能力 | 预期 signal | 预期要点 |
|---|---|---|---|
| A stable_object_tracking_case | 连续帧稳定化 | object_stability_signal | object_id 稳定；stability_score 可输出 |
| B object_jitter_case | 抖动抑制 | object_stability_signal | jitter reduction 不频繁翻转 tracking_status |
| C object_lost_reappeared_case | 丢失/重现 | object_stability_signal | tracking_status 表达 lost/reappeared |
| D ocr_sign_case | OCR 标识牌 | ocr_navigation_signal | text_type=sign |
| E ocr_doorplate_case | 门牌/楼层 | ocr_navigation_signal | text_type=doorplate/floor_number |
| F ocr_direction_board_case | 方向牌 | ocr_navigation_signal | navigation_relevance 可输出 |
| G passability_clear_path_case | 通行性：可通行 | spatial_passability_signal | passable=true |
| H passability_blocked_case | 通行性：障碍 | spatial_passability_signal | passable=false 或 passability_score 低；obstacle_direction 尽量提供 |
| I dynamic_pedestrian_case | 动态事件：行人 | dynamic_event_signal | event_type=pedestrian_moving |
| J dynamic_vehicle_approach_case | 动态事件：车辆接近 | dynamic_event_signal | urgency_level 提升 |
| K risk_obstacle_case | 风险场：障碍 | risk_field_signal | risk_type=obstacle；recommended_handling 输出 |
| L risk_edge_or_step_case | 风险场：台阶/边缘 | risk_field_signal | risk_type=step/edge |
| M low_confidence_case | 安全保守性 | all | confidence 低；不得强行高确定结论；unknown 合法 |

---

## 指标覆盖映射（最小）

### 稳定性指标
- object_stability_signal_rate：A/B/C 覆盖
- tracking_jitter_reduction_rate：B 覆盖
- lost_reappeared_detection_rate：C 覆盖

### OCR 指标
- ocr_navigation_signal_valid_rate：D/E/F 覆盖
- ocr_text_type_classification_rate：D/E 覆盖
- ocr_navigation_relevance_present_rate：F 覆盖

### 空间/通行性指标
- passability_signal_valid_rate：G/H 覆盖
- obstacle_direction_present_rate：H 覆盖
- unknown_distance_rate：G/H/M 覆盖

### 动态事件指标
- dynamic_event_signal_valid_rate：I/J 覆盖
- urgency_level_present_rate：I/J 覆盖
- temporal_window_present_rate：I/J 覆盖

### 风险场指标
- risk_field_signal_valid_rate：K/L 覆盖
- risk_level_present_rate：K/L 覆盖
- recommended_handling_present_rate：K/L 覆盖

### 安全保守性指标
- low_confidence_forced_decision_count：M 覆盖
- unknown_output_rate：M 覆盖
- unsafe_overconfident_output_count：M 覆盖

