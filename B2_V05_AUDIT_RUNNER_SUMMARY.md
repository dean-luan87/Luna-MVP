# B2 v0.5 自动化验收脚本（Audit Runner）总结

## ✅ 已完成

### 1. 规则模块实现

#### Step 1: Gate 规则
- **文件**: `vision_pipeline/b2/v03/validation/rules/s1_gate.py`
- **规则**:
  - S1.GATE.001: Gate 是否为第一步
  - S1.GATE.002: Gate Mode 合法性
  - S1.GATE.003: Gate 阻断一致性
  - S1.GATE.004: 抗视角污染字段完整性

#### Step 2: Evidence 规则
- **文件**: `vision_pipeline/b2/v03/validation/rules/s2_evidence.py`
- **规则**:
  - S2.EVIDENCE.001: 禁止瞬时证据
  - S2.EVIDENCE.002: 生命周期合法性
  - S2.EVIDENCE.003: 生命周期单向性

#### Step 3: Trigger 规则
- **文件**: `vision_pipeline/b2/v03/validation/rules/s3_trigger.py`
- **规则**:
  - S3.TRIGGER.001: Trigger 显式存在
  - S3.TRIGGER.002: Gate 控制 Trigger

#### Step 4: Impact 规则
- **文件**: `vision_pipeline/b2/v03/validation/rules/s4_impact.py`
- **规则**:
  - S4.IMPACT.001: Impact 枚举封闭性
  - S4.IMPACT.002: ENV 禁止直接影响
  - S4.IMPACT.003: FORCE_ALERT 权限约束

#### Step 5: B → C 通信规则
- **文件**: `vision_pipeline/b2/v03/validation/rules/s5_b2c.py`
- **规则**:
  - S5.B2C.001: 单一出口
  - S5.B2C.002: NO_OP 不得通信
  - S5.B2C.003: FORCE_ALERT 可打断

#### Step 6: Trace / Timeline 规则
- **文件**: `vision_pipeline/b2/v03/validation/rules/s6_trace.py`
- **规则**:
  - S6.TRACE.001: Trace 全覆盖
  - S6.TIMELINE.001: Timeline 去噪

#### Step 7: Web 可视化规则
- **文件**: `vision_pipeline/b2/v03/validation/rules/s7_web.py`
- **规则**:
  - S7.WEB.001: 前端只读 trace

#### 全局规则
- **文件**: `vision_pipeline/b2/v03/validation/rules/global_rules.py`
- **规则**:
  - G.FAIL.001: 世界语义残留检测

### 2. Audit Runner 实现
- **文件**: `vision_pipeline/b2/v03/validation/audit_runner.py`
- **功能**:
  - 加载 trace 和 timeline 文件
  - 运行所有验收规则
  - 生成验收报告（控制台 + JSON）

## 📊 使用方法

```bash
# 基本用法（只检查 trace）
python vision_pipeline/b2/v03/validation/audit_runner.py \
    traces/b2_runtime_trace_v05.jsonl

# 完整验收（trace + timeline + 总帧数）
python vision_pipeline/b2/v03/validation/audit_runner.py \
    traces/b2_runtime_trace_v05.jsonl \
    timeline.jsonl \
    12048
```

## 🎯 输出格式

### 控制台输出
- 实时显示失败的规则
- 最终统计报告（通过/警告/失败）

### JSON 报告
- 保存到 `b2_audit_report.json`
- 包含所有检查结果和证据

## 🔄 集成到 CI/CD

```yaml
# .github/workflows/b2_audit.yml
- name: Run B2 v0.5 Audit
  run: |
    python vision_pipeline/b2/v03/validation/audit_runner.py \
      traces/b2_runtime_trace_v05.jsonl \
      timeline.jsonl \
      12048
```

## 📝 验收规则总览

### 规则数量
- Step 1 (Gate): 4 个规则
- Step 2 (Evidence): 3 个规则
- Step 3 (Trigger): 2 个规则
- Step 4 (Impact): 3 个规则
- Step 5 (B → C): 3 个规则
- Step 6 (Trace): 2 个规则
- Step 7 (Web): 1 个规则
- Global: 1 个规则

**总计**: 20 个验收规则

## 🎯 下一步

1. 运行验收脚本检查现有 trace
2. 根据验收结果修复不符合项
3. 集成到 CI/CD 流程
4. 每次代码变更前自动运行
