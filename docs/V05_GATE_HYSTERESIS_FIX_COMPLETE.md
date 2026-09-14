# v0.5 Gate Hysteresis + Min-Hold + Cooldown 修复完成

## 问题描述

**BUG**: Gate 抖动过高（179 次切换 / 6m42s），Hysteresis 命中=0（等同于迟滞没生效或没记录）

**根因**: 
- Gate 状态切换逻辑缺少真正的 Hysteresis（enter/exit 双阈值）
- 缺少最小驻留帧（min-hold）机制
- 缺少切换冷却帧（cooldown）机制
- RuntimeProfile 缺少可视化字段，无法解释"为什么这一帧不切换"

---

## 修复方案

### 核心原则

通过三件套把抖动压下去：
1. **enter/exit 双阈值迟滞**：进入 ACTIVE 需要更高的阈值，退出 ACTIVE 需要更低的阈值
2. **最小驻留帧**：每个模式必须至少驻留 N 帧才能切换
3. **切换冷却帧**：切换后锁定 N 帧，避免 flip-flop

---

## 修复内容

### 1. `vision_pipeline/b2/v03/gate/gate_config.yaml`

**新增配置**:
```yaml
runtime_policy:
  cooldown_frames_after_switch: 15
  min_hold_frames:
    ACTIVE: 20
    READ_ONLY: 10
    SUSPENDED: 10

hard_gates:
  camera_stability:
    enter_threshold: 0.65  # 进入 ACTIVE 需要 >= 0.65
    exit_threshold: 0.55   # 退出 ACTIVE 需要 < 0.55

stability_score:
  missing_view_state_default_mode: "READ_ONLY"
  missing_view_state_human_readable: "缺少 view_state，仅允许只读（保守）"
```

### 2. `vision_pipeline/b2/v03/gate/gate_evaluator_v05.py`

**核心改进**:
- 新增 `GateRuntimeState` 数据类管理状态（residence_frames, cooldown_remaining, counters）
- 实现 `_apply_runtime_policy()` 方法：
  - 检查 cooldown：切换后锁定 N 帧
  - 检查 min-hold：当前模式必须驻留足够帧数
  - 记录 hysteresis hold hits
- 在 `gate_eval.runtime_profile.transition` 中写入：
  - `desired_mode`: 期望的模式
  - `switched`: 是否实际切换
  - `blocked_by`: 阻止切换的原因（cooldown/min_hold）
  - `residence_frames`: 当前模式已驻留帧数
  - `cooldown_remaining`: 剩余冷却帧数
  - `counters`: hysteresis_hold_hits, min_hold_hits, cooldown_hits

### 3. `vision_pipeline/b2/v03/b2_v03.py`

**更新**:
- 更新 `evaluate()` 调用方式，传递 `frame_id` 和 `evidence_ok`
- 从 `gate_trace.runtime_profile.transition` 提取 transition 信息
- 将 transition 信息写入 `GateRuntimeProfile.meta.transition`

### 4. `tools/run_v05_video_test.py`

**更新**:
- 确保 `view_state` 存在，如果 `stability_score=None`，让 GateEvaluator 走 missing_view_state 策略

### 5. `viewer/trace_viewer_v05_dashboard.html`

**更新**:
- Runtime Track 表格新增 "Transition" 列
- 显示 `blocked_by`, `residence_frames`, `cooldown_remaining`, `switched`
- Tooltip 显示完整的 transition 信息和 counters

---

## 验收标准

跑同一段 6分42秒视频后：

1. **Gate switch/min 大幅下降**
   - 目标：从 26.7 次/分钟 → ≤ 12 次/分钟

2. **READ_ONLY 不再是 1–2 帧闪烁**
   - READ_ONLY mean duration ≥ 10 帧（≈ 0.33s）

3. **Hysteresis 命中 > 0**
   - trace/指纹里 `hysteresis_hold_hits` 开始累计
   - Viewer 里能看到 transition 不切换的原因（min_hold/cooldown）

4. **Viewer 可视化**
   - Transition 列显示：`blocked:min_hold res:5 cd:3 switched`
   - Tooltip 显示完整信息：期望模式、阻止原因、驻留帧数、冷却帧数、计数器

---

## 使用方式

### 运行视频测试

```bash
python3 tools/run_v05_video_test.py test_video_complex_6m42s.mp4
```

### 运行 DCS 审计

```bash
python3 tools/run_trace_audit.py traces/b2_v05_video_trace.jsonl --rules tools/dcs_rules_v05.json
```

### 查看 Viewer

打开 `viewer/trace_viewer_v05_dashboard.html`，选择 `artifacts/trace_enriched.jsonl`

在 Runtime Track 中，Transition 列会显示：
- `blocked:cooldown res:2 cd:13` - 冷却中
- `blocked:min_hold res:5 cd:0` - 最小驻留未满足
- `switched` - 已切换
- `–` - 无特殊状态

---

## 关键指标

修复后应看到的关键指标：

- **switch_count / switch_per_min**: 显著下降（目标 ≤ 12 次/分钟）
- **hysteresis_hold_hits**: > 0（开始累计）
- **min_hold_hits**: > 0（开始累计）
- **cooldown_hits**: > 0（开始累计）
- **READ_ONLY mean duration**: ≥ 10 帧

---

## 状态

✅ **修复完成**

**日期**: 2025-01-14

**影响范围**:
- `vision_pipeline/b2/v03/gate/gate_config.yaml` - 添加 runtime_policy 配置
- `vision_pipeline/b2/v03/gate/gate_evaluator_v05.py` - 完整重写 Hysteresis 逻辑
- `vision_pipeline/b2/v03/b2_v03.py` - 更新调用方式和 transition 信息提取
- `tools/run_v05_video_test.py` - 确保 view_state 正确传递
- `viewer/trace_viewer_v05_dashboard.html` - 显示 transition 信息

**向后兼容**: ✅ 保持与现有调用方式的兼容性
