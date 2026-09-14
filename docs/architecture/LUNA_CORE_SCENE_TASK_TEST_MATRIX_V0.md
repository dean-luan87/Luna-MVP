# Phase-SceneTask-001 — Core Scene × Task Test Matrix v0（测试矩阵冻结）

**目的**：把 4 个核心场景的测试路径、输入 signals、预期 state transition、任务候选输出矩阵化。  
**注意**：所有输出为 candidate-only；不得触发真实执行。  

---

## 场景矩阵（A–N）

| 场景 | 场景类型 | 输入 signals（最小） | 预期 scene_phase | 预期任务候选/状态要点 |
|---|---|---|---|---|
| A sidewalk_clear_path_case | sidewalk_navigation | passability(clear) + risk(low) | moving_forward | 输出前进候选；deviation_detected=false |
| B sidewalk_obstacle_case | sidewalk_navigation | passability(blocked) + risk(obstacle) | obstacle_detected / slow_down_or_stop | 输出减速/停候选 |
| C sidewalk_low_confidence_case | degraded_scene | low confidence signals | passability_uncertain | degraded_mode=true；保守候选 |
| D road_crossing_wait_case | road_crossing | dynamic_event + risk | waiting | 不输出“真实通行命令” |
| E road_crossing_allowed_candidate_case | road_crossing | dynamic_event(light changed) + risk(low) | crossing_allowed_candidate | 仅候选；forced_crossing_decision_count=0 |
| F road_crossing_unsafe_case | road_crossing | vehicle_approaching + risk(high) | crossing_blocked_or_unsafe | 输出等待/停止候选 |
| G metro_sign_direction_case | metro_navigation | ocr(direction_board) | direction_candidate | 输出方向候选 |
| H metro_transfer_uncertain_case | metro_navigation | ocr缺失/低置信度 | uncertain_or_need_help | uncertain_scene_rate 增加；need_help 候选 |
| I hospital_registration_candidate_case | hospital_navigation | ocr(hospital_department/doorplate) | registration_or_consultation_candidate | 输出挂号/咨询候选 |
| J hospital_department_direction_case | hospital_navigation | ocr(direction_board/floor) | department_direction_candidate | 输出科室方向候选 |
| K inserted_task_recovery_case | any | inserted task marker | inserted/recovering | inserted_task_present=true；完成后 recovery_possible=true |
| L deviation_detected_case | any | deviation marker | recover_to_moving / correction_candidate | deviation_detected=true；输出纠偏候选 |
| M task_pause_resume_case | any | user pause/resume | paused -> recovering -> active | 状态一致；可回放 |
| N lost_or_degraded_case | uncertain/degraded | signals不足 | lost/degraded | need_human_help_candidate 输出；保守 |

