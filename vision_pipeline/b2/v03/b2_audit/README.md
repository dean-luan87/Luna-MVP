# B2 v0.5 自动化验收脚本（Audit Runner）

## 设计原则

- 不依赖 B2 业务代码
- 只读 trace / timeline / config
- Fail Fast，不"宽容解释"

## 目录结构

```
b2_audit/
├── audit_runner.py          # 主入口
├── context.py               # 加载 trace / timeline
├── report.py                # 统一输出格式
├── rules/
│   ├── __init__.py
│   ├── base.py              # 抽象规则基类
│   ├── s1_gate.py           # Step 1: Gate 规则
│   ├── s2_evidence.py       # Step 2: Evidence 规则
│   ├── s3_trigger.py        # Step 3: Trigger 规则
│   ├── s4_impact.py         # Step 4: Impact 规则
│   ├── s5_b2c.py            # Step 5: B → C 规则
│   ├── s6_trace.py          # Step 6: Trace 规则
│   └── g_failfast.py        # 全局 Fail Fast 规则
└── README.md
```

## 使用方法

```bash
# 基本用法（只检查 trace）
python vision_pipeline/b2/v03/b2_audit/audit_runner.py \
    traces/b2_runtime_trace_v05.jsonl

# 完整验收（trace + timeline）
python vision_pipeline/b2/v03/b2_audit/audit_runner.py \
    traces/b2_runtime_trace_v05.jsonl \
    timeline.jsonl
```

## 验收规则

### 全局规则（Fail Fast）
- G.FAIL.001: 世界语义残留检测

### Step 1: Gate（4 个规则）
- S1.GATE.001: Gate 是否为第一步
- S1.GATE.002: Gate Mode 合法性
- S1.GATE.003: Gate 阻断一致性
- S1.GATE.004: 抗视角污染字段完整性

### Step 2: Evidence（2 个规则）
- S2.EVIDENCE.001: 禁止瞬时证据
- S2.EVIDENCE.002: 生命周期合法性

### Step 3: Trigger（2 个规则）
- S3.TRIGGER.001: Trigger 显式存在
- S3.TRIGGER.002: Gate 控制 Trigger

### Step 4: Impact（3 个规则）
- S4.IMPACT.001: Impact 枚举封闭性
- S4.IMPACT.002: ENV 禁止直接影响
- S4.IMPACT.003: FORCE_ALERT 权限约束

### Step 5: B → C（2 个规则）
- S5.B2C.002: NO_OP 不得通信
- S5.B2C.003: FORCE_ALERT 可打断

### Step 6: Trace（1 个规则）
- S6.TIMELINE.001: Timeline 去噪

**总计**: 15 个验收规则

## 输出

### 控制台输出
- 实时显示失败的规则
- 最终统计报告（通过/警告/失败）

### JSON 报告
- 保存到 `b2_audit_report.json`
- 包含所有检查结果和证据

## 退出码

- 0: 所有检查通过
- 1: 存在失败项

## 重要提示

> B2 的任何改动，如果不能通过 Audit，一律视为"引入了不可控行为"。
