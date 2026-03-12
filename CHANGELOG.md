# Luna-2 版本变更日志

所有重要的变更都会记录在此文件中。

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)，
版本号遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

## [Unreleased]

（下一版变更将在此记录。）

---

## [1.8.0] - 2026-02-27

### Decision Monitor 目标层与后果层真实化（主线 1.1 / 1.2 封版）

显示器由「可看」进到「可信」：目标与后果由运行态规则生成，不再占位。

#### 新增
- **decision_monitor/goal_resolver.py**：根据运行态解析 goal_type / goal_description / subgoal / goal_status / goal_switch_reason；支持 observe_navigate、hold_for_floor、slow_down_observe、recheck_environment、run_detector_check、run_ocr_check 等；规则优先级：守底 > B2 介入 > 子目标 > 默认观测导航。
- **decision_monitor/consequence_evaluator.py**：根据决策与输出做轻量规则型后果评估；输出 expected_gain / expected_cost / expected_risk、consequence_confidence、rollback_hint、post_action_check_needed；分支：floor_guard、b2_impact、controller 采样、sampling_gate 节流。

#### 变更
- **decision_monitor/builder.py**：`goal` 改为 `goal_resolver.resolve(ctx)`，`consequence` 改为 `consequence_evaluator.evaluate(ctx, decision, outputs)`；移除原 `_build_goal` / `_build_consequence` 占位。
- **decision_monitor/CONTRACT.md**：更新「当前字段来源」表，标明 goal/consequence 来自 resolver/evaluator 规则驱动。

#### 验收
- goal 随 floor_forced、b2_impact、sampled、policy_run_detector/ocr 变化，不再固定 observe_navigate。
- consequence 随 decision_owner 与上述四类情况变化。
- Viewer 顶部一句话与「现在要做什么 / 预期后果」展示真实生成内容；`tests/test_decision_monitor.py` 全通过。

#### 约束
- 未接复杂任务系统、大模型意图、复杂后果模拟；未改 Dynamic Policy / B2 契约。

---

### Dynamic Policy × B2 最小 impact × runtime 单一入口 — 本条线已封版并退出主线

**状态（写死）**：已从「主线工程坑」收口为「稳定模块 + backlog」；后续只做 backlog 维护或回归打脸修复，不再占用主线资源。

#### 封版状态（写死）
- **P0**：通过并封版
- **P1**：通过
- **P1.1**：不通过（已归档，根因由 P1.2 修复）
- **P1.2**：通过（同一 impact 生命周期内 BALANCED→FULL 最多一次）
- **P1.2a**：已并入 P1.2（活跃 B2 impact 时 450ms 采样 floor，守底红灯已灭）
- **P2**：**通过**（B2 runtime 单一入口，版本债清理完成）

#### P2 验收项（写死）
- runtime import 检查通过：`python3 tools/check_b2_runtime_imports.py` → OK，主路径无 b2_v02/b2_v03 直连
- standalone gate 行为通过：`python3 tests/standalone/b2_v041_gate_behavior_standalone.py` → HARD_FAILURES=0，退出码 0
- trace anchor 通过：`python3 -m pytest tests/traces/test_baseline_check.py -m trace_anchor -v` → 1 passed（1 skipped 为预期）
- **Soft warnings 说明**：standalone 中 A/C/F 的「expected impact=NEED_SLOW_DOWN/NEED_STOP, got=None」属于**能力期望未实现**，非契约违规；按 CHANGELOG 约定 Soft 不阻塞封版、不阻塞合并。

#### 最终通过样本与三问（P0/P1.2）
- **样本**：video-1m01s（1838 帧）；baseline `logs/p11_sample_baseline_1m01s.jsonl`，b2-on `logs/p12a_sample_b2on_1m01s.jsonl`
- **三问**：算力降、口径未漂、守底未破（max_unsampled_gap_ms=500，floor 全绿）

