# Phase-Device-001 — On-Device Closed-Loop Test Matrix v0（A–M）

**目的**：覆盖 4 核心场景在设备环境中的最小闭环路径，并覆盖 controlled live 入口、降级/回退、时效控制、无泄漏、可回放、性能观测等。  

---

## 统一预期（所有用例通用）

- 记录完整 stage 链：`input_event` → `perception_signal` → `scene_state` → `task_state` → `fusion_decision_candidate` → `navigation_output_candidate` → `output_suppression_or_emit_candidate` → `whitebox_trace` → `replay_record` → `fallback_or_degraded_state`
- candidate-only integrity 成立：不得产生执行放权；不得出现 execute/release/retry/reopen 语义
- default-on 不得触发

---

## A. replay_sidewalk_closed_loop_case
- **模式**：`replay_device_mode`
- **输入**：replay 人行道片段
- **预期**：perception→scene→task→fusion→output 全链路可追踪；whitebox/replay 可回放

## B. replay_road_crossing_closed_loop_case
- **模式**：`replay_device_mode`
- **输入**：replay 过马路片段（含动态事件）
- **预期**：crossing 相关决策保持 candidate；不放权；动态事件时效短窗策略生效

## C. replay_metro_closed_loop_case
- **模式**：`replay_device_mode`
- **输入**：replay 地铁场景（OCR/指示牌）
- **预期**：ocr→fusion→output trace 完整；低置信时降级提示可见

## D. replay_hospital_closed_loop_case
- **模式**：`replay_device_mode`
- **输入**：replay 医院场景（走廊/科室）
- **预期**：scene/task/fusion/output 可追踪；可回放

## E. controlled_live_input_entry_case
- **模式**：`controlled_live_input_mode`
- **输入**：显式开启后的受控真实摄像头输入（短时）
- **预期**：必须记录 explicit entry；default_on_trigger=0；candidate-only

## F. degraded_on_low_confidence_case
- **模式**：`test_device_mode` 或 `controlled_live_input_mode`
- **输入**：低置信条件（遮挡/抖动/不确定）
- **预期**：进入 degraded 或输出 help/low-confidence；不强行确定；不崩溃

## G. model_disabled_fallback_case
- **模式**：`test_device_mode`
- **输入**：模型禁用开关为 disabled
- **预期**：系统可继续基线链路；记录 model_disabled_fallback；闭环仍可追踪

## H. perception_failure_fallback_case
- **模式**：`test_device_mode`
- **输入**：感知模块失败/异常（缺帧/解析失败）
- **预期**：保守降级（degraded/wait/silence）；不崩溃；fallback 成立

## I. output_timing_stale_case
- **模式**：`replay_device_mode`
- **输入**：输出候选过期（stale）
- **预期**：不播报过期候选；记录 suppression_reason=stale

## J. no_execute_leakage_device_case
- **模式**：任意（推荐 replay）
- **输入**：全链路覆盖片段
- **预期**：execute/release/retry/reopen leakage = 0；candidate-only integrity 成立

## K. trace_replay_integrity_case
- **模式**：`replay_device_mode`
- **输入**：任一核心场景片段
- **预期**：trace/replay/whitebox 字段齐全；run_id/frame_id 对齐；可回放

## L. basic_latency_observation_case
- **模式**：`test_device_mode` 或 `controlled_live_input_mode`
- **输入**：短时运行记录
- **预期**：端到端延迟可记录并统计（不要求达最终阈值）

## M. device_resource_observation_case
- **模式**：`test_device_mode` 或 `controlled_live_input_mode`
- **输入**：短时运行记录
- **预期**：CPU/内存等资源占用可记录并统计（不要求达最终阈值）

