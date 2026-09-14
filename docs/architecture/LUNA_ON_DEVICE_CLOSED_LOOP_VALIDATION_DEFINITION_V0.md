# Phase-Device-001 — On-Device Closed-Loop Validation Definition v0（定义冻结）

**阶段名**：Phase-Device-001  
**性质**：真机/近似真机环境的最小闭环验证（v0），验证“链路能不能在设备上跑通”。  

---

## 1) 唯一目标

在设备环境中完成最小闭环验证，确认系统能在受控场景下完成：

感知输入 → 场景判断 → 任务链状态 → 融合候选 → 输出候选 → trace/replay/whitebox 记录 → 降级/回退

一句话：Device-001 不是上用户，也不是产品发布，而是验证“链路能不能在设备上跑通”。

---

## 2) 严格限制（写死）

### 禁止事项
- 不进入 full controlled trial
- 不开启 default-on / 默认路径
- 不做开放真实用户测试
- 不扩大真实 side effects 面
- 不让模型拿执行权
- 不把输出候选变成真实执行命令
- 不新增长尾场景
- 不做完整世界模型
- 不做正式商业化产品验收
- 不做高级情感表达
- 不解决所有工业级 placeholder

### 允许事项
- 新增设备闭环验证定义
- 新增设备运行模式说明（contract）
- 新增设备测试 runbook/最小矩阵（本阶段用 test matrix 冻结替代 runbook 的详细操作细节）
- 新增设备日志/trace/replay 最低要求
- 新增验证工具（读取设备日志或 replay fixture，输出结构化 JSON）
- 新增最小性能观测（只要求可记录、可统计）
- 新增 Device go/no-go pack
- 更新 README 索引
- 必要时新增 placeholder（不阻塞，除非安全硬阻断）

---

## 3) 本阶段范围（仅最小真机闭环）

仅覆盖：
1. 设备运行入口（模式选择 + 显式开关记录）
2. 受控输入源（replay / fixture / controlled live input）
3. 链路串联（Model/Perception/SceneTask/Fusion/Expression）
4. 输出候选生成与抑制（candidate-only）
5. 设备侧日志/trace/whitebox/replay 记录
6. fallback/disable/degraded 验证
7. 最小性能观测（延迟/资源占用“可记录即可”）

---

## 4) 入口前提（已成立事实）

- Governance 主链已收口（Phase-Closure-001）
- Phase-Model-001/002/003 已成立（shadow/candidate-only；conditional_go）
- Phase-Perception-001 = GO
- Phase-SceneTask-001 = GO
- Phase-Fusion-001 = GO
- Phase-Expression-001 = GO
- 输出候选写死 `allows_execute_now=false`
- 默认路径仍未开启；full controlled trial 未进入；真实 side effects 面未扩大

---

## 5) 输出交付物（v0）

- `docs/architecture/LUNA_ON_DEVICE_CLOSED_LOOP_VALIDATION_DEFINITION_V0.md`（本文）
- `docs/architecture/LUNA_ON_DEVICE_RUNTIME_MODE_CONTRACT_V0.md`（设备运行模式 contract 冻结）
- `docs/architecture/LUNA_ON_DEVICE_CLOSED_LOOP_TEST_MATRIX_V0.md`（最小闭环测试矩阵冻结）
- `docs/architecture/LUNA_ON_DEVICE_LOG_TRACE_REPLAY_REQUIREMENTS_V0.md`（设备侧可观测性最低要求冻结）
- `tools/validate_on_device_closed_loop_v0.py`（验证工具）
- `docs/architecture/LUNA_ON_DEVICE_CLOSED_LOOP_GO_NO_GO_PACK_V0.md`（决策包）
- （如需）`docs/architecture/LUNA_INDUSTRIAL_GRADE_PLACEHOLDER_REGISTER_V0.md`（占位登记更新）
- `docs/architecture/README.md`（索引更新）

---

## 6) 完成指标（最小指标体系）

必须由验证工具输出至少以下指标：

### A. 闭环完整性
- `closed_loop_success_rate`
- `stage_chain_completeness_rate`
- `missing_stage_count`
- `candidate_only_integrity_rate`

### B. 安全保守性
- `execute_leakage_count`
- `release_retry_reopen_leakage_count`
- `default_on_trigger_count`
- `low_confidence_forced_action_count`

### C. 可观测性
- `device_trace_ready_rate`
- `device_replay_ready_rate`
- `whitebox_record_ready_rate`
- `reason_codes_present_rate`

### D. 降级与回退
- `degraded_mode_trigger_rate`
- `fallback_success_rate`
- `model_disabled_baseline_success_rate`
- `perception_failure_safe_degrade_rate`

### E. 最小性能观测（只要求可记录/可统计）
- `average_end_to_end_latency_ms`
- `max_end_to_end_latency_ms`
- `latency_record_ready_rate`
- `cpu_memory_record_ready_rate`
- `device_error_count`

---

## 7) 停止条件（满足即停止）

以下全部满足即停止（不得顺手进入下一阶段）：
- definition 已完成
- runtime mode contract 已完成
- closed-loop test matrix 已完成
- log/trace/replay requirements 已完成
- validation tool 已完成且可复现
- go/no-go pack 已完成并给出下一阶段结论

---

## 8) 明确声明（写死）

- 默认路径仍未开启  
- 本阶段未进入 full controlled trial  
- 本阶段未扩大真实 side effects 面  
- 本阶段未进入开放真实用户测试  
- 本阶段只完成 On-Device Closed-Loop Validation v0  