#### 当前有效实现
- **P1.2a 的 450ms active-impact floor**：当存在未过期 NEED_SLOW_DOWN impact 时，`SamplingGate` 使用 `MAX_SAMPLING_INTERVAL_SEC_ACTIVE_B2_IMPACT = 0.45`，否则 0.5s。见 `runtime/dynamic_policy/sampling_gate.py`。
- **P2 单一入口**：`vision_pipeline.b2.b2_runtime.get_b2_engine()`；主路径禁止直连 b2_v02/b2_v03；版本真相表见 `vision_pipeline/b2/B2_VERSION_TRUTH_TABLE.md`；静态检查 `python3 tools/check_b2_runtime_imports.py`。

#### 已知非阻塞尾巴
- YOLO 仍略高于 P1 第一版（b2-on 56 vs 49），不阻塞封版；后续可 backlog 再压。
- Standalone 中 3 个 Soft warnings（能力期望），不阻塞封版。

#### 后续（backlog，不占主线）
- B2 impact 触发更精准；YOLO 再压一点；更多弱证据样本回归；trace/日志降噪。**不再在此线继续磨，除非 backlog 或回归打脸；资源切去下一块工程主线。**

---

## [1.7.0] - 2026-03-04

### Trace Suite 封版与长视频回归锚点

本阶段收尾：稳定回归锚点与压力样本固化，四指标基线校验闭环；抖动治理占位，为下一阶段 jitter governance MVP 做准备。

#### 封版结论（写死）
- **medium_long_01** = `test_video_complex_6m42s.mp4`（6m42s）：产品级回归锚点，四指标 PASS 即封版通过
- **stress_oscillate_01** = `video-6m14s.mp4`（6m14s）：压力/故障样本（段内抖动），单独看抖动指标，不与稳定锚点混用

#### 固化命名与配置
- **tests/traces/suite.yaml**：label → 视频文件名映射（medium_long_01、stress_oscillate_01、easy_01/02）
- **tests/traces/baselines/medium_long_01.json**：四指标约束（mode_switch_total_max、CAUTION_ratio、SAFE_EDGE_duration、SAFE_EDGE_to_CAUTION_ratio）
- **tests/traces/baselines/stress_oscillate_01.json**：抖动指标约束（short_caution_run_ratio_max、switch_per_min_max），治理 MVP 通过后校验

#### 一键命令
- **make trace-suite**：跑 suite（medium_long_01 + stress_oscillate_01），输出 `logs/trace_report.json`
- **make trace-check**：基线校验稳定锚点四指标（PASS/FAIL，可接 CI）
- **make trace-check-stress**：压力样本抖动指标校验（jitter governance MVP 后应 PASS）

#### 可观测与脚本
- **tools/analyze_runtime_trace.py**：新增 caution_runs_total/short、short_caution_run_ratio、switch_per_min（抖动压力报告）
- **tools/dump_mode_runs.py**：导出 mode 段落 CSV，用于拆解 mode_switch 成因（段落切换 vs 段内抖动）
- **tools/plot_trace_timeline.py**：三条时间线（risk_score、SAFE_EDGE、mode）
- **tests/traces/check_baseline.py**：支持稳定锚点四指标 + 压力样本抖动约束；**tests/traces/test_baseline_check.py**：pytest 封装

#### 抖动治理占位（下一阶段 MVP）
- **a3/config.py**：`caution_min_dwell_sec`、`jitter_governance_enabled`、`jitter_switch_per_min_threshold`、`jitter_short_run_ratio_threshold`；治理逻辑待实现，目标仅针对 stress_oscillate_01 压短 CAUTION 段，不破坏 medium_long_01 四指标

#### B2 v0.4.1 契约回归与封版门禁

- **B2 v0.4.1 standalone regression is now contract-based**
- **Exit code semantics**: `0` = contract pass（可封版）, `2` = contract violation（架构违约，阻塞合并）
- **Hard checks** cover: Gate silence（SUSPENDED 必沉默）, `advisory_only` 必须 True, READ_ONLY 不产 impact, ENV 不触发 CONDITION_CHANGE/不确认风险, 禁止确认性语义
- **Soft warnings** indicate capability gaps only（如 A/C/F impact 未产出）, **do not block merge**

