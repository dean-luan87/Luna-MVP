# Phase-Perception-001 — Navigation Perception Baseline Definition v0（定义冻结）

**阶段名**：Phase-Perception-001  
**性质**：baseline definition freeze；不是完整世界模型；不是全场景视觉能力；不是任务链/地图融合  
**硬约束**：不接第二个模型；不做多模型调度；不做模型放权；不进入 full controlled trial；不扩大真实 side effects 面；不启用默认路径  

---

## 0) 后续执行约束（写死）

**工业级要求分期进入**；当前做不了的先进入 placeholder 并标明归属阶段，`blocking_current_phase=false`：  
- 不得阻塞当前阶段停止条件  
- 不得被遗忘（必须有 planned_phase 与可追踪 id）

---

## 1) 唯一目标

建立“视角导航感知基线 v0”，使系统具备支撑后续核心场景链开发的最小感知能力。

一句话：Perception-001 不是做完整视觉大脑，而是做视角导航所需的最小可用感知底座。

---

## 2) 非目标（写死）

- 不做完整世界模型
- 不做全场景识别/长尾物体库
- 不做多模型调度/模型放权
- 不做地图融合/任务链融合
- 不做真机性能总验收
- 不做高级表达链
- 不扩大真实 side effects 面/不启用默认路径

---

## 3) 输入依赖（已成立事实）

- Governance 主链已收口（Phase-Closure-001）
- Phase-Model-001 已冻结（bounded model integration constitution）
- Phase-Model-002 已完成（单模型 shadow integration）
- Phase-Model-003 admission baseline = conditional_go（无 hard blocker）
- 模型无执行权，仅 candidate/shadow 辅助
- default path disabled；full controlled trial 未进入；side effects 面未扩大

---

## 4) 本阶段范围（仅五类感知能力）

本阶段只覆盖：
1. 连续帧目标稳定化  
2. OCR 场景化理解  
3. 空间关系 / 距离 / 通行性基础判断  
4. 动态目标 / 动态事件基础识别  
5. 风险场基础版  

---

## 5) 输出交付物（v0）

1. baseline definition（本文）  
2. perception signal contract：`docs/architecture/LUNA_NAVIGATION_PERCEPTION_SIGNAL_CONTRACT_V0.md`  
3. test matrix：`docs/architecture/LUNA_NAVIGATION_PERCEPTION_BASELINE_TEST_MATRIX_V0.md`  
4. validation tool：`tools/validate_navigation_perception_baseline_v0.py`  
5. go/no-go pack：`docs/architecture/LUNA_NAVIGATION_PERCEPTION_BASELINE_GO_NO_GO_PACK_V0.md`  
6. industrial placeholder register：`docs/architecture/LUNA_INDUSTRIAL_GRADE_PLACEHOLDER_REGISTER_V0.md`  

---

## 6) 完成指标（最小指标体系，非工业级）

必须建立并由 validation tool 输出（至少）：

### A. 稳定性指标
- `object_stability_signal_rate`
- `tracking_jitter_reduction_rate`
- `lost_reappeared_detection_rate`

### B. OCR 指标
- `ocr_navigation_signal_valid_rate`
- `ocr_text_type_classification_rate`
- `ocr_navigation_relevance_present_rate`

### C. 空间/通行性指标
- `passability_signal_valid_rate`
- `obstacle_direction_present_rate`
- `unknown_distance_rate`

### D. 动态事件指标
- `dynamic_event_signal_valid_rate`
- `urgency_level_present_rate`
- `temporal_window_present_rate`

### E. 风险场指标
- `risk_field_signal_valid_rate`
- `risk_level_present_rate`
- `recommended_handling_present_rate`

### F. 安全保守性指标
- `low_confidence_forced_decision_count`
- `unknown_output_rate`
- `unsafe_overconfident_output_count`

---

## 7) 停止条件（满足即停止）

以下条件全部满足即停止（不得顺手扩范围）：
- baseline definition 已完成
- perception signal contract 已完成
- validation tool 已完成且可复现
- test matrix 已完成
- go/no-go pack 已完成并给出结论
- industrial placeholder register 已完成（placeholder_only，明确归属阶段且不阻塞）

---

## 8) 下一阶段入口条件（SceneTask-001）

允许进入 SceneTask-001 的最小条件：
- 五类 perception signal 均可输出且 schema 稳定（允许 unknown，但结构必须稳定）
- 低置信度不强行输出高确定结论
- 风险场基础输出成立
- validation 可复现并产出结构化报告
- go/no-go pack 给出 go 或 conditional_go

---

## 9) 明确声明

- 默认路径仍未开启  
- 本阶段未进入 full controlled trial  
- 本阶段未扩大真实 side effects 面  
- 本阶段未做完整世界模型  
- 本阶段只建立 navigation perception baseline，不扩长尾能力  

