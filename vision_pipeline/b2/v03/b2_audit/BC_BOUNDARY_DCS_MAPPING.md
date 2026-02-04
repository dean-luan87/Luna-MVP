# B/C Boundary Assumptions → DCS Rules Mapping

## 📊 DCS 评分维度定义

```
DCS_dimensions:
  - role_boundary
  - decision_semantics
  - intervention_scope
  - time_consistency
  - silence_validity
  - frequency_alignment
  - evolution_direction
```

## 🔍 每条裁定的 DCS 映射

### 裁定 1: 频率不同但同标尺

**DCS Rule:**
- **ID**: R1
- **Dimension**: `frequency_alignment`
- **Violation If:**
  - B attempts real_time_action
  - C attempts future_prediction
- **Penalty**: HIGH (-25)

**检查点:**
- B 输出中是否包含 "IMMEDIATE" / "REAL_TIME" / "URGENT"
- C 是否尝试长期预测

---

### 裁定 2: B 不自唤醒

**DCS Rule:**
- **ID**: R2
- **Dimension**: `role_boundary`
- **Violation If:**
  - B contains self_trigger_logic
  - B decides when to wake up
- **Penalty**: HIGH (-25)

**检查点:**
- Gate reason 中是否包含 "self" + "wake"/"trigger"
- B 是否包含自动调度逻辑

---

### 裁定 3: B 不确认风险

**DCS Rule:**
- **ID**: R3
- **Dimension**: `decision_semantics`
- **Violation If:**
  - confirmed_risk_language_detected
  - verification_claims
  - "must" / "enforce" language
- **Penalty**: CRITICAL (-50)

**检查点:**
- B 输出中是否包含 "confirmed" / "verified" / "must" / "enforce"
- 任何确认性语言

---

### 裁定 4: C 过度保守可接受

**DCS Rule:**
- **ID**: R4
- **Dimension**: `evolution_direction`
- **Violation If:**
  - attempts_to_optimize_c_aggressiveness_early
- **Penalty**: LOW (-5)

**说明:** 这是可接受的，不扣分或轻微扣分

---

### 裁定 5: 沉默无需解释

**DCS Rule:**
- **ID**: R5
- **Dimension**: `silence_validity`
- **Violation If:**
  - forced_user_explanation_for_NO_OP
  - NO_OP writes to timeline
  - NO_OP sends message to C
- **Penalty**: MEDIUM (-10)

**检查点:**
- NO_OP 是否写入 timeline
- NO_OP 是否发送消息给 C

---

### 裁定 6: 系统时间唯一

**DCS Rule:**
- **ID**: R6
- **Dimension**: `time_consistency`
- **Violation If:**
  - multiple_time_sources_used
  - missing system_ts in B→C message
- **Penalty**: CRITICAL (-50)

**检查点:**
- B→C 消息是否包含 system_ts
- 是否使用 camera_time / perception_time 等

---

### 裁定 7: 进化方向分离

**DCS Rule:**
- **ID**: R7
- **Dimension**: `evolution_direction`
- **Violation If:**
  - capability_substitution_detected
  - B doing C's job (execution)
  - C doing B's job (prediction)
- **Penalty**: HIGH (-25)

**检查点:**
- B 是否尝试执行（C 的职责）
- C 是否尝试预测（B 的职责）

---

## 📊 DCS 总评分逻辑

```yaml
DCS_scoring:
  initial_score: 100
  penalties:
    LOW: -5
    MEDIUM: -10
    HIGH: -25
    CRITICAL: -50
  thresholds:
    healthy: ">=85"
    warning: "70-84"
    broken: "<70"
```

### 评分计算

1. 初始分数: 100
2. 对每个违规规则，按 penalty 扣分
3. 每个规则最多扣 5 次（防止单规则过度扣分）
4. 最终分数 = max(0, 100 - 总扣分)

### 等级判定

- **HEALTHY** (≥ 85): 边界一致性良好
- **WARNING** (70-84): 边界一致性警告
- **BROKEN** (< 70): 边界一致性严重违规

---

## 🔧 实现位置

- **规则定义**: `vision_pipeline/b2/v03/b2_audit/rules/bc_boundary_rules.py`
- **评分器**: `vision_pipeline/b2/v03/b2_audit/dcs_boundary_scorer.py`
- **集成**: `vision_pipeline/b2/v03/b2_audit/audit_runner.py`

---

## 📝 使用示例

```python
from b2_audit.dcs_boundary_scorer import DCSBoundaryScorer
from b2_audit.context import AuditContext
from b2_audit.audit_runner import run_audit

# 运行审计（包含边界规则）
audit_report = run_audit(trace_path, timeline_path)
ctx = AuditContext(trace_path, timeline_path)

# 计算边界 DCS
boundary_scorer = DCSBoundaryScorer(ctx, audit_report)
result = boundary_scorer.calculate()
boundary_scorer.print_report(result)
```

---

**Version:** v1  
**Last Updated:** 2025-01-12
