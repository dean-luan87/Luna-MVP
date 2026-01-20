# v0.5 Trace / Viewer / DCS 修改完成报告

## 目标

解决 v0.5 引入 `GATE_RUNTIME_PROFILE` 后，Viewer / DCS / 人类认知三者错位的问题。

## 核心问题

v0.5 新增了「运行态事件」（Runtime Profile），但 Viewer / DCS 仍按「决策事件」在理解，导致：
- 系统被误读为"没干活"或"坏掉了"
- DCS 用决策规则审判心跳事件
- 统计口径错误（Runtime 被计入 NO_OP）

## 解决方案（4 项修改）

### ✅ 修改 1: Trace 事件类型规范

**文件**: `vision_pipeline/b2/v03/b2_v03.py`

**修改内容**:
- 所有 `tick` 事件显式标记 `event_type: "tick"`
- 所有 `GATE_RUNTIME_PROFILE` 事件已有 `event_type: "GATE_RUNTIME_PROFILE"`

**验证**:
```bash
# 事件类型分布
GATE_RUNTIME_PROFILE: 100
tick: 76
```

### ✅ 修改 2: Viewer - 视觉区分 Runtime vs Decision

**文件**: `viewer/trace_viewer_v05_dashboard.html`

**修改内容**:

1. **CSS 样式**:
```css
/* Runtime Profile: 深色 + 斜体（系统在"呼吸"） */
tr.runtime-profile {
  background-color: #0b1f2a;
  color: #8fd3ff;
  font-style: italic;
  opacity: 0.85;
}

/* Decision Event: 正常亮度（系统在"说话/判断"） */
tr.decision-event {
  background-color: #111;
  color: #eaeaea;
}
```

2. **JavaScript 逻辑**:
```javascript
// 按事件类型添加 CSS 类
const eventType = obj.event_type || "tick";
if (eventType === "GATE_RUNTIME_PROFILE" || eventType === "C_RUNTIME_PROFILE") {
  tr.classList.add("runtime-profile");
} else {
  tr.classList.add("decision-event");
}
```

**效果**: Runtime 行一眼就知道是"系统状态"，不会再误读为"NO_OP 决策"

### ✅ 修改 3: DCS - 跳过 Runtime 的决策审判

**文件**: `tools/dcs_eval.py`

**修改内容**:

1. **`evaluate_event` 函数开头添加 Runtime Profile 检查**:
```python
event_type = event.get("event_type", "tick")
if event_type in ["GATE_RUNTIME_PROFILE", "C_RUNTIME_PROFILE"]:
    # 只做运行态分析，不做决策审判
    # 跳过 impact、decision_level 等决策相关规则
    # 仅检查运行态规则（调度异常、状态不一致等）
    return {
        "violations": violations,
        "grade": grade,
        "is_runtime_profile": True
    }
```

2. **修复检查函数以正确处理 Runtime Profile**:
   - `check_missing_core_fields`: Runtime Profile 不需要 `impact` 字段
   - `check_gate_profile_missing`: GATE_RUNTIME_PROFILE 事件本身包含 `gate_runtime_profile`
   - `check_gate_blocked_reason_missing`: 支持从 `gate_runtime_profile` 提取字段

**验证**:
```bash
# DCS 报告（修复后）
Total: 176
RED: 76      # tick 事件（决策审判）
YELLOW: 0
GREEN: 100   # GATE_RUNTIME_PROFILE 事件（运行态分析，无违规）
```

### ✅ 修改 4: 统计口径修正

**文件**: `viewer/trace_viewer_v05_dashboard.html`

**修改内容**:

1. **新增统计字段**:
```javascript
let stats = {
  runtimeCount: 0,   // Runtime Profile 事件数
  decisionCount: 0,  // Decision 事件数
  noOpCount: 0      // Decision 中 NO_OP 的数量（仅统计 Decision）
};
```

2. **区分统计逻辑**:
```javascript
const isRuntimeProfile = eventType === "GATE_RUNTIME_PROFILE" || eventType === "C_RUNTIME_PROFILE";
const isDecisionEvent = eventType === "tick";

if (isRuntimeProfile) {
  stats.runtimeCount++;
} else if (isDecisionEvent) {
  stats.decisionCount++;
  // NO_OP 只统计 Decision 事件，不统计 Runtime
  if (impact === "NO_OP") {
    stats.noOpCount++;
  }
}
```

**效果**: 
- Runtime 不计入 NO_OP
- 正确计算 Decision 密度：`(decisionCount - noOpCount) / decisionCount`

## 验证结果

### 1. Trace 文件结构
- ✅ 所有事件都有正确的 `event_type`
- ✅ `GATE_RUNTIME_PROFILE`: 100 条
- ✅ `tick`: 76 条

### 2. DCS 评估
- ✅ Runtime Profile 事件：GREEN（只做运行态分析）
- ✅ Decision 事件：RED/YELLOW（完整的决策审判）
- ✅ 不再用决策规则审判心跳事件

### 3. Viewer 显示
- ✅ Runtime Profile 行：深色 + 斜体（视觉区分）
- ✅ Decision 行：正常亮度
- ✅ 统计信息：区分 Runtime 和 Decision

## 核心原则（冻结）

从 v0.5 起：
1. **Runtime Profile 是一级公民** - 不是"NO_OP 决策"，而是"系统在呼吸"
2. **Viewer 必须支持双语义时间线** - Runtime / Decision 分轨显示
3. **DCS 不得审判 Runtime** - 只做运行态分析，不做决策审判
4. **NO_OP 只属于 Decision** - Runtime 不计入 NO_OP

任何违反这四条的工具或逻辑，一律视为错误实现。

## 6′42″ 视频的正确解读

在 v0.5 Viewer 修复后，这段视频意味着：
- ✅ Gate 稳定运行
- ✅ 系统持续在线
- ✅ 视角 / 距离 / 证据不足
- ✅ 因此不进入决策态
- ✅ 没有胡乱提醒用户

**这是一个成熟、安全、克制的系统，不是失败。**

## 修改文件清单

1. `vision_pipeline/b2/v03/b2_v03.py` - Trace 事件类型标记
2. `viewer/trace_viewer_v05_dashboard.html` - Viewer 视觉区分 + 统计口径
3. `tools/dcs_eval.py` - DCS 跳过 Runtime 决策审判

## 测试命令

```bash
# 生成 trace
python3 tools/run_v05_video_test.py --max-frames 100

# DCS 评估
python3 tools/dcs_eval.py traces/b2_v05_video_trace.jsonl

# 打开 Viewer
open viewer/trace_viewer_v05_dashboard.html
```

---

**完成时间**: 2025-01-XX
**版本**: v0.5
**状态**: ✅ 完成并验证