**固定命令**

| 用途 | 命令 |
|------|------|
| 锚点回归 | `python3 -m pytest tests/traces/test_baseline_check.py -m trace_anchor -v` |
| B2 契约 standalone | `python3 tests/standalone/b2_v041_gate_behavior_standalone.py`，`echo $?` 期望 0 |
| **CI（仅跑锚点 + standalone，避免全量 pytest）** | `python3 -m pytest tests/traces/test_baseline_check.py -m trace_anchor -q`<br>`python3 tests/standalone/b2_v041_gate_behavior_standalone.py` |

**B2 TTL override 门禁（已落地）**

- **tools/analyze_b2_override_effect.py**：密度分母改为全 trace wall-clock（`duration_sec_all = max(ts_all)-min(ts_all)`），不再用“仅 b2 行”口径，避免密度被写入频率带偏；输出 `duration_sec_b2_only` 作对照。
- **tests/traces/test_b2_ttl_override_gate.py**：CI 级门禁（`@pytest.mark.trace_anchor`）：单段 medium_long_01 trace 检查 `b2_ttl_used_mean ∈ [1.0, 2.5]`、`ttl_expire_density_per_sec ≤ 0.05`、`advisory_suppressed_density_per_sec ≤ 0.2`；trace 不存在则 skip。
- **vision_pipeline/b2/b2_v02.py**：telemetry 增加 `suppress_reason`（仅 suppressed 时写，如 same_as_last / changed_or_ttl）；`ttl_used` 已有。
- **tools/analyze_runtime_trace.py**：`policy_fps_changes_per_min > 120` 时打印软门禁告警（不 fail）。

**下一轮**：可按证据链进一步收紧门禁阈值（如 b2_ttl_used_mean 收窄到 1.2–2.5）。

---

## [1.6.0] - 2026-03-03

### A3 收口 + B2 TTL 可观测与 A-route 审计封版

本版冻结两条线：A3 决策层不再拧参数；B2 TTL 审计具备可观测性与回归门禁，以 Observed 口径为准。

#### A3 收口与冻结
- **edge_multiplier** 默认 1.2，仅保留环境变量 `A3_EDGE_MULTIPLIER` 作为可控开关
- **tools/README_EXPERIMENTS.md** 新增「五.1、A3 回归/验收门槛」：EDGE% 稳定在现有量级，hit_rate 窗口 5/8 保持 EDGE > non_EDGE

#### B2 TTL 可观测性（先补数据再审计）
- **vision_pipeline/b2**：`b2_controller_v02`、`b2_v02` 增加本帧状态 `_last_ttl_expire`、`_last_suppressed` 与 `telemetry()`，写入 pipeline `result["telemetry"]`
- **runtime/a3_logger**：`log_a3(..., telemetry=...)`，trace 每帧带 `telemetry.b2`、`telemetry.c1.motion`
- **main**：采样帧写 trace 时传入 `pipeline_result.get("telemetry")`

#### B2 TTL 审计 A-route（双口径 + 门禁）
- **tools/analyze_b2_ttl_v2.py**：Observed（采样内）+ Estimated（全量估计）；回归门禁：`ttl_density_observed < 0.05` 且 `edge_suppressed_ratio < 0.2` 且 `suppressed_density_observed < 0.15` 为 PASS
- 支持 `--trace`、`--processed-frames`、`--out`，输出 JSON 报告与终端 PASS/FAIL

#### 文档与脚本
- **tools/README_EXPERIMENTS.md**：B2 TTL 审计收尾标准、v2 A-route 命令与三段示例
- **tools/analyze_b2_ttl.py**：旧版（依赖 logs 字符串），保留兼容

---

## [1.5.0] - 2026-02-14

### Guardian Discipline Phase 1 冻结

