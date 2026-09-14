# B2 v0.5 Audit Runner 使用指南

## 快速开始

```bash
# 基本用法
python vision_pipeline/b2/v03/validation/audit_runner.py \
    traces/b2_runtime_trace_v05.jsonl

# 完整验收（包含 timeline）
python vision_pipeline/b2/v03/validation/audit_runner.py \
    traces/b2_runtime_trace_v05.jsonl \
    timeline.jsonl \
    12048
```

## 验收规则总览

### Step 1: Gate（4 个规则）
- S1.GATE.001: Gate 是否为第一步
- S1.GATE.002: Gate Mode 合法性
- S1.GATE.003: Gate 阻断一致性
- S1.GATE.004: 抗视角污染字段完整性

### Step 2: Evidence（3 个规则）
- S2.EVIDENCE.001: 禁止瞬时证据
- S2.EVIDENCE.002: 生命周期合法性
- S2.EVIDENCE.003: 生命周期单向性

### Step 3: Trigger（2 个规则）
- S3.TRIGGER.001: Trigger 显式存在
- S3.TRIGGER.002: Gate 控制 Trigger

### Step 4: Impact（3 个规则）
- S4.IMPACT.001: Impact 枚举封闭性
- S4.IMPACT.002: ENV 禁止直接影响
- S4.IMPACT.003: FORCE_ALERT 权限约束

### Step 5: B → C（3 个规则）
- S5.B2C.001: 单一出口
- S5.B2C.002: NO_OP 不得通信
- S5.B2C.003: FORCE_ALERT 可打断

### Step 6: Trace（2 个规则）
- S6.TRACE.001: Trace 全覆盖
- S6.TIMELINE.001: Timeline 去噪

### Step 7: Web（1 个规则）
- S7.WEB.001: 前端只读 trace

### Global（1 个规则）
- G.FAIL.001: 世界语义残留检测

**总计**: 20 个验收规则

## 输出说明

### 控制台输出
- ✅ 通过: 规则检查通过
- ⚠️ 警告: 规则检查有警告
- ❌ 失败: 规则检查失败

### JSON 报告
报告保存到 `b2_audit_report.json`，包含：
- `stats`: 统计信息（总检查项、通过、警告、失败）
- `results`: 所有检查结果详情

## 集成到 CI/CD

```yaml
# .github/workflows/b2_audit.yml
name: B2 v0.5 Audit

on: [push, pull_request]

jobs:
  audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run B2 Audit
        run: |
          python vision_pipeline/b2/v03/validation/audit_runner.py \
            traces/b2_runtime_trace_v05.jsonl \
            timeline.jsonl \
            12048
```

## 验收标准

**通过条件**: 所有规则检查通过（失败数 = 0）

**失败条件**: 存在任何 FAIL 状态的规则

## 重要提示

> B2 的任何改动，如果不能通过 Audit，一律视为"引入了不可控行为"。
