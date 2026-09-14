# Phase-Expression-001 — Navigation Output & Timing Control Definition v0（定义冻结）

**阶段名**：Phase-Expression-001  
**性质**：输出与时效控制机制（v0）；不是情感化表达；不是人格化语言；不是真机总验收  
**硬约束**：不放权；不让输出层触发 execute/retry/reopen/release；不扩大真实 side effects 面；不启用默认路径；不修改 fusion candidate 的 no-execute 原则  

---

## 0) 工业级要求占位原则（写死）

工业级要求分期进入；当前做不了的只允许 placeholder/future hook，并且：
- 必须标明归属阶段（planned_phase）
- `blocking_current_phase=false`
- 不得阻塞本阶段停止条件

---

## 1) 唯一目标

建立第一版导航输出与时效控制机制，把 scene/task/fusion candidates 转换成**可控、及时、保守、可审计**的导航播报候选，并写死：
什么时候说、说什么、多久有效、超时如何处理、低置信如何降级、何时提示人工协助。

一句话：Expression-001 不是做情感化表达，而是让导航输出“及时、克制、可控、不误导”。

---

## 2) 非目标（写死）

- 不做高级情感表达/人格化语言
- 不做完整语音系统重构
- 不做真机总验收
- 不做长尾场景扩展
- 不让模型生成最终播报直接放权
- 不让输出层触发 execute/retry/reopen/release
- 不扩大真实 side effects 面/不启用默认路径

---

## 3) 输入依赖（已成立事实）

- Phase-Fusion-001 = GO（fusion_decision_candidate 写死 allows_execute_now=false；视角风险优先；记忆不覆盖实时风险）
- Phase-SceneTask-001 = GO（candidate-only 任务链桥接成立）
- default path disabled；full controlled trial 未进入；side effects 面未扩大

---

## 4) 本阶段范围（仅五类输出控制）

1. **Navigation Output Candidate Contract**：将上游候选转换为输出候选（结构化）
2. **Priority & Suppression Policy**：安全/普通/状态确认/低置信/求助的优先级与抑制
3. **Timing Window Policy**：有效期、过期丢弃、重复间隔、超时处理
4. **Degraded / Low Confidence Expression**：低置信必须保守表达
5. **Human Help Prompt Policy**：复杂/不确定/高风险时提示求助（候选）

---

## 5) 输出交付物（v0）

1. definition（本文）  
2. output candidate contract：`docs/architecture/LUNA_NAVIGATION_OUTPUT_CANDIDATE_CONTRACT_V0.md`  
3. priority & suppression policy：`docs/architecture/LUNA_NAVIGATION_OUTPUT_PRIORITY_AND_SUPPRESSION_POLICY_V0.md`  
4. timing window policy：`docs/architecture/LUNA_NAVIGATION_OUTPUT_TIMING_WINDOW_POLICY_V0.md`  
5. degraded/help prompt policy：`docs/architecture/LUNA_NAVIGATION_OUTPUT_DEGRADED_AND_HELP_PROMPT_POLICY_V0.md`  
6. test matrix：`docs/architecture/LUNA_NAVIGATION_OUTPUT_TEST_MATRIX_V0.md`  
7. validation tool：`tools/validate_navigation_output_timing_control_v0.py`  
8. go/no-go pack：`docs/architecture/LUNA_NAVIGATION_OUTPUT_TIMING_CONTROL_GO_NO_GO_PACK_V0.md`  
9. （如需）placeholder register 更新：`docs/architecture/LUNA_INDUSTRIAL_GRADE_PLACEHOLDER_REGISTER_V0.md`  

---

## 6) 完成指标（最小指标体系）

必须由 validation tool 输出至少以下指标：

### A. 输出候选完整性
- `output_candidate_schema_valid_rate`
- `message_template_present_rate`
- `reason_codes_present_rate`
- `confidence_present_rate`

### B. 优先级与抑制
- `priority_order_valid_rate`
- `safety_suppression_success_rate`
- `repeat_suppression_success_rate`
- `silence_valid_output_rate`

### C. 时效控制
- `stale_output_block_rate`
- `dynamic_timeout_block_rate`
- `expired_high_priority_block_rate`
- `validity_window_present_rate`

### D. 安全保守性
- `execute_leakage_count`
- `release_retry_reopen_leakage_count`
- `low_confidence_overstatement_count`
- `unsafe_stale_output_count`

### E. 可观测性
- `output_trace_ready_rate`
- `output_replay_ready_rate`
- `suppression_reason_present_rate`
- `source_candidate_attribution_rate`

---

## 7) 停止条件（满足即停止）

以下全部满足即停止（不得顺手进入 Device-001）：
- Output timing definition 已完成
- Output candidate contract 已完成
- Priority/suppression policy 已完成
- Timing window policy 已完成
- Degraded/help prompt policy 已完成
- test matrix 已完成
- validation tool 已完成且可复现
- go/no-go pack 已完成并给出进入 Device-001 的结论

---

## 8) 下一阶段入口条件（Device-001）

允许进入 Device-001 的最小条件：
- 输出 candidate schema 稳定
- 安全提醒优先级成立
- 过期输出不会播报
- 低置信不会确定化
- 重复抑制成立
- no execute/release/retry/reopen leakage
- trace/replay/source attribution 成立
- go/no-go pack 给出 go 或 conditional_go

---

## 9) 明确声明

- 默认路径仍未开启  
- 本阶段未进入 full controlled trial  
- 本阶段未扩大真实 side effects 面  
- 本阶段未做高级情感表达  
- 本阶段只建立 Navigation Output & Timing Control v0  