退出纪律审计层：基于 control_mode 评估 B 型配置是否存在粘滞型 Goodhart，与 A3 risk 数值解耦。

#### 新增
- **tools/audit_exit_latency.py**：baseline/candidate replay 审计，输出 exit_latency、hysteresis_efficiency、baseline_no_entry 等
- **tools/test_guardian_discipline.py**：审计 + Gate 回归测试（含 --suite 集成）
- **tools/run_video_replay.py**：真实视频 → trace → episode → recompute → 审计
- **tools/run_video_replay_suite.py**：6 测试视频批量跑审计
- **docs/GUARDIAN_DISCIPLINE_PHASE1.md**：口径、Gate 红线、复现命令、最小测试用例与真实视频说明
- 最小测试用例：baseline_test.jsonl、candidate_test.jsonl、baseline_test2.jsonl

#### 变更
- **tools/run_sim_suite.py**：集成 exit_latency 审计，per_episode 写入 guardian_discipline、exit_audit_path
- **simulation/logic/gate.py**：Guardian Discipline 红线（exit_latency_p95≤6、max≤12、hysteresis_efficiency≥0.90）

#### 验证
- test_guardian_discipline.py 全通过；6 视频套件 6/6 PASS。

---

## [Unreleased] A3 Deterministic Decision Stage 2

### 目标
决策闭环定点化：相同量化输入 → 相同 decision 与 advice_rhythm 路径，支持可回放、可审计、可复现（字节级一致）。

### SCALE 与舍入
- **SCORE_SCALE = 1000**（3 位小数定点）；**ALPHA_SCALE = 1000**
- **舍入**：round half away from zero（0.5 → 1，-0.5 → -1）
- **权威字段**：分支与状态更新以整数为准：`ema_q`、`raw_q`、`raw_effective_q`、`x_hold_q`、`peak_hold_value_q`；trace 中同时记录 `ema`（= dq(ema_q)）等浮点 shadow 便于可读

### 变更
- **runtime/a3_fixedpoint.py**：定点单源真理（q/dq/clamp_i/ema_step_i/view_conf_gate_q）
- **a3/engine.py**：`A3_FIXEDPOINT=1` 时走定点路径（raw_q → gate_q → raw_effective_q → peak_hold_q → ema_q → _classify_safety_q）；状态增加 `ema_q`、`peak_hold_value_q`
- **intervention/advice_rhythm_v0.py**：配额比较改为整数域（`count >= int(quota)`），QUOTA_EXCEEDED 判定确定
- **runtime/a3_logger.py**：debug 序列化保留 int（如 ema_q）不 round，浮点 round 3 位

### 回滚
- **A3_FIXEDPOINT=0** 关闭定点，恢复原有浮点决策路径（默认 `1`，即开启定点）

### 测试
- **tests/test_rounding_policy.py**：舍入策略与 0.5 边界、dq 往返
- **tests/test_determinism_fixedpoint.py**：同 obs 两遍决策一致、多 tick 序列一致、阈值边界、ema_q 权威

### 加固（工业级确定性）
- **q() 舍入**：加 epsilon（1e-12）消除浮点二进制边界抖动，跨平台一致；0.5005 → 501
- **advice_rhythm quota**：用 `ceil(quota)` 替代 `int(quota)`，避免 0.8 → 0 意外放行；配额口径明确
- **trace schema**：`trace_schema_version: 2`、`decision_authority: "fixedpoint"`，明确权威字段
- **tools/diff_traces.py**：首次分叉定位脚本，输出 ts/seq 及前后 5 行上下文；支持 `--keys` 仅比较决策/rhythm 路径

---

## [1.0.0] - 2025-11-05

### 🎉 首次发布 - 硬件Demo测试版本

这是Luna-2系统的第一个正式版本，面向硬件Demo测试。

### ✨ 新增功能

#### 核心系统
- **系统控制中枢** (`system_orchestrator.py`)
  - 完整的系统生命周期管理
  - 事件驱动架构
  - 模块化设计

