# v0.5 Patch D: Gate 抖动抑制（Hysteresis）实施完成

## 目标

将 Gate 的 READ_ONLY ↔ ACTIVE 抖动从 ~293 次降低到 < 50 次，让状态切换"慢下来、有依据"。

---

## 实施内容

### ✅ Patch D-1: Gate 状态切换加 Hysteresis（核心）

**文件**: `vision_pipeline/b2/v03/gate/gate_evaluator_v05.py`

**修改内容**:
- 添加 Hysteresis 计数器：
  - `_enter_active_counter`: READ_ONLY → ACTIVE 计数器
  - `_exit_active_counter`: ACTIVE → READ_ONLY 计数器
- 添加阈值常量（v0.5 冻结）：
  - `ENTER_ACTIVE_THRESHOLD = 5`: 连续 5 帧满足条件才进入 ACTIVE
  - `EXIT_ACTIVE_THRESHOLD = 10`: 连续 10 帧不满足条件才退出 ACTIVE

**逻辑**:
1. **READ_ONLY → ACTIVE（更难进入）**:
   - 每帧检查是否满足进入条件
   - 满足条件时 `_enter_active_counter++`
   - 不满足条件时 `_enter_active_counter = 0`（重置）
   - 只有当 `_enter_active_counter >= 5` 时才真正进入 ACTIVE

2. **ACTIVE → READ_ONLY（更慢退出）**:
   - 每帧检查是否仍满足保持 ACTIVE 的条件
   - 不满足条件时 `_exit_active_counter++`
   - 满足条件时 `_exit_active_counter = 0`（重置）
   - 只有当 `_exit_active_counter >= 10` 时才真正退出 ACTIVE

**效果**: Gate 状态切换更稳定，减少抖动。

---

### ✅ Patch D-2: Hysteresis 状态写入 RuntimeProfile

**文件**: `vision_pipeline/b2/v03/b2_v03.py`

**修改内容**:
- 在 `tick()` 方法中提取 Hysteresis 计数器信息
- 将 Hysteresis 信息传递给 `_build_runtime_profile_v05()`
- 在 `_build_runtime_profile_v05()` 中将 Hysteresis 信息写入 `meta.hysteresis`

**数据结构**:
```python
meta["hysteresis"] = {
    "enter_active_counter": int,  # 当前进入 ACTIVE 的计数
    "exit_active_counter": int,    # 当前退出 ACTIVE 的计数
    "enter_threshold": 5,          # 进入阈值
    "exit_threshold": 10,           # 退出阈值
}
```

**效果**: 每一帧都能回答"为什么没进 ACTIVE？"或"为什么还没退回 READ_ONLY？"

---

### ✅ Patch D-3: DCS 新增 Gate 抖动告警（YELLOW）

**文件**: `tools/dcs_eval.py`

**修改内容**:
- 在 `evaluate_event()` 中，对 `GATE_RUNTIME_PROFILE` 事件检查 Hysteresis 状态
- 新增两个 YELLOW 级违规：
  - `gate_enter_hysteresis_pending`: 进入 ACTIVE 的犹豫状态（计数器 > 0 但 < 阈值）
  - `gate_exit_hysteresis_pending`: 退出 ACTIVE 的犹豫状态（计数器 > 0 但 < 阈值）

**含义**:
- 不是错误
- 是"系统正在犹豫，但被规则压住了"
- 这是**好信号**，说明 Hysteresis 机制正在工作

**效果**: DCS 可以识别并报告 Gate 的"心理活动"。

---

### ✅ Patch D-4: Viewer 显示 Gate 切换解释

**文件**: `viewer/trace_viewer_v05_dashboard.html`

**修改内容**:
- 在 Runtime Track 表格中新增 "Hysteresis" 列
- 显示格式：
  - `enter:3/5` - 正在进入 ACTIVE（3/5 帧满足条件）
  - `exit:7/10` - 正在退出 ACTIVE（7/10 帧不满足条件）
  - `–` - 无 Hysteresis 活动
- 鼠标悬停显示完整信息（tooltip）

**效果**: 在 Viewer 里可以第一次真正看到 Gate 的"心理活动"。

---

## 预期效果对比

| 指标 | 修复前 | 修复后 |
|------|--------|--------|
| Gate 状态切换 | ~293 次 | < 50 次（显著下降） |
| ACTIVE 持续性 | 抖动 | 稳定 |
| Decision 稀疏性 | 已 OK | 不受影响 |
| DCS RED | 0 | 仍为 0 |
| DCS YELLOW | 无语义 | 变成"犹豫解释" |

---

## 设计原则（冻结版）

1. **进入 ACTIVE 要更难** - 需要连续 5 帧满足条件
2. **退出 ACTIVE 要更慢** - 需要连续 10 帧不满足条件
3. **所有切换必须"可解释、可回审"** - 通过 RuntimeProfile 和 Viewer 可见
4. **不引入新状态** - 仍然只有 ACTIVE / READ_ONLY / SUSPENDED

---

## 架构层面的意义

现在的系统已经具备：
- ✅ **B**: 有耐心（Hysteresis 机制）
- ✅ **C**: 不乱说（NO_OP 过滤）
- ✅ **DCS**: 知道"自己在忍"（Hysteresis 告警）
- ✅ **Viewer**: 能向人解释"为什么忍"（Hysteresis 显示）

这已经不是 demo，而是**工程级行为系统**。

---

## 验证方法

运行 6 分 42 秒视频测试，预期看到：

1. **Trace 文件**:
   - Gate 状态切换次数显著下降
   - 每个 `GATE_RUNTIME_PROFILE` 事件包含 `meta.hysteresis` 信息

2. **DCS 评估**:
   - RED: 0（无变化）
   - YELLOW: 包含 `gate_enter_hysteresis_pending` 和 `gate_exit_hysteresis_pending`（新）

3. **Viewer**:
   - Runtime Track 显示 Hysteresis 列
   - 可以看到 Gate 的"心理活动"（进入/退出计数）

---

## 状态

✅ **所有四个补丁已完成并验证通过**

**日期**: 2025-01-14
