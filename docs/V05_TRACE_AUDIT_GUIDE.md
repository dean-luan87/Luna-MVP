# B2 v0.5 Trace Audit Guide

**版本：** v0.5  
**日期：** 2025-01-12

---

## 📋 执行路径（不改模型，只跑审判）

### 1. 跑视频，生成 trace（B + C RuntimeProfile）

```bash
# 假设你有一个 pipeline 脚本
python3 run_pipeline_with_trace.py video.mp4
```

**输出：** `artifacts/trace.jsonl`（包含 B 和 C 的 RuntimeProfile）

---

### 2. DCS 审判

```bash
python3 tools/run_trace_audit.py artifacts/trace.jsonl
```

**输出：** 控制台报告 + 可选的 JSON 报告文件

---

### 3. 打开 Viewer

直接在浏览器中打开：
```
viewer/trace_viewer_v05_dashboard.html
```

然后选择 `artifacts/trace.jsonl` 文件。

---

## 🔍 回审时你会重点看三件事

### 🔴 1. 有没有 "算 / 控 在不该的时候发生"

**检查点：**
- Gate=SUSPENDED 但 B 仍计算 → RED
- C=SUSPENDED 但仍控制 → RED

**这是最危险的系统性错误**

**示例：**
```
Time: 02:03.450
B Gate: SUSPENDED
B Compute: FULL  ← ❌ 违规！
C Mode: SUSPENDED
C Control: FULL  ← ❌ 违规！
```

---

### 🟨 2. 有没有 调度异常

**检查点：**
- tick / update 过快
- Gate / Mode 高频抖动

**这类问题不一定立刻出事，但一定会拖垮系统**

**示例：**
```
Time: 02:03.450 - 02:03.500 (50ms 内)
Gate 状态切换: ACTIVE → READ_ONLY → SUSPENDED → ACTIVE
← 🟨 频繁切换，系统不稳定
```

---

### 🟩 3. 正常态比例

**你会看到类似：**

```
Summary
GREEN: 92%
YELLOW: 7%
RED: 1%
```

**这不是 KPI，是系统稳定度画像。**

---

## 💡 你能直接得到的结论类型

### 1. 「这段视频里，C 比 B 激进」

**表现：**
- B 处于 READ_ONLY，但 C 处于 ACTIVE + FULL
- B 提醒了风险，但 C 仍执行完整控制

**含义：** C 可能忽略了 B 的建议，或 B 的建议不够及时

---

### 2. 「这里 B 提醒了，但 C 忽略了」

**表现：**
- B 输出 NEED_STOP，但 C 仍处于 ACTIVE + FULL
- B 的 to_c.send = true，但 C 的 control_level = FULL

**含义：** B→C 通信链路可能有问题，或 C 的决策逻辑需要调整

---

### 3. 「这个红点不是识别错，是调度错」

**表现：**
- DCS 显示 RED，但原因是 `scheduler_violation` 或 `gate_suspended_but_computed`
- 不是 `missing_advisory` 或 `over_prediction_language`

**含义：** 问题不在 AI 判断，而在运行纪律

---

## 🎯 这正是你前面说的那句话的落地

> **不是 AI 聪不聪明，而是系统有没有纪律**

---

## 📊 示例报告输出

```
============================================================
B2 v0.5 Trace Audit Report
============================================================

总帧数: 1500

B Gate 状态分布:
  ACTIVE: 1200
  READ_ONLY: 250
  SUSPENDED: 50

C Control 状态分布:
  ACTIVE: 1100
  DEGRADED: 350
  SUSPENDED: 50

DCS 结果:
  🔴 RED: 15 (1.0%)
  🟨 YELLOW: 105 (7.0%)
  🟩 GREEN: 1380 (92.0%)

🔴 RED 违规 (15 条):
  - gate_suspended_but_computed: Gate=SUSPENDED 时仍发生计算 (frame 234)
  - c_suspended_but_control: C=SUSPENDED 但仍在执行控制 (frame 567)
  - scheduler_violation: tick 调度频率超过系统安全阈值 (frame 890)

🟨 YELLOW 警告 (105 条):
  - gate_flapping: Gate 状态频繁切换，系统不稳定 (frame 123)
  - read_only_ratio_high: 长期处于 READ_ONLY，可能感知或 Gate 参数异常
  - c_full_control_without_b_signal: C 在无 B 风险提示下进入 FULL 控制 (frame 456)
```

---

## ✅ 最终状态确认

到这一步：
- ✅ B / C 共享同一套 RuntimeProfile 语言
- ✅ DCS 能审判两者是否越权
- ✅ Viewer 能让人一眼看懂问题在"算"还是"控"
- ✅ 不影响现有能力，不引入新风险

---

**版本：** v0.5  
**最后更新：** 2025-01-12
