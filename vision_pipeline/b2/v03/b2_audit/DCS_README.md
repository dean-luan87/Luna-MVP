# B2 v0.5 设计一致性评分（DCS）使用指南

## 📊 什么是 DCS？

**设计一致性评分（Design Consistency Score, DCS）** 是一个 100 分制的评分系统，用于评估 B2 代码改动是否破坏了设计边界。

### 核心定位

- ✅ DCS 不是性能评分
- ✅ DCS 不评模型好坏
- ✅ DCS 只评一件事：**这次改动，有没有破坏 B2 / C / Gate 的设计边界**

## 🎯 评分结构

### 6 个维度（100 分制）

| 维度 | 分值 | 本质 |
|------|------|------|
| Gate 合规性 | 25 | 是否尊重现实（抗视角污染） |
| Evidence 合规性 | 15 | 是否尊重时间 |
| Trigger 正当性 | 15 | 是否克制 |
| Impact & 干预边界 | 20 | 是否越权 |
| Trace & 可追溯性 | 15 | 是否敢被审视 |
| Timeline 克制性 | 10 | 是否话多 |

### 评分等级

- ✅ **PASS** (≥ 85 分): 可以合并
- ⚠️  **FAIL** (70-84 分): 需要修复
- ❌ **ROLLBACK** (< 70 分): 强制回滚

## 📊 使用方法

### 基本用法

```bash
# 只运行自动化评分
python vision_pipeline/b2/v03/b2_audit/dcs_runner.py \
    traces/b2_runtime_trace_v05.jsonl

# 包含 timeline
python vision_pipeline/b2/v03/b2_audit/dcs_runner.py \
    traces/b2_runtime_trace_v05.jsonl \
    timeline.jsonl

# 包含人工评分
python vision_pipeline/b2/v03/b2_audit/dcs_runner.py \
    traces/b2_runtime_trace_v05.jsonl \
    timeline.jsonl \
    '{"gate": 20, "evidence": 12, "trigger": 15, "impact": 18, "trace": 14, "timeline": 8}'
```

### 输出示例

```
======================================================================
设计一致性评分（Design Consistency Score, DCS）
======================================================================

总分: 92 / 100
等级: ✅ PASS
及格线: 85 分
强制回滚线: 70 分

----------------------------------------------------------------------
维度得分:
----------------------------------------------------------------------
  gate         25 /  25  [████████████████████] 100%
  evidence     13 /  15  [██████████████░░░░░░] 87%
  trigger      15 /  15  [████████████████████] 100%
  impact       20 /  20  [████████████████████] 100%
  trace        14 /  15  [█████████████████░░░] 93%
  timeline      5 /  10  [█████████░░░░░░░░░░░░] 50%

----------------------------------------------------------------------
警告:
----------------------------------------------------------------------
  ⚠️  Evidence DEGRADED/DROPPED 逻辑覆盖率偏低
  ⚠️  Timeline 中发现 NO_OP 条目

======================================================================
✅ 设计一致性检查通过
======================================================================
```

### JSON 报告

报告保存到 `b2_dcs_report.json`，格式：

```json
{
  "design_consistency_score": 92,
  "grade": "PASS",
  "breakdown": {
    "gate": 25,
    "evidence": 13,
    "trigger": 15,
    "impact": 20,
    "trace": 14,
    "timeline": 5
  },
  "fatal_violations": [],
  "warnings": [
    "Evidence DEGRADED/DROPPED 逻辑覆盖率偏低",
    "Timeline 中发现 NO_OP 条目"
  ],
  "thresholds": {
    "pass": 85,
    "rollback": 70
  }
}
```

## 🔄 集成到 CI/CD

### GitHub Actions 示例

```yaml
name: B2 DCS Check

on: [pull_request]

jobs:
  dcs:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Run DCS
        run: |
          python vision_pipeline/b2/v03/b2_audit/dcs_runner.py \
            traces/b2_runtime_trace_v05.jsonl \
            timeline.jsonl
      
      - name: Check DCS Score
        run: |
          SCORE=$(jq -r '.design_consistency_score' b2_dcs_report.json)
          if [ "$SCORE" -lt 85 ]; then
            echo "❌ DCS 评分不足 85 分: $SCORE"
            exit 1
          fi
```

### PR 合并规则

- DCS < 85 → 禁止合并
- 任意 G 级违规 → 自动 FAIL

## 📝 PR 模板

使用 `PR_TEMPLATE_DCS.md` 作为 PR 模板，确保每次 PR 都进行 DCS 检查。

## 💡 评分规则详解

### 1. Gate 合规性（25 分）

**自动化（A）**
- Gate fail 时仍然 trigger → -25（直接 0 分）
- Gate 状态未写入 trace → -10

**人工（B）**
- PR 描述中是否明确 Gate 在本次改动中的角色
- 是否影响 stability_score / 阈值

### 2. Evidence 生命周期（15 分）

**自动化（A）**
- 单帧 CONFIRMED → -10
- 没有 DEGRADED / DROPPED → -5

**人工（B）**
- 能否回答："这条 evidence 什么时候会消失？"

### 3. Trigger 正当性（15 分）

**自动化（A）**
- Trigger 但 impact = NO_OP → -15
- 连续 trigger 无冷却 → -5

**人工（B）**
- PR 中是否能用一句话说明："如果 C 什么都不做，会发生什么？"

### 4. Impact & 干预边界（20 分）

**自动化（A）**
- 出现非标准 Impact 枚举 → -20
- B 对 C 下达非安全类"命令" → -20

**人工（B）**
- 是否明确：这是建议还是唯一允许的安全干预

### 5. Trace & 可追溯性（15 分）

**自动化（A）**
- 缺少 Gate / Trigger / Impact 任一 → -10
- NO_OP 无 reason → -5

**人工（B）**
- 是否能通过 trace 回答："为什么这一秒 B 没说话？"

### 6. Timeline 克制性（10 分）

**自动化（A）**
- NO_OP 写入 timeline → -10
- 高频重复同类事件 → -5

**人工（B）**
- Timeline 上的每一条，是否都会改变人的行为判断

## 🎯 长期价值

**DCS 趋势 = 系统是否在变"像人"还是"像机器"**

通过长期跟踪 DCS 趋势，可以：
- 发现设计偏移
- 评估系统成熟度
- 指导架构演进

## 💡 重要提示

> **你现在做的这套东西，不是"AI 系统"，而是：一个会被未来的你审判的系统。**
> 
> **DCS 的意义是：让未来的你，找得到现在的你为什么这么设计。**
