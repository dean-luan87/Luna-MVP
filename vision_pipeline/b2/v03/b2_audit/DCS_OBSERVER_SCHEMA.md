# B2 v0.5 DCS Observer Schema 文档

## 📋 定位

**这是"事故黑匣子 + 设计审计台"，不是 Dashboard。**

- ❌ 不对外
- ❌ 不做 KPI
- ❌ 不做"模型效果展示"
- ❌ 不允许 PR 用截图糊过去

## 🎯 核心原则

**这是"解剖系统的观察台"，不是展示系统。**

### 设计语义说明

- ❌ 不显示 FPS、性能、吞吐
- ✅ 只回答：
  - 这套系统现在还讲不讲理
  - 它有没有越权

## 📊 页面总结构

```yaml
page: dcs_observer
purpose: system_diagnosis
visibility: internal_only

sections:
  - overview
  - dimension_breakdown
  - violation_timeline
  - frame_trace_inspector
```

## 🔍 Section 1: Overview

**一次判断系统是否"还活着"**

### 字段

- `dcs_score`: number [0, 100] - DCS 总分
- `status`: enum [EXCELLENT, PASS, WARNING, FAIL] - 系统状态
- `evaluated_version`: string - 评估版本
- `trace_range`: time_range - Trace 时间范围
- `fatal_violations`: list - 致命违规列表
- `warning_count`: number - 警告数量

### 语义重点

**这一层不是"哪跑慢了"，而是 "谁在设计上越界了"。**

## 📊 Section 2: Dimension Breakdown

**责任拆解层**

### 维度结构

每个维度包含：
- `score`: number - 实际得分
- `max`: number - 满分
- `violations`: list - 违规列表

### 违规项结构

每个 violation 必须包含：
- `rule_id`: string - 对应 A / B 的规则编号
- `description`: string - 人类语言
- `count`: number - 违规次数
- `severity`: enum [WARN, FAIL] - 严重程度

### 语义重点

**这一层不是"哪跑慢了"，而是 "谁在设计上越界了"。**

## ⏱️ Section 3: Violation Timeline

**时间责任定位**

### 结构

- `unit`: "second" - 时间单位
- `items`: array - 违规时间线项

### 违规时间线项

每个项包含：
- `time`: time_point - 时间点（秒 + 帧）
- `violation_type`: enum [GATE, TRIGGER, IMPACT, TRACE, TIMELINE]
- `rule_id`: string - 规则 ID
- `summary`: string - 违规摘要
- `drilldown_ref`: string - Trace ID（用于下钻）

### 必须满足

- 所有扣分都能定位到某一秒
- 不允许"模糊区间扣分"

**👉 这是你以后 Debug 的生命线**

## 🔬 Section 4: Frame Trace Inspector

**终极审判层**

### 输入

- `trace_id`: string - Trace ID

### 输出

- `time`: time_point - 时间信息
- `gate_state`: {mode, reason} - Gate 状态
- `evidence_state`: {active: []} - 证据状态
- `trigger`: {fired, reason} - Trigger 信息
- `impact`: {value, confidence} - Impact 信息
- `to_c`: {sent, payload?} - B → C 消息

### 这层只解决一个问题

**"为什么这一秒系统这么想？"**

## 📝 Schema 文件

完整 Schema 定义见：`dcs_observer_schema.json`

## 🎯 使用场景

1. **事故分析**: 通过 Frame Trace Inspector 分析特定时刻
2. **设计审计**: 通过 Dimension Breakdown 定位设计越界
3. **时间定位**: 通过 Violation Timeline 定位问题时间点
4. **系统诊断**: 通过 Overview 判断系统是否"还活着"

## 💡 重要提示

> **这是"解剖系统的观察台"，不是展示系统。**
> 
> **所有数据都用于回答：系统现在还讲不讲理？它有没有越权？**
