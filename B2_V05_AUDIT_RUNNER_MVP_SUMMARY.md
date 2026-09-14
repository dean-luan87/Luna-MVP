# B2 v0.5 自动化验收脚本（MVP）总结

## ✅ 已完成

### 1. 目录结构

```
vision_pipeline/b2/v03/b2_audit/
├── audit_runner.py          # 主入口
├── context.py               # 加载 trace / timeline
├── report.py                # 统一输出格式
├── rules/
│   ├── __init__.py
│   ├── base.py              # 抽象规则基类
│   ├── s1_gate.py           # Step 1: Gate 规则（4 个）
│   ├── s2_evidence.py       # Step 2: Evidence 规则（2 个）
│   ├── s3_trigger.py        # Step 3: Trigger 规则（2 个）
│   ├── s4_impact.py         # Step 4: Impact 规则（3 个）
│   ├── s5_b2c.py            # Step 5: B → C 规则（2 个）
│   ├── s6_trace.py          # Step 6: Trace 规则（1 个）
│   └── g_failfast.py        # 全局 Fail Fast 规则（1 个）
└── README.md
```

### 2. 核心组件

#### AuditRule 基类
- 抽象接口：`check(ctx) -> Optional[Dict]`
- 返回 `None` → PASS
- 返回 `dict` → FAIL / WARN

#### AuditContext
- 只读数据加载
- 支持 trace 和 timeline
- 自动处理 JSONL 格式

#### AuditReport
- 统一输出格式
- 控制台 + JSON 报告
- 统计信息

### 3. 验收规则总览

**总计**: 15 个验收规则

- **全局规则（Fail Fast）**: 1 个
  - G.FAIL.001: 世界语义残留检测

- **Step 1: Gate**: 4 个
  - S1.GATE.001: Gate 是否为第一步
  - S1.GATE.002: Gate Mode 合法性
  - S1.GATE.003: Gate 阻断一致性
  - S1.GATE.004: 抗视角污染字段完整性

- **Step 2: Evidence**: 2 个
  - S2.EVIDENCE.001: 禁止瞬时证据
  - S2.EVIDENCE.002: 生命周期合法性

- **Step 3: Trigger**: 2 个
  - S3.TRIGGER.001: Trigger 显式存在
  - S3.TRIGGER.002: Gate 控制 Trigger

- **Step 4: Impact**: 3 个
  - S4.IMPACT.001: Impact 枚举封闭性
  - S4.IMPACT.002: ENV 禁止直接影响
  - S4.IMPACT.003: FORCE_ALERT 权限约束

- **Step 5: B → C**: 2 个
  - S5.B2C.002: NO_OP 不得通信
  - S5.B2C.003: FORCE_ALERT 可打断

- **Step 6: Trace**: 1 个
  - S6.TIMELINE.001: Timeline 去噪

## 📊 使用方法

```bash
# 基本用法（只检查 trace）
cd vision_pipeline/b2/v03/b2_audit
python audit_runner.py ../../../../traces/b2_runtime_trace_v05.jsonl

# 完整验收（trace + timeline）
python audit_runner.py \
    ../../../../traces/b2_runtime_trace_v05.jsonl \
    ../../../../timeline.jsonl
```

## 🎯 输出格式

### 控制台输出
```
======================================================================
B2 v0.5 自动化验收
======================================================================
Trace 文件: traces/b2_runtime_trace_v05.jsonl

加载了 12048 条 trace 记录

运行验收规则...

======================================================================
B2 v0.5 自动化验收报告
======================================================================

总检查项: 180720
✅ 通过: 180705
⚠️  警告: 10
❌ 失败: 5

失败项详情:
----------------------------------------------------------------------

❌ S1.GATE.001: gate_eval 缺失
   Trace Index: 1234
   Frame ID: 1234
   时间: 00:41.234

======================================================================
❌ AUDIT FAILED
======================================================================
```

### JSON 报告
保存到 `b2_audit_report.json`，包含：
- `stats`: 统计信息
- `failures`: 失败项详情
- `warnings`: 警告项详情

## 🔄 退出码

- `0`: 所有检查通过
- `1`: 存在失败项

## 🎯 设计特点

1. **Fail Fast**: 全局规则失败时立即停止
2. **只读数据**: 不依赖 B2 业务代码
3. **精确定位**: 每条失败都有 trace_index / frame_id
4. **可扩展**: 新增规则只需实现 `AuditRule` 接口

## 📝 下一步

1. 运行验收脚本检查现有 trace
2. 根据验收结果修复不符合项
3. 集成到 CI/CD 流程
4. 每次代码变更前自动运行

## 💡 重要提示

> B2 的任何改动，如果不能通过 Audit，一律视为"引入了不可控行为"。
