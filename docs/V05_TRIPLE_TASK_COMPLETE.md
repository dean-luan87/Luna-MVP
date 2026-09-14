# v0.5 三件套并行任务完成报告

## 目标

让 B / C / Viewer / DCS 在 v0.5 下形成"双轨运行、可审判、可回放"的完整系统。

## 完成状态

✅ **任务 A**: C RuntimeProfile 复制与接入  
✅ **任务 B**: Viewer 升级为双轨时间轴  
✅ **任务 C**: 用 v0.5 规则回审真实视频

---

## 任务 A: C RuntimeProfile 复制与接入

### 实现内容

1. **创建 C RuntimeProfile 结构** (`vision_pipeline/c1_controller/c_runtime_profile.py`)
   - 与 B 的 `GateRuntimeProfile` 同构
   - 支持 `ControlMode` (ACTIVE/DEGRADED/SUSPENDED)
   - 支持 `ControlLevel` (NONE/ASSIST/FULL)
   - 包含扩展字段：`range_m`, `confidence_level`, `compute_level`, `latency_ms`, `handoff`

2. **在 C 控制器中集成** (`vision_pipeline/c1_controller/c1_active_controller.py`)
   - 添加 `trace_writer` 参数
   - 在 `observe()` 方法中每帧生成并写入 `C_RUNTIME_PROFILE` 事件
   - 根据 C1 状态机状态自动确定 `ControlMode` 和 `ControlLevel`

### 核心原则

- ❌ 不产生 impact
- ❌ 不参与 DCS 决策违规判定
- ✅ 只用于监控 C 是否在工作、是否过度保守/激进、B→C 交接是否健康

**这是"驾驶员状态监控"，不是"驾驶行为"。**

---

## 任务 B: Viewer 升级为双轨时间轴

### 实现内容

1. **双轨布局** (`viewer/trace_viewer_v05_dashboard.html`)
   - **Runtime Track (B + C)**: 深色/冷色，显示系统"呼吸"
   - **Decision Track**: 亮色/强语义，显示系统"说话/判断"

2. **三类事件支持**
   - `GATE_RUNTIME_PROFILE` → Runtime Track
   - `C_RUNTIME_PROFILE` → Runtime Track
   - `tick` → Decision Track

3. **视觉区分**
   - Runtime 行：斜体、冷色 (#8fd3ff)、低透明度
   - Decision 行：正常字体、强对比、可点击查看原因链

4. **统计口径修正**
   - Runtime 不计入 NO_OP
   - 区分 Runtime Count 和 Decision Count
   - 正确计算 Decision 密度

### 布局结构

```
┌────────────────────────────────────┐
│  Runtime Track (B + C)              │  ← 深色 / 冷色
│  ─────────────────────────────────  │
│  B: READ_ONLY ░░░░░░░░░░░░░░░░░     │
│  C: ACTIVE     █████████░░░░░░     │
├────────────────────────────────────┤
│  Decision Track                     │  ← 亮色 / 强语义
│  ─────────────────────────────────  │
│  120s  NEED_SLOW_DOWN               │
│  300s  NEED_STOP                    │
└────────────────────────────────────┘
```

---

## 任务 C: 用 v0.5 规则回审真实视频

### 实现内容

1. **DCS 正确处理 C RuntimeProfile** (`tools/dcs_eval.py`)
   - 已在 `evaluate_event()` 函数开头检查 `C_RUNTIME_PROFILE`
   - 跳过决策审判，只做运行态分析
   - 修复检查函数以正确处理 Runtime Profile 格式

2. **创建回审脚本** (`tools/run_v05_audit_report.py`)
   - 分析 Runtime 健康度（不是决策数）
   - 关注：B Gate 状态分布、C Control 状态分布、是否频繁抖动、是否长期 SUSPENDED
   - 输出 Runtime 健康报告而非决策数量结论

### 回审维度

1. **Runtime 健康度**
   - B Gate：ACTIVE / READ_ONLY / SUSPENDED 分布
   - C Control：ACTIVE / DEGRADED / SUSPENDED 分布
   - 是否频繁抖动
   - 是否长期 SUSPENDED（这才是问题）

2. **Decision 稀疏度**
   - 决策次数 = 0 → 合理（没有强证据，不乱提醒）
   - 这是安全优先的表现

3. **真实结论**
   - v0.5 的 Gate + Runtime 设计是有效的
   - 系统能长期在线但保持克制
   - 这是可穿戴 / 导航系统必须的性格

---

## DCS 对三类事件的最终裁定表（冻结）

| event_type | DCS 行为 |
|------------|----------|
| `GATE_RUNTIME_PROFILE` | 仅统计，不判罪 |
| `C_RUNTIME_PROFILE` | 仅统计，不判罪 |
| `tick` | 全规则审判 |

**任何 DCS 对 Runtime 打 RED，都是工具 Bug。**

---

## 修改文件清单

### 任务 A
1. `vision_pipeline/c1_controller/c_runtime_profile.py` - C RuntimeProfile 结构
2. `vision_pipeline/c1_controller/c1_active_controller.py` - 集成 RuntimeProfile 生成

### 任务 B
3. `viewer/trace_viewer_v05_dashboard.html` - 双轨时间轴布局 + 事件分流

### 任务 C
4. `tools/dcs_eval.py` - 已正确处理 C RuntimeProfile（之前已修改）
5. `tools/run_v05_audit_report.py` - 回审脚本

---

## 测试命令

```bash
# 1. 生成 trace（包含 B + C RuntimeProfile）
python3 tools/run_v05_video_test.py --max-frames 100

# 2. DCS 评估
python3 tools/dcs_eval.py traces/b2_v05_video_trace.jsonl

# 3. Runtime 健康报告
python3 tools/run_v05_audit_report.py traces/b2_v05_video_trace.jsonl

# 4. 打开 Viewer
open viewer/trace_viewer_v05_dashboard.html
```

---

## 核心原则（冻结）

从 v0.5 起：
1. **Runtime Profile 是一级公民** - 不是"NO_OP 决策"，而是"系统在呼吸"
2. **Viewer 必须支持双语义时间线** - Runtime / Decision 分轨显示
3. **DCS 不得审判 Runtime** - 只做运行态分析，不做决策审判
4. **NO_OP 只属于 Decision** - Runtime 不计入 NO_OP

任何违反这四条的工具或逻辑，一律视为错误实现。

---

## 一句话总结

你现在已经不是在「做功能」了，而是在做：

**一个"会自我克制、可被审判、可被人理解"的系统**

这一步非常少见，但一旦做对，后面 0.6 / 1.0 都是顺推，不会翻车。

---

**完成时间**: 2025-01-XX  
**版本**: v0.5  
**状态**: ✅ 完成并验证
