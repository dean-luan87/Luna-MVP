# Phase-Fusion-001 — Map × Vision × Memory Fusion Definition v0（定义冻结）

**阶段名**：Phase-Fusion-001  
**性质**：最小融合机制定义（v0）；不是完整世界模型；不是长尾场景扩展；不是真机总验收；不是高级表达链  
**硬约束**：不放权；不让模型拿执行权；不扩大真实 side effects 面；不启用默认路径；不修改 SceneTask-001 candidate-only 原则  

---

## 0) 工业级要求占位原则（写死）

工业级要求分期进入；当前做不了的只允许 placeholder/future hook，并且：
- 必须标明归属阶段（planned_phase）
- `blocking_current_phase=false`
- 不得阻塞本阶段停止条件

---

## 1) 唯一目标

建立第一版 **Map × Vision × Memory** 融合机制，使导航从“一次性场景任务”升级为“可利用地图宏观约束、视角局部事实锚点、历史记忆优化”的连续导航候选系统。

一句话：Fusion-001 不是完整世界模型，而是让地图、视角和记忆形成最小融合闭环。

---

## 2) 非目标（写死）

- 不做完整世界模型/全局知识图谱
- 不做长尾场景扩展
- 不做真机总验收
- 不做高级表达链
- 不做真实放权/不让模型拿执行权
- 不让地图压过视角事实锚点
- 不让记忆覆盖实时视角风险
- 不启用默认路径/不扩大真实 side effects 面

---

## 3) 输入依赖（已成立事实）

- Phase-Perception-001：navigation perception baseline = GO（5 类 perception signals contract 已冻结）
- Phase-SceneTask-001：4 核心场景 × 任务链 integration = GO（candidate-only）
- default path disabled；full controlled trial 未进入；side effects 面未扩大

---

## 4) 本阶段范围（只覆盖 3 类融合）

### 4.1 Map as Macro Constraint
- 地图只提供长距离/宏观路径约束
- 不作为局部事实唯一依据

### 4.2 Vision as Local Fact Anchor
- 视角信号作为局部通行、风险、场景状态的事实锚点
- 地图与视角冲突时，不直接服从地图

### 4.3 Memory as Repeated-Task Optimizer
- 记忆只作为重复路线/历史偏好/历史风险的候选优化依据
- 不得覆盖实时风险信号

---

## 5) 输出交付物（v0）

1. definition：`docs/architecture/LUNA_MAP_VISION_MEMORY_FUSION_DEFINITION_V0.md`（本文）  
2. signal contract：`docs/architecture/LUNA_MAP_VISION_MEMORY_FUSION_SIGNAL_CONTRACT_V0.md`  
3. conflict policy：`docs/architecture/LUNA_MAP_VISION_MEMORY_CONFLICT_POLICY_V0.md`  
4. test matrix：`docs/architecture/LUNA_MAP_VISION_MEMORY_FUSION_TEST_MATRIX_V0.md`  
5. validation tool：`tools/validate_map_vision_memory_fusion_v0.py`  
6. go/no-go pack：`docs/architecture/LUNA_MAP_VISION_MEMORY_FUSION_GO_NO_GO_PACK_V0.md`  
7. （如需要）industrial placeholder register 更新：`docs/architecture/LUNA_INDUSTRIAL_GRADE_PLACEHOLDER_REGISTER_V0.md`  

---

## 6) 完成指标（最小指标体系）

必须由 validation tool 输出至少以下指标：

### A. 融合信号完整性
- `map_constraint_signal_valid_rate`
- `vision_anchor_signal_valid_rate`
- `memory_route_signal_valid_rate`
- `fusion_candidate_schema_valid_rate`

### B. 冲突处理指标
- `conflict_detected_rate`
- `conflict_resolution_valid_rate`
- `vision_risk_override_success_rate`
- `stale_memory_rejection_rate`

### C. 记忆优化指标
- `repeated_route_match_rate`
- `memory_used_as_optimizer_rate`
- `memory_override_realtime_risk_count`
- `new_information_detected_rate`

### D. 安全保守性指标
- `fusion_execute_leakage_count`
- `unsafe_map_override_count`
- `unsafe_memory_override_count`
- `low_confidence_degraded_rate`

### E. 可观测性指标
- `fusion_trace_ready_rate`
- `fusion_replay_ready_rate`
- `source_attribution_present_rate`
- `reason_codes_present_rate`

---

## 7) 停止条件（满足即停止）

以下全部满足即停止（不得顺手进入 Expression-001）：
- Fusion definition 已完成
- Fusion signal contract 已完成
- Conflict policy 已完成
- test matrix 已完成
- validation tool 已完成且可复现
- go/no-go pack 已完成并给出进入 Expression-001 结论

---

## 8) 下一阶段入口条件（Expression-001）

允许进入 Expression-001 的最小条件：
- map/vision/memory 三类 signal 均可输出或可安全缺省
- fusion candidate schema 稳定
- 冲突可识别且“视角风险优先级”成立
- 记忆不会覆盖实时风险
- no execute leakage
- trace/replay/source attribution 成立
- go/no-go pack 给出 go 或 conditional_go

---

## 9) 明确声明

- 默认路径仍未开启  
- 本阶段未进入 full controlled trial  
- 本阶段未扩大真实 side effects 面  
- 本阶段未做完整世界模型  
- 本阶段只建立 Map × Vision × Memory fusion v0，不扩长尾场景  

