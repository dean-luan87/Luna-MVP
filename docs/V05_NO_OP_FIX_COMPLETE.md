# v0.5 NO_OP 污染修复完成报告

## 修复目标（已全部达成）

✅ **1. RuntimeProfile 全量**：每帧都有 Gate / C runtime profile（用于健康监控与追溯）  
✅ **2. Decision 极稀疏**：只有"需要提醒/干预"才写 tick 事件  
✅ **3. NO_OP 完全沉默**：NO_OP 不进入 decision track、不进入 timeline、不触发 DCS 红牌  
✅ **4. DCS 分流审判**：RuntimeProfile 用 runtime 规则审；Decision 用 authority/overreach 规则审  
✅ **5. Viewer 明确分轨**：Runtime Track vs Decision Track 清晰分开，避免误解

---

## 修复前 vs 修复后对比

### 修复前（问题状态）

```
Trace 记录数: 32,156
  - GATE_RUNTIME_PROFILE: 12,048
  - C_RUNTIME_PROFILE: 12,048
  - tick: 8,060 (全部 NO_OP)

DCS 评估:
  - RED: 8,060 (NO_OP tick 被误判为违规)
  - YELLOW: 12,048
  - GREEN: 12,048

问题：
  - NO_OP tick 泛滥，污染 trace
  - DCS 用决策规则审判 NO_OP，造成 RED 洪水
  - Viewer 被 NO_OP 决策污染
```

### 修复后（目标状态）

```
Trace 记录数: 24,096
  - GATE_RUNTIME_PROFILE: 12,048 (50.0%)
  - C_RUNTIME_PROFILE: 12,048 (50.0%)
  - tick: 0 (NO_OP 已被过滤)

DCS 评估:
  - RED: 0 (没有 NO_OP tick 导致的 RED 洪水)
  - YELLOW: 12,048 (Runtime Profile 的运行态警告)
  - GREEN: 12,048 (Runtime Profile 正常运行)

结果：
  ✅ NO_OP tick 完全过滤
  ✅ DCS 正确分流（Runtime vs Decision）
  ✅ Viewer 双轨清晰（Runtime Track 密集，Decision Track 稀疏）
```

---

## 修复方案实施（三个补丁）

### ✅ Patch A: Trace 生成脚本 - NO_OP 不写 tick

**文件**: `vision_pipeline/b2/v03/b2_v03.py`

**修改内容**:

1. **提前返回，不写 NO_OP tick**:
   - `tick_rate_too_fast` → 不写 tick（只有 Runtime Profile）
   - `SUSPENDED` → 不写 tick（只有 Runtime Profile）
   - `compute_level NONE` → 不写 tick（只有 Runtime Profile）
   - `READ_ONLY` → 不写 tick（只有 Runtime Profile）
   - `state_gate_blocked` → 不写 tick（只有 Runtime Profile）
   - `insufficient_window_data` → 不写 tick（只有 Runtime Profile）

2. **确保所有事件都有 event_type**:
   - `GATE_RUNTIME_PROFILE` 事件：已有 `event_type: "GATE_RUNTIME_PROFILE"`
   - `tick` 事件：已有 `event_type: "tick"`（但 NO_OP 不写）

**验证**:
- ✅ Trace 文件：24,096 条记录，全部是 Runtime Profile
- ✅ Tick 事件数：0（NO_OP 已被过滤）

---

### ✅ Patch B: DCS - 按事件类型分流审判

**文件**: `tools/dcs_eval.py`

**修改内容**:

1. **按 event_type 分流**:
   - `tick` → Decision Rules
   - `GATE_RUNTIME_PROFILE` / `C_RUNTIME_PROFILE` → Runtime Rules

2. **NO_OP tick 直接 SKIP**:
   ```python
   if event_type == "tick":
       impact = safe_get(event, "impact.impact") or ...
       if impact == "NO_OP":
           return {"violations": [], "grade": "GREEN", "is_no_op": True}
   ```

3. **RuntimeProfile 规则只做调度违规检查**:
   - 仅检查运行态相关规则（调度异常、状态不一致等）
   - 不检查 impact、decision_level 等决策相关规则

4. **统计时跳过 NO_OP**:
   - NO_OP tick 不计入 R/Y/G 统计

**验证**:
- ✅ DCS RED: 0（没有 NO_OP tick 导致的 RED 洪水）
- ✅ DCS YELLOW: 12,048（Runtime Profile 的运行态警告）
- ✅ DCS GREEN: 12,048（Runtime Profile 正常运行）

---

### ✅ Patch C: Viewer - 三类事件明确分轨