- **增强版系统控制中枢** (`system_orchestrator_enhanced.py`)
  - Whisper语音识别集成
  - YOLO视觉检测集成
  - 任务打断与恢复机制
  - 失败重试队列

#### 语音系统
- **Whisper语音识别** (`whisper_recognizer.py`)
  - 支持多种模型大小（tiny, base, small, medium, large）
  - 中文语音识别
  - 实时录音和识别

- **TTS语音合成** (`tts_manager.py`)
  - 多引擎支持（edge-tts, pyttsx3）
  - 中文语音播报
  - 异步播报支持

- **语音唤醒** (`voice_wakeup.py`, `voice_wakeup_manager.py`)
  - 关键词唤醒检测
  - 实时语音处理

#### 视觉系统
- **视觉OCR引擎** (`vision_ocr_engine.py`)
  - YOLOv8物体检测（支持1080P输入，imgsz=1280）
  - PaddleOCR文字识别
  - 多模态识别组合

- **台阶检测** (`step_detector.py`)
  - YOLO模型集成
  - 台阶方向识别
  - 1080P分辨率支持

- **标识牌检测** (`signboard_detector.py`)
  - 颜色识别
  - 形状识别

- **设施检测** (`facility_detector.py`)
  - 公共设施识别
  - 位置定位

#### 导航系统
- **导航管理器** (`navigation_manager.py`)
  - 路径规划
  - 语音导航
  - 实时位置更新

- **AI导航** (`ai_navigation.py`)
  - YOLO实时检测
  - 导航引导

- **医院导航** (`hospital_facility_navigator.py`)
  - 医院场景专用导航
  - 诊室定位

#### 学习系统
- **错误学习引擎** (`error_learning.py`)
  - 错误记录与分析
  - 纠正方案学习
  - 错误模式识别

- **任务优化引擎** (`task_optimizer.py`)
  - 任务执行记录
  - 优化方案学习
  - 性能分析

- **用户习惯分析** (`user_habit_analyzer.py`)
  - 行走习惯记录
  - 用户画像生成
  - 时间估算

- **视觉学习引擎** (`visual_learning.py`)
  - 物体识别学习
  - 知识库构建
  - 识别结果纠正

- **统一学习管理器** (`learning_manager.py`)
  - 统一接口管理
  - 数据同步
  - 统计汇总

#### 任务系统
- **任务引擎** (`task_engine.py`)
  - 任务链管理
  - 任务模板
  - 任务执行

- **任务打断器** (`task_interruptor.py`)
  - 主任务暂停
  - 子任务插入
  - 任务恢复

#### 地图系统
- **情感地图生成** (`emotional_map_card_generator_enhanced.py`)
  - 手绘风格地图
  - 图标标注
  - 情感标签

#### 数据管理
- **记忆存储** (`memory_store.py`)
  - 本地存储
  - 云端同步
  - 数据持久化

- **日志管理** (`log_manager.py`)
  - 行为日志记录
  - 日志查询
  - 日志导出

- **配置管理** (`config.py`, `unified_config_manager.py`)
  - 统一配置管理
  - 配置验证
  - 配置热更新

#### 故障处理
- **故障处理器** (`fault_handler.py`)
  - 故障检测
  - 故障回调
  - 故障恢复

- **重试队列** (`retry_queue.py`)
  - 失败任务重试
  - 重试策略
  - 队列管理

### 🔧 技术特性

- **模块化架构**: 高度模块化设计，易于扩展
- **事件驱动**: 基于事件总线的异步处理
- **1080P支持**: YOLO模型支持1080P输入（imgsz=1280）
- **性能优化**: 多线程处理、异步I/O
- **容错机制**: 完善的错误处理和重试机制

### 📝 文档

- 完整的模块文档
- 集成测试用例
- 使用指南

### 🔒 稳定性

- 完整的错误处理
- 资源清理机制
- 线程安全设计

