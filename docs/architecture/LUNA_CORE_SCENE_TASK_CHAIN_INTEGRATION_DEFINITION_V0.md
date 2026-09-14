# Phase-SceneTask-001 — Core Scene × Task Chain Integration Definition v0（定义冻结）

**阶段名**：Phase-SceneTask-001  
**性质**：核心场景 × 任务链连续闭环（definition freeze）  
**硬约束**：只做 4 个高频核心场景；不扩长尾；不做世界模型；不做地图×视角×记忆融合；不做真机总验收；不做高级表达链；不扩大真实 side effects 面；不启用默认路径；不修改 Perception-001 signal contract  

---

## 0) 工业级要求占位原则（写死）

工业级要求分期进入；当前做不了的只允许 placeholder/future hook，并且：
- 必须标明归属阶段（planned_phase）
- `blocking_current_phase=false`
- 不得阻塞本阶段停止条件

---

## 1) 唯一目标

把 4 个核心高频导航场景接入任务链，形成**最小连续任务闭环**。

固定 4 场景（写死）：
1. 人行道行走
2. 过马路
3. 地铁进出站/换乘
4. 医院内导航

一句话：SceneTask-001 不是扩场景，而是让核心场景能和任务链连续跑起来。

---

## 2) 非目标（写死）

- 不扩展到商场/展馆/政务大厅等长尾场景
- 不做完整世界模型
- 不做地图×视角×记忆融合（Fusion-001 才做）
- 不做真机总验收（Device-001 才做）
- 不做高级语言表达链（Expression-001 才做）
- 不做多模型调度、不让模型拿执行权
- 不把场景链做成真实放权链（只输出 candidate）

---

## 3) 输入依赖（已成立事实）

- Phase-Perception-001 = GO
- 5 类 perception signal contract 已冻结：
  - `object_stability_signal`
  - `ocr_navigation_signal`
  - `spatial_passability_signal`
  - `dynamic_event_signal`
  - `risk_field_signal`
- 模型仅为 shadow/candidate 辅助（无执行权）
- default path disabled；full controlled trial 未进入；side effects 面未扩大

---

## 4) 输出交付物（v0）

1. SceneTask definition（本文）
2. 核心场景状态机：`docs/architecture/LUNA_CORE_SCENE_STATE_MACHINE_V0.md`
3. Task Chain × Scene Bridge Contract：`docs/architecture/LUNA_TASK_CHAIN_SCENE_BRIDGE_CONTRACT_V0.md`
4. 测试矩阵：`docs/architecture/LUNA_CORE_SCENE_TASK_TEST_MATRIX_V0.md`
5. validation tool：`tools/validate_core_scene_task_chain_v0.py`
6. go/no-go pack：`docs/architecture/LUNA_CORE_SCENE_TASK_CHAIN_GO_NO_GO_PACK_V0.md`

---

## 5) 完成指标（必须建立并可复现）

### A. 场景识别指标
- `scene_classification_valid_rate`
- `scene_confidence_present_rate`
- `uncertain_scene_rate`

### B. 状态转换指标
- `valid_transition_rate`
- `invalid_transition_count`
- `transition_reason_present_rate`

### C. 任务链桥接指标
- `task_status_valid_rate`
- `task_recovery_success_rate`
- `inserted_task_recovery_rate`
- `deviation_candidate_generated_rate`

### D. 安全保守性指标
- `direct_execute_leakage_count`
- `forced_crossing_decision_count`
- `low_confidence_forced_action_count`
- `need_human_help_candidate_rate`

### E. 可观测性指标
- `scene_trace_ready_rate`
- `task_replay_ready_rate`
- `transition_audit_ready_rate`

---

## 6) 停止条件（满足即停止）

以下全部满足即停止（不得顺手进入 Fusion-001）：
- definition 已完成
- state machine 已完成
- bridge contract 已完成
- test matrix 已完成
- validation tool 已完成且可复现
- go/no-go pack 已完成并给出“进入 Fusion-001”的结论

---

## 7) 下一阶段入口条件（Fusion-001）

允许进入 Fusion-001 的最小条件：
- 4 个核心场景均可进入 `scene_state`
- task chain bridge 成立（candidate-only，无 direct execute leakage）
- inserted task 可恢复
- deviation candidate 可输出
- 低置信度不强行动作
- trace/replay/audit 成立
- go/no-go pack 给出 go 或 conditional_go

---

## 8) 明确声明

- 默认路径仍未开启  
- 本阶段未进入 full controlled trial  
- 本阶段未扩大真实 side effects 面  
- 本阶段未做地图×视角×记忆融合  
- 本阶段只打通 4 个核心场景×任务链，不扩长尾场景  

