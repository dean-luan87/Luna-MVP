# Luna-2 版本变更日志

所有重要的变更都会记录在此文件中。

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)，
版本号遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

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