**文件**: `viewer/trace_viewer_v05_dashboard.html`

**修改内容**:

1. **三条轨布局**:
   - **Track 1: Gate Runtime** - 显示 B Gate 状态
   - **Track 2: C Runtime** - 显示 C Control 状态
   - **Track 3: Decision** - 只显示 impact != NO_OP 的 tick

2. **Decision Track 默认过滤 NO_OP**:
   ```javascript
   if (isDecisionEvent) {
       const impact = obj.impact?.impact || ...;
       if (impact === "NO_OP") {
           return;  // 跳过，不添加到 Decision Track
       }
       // 只显示非 NO_OP 的决策
   }
   ```

3. **增加仪表盘指标**:
   - Decision Count（有意义决策 / 总决策数）
   - Decision Density（决策密度百分比）
   - Gate 状态分布
   - DCS 汇总

**验证**:
- ✅ Runtime Track：24,096 条记录（密集，健康监控）
- ✅ Decision Track：0 条记录（稀疏，真正提醒）
- ✅ 不会出现"NO_OP 也占满时间轴"的假象

---

## 验收标准验证

### ✅ 必须满足的数值形态

| 指标 | 要求 | 实际结果 | 状态 |
|------|------|----------|------|
| tick 事件数（impact!=NO_OP） | 应接近 0 | 0 | ✅ |
| tick 事件数（NO_OP） | 必须为 0 | 0 | ✅ |
| DCS RED | 不应因 NO_OP/tick 泛滥而爆红 | 0 | ✅ |
| RuntimeProfile | 每帧都有 | 24,096 条（12,048 帧 × 2） | ✅ |

### ✅ 必须满足的语义形态

- ✅ Viewer 上 Runtime Track 很密（健康监控）
- ✅ Viewer 上 Decision Track 很稀（真正提醒）
- ✅ 不会出现"NO_OP 也占满时间轴"的假象

---

## 完整测试结果（6分42秒视频）

### Trace 文件统计

```
总记录数: 24,096
事件类型分布:
  C_RUNTIME_PROFILE: 12,048 (50.0%)
  GATE_RUNTIME_PROFILE: 12,048 (50.0%)
  tick: 0 (NO_OP 已被过滤)
```

### DCS 评估结果

```
Total: 24,096
RED: 0
YELLOW: 12,048 (Runtime Profile 运行态警告)
GREEN: 12,048 (Runtime Profile 正常运行)
```

### Runtime 健康报告

```
B Gate 状态分布:
  ACTIVE: 11,930 (99.0%)
  READ_ONLY: 118 (1.0%)
  SUSPENDED: 0 (0.0%)

C Control 状态分布:
  ACTIVE: 12,048 (100.0%)
  DEGRADED: 0 (0.0%)
  SUSPENDED: 0 (0.0%)

Decision 稀疏度:
  决策事件总数: 0
  NO_OP: 0
  有意义决策: 0
  👉 结论: 合理 - 没有强证据，不乱提醒（安全优先）
```

---

## 修复文件清单

1. **`vision_pipeline/b2/v03/b2_v03.py`**
   - Patch A: 提前返回，不写 NO_OP tick

2. **`tools/dcs_eval.py`**
   - Patch B: 按事件类型分流，NO_OP tick 直接 skip

3. **`viewer/trace_viewer_v05_dashboard.html`**
   - Patch C: Decision Track 默认过滤 NO_OP，增加仪表盘指标

---

## 核心原则（已冻结）

从 v0.5 起：
1. **Runtime Profile 是一级公民** - 每帧都写，用于健康监控
2. **NO_OP 完全沉默** - 不写 tick 事件，不进入 Decision Track
3. **DCS 分流审判** - Runtime 用 runtime 规则，Decision 用 decision 规则
4. **Viewer 明确分轨** - Runtime Track 密集，Decision Track 稀疏

任何违反这四条的工具或逻辑，一律视为错误实现。

---

## 测试命令

```bash
# 1. 生成 trace（NO_OP 不写 tick）
python3 tools/run_v05_video_test.py

# 2. DCS 评估（NO_OP tick 被 skip）
python3 tools/dcs_eval.py traces/b2_v05_video_trace.jsonl

# 3. Runtime 健康报告
python3 tools/run_v05_audit_report.py traces/b2_v05_video_trace.jsonl

# 4. 打开 Viewer（双轨时间轴）
open viewer/trace_viewer_v05_dashboard.html
```

---

**修复完成时间**: 2025-01-14  
**版本**: v0.5  
**状态**: ✅ 修复完成并验证通过
